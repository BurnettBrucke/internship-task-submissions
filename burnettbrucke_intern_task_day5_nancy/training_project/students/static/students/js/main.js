// students/static/students/js/main.js
//
// Prevents double submission on every <form> in the app: once a submit
// button is clicked, it's immediately disabled (and visually dimmed via
// the .is-submitting class in main.css) so a slow connection or an
// impatient double-click can't fire the same POST twice (e.g. adding the
// same student, or updating marks, more than once).
document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("form").forEach(function (form) {
        form.addEventListener("submit", function () {
            const submitButtons = form.querySelectorAll('button[type="submit"]');
            submitButtons.forEach(function (btn) {
                // Let the browser submit the form first, then disable --
                // disabling before submit can prevent the button's value
                // from being sent, and can block the submit entirely in
                // some browsers.
                setTimeout(function () {
                    btn.classList.add("is-submitting");
                    btn.disabled = true;
                }, 0);
            });
        });
    });
});
