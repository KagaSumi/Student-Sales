/**
 * @fileoverview This file contains all the functions that are used in the create_listing.html file.
 * 
 */
const title = document.getElementById("title");
const description = document.getElementById("description");
const price = document.getElementById("price");
const create_listingBTN = document.getElementById("create_listing");
const cancelButton = document.getElementById("cancel_listing");

const send_request = () => {
  const payload = { title: title.value, description: description.value, price: price.value};
  fetch("/create_listing", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => Promise.all([response.json(), response.status]))
    .then(([json, status]) => {
      let message = json.message;
      localStorage.setItem("message", message);
      if (status == 400) {
        window.location.href = '/create_listing';
      } else {
        window.location.href = '/profile';
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

const check_inputs = () => {
  if (title.value && description.value && /^\d+(\.\d{1,2})?$/.test(price.value)) {
    create_listingBTN.disabled = false;
  } else {
    create_listingBTN.disabled = true;
  }
  
  const priceErrorMessage = document.getElementById("price-error-message");
  if (priceErrorMessage) {
    if (/^\d+(\.\d{1,2})?$/.test(price.value)) {
      priceErrorMessage.remove();
    }
  }
};

create_listingBTN.addEventListener("click", send_request);

cancelButton.addEventListener("click", () => {
  let inputFields = document.querySelectorAll("input");
  for (let i = 0; i < inputFields.length; i++) {
    inputFields[i].value = "";
  }
});

title.addEventListener("input", check_inputs);
description.addEventListener("input", check_inputs);
price.addEventListener("input", check_inputs);

price.addEventListener("keydown", (event) => {
  if (
    event.key === "Backspace" ||
    event.key === "Delete" ||
    event.key === "ArrowLeft" ||
    event.key === "ArrowRight" ||
    event.key === "Tab"
  ) {
    return;
  }

  const input = event.target.value + event.key;
  if (!/^\d+(\.\d{0,2})?$/.test(input)) {
    event.preventDefault();
  }
});

check_inputs();
