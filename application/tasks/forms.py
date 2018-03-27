from flask_wtf import FlaskForm
from wtforms import TextField, validators

class TaskForm(FlaskForm):
    description = TextField("Description", [validators.Length(min=1, max=100)])

    class Meta:
        csrf = False
