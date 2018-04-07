from flask_wtf import FlaskForm
from wtforms import StringField, validators


class TaskForm(FlaskForm):
    description = StringField("Description", [validators.Length(min=1, max=100)])

    class Meta:
        csrf = False
