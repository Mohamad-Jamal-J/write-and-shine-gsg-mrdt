
// Get modal element
var createPostModal = document.getElementById("createPostModal");

// Get the button that opens the create post modal
var openCreatePostModalBtn = document.getElementById("postModalBtn"); // Adjust this ID if necessary

// Get close button
var createPostCloseBtn = createPostModal.querySelector(".create-post-close");

// When the user clicks the button, open the modal
openCreatePostModalBtn.onclick = function(event) {
    event.preventDefault();
    createPostModal.style.display = "flex";
};

// When the user clicks on <span> (x), close the modal
createPostCloseBtn.onclick = function() {
    createPostModal.style.display = "none";
};

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == createPostModal) {
        createPostModal.style.display = "none";
    }
};
