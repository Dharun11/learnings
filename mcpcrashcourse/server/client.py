import asyncio
from langchain_openai import AzureChatOpenAI
from mcp_use import MCPClient,MCPAgent
from dotenv import load_dotenv
import os

async def execute_chat():
    # Load environment variables
    load_dotenv()
    
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
    api_base=os.getenv("AZURE_ENDPOINT")
    api_version=os.getenv("AZURE_API_VERSION")
    
    
      # Config file path - change this to your config file
    config_file = "server/weather.json"
    
    print("initiating chat.................")
    
    ## Here it is reading the server , and getting all the information from the config file
    client=MCPClient.from_config_file(config_file)
    
    llm=AzureChatOpenAI(
        azure_deployment='gpt-4.1',
        api_version=api_version,
        temperature=0.7,
        azure_endpoint=api_base,
        
        
    )
    
    
    """ here client is going to provide context to the agent (LLM) which is acting in the form of agent """
    # Create agent with memory_enabled=True
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,  # Enable built-in conversation memory
    )
    
    print("\n===== Interactive MCP Chat =====")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("==================================\n")

    try:
        # Main chat loop
        while True:
            # Get user input
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Ending conversation...")
                break

            # Check for clear history command
            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared.")
                continue

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                # Run the agent with the user input (memory handling is automatic)
                response = await agent.run(user_input)
                print(response)

            except Exception as e:
                print(f"\nError: {e}")

    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()


if __name__ == "__main__":
    asyncio.run(execute_chat())