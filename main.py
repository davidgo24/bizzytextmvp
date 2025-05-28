from fastapi import FastAPI, Request
from storage import contacts, load_contacts
from services.message_parser import process_message

app = FastAPI()

# Load contacts once when app starts
@app.on_event("startup")
def startup_event():
    load_contacts()

# Simulated route to act like incoming SMS
@app.post("/simulate-inbound")
async def simulate_inbound(request: Request):
    body = await request.json()
    sender = body.get("From")
    message = body.get("Body")

    owner_contacts = contacts.get(sender, {}).get("clients", {})
    parsed = process_message(message, owner_contacts)

    return {"status": "received", "parsed": parsed}
