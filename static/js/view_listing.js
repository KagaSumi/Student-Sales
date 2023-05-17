const messageBTN = document.getElementById("messageBTN");
const submitBTN = document.getElementById("submitBTN");
const cancelBTN = document.getElementById("cancelBTN");
const contact = document.querySelector(".contact");
const subject = document.getElementById("subject");
const message = document.getElementById("message");

const listing_id = window.location.href.substring(
  window.location.href.lastIndexOf("/") + 1
);

messageBTN.addEventListener("click", () => {
  if (contact.style.display === "none") {
    contact.style.display = "block";
  } else {
    contact.style.display = "none";
  }
});

cancelBTN.addEventListener("click", () => {
  subject.value = "";
  message.value = "";
  contact.style.display = "none";
});

const send_message = () => {
  let payload = {
    subject: subject.value,
    message: message.value,
    listing_id: listing_id,
  };
  fetch(`/create_message`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => response.json())
    .then((json) => {
      let message = json.message;
      localStorage.setItem("message", message);
      window.location.href = `/view_listing/${listing_id}`;
    })
    .catch((error) => {
      console.error(error);
    });
};

submitBTN.addEventListener("click", () => send_message());