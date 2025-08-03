import json
import os

FILENAME = "contacts.json"

def load_contacts():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r") as f:
            return json.load(f)
    return {}

def save_contacts(contacts):
    with open(FILENAME, "w") as f:
        json.dump(contacts, f, indent=4)

def add_contact(contacts, name, phone):
    if name in contacts:
        return False  # مخاطب تکراری
    contacts[name] = phone
    save_contacts(contacts)
    return True

def edit_contact(contacts, old_name, new_name, new_phone):
    if old_name not in contacts:
        return False  # مخاطب وجود ندارد
    if new_name != old_name and new_name in contacts:
        return False  # نام جدید تکراری است
    del contacts[old_name]
    contacts[new_name] = new_phone
    save_contacts(contacts)
    return True

def delete_contact(contacts, name):
    if name in contacts:
        del contacts[name]
        save_contacts(contacts)
        return True
    return False
