from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.cli import load_dotenv
from flask_ckeditor import CKEditor
from werkzeug.utils import redirect
from flask_wtf.csrf import CSRFProtect
from forms import AddRecipeForm
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ckeditor = CKEditor(app)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    recipe_name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(200))
    recipe = db.Column(db.Text)

# for debugging
    def __repr__(self):
        return f'<Recipe {self.recipe_name}>'

with app.app_context():
    db.create_all()


# Routes
@app.route("/")
def home():
    recipes = Recipe.query.all()
    return render_template("index.html", recipe_list = recipes)

@app.route("/all_recipes")
def all_recipes():
    recipes = Recipe.query.all()
    return render_template("all_recipes.html", recipe_list = recipes)

@app.route("/breakfast_recipes")
def breakfast_recipes():
    return render_template("breakfast_recipes.html")

@app.route("/lunch_recipes")
def lunch_recipes():
    return render_template("lunch_recipes.html")

@app.route("/dinner_recipes")
def dinner_recipes():
    return render_template("dinner_recipes.html")

@app.route("/dessert_recipes")
def dessert_recipes():
    return render_template("dessert_recipes.html")

@app.route("/drink_recipes")
def drink_recipes():
    return render_template("drink_recipes.html")

@app.route("/side_dish_recipes")
def side_dish_recipes():
    return render_template("side_dish_recipes.html")

@app.route("/breads_and_baked_goods")
def breads_and_baked_goods_recipes():
    return render_template("breads_and_baked_goods_recipes.html")

@app.route("/soups_and_stews_recipes")
def soups_and_stews_recipes():
    return render_template("soups_and_stews_recipes.html")

@app.route("/condiments_and_staples")
def condiments_and_staples():
    return render_template("condiments_and_staples.html")


@app.route("/add_new_recipe", methods =['POST', 'GET'])
def add_recipe():
    form = AddRecipeForm()
    if form.validate_on_submit():

        # append values to db table
        new_recipe = Recipe(
            recipe_name = form.recipe_name.data,
            url = form.url.data,
            recipe=form.recipe.data
        )
        db.session.add(new_recipe)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add_recipe.html", form=form)

if __name__ == "__main__":
    app.run(debug=False)
