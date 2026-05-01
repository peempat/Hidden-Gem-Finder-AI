<<<<<<< HEAD
# Hidden Gem Finder AI

> **Super AI Engineer Season 6** — Mini Hack Project

An AI-powered travel assistant that helps you discover hidden gems and plan trips across Thailand. Built on an **Agentic RAG** architecture — the agent automatically picks the right tools (crowd check, trend analysis, RAG knowledge base, web search) to give you real-time, context-aware travel recommendations.

---

## Architecture Overview

```
User → Chat Interface → Agent → LLM (Groq / LLaMA 3.3 70B)
                                     ↕
                                   Tools
                              ┌──────────────────────────┐
                              │ crowded_check             │ ← Estimate crowd level
                              │ trend_crowded_check       │ ← Year-round crowd trend
                              │ search_travel_info        │ ← Web travel search
                              │ agentic_nakhon_nayok_rag  │ ← Local RAG knowledge base
                              │ current_datetime          │ ← Real-time date/time
                              └──────────────────────────┘
```

- **Backend**: FastAPI + OpenAI-compatible client (Groq)
- **Frontend**: React + Vite + TailwindCSS
- **RAG**: Qdrant vector store for Nakhon Nayok hidden gem knowledge
- **LLM**: LLaMA 3.3 70B via Groq API (swappable via `.env`)

---

## Prerequisites

- Python 3.10+
- Node.js 18+
- API keys (see below)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-org>/Hidden-Gem-Finder-AI.git
cd Hidden-Gem-Finder-AI
```

### 2. Configure API keys

```bash
cd GemmyAI/backend
cp .env.example .env
```

Open `.env` and fill in your keys:

```env
# Required — LLM provider (Groq)
GROQ_API_KEY=your_groq_api_key_here
GROQ_BASE_URL=https://api.groq.com/openai/v1
GROQ_MODEL=llama-3.3-70b-versatile

# Required — for RAG embeddings
GEMINI_API_KEY=your_gemini_api_key_here

# Required — for weather/crowd data
OPENWEATHER_API_KEY=your_openweather_api_key_here

# Optional tuning
MAX_TOKENS=4096
TEMPERATURE=0
```

| Key | Where to get it |
|-----|----------------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) |
| `GEMINI_API_KEY` | [aistudio.google.com](https://aistudio.google.com) |
| `OPENWEATHER_API_KEY` | [openweathermap.org/api](https://openweathermap.org/api) |

---

### 3. Start the backend

```bash
cd GemmyAI/backend

# Create virtual environment (first time only)
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

---

### 4. Start the frontend

```bash
cd GemmyAI/frontend

# Install dependencies (first time only)
npm install

# Run dev server
npm run dev
```

Frontend will be available at `http://localhost:5173`

---

## Usage

1. Open `http://localhost:5173` in your browser
2. Ask anything about traveling in Thailand, e.g.:
   - *"Plan a 3-day trip to Chiang Mai in July for 2 people, mid budget"*
   - *"What are hidden gems in Nakhon Nayok?"*
   - *"Is Phuket crowded in December?"*

The agent will automatically call the relevant tools and return a structured Markdown response with crowd status, recommended places, itinerary, transport, and budget.

---

## Project Structure

```
Hidden-Gem-Finder-AI/
├── GemmyAI/
│   ├── backend/
│   │   ├── main.py          # FastAPI app & routes
│   │   ├── agent.py         # TravelAgent — agentic loop & tool dispatch
│   │   ├── tools/
│   │   │   ├── agentic_rag.py          # RAG tool (Qdrant + Gemini embeddings)
│   │   │   ├── crowded_check.py        # Crowd level estimation
│   │   │   ├── trend_crowded_check.py  # Year-round crowd trend
│   │   │   ├── search_api.py           # Web travel search
│   │   │   ├── current_datetime.py     # Real-time date/time
│   │   │   └── english_adapter.py      # Thai→English output adapter
│   │   ├── requirements.txt
│   │   └── .env.example
│   └── frontend/
│       ├── src/             # React components
│       ├── index.html
│       └── package.json
└── agentic-rag.ipynb        # Notebook for RAG experimentation
```

---

## Team

Built for **Super AI Engineer Season 6** Mini Hack.
=======
# Gemmy-AI: Secondary Cities Finder LLM
>>>>>>> 870ab84b8dbebf9389c7e00a9b80be7873afe413
