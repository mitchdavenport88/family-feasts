# Milestone Project Three - Testing

The live site can be viewed here - [Family Feasts](https://family-feasts.herokuapp.com/).

[Back to README file.](README.md)

## Testing
My code has been put through the following:
* W3C HTML validation. The W3C validator doesn't like jinja templating and raises a bad value error for every instance. So to avoid this I put each HTML file through the validator as it appears in the view page source document (accessed by left clicking the page).
    * Consider using the h1 element as a top-level heading only - index
    * Duplicate ID staticBackdropLabel - recipes (changed)
    * Section lacks heading - login, register, add & edit recipe, changed to div tags as they are already in section tags(base)
* CSS AutoPrefixer.
* W3C CSS validation - passed.
* JSHint JavaScript validation - no errors.
* PEP8 online check - boths files all right.
