const email = document.getElementById('email');
const submitBTN = document.getElementById('submit_button');
const emailconfirm = document.getElementById('conf_email')
const cancelBTN = document.getElementById("cancel_listing");

const verify_email = (event) => {
  const email = document.getElementById('email');
  const email_error = document.getElementById('email_error');
  const isValidEmail = email.value.includes("@");

  if (!isValidEmail) {
    email_error.textContent = "Please provide a valid email address.";
    email_error.classList.add("error-message");
  } else {
    email_error.textContent = "";
    email_error.classList.remove("error-message");
  }
};
const verify_fields = (event) => {
    const FLAG_EMAIL = email.value.includes("@");
    if (FLAG_EMAIL) {
        submitBTN.classList.remove("disabled");
      }
      else{
        submitBTN.classList.add("disabled");
      }
}

cancelBTN.addEventListener("click", () => {
    let inputFields = document.querySelectorAll("input");
    for (let i = 0; i < inputFields.length; i++) {
      inputFields[i].value = "";
    }
  });

  const Submit = async () => {
    let hash_password = await hashedPassword(password.value);
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
        password: hash_password
      })
    })
      .then((response) => {
        return Promise.all([response.json(), response.status]);
      })
      .then(([json, status]) => {
        let message = json.message;
        localStorage.setItem("message", message);
        if (status == 200) {
          window.location.href = "/login";
        } else {
          window.location.href = "/sign-up";
        }
      })
      .catch((error) => {
        console.log(error);
      });
    };