const email = document.getElementById("email");
const first_name = document.getElementById("firstName");
const last_name = document.getElementById("lastName");
const phone_number = document.getElementById("phonenumber");
const password = document.getElementById("password");
const confirm_password = document.getElementById("conf_password");
const submitBTN = document.getElementById("submit_button");

const verify_fields = (event) => {
  // FLAG_EMAIL = email.value.includes("@my.bcit.ca");
  const FLAG_EMAIL = email.value.includes("@");
  const FLAG_FIRST_NAME = first_name.value.length > 0;
  const FLAG_LAST_NAME = last_name.value.length > 0;
  const FLAG_PHONE_NUMBER = phone_number.value.length == 10;
  const FLAG_PASSWORD = password.value.length >= 4 && password.value === confirm_password.value;
  if (FLAG_EMAIL && 
    FLAG_FIRST_NAME && 
    FLAG_LAST_NAME && 
    FLAG_PASSWORD && 
    FLAG_PHONE_NUMBER) {
    submitBTN.classList.remove("disabled");
  }
  else{
    submitBTN.classList.add("disabled");
  }
};

const Submit = () => {
  fetch("/sign-up", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      email: email.value.toLowerCase(),
      first_name: first_name.value,
      last_name: lastName.value,
      phone_number: phone_number.value,
      password: password.value
    })
  })
    .then((response) => {
      return Promise.all([response.json(), response.status]);
    })
    .then(([json, status]) => {
      let message = json.message;
      localStorage.setItem("message", message);
      if (status == 400) {
        window.location.href = "/sign-up";
      } else {
        window.location.href = "/profile";
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

submitBTN.addEventListener("click", Submit);
for (element of [email, first_name, last_name, password, confirm_password, phone_number]) {
  element.addEventListener("input", verify_fields);
}
