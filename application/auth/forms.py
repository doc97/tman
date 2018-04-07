from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, BooleanField, validators


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [validators.Length(min=7)])
    remember = BooleanField('Remember me')

    class Meta:
        csrf = False


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired()])
    password = PasswordField('Password', [
        validators.Length(min=7),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat password')

    class Meta:
        csrf = False
