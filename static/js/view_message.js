const sendBTN = document.getElementById("sendBTN");
const newMessage = document.getElementById("newMessage");

const message_id = window.location.href.substring(
    window.location.href.lastIndexOf("/") + 1
  );

const send_request = () => {
    let payload = {
      message: newMessage.value
    };
    console.log(payload)
    fetch(`/update_message/${message_id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((json) => {
        let message = json.message;
        console.log(message)
        localStorage.setItem("message", message);
        window.location.href = `/view_message/${message_id}`;
      })
      .catch((error) => {
        console.error(error);
      });
  };

sendBTN.addEventListener("click", () => send_request());
