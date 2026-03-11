const api = "http://" + window.location.hostname + ":5000";

function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  if (!username || !password) {
    alert("Enter username and password");
    return;
  }

  fetch(api + "/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  })
  .then(response => {
    if (!response.ok) {
      return response.json().then(data => { throw new Error(data.message); });
    }
    return response.json();
  })
  .then(data => {
    localStorage.setItem("user", username);
    window.location.href = "about.html";
  })
  .catch(error => {
    alert(error.message);
    console.error("Login error:", error);
  });
}

// Handle Enter key / form submit
document.getElementById("loginForm").addEventListener("submit", function(e) {
  e.preventDefault();
  login();
});

// Display welcome message
window.onload = function () {
  const welcome = document.getElementById("welcome");
  if (welcome) {
    const user = localStorage.getItem("user");
    welcome.textContent = "WELCOME, " + user.toUpperCase();
  }
};

// Navigation
function goDiagram() { window.location.href = "diagram.html"; }
function goBack() { window.location.href = "about.html"; }
