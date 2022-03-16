from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired
# from flask_uploads import  configure_uploads, UploadSet, IMAGES, patch_request_class
from flask_wtf.file import FileField, FileRequired, FileAllowed
    
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [DataRequired()])
    submit = SubmitField('Submit')
    
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
    
    
class CommentForm(FlaskForm):
    comment = TextAreaField('Comment')
    submit = SubmitField('Submit')

class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed('Image only!'), FileRequired('File was empty!')])
    submit = SubmitField('Upload')
