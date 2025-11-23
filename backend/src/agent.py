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

from .order_state import OrderState, save_order_to_file

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        brand_name = "Nebula Coffee Co."  # pick any brand name you like

        super().__init__(
            instructions=f"""
You are a friendly, efficient barista at {brand_name}.

The user is speaking to you via voice to place a coffee order.
We are tracking the order in a JSON object with these exact keys:

{{
  "drinkType": "string",
  "size": "string",
  "milk": "string",
  "extras": ["string"],
  "name": "string"
}}

Your job:
- Take ONE coffee order at a time.
- Ask clear follow-up questions until all of these fields are filled.
- Clarify anything ambiguous (e.g., "regular coffee" → ask about size and milk).
- Extras can be toppings/modifiers like "extra shot", "caramel", "whipped cream", "no sugar" etc.
- The name is the customer's name to write on the cup.

Tool usage:
- Whenever the customer mentions drink type, size, milk, extras, or name,
  CALL the `update_order` tool with whatever fields you can fill.
- When you are confident the order is complete, CALL the `finalize_order` tool.
- After `finalize_order`, briefly summarize the full order to the customer.

Conversation style:
- Warm, upbeat, like a real barista.
- Short, natural sentences.
- Never mention JSON, tools, or internal functions to the customer.
""".strip(),
        )

        # Simple per-session state for this agent
        self.order_state = OrderState()
        self._saved_once = False

    # ---------------- TOOLS ---------------- #

    @function_tool()
    async def update_order(
        self,
        context: RunContext,
        drinkType: Optional[str] = None,
        size: Optional[str] = None,
        milk: Optional[str] = None,
        extras: Optional[List[str]] = None,
        name: Optional[str] = None,
    ) -> dict[str, Any]:
        """
        Update the current coffee order based on new information from the customer.
        The LLM should call this whenever the user provides any part of their order.
        """

        logger.info(
            f"update_order called with: drinkType={drinkType}, size={size}, milk={milk}, extras={extras}, name={name}"
        )

        if drinkType is not None:
            self.order_state.drinkType = drinkType

        if size is not None:
            self.order_state.size = size

        if milk is not None:
            self.order_state.milk = milk

        if name is not None:
            self.order_state.name = name

        if extras is not None:
            # overwrite for simplicity; could also merge/extend
            self.order_state.extras = extras

        current = self.order_state.to_dict()
        missing = self.order_state.missing_fields()
        logger.info(f"Current order state: {current}, missing: {missing}")

        return {
            "order": current,
            "is_complete": self.order_state.is_complete(),
            "missing_fields": missing,
        }

    @function_tool()
    async def finalize_order(self, context: RunContext) -> dict[str, Any]:
        """
        Finalize the current order, save it to a JSON file, and return a summary.
        Only call this when the order is complete.
        """

        if not self.order_state.is_complete():
            missing = self.order_state.missing_fields()
            logger.warning(
                f"finalize_order called but order is incomplete. Missing: {missing}"
            )
            return {
                "error": "Order is not complete yet",
                "missing_fields": missing,
            }

        # Build a brief human-readable summary
        summary = (
            f"{self.order_state.size} {self.order_state.drinkType} "
            f"with {self.order_state.milk} milk"
        )
        if self.order_state.extras:
            summary += f", extras: {', '.join(self.order_state.extras)}"
        summary += f" for {self.order_state.name}"

        logger.info(f"Final order summary: {summary}")

        # Save only once per session to avoid duplicates
        if not self._saved_once:
            path = save_order_to_file(
                self.order_state,
                base_dir=Path(__file__).resolve().parent.parent,
                summary=summary,  # <-- pass summary into JSON
            )
            self._saved_once = True
            logger.info(f"Order saved to {path}")
        else:
            path = None

        return {
            "order": self.order_state.to_dict(),
            "saved_to": str(path) if path else None,
            "summary": summary,
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
