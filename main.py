import os
import sys
from dotenv import load_dotenv
import argparse

from prompts import system_prompt
from functions.call_function import available_functions, call_function

parser = argparse.ArgumentParser(description="Chatbot")

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def generate_content(client, messages, model):
    return client.chat.completions.create(
        model=model,
        messages=messages,
        tools=available_functions,
        temperature=0,
    )


def main():
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--model",
        default="openrouter/free",
        help="OpenRouter model id (default: openrouter/free)",
    )
    args = parser.parse_args()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    for _ in range(20):
        response = generate_content(client, messages, args.model)
        if args.verbose:
            usage = response.usage
            print(f"Prompt tokens: {usage.prompt_tokens if usage else 0}")
            print(f"Response tokens: {usage.completion_tokens if usage else 0}")

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, verbose=args.verbose)
                if not result_message.get("content"):
                    raise Exception("no content in tool message")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
            continue

        print("Final response:")
        print(message.content)
        break
    else:
        print("Error: Agent reached maximum iterations (20) without a final response.")
        sys.exit(1)


if __name__ == "__main__":
    main()
