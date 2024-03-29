# Milestone Project Three - Testing

The live site can be viewed here - [Family Feasts](https://family-feasts.herokuapp.com/).

[Back to README file.](README.md)

## Testing
My code has been put through the following:
* W3C HTML validation. The W3C validator doesn't like the jinja templating language and raises a bad value error for every instance where its used. So to avoid this I put each HTML file through the validator as it appears in the view page source document (accessed by left clicking the page). Things that got highlighted were:
    * Duplicate ID's "staticBackdropLabel" in recipes.html caused by the code that generates the delete button and confirmation modal. As an ID needs to be unique I altered the names to include the relevant ID so that it's now unique in every instance where it gets generated. 
    * On the home page I got a warning of *"Consider using the h1 element as a top-level heading only."* As I'm using the h1's in question as headings for the about and why cook together sections I've chosen to ignore this.  
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

**Navigation:**
1. Clicked on all the links in the navigation bar to ensure they do what they're supposed to do.
    * I did this whilst logged in and out, checking that the correct links appear each time.
2. Clicked the logo at various points to make sure that doing so takes me back to the home page.
3. Hovered over the links and buttons to make sure the hover classes are working.
4. Checked the navigation bar remains at the top of the page at all times and is never hidden by any other content.
5. Changed the window width to below 992px in order to check that the navigation bar content changes. A menu icon should be displayed to the right and all links should now display via a dropdown menu only.
    * The logo is always positioned top left.
6. Toggled the menu icon button on/off to check it displays and hides the dropdown menu accordingly.
    * All links are now shown in this dropdown menu.
    * Call-to-action buttons now appear as links.
7. Repeated step 1 but using the dropdown menu only.

**Footer:**
1. Checked the footer sticks to the bottom of every page and never hides any content.
2. Checked that the social links are always aligned centrally.
3. Clicked on all icons in the footer to check that they open and do so in a new tab.
4. Repeated step 1-2 but at different breakpoints. 

**Buttons:**
1. Hovered over all buttons to check they invert colour on hover.
2. Clicked on all buttons checking that they do what they should.
3. Checked when numerous buttons are used that they are responsive and will stack on top of each other. They should remain centrally aligned to their containers as they decrease in width.

**Page and section headings:**
1. Checked that page/section title's are always aligned centrally and positioned correctly.

**Home:**
1. Checked that the background image isn't pixelated and loads as intended.
2. Checked the text overlay box appears and that the relevant text and button are visible within it.
    * The box and its contents should always be justified and aligned centrally.
3. Checked the save, share and experiment sections are displayed as intended at varying breakpoints:
    * Across the entire page on widths above 992px.
    * In two separate rows between widths of 768px and 992px.
    * In three rows on widths below 768px.
    * The three sections always appear separate.
4. Checked the why cook together section displayed as intended at varying breakpoints:
    * Each section should appear across the page on widths above 992px and consist of an image next to a block of text.
        * Checked the pictures load, are positioned well and are of good quality.
        * Text within the text boxes is legible and the boxes adapt to a change of width.
    * Below 992px the images should get hidden with the text boxes stretching to fill the full width of the page and stack one on top of another.

**Recipes:**
1. Check that the page title changes to include the name of a category when a filter is applied e.g. breakfast recipes or dessert recipes when the relevant button is clicked.
2. Search bar is positioned between the title and the filter buttons and is displayed centrally at all breakpoints.
    * Checked it contains a placeholder of “search all recipes by name or ingredient”.
    * Checked that an orange submit button is built into the right hand side of the input field and loads showing an icon of a magnifying glass. Button has the same hover class as all other buttons.
3. Test search function:
    * Text input is required to search.
    * Searched for egg.
        * Title changed to “search results for egg”.
        * All recipe cards for the recipes that have egg in their titles or ingredients list are now shown below.
    * Searched for something that doesn’t exist – swede:
        * Title changed to “search results for swede”.
        * No cards appear. A message stating "no recipes containing ‘swede’" appears where the cards would otherwise.
4. Buttons used to filter recipes shown are dynamically generated using information from the categories collection in the database. Checked that all categories in the database have a button.
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

**View recipe (individual recipe pages):**
1. Checked that the correct recipe title is displayed at the top of the page.
2. The appropriate buttons based on the user’s registration status appear in a row underneath the title.
    * "back to recipes" button appears for every user and returns the user to the recipes page.
    * Additional buttons: "delete recipe" and "edit recipe" should show here if the recipe was uploaded by the user currently logged in or if they have admin rights.
3. Checked that the correct information is pulled from the database and displayed as expected with the image, times, servings and category name displayed in a table while the ingredients and method are listed below side by side.
4. On screen widths of below 768px the table adapts to smaller screen sizes now displaying the times, servings and category name underneath the image. The lists are still below the table but now positioned one on top of another.
5. Checked that the "back to top" button has a matching hover class and scrolls the page back to the top on click.

**Register:**
1. Checked the number of input fields, 3 in total: username, password and confirm password. Each having a relevant label and input instructions where necessary. 
2. Tested the buttons and link:
    * Pressed "cancel", which takes me back to the home page.
    * Pressed "register" to try and send an empty form. Input required error message appears as it should.
    * Clicked the log in link, which took me to the login page.
3. Checked that if a username already exists or the passwords dont match that the relevant flash message appears.
4. Tested that the form validated the inputted data correctly when the criteria from step 3 is met. The form will then only send once the following conditions are met:
    * Username is entered and contains letters and numbers only. Usernames also need to be between 5 and 20 characters long. 
        * Checked error message appears under the input field if criteria isn't met.
    * Passwords should also be between 5 and 20 characters long and are also required.
        * Checked error message appears under the input field if criteria isn't met.
5. On successful completion of the form I'm directed to my newly created user profile page and a flash message displays “registration complete!”

**Log in:**
1. Checked the number of input fields, 2 in total: username and password. Each having a relevant label.
2. Tested the buttons and link:
    * Pressed "cancel", which takes me back to the home page.
    * Pressed "log in" to try and send an empty form. Input required error message appears as it should.
    * Clicked the register here link, which took me to the register page.
3. Tested that the form validated the inputted data correctly, the criteria is the same as that in the registration form. The form will only send if all the conditions are met.
    * Checked error message appears under the input field if criteria isn't met.
4. On successful completion of the form the data is cross-referenced against data in the database:
    * If neither field match anything in the database then a flash message stating "incorrect username or password entered" appears.
    * On successful completion of the form I'm directed to my existing user profile page.

**Log out:**
1. When logged in the logout button should be located at the top right of the screen in the navigation bar. On screen widths below 992px the button becomes a link, which is found in the dropdown menu.
2. When the button or link is clicked I'm logged out, I get redirected to the login page and a flash message appears reading “you’ve been logged out!”
3. My session cookie should have been removed so I should no longer have access to any unauthorized content:
    * Tried to access the add recipe page via the URL. I get redirected to the login page and the flash message reads “you need to be logged in to perform this task!”

**User profile:**
1. Checked that the user’s username is displayed at the top of the page.
2. Seen that the “view all recipes”, “add recipe” and “delete profile” buttons are located underneath the title.
    * Checked that when the user has admin rights the “delete profile” button becomes the “manage categories” button.
3. If the registered user has previously uploaded any recipes then:
    * Checked that recipe cards display recipes uploaded by that user only under the heading of "my recipes".
    * Check the cards all have the appropriate buttons to take any further action.
4. If no recipes have been created by the registered user then a message to say “you’ve not added any recipes yet!” appears. A call-to-action button also appears in order to add a recipe.

**Add recipe:**
1. Checked the number of input fields, 8 in total: recipe name, recipe image, category, servings, prep time, cook time, ingredients and method.
    * Each have a relevant label and input instructions where necessary.
2. Tested the buttons:
    * Pressed "cancel" - takes me to the recipes page.
    * Pressed "clear form" – reloads the page.
    * Pressed "add recipe" to try and send an empty form. Input required error message appears.
3. Tested that the form validated the inputted data correctly. The form will then only send if all fields are filled in and the following conditions are met:
    * Recipe name is no longer than 35 characters long. 
    * Recipe image is an active URL link.
    * Category name is selected from the dropdown menu.
    * Serving is an integer between 1 and 100.
    * Timings are an integer between 0 and 999.
    * Ingredients and method are required.
        * Error messages appear under the input fields if requirements aren't met.
4. On successful completion of the form I get redirected to the newly created recipe page, which will show the recipe I’ve just added.

**Edit recipe:**
1. Checked the form is the same as that found on the add recipe page and pre-populated with the data of the recipe I'm editing.
2. Tested the buttons:
    * Pressed "cancel" - takes me to the recipes page.
    * Pressed "update recipe" – the recipe page will load with a flash message of “your recipe has been updated!”
    * Pressed delete recipe – deletion modal pops up. 
3. Tested that the form validates the data inputted correctly, the criteria is the same as the add recipe form. All fields are required and the form will only send if all conditions are met.
4. On successful completion of the form I get redirected to the recipes page, which will show the updated recipe information and a flash message states that "recipe has been updated".

**Manage categories:**
1. Checked that there is only one input field; category name. It should have the relevant label and input instructions.
2. Tested the "add category" button:
    * Pressed button to try and send the form empty. Input required error message appears as should.
3. The form only sends if the category name is between 1 and 10 characters and can contain letters and numbers only.
    * Checked error message appears under the input field if criteria isn't met.
4. On successful completion of the form the page reloads and a flash message saying “the category has been added!” appears.
5. The newly created category now appears on a card in the manage categories section below.
6. As cards are dynamically generated using information from the categories section in the database I checked that all categories that exist have a card.
    * Checked each card has a delete button.
    * Checked that the new category appears on the recipes page (as a button) and in the dropdown menu on both the edit and add recipe forms.
7. Checked that the cards are displayed as intended at varying breakpoints:
    * In four columns on screen widths above 1200px.
    * In three columns on screen widths between 992px and 1200px.
    * In two columns on screen widths between 768px and 992px.
    * In one column on screen widths below 768px.

**Delete functions:**
1. Checked that all deletion buttons prompt the “are you sure...” modal to appear to proceed with the deletion.
    * The close button closes the modal with no action taken.
    * The delete button triggers the deletion process.
2. Deleting a recipe:
    * When a recipe is deleted I’m redirected back to my profile page.
    * A flash message reading “your recipe has been deleted!” appears.
    * Checked that the recipe can no longer be found on the site.
    * Checked that this process can only be completed by the user who’s profile it is or someone with admin rights.
3. Deleting a profile:
    * When a profile is deleted I’m redirected back to the registration page.
    * A flash message reading “profile deleted!” appears.
    * Checked that I can no longer log into the site using the deleted credentials.
    * Checked that this process can only be completed by the user whose profile it is.
4. Deleting a category:
    * On successful deletion the manage categories page reloads and a flash message saying “the category has been deleted!” appears.
    * Checked that the category no longer appears on the recipes page (as a button) or in the dropdown menu on either the edit/add recipe forms.
    * Checked that this action can only be done by someone with admin rights.

### Defensive design / "brute forcing"
I put measures in place in my app.py to stop instances of certain types of user being able to access certain features, run certain functions or access pages (sometimes known as brute forcing). Below shows a table illustrating the tests I did to check the accesses and restrictions I put in place work based on a user’s login/registration status or admin rights. The table indicates how the site responds in these instances.

![defensive design testing table](readme-docs/screenshots/access-test-table.jpg)

## Responsiveness
Whilst building my site I have been checking my progress and testing any changes made using Chrome DevTools at different breakpoints. I try to push my work to GitHub as often as possible so I can physically see the live site on either my desktop or iPhone via Heroku. I do this at varying stages of the build and especially when new features get added, as I find physically seeing something more beneficial than a projection.

I have physically tested my site on my iPhone 6 using both Safari and Chrome. I have tested for responsiveness on other devices using DevTools along with the Responsive Design Mode on Firefox. Using these tools I have tested on numerous mobile devices such as the Moto G4, Galaxy X9 and the iPhone range as well as numerous tablet devices in both landscape and portrait views.

![recipe as seen on an iPad](readme-docs/screenshots/recipe-ipad.jpg)

## Browser compatibility
I have physically tested my website by completing my manual testing plan on the following browsers and devices:
* Chrome (desktop and iPhone).
* Firefox (desktop).
* Microsoft Edge (desktop).
* Safari (iPhone).

I also tested compatibility at varying screen sizes to test the responsiveness on each Browser using Chrome DevTools along with the Responsive Design Mode on Firefox or the Inspect tool on Microsoft Edge.

## User Stories
### As a first time user I'd like:
**"To access and view all recipes."**
* The recipes page, filtering buttons and search function are accessible to all users, registered or not.
* A link to the recipes page can always be found in the navigation bar.
* There is a call-to-action button on every card linking the user to the individual page of each recipe. These pages are also accessible to all users.

![Recipes page as seen by anyone.](readme-docs/screenshots/user-stories/user-stories1.jpg)


**"To be able to browse by recipe category."**
* The buttons used to apply the filter are dynamically generated by using values found in the categories collection in my database. This means as the site progresses new categories may be added or removed but these buttons will get updated accordingly.
* There is a button for each category that is selectable when adding or updating a recipe via the forms.
* When a filter is applied the section header changes to match the filter and the relevant recipes get displayed.
* If a filter has no matches then a message gets shown to inform the user of this [as shown here](readme-docs/screenshots/user-stories/user-stories3.jpg).

![Breakfast recipes filter in action.](readme-docs/screenshots/user-stories/user-stories2.jpg)


**"To search for suitable recipes by using keywords or ingredients."**
* A search is carried out using the value of what is typed into the input field. We look for a match of this value in the recipe name and/or its ingredients list (stored in the recipes collection).
* Multiple words can be searched for at once. The results shown as a result will be matches of any of the words searched.
* On completion of a search the section header changes to show the user that a search has been conducted.
* The search function was tested using my manual testing plan:
    * If a match is found then all the results get displayed below [as shown here.](readme-docs/screenshots/user-stories/user-stories4.jpg)
    * Else if no match was found we show the user this by displaying a message as shown below.

![Search results for 'swede'.](readme-docs/screenshots/user-stories/user-stories5.jpg)


**"Information on each recipe to be presented in a clear and concise manner."**
* Most of the recipe information gets displayed via a visually appealing table, which breaks the information up into columns and rows with division between cells. The table adapts to changes in page width while the information on show remains clear at all times [as shown here.](readme-docs/screenshots/user-stories/user-stories6.jpg)
* I thought it would be more aesthetically pleasing and clearer to display the recipe ingredients and the recipes method as lists shown below this table. Still keeping to a structured format that responds to differing breakpoints the lists provide clear information, are easy to read and are in keeping with the overall style of the site.

**"To sign up to the community easily."**
* A call-to-action button linking to the registration page can be found both on the home page and in the navigation bar.
* Registering is a simple process with only a username and password required. Password confirmation will also be required for added security.
* Each input field is clearly labelled and has an additional note informing a user about the validation requirements.
* If the validation requirements aren’t met then the user is informed of this using a little note below the input field – as shown below.
* A user is clearly informed if the username is in use or if the passwords don’t match via a flash message. 

![Registration form validation messages.](readme-docs/screenshots/user-stories/user-stories9.jpg)


**"The site to be easy to navigate around and user friendly."**
* I've used a fixed navigation bar so that the page links are available at the top of every page and at any point.
* This is also the case on smaller devices but the links get placed into a dropdown menu, which is operational by clicking the menu button [as shown here.](readme-docs/screenshots/user-stories/user-stories7.jpg) 
* I’ve placed call-to-action buttons all over the site (where relevant). These are clear in what they do, have a hover classes to show they can be interacted with and aid with the overall navigation around the site by showing a user what they can do there and then.

![Example of call-to-action buttons in use.](readme-docs/screenshots/user-stories/user-stories8.jpg)


**"To do all of the above regardless of what device I’m using."**
* I have done thorough browser compatibility testing as well as responsiveness testing at different breakpoints. I am confident that the site is suitable for use on a wide range of devices and browsers.

### As a returning user I'd like:
**"To login and logout easily."**
* A call-to-action button linking to the login page can be found in the navigation bar at all times.
* The logging in process is just as simple as registering with only a username and password required with each input field being clearly labelled.
* The validation requirements are the same as those for when registering an account. When this criteria isn’t met then the user is informed of this using a little note below the input field – as shown below.
* A user is clearly informed if the username or password provided is incorrect via a flash message above the form.
* A call-to-action button that logs the user out is found in the navigation bar when a user is logged in, [shown here.](readme-docs/screenshots/user-stories/user-stories13.jpg)

![Login form validation messages.](readme-docs/screenshots/user-stories/user-stories12.jpg)


**"To be able to create and post new recipes to the site."**
* Adding a recipe is done via a form. The link to access this is always in the navigation bar once logged in.
* This process requires more information this time around and all fields are required to be filled in to be able to submit the form.
* Each input field is clearly labelled and has an additional note informing a user about the validation requirements. If the validation requirements aren’t met then the user is informed of this using a little note below the input field – as shown below.
* On successful completion we get sent to our newly created recipe page!

![Adding my toast recipe.](readme-docs/screenshots/user-stories/user-stories16.jpg)


**"Access to my own personal profile where I can view my posted recipes."**
* Profile page can be accessed via the link found in the navigation bar once logged in, [displayed here.](readme-docs/screenshots/user-stories/user-stories13.jpg)
* Once on the page relevant call-to-action buttons are displayed as well as the delete profile button.
* On your profile page all recipes you’ve uploaded will appear in the same card format used throughout as [shown here.](readme-docs/screenshots/user-stories/user-stories14.jpg)

**"The ability to edit and delete my recipes."**
* Call-to-action buttons appear on all your recipe cards when they are displayed making editing and deleting easy. These buttons are also accessible on the individual recipe pages, if it’s your recipe as shown below.
* Deleting a recipe is a two-step process where confirmation is needed in order to avoid any accidents.
* Editing a recipe will take you to the relevant form, which will be pre-populated with the data that’s already been provided. This means you just have to worry about the editing.

![Recipe page for an omelette.](readme-docs/screenshots/user-stories/user-stories15.jpg)


**"Feedback when I’m interacting with the site and whilst inputting data."**
* The site is constantly relaying messages in the form of:
    * Flash messages show when a function is completed or access is denied.
    * Validation messages appear on forms when input is incorrect.
    * Messages get displayed when no results are found or nothing exists.

### As the site owner / admin I want:
**"The ability to edit and delete any recipes regardless of who posted it."**
* I’ve put measures in place so that any user that has “is_admin” set to true in the users collection in MongoDB can edit and delete any recipe on the site (they can still add their own recipes too). Setting this to true can only be done through MongoDB currently.
* When logged in to an account with admin rights all call-to-action buttons on recipe cards will be visible as shown below. Call-to-action buttons will also be visible on each individual recipe page.
* I felt this was an important implement to feature so that any offensive material or spam like posts can be easy be deleted. This way, with these rights I can control the content of the site and maintain its appearance of being a family-orientated platform.

![All recipes page when logged in as admin.](readme-docs/screenshots/user-stories/user-stories10.jpg)


**"The ability to remove user profiles if needed."**
* Currently the only way to achieve this is by doing it manually on the MongoDB dashboard when logged in. Due to time constraints I wasn’t able to administer this functionality through the sites interface but it has been added to my features left to implement list.

**"To be able to add new categories, edit and delete existing ones."**
* The manage category page is only accessible to users that have “is_admin” set to true.
* On log in the admin or superuser account will have a "manage category" button as part of their user profile dashboard for quick navigation to the page.
* The page is set up as shown below and is very simple to use. The new category gets inputted into the form and on successful submission the category becomes live and can be accessed throughout the site.
* To delete a category is just as simple as each category card comes with its own delete button.

![Manage categories page.](readme-docs/screenshots/user-stories/user-stories11.jpg)