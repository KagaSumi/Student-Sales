/**
 * @fileoverview This file contains all the functions that are used in the create_listing.html file.
 * 
 */
const title = document.getElementById("title");
const description = document.getElementById("description");
const price = document.getElementById("price");
const images = document.getElementById("image");
const createListingBTN = document.getElementById("create_listing");
const cancelBTN = document.getElementById("cancel_listing");

async function send_request() {
  let payload = {
    title: title.value,
    description: description.value,
    price: price.value,
    images: []
  };

  if (images.files) {
    const readFilePromises = Array.from(images.files).map((img) => {
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onloadend = function () {
          const binaryData = reader.result
          let image = {
            pic: binaryData,
            filename: img.name,
            mimetype: img.type,
          };
          payload.images.push(image);
          resolve();
        };
        reader.readAsDataURL(img);;
      });
    });
    await Promise.all(readFilePromises);
  }

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
      if (status == 400 || status == 401) {
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
    createListingBTN.disabled = false;
  } else {
    createListingBTN.disabled = true;
  }
  
  const priceErrorMessage = document.getElementById("price-error-message");
  if (priceErrorMessage) {
    if (/^\d+(\.\d{1,2})?$/.test(price.value)) {
      priceErrorMessage.remove();
    }
  }
};

createListingBTN.addEventListener("click", send_request);

cancelBTN.addEventListener("click", () => {
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
