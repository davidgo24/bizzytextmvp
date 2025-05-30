import re
import dateparser  
from datetime import datetime, timedelta
from dateutil.parser import ParserError


 
def parse_owner_message(message: str, contacts: dict):
    client_name = None
    client_phone = None

    #try to match known client names from contact list
    for name in contacts:
        if name.split()[0].lower() in message.lower():
            client_name = name
            client_phone = contacts[name]["phone"]
            break
    

    try:
        appointment_time = dateparser.parse(message, fuzzy=True)
    except (ParserError, TypeError, ValueError):
        appointment_time = None
    intent = "reminder" if "remind" in message.lower() else "unknown"

    return {
        "intent": intent,
        "client_name": client_name,
        "client_phone": client_phone,
        "appointment_time": appointment_time.isoformat() if appointment_time else None,
        "raw": message
    }





