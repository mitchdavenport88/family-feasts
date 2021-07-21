import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired

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


# Intro to Flask-WTF series - Pretty Printed
# (https://www.youtube.com/watch?v=vzaXBm-ZVOQ)
class addForm(FlaskForm):
    recipe_name = StringField('recipe name',
                              validators=[DataRequired()])
    recipe_image = StringField('recipe img (url)')
    prep_time = IntegerField('prep time (mins)',
                             validators=[DataRequired()])
    cook_time = IntegerField('cooking time (mins)',
                             validators=[DataRequired()])
    servings = IntegerField('number of servings',
                            validators=[DataRequired()])
    category_name = SelectField('category')


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    form = addForm()
    # https://stackoverflow.com/questions/28133859/how-to-populate-wtform-select-field-using-mongokit-pymongo
    form.category_name.choices = [(category['category_name'])
                                  for category in mongo.db.categories.find()]
    if form.validate_on_submit():
        recipe = {
            "recipe_name": request.form.get("recipe_name").title(),
            "recipe_image": request.form.get("recipe_image"),
            "servings": request.form.get("servings"),
            "prep_time": request.form.get("prep_time"),
            "cook_time": request.form.get("cook_time"),
            "category_name": request.form.get("category_name")
        }
        mongo.db.recipes.insert_one(recipe)
        return redirect(url_for("recipes"))
    return render_template("add_recipe.html", form=form)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            # Change to debug=False before submission
            debug=True)
