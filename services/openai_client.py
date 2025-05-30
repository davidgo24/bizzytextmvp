import os
from openai import OpenAI
from dotenv import load_dotenv

# Load env vars if not already done elsewhere
load_dotenv(dotenv_path=".env_template")

# Create OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set in environment.")

client = OpenAI(api_key=api_key)

def run_gpt(message: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": (
                    "You're an assistant that helps interpret client SMS messages for appointment-based businesses.\n"
                    "You were only called because the system couldn't match the client in the contacts list.\n"
                    "If you detect a name in the message, ask the business owner if they'd like to add them as a new contact.\n"
                    "You may also confirm the appointment time if it's clearly stated."
                )
            },
            {"role": "user", "content": message}
        ],
        max_tokens=200
    )
    return response.choices[0].message.content.strip()