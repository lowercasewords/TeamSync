from flask import render_template, session, redirect, url_for
from flask.views import MethodView

class User(MethodView):
    def get(self):
        user = session.get('user')
        if user is None:
            return redirect(url_for('login'))
        else:
            return render_template('new_user.html', user=user)
