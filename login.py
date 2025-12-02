from flask import render_template, request, url_for, redirect, session
from flask.views import MethodView
from entrymodel import get_model as get_user_model

class Login(MethodView):
    def get(self):
        session.clear()
        return render_template("login.html")
    def post(self):
        users_model = get_user_model()
        user = users_model.get_user_by_email(request.form['email'])
        if user is None:
            return self.get()
        else:
            session["user"] = user
            return redirect(url_for('dashboard', user=user['email']))
