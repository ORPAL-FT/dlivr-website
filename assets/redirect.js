/* Preserve bookmarked sections when moving the former pages into the home page. */
(function () {
  var target = document.body.dataset.target;
  var allowed = ['start', 'leistungen', 'kontakt', 'beratung', 'interim', 'autohandel', 'digitalisierung', 'team', 'projekte', 'mi-tool', 'ueber', 'impressum', 'datenschutz'];
  var hash = location.hash.slice(1);
  location.replace('index.html' + location.search + '#' + (allowed.includes(hash) ? hash : target));
})();
