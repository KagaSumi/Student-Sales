const title = document.getElementById("title");
const description = document.getElementById("description");
const price = document.getElementById("price");
const images = document.getElementById("image");
const updateBTN = document.getElementById("update_button");
const previewBTN = document.getElementById("preview_button");
const deleteBTN = document.getElementById("delete_button");
const deleteImgBTN = document.querySelectorAll(".deleteImgBTN");

const listing_id = window.location.href.substring(
  window.location.href.lastIndexOf("/") + 1
);

const verify_fields = (event) => {
  FLAG_TITLE = title.value.length == 0;

  if (FLAG_TITLE) {
    for (const button of [updateBTN, deleteBTN, previewBTN]) {
      button.classList.add("disabled");
    }
  } else {
    for (const button of [updateBTN, deleteBTN, previewBTN]) {
      button.classList.remove("disabled");
    }
  }
};

async function updateListing () {
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
        reader.readAsDataURL(img);
        console.log(payload)
      });
    });
    await Promise.all(readFilePromises);
  }

  fetch(`/update_listing/${listing_id}`, {
    method: "PUT",
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
      window.location.href = `/edit_listing/${listing_id}`;
    })
    .catch((error) => {
      console.log(error);
    });
};

const deleteListing = () => {
  fetch(`/delete_listing/${listing_id}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      return Promise.all([response.json(), response.status]);
    })
    .then(([json, status]) => {
      let message = json.message;
      localStorage.setItem("message", message);
      if (status == 200) {
        window.location.href = "/profile";
      } else {
        window.location.href = `/edit_listing/${listing_id}`;
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

const deleteImg = async (image_id) => {
  try {
    const response = await fetch(`/image/${image_id}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    const message = data.message;
    console.log(message);
    localStorage.setItem("message", message);
    window.location.href = `/edit_listing/${listing_id}`;
  } catch (error) {
    console.log(error);
  }
};

const previewListing = () => {
  fetch(`/preview_listing/${listing_id}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => {
      if (response.ok) {
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
          return response.json().then((json) => [json, response.status]);
        }
        return [null, response.status];
      }
      throw new Error("Network response was not OK");
    })
    .then(([json, status]) => {
      let message = json ? json.message : `Previewing Listing!`;
      localStorage.setItem("message", message);
      if (status === 200) {
        window.location.href = `/preview_listing/${listing_id}`;
      } else {
        window.location.href = `/edit_listing/${listing_id}`;
      }
    })
    .catch((error) => {
      console.log(error);
    });
};

for (const element of [title, description, price]) {
  element.addEventListener("input", verify_fields);
}

deleteImgBTN.forEach((button) => {
  button.addEventListener("click", () => deleteImg(button.value));
});

updateBTN.addEventListener("click", () => updateListing());
previewBTN.addEventListener("click", () => previewListing());
deleteBTN.addEventListener("click", () => deleteListing());
