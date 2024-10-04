document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', function() {
        this.classList.toggle('liked');
    });
});