from flask import render_template
from flask.views import MethodView

class User(MethodView):
    def get(self):
        return render_template('new_user.html')
