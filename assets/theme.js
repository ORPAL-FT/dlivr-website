/* Apply the saved preference before rendering. Default to the system theme. */
(function () {
  'use strict';
  var root = document.documentElement;
  // Preserve former legal bookmarks on the home page.
  if ((location.pathname.endsWith('/') || location.pathname.endsWith('/index.html')) &&
      (location.hash === '#impressum' || location.hash === '#datenschutz')) {
    location.replace(location.hash.slice(1) + '.html');
    return;
  }
  var system = window.matchMedia('(prefers-color-scheme: dark)');
  var preference = null;
  try { preference = localStorage.getItem('dlivr-theme'); } catch (_) {}
  if (preference !== 'light' && preference !== 'dark') preference = null;
  function apply(theme) {
    root.dataset.theme = theme;
    var button = document.querySelector('.theme-toggle');
    var label = theme === 'dark' ? 'Hellmodus aktivieren' : 'Dunkelmodus aktivieren';
    if (button) { button.setAttribute('aria-label', label); button.title = label; }
    var meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = theme === 'dark' ? '#17191d' : '#f4f2ef';
  }
  apply(preference || (system.matches ? 'dark' : 'light'));
  system.addEventListener('change', function (event) {
    if (!preference) apply(event.matches ? 'dark' : 'light');
  });
  window.addEventListener('storage', function (event) {
    if (event.key !== 'dlivr-theme' && event.key !== null) return;
    preference = event.newValue === 'light' || event.newValue === 'dark' ? event.newValue : null;
    apply(preference || (system.matches ? 'dark' : 'light'));
  });
  document.addEventListener('DOMContentLoaded', function () {
    var button = document.querySelector('.theme-toggle');
    button.hidden = false;
    apply(root.dataset.theme);
    button.addEventListener('click', function () {
      preference = root.dataset.theme === 'dark' ? 'light' : 'dark';
      apply(preference);
      try { localStorage.setItem('dlivr-theme', preference); } catch (_) {}
    });
    var menu = document.querySelector('.mobile-menu');
    menu.addEventListener('click', function (event) {
      if (event.target.closest('a')) {
        menu.open = false;
        document.querySelector('main').focus({ preventScroll: true });
      }
    });
    var main = document.querySelector('main');
    var sections = ['start', 'leistungen', 'kontakt'].map(function (id) { return document.getElementById(id); }).filter(Boolean);
    var links = document.querySelectorAll('.site-header nav a');
    function updateNavigation() {
      if (!sections.length) return;
      var current = 'start';
      var edge = getComputedStyle(main).overflowY === 'visible' ? 80 : main.getBoundingClientRect().top + 80;
      sections.forEach(function (section) {
        if (section.getBoundingClientRect().top <= edge) current = section.id;
      });
      links.forEach(function (link) {
        if (link.hash === '#' + current) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    }
    main.addEventListener('scroll', updateNavigation, { passive: true });
    window.addEventListener('scroll', updateNavigation, { passive: true });
    window.addEventListener('resize', updateNavigation);
    updateNavigation();
    var motion = window.matchMedia('(prefers-reduced-motion: reduce)');
    var approach = document.querySelector('.approach-steps');
    var approachObserver;
    function replayApproach() {
      if (!approach || motion.matches || !('IntersectionObserver' in window)) return;
      if (approachObserver) approachObserver.disconnect();
      approach.classList.remove('motion-playing');
      approach.classList.add('motion-ready');
      // Commit the reset so a repeated Start click restarts the CSS animation.
      void approach.offsetWidth;
      approachObserver = new IntersectionObserver(function (entries) {
        if (entries.some(function (entry) { return entry.isIntersecting; })) {
          approach.classList.add('motion-playing');
          approachObserver.disconnect();
        }
      }, { threshold: 0.15 });
      approachObserver.observe(approach);
    }
    replayApproach();
    motion.addEventListener('change', function (event) {
      if (event.matches && approach) {
        if (approachObserver) approachObserver.disconnect();
        approach.classList.remove('motion-ready', 'motion-playing');
      }
    });
    // Move keyboard and reading focus along with in-page navigation.
    document.addEventListener('click', function (event) {
      var link = event.target.closest('a[href]');
      if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      var url = new URL(link.href);
      if (url.origin !== location.origin || url.pathname !== location.pathname || url.search !== location.search || !url.hash) return;
      var target = document.getElementById(decodeURIComponent(url.hash.slice(1)));
      if (!target) return;
      event.preventDefault();
      if (location.hash !== url.hash) history.pushState(null, '', url.hash);
      var focusTarget = target.querySelector('h1, h2, h3') || target;
      if (!focusTarget.hasAttribute('tabindex')) focusTarget.setAttribute('tabindex', '-1');
      focusTarget.classList.add('anchor-focus-target');
      focusTarget.classList.toggle('anchor-focus-pointer', event.detail !== 0);
      focusTarget.focus({ preventScroll: true });
      if (target.id === 'start') replayApproach();
      target.scrollIntoView({ block: 'start', behavior: motion.matches || event.detail === 0 ? 'instant' : 'smooth' });
    });
    document.addEventListener('focusin', function (event) {
      if (!menu.contains(event.target)) menu.open = false;
    });
    document.addEventListener('keydown' , function (event) {
      if (event.key === 'Escape' && menu.open) { menu.open = false; menu.querySelector('summary').focus(); }
    });
    document.addEventListener('click', function (event) {
      if (!menu.contains(event.target)) menu.open = false;
    });
  });
})();
