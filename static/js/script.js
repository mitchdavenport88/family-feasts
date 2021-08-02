// change bootstrap classes for register / login / logout depending on breakpoint
// code found on https://www.w3schools.com/howto/howto_js_media_queries.asp and edited accordingly
function linksToButton(maxScreenWidth) {
    const buttonsToChange = document.getElementsByClassName('link-button');
    if (maxScreenWidth.matches) {
        for (let i = 0; i < buttonsToChange.length; i++ ) {
            buttonsToChange[i].classList.remove("btn", "my-btn");
            buttonsToChange[i].classList.add("nav-link");
        }      
    } else {
        for (let i = 0; i < buttonsToChange.length; i++ ) {
            buttonsToChange[i].classList.add("btn", "my-btn");
            buttonsToChange[i].classList.remove("nav-link");
        }
    }
}
const maxScreenWidth = window.matchMedia("(max-width: 991px)");
linksToButton(maxScreenWidth);
maxScreenWidth.addEventListener("change", linksToButton);

// https://www.csestack.org/hide-show-password-eye-icon-html-javascript/
const togglePassword = document.getElementById('togglePassword');
const password = document.getElementById('password');
const toggleConfirmPassword = document.getElementById('toggleConfirmPassword');
const confirmPassword = document.getElementById('confirm-password');
if (togglePassword) {
    togglePassword.addEventListener('click', function() {
        const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
        password.setAttribute('type', type);
        this.classList.toggle('fa-eye-slash');
    });
}
if (toggleConfirmPassword) {
    toggleConfirmPassword.addEventListener('click', function() {
        const type = confirmPassword.getAttribute('type') === 'password' ? 'text' : 'password';
        confirmPassword.setAttribute('type', type);
        this.classList.toggle('fa-eye-slash');
    });    
}
