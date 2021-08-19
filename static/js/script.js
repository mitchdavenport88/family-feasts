// Code found on https://www.w3schools.com/howto/howto_js_media_queries.asp and edited accordingly
/** Checks page width and changes register / login / logout links to buttons depending on breakpoint */
function linksToButton(maxScreenWidth) {
    const buttonsToChange = document.getElementsByClassName('link-button');
    if (maxScreenWidth.matches) {
        for (let i = 0; i < buttonsToChange.length; i++ ) {
            buttonsToChange[i].classList.remove('btn', 'my-btn');
            buttonsToChange[i].classList.add('nav-link');
        }      
    } else {
        for (let i = 0; i < buttonsToChange.length; i++ ) {
            buttonsToChange[i].classList.add('btn', 'my-btn');
            buttonsToChange[i].classList.remove('nav-link');
        }
    }
}
const maxScreenWidth = window.matchMedia('(max-width: 991px)');
linksToButton(maxScreenWidth);
maxScreenWidth.addEventListener('change', linksToButton);