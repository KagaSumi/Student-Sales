const password = document.getElementById('password');
const confirm_password = document.getElementById('conf_password');
const submitBTN = document.getElementById('submit_button');
const pattern = /^[0-9]{3}-?[0-9]{3}-?[0-9]{4}$/;
const symbols = ['$','!','@','#','%','^','&','*','_','+','=','-','`','~'];
const password_error = document.getElementById('password_error');
const conf_password_error = document.getElementById('conf_password_error');
const cancelBTN = document.getElementById("cancel_listing");
const token = window.location.href.split('/').pop(); 
let request_url
if (!token.includes("change_password")){
  request_url = "/change_password/" + String(token)
}
else{
  request_url = "/change_password"

}
const verify_fields = (event) => {
    const FLAG_PASSWORD = password.value.length >= 4 && password.value === confirm_password.value;
    if (FLAG_PASSWORD) {
      submitBTN.classList.remove("disabled");
    }
    else{
      submitBTN.classList.add("disabled");
    }
  };


  const verify_password = (event) => {
    const password = document.getElementById('password');
    const password_error = document.getElementById('password_error');
    const hasSymbol = symbols.some((symbol) => password.value.includes(symbol));
  
    if (password.value.length < 4) {
      password_error.textContent = "Password is too short.";
    } else if (!hasSymbol) {
      password_error.textContent = "Password must contain a symbol.";
    } else {
      password_error.textContent = "";
      password_error.classList.add("hidden");
    }
  };
  
  const verify_confirm_password = (event) => {
    const confirm_password = document.getElementById('conf_password');
    const conf_password_error = document.getElementById('conf_password_error');
    const isValidpassword = confirm_password.value === password.value;
  
    if (!isValidpassword) {
      conf_password_error.textContent = "Passwords do not match.";
      conf_password_error.classList.remove("hidden");
    } else {
      conf_password_error.textContent = "";
      conf_password_error.classList.add("hidden");
    }
  };
  

