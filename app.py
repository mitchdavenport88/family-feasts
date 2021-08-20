import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
from forms import RegistrationForm, LoginForm, AddRecipeForm, AddCategoryForm

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)
Bootstrap(app)


@app.route("/")
def home():
    """Renders home page / index page."""
    return render_template("index.html",
                           page_title="Home")


@app.route("/recipes/<filter>")
def recipes(filter):
    """
    Renders recipes page. Accepts the input of filter, which is used to apply
    a filter that determines what recipes are shown. All recipes will show
    if filter is "all" or not in categories list.
    """
    if session.get("user"):
        # Create variable used to check admin rights/privileges on the page.
        user_details = mongo.db.users.find_one({"username": session["user"]})
    else:
        user_details = None
    # Create a list of category names to dynamically add buttons.
    categories = [(category["category_name"])
                  for category in mongo.db.categories.find()]
    # If the name passed into the function isnt on the categories list we use
    # the value "all" as the argument.
    if filter not in categories and filter != "all":
        flash("this category does not exist!")
        return redirect(url_for("recipes",
                                filter="all"))
    # If the name is on the categories list we show the relevent recipes.
    elif filter in categories:
        recipes = list(mongo.db.recipes.find({"category_name": filter}))
    # Page will show all recipes otherwise.
    else:
        recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html",
                           recipes=recipes,
                           categories=categories,
                           user_details=user_details,
                           filter=filter,
                           page_title=(filter.title() + " Recipes"))


@app.route("/search", methods=["GET", "POST"])
def search():
    """Search bar function found on recipes page."""
    if session.get("user"):
        # Create variable used to check admin rights/privileges on the page.
        user_details = mongo.db.users.find_one({"username": session["user"]})
    else:
        user_details = None
    # Assigns the input from the searchbar to a variable.
    search = request.form.get("search")
    # Assigns the search results to a variable.
    recipes = list(mongo.db.recipes.find({"$text": {"$search": search}}))
    # Create a list of category names to dynamically add buttons.
    categories = [(category["category_name"])
                  for category in mongo.db.categories.find()]
    return render_template("recipes.html",
                           recipes=recipes,
                           filter="search",
                           categories=categories,
                           search=search,
                           user_details=user_details,
                           page_title="Search Results")


