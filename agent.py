# agent.py
import ollama
from tools import read_file, write_file, list_files
from prompts import SYSTEM_PROMPT

client = ollama.Client(host="http://localhost:11434")

# Tool Registry
tools = {
    "read_file": read_file,
    "write_file": write_file,
    "list_files": list_files
}

# The model receives this definition to understand how to call tools
tools_definition = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a file at the specified path.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The relative or absolute file path (e.g., 'data.txt')."
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text content to a file at the specified path. Overwrites if file exists.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "The destination file path."
                    },
                    "content": {
                        "type": "string",
                        "description": "The text content to be written to the file."
                    }
                },
                "required": ["path", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List all files in the current working directory.",
            "parameters": {
                "type": "object",
                "properties": {} # No arguments needed for this function
            }
        }
    }
]

def run_agent(messages: list):
    print(f"DEBUG: messages type is {type(messages)}")
    print(f"DEBUG: first element is {messages[0]}")
    while True: 
        response = client.chat(model="qwen3:0.6b", 
                                messages=messages,
                                tools=tools_definition)

        # 1. Append the model's response to history
        # Important: Add the whole message object, not just the content string
        messages.append({
            "role": "assistant",
            "content": str(response.message.content) if response.message.content else ""
        })
        
        # 2. Check if it's a tool call
        if response.message.tool_calls:
            # We add the tool call info to the assistant message 
            # (or append it as a separate dict depending on your Ollama version)
            messages[-1]["tool_calls"] = response.message.tool_calls
            
            for tool_call in response.message.tool_calls:
                # Extract the function name and the arguments dictionary
                name = tool_call.function.name
                args = tool_call.function.arguments # This is already a clean dict!
                
                # Dispatch to your local 'tools' dictionary
                if name in tools:
                    # Execute the function using the arguments dictionary
                    # The ** unpacks the dict into function keyword arguments
                    tool_result = tools[name](**args)
                    tool_result_str = str(tool_result)
                    
                    # Store the result as a 'tool' role message
                    messages.append({
                        "role": "tool", 
                        "content": tool_result_str,
                        "name": name # Some APIs prefer the tool name here
                    })
            continue 
        
        # 2. If no tool, it's the final answer
        return response.message.content