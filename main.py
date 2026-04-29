from agent import run_agent
from prompts import SYSTEM_PROMPT

if __name__ == "__main__":
    # Initialize the history once
    messages = [{'role': 'system', 'content': SYSTEM_PROMPT}]

    print("Agent is ready! (Type 'quit' to exit)")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        # add user input to presistent history
        messages.append({"role": "user", "content": user_input})    

        # Run agent with presistent history
        result = run_agent(messages)
        
        # Add agent's final response to history so it remembers later
        messages.append({"role": "assistant", "content": result})   
        print(f"Agent: {result}")