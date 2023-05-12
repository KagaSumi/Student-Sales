const alertSpan = document.getElementById('alertSpan')
const alertContainer = document.getElementById('Alert')
// const alertBTN = document.getElementById('closeBTN')

// alertBTN.addEventlistener('click',() => alertContainer.classList.add('hidden'));

// console.log(alertBTN)

function displayMessage(message){
    alertSpan.innerText = message;
    alertContainer.classList.remove('hidden')
}
const displayAnyMessages = () => {
    if (localStorage.getItem("message")){
        displayMessage(localStorage.getItem("message"));
        localStorage.clear();
    }
};
displayAnyMessages();