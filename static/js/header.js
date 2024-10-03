document.addEventListener('DOMContentLoaded', function() {
    const userIcon = document.querySelector('.dropdown a');
    const dropdown = document.querySelector('.dropdown');

    userIcon.addEventListener('click', function(event) {
        event.preventDefault();
        dropdown.classList.toggle('show');  // Toggle the 'show' class to display the dropdown
    });

    // Close dropdown if clicking outside
    window.addEventListener('click', function(event) {
        if (!event.target.matches('.user-icon')) {
            const dropdowns = document.querySelectorAll('.dropdown-content');
            dropdowns.forEach(function(dropdownContent) {
                dropdownContent.parentElement.classList.remove('show');
            });
        }
    });
});