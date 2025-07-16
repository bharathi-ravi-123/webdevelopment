function validateloginform() {
    const email = document.getElementById('email').value.trim();
    const password = document.getElementById('pass').value.trim();
    const errorMsg = document.getElementById('errormsg');

    
    errorMsg.textContent = "...";

    if (!email || !password) {
        errorMsg.textContent = "Please fill in both email and password.";
        return false;
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        errorMsg.textContent = "Please enter a valid email address.";
        return false;
    }

    return true;
}

