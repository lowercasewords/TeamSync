# TeamSync

The calendar-management app prototype

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
| Event Name | Arguments | Response Event Name | Returns |
|----|----|----|----|
| `connect`| _(none)_ | _(none)_ | _(none)_ |
| `disconnect`| _(none)_ | _(none)_ | _(none)_ |
| `new_user` | `formInfo: dict` with keys `email`, `name`, `role` | `updated_users` | `dict` with key `new_user` |
| `delete_user` | `formInfo: dict` with key `user_id` | `updated_users` | `dict` with key `user_deleted` |
| `create_event` | `formInfo: dict` with keys `title`, `description`, `start_time`, `end_time`, `created_by` | `updated_events` | `dict` with key `new_event` |
| `delete_event` | `formInfo: dict` with key `event_id` | `updated_events` | `dict` with key `event_deleted` |

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
