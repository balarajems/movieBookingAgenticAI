import asyncio
import logging
from modules.group_chat import MovieBookingGroupChat  # ✅ Use new `MovieBookingGroupChat`

# Configure logging
logging.basicConfig(level=logging.DEBUG)

async def run_test_queries():
    """Manually test queries without Flask using SelectorGroupChat."""
    movie_chat = MovieBookingGroupChat()  # ✅ Use `MovieBookingGroupChat` instead of `RouterAgent`

    print("\n🚀 Starting AutoGen Agent System...\n")
    
    while True:
        user_query = input("👤 User: ")
        if user_query.lower() in ["exit", "quit"]:
            print("\n👋 Exiting...")
            break

        response = await movie_chat.process_query(user_query, user_id="12345")  # ✅ Await the async function
        print("")
        print("")
        print(f"🤖 AI: {response}\n")

if __name__ == "__main__":
    asyncio.run(run_test_queries())  # ✅ Use asyncio to properly run async functions
