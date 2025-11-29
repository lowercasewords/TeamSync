# TeamSync

The calendar-management app prototype

## Database Back-End( Users & Events)

Owner: Taka Irizarry billionaire philanthropist/batman/Terry Davis apologist
Packages: entrymode, eventsmodel

### entrymodel (users)

    entrymodel/__init__.py

exposes a singleton UserModel via get_model()
entrymodel/model_sqlite3.py
implements the UserModel class and the users table.

### eventsmodel (events)

    eventsmodel/__init__.py

exposes a singleton EventModel vai get_model()
eventsmodel/mode_sqlite3.py
implements the eventmodel class and the events table.

## Schema

User table schema defined in `entrymodel/modl_sqlite3.py`

```
CREATE TABLE IF NOT EXISTS users (
    id    INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    name  TEXT NOT NULL,
    role  TEXT NOT NULL CHECK(role IN ('read', 'write', 'admin'))
);
```

Events table schema defined in `eventsmodel/model_sqlite3.py`

```
CREATE TABLE IF NOT EXISTS events (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    description TEXT,
    start_time  TEXT NOT NULL,
    end_time    TEXT NOT NULL,
    created_by  INTEGER,
    FOREIGN KEY (created_by) REFERENCES users(id)
);
```

Both tables are stored in `teamsync.db` in root.

## Importing Models

In app.py or any server module:

```
from entrymodel import get_model as get_user_model
from eventsmodel import get_model as get_event_model

users_model = get_user_model()
events_model = get_event_model()
```

## UserModel Methods

| Function Name            | Arguments                                       | Returns                |
| ------------------------ | ----------------------------------------------- | ---------------------- |
| `get_all_users()`        | _(none)_                                        | `list[dict]` all users |
| `get_user_by_email()`    | `email: str`                                    | `dict` or `None`       |
| `create_user()`          | `email: str`, `name: str`, `role: str = "read"` | `int` new user ID      |
| `delete_user_by_id()`    | `user_id: int`                                  | `bool` True if deleted |
| `delete_user_by_email()` | `email: str`                                    | `bool` True if deleted |

## EventModel Methods

| Function Name       | Arguments                                                                              | Returns                   |
| ------------------- | -------------------------------------------------------------------------------------- | ------------------------- | -------------------- |
| `get_all_events()`  | _(none)_                                                                               | `list[dict]` — all events |
| `get_event_by_id()` | `event_id: int`                                                                        | `dict` or `None`          |
| `create_event()`    | `title: str`, `description: str`, `start_time: str`, `end_time: str`, `created_by: int | None = None`              | `int` — new event ID |
| `delete_event()`    | `event_id: int`                                                                        | `bool` — True if deleted  |

## Server Back-End ( MVP Flask App with Sockets)

Owner: Victor Ramirez Garcia

### Flask application

    app.py

This file creates the calendar scheduling flask application with defined routes that are bound
to their respective web pages and handle user requests in real-time via flask websockets. The
following routes are created:

    /

Bound to Login class via HTTP GET and POST

    /logout

Bound to Logout class via HTTP POST

    /dashboard

Bound to Dashboard class via HTTP GET

    /create_event

Bound to Event class via HTTP GET

    /new_user

Bound to User class via HTTP GET

Moreover, the following socket events are created to handle changes in real-time:
| Event Name | Arguments | Returns |
|----|----|----|
| `connect`| _(none)_ | _(none)_ |
| `disconnect`| _(none)_ | _(none)_ |
| `new_user` | `formInfo: dict` with keys `email`, `name`, `role` | `dict` with key `new_user` |
| `delete_user` | `formInfo: dict` with key `user_id` | `dict` with key `user_deleted` |
| `create_event` | `formInfo: dict` with keys `title`, `description`, `start_time`, `end_time`, `created_by` | `dict` with key `new_event` |
| `delete_event` | `formInfo: dict` with key `event_id` | `dict` with key `event_deleted` |

### Presenter files

The following presenter files are implemented as a subclass of Flask's "MethodView":

```
    login.py
```

Login class handles GET and POST requests:

- GET: renders `login.html`
- POST: checks if a given email exists in the database. Redirects to dashboard if true.

```
    dashboard.py
```

Dashboard class handles GET requests:

- GET: renders `index.html`, passing list of users and events

```
    event.py
```

Event class handles GET requests:

- GET: renders `create_event.html`

```
    user.py
```

User class handles GET requests:

- GET: renders `new_user.html`

```
    logout.py
```

Logout class handles POST requests:

- GET: redirects to login.
