# CarAPI
System for receiving and sending data to the Pi remotely.

## Setup
1. Clone this repository
2. Open a terminal, and navigate inside the repository
3. Follow a tutorial ([like this one](http://docs.python-guide.org/en/latest/dev/virtualenvs/)) on how to set up virtualenv. 
Remember to use Python 3.4.
4. Active the virtualenv. Assuming you named the folder venv, run `source venv/bin/activate`
4. Run `pip install -r requirements.txt`
6. Run `python manage.py makemigrations api`
7. Run `python manage.py migrate`
8. Run `python manage.py createsuperuser`, and follow the prompts to create a local user for the system.

## Settings
You can make the server delete messages when they are sent by setting `DELETE_FETCHED_MESSAGES` to True in `carapi/settings.py`.

## How to run test server
Run `python manage.py runserver 34446` to run a server appropiate for development use.

## How to use
1. With the server and PI (see PI/readme) up and running, navigate to `http://localhost:34446/` to see a deployed version of this in action.
2. To see what messages that can be stored, navigate to `http://localhost:34446/admin` and log in with the user and password you created.

## Protocol / message format
See https://github.com/BoreasCarSystem/PI/blob/master/Protocols.md
