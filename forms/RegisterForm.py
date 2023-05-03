from wtforms import validators, StringField, PasswordField, ValidationError
from database.mongo import Database as Mongo
from forms.LoginForm import LoginForm

class RegisterForm(LoginForm):
    skills = StringField('Skills', validators=[
        validators.input_required(message="Skills is required")
    ])
    name = StringField('Name', validators=[
        validators.input_required(message="Name is required")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        validators.input_required(message="Confirm Password is required"),
        validators.length(min=8, message="Confirm Password must be a minimum of 8 characters")
    ])

    def validate_email(form, field):
        developer = Mongo().db.developers.find_one({
            'email': field.data
        })
        if developer:
            raise ValidationError('Email is already registred')
    
    def validate_confirm_password(form, field):
        if form.password.data != field.data:
            raise ValidationError('Password did not match')