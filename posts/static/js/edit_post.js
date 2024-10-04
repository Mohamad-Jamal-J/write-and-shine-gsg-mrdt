// Get modal and elements
var modal = document.getElementById("editPostModal");
var openModalBtn = document.getElementById("openEditPostModal");
var closeModalSpan = modal.getElementsByClassName("edit-close")[0];

// Open the modal when the edit icon is clicked
openModalBtn.onclick = function(event) {
    event.preventDefault(); // Prevent default anchor behavior
    modal.style.display = "block"; // Show the modal
}

// Close the modal when the "x" is clicked
closeModalSpan.onclick = function() {
    modal.style.display = "none"; // Hide the modal
}

// Close the modal if the user clicks outside of the modal
window.onclick = function(event) {
    if (event.target === modal) {
        modal.style.display = "none"; // Hide the modal
    }
}
