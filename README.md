# TeamSync
The calendar-management app prototype

## Database Back-End( Users & Events)
Owner: Taka Irizarry
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
| Function Name | Arguments | Returns  |
|----|----|----|
| `get_all_users()` | *(none)*  | `list[dict]`  all users |
| `get_user_by_email()`  | `email: str` | `dict` or `None`  |
| `create_user()` | `email: str`, `name: str`, `role: str = "read"` | `int`  new user ID |
| `delete_user_by_id()`  | `user_id: int` | `bool`  True if deleted |
| `delete_user_by_email()`| `email: str`  | `bool` True if deleted |

## EventModel Methods

| Function Name | Arguments | Returns |
|----|----|----|
| `get_all_events()`| *(none)* | `list[dict]` — all events |
| `get_event_by_id()` | `event_id: int` | `dict` or `None` |
| `create_event()`  | `title: str`, `description: str`, `start_time: str`, `end_time: str`, `created_by: int | None = None` | `int` — new event ID  |
| `delete_event()`| `event_id: int` | `bool` — True if deleted |
