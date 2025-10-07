# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic",
#     "pydantic",
# ]
# ///

import os
import sys
import argparse
# Import AIAgent from the new module
from ai_agent import AIAgent


def main():
    parser = argparse.ArgumentParser(
        description="AI Code Assistant - A conversational AI agent with file editing capabilities"
    )
    parser.add_argument(
        "--api-key", help="Anthropic API key (or set ANTHROPIC_API_KEY env var)"
    )
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "Error: Please provide an API key via --api-key or ANTHROPIC_API_KEY environment variable"
        )
        sys.exit(1)

    # Instantiate the imported AIAgent
    agent = AIAgent(api_key)

    print("AI Code Assistant")
    print("================")
    print("A conversational AI agent that can read, list, and edit files.")
    print("Type 'exit' or 'quit' to end the conversation.")
    print()

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            if not user_input:
                continue

            print("\nAssistant: ", end="", flush=True)
            # Use the chat method from the AIAgent class
            response = agent.chat(user_input)
            print(response)
            print()

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            print()


if __name__ == "__main__":
    main()