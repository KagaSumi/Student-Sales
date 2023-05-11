const title = document.getElementById("title");
const description = document.getElementById("description");
const price = document.getElementById("price");
const create_listingBTN = document.getElementById("create_listing");
const cancelButton = document.getElementById("cancel_listing");

function send_request() {
  const payload = { title: title.value, description: description.value, price: price.value};
  fetch("/create_listing", {
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
        window.location.href = '/create_listing';
      } 
      else {
        window.location.href = '/profile';
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

function check_inputs() {
  if (title.value && description.value && price.value) {
    create_listingBTN.disabled = false;
  } else {
    create_listingBTN.disabled = true;
  }
}

create_listingBTN.addEventListener("click", send_request);

cancelButton.addEventListener("click", function() {
  let inputFields = document.querySelectorAll("input");
  for (let i = 0; i < inputFields.length; i++) {
    inputFields[i].value = "";
  }
});

title.addEventListener("input", check_inputs);
description.addEventListener("input", check_inputs);
price.addEventListener("input", check_inputs);

check_inputs(); // check inputs on page load
