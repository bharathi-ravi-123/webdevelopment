document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("myform");
    const fnameInput = document.getElementById("fname");
    const emailInput = document.getElementById("mail");
    const passInput = document.getElementById("passw");
    const emailFeedback = document.getElementById("emailFeedback");
    const passFeedback = document.getElementById("passFeedback");

    emailInput.addEventListener("input", function () {
        const email = emailInput.value.trim().toLowerCase();

        if (registeredEmails.includes(email)) {
            emailFeedback.textContent = "⚠️ Email already registered!";
            emailFeedback.style.color = "red";
        } else if (!email.includes("@") || !email.includes(".")) {
            emailFeedback.textContent = "❌ Invalid email format.";
            emailFeedback.style.color = "red";
        } else {
            emailFeedback.textContent = "✅ Email looks good.";
            emailFeedback.style.color = "green";
        }
    });

    passInput.addEventListener("input", function () {
        const password = passInput.value;
        const strongPassword = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

        if (strongPassword.test(password)) {
            passFeedback.textContent = "✅ Strong password.";
            passFeedback.style.color = "green";
        } else {
            passFeedback.textContent = "❌ Use 8+ chars, mix of uppercase, lowercase, number & special.";
            passFeedback.style.color = "red";
        }
    });
});



