from flask_wtf import FlaskForm
from wtforms import PasswordField, TextField, validators

class LoginForm(FlaskForm):
    username = TextField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.Length(min=7)])

    class Meta:
        csrf = False

class RegistrationForm(FlaskForm):
    username = TextField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.Length(min=7), validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat password')

    class Meta:
        csrf = False
