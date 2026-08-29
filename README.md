# 🔎 Research Agent (LangGraph)

A multi-source research agent that takes a topic, breaks it into sub-angles, searches each independently in parallel, retries weak results, detects when sources disagree, and synthesizes everything into a single cited brief — built with [LangGraph](https://github.com/langchain-ai/langgraph).

Includes a Streamlit UI for trying it out interactively.

## Why this project

Most "agent" demos wire together 2–3 fixed steps in a straight line. This one needs a real graph: each subtopic runs its own independent search → verify → retry loop **in parallel** (via LangGraph's `Send` API / map-reduce pattern), results converge at a single point, and conflicting sources are flagged rather than silently resolved.

## How it works

1. **Break into subtopics** — an LLM (Groq) splits the research topic into 3 distinct sub-angles.
2. **Parallel search** — each subtopic is researched independently and concurrently (Tavily search), with its own retry loop: if the LLM judges a result inadequate, it searches again (up to a fixed attempt limit).
3. **Convergence** — once all subtopic branches finish, execution converges at a single point before continuing.
4. **Conflict detection** — an LLM compares the combined sources and flags disagreements, with a dedicated resolution step when needed.
5. **Synthesis** — a final research brief is generated, citing the underlying sources.

## Tech stack

- [LangGraph](https://github.com/langchain-ai/langgraph) — graph orchestration, parallel fan-out (`Send`), conditional routing
- [Groq](https://groq.com) (`openai/gpt-oss-20b`) — LLM calls via `langchain-groq`
- [Tavily](https://tavily.com) — web search
- [Streamlit](https://streamlit.io) — UI

## Setup

```bash
git clone https://github.com/MehdiBeghoura/research-agent-langgraph.git
cd research-agent-langgraph
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` with your own keys:

```
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

Both keys are free to obtain from [Groq Console](https://console.groq.com) and [Tavily](https://tavily.com).

## Usage

**Command line:**
```bash
python -m src.main
```

**Streamlit UI:**
```bash
streamlit run app.py
```

Enter a research topic and the agent will investigate it, showing progress and a final cited brief.

## Project structure

```
src/
  state.py    # graph state schemas
  llm.py      # model + search tool setup
  nodes.py    # node and routing function definitions
  graph.py    # graph assembly
  main.py     # CLI entry point
app.py        # Streamlit UI
```

## Status

Built as a hands-on project while learning LangGraph — the retry loop, parallel fan-out, and convergence pattern were the main things this project was designed to exercise.