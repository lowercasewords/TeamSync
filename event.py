from flask import render_template, session, redirect, url_for, abort
from flask.views import MethodView

class Event(MethodView):
    def get(self):
        user = session.get("user")
        if user is None:
            return redirect(url_for('login'))
        elif user["role"] == "read":
            abort(403, "Invalid permissions")
        else:
            return render_template('create_event.html', user=user)
