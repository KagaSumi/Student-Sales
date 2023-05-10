const title = document.getElementById('title');
const description = document.getElementById('description');
const price = document.getElementById('price');
const updateBTN = document.getElementById('update_button');
const previewBTN = document.getElementById('preview_button');
const deleteBTN = document.getElementById('delete_button');
const listing_id = window.location.href.substring(currentUrl.lastIndexOf('/') + 1);
const verify_fields = (event) => {
    FLAG_TITLE = title.value.length == 0
    if (FLAG_TITLE){
        for (button of [updateBTN, deleteBTN,previewBTN]){
            button.classList.add('disabled');
        }
    }
    else {
        for (button of [updateBTN, deleteBTN,previewBTN]){
            button.classList.remove('disabled');
        }
    }
}

const update = () => {
    //TODO Finish update button functionality
}
const list_delete = () => {
    //TODO Finish delete button functionality
    return
}
const preview = () => {
    window.location.href = "/preview/" + id;
}

    for (element of [title,description,price]){
    element.addEventListener('input',verify_fields)
}