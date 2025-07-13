from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, URL, Email, Length, InputRequired
from flask_ckeditor import CKEditorField

CATEGORY_CHOICES = [
    ("", "-- Select Category --"),
    ("Breakfast", "Breakfast"),
    ("Lunch", "Lunch"),
    ("Dinner", "Dinner"),
    ("Side Dishes", "Side Dishes"),
    ("Desserts", "Desserts"),
    ("Drinks", "Drinks"),
    ("Breads & Baked Goods", "Breads & Baked Goods"),
    ("Soups & Stews", "Soups & Stews"),
    ("Condiments & Staples", "Condiments & Staples"),
]
# WTForm for adding a new recipe
class AddRecipeForm(FlaskForm):
    category = SelectField(label="Category", choices= CATEGORY_CHOICES, validators=[InputRequired(message="Please select a category.")])
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