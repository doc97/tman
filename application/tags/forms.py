from flask_wtf import FlaskForm
from wtforms import StringField, validators


class TagForm(FlaskForm):
    name = StringField("Name", [validators.Length(min=1, max=20)])

    class Meta:
        csrf = False