function hashedPassword(input) {
  function rotateRight(n, x) {
    return (x >>> n) | (x << (32 - n));
  }

  function toHex(num) {
    let hex = num.toString(16);
    return hex.length === 1 ? "0" + hex : hex;
  }

  function utf8Encode(input) {
    input = input.replace(/\r\n/g, "\n");
    let utf8Text = "";

    for (let i = 0; i < input.length; i++) {
      const charCode = input.charCodeAt(i);

      if (charCode < 128) {
        utf8Text += String.fromCharCode(charCode);
      } else if (charCode < 2048) {
        utf8Text += String.fromCharCode((charCode >> 6) | 192);
        utf8Text += String.fromCharCode((charCode & 63) | 128);
      } else {
        utf8Text += String.fromCharCode((charCode >> 12) | 224);
        utf8Text += String.fromCharCode(((charCode >> 6) & 63) | 128);
        utf8Text += String.fromCharCode((charCode & 63) | 128);
      }
    }

    return utf8Text;
  }

  const blocks = [];
  const paddingBytes = 64;

  let message = utf8Encode(input);
  let messageLength = message.length;
  let paddedLength = messageLength + paddingBytes - ((messageLength + paddingBytes) % paddingBytes);

  for (let i = 0; i < paddedLength; i += paddingBytes) {
    blocks.push(message.slice(i, i + paddingBytes));
  }

  blocks.push("\x80".padEnd(paddingBytes - 1, "\x00") + String.fromCharCode(messageLength >> 29));
  blocks.push(String.fromCharCode((messageLength << 3) & 0xffffffff));

  const K = [
    0x428a2f98,
    0x71374491,
    0xb5c0fbcf,
    0xe9b5dba5,
    0x3956c25b,
    0x59f111f1,
    0x923f82a4,
    0xab1c5ed5,
    0xd807aa98,
    0x12835b01,
    0x243185be,
    0x550c7dc3,
    0x72be5d74,
    0x80deb1fe,
    0x9bdc06a7,
    0xc19bf174,
    0xe49b69c1,
    0xefbe4786,
    0x0fc19dc6,
    0x240ca1cc,
    0x2de92c6f,
    0x4a7484aa,
    0x5cb0a9dc,
    0x76f988da,
    0x983e5152,
    0xa831c66d,
    0xb00327c8,
    0xbf597fc7,
    0xc6e00bf3,
    0xd5a79147,
    0x06ca6351,
    0x14292967,
    0x27b70a85,
    0x2e1b2138,
    0x4d2c6dfc,
    0x53380d13,
    0x650a7354,
    0x766a0abb,
    0x81c2c92e,
    0x92722c85,
    0xa2bfe8a1,
    0xa81a664b,
    0xc24b8b70,
    0xc76c51a3,
    0xd192e819,
    0xd6990624,
    0xf40e3585,
    0x106aa070,
    0x19a4c116,
    0x1e376c08,
    0x2748774c,
    0x34b0bcb5,
    0x391c0cb3,
    0x4ed8aa4a,
    0x5b9cca4f,
    0x682e6ff3,
    0x748f82ee,
    0x78a5636f,
    0x84c87814,
    0x8cc70208,
    0x90befffa,
    0xa4506ceb,
    0xbef9a3f7,
    0xc67178f2,
  ];

  let H = [
    0x6a09e667,
    0xbb67ae85,
    0x3c6ef372,
    0xa54ff53a,
    0x510e527f,
    0x9b05688c,
    0x1f83d9ab,
    0x5be0cd19,
  ];

  for (let i = 0; i < blocks.length; i++) {
    const words = new Array(64);

    for (let t = 0; t < 16; t++) {
      words[t] = (
        (blocks[i].charCodeAt(t * 4) << 24) |
        (blocks[i].charCodeAt(t * 4 + 1) << 16) |
        (blocks[i].charCodeAt(t * 4 + 2) << 8) |
        (blocks[i].charCodeAt(t * 4 + 3))
      );
    }

    for (let t = 16; t < 64; t++) {
      const s0 = rotateRight(7, words[t - 15]);
      const s1 = rotateRight(18, words[t - 15]);
      const s2 = words[t - 15] >>> 3;
      const s3 = words[t - 15] >>> 10;
      const s4 = rotateRight(17, words[t - 2]);
      const s5 = rotateRight(19, words[t - 2]);
      const s6 = words[t - 2] >>> 10;
      const s7 = words[t - 2] >>> 17;

      words[t] = (s4 + words[t - 7] + s5 + words[t - 16]) & 0xffffffff;
    }

    let [a, b, c, d, e, f, g, h] = H;

    for (let t = 0; t < 64; t++) {
      const s0 = rotateRight(2, a);
      const s1 = rotateRight(13, e);
      const s2 = rotateRight(6, e);
      const s3 = rotateRight(11, f);
      const s4 = rotateRight(25, f);
      const ch = (e & f) ^ (~e & g);
      const maj = (a & b) ^ (a & c) ^ (b & c);
      const temp1 = (h + s4 + ch + K[t] + words[t]) & 0xffffffff;
      const temp2 = (s0 + maj) & 0xffffffff;

      h = g;
      g = f;
      f = e;
      e = (d + temp1) & 0xffffffff;
      d = c;
      c = b;
      b = a;
      a = (temp1 + temp2) & 0xffffffff;
    }

    H[0] = (H[0] + a) & 0xffffffff;
    H[1] = (H[1] + b) & 0xffffffff;
    H[2] = (H[2] + c) & 0xffffffff;
    H[3] = (H[3] + d) & 0xffffffff;
    H[4] = (H[4] + e) & 0xffffffff;
    H[5] = (H[5] + f) & 0xffffffff;
    H[6] = (H[6] + g) & 0xffffffff;
    H[7] = (H[7] + h) & 0xffffffff;
  }

  let hash = "";

  for (let i = 0; i < H.length; i++) {
    hash += toHex(H[i]);
  }

  return hash;
}

const Submit = async () => {
let hash_password = hashedPassword(password.value);

fetch(request_url, {
    method: "PUT",
    headers: {
    "Content-Type": "application/json"
    },
    body: JSON.stringify({
    password: hash_password
    })
})
    .then((response) => {
    return Promise.all([response.json(), response.status]);
    })
    .then(([json, status]) => {
    let message = json.message;
    localStorage.setItem("message", message);
    window.location.href = "/login";
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