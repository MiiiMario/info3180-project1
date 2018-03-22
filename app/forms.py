from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, PasswordField,TextAreaField
from wtforms.validators import InputRequired,DataRequired
from flask_wtf.file import FileAllowed, FileField,FileRequired

class ProForm(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired()])
    lastname = StringField('Last Name', validators=[InputRequired()])
    email = StringField('Email', validators = [DataRequired()])
    gender = SelectField('Gender', choices = [('M', 'Male'), ('F', 'Female')])
    location = StringField('Location', validators=[InputRequired()])
    biography= TextAreaField('Biography', validators=[InputRequired()])
    image = FileField('Profile Picture',validators=[FileRequired(),FileAllowed(['jpg','png'])])