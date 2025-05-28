import dateparser
from datetime import datetime

def parse_owner_message(message: str, contacts: dict):
    client_name = None
    client_phone = None

    #try to match known client names from contact list
    for name in contacts:
        if name.split()[0].lower() in message.lower():
            client_name = name
            client_phone = contacts[name]["phone"]
            break
    

    appointment_time = dateparser.parse(message, settings ={'PREFER_DATES_FROM': 'future'})
    intent = "reminder" if "remind" in message.lower() else "unknown"

    return {
        "intent": intent,
        "client_name": client_name,
        "client_phone": client_phone,
        "appointment_time": appointment_time.isoformat() if appointment_time else None,
        "raw": message
    }




def process_message(sender: str, message: str):
    return {
        "sender": sender,
        "message": message,
        "status": "parsed_placeholder"
    }