@app.route("/view_recipe/<id>")
def view_recipe(id):
    """
    Renders individual recipe pages. The input id is the _id that the recipe
    is allocated in MongoDB. We use this to find and render the data for
    the recipe on the page.
    """
    if session.get("user"):
        # Create variable used to check admin rights/privileges on the page.
        user_details = mongo.db.users.find_one({"username": session["user"]})
    else:
        user_details = None
    # Finds data using the id provided and assigns it to variable to render.
    recipe = mongo.db.recipes.find_one_or_404({"_id": ObjectId(id)})
    return render_template("view_recipe.html",
                           recipe=recipe,
                           user_details=user_details,
                           page_title=recipe["recipe_name"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Renders registration page. Validates and adds data given
    by the user to the db.
    """
    # Stops access to users that have registered already.
    if session.get("user"):
        flash("you're already registered!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    else:
        # RegistrationForm class found in forms.py.
        form = RegistrationForm()
        if form.validate_on_submit():
            # Used to check if username already exists in db.
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            if existing_user:
                flash("the username you've chosen is taken!")
                return redirect(url_for("register"))
            # Passwords given need to match to complete registration.
            elif (request.form.get("password") ==
                  request.form.get("confirm_password")):
                register = {
                    "username": request.form.get("username").lower(),
                    "password": generate_password_hash(
                        request.form.get("password")),
                    "is_admin": False
                }
                mongo.db.users.insert_one(register)
                # Session cookie assigned.
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


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Renders log in page. Validates and checks data given by the user and
    grants/denies entry to the site accordingly.
    """
    # Stops access to users that have logged in already.
    if session.get("user"):
        flash("you're already logged in!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    else:
        # LoginForm class found in forms.py.
        form = LoginForm()
        if form.validate_on_submit():
            # Used to check if username exists in db.
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            if existing_user:
                # Checks password exists in db for that specific user.
                if check_password_hash(existing_user["password"],
                                       request.form.get("password")):
                    # Session cookie assigned and sent to user profile.
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


@app.route("/logout")
def logout():
    """Log out function."""
    # Checks if they're logged in.
    if session.get("user"):
        # Removes session cookie.
        session.pop("user")
        flash("you've been logged out!")
        return redirect(url_for("login"))
    # Stops access to users that haven't logged in yet.
    else:
        flash("you need to be logged in to perform this task!")
        return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """
    Renders add recipe page. Validates and adds data given
    by the user to the db.
    """
    # Stops access to users that aren't registed or logged in.
    if not session.get("user"):
        flash("you need to be logged in to perform this task!")
        return redirect(url_for("login"))
    else:
        # AddRecipeForm class found in forms.py.
        form = AddRecipeForm()
        # Applies the options and values shown in the dropdown menu.
        # These are dynamically generated from the categories collection in db.
        # https://stackoverflow.com/questions/28133859/how-to-populate-wtform-select-field-using-mongokit-pymongo
        form.category_name.choices = [
            ('', 'select one of the following')] + [
                (category['category_name'], category['category_name'])
                for category in mongo.db.categories.find()]
        if form.validate_on_submit():
            # Splitlines turn string into a list when each list item is on a
            # newline within the textarea. Found this on w3schools.
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


@app.route("/edit_recipe/<id>", methods=["GET", "POST"])
def edit_recipe(id):
    """
    Renders edit recipe page. Prepopulates the form with existing data pulled
    from the db by using the id value passed in to find it. Data then gets
    re-validated before getting added back into the db.
    """
    # Stops access to users that aren't registed or logged in.
    if not session.get("user"):
        flash("you need to be a registered user to perform this task!")
        return redirect(url_for("register"))
    else:
        # Creates variable used to check admin rights.
        user_details = mongo.db.users.find_one({"username": session["user"]})
        recipe = mongo.db.recipes.find_one_or_404({"_id": ObjectId(id)})
    # Stops the editing of recipes created by different users via the URL.
    if session.get("user") != recipe["author"] and not (
         user_details["is_admin"]):
        flash("you can only edit your own entries!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    # Allows authorization to edit recipes to recipe author or admin.
    else:
        # AddRecipeForm class found in forms.py.
        form = AddRecipeForm()
        form.category_name.choices = [
            ('', 'select one of the following')] + [
                (category['category_name'], category['category_name'])
                for category in mongo.db.categories.find()]
        if recipe["category_name"] not in list(category['category_name']
                                               for category in
                                               mongo.db.categories.find()):
            form.category_name.data = ('')
        else:
            # Sets dropdown option to match that given when recipe was added.
            # https://stackoverflow.com/questions/12099741/how-do-you-set-a-default-value-for-a-wtforms-selectfield
            form.category_name.data = (recipe["category_name"])
        # Inserts the ingredients in the textarea with each item on a new line.
        form.ingredients.data = ('\n'.join(str(ing)
                                 for ing in recipe["ingredients"]))
        # Inserts the steps in the textarea with each item on a new line.
        form.recipe_steps.data = ('\n'.join(str(ing)
                                  for ing in recipe["recipe_steps"]))
        if form.validate_on_submit():
            submit = {"$set": {
                "recipe_name": request.form.get("recipe_name").title(),
                "recipe_image": request.form.get("recipe_image"),
                "category_name": request.form.get("category_name"),
                "servings": request.form.get("servings"),
                "prep_time": request.form.get("prep_time"),
                "cook_time": request.form.get("cook_time"),
                "ingredients": request.form.get("ingredients").splitlines(),
                "recipe_steps": request.form.get("recipe_steps").splitlines(),
                # If admin edits recipe original author will remain.
                "author": recipe["author"]
            }}
            mongo.db.recipes.update_one({"_id": ObjectId(id)}, submit)
            flash("your recipe has been updated!")
            return redirect(url_for("view_recipe",
                                    id=recipe["_id"]))
        return render_template("edit_recipe.html",
                               recipe=recipe,
                               page_title="Edit Recipe",
                               form=form)


@app.route("/delete_recipe/<id>")
def delete_recipe(id):
    """
    Delete recipe function. The id passed into the function identifies the
    recipe for deletion. The checks are then done to check they are the author
    or have admin rights. The recipe is then removed from the database.
    """
    # Stops access to users that aren't registed or logged in.
    if not session.get("user"):
        flash("you need to be a registered user to perform this task!")
        return redirect(url_for("register"))
    else:
        recipe = mongo.db.recipes.find_one_or_404({"_id": ObjectId(id)})
        # Creates variable used to check admin rights.
        user_details = mongo.db.users.find_one({"username": session["user"]})
    # Stops the deletion of recipes created by different users via the URL.
    if session.get("user") != recipe["author"] and not (
         user_details["is_admin"]):
        flash("you can only delete your own entries!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    else:
        mongo.db.recipes.delete_one({"_id": ObjectId(id)})
        flash("your recipe has been deleted!")
        return redirect(url_for("user_profile",
                                username=session["user"]))


@app.route("/user_profile/<username>", methods=["GET", "POST"])
def user_profile(username):
    """
    Renders user profile page. Only accessable to the user whos account it is
    when logged in. Page takes the input of username to both check this and
    to show the recipes on the page that they have added themselves.
    """
    # Stops access to users that aren't registed or logged in.
    if not session.get("user"):
        flash("you dont have authorization to view this page!")
        return redirect(url_for("login"))
    # Stops access to other users whose account this isn't.
    if username != session.get("user"):
        flash("you dont have authorization to view this page!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    else:
        # Create list of recipes the user has added to render on the page.
        user_recipes = list(mongo.db.recipes.find(
            {"author": session["user"]}))
        # Create variable used to check admin rights on the page.
        user_details = mongo.db.users.find_one(
            {"username": session["user"]})
        return render_template("user_profile.html",
                               username=session["user"],
                               user_recipes=user_recipes,
                               user_details=user_details,
                               page_title="My Profile")


@app.route("/delete_profile/<user>")
def delete_profile(user):
    """
    Delete profile function. The user passed into the function identifies the
    profile for deletion. The checks are then done to check they are the user.
    The profile is then removed from the database.
    """
    # Stops access to users that aren't registed or logged in.
    if "user" not in session:
        flash("you dont have authorization to perform this task!")
        return redirect(url_for("login"))
    # Stops the deletion of profiles by different users.
    else:
        if user == session["user"]:
            # Removes all recipes by the user.
            mongo.db.recipes.remove({"author": session["user"]})
            mongo.db.users.delete_one({"username": session["user"]})
            # Removes session cookie.
            session.pop("user")
            flash("profile deleted!")
            return redirect(url_for("register"))
        else:
            flash("you can only delete your own profile!")
            return redirect(url_for("user_profile",
                                    username=session["user"]))


@app.route("/manage_categories", methods=["GET", "POST"])
def manage_categories():
    """
    Renders manage categories page. Only accessable to admin only. Validates
    and adds data given by the user to the db.
    """
    # Stops access to users that aren't registed or logged in.
    if not session.get("user"):
        flash("you dont have authorization to access this page!")
        return redirect(url_for("login"))
    else:
        # Creates variable used to check admin rights.
        user_details = mongo.db.users.find_one({"username": session["user"]})
    # Admin rights are required for access.
    if not user_details["is_admin"]:
        flash("you dont have authorization to access this page!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    else:
        # AddCategoryForm class found in forms.py.
        form = AddCategoryForm()
        # Create a list of category names to dynamically add cards.
        categories = mongo.db.categories.find()
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


@app.route("/delete_category/<id>", methods=["GET", "POST"])
def delete_category(id):
    """
    Delete category function. Only accessable to admin only. The id passed into
    the function identifies the category for deletion. The checks are then done
    to check user is admin. The category is then removed from the database.
    """
    # Stops access to users that aren't registed or logged in.
    if not session.get("user"):
        flash("you dont have authorization to perform this task!")
        return redirect(url_for("login"))
    else:
        # Creates variable used to check admin rights.
        user_details = mongo.db.users.find_one({"username": session["user"]})
    # Admin rights are required.
    if not user_details["is_admin"]:
        flash("you dont have authorization to perform this task!")
        return redirect(url_for("user_profile",
                                username=session["user"]))
    elif user_details["is_admin"]:
        mongo.db.categories.delete_one({"_id": ObjectId(id)})
        flash("the category has been deleted!")
        return redirect(url_for("manage_categories"))


# Code for error pages found here and was edited accordingly
# https://www.youtube.com/watch?v=3O4ZmH5aolg
@app.errorhandler(404)
def page_not_found(e):
    """Renders 404 page not found page."""
    return render_template("404.html",
                           error=e), 404


# Code for error pages found here and was edited accordingly
# https://www.youtube.com/watch?v=3O4ZmH5aolg
@app.errorhandler(500)
def internal_server_error(e):
    """Renders 500 internal server error page."""
    return render_template("500.html",
                           error=e), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
