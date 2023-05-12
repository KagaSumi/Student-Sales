const first_name = document.getElementById("first_name");
const last_name = document.getElementById("last_name");
const update_button = document.getElementById("update_button");
const delete_button = document.getElementById("delete_button");

const symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '='];


const phone_number = document.getElementById("phone_number");
const phone_number_error = document.getElementById("phone_number_error");


const delete_request = () => {
  fetch('/delete_user', {
      method: 'DELETE',

  })
  .then((response) => {
      return Promise.all([response.json(), response.status]);
  })
  .then(([json, status]) => {
      let message = json.message;
      localStorage.setItem('message', message);
      if (status == 400){
        window.location.href = '/account';
      }
      window.location.href = '/'
  })
  .catch((error) => {
      console.log(error);
  });
}

const verify_fields = (event) =>{
    if (first_name.value.length == 0 || last_name.value.length == 0 || !(phone_number.value.length == 0 || phone_number.value.length == 10)) {
        update_button.classList.add("disabled");
    }
    else{
        update_button.classList.remove("disabled");
    }
}

const update_request = () => {
    let payload = {first_name: first_name.value, last_name: last_name.value, phone_number:phone_number.value}
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


update_button.addEventListener("click",update_request);
delete_button.addEventListener("click",delete_request);
for (element of [first_name,last_name,phone_number]){
    element.addEventListener('input', verify_fields);
}


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
