const messageBTNS = document.getElementsByClassName("messageBTNS");

Array.from(messageBTNS).forEach((button) => {
  button.addEventListener("click", () => {
    const messageID = button.name;
    window.location.href = `/view_message/${messageID}`;
  });
});
