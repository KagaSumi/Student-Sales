const email = document.getElementById("email");
const password = document.getElementById("password");
const loginBTN = document.getElementById("login_button");

function send_request() {
  const payload = { email: email.value, password: password.value };
  fetch("/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => {
      return Promise.all([response.json(), response.status]);
    })
    .then(([json, status]) => {
      let message = json.message;
      localStorage.setItem("message", message);
      if (status == 400) {
        window.location.href = '/login';
      } 
      else {
        window.location.href = '/profile';
      }
    })
    .catch((error) => {
      console.log(error);
    });
}


loginBTN.addEventListener("click", send_request);
