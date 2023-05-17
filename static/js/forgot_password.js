const password = document.getElementById('password');
const confirm_password = document.getElementById('conf_password');
const submitBTN = document.getElementById('submit_button');
const pattern = /^[0-9]{3}-?[0-9]{3}-?[0-9]{4}$/;
const symbols = ['$','!','@','#','%','^','&','*','_','+','=','-','`','~'];
const password_error = document.getElementById('password_error');
const conf_password_error = document.getElementById('conf_password_error');
const cancelBTN = document.getElementById("cancel_listing");

const verify_fields = (event) => {
    const FLAG_PASSWORD = password.value.length >= 4 && password.value === confirm_password.value;
    if (FLAG_PASSWORD) {
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
      email_error.classList.add("error-message");
    } else {
      email_error.textContent = "";
      email_error.classList.remove("error-message");
    }
  };

const verify_password = (event) => {
    const password = document.getElementById('password');
    const password_error = document.getElementById('password_error');
    const hasSymbol = symbols.some((symbol) => password.value.includes(symbol));
  
    if (password.value.length < 4) {
      password_error.textContent = "Password is too short.";
      password_error.classList.add("error-message");
    } else if (!hasSymbol) {
      password_error.textContent = "Password must contain a symbol.";
      password_error.classList.add("error-message");
    }
     else {
      password_error.textContent = "";
      password_error.classList.remove("error-message");
    }
  };
  
const verify_confirm_password = (event) => {
    const confirm_password = document.getElementById('conf_password');
    const conf_password_error = document.getElementById('conf_password_error');
    const isValidpassword = confirm_password.value === password.value;

    if (!isValidpassword) {
        conf_password_error.textContent = "Passwords do not match.";
        conf_password_error.classList.add("error-message");
    } else {
        conf_password_error.textContent = "";
        conf_password_error.classList.remove("error-message");
    }
};

async function hashedPassword(password) {
    const utf8 = new TextEncoder().encode(password);
    const hashBuffer = await crypto.subtle.digest('SHA-256', utf8);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    const hashHex = hashArray
        .map((bytes) => bytes.toString(16).padStart(2, '0'))
        .join('');
    return hashHex;
};

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

cancelBTN.addEventListener("click", () => {
  let inputFields = document.querySelectorAll("input");
  for (let i = 0; i < inputFields.length; i++) {
    inputFields[i].value = "";
  }
});

submitBTN.addEventListener('click', Submit);
for (element of [password, confirm_password]) {
    element.addEventListener('input', verify_fields);
}

password.addEventListener('input', verify_password);
confirm_password.addEventListener('input', verify_confirm_password);