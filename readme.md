
# CEAF v3.0 - Coherent Emergence Agent Framework

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

CEAF is an advanced, multi-module framework for building AI agents that demonstrate metacognitive awareness, long-term learning, and a coherent sense of identity. It is designed to move beyond simple request-response models by endowing an agent with internal states, reflective capabilities, and the ability to learn deeply from both success and failure.

The core principle of CEAF is **"Coherent Emergence"**: the idea that a robust, intelligent, and principled agent consciousness can emerge from the interaction of specialized, well-defined subsystems.

## Core Features

- **Metacognitive Control:** The agent is aware of its own cognitive state (e.g., stable, exploring, confused) and adapts its behavior accordingly.
- **Adaptive Memory (AMA):** A sophisticated memory system that clusters experiences, associates successes with failures, and learns from loss patterns.
- **Virtue-Based Reasoning (VRE):** Provides principled guidance, promoting intellectual humility, courage, and wisdom based on the current context.
- **Narrative Identity (NCIM):** The agent maintains an evolving, first-person narrative of its identity, which is updated after significant experiences.
- **Failure Analysis (LCAM):** Explicitly catalogs, analyzes, and learns from failures to develop resilience and avoid repeating mistakes.
- **Long-Term Reflection (AURA):** Periodically analyzes the agent's entire history to find deep patterns, evolutionary trends, and systemic insights.
- **Modular & Orchestrated:** Built with independent modules coordinated by a central orchestrator (`ORA`) using `LangGraph`, making the system extensible and robust.

## System Architecture

CEAF's architecture is composed of several interconnected modules that work together to process a user's query and update the agent's internal state.

```
+------------------+      +---------------------+
|   User / Input   |----->|   Integration.py    |
+------------------+      |  (Main Entrypoint)  |
                          +----------+----------+
                                     |
                                     |
             +-----------------------v-----------------------+
             |        ORA (Orchestrator - LangGraph)         |
             |                                               |
             |   [1. Retrieve] <------> AMA (Memory)         |
             |   [2. Assess]   <------> MCL (Metacognition)   |
             |   [3. Insights] <------> LCAM (Loss Analysis)  |
             |   [4. Guide]    <------> VRE (Virtue Engine)   |
             |   [5. Respond]  <------> LLM (via OpenRouter)  |
             |   [6. Learn]    ------> [AMA, LCAM]            |
             |   [7. Update]   <------> NCIM (Identity)       |
             |                                               |
             +-----------------------------------------------+
                                     |
                                     | (Periodic background task)
                                     |
                          +----------v----------+
                          |   AURA (Reflector)  |
                          | (Analyzes AMA/MCL)  |
                          +---------------------+
```

### Component Breakdown

| File                 | Component                                | Role                                                                                              |
| -------------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------- |
| `Integration.py`     | **System Integration**                   | The main entry point. Initializes all modules, manages state persistence, and runs the interactive session. |
| `ORA.py`             | **Orchestrator/Responder Agent**         | Uses `LangGraph` to define and execute the step-by-step cognitive cycle for responding to a query.   |
| `MCL.py`             | **Metacognitive Control Loop**           | Assesses the system's "coherence state" (e.g., stable, edge of chaos) to guide agent strategy.     |
| `AMA.py`             | **Adaptive Memory Architecture**         | The agent's long-term memory. Stores, clusters, and retrieves experiences, with a focus on loss context. |
| `NCIM.py`            | **Narrative Coherence & Identity Module**| Manages the agent's evolving first-person identity narrative.                                       |
| `LCAM.py`            | **Loss Cataloging & Analysis Module**    | Specializes in analyzing failure experiences to provide cautionary insights and identify patterns.    |
| `VRE.py`             | **Virtue & Reasoning Engine**            | Provides principled, ethical guidance (e.g., "be humble," "be courageous") based on the agent's state. |
| `AURA.py`            | **Autonomous Universal Reflective Analyzer** | A background process that performs deep, long-term analysis on memory and state history to find systemic patterns. |

