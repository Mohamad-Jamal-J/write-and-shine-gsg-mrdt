document.querySelectorAll('.read-more').forEach(function(readMoreLink) {
    readMoreLink.addEventListener('click', function(event) {
        event.preventDefault(); // Prevent the default link behavior
        
        // Find the associated full content paragraph
        const fullContent = this.previousElementSibling;
        
        // Toggle display of the full content
        if (fullContent.style.display === 'none' || fullContent.style.display === '') {
            fullContent.style.display = 'block';
            this.innerHTML = 'Read Less <i class="fas fa-arrow-up"></i>';
        } else {
            fullContent.style.display = 'none';
            this.innerHTML = 'Read More <i class="fas fa-arrow-right"></i>';
        }
    });
});
