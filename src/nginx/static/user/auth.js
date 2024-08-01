global_token = ""

function login() {
    fetch('/api/auth/token', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({
            username: "vlad",
            password: "1111"
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
    fetch('/api/user/', {/*
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({'access_token': token})
        */
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