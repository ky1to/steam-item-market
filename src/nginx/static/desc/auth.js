var modal = document.getElementById("modal");
var span = document.getElementsByClassName("close")[0];

document.addEventListener("DOMContentLoaded", function() {
    const btns = document.querySelectorAll(".btn");
    const formSignin = document.querySelector(".form-signin");
    const formSignup = document.querySelector(".form-signup");
    
    btns.forEach(function(btn) {
        btn.addEventListener("click", function() {
            formSignin.classList.toggle("form-signin-left");
            formSignup.classList.toggle("form-signup-left");
        });
    });
});


function btn_register(){
    const password = document.getElementById("reg-password");
    const confirmpassword = document.getElementById("reg-confirmpassword");
    if (password == confirmpassword){
        const username = document.getElementById("reg-username");
        const email = document.getElementById("reg-email");
        register(username.value, password.value, email.value)
        modal.style.display = "none"
    }
}

function btn_login(){
    const username = document.getElementById("log-username");
    const password = document.getElementById("log-password");
    login(username.value, password.value)
    modal.style.display = "none"
}

if (localStorage.getItem('token') == null || localStorage.getItem('token') == "null"){
    modal.style.display = "block";
}

function login(username, password) {
    fetch('/api/auth/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            username: username,
            password: password
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        localStorage.setItem('token', data.access_token);
    }).catch(error => {querySelector
        console.error('There was a problem with the fetch operation:', error);
    });
}

function register(username, password, email) {
    fetch('/api/auth/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            username: username,
            password: password,
            email: email
        })
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        localStorage.setItem('token', data.access_token);
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}

function getUserInfo() {
    const token = localStorage.getItem('token');
    console.log(token)
    fetch('/api/user/', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    }).then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    }).then(data => {
        console.log(data);
    }).catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}