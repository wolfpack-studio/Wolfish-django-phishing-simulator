## Getting Started

### Prerequisites
You should have Python 3x installed on your machine.
You should have virtualenv installed. https://realpython.com/python-virtual-environments-a-primer/

### Installation.

Just make a virtual environment in the project directory and activate it.
Then install all the dependencies given in requirements.txt using
#### `pip install -r requirements.txt` 

Let's sync your database with the models.
#### `python manage.py migrate`

Then start the development server.
#### `python manage.py runserver`

Start the server with port custom port and ip.
#### `python manage.py runserver 0.0.0.0:8000`

<br/>
