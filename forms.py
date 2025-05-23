from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

# WTForm for adding a new recipe
class AddRecipeForm(FlaskForm):
    recipe_name = StringField("Recipe Name", validators=[DataRequired()])
    url = StringField("URL", validators=[DataRequired()])
    recipe = CKEditorField("Written Recipe")
    submit = SubmitField("Submit Post")