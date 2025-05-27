import json

contacts = {}

def load_contacts():
    global contacts
    with open("data/dummy_contacts.json", "r") as f:
        contacts.update(json.load(f))
    print("📁 Dummy contacts loaded.")

def get_owner_clients(owner_id):
    return contacts.get(owner_id, {}).get("clients", {})
