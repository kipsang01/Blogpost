from flask_wtf import FlaskForm
from flask_mde import Mde, MdeField
from wtforms import SubmitField,StringField,RadioField
from wtforms.validators import InputRequired


class PostForm(FlaskForm):
    title =  StringField('Enter title:',validators = [InputRequired()])
    category = RadioField('Category:', choices=[('politics','Politics'),('technology','Technology'),('business','Business'),('fashion','Fashion')])
    editor = MdeField('content')
    submit = SubmitField('Submit')