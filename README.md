# Piloto Challenge

## Introduction

The project will consist of building a simple web server that can store and serve two types email events, open and click. People should be able to get all events related to the client or filter by action, recipient or timestamp.

## User Stories

- As a client, I want to see a list of email events.

- As a client, I want to search for events by action, recipient or timestamp.

- As a client, I want be able to create email events.

- As a client, I want be able retrieve a summery event count for each action (open, click) filterable by recipient or a startDate/endDate combination.

## Proposed Solution

### Stack

- Python
- Django
- Django Rest Framework

### Models

- `Event` <br />
  Represents event that can be made to an email.

  - `action` - REQUIRED CHARFIELD <br />
    Action made on email ("click", "open").
  - `subject` - REQUIRED CHARFIELD <br />
    Email subject
  - `recipient` -REQUIRED EMAILFIELD <br />
    Recipient email address
  - `timestamp` - REQUIRED DATETIMEFIELD <br />
    Optional short description for the escalation in Spanish, intended for display in the product.

### APIS

- GET `/events` <br />
  A route that serve events back to clients as a whole or filtered by action, recipient or timestamp query params. <br />
  Valid query params: <br />

  - action
  - recipient
  - timestamp <br />

  ```
  // Event
  {
    id: "123e4567-e89b-12d3-a456-426614174000",
    action: "click",
    subject: "Subscribe Now",
    recipient: "eric@piloto151.com",
    timestamp: "2021-02-11T13:57:35.780Z"
  }
  ```

  `NOTE: assumption /events return all events since no user management/validation is provided`
  `NOTE: assumption timestamp is in UTC`

- GET `/events/summary` <br />
  A route to serve event count for each action (open, click) filterable by recipient or a start_date/end_date combination. <br />
  Valid query params: <br />

  - recipient
  - start_date and end_date (both must be present) <br />

  ```
  // Event summary
  {
    "open": 5,
    "closed: 10
  }
  ```

  `NOTE: assumption start_date and end_date are inclusive`

- POST `/events` <br />
  A route to handle posting of events <br />
  Request must have: <br />

  - action
  - recipient
  - subject <br />

  ```
  // Event summary
  {
    id: "123e4567-e89b-12d3-a456-426614174000",
    action: "click",
    subject: "Subscribe Now",
    recipient: "eric@piloto151.com",
    timestamp: "2021-02-11T13:57:35.780Z"
  }
  ```

  `NOTE: assumption subject can not be empty`
  `NOTE: assumption subject can not be empty`

## Setup

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

###### OPTIONAL (recommended)

There is a data dump names `test-data.json` that can be imported to populate the database with usable data and a default superuser. To load the data run

```
python manage.py loaddata test-data.json

# user : admin
# pass : 1234

```

To create a new superuser you can run the create super user command and follow the instruction.

```
python manage.py createsuperuser
```

#### LOCAL SERVER

To run a local server use the command

```
python manage.py runserver
```

### How to access admin portal

Create a new superuser, you can run the create super user command and follow the instruction.

```
python manage.py createsuperuser
```

Then go to: `http://localhost:8000/piloto_admin` (if using default port)

### TESTS

To run tests use the `python manage.py test`

### TODO

- Dockerize
- Validate recipient email in query params
- Deploy
