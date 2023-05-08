const title = document.getElementById("title");
const description = document.getElementById("description");
const price = document.getElementById("price");
const create_listingBTN = document.getElementById("create_listing");

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


create_listingBTN.addEventListener("click", send_request);
