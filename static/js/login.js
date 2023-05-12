const email = document.getElementById('email');
const password = document.getElementById('password');
const loginBTN = document.getElementById('loginBTN');

async function hashedPassword(password) {
  const utf8 = new TextEncoder().encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', utf8);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray
    .map((bytes) => bytes.toString(16).padStart(2, '0'))
    .join('');
  return hashHex;
};
async function  send_request() {
  let hash_password = await hashedPassword(password.value);
  let payload = { email: email.value.toLowerCase(), password: hash_password };
  fetch('/login', {
    method: 'POST',
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
      if (status == 200) {
        window.location.href = '/profile';
      } else {
        window.location.href = '/login';
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

loginBTN.addEventListener('click', send_request);
