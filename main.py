from fastapi import FastAPI, Request
from storage import contacts, load_contacts
from services.message_parser import parse_owner_message
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from services.openai_client import run_gpt


load_dotenv(dotenv_path=".env_template")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class SimulateInbound(BaseModel):
    From: str
    Body: str


app = FastAPI()

# Load contacts once when app starts
@app.on_event("startup")
def startup_event():
    load_contacts()

##built for testing directly in fastapi docs

@app.post("/simulate-inbound")
async def simulate_inbound(payload: SimulateInbound):
    sender = payload.From
    message = payload.Body

    owner_contacts = contacts.get(sender, {}).get("clients", {})
    parsed = parse_owner_message(message, owner_contacts)

    # default
    ai_response = None

    if parsed.get("intent") == "reminder" and parsed.get("client_name"):
        confirmation = (
            f"📤 Would you like me to remind {parsed['client_name']} "
            f"({parsed['client_phone']}) about their appointment at {parsed['appointment_time']}?"
        )
    else:
        # GPT helps figure out unknown messages
        ai_response = run_gpt(message)
        print("🧠 GPT says:", ai_response)
        confirmation = "🤖 Sorry, couldn't understand or match that command."

    return {
        "status": "received",
        "confirmation": confirmation,
        "parsed": parsed,
        "ai_response": ai_response
    }
    


# Simulated route to act like incoming SMS -without fastapi routing
'''

@app.post("/simulate-inbound")
async def simulate_inbound(request: Request):
    body = await request.json()
    sender = body.get("From")
    message = body.get("Body")

    owner_contacts = contacts.get(sender, {}).get("clients", {})
    parsed = parse_owner_message(message, owner_contacts)

    # Fake response to show what *would* happen
    if parsed["intent"] == "reminder" and parsed["client_name"]:
        confirmation = f"📤 Would remind {parsed['client_name']} ({parsed['client_phone']}) about appointment at {parsed['appointment_time']}"
    else:
        confirmation = "🤖 Sorry, couldn't understand or match that command."

    return {
        "status": "received",
        "confirmation": confirmation,
        "parsed": parsed
    }

'''