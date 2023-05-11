const first_name = document.getElementById("first_name");
const last_name = document.getElementById("last_name");
const update_button = document.getElementById("update_button");
const delete_button = document.getElementById("delete_button");
const verify_fields = (event) =>{
    if (first_name.value.length == 0 || last_name.value.length == 0) {
        update_button.classList.add("disabled");
    }
    else{
        update_button.classList.remove("disabled");
    }
}

const update_request = () =>{
    let payload = { first_name: first_name.value, last_name: last_name.value };
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
for (element of [first_name,last_name]){
    element.addEventListener('input', verify_fields);
}