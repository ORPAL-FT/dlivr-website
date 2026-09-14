/* Apply the saved preference before rendering. Default to the system theme. */
(function () {
  'use strict';
  var root = document.documentElement;
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
    var header = document.querySelector('.site-header');
    function measureHeader() {
      root.style.setProperty('--header-height', header.getBoundingClientRect().height + 'px');
    }
    measureHeader();
    if ('ResizeObserver' in window) new ResizeObserver(measureHeader).observe(header);
    else window.addEventListener('resize', measureHeader);
    var menu = document.querySelector('.mobile-menu');
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && menu.open) { menu.open = false; menu.querySelector('summary').focus(); }
    });
    document.addEventListener('click', function (event) {
      if (!menu.contains(event.target)) menu.open = false;
    });
  });
})();
