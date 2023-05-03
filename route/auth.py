from flask import Blueprint, request, redirect, url_for, flash, session
from database.mongo import Database as Mongo
from bson import ObjectId
from werkzeug.exceptions import NotFound, BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
import json
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post('/login')
def login():
    try:
        form = LoginForm(request.form)
        if not form.validate():
            session['errors'] = form.errors
            return redirect(url_for('home.loginForm'))
        developer = Mongo().db.developers.find_one({
            'email': request.form['email']
        })
        del developer['password']
        session['loggedin_user'] = json.loads(json.dumps(developer, default=str))
        return redirect(url_for('home.dashboard'))
    except Exception as ex:
        flash(ex.__str__())
        return redirect(url_for('home.loginForm'))

@auth_bp.post('/register')
def register():
    try:
        form = RegisterForm(request.form)
        if not form.validate():
            session['errors'] = form.errors
            return redirect(url_for('home.registerForm'))
        password = generate_password_hash(request.form['password'], method='pbkdf2:sha256', salt_length=9)
        skills = request.form['skills'].split(',')
        Mongo().db.developers.insert_one({
            'name': request.form['name'],
            'skills': skills,
            'password': password,
            'email': request.form['email']
        })
        return redirect(url_for('home.loginForm'))
    except Exception as ex:
        flash(ex.__str__())
        return redirect(url_for('home.registerForm'))

@auth_bp.post('/logout')
def logout():
    try:
        session.pop('loggedin_user')
        return redirect(url_for('home.loginForm'))
    except Exception as ex:
        Mongo().db.logs.insert_one({
            'type': 'error',
            'url': request.url,
            'message': ex.__str__()
        })
        return {'status': False, 'error': ex.__str__()}