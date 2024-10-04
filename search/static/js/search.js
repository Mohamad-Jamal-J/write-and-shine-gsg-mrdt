const searchBar = document.getElementById('search-bar');

searchBar.addEventListener('input', function () {
    const searchTerm = searchBar.value.toLowerCase();
    const cards = document.querySelectorAll('.card');

    cards.forEach(card => {
        const tags = card.getAttribute('data-tags');

        if (tags.includes(searchTerm)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});
