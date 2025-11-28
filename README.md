# 🛒 Day 7 — Food & Grocery Ordering Voice Agent

For **Day 7 of the Murf AI Voice Agents Challenge**, I built a **food & grocery ordering voice agent** for a fictional quick-commerce store.

The agent allows users to order groceries and prepared food via natural voice conversation, maintains a live cart, and places the order by saving it to a **database-backed order record**.

---

## 🎯 Primary Objective

Build a voice assistant that can:
- Understand grocery and food orders
- Maintain a cart across the conversation
- Intelligently handle “ingredients for X” requests
- Persist the final order when the user is done

✅ All Day-7 primary goals are completed using a database for persistence.

---

## 🗂 Catalog & Data

- A structured **catalog** is stored in the database, covering:
  - Groceries (bread, milk, eggs, etc.)
  - Snacks
  - Prepared foods
- Each item includes:
  - Name
  - Category
  - Price
  - Optional attributes (size, tags, etc.)

---

## 🧠 Agent Capabilities

### 🛍 Cart Management
The agent can:
- Add items with quantity
- Remove items
- Update quantities
- List current cart contents
- Verbally confirm every cart update

### 🥪 Intelligent “Ingredients for X”
The agent understands high-level requests such as:
- “Ingredients for a peanut butter sandwich”
- “What I need to cook pasta for two”

It maps these requests to multiple catalog items and adds them together to the cart, confirming the action verbally.

---

## ✅ Order Placement & Persistence

When the user says:
- “That’s all”
- “Place my order”
- “I’m done”

The agent:
1. Confirms final cart contents and total
2. Creates an order object with:
   - Items & quantities
   - Prices and total
   - Timestamp
3. Saves the order to the **database**
4. Confirms that the order has been successfully placed

---

## 🧩 Tech Stack

- LiveKit Agents (voice orchestration)
- Murf Falcon (natural TTS)
- LLM-based intent understanding
- Database-backed catalog and orders

---

## ✅ Day 7 Status

- Catalog creation ✅  
- Cart management ✅  
- Ingredient-based ordering ✅  
- Order persistence in database ✅  

✅ **Day 7 Primary Goal Completed**
---

## 🎯 Primary Objective

Build a **voice-based SDR agent** that:
- Behaves like a representative of a specific company
- Answers FAQ questions accurately (no hallucinations)
- Collects lead information during the conversation
- Saves the lead data at the end of the call

✅ All required Day-5 goals are completed.

---

## 🎯 Core Objectives Completed

- Built a **voice-first learning experience**
- Implemented **three learning modes**, switchable by voice at any time
- Used **Murf Falcon TTS** with **different voice personas per mode**
- Added **JSON-driven concept library**
- Tracked **concept-level mastery and progress over time**

---

## 🧠 Learning Modes + Voice Personas

| Mode | Purpose | Murf Falcon Voice | Personality |
|------|---------|------------------|-------------|
| `learn` | Agent explains the concept | **Matthew** | Calm & encouraging |
| `quiz` | Agent asks questions to test understanding | **Alicia** | Energetic quiz master |
| `teach_back` | User explains the concept back | **Ken** | Supportive coach, reflective |

🔄 The user can switch modes *at any time* by simply speaking:
> “Let’s switch to quiz mode”  
> “Can I do teach-back now?”  
> “I want to learn instead”

Voice switching happens **dynamically in real time** without restarting the session.

---

More updates will be pushed day by day.
---


# AI Voice Agents Challenge - Starter Repository

