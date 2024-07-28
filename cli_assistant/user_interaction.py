from collections import UserDict
from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self) -> str:
        return str(self.value)
    
class Name(Field):
    def __init__(self, name):
         self.validate(name)
         super().__init__(name)

    @staticmethod
    def validate(name):
         if not name.strip():
              raise ValueError('Required field')

class Phone(Field):
    
    def __init__(self, phone_number):
        self.validate(phone_number)
        super().__init__(phone_number)

    @staticmethod
    def validate(phone_number):
        if not re.match(r'^\d{10}$', phone_number):
             raise ValueError(f'Phone number {phone_number} is not valid.')

class Birthday(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    @staticmethod
    def validate(value):
        try:
            datetime.strptime(value, "%d.%m.%Y").date()     
        except ValueError:
            raise ValueError('Invalid date format. Use DD.MM.YYYY')

class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        Phone.validate(phone)
        self.phones.append(Phone(phone))
        return f"Phone {phone} added to {self.name.value}"

    def remove_phone(self, contact_phone):
        self.phones = [phone for phone in self.phones if phone.value != contact_phone]
        return f"Phone {contact_phone} removed from {self.name.value}"

    def edit_phone(self, contact_phone, new_phone):
        Phone.validate(new_phone)
        for phone in self.phones:
            if phone.value == contact_phone:
                phone.value = new_phone
            
        return f"Phone {contact_phone} updated to {new_phone} in {self.name.value}"

    def find_phone(self, contact_phone):
        matching = [phone for phone in self.phones if phone == contact_phone]
        return matching

    def add_birthday(self, birthday):
        Birthday.validate(birthday)
        self.birthday = Birthday(birthday)
        return f"Birthday {birthday} added to {self.name.value}"
                  
    def __str__(self) -> str:
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record
        return f"Record for {record.name.value} added."

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record for {name} deleted."
        else:
            return f'Record {name} not found'

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                birthday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = birthday.replace(year=today.year)

                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)

                days_until_birthday = (birthday_this_year - today).days

                if 0 <= days_until_birthday <= 7:
                    congratulation_date = birthday_this_year

                    if birthday_this_year.weekday() >= 5: 
                        congratulation_date += timedelta(days=(7 - birthday_this_year.weekday()))

                    upcoming_birthdays.append({
                        'name': record.name.value,
                        'congratulation_date': congratulation_date.strftime('%d.%m.%Y')
                    })

        return upcoming_birthdays

