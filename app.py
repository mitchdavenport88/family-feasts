import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
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
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)


@app.route("/view_recipe/<id>")
def view_recipe(id):
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})
    return render_template("view_recipe.html", recipe=recipe)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    if request.method == "POST":
        recipe_url = request.form.get("recipe_image")
        if recipe_url == "":
            # https://www.cleanpng.com/png-free-lunch-free-content-clip-art-youth-luncheon-cl-167343/
            recipe_url = url_for('static',
                                 filename='images/default-recipe-image.png')
        # https://www.w3schools.com/python/ref_string_splitlines.asp
        recipe = {
            "recipe_name": request.form.get("recipe_name").title(),
            "recipe_image": recipe_url,
            "category_name": request.form.get("category_name"),
            "servings": request.form.get("servings"),
            "prep_time": request.form.get("prep_time"),
            "cook_time": request.form.get("cook_time"),
            "ingredients": request.form.get("ingredients").splitlines(),
            "recipe_steps": request.form.get("recipe_steps").splitlines()
        }
        mongo.db.recipes.insert_one(recipe)
        return render_template("view_recipe.html", recipe=recipe)
    categories = mongo.db.categories.find()
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<id>", methods=["GET", "POST"])
def edit_recipe(id):
    if request.method == "POST":
        submit = {
            "recipe_name": request.form.get("recipe_name").title(),
            "recipe_image": request.form.get("recipe_image"),
            "category_name": request.form.get("category_name"),
            "servings": request.form.get("servings"),
            "prep_time": request.form.get("prep_time"),
            "cook_time": request.form.get("cook_time"),
            "ingredients": request.form.get("ingredients").splitlines(),
            "recipe_steps": request.form.get("recipe_steps").splitlines()
        }
        mongo.db.recipes.update({"_id": ObjectId(id)}, submit)
        recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})
        flash("your recipe has been updated!")
        return render_template("view_recipe.html", recipe=recipe)
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(id)})
    categories = mongo.db.categories.find()
    return render_template("edit_recipe.html", categories=categories,
                           recipe=recipe)


@app.route("/delete_recipe/<id>")
def delete_recipe(id):
    mongo.db.recipes.remove({"_id": ObjectId(id)})
    flash("your recipe has been deleted!")
    return redirect(url_for("recipes"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        if existing_user:
            flash("the username you've chosen is taken!")
            return redirect(url_for("register"))
        elif password != confirm_password:
            flash("the passwords entered didn't match!")
            return redirect(url_for("register"))
        else:
            register = {
                "username": request.form.get("username").lower(),
                "password": generate_password_hash(request.form.get("password"))
            }
            mongo.db.users.insert_one(register)
            session["user"] = request.form.get("username").lower()
            flash("registration complete!")
            return redirect(url_for("recipes"))  # Link to profile when made
    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Change to debug=False before submission
            debug=True)
