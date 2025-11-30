from flask import Flask, session
from flask_socketio import SocketIO, emit
from flask.views import MethodView
from login import Login
from logout import Logout
from dashboard import Dashboard
from event import Event
from user import User
from entrymodel import get_model as get_user_model
from eventsmodel import get_model as get_event_model

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
                 methods=["GET"])

app.add_url_rule('/create_event',
                 view_func=Event.as_view('create_event'),
                 methods=["GET"])

app.add_url_rule('/new_user',
                 view_func=User.as_view('new_user'),
                 methods=["GET"])

@socketio.on('connect')
def connect():
    user = session.get("user")
    if not user:
        return
    else:
        print('user has connected')

@socketio.on('disconnect')
def disconnect():
    user = session.get("user")
    if not user:
        return
    else:
        print('user has disconnected')

@socketio.on('new_user')
def new_user(form_info):
    user = session.get("user")
    if not user:
        return
    else:
        users_model = get_user_model()
        user_email = users_model.create_user(form_info['email'], form_info['name'], form_info['role'])
        new_user = users_model.get_user_by_email(user_email)
        emit('updated_users', {'new_user': new_user}, broadcast=True)
        
@socketio.on('delete_user')
def delete_user(form_info):
    user = session.get("user")
    if not user:
        return
    else:
        users_model = get_user_model()
        user_deleted = users_model.delete_user_by_id(form_info['user_id'])
        if user_deleted is True:
            emit('updated_users', {'user_deleted': form_info['user_id']}, broadcast=True)

@socketio.on('create_event')
def create_event(form_info):
    user = session.get("user")
    if not user:
        return
    else:
        events_model = get_event_model()
        event_id = events_model.create_event(form_info['title'], form_info['description'], form_info['start_time'], form_info['end_time'], form_info['created_by'])
        created_event = events_model.get_event_by_id(event_id)
        emit('updated_events', {'new_event': created_event}, broadcast=True)

@socketio.on('delete_event')
def delete_event(form_info):
    user = session.get("user")
    if not user:
        return
    else:
        events_model = get_event_model()
        event_deleted = events_model.delete_event(form_info['event_id'])
        if event_deleted is True:
            emit('updated_events', {'event_deleted': form_info['event_id']}, broadcast=True)
        
if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True) # debug=True enables reloader and debugger for development
