from flask import render_template, session, redirect, url_for
from flask.views import MethodView
from entrymodel import get_model as get_user_model
from eventsmodel import get_model as get_event_model

class Dashboard(MethodView):
    def get(self):
        user = session.get('user')
        if user is None:
            return redirect(url_for('login'))
        else:
            users_model = get_user_model();
            events_model = get_event_model();
            users = users_model.get_all_users();
            events = events_model.get_all_events();
            return render_template('index.html', users=users, events=events, user=user)
