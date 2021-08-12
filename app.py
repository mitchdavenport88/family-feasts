import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, IntegerField, TextAreaField, SelectField)
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms_validators import AlphaNumeric, ActiveUrl
from flask_bootstrap import Bootstrap

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
Bootstrap(app)

# Form classes #


# Class for registration form
class RegistrationForm(FlaskForm):
    username = StringField('username',
                           validators=[InputRequired(),
                                       Length(min=5, max=20,
                                       message="username must be between 5 &\
                                           20 characters"),
                                       AlphaNumeric("username can contain\
                                           letters and numbers only")])
    password = PasswordField('password',
                             validators=[InputRequired(),
                                         Length(min=5, max=20,
                                         message="password must be between 5 &\
                                             20 characters")])
    confirm_password = PasswordField('confirm password',
                                     validators=[InputRequired(),
                                                 Length(min=5, max=20,
                                                 message="password must be between\
                                                     5 & 20 characters")])


# Class for login form
class LoginForm(FlaskForm):
    username = StringField('username',
                           validators=[InputRequired(),
                                       Length(min=5, max=20,
                                       message="username should be between 5 &\
                                           20 characters"),
                                       AlphaNumeric("username should contain\
                                           letters and numbers only")])
    password = PasswordField('password',
                             validators=[InputRequired(),
                                         Length(min=5, max=20,
                                         message="password should be between 5 &\
                                             20 characters")])


# Class for add and edit recipe forms
class addRecipeForm(FlaskForm):
    recipe_name = StringField('recipe name',
                              validators=[InputRequired(),
                                          Length(max=35,
                                          message="recipe name can be no longer\
                                              then 35 characters")])
    recipe_image = StringField('recipe image',
                               validators=[InputRequired(),
                                           ActiveUrl(message="must start with\
                                               http:// or https:// and\
                                                   be an active link")])
    category_name = SelectField('category', validators=[InputRequired()])
    servings = IntegerField('servings',
                            validators=[InputRequired(),
                                        NumberRange(min=1, max=100,
                                                    message="value must be\
                                                        between 1-100")])
    prep_time = IntegerField('prep time (mins)',
                             validators=[InputRequired(),
                                         NumberRange(min=0, max=999,
                                                     message="value must be\
                                                         between 0-999")])
    cook_time = IntegerField('cook time (mins)',
                             validators=[InputRequired(),
                                         NumberRange(min=0, max=999,
                                                     message="value must be\
                                                         between 0-999")])
    ingredients = TextAreaField('ingredients', validators=[InputRequired()])
    recipe_steps = TextAreaField('method', validators=[InputRequired()])


# Class for add category form
class addCategoryForm(FlaskForm):
    category_name = StringField('category name',
                                validators=[InputRequired(),
                                            Length(min=1, max=10,
                                                   message="category name\
                                                       should be a maximum of\
                                                           10 characters"),
                                            AlphaNumeric("category name should\
                                                contain letters and numbers\
                                                    only")])


# Routes #


# Home / Index page
@app.route("/")
def home():
    return render_template("index.html",
                           page_title="Home")


# Recipes page
@app.route("/recipes/<filter>")
def recipes(filter):
    categories = [(category["category_name"])
                  for category in mongo.db.categories.find()]
    if session.get("user"):
        user_details = mongo.db.users.find_one({"username": session["user"]})
    else:
        user_details = None
    if filter not in categories and filter != "all":
        flash("this category does not exist!")
        return redirect(url_for("recipes",
                                filter="all"))
    elif filter in categories:
        recipes = list(mongo.db.recipes.find({"category_name": filter}))
    else:
        recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html",
                           recipes=recipes,
                           categories=categories,
                           user_details=user_details,
                           filter=filter,
                           page_title=(filter.title() + " Recipes"))


# Search bar on recipes page
@app.route("/search", methods=["GET", "POST"])
def search():
    search = request.form.get("search")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": search}}))
    categories = [(category["category_name"])
                  for category in mongo.db.categories.find()]
    if session.get("user"):
        user_details = mongo.db.users.find_one({"username": session["user"]})
    else:
        user_details = None
    return render_template("recipes.html",
                           recipes=recipes,
                           filter="search",
                           categories=categories,
                           search=search,
                           user_details=user_details,
                           page_title="Search Results")


# Individual recipe pages
@app.route("/view_recipe/<id>")
def view_recipe(id):
    # Shows individual recipes based on thier db id
    recipe = mongo.db.recipes.find_one_or_404({"_id": ObjectId(id)})
    if session.get("user"):
        user_details = mongo.db.users.find_one({"username": session["user"]})
    else:
        user_details = None
    return render_template("view_recipe.html",
                           recipe=recipe,
                           user_details=user_details,
                           page_title=recipe["recipe_name"])


