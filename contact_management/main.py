import mysql.connector
from mysql.connector import Error

class Contact:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Yagya@2003",
                database="contacts_db"
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor()
                print("Connected to the database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.cursor = None
            self.conn = None

    def add_contact(self, name: str, number: str):
        if len(number) < 10:
            print("Number is invalid")
            return
        try:
            query = "INSERT INTO contacts (name, number) VALUES (%s, %s)"
            self.cursor.execute(query, (name, number))
            self.conn.commit()
            print(f"Contact added: {name} - {number}")
        except Error as e:
            print(f"Failed to add contact: {e}")

    def delete_contact(self, name: str):
        try:
            query = "DELETE FROM contacts WHERE name = %s"
            self.cursor.execute(query, (name,))
            if self.cursor.rowcount == 0:
                print("No contact with this name is present")
            else:
                self.conn.commit()
                print(f"Contact deleted: {name}")
        except Error as e:
            print(f"Failed to delete contact: {e}")

    def update_contact(self, name: str, new_number: str):
        if len(new_number) < 10:
            print("New number is invalid")
            return
        try:
            query = "UPDATE contacts SET number = %s WHERE name = %s"
            self.cursor.execute(query, (new_number, name))
            if self.cursor.rowcount == 0:
                print("No contact with this name is present")
            else:
                self.conn.commit()
                print(f"Contact updated: {name} - {new_number}")
        except Error as e:
            print(f"Failed to update contact: {e}")

    def display_contacts(self):
        try:
            self.cursor.execute("SELECT name, number FROM contacts")
            results = self.cursor.fetchall()
            if not results:
                print("No contacts to display")
            else:
                for name, number in results:
                    print(f"{name}: {number}")
        except Error as e:
            print(f"Failed to retrieve contacts: {e}")

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("Connection to the database closed")

if __name__ == "__main__":
    contact_manager = Contact()
    flag = True

    options = {
        "1": "Add",
        "2": "Delete",
        "3": "Update",
        "4": "Display",
        "5": "Exit"
    }

    while flag:
        for key, value in options.items():
            print(f"Enter {key} for {value}")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter the name of contact: ")
            number = input("Enter the number: ")
            contact_manager.add_contact(name, number)
        elif choice == "2":
            name = input("Enter the name of contact: ")
            contact_manager.delete_contact(name)
        elif choice == "3":
            name = input("Enter the name of contact: ")
            new_number = input("Enter the new number: ")
            contact_manager.update_contact(name, new_number)
        elif choice == "4":
            contact_manager.display_contacts()
        elif choice == "5":
            flag = False
        else:
            print("Enter a valid choice")
