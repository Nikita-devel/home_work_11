# home_work_11

# Address Book Assistant

The Address Book Assistant is a simple command-line application that allows you to manage contacts in an address book. You can add, edit, delete, and search for contacts, as well as get weather information and the current time. The assistant also supports adding and tracking the birthdays of your contacts.

## Getting Started

### Prerequisites

- Python 3.6 or higher

### Installation

1. Clone this repository to your local machine or download the ZIP file.

2. Open a terminal or command prompt and navigate to the project directory.

3. It's recommended to create a virtual environment to manage dependencies:

   python -m venv venv


4. Activate the virtual environment:

   - On Windows:

   venv\Scripts\activate


   - On macOS and Linux:

   source venv/bin/activate


5. Install the required dependencies from the `requirements.txt` file:

   pip install -r requirements.txt


### Usage

To start the Address Book Assistant, run the `main.py` script:

python main.py


Once the assistant is running, you can interact with it using commands:

- To add a contact:

  add <name> <phone> [birthday]

  If the `birthday` argument is provided in the format "DD/MM," the assistant will add the contact's birthday.

- To change a contact's phone number:

  change <name> <old_phone> <new_phone>


- To get the phone number(s) of a contact:

  phone <name>


- To show all saved contacts with pagination (default page size is 10):

  show all


- To get the current weather in a specified city:

  weather <city>


- To get the current time:

  time


- To see available commands:

  help


- To exit the assistant:

  goodbye, close, bye, good, exit


## Contributing

Contributions to this project are welcome. If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.
