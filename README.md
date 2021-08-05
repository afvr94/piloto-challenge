# Piloto Challenge

## Introduction

The project will consist of building a simple web server that can store and serve two types email events, open and click. People should be able to get all events related to the client or filter by action, recipient or timestamp.

## User Stories

- As a client, I want to see a list of email events.

- As a client, I want to search for events by action, recipient or timestamp.

- As a client, I want be able to create email events.

- As a client, I want be able retrieve a summery event count for each action (open, click) filterable by recipient or a startDate/endDate combination.

## How To

To run the backend locally is recommended to create a virtual environment.

```
pip install virtualenv
virtualenv venv

# Activate environment
source venv/bin/activate
```

With the virtual environment activated we can install all the required python libraries. To install all dependencies run:

```
pip install -r requirements.txt
```

Once inside the folder the database must be initialize by running

```
python manage.py migrate
```

This will generate a new SQLite database with all the data structure necessary to run the application.

#### LOCAL SERVER

To run a local server use the command

```
python manage.py runserver
```

#### TESTS

To run tests use the `python manage.py test`
