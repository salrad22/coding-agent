from agent import run_agent

if __name__ == "__main__":
    prompt = input("Enter your prompt: ")
    result = run_agent("Make example/utils/logger.py async")
    print(result)