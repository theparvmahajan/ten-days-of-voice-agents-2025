import logging
from pathlib import Path
from typing import Any, List, Optional

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext,
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from .wellness_log import append_entry, load_log, summarize_last_entry


logger = logging.getLogger("agent")

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        # Load previous wellness history for this user (basic, file-based)
        history = load_log(base_dir=Path(__file__).resolve().parent.parent)
        last_summary = summarize_last_entry(history)

        # Build history context text to inject into system prompt
        if last_summary:
            history_text = (
                "Here is a brief summary of the last check-in for this user: "
                + last_summary
                + " Use this to compare how today feels versus last time, "
                  "and reference it softly in conversation."
            )
        else:
            history_text = (
                "There is no previous check-in logged yet. Treat this as the first one."
            )

        super().__init__(
            instructions=f"""
You are a supportive, grounded health and wellness voice companion.

Your role:
- Do brief daily check-ins about how the user is feeling and what they want to focus on.
- You are NOT a therapist or doctor. You MUST NOT diagnose conditions or give medical advice.
- If the user brings up serious distress or crisis, gently encourage them to seek support from a trusted person or professional.

Conversation flow for each check-in:
1. Ask about mood and energy in a natural way.
   - Examples: "How are you feeling today?" "What’s your energy like?" "Anything stressing you out?"
2. Ask about 1–3 intentions or objectives for today.
   - Examples: "What are 1–3 things you’d like to get done today?"
     "Is there anything you want to do for yourself — rest, exercise, hobbies?"
3. Offer small, realistic suggestions or reflections.
   - Examples: break big tasks into smaller steps, take short breaks,
     consider a 5-minute walk or simple self-care.
   - Keep advice very practical, non-medical, and non-diagnostic.
4. Close with a recap:
   - Briefly summarize mood/energy and the 1–3 main goals.
   - Ask: "Does this sound right?" and adjust if needed.

Persistence:
- When you have a clear sense of:
  - mood
  - energy
  - key stressors (if any)
  - main objectives (1–3)
  - self-care ideas (if any)
  and after you give your recap, CALL the `save_checkin` tool with those fields filled.
- Do not call the tool too early; only after you reach the recap stage.

Context from previous check-ins:
- {history_text}

Style:
- Calm, kind, encouraging, but realistic.
- Keep responses concise and conversational.
- Do not mention JSON, files, tools, or internal implementation details.
""".strip(),
        )

    # --------------- TOOLS --------------- #

    @function_tool()
    async def save_checkin(
        self,
        context: RunContext,
        mood: str,
        energy: str,
        stressors: str,
        objectives: List[str],
        self_care: List[str],
        recap_summary: str,
    ) -> dict[str, Any]:
        """
        Save the current day's wellness check-in to a JSON log.

        The LLM should call this AFTER it has:
        - asked about mood & energy
        - explored current stressors (if any)
        - collected 1–3 main objectives
        - suggested at least one simple self-care idea (if applicable)
        - given a brief recap to the user

        Args:
            mood: User's self-reported mood (short text, or simple scale like "3/5, okay but tired").
            energy: User's self-reported energy level.
            stressors: Short description of anything stressing the user.
            objectives: 1–3 concrete goals or intentions for today.
            self_care: Simple self-care or rest ideas the user mentioned or agreed to.
            recap_summary: One-sentence recap of today’s check-in.

        Returns:
            A dict with the stored entry.
        """

        logger.info(
            f"save_checkin called with mood={mood}, energy={energy}, "
            f"stressors={stressors}, objectives={objectives}, self_care={self_care}"
        )

        entry = append_entry(
            mood=mood,
            energy=energy,
            stressors=stressors,
            objectives=objectives,
            self_care=self_care,
            agent_summary=recap_summary,
            base_dir=Path(__file__).resolve().parent.parent,
        )

        return {
            "stored": True,
            "timestamp": entry.timestamp,
            "mood": entry.mood,
            "energy": entry.energy,
            "stressors": entry.stressors,
            "objectives": entry.objectives,
            "self_care": entry.self_care,
            "agent_summary": entry.agent_summary,
        }



def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Voice AI pipeline: Deepgram STT, Gemini LLM, Murf TTS, Silero VAD, LiveKit turn detector
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(
            model="gemini-2.5-flash",
        ),
        tts=murf.TTS(
            voice="en-US-matthew",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
