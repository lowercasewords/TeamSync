from flask import render_template
from flask.views import MethodView

class Event(MethodView):
    def get(self):
        return render_template('create_event.html')
