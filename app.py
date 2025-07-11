from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask.cli import load_dotenv
from flask_ckeditor import CKEditor
from werkzeug.utils import redirect
from flask_wtf.csrf import CSRFProtect
from forms import AddRecipeForm, LoginForm, RegisterForm
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ckeditor = CKEditor(app)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
# If user attempts to access a login required route:
login_manager.login_view = 'login'

# Flask login will load a user from the database through their id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Unique ID for each user
    email = db.Column(db.String(150), unique=True, nullable=False)  # Email must be unique
    password = db.Column(db.String(256), nullable=False)  # Store hashed password

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
    return render_template("index.html", recipe_list = recipes, user=current_user)

@app.route("/login")
def login():
#     if logged in go home
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check email and password.')

    return render_template('login.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
    #     Check if user is already in database
        result = db.session.execute(db.select(User).where(User.email == form.email.data))
        user = result.scalar()
        if user:
    #         if user exists
            flash("This email is already registered, login instead")
            return redirect(url_for('login'))

    #         hash password
        hashed_and_salted_password = generate_password_hash(form.password.data,
            method = 'pbkdf2:sha256',
            salt_length= 8
            )
        user = User(
            email = form.email.data,
            password = hashed_and_salted_password,
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))





    return render_template("register.html", form=form)

@app.route("/planner")
def planner():
    return render_template("planner.html")

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
    app.run(debug=False, port=8003)