Welcome to the **AI Voice Agents Challenge** by [murf.ai](https://murf.ai)!

## About the Challenge

We just launched **Murf Falcon** – the consistently fastest TTS API, and you're going to be among the first to test it out in ways never thought before!

**Build 10 AI Voice Agents over the course of 10 Days** along with help from our devs and the community champs, and win rewards!

### How It Works

- One task to be provided everyday along with a GitHub repo for reference
- Build a voice agent with specific personas and skills
- Post on GitHub and share with the world on LinkedIn!

## Repository Structure

This is a **monorepo** that contains both the backend and frontend for building voice agent applications. It's designed to be your starting point for each day's challenge task.

```
falcon-tdova-nov25-livekit/
├── backend/          # LiveKit Agents backend with Murf Falcon TTS
├── frontend/         # React/Next.js frontend for voice interaction
├── start_app.sh      # Convenience script to start all services
└── README.md         # This file
```

### Backend

The backend is based on [LiveKit's agent-starter-python](https://github.com/livekit-examples/agent-starter-python) with modifications to integrate **Murf Falcon TTS** for ultra-fast, high-quality voice synthesis.

**Features:**

- Complete voice AI agent framework using LiveKit Agents
- Murf Falcon TTS integration for fastest text-to-speech
- LiveKit Turn Detector for contextually-aware speaker detection
- Background voice cancellation
- Integrated metrics and logging
- Complete test suite with evaluation framework
- Production-ready Dockerfile

[→ Backend Documentation](./backend/README.md)

### Frontend

The frontend is based on [LiveKit's agent-starter-react](https://github.com/livekit-examples/agent-starter-react), providing a modern, beautiful UI for interacting with your voice agents.

**Features:**

- Real-time voice interaction with LiveKit Agents
- Camera video streaming support
- Screen sharing capabilities
- Audio visualization and level monitoring
- Light/dark theme switching
- Highly customizable branding and UI

[→ Frontend Documentation](./frontend/README.md)

## Quick Start

### Prerequisites

Make sure you have the following installed:

- Python 3.9+ with [uv](https://docs.astral.sh/uv/) package manager
- Node.js 18+ with pnpm
- [LiveKit CLI](https://docs.livekit.io/home/cli/cli-setup) (optional but recommended)
- [LiveKit Server](https://docs.livekit.io/home/self-hosting/local/) for local development

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd falcon-tdova-nov25-livekit
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
uv sync

# Copy environment file and configure
cp .env.example .env.local

# Edit .env.local with your credentials:
# - LIVEKIT_URL
# - LIVEKIT_API_KEY
# - LIVEKIT_API_SECRET
# - MURF_API_KEY (for Falcon TTS)
# - GOOGLE_API_KEY (for Gemini LLM)
# - DEEPGRAM_API_KEY (for Deepgram STT)

# Download required models
uv run python src/agent.py download-files
```

For LiveKit Cloud users, you can automatically populate credentials:

```bash
lk cloud auth
lk app env -w -d .env.local
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
pnpm install

# Copy environment file and configure
cp .env.example .env.local

# Edit .env.local with the same LiveKit credentials
```

### 4. Run the Application

#### Install livekit server

```bash
brew install livekit
```

You have two options:

#### Option A: Use the convenience script (runs everything)

```bash
# From the root directory
chmod +x start_app.sh
./start_app.sh
```

This will start:

- LiveKit Server (in dev mode)
- Backend agent (listening for connections)
- Frontend app (at http://localhost:3000)

#### Option B: Run services individually

```bash
# Terminal 1 - LiveKit Server
livekit-server --dev

# Terminal 2 - Backend Agent
cd backend
uv run python src/agent.py dev

# Terminal 3 - Frontend
cd frontend
pnpm dev
```

Then open http://localhost:3000 in your browser!

## Daily Challenge Tasks

Each day, you'll receive a new task that builds upon your voice agent. The tasks will help you:

- Implement different personas and conversation styles
- Add custom tools and capabilities
- Integrate with external APIs
- Build domain-specific agents (customer service, tutoring, etc.)
- Optimize performance and user experience

**Stay tuned for daily task announcements!**

## Documentation & Resources

- [Murf Falcon TTS Documentation](https://murf.ai/api/docs/text-to-speech/streaming)
- [LiveKit Agents Documentation](https://docs.livekit.io/agents)
- [Original Backend Template](https://github.com/livekit-examples/agent-starter-python)
- [Original Frontend Template](https://github.com/livekit-examples/agent-starter-react)

## Testing

The backend includes a comprehensive test suite:

```bash
cd backend
uv run pytest
```

Learn more about testing voice agents in the [LiveKit testing documentation](https://docs.livekit.io/agents/build/testing/).

## Contributing & Community

This is a challenge repository, but we encourage collaboration and knowledge sharing!

- Share your solutions and learnings on GitHub
- Post about your progress on LinkedIn
- Join the [LiveKit Community Slack](https://livekit.io/join-slack)
- Connect with other challenge participants

## License

This project is based on MIT-licensed templates from LiveKit and includes integration with Murf Falcon. See individual LICENSE files in backend and frontend directories for details.

## Have Fun!

Remember, the goal is to learn, experiment, and build amazing voice AI agents. Don't hesitate to be creative and push the boundaries of what's possible with Murf Falcon and LiveKit!

Good luck with the challenge!

---

Built for the AI Voice Agents Challenge by murf.ai
