document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const articles = document.querySelectorAll('article.card, article.featured');
  const categoryButtons = document.querySelectorAll('.categories button');

  searchInput?.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    articles.forEach(article => {
      const text = article.innerText.toLowerCase();
      article.style.display = text.includes(query) ? 'block' : 'none';
    });
  });

  categoryButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      categoryButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const category = btn.dataset.category;
      articles.forEach(article => {
        const match = category === 'all' || article.dataset.category === category;
        article.style.display = match ? 'block' : 'none';
      });
    });
  });

  // Shortcut for quick search
  document.addEventListener('keydown', (e) => {
    if (e.key === '/' && document.activeElement !== searchInput) {
      e.preventDefault();
      searchInput.focus();
    }
  });
});
