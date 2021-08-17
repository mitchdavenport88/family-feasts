# Milestone Project Three - Testing

The live site can be viewed here - [Family Feasts](https://family-feasts.herokuapp.com/).

[Back to README file.](README.md)

## Testing
My code has been put through the following:
* W3C HTML validation. The W3C validator doesn't like jinja templating and raises a bad value error for every instance. So to avoid this I put each HTML file through the validator as it appears in the view page source document (accessed by left clicking the page). Things that got highlighted were:
    * Duplicate ID's "staticBackdropLabel" on recipes.html caused by the delete button and confirmation button. As an ID needs to be unique I altered the name to include the relevant id so that it's now unique if/when it gets generated. 
    * On the home page I got a warning of *"Consider using the h1 element as a top-level heading only."* As I'm using the h1's in question as headings for about and why cook together sections I've chosen to ignore this.  
    * I changed the `<section>` tag to a `<div>` on the following documents because the `{% block content %}` on the base.html was already surrounded by a `<section>` tag:
        * login.html
        * register.html
        * add_recipe.html
        * edit_recipe.html
* CSS AutoPrefixer.
* W3C CSS validation - passed.
* JSHint JavaScript validation - no errors.
* PEP8 online check - boths files "all right".

## Functionality
### Manual Testing
These are the steps I went through testing my website and it's functionality.

Navigation:
1. Clicked on all the links in the navigation bar to ensure they do what they're supposed to.
    * Did this whilst logged in and out, checking that the correct links appear each time.
2. Clicked the logo at various points to make sure that doing so takes me back to the home page.
3. Hovered over the links and buttons to make sure the hover classes are working.
4. Checked the navigation bar remains at the top of the page at all times and is never hidden by any other content.
5. Changed the window width to below 992px in order to check that the navigation bar content changes. A menu icon should be displayed to the right and all links should now display via a dropdown menu only.
    * The logo should always be positioned top left.
6. Toggled the menu icon button on/off to check it displays and hides the dropdown menu accordingly.
    * All links now shown in this dropdown menu.
    * Call-to-action buttons should now appear as links.
7. Repeated step 1 but using the dropdown menu only.

Buttons:
1. Hovered over all buttons to check they invert colour on hover.
2. Clicked on all buttons checking that they do what they should.
3. Checked when numerous buttons are used that they are responsive and will stack on top of each over whilst remaining centrally aligned as containers decrease in width.

Page and section headings:
1. Checked that page/section title's are always aligned centrally and positioned correctly.

Home:
1. Checked that the background image isn't pixelated and loads as intended.
2. Checked the text overlay box appears and that the relevant text and button are visible within it.
    * The box and its contents is always justified and aligned centrally.
3. Checked the about us and why cook together titles are displayed and aligned centrally.
4. Checked the save, share and experiment sections are displayed as intended at varying breakpoints:
    * Across the entire page on widths above 992px.
    * In two separate rows between widths of 768px and 992px.
    * In three rows on widths below 768px.
    * The three sections always appear separate.
5. Checked the why cook together section displayed as intended at varying breakpoints:
    * Each section should appear across the page on widths above 992px and consist of an image next to a block of text.
        * Checked the pictures load, are positioned well and are of good quality.
        * Text within the text boxes is legible and the boxes adapt to change of width.
    * Below 992px the images should get hidden with the text boxes stretching to fill the width of the page and stack one on top of another.

Recipes:
1. Check that the page title changes to include the name of a category when a filter is applied e.g. breakfast recipes or dessert recipes when the relevant button is clicked.
2. Search bar is positioned between the title and the filter buttons and is displayed centrally at all breakpoints.
    * Checked it contains a placeholder of “search all recipes by name or ingredient”.
    * Checked an orange submit button is built into the right side of the input field and loads showing an icon of a magnifying glass. Button has the same hover class as all other buttons.
3. Test search function:
    * Text input is required to search.
    * Searched for "egg".
        * Title changed to “search results for egg”.
        * All recipe cards for the recipes that have egg in their titles or ingredients list are now shown below.
    * Searched for something that doesn’t exist – "swede":
        * Title changed to “search results for swede”.
        * No cards appear. A message stating "no recipes containing ‘swede’" appears where the cards would otherwise.
4. Buttons used to filter recipes shown are dynamically generated using information from the categories section in the database. Checked that all categories in the database have a button.
    * Checked that if a category is added or removed from the database these buttons alter accordingly.
    * Checked that each button applies the intended filter and that the relevant recipe cards are displayed below.
5. Checked that if there are no recipes for that category then a message stating “no recipes for this category yet” appears where the cards would otherwise.
    * Checked that a call-to-action button appears underneath this message if the user is logged in to add a recipe.
6. Checked that the recipe cards are displayed as intended at varying breakpoints:
    * In four columns on screen widths above 1200px.
    * In three columns on screen widths between 992px and 1200px.
    * In two columns on screen widths between 768px and 992px.
    * In one column on screen widths below 768px.
7. Each card contains:
    * A picture of the recipe, which is positioned well and is of good quality.
    * The recipe title.
    * The "view recipe" button.
        * Other buttons will appear here also based on the user’s registration status.

View recipe (individual recipe pages):
1. Checked that the correct recipe title is displayed at the top of the page.
2. The appropriate buttons based on the user’s registration status appear in a row underneath the title.
    * "back to recipes" button appears for every user and returns the user to the recipes page.
    * Additional buttons "delete recipe" and "edit recipe" will show here if the recipe was uploaded by the user currently logged in or if they have admin rights.
3. Check that the correct information is pulled from the database and displayed as expected with the image, times, servings and category name displayed in a table while the ingredients and method are listed below side by side.
4. On screen widths of below 768px the table adapts to smaller screen sizes now displaying the times, servings and category name underneath the image (still in a table). The lists are still below these but now positioned one on top of another.
5. Checked that the "back to top" button has a matching hover class and scrolls the page back to the top on click.

Register:
1. Checked the number of input fields, 3 in total: username, password and confirm password. Each having a relevant label and input instructions were necessary. 
2. Tested the buttons and link:
    * Pressed cancel, which takes me back to the home page.
    * Pressed register to try and send an empty form. Input required error message appears as it should.
    * Clicked the log in link, which took me to the login page.
3. Checked that if a username already exists or the passwords dont match that the relevant flash message appears.
4. Tested that the form validated the inputted data correctly when the critera from step 5 is met. The form will then only send once the following conditions are met:
    * Username is entered and contains letters and numbers only. Usernames also need to be between 5 and 20 characters long. 
        * Error message appears under the input field if not.
    * Passwords should also be between 5 and 20 characters long and are also required.
        * Error message appears under the input field if not.
7.	On successful completion of the form I'm directed to my newly created user profile page and a flash message displays “registration complete!”
8. Once registered and logged in this page is unaccessable. If I attempt to access this page via the URL then I should get redirected back to my user profile page and a flash message reading “you’re already registered” appears.

Log in:
1. Checked the number of input fields, 2 in total: username and password. Each having a relevant label.
2. Tested the buttons and link:
    * Pressed cancel, which takes me back to the home page.
    * Pressed log in to try and send an empty form. Input required error message appears as it should.
    * Clicked the register here link, which took me to the login page.
3. Tested that the form validated the inputted data correctly, the criteria is the same as that in the registration form. The form will only send if all the conditions are met.
    * Error messages will appear under the input fields if not.
4. On successful completion of the form the data is cross-referenced against data in the db:
    * If neither field match anything in the database then a flash message stating "incorrect username or password entered".
    * On successful completion of the form I'm directed to my existing user profile page.
5. Once logged in this page is unaccessable. If I attempt to access this page via the URL then I should get redirected back to my user profile page and a flash message reading “you’re already logged in!” appears.

Log out:
1. When logged in the logout button should be located at the top right of the screen in the navigation bar. On screen widths below 992px the button becomes a link, which is found in the dropdown menu.
2. When the button or link is clicked I'm logged out, I get redirected to the login page and a flash message appears reading “you’ve been logged out!”
3. My session cookie should have been removed so I no longer have access to any unauthorized content:
    * Tried to access the add recipe page via the URL. I should get redirected to the login page and told that“you need to be logged in to perform this task!”
4. This feature is accessable only if you are logged in. If I attempt to access this via the URL then I should get redirected to the login page and a flash message reading “you need to be logged in to perform this task!”

Footer:
1. Checked the footer sticks to the bottom of every page and never hides any content.
2. Checked that the social links are always aligned centrally.
3. Clicked all icons the footer to check that they open and do so in a new tab.
4. Repeated step 1-2 but at different breakpoints. 
