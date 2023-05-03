from wtforms import Form, EmailField, validators, PasswordField, ValidationError
from database.mongo import Database as Mongo
from werkzeug.security import check_password_hash

class LoginForm(Form):
    email = EmailField('Email', validators=[
        validators.input_required(message='Email is required'), 
        validators.regexp('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}', message='Invalid email')
    ])
    password = PasswordField('Password', validators=[
        validators.input_required(message='Password is required'),
        validators.length(min=8, message="Password must be a minimum of 8 characters")
    ])

    def validate_email(form, field):
        developer = Mongo().db.developers.find_one({
            'email': field.data
        })
        if not developer:
            raise ValidationError('Email is not registred')
    
    def validate_password(form, field):
        developer = Mongo().db.developers.find_one({
            'email': form.email.data
        })
        if not developer:
            return
        match = check_password_hash(developer.get('password'), field.data)
        if not match:
            raise ValidationError('Password did not match')