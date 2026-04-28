# agent.py
import ollama
from tools import read_file, write_file, list_files
from prompts import SYSTEM_PROMPT

# Tool Registry
tools = {
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files
}

def run_agent(prompt: str):
    response = ollama.chat(
        model="qwen2.5-coder:7b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
    )
    return response["message"]["content"]

    


