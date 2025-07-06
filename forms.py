from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, URL, Email, Length, InputRequired
from flask_ckeditor import CKEditorField

# WTForm for adding a new recipe
class AddRecipeForm(FlaskForm):
    recipe_name = StringField("Recipe Name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired()])
    recipe = CKEditorField("Written Recipe")
    submit = SubmitField("Submit Post")

# Login form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Log In')

# Register Form
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    submit = SubmitField('Create Account')