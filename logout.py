from flask import url_for, redirect
from flask.views import MethodView

class Logout(MethodView):
    def post(self):
        return redirect(url_for('login'))
