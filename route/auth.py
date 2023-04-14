from flask import Blueprint, request, redirect, url_for, flash
from database.mongo import Database as Mongo
from bson import ObjectId
from werkzeug.exceptions import NotFound, BadRequest
from werkzeug.security import check_password_hash, generate_password_hash
import json

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post('/login')
def login():
    try:
        developer = Mongo().db.developers.find_one({
            'email': request.form['email']
        })
        if not developer:
            raise NotFound('Email is not registred')
        match = check_password_hash(developer.get('password'), request.form['password'])
        if not match:
            raise BadRequest('Password did not match')
        return redirect(url_for('home.dashboard'))
    except Exception as ex:
        flash(ex.__str__())
        return redirect(url_for('home.loginForm'))

@auth_bp.post('/register')
def register():
    try:
        developer = Mongo().db.developers.find_one({
            'email': request.form['email']
        })
        if developer:
            raise BadRequest('Email is already registred')
        if request.form['password'] != request.form['confirm_password']:
            raise BadRequest('Password did not match')
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