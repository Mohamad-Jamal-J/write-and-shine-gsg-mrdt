// modal.js

// Edit Profile Modal
var editProfileModal = document.getElementById("editProfileModal");
var openEditProfileModalBtn = document.querySelector(".edit-icon"); // Update to match the button's class
var editProfileCloseBtn = editProfileModal.querySelector(".close");

// When the user clicks the button, open the modal
openEditProfileModalBtn.onclick = function() {
    editProfileModal.style.display = "flex";
};

// When the user clicks on <span> (x), close the modal
editProfileCloseBtn.onclick = function() {
    editProfileModal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target === editProfileModal) {
        editProfileModal.style.display = "none";
    }
};


