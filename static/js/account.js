const first_name = document.getElementById("first_name");
const last_name = document.getElementById("last_name");
const update_button = document.getElementById("update_button");
const delete_button = document.getElementById("delete_button");

const symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '='];

const old_password = document.getElementById("old_password");
const old_password_error = document.getElementById('password_error');

const new_password = document.getElementById("new_password");
const new_password_error = document.getElementById('new_password_error');

const confirm_password = document.getElementById("confirm_password");
const confirm_password_error = document.getElementById("confirm_password_error");

const phone_number = document.getElementById("phone_number");
const phone_number_error = document.getElementById("phone_number_error");


const delete_user = () => {
  
}

const verify_fields = (event) =>{
    if (first_name.value.length == 0 || last_name.value.length == 0) {
        update_button.classList.add("disabled");
    }
    else{
        update_button.classList.remove("disabled");
    }
}

const update_request = () => {
  // Check whether the new password meets the requirements
  verify_new_password();

  // Check whether the confirmed password matches the new password
  verify_confirm_password();

  // If there is no error message, send a request to update the profile
  if (!new_password_error.textContent && !confirm_password_error.textContent) {
      let payload = { first_name: first_name.value, last_name: last_name.value, phone_number: phone_number.value };
      fetch('/update_profile', {
          method: 'PUT',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
      })
      .then((response) => {
          return Promise.all([response.json(), response.status]);
      })
      .then(([json, status]) => {
          let message = json.message;
          localStorage.setItem('message', message);
          window.location.href = '/account';
      })
      .catch((error) => {
          console.log(error);
      });
  }
};

update_button.addEventListener("click",update_request);
for (element of [first_name,last_name]){
    element.addEventListener('input', verify_fields);
}

const verify_new_password = (event) =>{
  const new_password = document.getElementById('new_password');
  const new_password_error = document.getElementById('new_password_error');
  const hasSymbol = symbols.some((symbol) => new_password.value.includes(symbol));

  if (new_password.value.length < 4) {
    new_password_error.textContent = "Password is too short.";
    new_password_error.classList.add("error-message");
  } else if (!hasSymbol) {
    new_password_error.textContent = "Password must contain a symbol.";
    new_password_error.classList.add("error-message");
  }
   else {
    new_password_error.textContent = "";
    new_password_error.classList.remove("error-message");
  }
};

const verify_confirm_password = (event) => {
  const confirm_password = document.getElementById('confirm_password');
  const confirm_password_error = document.getElementById('confirm_password_error');
  const isValidpassword = confirm_password.value === new_password.value;

  if (!isValidpassword) {
    confirm_password_error.textContent = "Passwords do not match.";
    confirm_password_error.classList.add("error-message");
  } else {
    confirm_password_error.textContent = "";
    confirm_password_error.classList.remove("error-message");
  }
};

const verify_phone_number = (event) => {
  const phone_number = document.getElementById('phone_number');
  const phone_number_error = document.getElementById('phone_number_error');
  const pattern = /^[0-9]{3}-?[0-9]{3}-?[0-9]{4}$/; // 10-digit
  const isValidPhoneNumber = pattern.test(phone_number.value) || phone_number.value.length == 0;
  
  if (!isValidPhoneNumber) {
    phone_number_error.textContent = "Please enter a valid 10-digit phone number.";
    phone_number_error.classList.add("error-message");
  } else {
    phone_number_error.textContent = "";
    phone_number_error.classList.remove("error-message");
  }
};

/* Event Listeners */
new_password.addEventListener('input', verify_new_password);
confirm_password.addEventListener('input', verify_confirm_password);
phone_number.addEventListener('input', verify_phone_number);

phone_number.addEventListener('keypress', function(event) {
  // Prevent non-numeric input
  if (isNaN(parseInt(event.key))) {
    event.preventDefault();
    return;
  }
  
  // Limit input to 10 digits
  const currentValue = phone_number.value.replace(/[^0-9]/g, '');
  if (currentValue.length >= 10) {
    event.preventDefault();
  }
});

update_button.addEventListener("click", () => {updateUser()})