import os
from dotenv import load_dotenv
import argparse

from prompts import system_prompt

parser = argparse.ArgumentParser(description="Chatbot")

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


def generate_content(client, messages):
    return client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        temperature=0,
    )


def main():
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    response = generate_content(client, messages)
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        usage = response.usage
        print(f"Prompt tokens: {usage.prompt_tokens if usage else 0}")
        print(f"Response tokens: {usage.completion_tokens if usage else 0}")
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
