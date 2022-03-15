from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [DataRequired()])
    submit = SubmitField('Submit')
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    # category = SelectField('Categories', choices=[('Interview Pitch', 'Interview Pitch'), 
    # ('Product Pitch', 'Product Pitch'), ('Personal Pitch', 'Personal Pitch'), 
    # ('Education Pitch', 'Education Pitch'), ('Experience Pitch', 'Experience Pitch'),
    # ('Family Pitch', 'Family Pitch')], validators=[DataRequired()])
    submit = SubmitField('Post')
    
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit')
