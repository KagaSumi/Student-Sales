const testBTN = document.getElementById("test_button");

function send_request()
{
console.log("Button Pressed")
fetch("/test_endpoint", {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({test: 'ok'})
  })
  .then(response => response.json())
  .then(data => console.log(data))
  .then(()=>{ window.location.href = "/login" })
  .catch(error => console.error(error));
}

testBTN.addEventListener('click',send_request);

