
function sendPostRequest() {
    const user = document.getElementById("inputText").value; // 
    const data = { name: user}

    fetch('/test', {
        method: "POST",
        headers: {"content-type": "application/json"},
        body: JSON.stringify(data)
     })
}
