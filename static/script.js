document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.querySelector('#login-form');
    const signupForm = document.querySelector('#signup-form');
    const toggleButtons = document.querySelectorAll('.toggle-btn');
    const loginError = document.querySelector('#login-error');
    const signupError = document.querySelector('#signup-error');

    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            document.querySelector('.login-form').classList.toggle('slide-left');
            document.querySelector('.signup-form').classList.toggle('slide-right');
            
            loginError.textContent = '';
            signupError.textContent = '';
        });
    });

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(loginForm);
        
        fetch('/login', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.redirect;
            } else {
                loginError.textContent = data.message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            loginError.textContent = 'An error occurred. Please try again.';
        });
    });

    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(signupForm);
        
        if (formData.get('password') !== formData.get('confirm_password')) {
            signupError.textContent = 'Passwords do not match';
            return;
        }
        
        fetch('/signup', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                window.location.href = data.redirect;
            } else {
                signupError.textContent = data.message;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            signupError.textContent = 'An error occurred. Please try again.';
        });
    });
});
