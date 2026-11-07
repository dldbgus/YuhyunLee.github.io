(() => {
  const menuButton = document.getElementById('menu-toggle');
  const menu = document.getElementById('mobile-menu');
  if (menuButton && menu) {
    const closeMenu = () => {
      menu.hidden = true;
      menuButton.setAttribute('aria-expanded', 'false');
      menuButton.setAttribute('aria-label', 'Open menu');
      document.body.classList.remove('menu-open');
    };
    menuButton.addEventListener('click', () => {
      const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
      menu.hidden = isOpen;
      menuButton.setAttribute('aria-expanded', String(!isOpen));
      menuButton.setAttribute('aria-label', isOpen ? 'Open menu' : 'Close menu');
      document.body.classList.toggle('menu-open', !isOpen);
    });
    menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
    window.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(); });
    window.addEventListener('resize', () => { if (window.innerWidth > 780) closeMenu(); });
  }
  const year = document.getElementById('copyright-year');
  if (year) year.textContent = String(new Date().getFullYear());
  // Keep the November 2026 conference mention accurate after the events.
  const conferenceLabel = document.getElementById('conference-label');
  if (conferenceLabel) {
    conferenceLabel.textContent = new Date() < new Date('2026-11-11T00:00:00-05:00')
      ? 'Upcoming conference presentations · 2026'
      : 'Selected conference presentations · 2026';
  }
  if ('IntersectionObserver' in window) {
    const navLinks = document.querySelectorAll('.desktop-nav a');
    const sections = document.querySelectorAll('main section[id]');
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        navLinks.forEach(a => a.classList.toggle('active', a.getAttribute('href') === `#${entry.target.id}`));
      });
    }, { rootMargin: '-25% 0px -60% 0px' });
    sections.forEach(section => observer.observe(section));
  }
})();
