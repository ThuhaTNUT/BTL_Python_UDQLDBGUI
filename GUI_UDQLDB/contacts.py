import json
import os

class ContactManager:
    def __init__(self, filename='contacts.json'):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.contacts = json.load(f)
            except json.JSONDecodeError:
                self.contacts = []
        else:
            self.contacts = []

    def save_contacts(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.contacts, f, indent=4, ensure_ascii=False)

    def add_contact(self, contact):
        self.contacts.append(contact)
        self.save_contacts()

    def update_contact(self, index, new_contact):
        if 0 <= index < len(self.contacts):
            self.contacts[index] = new_contact
            self.save_contacts()

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            self.contacts.pop(index)
            self.save_contacts()