## Setup and Installation

### 1. Prerequisites

- Python 3.9 or higher.
- Git.

### 2. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 3. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage dependencies.

```bash
# For Unix/macOS
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
.\venv\Scripts\activate
```

### 4. Install Dependencies

The required Python packages are listed in `requirements.txt`.

First, create a `requirements.txt` file with the following content:

```text
# requirements.txt
numpy
sentence-transformers
scikit-learn
faiss-cpu
langchain
langgraph
langchain-core
langchain-community
litellm
python-dotenv
```

Then, install them using pip:

```bash
pip install -r requirements.txt
```

### 5. Set Up API Keys

The system uses [OpenRouter.ai](https://openrouter.ai/) to access various large language models. You will need an OpenRouter API key.

1.  Create a file named `.env` in the root of the project directory.
2.  Add your API key to this file:

```env
# .env
OPENROUTER_API_KEY='your-openrouter-api-key-here'
```

## How to Run

The main entry point for the system is `Integration.py`. Run this file from your terminal to start an interactive chat session with the CEAF agent.

```bash
python Integration.py
```

You will see a welcome message, and you can start typing your queries.

```
🧠 CEAF v3.0 - Coherent Emergence Agent Framework
==================================================
2023-10-27 12:00:00,000 - __main__ - INFO - Initializing CEAF v3.0 System...
... (initialization logs) ...
2023-10-27 12:00:05,000 - __main__ - INFO - CEAF v3.0 System initialized successfully

💭 You: What is the nature of consciousness?
```

### In-Session Commands

-   `status`: Type `status` to get a JSON dump of the current system state, including memory stats, MCL state, and AURA insights.
-   `quit`: Type `quit` to gracefully shut down the system. This will save the latest state of all modules.

## How It Works: The Lifecycle of a Query

1.  **Input:** A user query is passed to `CEAFSystem.process()`.
2.  **Orchestration Begins:** The `ORA`'s LangGraph workflow is invoked.
3.  **Memory Retrieval (`AMA`):** The `ORA` queries the `AMA` to find relevant past experiences, including both successes and failures related to the query.
4.  **Coherence Assessment (`MCL`):** The `MCL` analyzes the context and determines the agent's current metacognitive state (e.g., `STABLE`, `EDGE_OF_CHAOS`).
5.  **Failure Insight (`LCAM`):** The `LCAM` checks the retrieved memories for known failure patterns and provides cautionary insights.
6.  **Virtuous Guidance (`VRE`):** The `VRE` analyzes the full context (MCL state, failures, etc.) and generates a list of principles to guide the response (e.g., "Acknowledge uncertainty").
7.  **Response Generation (`ORA`):** The `ORA` constructs a detailed prompt for a large language model. This prompt includes the user's query, the agent's identity narrative (`NCIM`), retrieved memories, coherence state, and virtue considerations. It then calls the LLM via OpenRouter.
8.  **Learning (`AMA` & `LCAM`):** The interaction (query, response, outcome) is saved as a new `MemoryExperience` in the `AMA`. If it was a failure, the `LCAM` catalogs it.
9.  **Identity Update (`NCIM`):** The `NCIM` receives a summary of the interaction and uses an LLM call to weave the lesson learned into the agent's core identity narrative.
10. **Periodic Reflection (`AURA`):** Independently and periodically (e.g., every 10 interactions), `AURA` runs in the background. It analyzes the entire history of experiences and states to find high-level insights, which can influence future reasoning.

## State Persistence

The system is designed to be persistent. When you run it, it will create a `ceaf_data/` directory in your project root. This directory stores the state of all modules:

-   `memory_state.json`: All experiences and clusters from `AMA`.
-   `mcl_state.json`: State history and metrics from `MCL`.
-   `ncim_state.json`: The current identity narrative from `NCIM`.
-   `aura_state.json`: All long-term insights discovered by `AURA`.

When you restart the application, it will automatically load this state, allowing the agent to learn and evolve across sessions.
