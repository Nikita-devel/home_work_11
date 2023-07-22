import datetime

class Name:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value).capitalize()


class Phone:
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return str(self.value)
    

class Birthday:
    def __init__(self, day=None, month=None):
        self.day = day
        self.month = month

    def __str__(self):
        if self.day is None or self.month is None:
            return "Not specified"
        return f"{self.day:02d}/{self.month:02d}"


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(str(name).capitalize())
        self.phones = []
        if phone is not None:
            self.phones.append(Phone(phone))
        self.birthday = birthday

    def add_phone(self, phone):
        if phone not in self.phones:
            self.phones.append(phone)

    def delete_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if str(phone) == old_phone:
                phone.value = new_phone
                return
        raise ValueError("Phone number not found")

    def days_to_birthday(self):
        if self.birthday is None:
            return "Birthday not specified"
        
        today = datetime.date.today()
        next_birthday = datetime.date(today.year, self.birthday.month, self.birthday.day)
        
        if next_birthday < today:
            next_birthday = datetime.date(today.year + 1, self.birthday.month, self.birthday.day)
        
        days_remaining = (next_birthday - today).days
        return days_remaining

    def __str__(self):
        output = f"Name: {self.name.value}\n"
        output += f"Birthday: {self.birthday}\n"
        for phone in self.phones:
            output += f"Phone: {phone.value}\n"
        output += "---------\n"
        return output
    
class AddressBook(dict):
    def __init__(self):
        self.page_size = 10

    def set_page_size(self, size):
        self.page_size = size

    def add_record(self, record):
        self[record.name.value] = record

    def delete_record(self, name):
        del self[name.value]

    def edit_record(self, name, new_record):
        self[name.value] = new_record

    def search_records(self, query):
        search_results = AddressBook()
        for record in self.values():
            if query.lower() in record.name.value.lower():
                search_results.add_record(record)
        return search_results

    def iterator(self):
        records = list(self.values())
        total_pages = (len(records) + self.page_size - 1) // self.page_size

        for page_num in range(total_pages):
            start_idx = page_num * self.page_size
            end_idx = (page_num + 1) * self.page_size
            yield records[start_idx:end_idx]
