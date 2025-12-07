from flask import Flask, abort, session, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask.views import MethodView
from login import Login
from logout import Logout
from dashboard import Dashboard
from event import Event
from user import User
from entrymodel import get_model as get_user_model
from eventsmodel import get_model as get_event_model

from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "TeamSync Pro S++ 2.0 Demo"
socketio = SocketIO(app)

app.add_url_rule('/',
                 view_func=Login.as_view('login'),
                 methods=["GET", "POST"])

app.add_url_rule('/logout',
                 view_func=Logout.as_view('logout'),
                 methods=["POST"])

app.add_url_rule('/dashboard',
                 view_func=Dashboard.as_view('dashboard'),
                 methods=["GET", "POST"])

app.add_url_rule('/create_event',
                 view_func=Event.as_view('create_event'),
                 methods=["GET"])

app.add_url_rule('/new_user',
                 view_func=User.as_view('new_user'),
                 methods=["GET"])

# Display the html's "datetime-local" in a more human-readable format
@app.template_filter("format_datetime")
def format_datetime(value):
    try:
        dt = datetime.fromisoformat(value)
        return dt.strftime("%B %d, %Y")  # "Month Day, Year" formatting on the client
    # Just in case if the original formatting was not correct
    except:
        return value

users = {}

@socketio.on('connect')
def handle_connect():
    user = request.args.get("user")
    sid = request.sid
    if user == session.get("user")['email']:
        users[sid] = user
        print(session.get("user"))
        print(f"1: user {user} has connected")
    else:
        users_model = get_user_model()
        session['user'] = users_model.get_user_by_email(user)
        users[sid] = user
        print(session.get("user"))
        print(f"2: user {user} has connected")

@socketio.on('disconnect')
def handle_disconnect(data=None):
    user = users.pop(request.sid, None)
    print(f"user {user} has disconnected")

@socketio.on('new_user')
def new_user(form_info):
    user = users.get(request.sid)
    if not user:
        return
    else:
        users_model = get_user_model()
        user_email = users_model.create_user(form_info['email'], form_info['name'], form_info['role'])
        if user_email == None:
            # Couldn't add a user: (Duplicate users, etc)
            # abort(403, "Duplicate user error")
            # print("works")
            # emit('updated_users', {'new_user': user}, broadcast=True)
            pass
        else:
            new_user = users_model.get_user_by_email(user_email)
            emit('updated_users', {'new_user': new_user}, broadcast=True)
            # redirect(url_for('dashboard', user=user.email))
        
@socketio.on('delete_user')
def delete_user(form_info):
    user = users.get(request.sid)
    role = session.get("user")['role']
    if not user:
        return
    elif role != 'admin':
        abort(403, "Invalid permissions")
    else:
        users_model = get_user_model()
        user_deleted = users_model.delete_user_by_id(form_info['user_id'])
        if user_deleted is True:
            emit('updated_users', {'user_deleted': form_info['user_id']}, broadcast=True)

@socketio.on('create_event')
def create_event(form_info):
    user = users.get(request.sid)
    if not user:
        return
    else:
        events_model = get_event_model()
        event_id = events_model.create_event(form_info['title'], form_info['description'], form_info['start_time'], form_info['end_time'], form_info['created_by'])
        created_event = events_model.get_event_by_id(event_id)
        emit('updated_events', {'new_event': created_event}, broadcast=True)

@socketio.on('delete_event')
def delete_event(form_info):
    user = users.get(request.sid)
    if not user:
        return
    else:
        events_model = get_event_model()
        event_deleted = events_model.delete_event(form_info['event_id'])
        if event_deleted is True:
            emit('updated_events', {'event_deleted': form_info['event_id']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True) # debug=True enables reloader and debugger for development
