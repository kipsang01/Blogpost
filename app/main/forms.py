from flask_wtf import FlaskForm
from flask_mde import Mde, MdeField
from wtforms import SubmitField,StringField,RadioField,TextAreaField
from wtforms.validators import InputRequired


class PostForm(FlaskForm):
    title =  StringField('Title:',validators = [InputRequired()])
    category = RadioField('Category:', choices=[('politics','Politics'),('technology','Technology'),('business','Business'),('fashion','Fashion')])
    editor = MdeField('Content:')
    submit = SubmitField('Submit')
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment:',validators=[InputRequired()])
    submit = SubmitField('Post')
    
class AddBioForm(FlaskForm):
    bio = TextAreaField('Bio:',validators=[InputRequired()])
    submit = SubmitField('Post')
    