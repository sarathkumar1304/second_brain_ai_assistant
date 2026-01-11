import asyncio
from pathlib import Path
import sys

from src.slack_integrations_online.application.agents.agents import SupportAgentsManager


async def main(user_query):
    """Run the app in CLI mode"""
    print(f"\nQuery: {user_query}")
    print("-" * 50)
    
    agent = SupportAgentsManager()
    
    try:
        response = await agent.run(query=user_query)
        
        print(f"\n🤖 AGENT RESPONSE:\n")
        print(response)
        print("\n" + "=" * 50)
        print(f"Response length: {len(response)} characters")
        
        # Check if documents were used
        if "http" in response or "https://" in response:
            print("Documents were cited in the response!")
        elif "I don't have enough information" in response:
            print("No relevant documents found")
        else:
            print("General response generated")
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print('\n' + '='*50)
    print('AI Support Engineer')
    print('='*50)
    
    while True:
        try:
            user_query = input("\nEnter your query (or 'quit' to exit): ")
            if user_query.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
                
            asyncio.run(main(user_query=user_query))
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n Unexpected error: {str(e)}")
