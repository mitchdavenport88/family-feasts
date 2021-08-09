import os
from flask import (
    Flask, flash, render_template, redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

if os.path.exists("env.py"):
    import env

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def home():
    return render_template("index.html", page_title="Home")


@app.route("/recipes/<filter>")
def recipes(filter):
    categories = [(category["category_name"])
                  for category in mongo.db.categories.find()]
    if filter not in categories and filter != "all":
        flash("this category does not exist!")
        return redirect(url_for("recipes", filter="all"))
    elif filter in categories:
        recipes = list(mongo.db.recipes.find({"category_name": filter}))
    else:
        recipes = list(mongo.db.recipes.find())
    return render_template("recipes.html", recipes=recipes,
                           categories=categories, filter=filter)


@app.route("/search", methods=["GET", "POST"])
def search():
    search = request.form.get("search")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": search}}))
    categories = [(category["category_name"])
                  for category in mongo.db.categories.find()]
    return render_template("recipes.html", recipes=recipes, filter="search",
                           categories=categories, search=search)


@app.route("/view_recipe/<id>")
def view_recipe(id):
    # Shows individual recipes based on thier db id
    recipe = mongo.db.recipes.find_one_or_404({"_id": ObjectId(id)})
    return render_template("view_recipe.html", recipe=recipe,
                           page_title=recipe["recipe_name"])


@app.route("/register", methods=["GET", "POST"])
def register():
    # stops access to users that have registered already
    if session.get("user"):
        flash("you're already registered!")
        return redirect(url_for("user_profile", username=session["user"]))
    else:
        if request.method == "POST":
            existing_user = mongo.db.users.find_one(
                {"username": request.form.get("username").lower()})
            #  https://techmonger.github.io/4/secure-passwords-werkzeug/
            #  https://www.youtube.com/watch?v=jJ4awOToB6k
            password = generate_password_hash(request.form.get("password"))
            if existing_user:
                flash("the username you've chosen is taken!")
                return redirect(url_for("register"))
            elif check_password_hash(password,
                                     request.form.get("confirm-password")):
                register = {
                    "username": request.form.get("username").lower(),
                    "password": password
                }
                mongo.db.users.insert_one(register)
                session["user"] = request.form.get("username").lower()
                flash("registration complete!")
                return redirect(url_for("user_profile",
                                        username=session["user"]))
            else:
                flash("the passwords entered didn't match!")
                return redirect(url_for("register"))
        return render_template("register.html", page_title="Register")


@app.route("/login", methods=["GET", "POST"])
def login():
    # stops access to users that have logged in already
    if session.get("user"):
        flash("you're already logged in!")
        return redirect(url_for("user_profile", username=session["user"]))
    else:
        if request.method == "POST":
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
        return render_template("login.html", page_title="Log In")


@app.route("/logout")
def logout():
    # Prevents ability to logout if not logged in
    if session.get("user"):
        session.pop("user")
        return redirect(url_for("login"))
    else:
        flash("you need to be logged in to perform this task!")
        return redirect(url_for("login"))


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    # Prevents unauthorized access to page
    if not session.get("user"):
        flash("you need to be logged in to perform this task!")
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
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
            return redirect(url_for("view_recipe", id=recipe["_id"]))
        categories = mongo.db.categories.find()
        return render_template("add_recipe.html", categories=categories,
                               page_title="Add Recipe")


@app.route("/edit_recipe/<id>", methods=["GET", "POST"])
def edit_recipe(id):
    recipe = mongo.db.recipes.find_one_or_404({"_id": ObjectId(id)})
    categories = mongo.db.categories.find()
    # Prevents unauthorized access to page
    if not session.get("user"):
        flash("you need to be a registered user to perform this task!")
        return redirect(url_for("register"))
    # Stops the deletion of recipes created by different users via the URL
    elif session.get("user") != recipe["author"]:
        flash("you can only edit your own entries!")
        return redirect(url_for("user_profile", username=session["user"]))
    else:
        if request.method == "POST":
            submit = {
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
            mongo.db.recipes.update({"_id": ObjectId(id)}, submit)
            flash("your recipe has been updated!")
            return redirect(url_for("view_recipe", id=recipe["_id"]))
        return render_template("edit_recipe.html", categories=categories,
                               recipe=recipe, page_title="Edit Recipe")


@app.route("/delete_recipe/<id>")
def delete_recipe(id):
    recipe = mongo.db.recipes.find_one_or_404({"_id": ObjectId(id)})
    # Stops unregistered users or those not logged in deleting recipes
    if not session.get("user"):
        flash("you need to be a registered user to perform this task!")
        return redirect(url_for("register"))
    # Stops the deletion of recipes created by different users via the URL
    elif session.get("user") != recipe["author"]:
        flash("you can only delete your own entries!")
        return redirect(url_for("user_profile", username=session["user"]))
    else:
        mongo.db.recipes.delete_one({"_id": ObjectId(id)})
        flash("your recipe has been deleted!")
        return redirect(url_for("user_profile", username=session["user"]))


@app.route("/user_profile/<username>", methods=["GET", "POST"])
def user_profile(username):
    # Prevents unauthorized access to page
    if not session.get("user"):
        flash("you dont have authorization to view this page!")
        return redirect(url_for("login"))
    # Users can only view thier own profile page
    elif username != session.get("user"):
        flash("you dont have authorization to view this page!")
        return redirect(url_for("user_profile", username=session["user"]))
    else:
        user_recipes = list(mongo.db.recipes.find({"author": session["user"]}))
        if session["user"]:
            return render_template("user_profile.html",
                                   username=session["user"],
                                   user_recipes=user_recipes,
                                   page_title="My Profile")
        return redirect(url_for("login"))


@app.route("/delete_profile/<user>")
def delete_profile(user):
    # Prevents unauthorized access to page
    if not session.get("user"):
        flash("you dont have authorization to perform this task!")
        return redirect(url_for("login"))
    # Users can only delete thier own profile
    elif session.get("user") != user:
        flash("you can only delete your own profile!")
        return redirect(url_for("user_profile", username=session["user"]))
    else:
        mongo.db.users.remove({"username": user})
        session.pop("user")
        #  Removes all recipes by the user
        mongo.db.recipes.remove({"author": user})
        return redirect(url_for("home"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", error=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template("500.html", error=e), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Change to debug=False before submission
            debug=True)
