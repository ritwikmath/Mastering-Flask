from flask import Blueprint, render_template
from database.mongo import Database as Mongo
import json

home_bp = Blueprint('home', __name__)

@home_bp.get('/')
def dashboard():
    logs = list(Mongo().db.logs.find({}))
    return render_template('dashboard.html', logs=json.loads(json.dumps(logs, default=str)))

@home_bp.get('/login')
def loginForm():
    return render_template('login.html')

@home_bp.get('/register')
def registerForm():
    return render_template('register.html')