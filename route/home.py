from flask import Blueprint, render_template, url_for, session, redirect, request
from database.mongo import Database as Mongo
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
import json

home_bp = Blueprint('home', __name__)

@home_bp.get('/')
def dashboard():
    if not session.get('loggedin_user'):
        return redirect(url_for('home.loginForm'))
    logs = list(Mongo().db.logs.find({}))
    return render_template('dashboard.html', logs=json.loads(json.dumps(logs, default=str)))

@home_bp.get('/login')
def loginForm():
    if session.get('loggedin_user'):
        return redirect(request.referrer or url_for('home.dashboard'))

    form = LoginForm()
    errors = None
    if session.get('errors'):
        errors = session['errors']
        del session['errors']
    return render_template('login.html', form=form, errors=errors)

@home_bp.get('/register')
def registerForm():
    if session.get('loggedin_user'):
        return redirect(request.referrer or url_for('home.dashboard'))

    form = RegisterForm()
    errors = None
    if session.get('errors'):
        errors = session['errors']
        del session['errors']
    return render_template('register.html', form=form, errors=errors)