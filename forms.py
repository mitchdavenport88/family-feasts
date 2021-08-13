from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, IntegerField, TextAreaField, SelectField)
from wtforms.validators import InputRequired, Length, NumberRange
from wtforms_validators import AlphaNumeric, ActiveUrl


class RegistrationForm(FlaskForm):
    """
    Inserts the following input fields into the registration form and
    validates the data returned before inserting data into the db
    """
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


class LoginForm(FlaskForm):
    """
    Inserts the following input fields into the log in form and validates the
    data returned before querying the data against the db
    """
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


class AddRecipeForm(FlaskForm):
    """
    Inserts the following input fields into the add and edit recipe forms and
    validates the data returned before inserting data into the db
    """
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


class AddCategoryForm(FlaskForm):
    """
    Inserts category name input field on the manage_catergories page
    (admin only) and validates data returned before insertion into the db
    """
    category_name = StringField('category name',
                                validators=[InputRequired(),
                                            Length(min=1, max=10,
                                                   message="category name\
                                                       should be a maximum of\
                                                           10 characters"),
                                            AlphaNumeric("category name should\
                                                contain letters and numbers\
                                                    only")])
