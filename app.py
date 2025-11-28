from flask import Flask
from flask_socketio import SocketIO, emit
from flask.views import MethodView
from login import Login
from dashboard import Dashboard
from event import Event
from user import User

app = Flask(__name__)
socketio = SocketIO(app)

app.add_url_rule('/login',
                 view_fun=Login.as_view('login'),
                 methods=["GET", "POST"])

app.add_url_rule('/dashboard',
                 view_fun=Dashboard.as_view('dashboard'),
                 methods=["GET"])

app.add_url_rule('/event',
                 view_fun=Event.as_view('event'),
                 methods=["GET", "POST"])

app.add_url_rule('/user',
                 view_fun=User.as_view('user'),
                 methods=["GET", "POST"])

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True) # debug=True enables reloader and debugger for development
