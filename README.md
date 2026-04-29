# Local Code Agent

A lightweight, autonomous AI agent designed to interact with your local file system. This agent uses Ollama and any open source model model (that supports tools) calling to perform file operations (read, write, list) through structured tool calling.

## Purpose
- This agent is designed mainly for learning purposes, to understand how AI agents work and how to build them in practice.
- This agent is not meant for production use, but rather for educational purposes.
- Anyone can fork and modify this agent to suit their needs, and use it as a starting point for their own projects.

## Features
* **Autonomous Tool Use**: The agent intelligently decides when to read, write, or list files based on your natural language requests.
* **Structured Interaction**: Uses JSON-based tool calling for high reliability and error reduction.
* **Persistent Memory**: Maintains conversation context, allowing for multi-turn tasks and file-based workflows.
* **Local Execution**: Everything runs locally on your machine via Ollama, ensuring your data stays private.

## Quick Start

### Prerequisites
* [Ollama](https://ollama.com/) installed and running locally.
* Python 3.x installed.
* The `ollama` Python library: `pip install ollama`

### Setup
1.  **Clone the project** to your local machine.
2.  **Pull the model**: Ensure you have the model pulled in Ollama:
    ```bash
    ollama pull codellama
    ```
3.  **Run the agent**:
    ```bash
    python main.py
    ```

## Project Structure
* `agent.py`: Contains the core logic, loop, and integration with the Ollama client.
* `main.py`: The entry point that manages the persistent conversation history.
* `tools.py`: Contains the actual Python functions for file system interactions.
* `prompts.py`: Defines the `SYSTEM_PROMPT` that guides the agent's behavior.

## How it Works
The agent operates on a continuous feedback loop. When you provide a prompt, the agent:
1.  Analyzes the request.
2.  Calls a specific tool if needed (e.g., `read_file`).
3.  Receives the tool output as a "tool" role message.
4.  Processes the information to formulate a final response.

## Safety & Privacy
Since this agent has write access to your local file system, please ensure you are running it in a sandbox or a directory where you have tested its behavior.

To incorporate this clearly into your `README.md`, you can include the following section. I have added a diagram tag that illustrates the interaction between your persistent history (Main Loop) and the recursive execution cycle (Agent Loop).

***

## Architecture & Data Flow

Your agent utilizes a two-tier loop architecture to maintain state while performing complex tasks:

### 1. Main Loop (`main.py`)
* **Role**: Acts as the **Memory Controller**.
* **Function**: Initializes the conversation history (System Prompt + User Input) once. It keeps this state alive across multiple user prompts, ensuring the agent "remembers" previous interactions.

### 2. Agent Loop (`agent.py`)
* **Role**: Acts as the **Execution Engine**.
* **Function**: Accepts the current conversation history. It enters a recursive cycle where it calls tools, processes their outputs, and continues communicating with the LLM until the final answer is reached. Once finished, it returns the result to the Main Loop without destroying the history.

***

### Why this design?
* **Persistence**: The conversation never resets because the `messages` list is held in `main.py` and passed by reference.
* **Separation of Concerns**: `main.py` handles the *session*, while `agent.py` handles the *tasks*. This makes it easy to swap out models or add new tools without breaking the conversational flow.

### The Synergy

When you combine them, you get a powerful workflow:

|**Feature**|**Brain (Main Loop)**|**Action (Agent Loop)**|
|---|---|---|
|**Persistence**|Lives for the duration of the chat|Exists only for the duration of one task|
|**State**|Holds the full context (`messages`)|Holds the temporary tool-call state|
|**Interaction**|User speaks to the Brain|Brain dispatches tasks to the Action|

**This architecture allows for "Stateful Delegation."** The Brain sets the goal and keeps track of progress, while the Action does the "dirty work" of interfacing with your computer's file system.
