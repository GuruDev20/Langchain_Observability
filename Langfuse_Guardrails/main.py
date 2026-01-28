from agent.agent import run_agent

if __name__ == "__main__":
    print("Safe Research Agent (type 'exit' to quit)\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = run_agent(user_input)
        print(f"Agent: {response}")
