import logging
import json
import os
import asyncio
from typing import Annotated, Literal, Optional
from dataclasses import dataclass

print("🚀 DSA and AI TUTOR - DAY 4 TUTORIAL")
print("💡 agent.py LOADED SUCCESSFULLY!")

from dotenv import load_dotenv
from pydantic import Field
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    WorkerOptions,
    cli,
    function_tool,
    RunContext,
)

# 🔌 PLUGINS
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")
load_dotenv(".env.local")

CONTENT_FILE = "day4_tutor_content.json" 

DEFAULT_CONTENT = [
  {
    "id": "variables",
    "title": "Variables",
    "summary": "Variables store values so you can reuse them later. You give them a name, assign a value, and then you can use that name throughout your program.",
    "sample_question": "What is a variable and why is it useful when writing code?"
  },
  {
    "id": "loops",
    "title": "Loops",
    "summary": "Loops let you repeat an action multiple times without rewriting the same code.",
    "sample_question": "Explain the difference between a for loop and a while loop."
  },
  {
    "id": "linked_lists",
    "title": "Linked Lists",
    "summary": "A linked list is a linear data structure where each node stores a value and a pointer to the next node.",
    "sample_question": "What is a linked list, and when would you prefer it over an array?"
  },
  {
    "id": "basic_ai",
    "title": "Basic AI Concepts",
    "summary": "Artificial Intelligence is about building systems that can perform tasks that typically require human intelligence.",
    "sample_question": "In simple terms, what is Artificial Intelligence and where might you see it in everyday life?"
  },
  {
    "id": "genai",
    "title": "Generative AI",
    "summary": "Generative AI refers to models that can create new content such as text, images, or code based on patterns learned from data.",
    "sample_question": "What is Generative AI, and how is it different from traditional AI systems?"
  }
]


def load_content():

    try:
        path = os.path.join(os.path.dirname(__file__), CONTENT_FILE)
        
        # Check if file exists
        if not os.path.exists(path):
            print(f"⚠️ {CONTENT_FILE} not found. Generating AI data...")
            with open(path, "w", encoding='utf-8') as f:
                json.dump(DEFAULT_CONTENT, f, indent=4)
            print("✅ AI content file created successfully.")
            
        # Read the file
        with open(path, "r", encoding='utf-8') as f:
            data = json.load(f)
            return data
            
    except Exception as e:
        print(f"⚠️ Error managing content file: {e}")
        return []

# Load data immediately on startup
COURSE_CONTENT = load_content()


@dataclass
class TutorState:
    """🧠 Tracks the current learning context"""
    current_topic_id: str | None = None
    current_topic_data: dict | None = None
    mode: Literal["learn", "quiz", "teach_back"] = "learn"
    
    def set_topic(self, topic_id: str):
        # Find topic in loaded content
        topic = next((item for item in COURSE_CONTENT if item["id"] == topic_id), None)
        if topic:
            self.current_topic_id = topic_id
            self.current_topic_data = topic
            return True
        return False

@dataclass
class Userdata:
    tutor_state: TutorState
    agent_session: Optional[AgentSession] = None 


@function_tool
async def select_topic(
    ctx: RunContext[Userdata], 
    topic_id: Annotated[str, Field(description="The ID of the topic to study (e.g., 'loops', 'variables', 'genai')")]
) -> str:
    """📚 Selects a topic to study from the available list."""
    state = ctx.userdata.tutor_state
    success = state.set_topic(topic_id.lower())
    
    if success:
        return f"Topic set to {state.current_topic_data['title']}. Ask the user if they want to 'Learn', be 'Quizzed', or 'Teach it back'."
    else:
        available = ", ".join([t["id"] for t in COURSE_CONTENT])
        return f"Topic not found. Available topics are: {available}"

@function_tool
async def set_learning_mode(
    ctx: RunContext[Userdata], 
    mode: Annotated[str, Field(description="The mode to switch to: 'learn', 'quiz', or 'teach_back'")]
) -> str:
    """🔄 Switches the interaction mode and updates the agent's voice/persona."""
    
    # 1. Update State
    state = ctx.userdata.tutor_state
    state.mode = mode.lower()
    
    # 2. Switch Voice based on Mode
    agent_session = ctx.userdata.agent_session 
    
    if agent_session:
        if state.mode == "learn":
            # 👨‍🏫 MATTHEW: The Lecturer
            agent_session.tts.update_options(voice="en-US-matthew", style="Promo")
            instruction = f"Mode: LEARN. Explain: {state.current_topic_data['summary']}"
            
        elif state.mode == "quiz":
            # 👩‍🏫 ALICIA: The Examiner
            agent_session.tts.update_options(voice="en-US-alicia", style="Conversational")
            instruction = f"Mode: QUIZ. Ask this question: {state.current_topic_data['sample_question']}"
            
        elif state.mode == "teach_back":
            # 👨‍🎓 KEN: The Student/Coach
            agent_session.tts.update_options(voice="en-US-ken", style="Promo")
            instruction = "Mode: TEACH_BACK. Ask the user to explain the concept to you as if YOU are the beginner."
        else:
            return "Invalid mode."
    else:
        instruction = "Voice switch failed (Session not found)."

    print(f"🔄 SWITCHING MODE -> {state.mode.upper()}")
    return f"Switched to {state.mode} mode. {instruction}"

@function_tool
async def evaluate_teaching(
    ctx: RunContext[Userdata],
    user_explanation: Annotated[str, Field(description="The explanation given by the user during teach-back")]
) -> str:
    """📝 call this when the user has finished explaining a concept in 'teach_back' mode."""
    print(f"📝 EVALUATING EXPLANATION: {user_explanation}")
    return "Analyze the user's explanation. Give them a score out of 10 on accuracy and clarity, and correct any mistakes."

# ======================================================
# 🧠 AGENT DEFINITION
# ======================================================

class TutorAgent(Agent):
    def __init__(self):
        # Generate list of topics for the prompt
        topic_list = ", ".join([f"{t['id']} ({t['title']})" for t in COURSE_CONTENT])
        
        super().__init__(
            instructions=f"""
            You are an DSA and AI Tutor designed to help users master concepts like DNA and Cells.
            
            📚 **AVAILABLE TOPICS:** {topic_list}
            
            🔄 **YOU HAVE 3 MODES:**
            1. **LEARN Mode (Voice: Matthew):** You explain the concept clearly using the summary data.
            2. **QUIZ Mode (Voice: Alicia):** You ask the user a specific question to test knowledge.
            3. **TEACH_BACK Mode (Voice: Ken):** YOU pretend to be a student. Ask the user to explain the concept to you.
            
            ⚙️ **BEHAVIOR:**
            - Start by asking what topic they want to study.
            - Use the `set_learning_mode` tool immediately when the user asks to learn, take a quiz, or teach.
            - In 'teach_back' mode, listen to their explanation and then use `evaluate_teaching` to give feedback.
            """,
            tools=[select_topic, set_learning_mode, evaluate_teaching],
        )

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    ctx.log_context_fields = {"room": ctx.room.name}

    print("\n" + "🧬" * 25)
    print("🚀 STARTING TUTOR SESSION")
    print(f"📚 Loaded {len(COURSE_CONTENT)} topics from Knowledge Base")
    
    # 1. Initialize State
    userdata = Userdata(tutor_state=TutorState())

    # 2. Setup Agent
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-matthew", 
            style="Promo",        
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        userdata=userdata,
    )
    
    # 3. Store session in userdata for tools to access
    userdata.agent_session = session
    
    # 4. Start
    await session.start(
        agent=TutorAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )

    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))