# Registration form /page
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    # stops access to users that have registered already
    if session.get("user"):
        flash("you're already registered!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    else:
        if form.validate_on_submit():
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            if existing_user:
                flash("the username you've chosen is taken!")
                return redirect(url_for("register"))
            elif (request.form.get("password")
                  == request.form.get("confirm_password")):
                register = {
                    "username": request.form.get("username").lower(),
                    "password": generate_password_hash(
                        request.form.get("password")),
                    "is_admin": bool(False)
                }
                mongo.db.users.insert_one(register)
                session["user"] = request.form.get("username").lower()
                flash("registration complete!")
                return redirect(url_for("user_profile",
                                        username=session["user"]))
            else:
                flash("the passwords entered didn't match!")
                return redirect(url_for("register"))
        return render_template("register.html",
                               page_title="Register",
                               form=form)


# Log in page / form
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # stops access to users that have logged in already
    if session.get("user"):
        flash("you're already logged in!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    else:
        if form.validate_on_submit():
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            if existing_user:
                if check_password_hash(existing_user["password"],
                                       request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    return redirect(url_for("user_profile",
                                            username=session["user"]))
                else:
                    flash("incorrect username or password entered")
                    return redirect(url_for("login"))
            else:
                flash("incorrect username or password entered")
                return redirect(url_for("login"))
        return render_template("login.html",
                               page_title="Log In",
                               form=form)


# Log out function
@app.route("/logout")
def logout():
    # Prevents ability to logout if not logged in
    if session.get("user"):
        session.pop("user")
        return redirect(url_for("login"))
    else:
        flash("you need to be logged in to perform this task!")
        return redirect(url_for("login"))


# Add recipe form / page
@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    form = addRecipeForm()
    form.category_name.choices = [
        ('', 'select one of the following')] + [
            (category['category_name'], category['category_name'])
            for category in mongo.db.categories.find()]
    # Prevents unauthorized access to page
    if not session.get("user"):
        flash("you need to be logged in to perform this task!")
        return redirect(url_for("login"))
    else:
        if form.validate_on_submit():
            # https://www.w3schools.com/python/ref_string_splitlines.asp
            recipe = {
                "recipe_name": request.form.get("recipe_name").title(),
                "recipe_image": request.form.get("recipe_image"),
                "category_name": request.form.get("category_name"),
                "servings": request.form.get("servings"),
                "prep_time": request.form.get("prep_time"),
                "cook_time": request.form.get("cook_time"),
                "ingredients": request.form.get("ingredients").splitlines(),
                "recipe_steps": request.form.get("recipe_steps").splitlines(),
                "author": session["user"]
            }
            mongo.db.recipes.insert_one(recipe)
            return redirect(url_for("view_recipe",
                                    id=recipe["_id"]))
        return render_template("add_recipe.html",
                               page_title="Add Recipe",
                               form=form)


# Edit recipe form / page
@app.route("/edit_recipe/<id>", methods=["GET", "POST"])
def edit_recipe(id):
    recipe = mongo.db.recipes.find_one_or_404({"_id": ObjectId(id)})
    form = addRecipeForm()
    form.category_name.choices = [
        ('', 'select one of the following')] + [
            (category['category_name'], category['category_name'])
            for category in mongo.db.categories.find()]
    # https://stackoverflow.com/questions/12099741/how-do-you-set-a-default-value-for-a-wtforms-selectfield
    # sets the dropdown menu to the recipes category
    form.category_name.data = (recipe["category_name"])
    # inserts the recipe ingredients into the textarea
    form.ingredients.data = ('\n'.join(str(ing)
                             for ing in recipe["ingredients"]))
    # inserts the recipe steps into the textarea
    form.recipe_steps.data = ('\n'.join(str(ing)
                              for ing in recipe["recipe_steps"]))
    # Assigns user details to logged in users
    if session.get("user"):
        user_details = mongo.db.users.find_one({"username": session["user"]})
    # Prevents unauthorized access to page
    if not session.get("user"):
        flash("you need to be a registered user to perform this task!")
        return redirect(url_for("register"))
    # Stops the deletion of recipes created by different users via the URL
    elif session.get("user") != recipe["author"] and not (
         user_details["is_admin"]):
        flash("you can only edit your own entries!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    # grants edit authorization to recipes author or admin
    else:
        if form.validate_on_submit():
            submit = {
                "recipe_name": request.form.get("recipe_name").title(),
                "recipe_image": request.form.get("recipe_image"),
                "category_name": request.form.get("category_name"),
                "servings": request.form.get("servings"),
                "prep_time": request.form.get("prep_time"),
                "cook_time": request.form.get("cook_time"),
                "ingredients": request.form.get("ingredients").splitlines(),
                "recipe_steps": request.form.get("recipe_steps").splitlines(),
                # If admin edit recipe author will remain as
                "author": recipe["author"]
            }
            mongo.db.recipes.update({"_id": ObjectId(id)}, submit)
            flash("your recipe has been updated!")
            return redirect(url_for("view_recipe",
                                    id=recipe["_id"]))
        return render_template("edit_recipe.html",
                               recipe=recipe,
                               page_title="Edit Recipe",
                               form=form)


# Delete recipe function
@app.route("/delete_recipe/<id>")
def delete_recipe(id):
    recipe = mongo.db.recipes.find_one_or_404({"_id": ObjectId(id)})
    # Assigns user details to logged in users
    if session.get("user"):
        user_details = mongo.db.users.find_one({"username": session["user"]})
    # Stops unregistered users or those not logged in deleting recipes
    if not session.get("user"):
        flash("you need to be a registered user to perform this task!")
        return redirect(url_for("register"))
    # Stops the deletion of recipes created by different users via the URL
    elif session.get("user") != recipe["author"] and not (
         user_details["is_admin"]):
        flash("you can only delete your own entries!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    else:
        mongo.db.recipes.delete_one({"_id": ObjectId(id)})
        flash("your recipe has been deleted!")
        return redirect(url_for("user_profile",
                                username=session["user"]))


# User profile page
@app.route("/user_profile/<username>", methods=["GET", "POST"])
def user_profile(username):
    # Prevents unauthorized access to page
    if not session.get("user"):
        flash("you dont have authorization to view this page!")
        return redirect(url_for("login"))
    # Users can only view thier own profile page
    elif username != session.get("user"):
        flash("you dont have authorization to view this page!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    else:
        if session["user"]:
            user_recipes = list(mongo.db.recipes.find(
                {"author": session["user"]}))
            user_details = mongo.db.users.find_one(
                {"username": session["user"]})
            return render_template("user_profile.html",
                                   username=session["user"],
                                   user_recipes=user_recipes,
                                   user_details=user_details,
                                   page_title="My Profile")
        return redirect(url_for("login"))


# Delete profile function
@app.route("/delete_profile/<user>")
def delete_profile(user):
    # Prevents unauthorized access to page
    if not session.get("user"):
        flash("you dont have authorization to perform this task!")
        return redirect(url_for("login"))
    # Users can only delete thier own profile
    elif session.get("user") != user:
        flash("you can only delete your own profile!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    else:
        mongo.db.users.remove({"username": user})
        session.pop("user")
        #  Removes all recipes by the user
        mongo.db.recipes.remove({"author": user})
        return redirect(url_for("home"))


# Add category page
@app.route("/manage_categories", methods=["GET", "POST"])
def manage_categories():
    categories = mongo.db.categories.find()
    # Prevents unauthorized access to page
    if not session.get("user"):
        flash("you dont have authorization to access this page!")
        return redirect(url_for("login"))
    else:
        user_details = mongo.db.users.find_one({"username": session["user"]})
        if not user_details["is_admin"]:
            flash("you dont have authorization to access this page!")
            return redirect(url_for("user_profile",
                                    username=session["user"]))
        elif user_details["is_admin"]:
            form = addCategoryForm()
            if form.validate_on_submit():
                category = {
                    "category_name": request.form.get("category_name").lower()
                }
                mongo.db.categories.insert_one(category)
                flash("the category has been added!")
                return redirect("manage_categories")
            return render_template("manage_categories.html",
                                   form=form,
                                   categories=categories,
                                   page_title="Manage Categories")


# Delete category function
@app.route("/delete_category/<id>", methods=["GET", "POST"])
def delete_category(id):
    if not session.get("user"):
        flash("you dont have authorization to access this page!")
        return redirect(url_for("login"))
    else:
        user_details = mongo.db.users.find_one({"username": session["user"]})
    if not user_details["is_admin"]:
        flash("you dont have authorization to access this page!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    elif user_details["is_admin"]:
        mongo.db.categories.delete_one({"_id": ObjectId(id)})
        flash("the category has been deleted!")
        return redirect(url_for("manage_categories"))


# 404 page not found error
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html",
                           error=e), 404


# 500 internal server error
@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html",
                           error=e), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Change to debug=False before submission
            debug=True)
