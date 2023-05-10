const email = document.getElementById('email');
const first_name = document.getElementById('firstName');
const last_name = document.getElementById('lastName');
const phone_number = document.getElementById('phonenumber');
const password = document.getElementById('password');
const confirm_password = document.getElementById('conf_password');
const submitBTN = document.getElementById('submit_button');

const symbols = ['$','!','@','#','%','^','&','*','_','+','=','-','`','~'];
/* Error Handling For Input Fields*/
const email_error = document.getElementById('email_error');
const firstName_error = document.getElementById('firstName_error');
const lastName_error = document.getElementById('lastName_error');
const phonenumber_error = document.getElementById('phonenumber_error');
const password_error = document.getElementById('password_error');
const conf_password_error = document.getElementById('conf_password_error');


const verify_fields = (event) => {
  // FLAG_EMAIL = email.value.includes("@my.bcit.ca");
  const FLAG_EMAIL = email.value.includes("@");
  const FLAG_FIRST_NAME = first_name.value.length > 0;
  const FLAG_LAST_NAME = last_name.value.length > 0;
  const FLAG_PHONE_NUMBER = phone_number.value.length == 10 || phone_number.value.length == 0;
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


const verify_email = (event) => {
  const email = document.getElementById('email');
  const email_error = document.getElementById('email_error');
  const isValidEmail = email.value.includes("@");

  if (!isValidEmail) {
    email_error.textContent = "Please provide a valid email address.";
    email_error.classList.add("error");
  } else {
    email_error.textContent = "";
    email_error.classList.remove("error");
  }
};

const verify_firstName = (event) => {
  const first_name = document.getElementById('firstName');
  const firstName_error = document.getElementById('firstName_error');
  const isValidFirstName = first_name.value.length > 0;

  if (!isValidFirstName) {
    firstName_error.textContent = "Please provide a valid first name.";
    firstName_error.classList.add("error");
  } else {
    firstName_error.textContent = "";
    firstName_error.classList.remove("error");
  }
};

const verify_lastName = (event) => {
  const last_name = document.getElementById('lastName');
  const lastName_error = document.getElementById('lastName_error');
  const isValidLastName = last_name.value.length > 0;

  if (!isValidLastName) {
    lastName_error.textContent = "Please provide a valid last name.";
    lastName_error.classList.add("error");
  } else {
    lastName_error.textContent = "";
    lastName_error.classList.remove("error");
  }
};

const verify_password = (event) => {
  const password = document.getElementById('password');
  const password_error = document.getElementById('password_error');
  const hasSymbol = symbols.some((symbol) => password.value.includes(symbol));

  if (password.value.length < 4) {
    password_error.textContent = "Password is too short.";
    password_error.classList.add("error");
  } else if (!hasSymbol) {
    password_error.textContent = "Password must contain a symbol. (e.g. $, !, @, #, %, ^, &, *, _, +, =, -, `, ~)";
    password_error.classList.add("error");
  }
   else {
    password_error.textContent = "";
    password_error.classList.remove("error");
  }
};

const verify_confirm_password = (event) => {
  const confirm_password = document.getElementById('conf_password');
  const conf_password_error = document.getElementById('conf_password_error');
  const isValidpassword =  confirm_password.value === password.value;

  if (!isValidpassword) {
    conf_password_error.textContent = "Passwords do not match.";
    conf_password_error.classList.add("error");
  } else {
    conf_password_error.textContent = "";
    conf_password_error.classList.remove("error");
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

submitBTN.addEventListener('click', Submit);
for (element of [email, first_name, last_name, password, confirm_password, phone_number]) {
  element.addEventListener('input', verify_fields);
}

/*
  Event Listeners Handlers for each input field
*/
email.addEventListener('input', verify_email);
first_name.addEventListener('input', verify_firstName);
last_name.addEventListener('input', verify_lastName);
password.addEventListener('input', verify_password);
confirm_password.addEventListener('input', verify_confirm_password);
