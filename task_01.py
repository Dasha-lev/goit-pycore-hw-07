from collections import UserDict
from datetime import datetime, timedelta

# Base class for fields in a contact record
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

# Class to store names
class Name(Field):
    pass

# Class to store and validate phone numbers
class Phone(Field):
    def __init__(self, value):
        # Validate the phone number before initializing
        if not self.validate(value):
            raise ValueError("Invalid phone number")
        super().__init__(value)

    @staticmethod
    def validate(phone):
        # Check if the phone number is exactly 10 digits
        return phone.isdigit() and len(phone) == 10

# Class to store and validate birthdays
class Birthday(Field):
    def __init__(self, value):
        try:
            # Try to convert the string value to a datetime object
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

# Class to store a single contact record
class Record:
    def __init__(self, name):
        self.name = Name(name)  # Store the name
        self.phones = []  # Initialize an empty list for phone numbers
        self.birthday = None  # Initialize birthday as None

    def add_phone(self, phone):
        # Add a phone number to the record
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Remove a phone number from the record
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        # Edit an existing phone number in the record
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone

    def find_phone(self, phone):
        # Find a phone number in the record
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        # Add a birthday to the record
        self.birthday = Birthday(birthday)

    def __str__(self):
        # Return a string representation of the record
        phones = '; '.join(p.value for p in self.phones)
        if self.birthday:
            birthday = self.birthday.value.strftime("%d.%m.%Y")
        else:
            birthday = "N/A"
        return f"Contact name: {self.name.value}, phones: {phones}, birthday: {birthday}"

# Class to store a collection of contact records
class AddressBook(UserDict):
    def add_record(self, record):
        # Add a record to the address book
        self.data[record.name.value] = record

    def find(self, name):
        # Find a record by name in the address book
        return self.data.get(name, None)

    def delete(self, name):
        # Delete a record by name from the address book
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self, days=7):
        # Return a list of users with birthdays in the next 'days' days
        today = datetime.now()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                # Calculate the next birthday for the current year
                next_birthday = record.birthday.value.replace(year=today.year)
                # Check if the next birthday falls within the specified range
                if today <= next_birthday <= today + timedelta(days=days):
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

# Create a new address book
book = AddressBook()

# Create a record for John
john_record = Record("John")
john_record.add_phone("1234567890")
john_record.add_phone("5555555555")
john_record.add_birthday("15.08.1985")
book.add_record(john_record)

# Create and add a new record for Jane
jane_record = Record("Jane")
jane_record.add_phone("9876543210")
jane_record.add_birthday("20.08.1990")
book.add_record(jane_record)

# Display all records in the book
for name, record in book.data.items():
    print(record)

# Search and edit the phone for John
john = book.find("John")
john.edit_phone("1234567890", "1112223333")
print(john)  # Display: Contact name: John, phones: 1112223333; 5555555555, birthday: 15.08.1985

# Find a specific phone number in John's record
found_phone = john.find_phone("5555555555")
print(f"Found phone in {john.name.value}'s record: {found_phone}")  # Display: Found phone in John's record: 5555555555

# Delete Jane
book.delete("Jane")

# Get upcoming birthdays
upcoming_birthdays = book.get_upcoming_birthdays()
for record in upcoming_birthdays:
    print(f"Upcoming birthday: {record.name.value} on {record.birthday.value.strftime('%d.%m.%Y')}")
