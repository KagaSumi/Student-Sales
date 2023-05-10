const title = document.getElementById("title");
const description = document.getElementById("description");
const price = document.getElementById("price");
const images = document.getElementById("image");
const create_listingBTN = document.getElementById("create_listing");

async function send_request() {
  let payload = {
    title: title.value,
    description: description.value,
    price: price.value,
    images: [],
  };

  if (images.files) {
    // Wrap reading of each file in a Promise
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
          console.log(image.pic)
          resolve();
        };
        reader.readAsDataURL(img);;
      });
    });

    // Wait for all files to be read
    await Promise.all(readFilePromises);
  }

  // Now, the images are read, and you can send the fetch request
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
      if (status == 200) {
        window.location.href = "/profile";
      }
    })
    .catch((error) => {
      console.log(error);
    });
}

create_listingBTN.addEventListener("click", send_request);
