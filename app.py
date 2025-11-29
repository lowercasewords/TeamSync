from flask import Flask, session
from flask_socketio import SocketIO, emit
from flask.views import MethodView
from login import Login
from logout import Logout
from dashboard import Dashboard
from event import Event
from user import User

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

@socketio.on("connect")
def connect():
    user = session.get("user")
    if type(user) is None:
        return
    else:
        emit("connect-after", {"user": user, "msg": "user has entered"})

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True) # debug=True enables reloader and debugger for development
