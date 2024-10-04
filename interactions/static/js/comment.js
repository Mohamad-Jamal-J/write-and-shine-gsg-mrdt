// Toggle comments section
document.querySelectorAll('.comment-btn').forEach(button => {
    button.addEventListener('click', function() {
        const commentsSection = this.closest('.post-footer').querySelector('.comments-section');
        commentsSection.style.display = commentsSection.style.display === 'none' ? 'flex' : 'none';
    });
});

// Handle comment submission
function toggleComments(button) {
    // Find the closest comments section from the clicked button
    const commentsSection = button.closest('.post-footer').querySelector('.comments-section');
    
    // Toggle visibility
    if (commentsSection.style.display === 'none') {
        commentsSection.style.display = 'block';
    } else {
        commentsSection.style.display = 'none';
    }
}