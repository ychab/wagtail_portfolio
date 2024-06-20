(() => {
    document.addEventListener("DOMContentLoaded", () => {

        document.querySelector("#contactForm").addEventListener("submit", (event) => {
            event.preventDefault();

            var formElem = event.target;
            var submitButtonElem = document.querySelector("#submitButton");
            var successElem = document.querySelector("#submitSuccessMessage");
            var errorElem = document.querySelector("#submitErrorMessage");

            // In case of multiples submissions, clear any previous messages.
            successElem.classList.add("d-none");
            errorElem.classList.add("d-none");
            [...formElem.elements].forEach((item) => {
               item.classList.remove("is-invalid");
            });

            // Disable submit button until AJAX call is complete to prevent duplicate messages
            submitButtonElem.disabled = true;

            fetch(formElem.action, {
                method: formElem.method,
                body: new FormData(formElem),
                headers: {
                    "Accept": "application/json",
                },
            }).then((response) => {
                if (!response.ok) {
                    errorElem.classList.remove("d-none");
                }
                return response.json();
            }).then((data) => {
                if ("success" in data) {
                    formElem.reset();
                    successElem.classList.remove("d-none");
                } else {
                    for (var key in data) {
                        var elem = document.querySelector(`#${key}`);
                        elem.classList.add("is-invalid");
                        elem.nextElementSibling.textContent = data[key][0].message;
                    }
                }
            }).catch((error) => {
                // Network errors or weird stuff like that!
                errorElem.classList.remove("d-none");
            }).finally(() => {
                // Don't forgot to release the button!
                submitButtonElem.disabled = false;
            })
        });
    });
})();
