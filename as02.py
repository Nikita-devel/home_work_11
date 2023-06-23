from collections import UserDict
import datetime
import requests


class Field:
    def __init__(self, value=None):
        self._value = value

    def __str__(self):
        return str(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value


class Name(Field):
    def __str__(self):
        return str(self._value).capitalize()


class Phone(Field):
    def __str__(self):
        return str(self._value)

    @Field.value.setter
    def value(self, new_value):
        if not self._is_valid_phone(new_value):
            raise ValueError("Invalid phone number")
        self._value = new_value

    @staticmethod
    def _is_valid_phone(phone):
        if len(phone) != 10:
            return False
        if not phone.isdigit():
            return False
        return True


class Birthday(Field):
    def __str__(self):
        return str(self._value)

    @Field.value.setter
    def value(self, new_value):
        if not self._is_valid_birthday(new_value):
            raise ValueError("Invalid birthday")
        self._value = new_value

    @staticmethod
    def _is_valid_birthday(birthday):
        try:
            datetime.datetime.strptime(birthday, "%Y-%m-%d")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday

    def add_phone(self, phone):
        self.phones.append(phone)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        if old_phone in self.phones:
            index = self.phones.index(old_phone)
            self.phones[index] = new_phone

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.date.today()
            next_birthday = datetime.date(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = datetime.date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        return None

    def __str__(self):
        output = f"Name: {self.name.value}\n"
        for phone in self.phones:
            output += f"Phone: {phone.value}\n"
        output += "---------\n"
        return output


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def delete_record(self, name):
        del self.data[name.value]

    def edit_record(self, name, new_record):
        self.data[name.value] = new_record

    def search_records(self, query):
        search_results = AddressBook()
        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                search_results.add_record(record)
        return search_results


API_KEY = "653c3ccd328356a16a58c6dbd440c093"


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Enter user name"
        except ValueError:
            return "Give me name and phone please"
        except IndexError:
            return "Enter both name and phone"

    return inner


contacts = AddressBook()


@input_error
def add_contact(name, phone):
    name = Name(str(name).capitalize())
    phone = Phone(phone)
    if name.value in contacts:
        record = contacts[name.value]
    else:
        record = Record(name)
    record.add_phone(phone)
    contacts.add_record(record)
    return "Contact added successfully"


@input_error
def change_contact(name, old_phone, new_phone):
    if name.value in contacts:
        record = contacts[name.value]
        record.edit_phone(old_phone, new_phone)
        return "Contact updated successfully"
    else:
        return "Contact not found"


@input_error
def get_phone(name):
    if name.value in contacts:
        record = contacts[name.value]
        return [str(phone) for phone in record.phones]
    else:
        return "Contact not found"


def show_all_contacts():
    if contacts:
        output = ""
        for record in contacts.values():
            output += str(record)
        return output
    else:
        return "No contacts found"


def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    if data["cod"] == 200:
        temperature = data["main"]["temp"]
        weather_description = data["weather"][0]["description"]
        return f"The current weather in {city} is {weather_description}. Temperature: {temperature}°C"
    else:
        return "Failed to retrieve weather information"


def get_current_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return f"The current time is {current_time}"


def help_commands():
    return """
    Available commands:
    - hello: Greet the assistant
    - add <name> <phone>: Add a contact with the given name and phone number
    - change <name> <old_phone> <new_phone>: Change the phone number of an existing contact
    - phone <name>: Get the phone number(s) of a contact
    - show all: Show all saved contacts
    - weather <city>: Get the current weather in the specified city
    - time: Get the current time
    - help: Show available commands
    - goodbye, close, exit: Close the assistant
    """


def parse_command(user_input):
    command = user_input[0]
    arguments = user_input[1:]

    if command == "hello":
        print("How can I help you?")
    elif command == "add":
        if len(arguments) >= 2:
            name = Name(" ".join(arguments[:-1]))
            phone = Phone(arguments[-1])
            print(add_contact(name, phone))
        else:
            raise ValueError("Give me name and phone please")
    elif command == "change":
        if len(arguments) == 3:
            name, old_phone, new_phone = arguments
            print(change_contact(name, old_phone, new_phone))
        else:
            raise ValueError("Give me name, old phone, and new phone please")
    elif command == "phone":
        if len(arguments) == 1:
            name = arguments[0]
            try:
                print(get_phone(name))
            except KeyError:
                print("Contact not found")
        else:
            raise ValueError("Enter user name")
    elif command == "show":
        if len(arguments) == 1 and arguments[0] == "all":
            print(show_all_contacts())
        else:
            raise ValueError("Invalid command. Type 'help' to see the available commands.")
    elif command == "weather":
        if len(arguments) == 1:
            city = arguments[0]
            print(get_weather(city))
        else:
            raise ValueError("Enter city name")
    elif command == "time":
        print(get_current_time())
    elif command == "help":
        print(help_commands())
    elif command in ["goodbye", "close", "exit"]:
        print("Goodbye!")
        exit()
    else:
        print("Invalid command. Type 'help' to see the available commands.")


if __name__ == "__main__":
    print("Welcome to the Address Book Assistant!")
    while True:
        user_input = input("Enter a command: ").strip().split(" ")
        parse_command(user_input)
