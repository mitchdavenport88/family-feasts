# Family Feasts

### Milestone Project Three
Family Feasts is a cooking e-book that aims to build a library of recipes that will inspire households and families to get off the couch and into the kitchen to cook together! Any member of the family will be able to browse, search and follow recipes that have been posted up by the online community. Users will be encouraged to join the community by signing up to share their family favourites in order to encourage others to cook and spend time with their loved ones.

## Demo
The live site can be viewed here - [Family Feasts](https://family-feasts.herokuapp.com/).

GitHub repository can be viewed here - [mitchdavenport88/family-feasts](https://github.com/mitchdavenport88/family-feasts).

![Site Mockup](readme-docs/screenshots/amiresponsive-image1.jpg)

## UX
### Strategy
The aim is to create a simple, user friendly recipe e-book using the functionality of creating, reading, updating and deleting data objects. The sites premise is built around the idea of getting households (primarily families) cooking together, spending time together and making tea time that little bit more exciting! Although the site will have a family orientated feel and be suited for users of all ages there is no reason why it shouldn’t also be suitable for other types of users such as couples and housemates as the message is still relevant.

Any user should be able to access and view recipes that have been uploaded to the platform. Results and information should be shown in an appropriate and clear way, with the user having the ability to filter and search for recipes by using keywords or ingredients. In order to create, edit and delete recipes users will have to register. Once registered users will also have access to their own personal profile page/dashboard where their uploaded recipes will be displayed. The site’s admin will have all these privileges along with the ability to edit and delete other user’s entries along with being able to add further content at a later date.

### User Stories
As a first time user I'd like:
* To access and view all recipes.
* To be able to browse by recipe category.
* Information on each recipe to be presented in a clear and concise manner.
* To search for suitable recipes by using keywords or ingredients.
* To sign up to the community easily.
* The site to be easy to navigate around and user friendly.
* To do all of the above regardless of what device I’m using.

As a returning user I'd like:
* To login and logout easily.
* To be able to create and post new recipes to the site.
* Access to my own personal profile where I can view my posted recipes.
* The ability to edit and delete my recipes.
* Feedback when I’m interacting with the site and whilst inputting data.

As the site owner / admin I want:
* The ability to edit and delete any recipes regardless of who posted it.
* The ability to remove user profiles if needed.
* To be able to add new categories and edit and delete existing ones.

### Scope - functionality
* The site must have a section where recipes are displayed, for all to see.
* Present the relevant information on each individual recipe on its own page following a pre-determined template.
    * This information should be displayed in a visually appealing way.
    * Information should be clear to understand and follow.
* Allow users to login or register in order to be able to contribute towards the sites content (add, edit and delete recipes).
* The user will be able to add, edit and delete recipes once logged in/registered.
    * Methods of data input must be clear and easy to operate.
    * Restrictions will need to be placed on what registered users can see and use verses what unregistered users can see and use.
    * The site will need to feed relevant information back to the user when required and appropriate. 
* We want the user to remain engaged throughout use so must be user-friendly and easy to navigate around.
* Function as expected:
    * Fully responsive on all devices.
    * Links or buttons take you to the expected place or complete the expected task.
    * External links must open in new windows.

### Scope - content
* A home page that tells the user all about Family Feasts and talks about the site’s message in more detail.
* A recipes page, which the rest of the site will be built around.
    * All recipes will need to be shown on this page in a visually appealing manner.
    * Users will want the ability to interact with the page by filtering and searching for results.
    * Each recipe card should act as a link to the recipe’s own page and to it's functions.
* Individual recipe pages will follow a template, which will be populated with information pulled from the database.
* Log in / registration forms will not only interact with the database but will grant authorization to add, edit and delete data objects via the site.
* Logout function. (restricted)
* A personalised profile page that shows recipes uploaded by the user. (restricted)
* Add recipe form / page should add new data objects to the database and then display them on the recipes page. (restricted)
* Edit recipe form / page will edit data that already exists in the database and update the information displayed on the site. (restricted)
* Recipe deletion should remove the data object from the database, with information no longer able to be viewed by users. This could be a process where confirmation of deletion would be required. (restricted)

<!-- ### Structure -->


### Skeleton
Initial idea - [sketch](readme-docs/wireframes/initial-wireframe-sketch.jpg)

Home - [desktop](readme-docs/wireframes/home-desktop.png) | 
[tablet](readme-docs/wireframes/home-tablet.png) | 
[mobile](readme-docs/wireframes/home-phone.png).

Register and login forms - [desktop](readme-docs/wireframes/userforms-desktop.png) | 
[tablet](readme-docs/wireframes/userforms-tablet.png) | 
[mobile](readme-docs/wireframes/userforms-phone.png).

View recipes - [desktop](readme-docs/wireframes/recipe-menu-desktop.png) | 
[tablet](readme-docs/wireframes/recipe-menu-phone.png) | 
[mobile](readme-docs/wireframes/recipe-menu-tablet.png).

Individual recipe page - [desktop](readme-docs/wireframes/view-recipe-desktop.png) | 
[tablet](readme-docs/wireframes/view-recipe-tablet.png) | 
[mobile](readme-docs/wireframes/view-recipe-phone.png).

Add and update recipes - [desktop](readme-docs/wireframes/recipe-forms-desktop.png) | 
[tablet](readme-docs/wireframes/recipe-forms-tablet.png) | 
[mobile](readme-docs/wireframes/recipe-forms-phone.png).

User profile - [desktop](readme-docs/wireframes/userprofile-desktop.png) | 
[tablet](readme-docs/wireframes/userprofile-tablet.png) | 
[mobile](readme-docs/wireframes/userprofile-phone.png).

<!-- ### Surface -->


## Testing
Separate testing document can be found here - [testing documentation.](TESTING.md)

## Deployment
### Heroku deployment
This project is hosted by Heroku but is still deployed from the master branch of a GitHub repository. The following steps were taken to deploy this project:
1. Login to Heroku.
2. Click the **create new app** button. Give your app a unique name (this could match the name of the repository) and select the region from the dropdown menu that is closest to you geographically. Click the **create app button** then a dashboard for this newly created app will load.

Ideally we want Heroku to automatically pick up changes that are pushed to the GitHub repository. In order to do this the following steps were taken:

3. On the dashboard scroll down to the “Deployment method” section and click the connect to GitHub button (you may have to log in to GitHub here). In the section below called “Connect to GitHub” your profile should now appear. Now you can search for the repository you wish to link to Heroku, select it and click **connect**.
4. Back at the top of the dashboard select settings. Scroll down to the “Config Vars” section and click the **Reveal Config Vars** button. In here enter the environment variables from the `env.py` file that was created when setting up flask. In this instance I included the fields and values of:
    * IP
    * PORT
    * SECRET_KEY
    * MONGO_URI - used to connect to MongoDB
    * MONGO_DBNAME - as named in MongoDB
5. Before completing the connection we need to create, commit and push the `requirements.txt` file and `Procfile` to the GitHub repository.
    * requirements.txt tells Heroku the applications and dependencies required to run the app (`app.py`).
    * The Procfile instructs Heroku on how to run and which file runs the app.
6. Go back to the top of the Heroku dashboard and select deploy. Scroll down to the “Automatic deployment” section, check that the main branch is selected and then click **Enable Automatic Deploys**.
7. Underneath is another section – “Manual deploy”. We’re ready to deploy now so click **deploy branch**. This will take a minute to receive the code from GitHub and build the app. Once this process is complete a message confirming that the app was successfully deployed will show.
8. Click **view to launch app** to view.
9. Heroku is now set up. And will automatically update whenever commits are pushed to Github via our IDE.

### Adding and committing files
I’ve been using Gitpod to write my code and using the terminal to add, commit and push code from my workspace to GitHub where it is stored remotely as shown in the course content.
1. Typing `git add` into the terminal will move files to the staging area. You should normally do this once a couple of minor additions or changes have been made or one large change or addition has been made. `git add .` will add all files that have been modified, the full stop here means all. If I want to be more selective I can type in the file name e.g. index.html or the files pathway e.g. assets/css/style.css instead of the full stop e.g. `git add index.html`.
2. To send these changes to the local repository we use `git commit`. Normally you'll want to include a brief description of these changes so instead use `git commit –m “ ”`. Between the “ ” write a clear, concise message detailing what this commit has done.
3. To view the changes on Heroku or when you want to send your work to the remote repository (GitHub in this instance) then use the `git push` command. This pushes all the previous commits made to the remote repository. Once Heroku is set up for the repository it will automatically pick up these changes and display the most up to date version that has been pushed.

### Cloning
You can clone a repository so that it can be worked on locally in an IDE such as VSCode by following these steps:
1. Log in to GitHub and navigate to the repository you wish to clone.
2. Click the button that reads **code**. This button is situated to the left of the green Gitpod button near the top of the page.
3. To clone the repository using HTTPS, copy the link shown whilst HTTPS is selected. The link will look something like this: `https://github.com/YOUR-USERNAME/YOUR-REPOSITORY`
4. Open your local IDE and in the terminal navigate to the working directory of where you wish to insert the cloned directory.
5. Type `git clone` followed by the link you copied in step 3 into the terminal, this will look something like this: `git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY`
6. Press **enter** and the clone will be created in your selected / current working directory (cwd).

Taken from GitHub's documentation on cloning, which can be found [here.](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository#cloning-a-repository-to-github-desktop)