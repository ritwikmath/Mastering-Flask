from flask import Blueprint, render_template
from database.mongo import Database as Mongo
import json

home_bp = Blueprint('home', __name__)

@home_bp.get('/')
def dashboard():
    logs = list(Mongo().db.logs.find({}))
    return render_template('index.html', logs=json.loads(json.dumps(logs, default=str)))