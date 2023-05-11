/**
 * @fileoverview This file is to be used for the edit listing page.
 */

const title = document.getElementById('title');
const description = document.getElementById('description');
const price = document.getElementById('price');
const updateBTN = document.getElementById('update_button');
const previewBTN = document.getElementById('preview_button');
const deleteBTN = document.getElementById('delete_button');
const listing_id = window.location.href.substring(window.location.href.lastIndexOf('/') + 1);

const verify_fields = (event) => {
    const FLAG_TITLE = title.value.length == 0
    if (FLAG_TITLE){
        for (button of [updateBTN, deleteBTN,previewBTN]){
            button.classList.add('disabled');
        }
    }
    else {
        for (button of [updateBTN, deleteBTN,previewBTN]){
            button.classList.remove('disabled');
        }
    }
}

const update = () => {
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
    //TODO: update listing, currently creates new stuff.


updateBTN.addEventListener('click', update);

const list_delete = () => {
    //TODO delete listing
}

deleteBTN.addEventListener('click', list_delete);

const preview = () => {
    window.location.href = `/preview_listing/${listing_id}`;
}

previewBTN.addEventListener('click', preview);


for (element of [title,description,price]){
    element.addEventListener('input',verify_fields)
}