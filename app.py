from flask import Flask, render_template, url_for
from flask.cli import load_dotenv
from flask_ckeditor import CKEditor
from werkzeug.utils import redirect
from forms import AddRecipeForm
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
ckeditor = CKEditor(app)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add_new_recipe", methods =['POST', 'GET'])
def add_recipe():
    form = AddRecipeForm()
    if form.validate_on_submit():
        print(form.recipe_name.data)
        return redirect(url_for('home'))
    return render_template("add_recipe.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
