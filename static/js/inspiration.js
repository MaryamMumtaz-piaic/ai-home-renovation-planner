/**
 * inspiration.js — inspiration.html only.
 * Same progressive-enhancement pattern as materials.js: instant client-side
 * search over the server-rendered inspiration grid (section 63, 49).
 */

(function () {
  "use strict";

  var searchInput = document.getElementById("inspiration-search-input");
  var grid = document.getElementById("inspiration-grid");
  var searchForm = document.getElementById("inspiration-search-form");
  if (!searchInput || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll(".inspiration-card"));
  if (!cards.length) return;

  if (searchForm) {
    searchForm.addEventListener("submit", function (e) {
      e.preventDefault();
    });
  }

  var debounceTimer = null;

  function filterCards(query) {
    var q = query.trim().toLowerCase();
    cards.forEach(function (card) {
      var text = card.textContent.toLowerCase();
      var matches = !q || text.indexOf(q) !== -1;
      card.style.display = matches ? "" : "none";
    });
  }

  function syncUrl(query) {
    var url = new URL(window.location.href);
    if (query) {
      url.searchParams.set("q", query);
    } else {
      url.searchParams.delete("q");
    }
    window.history.replaceState({}, "", url.toString());
  }

  searchInput.addEventListener("input", function () {
    var query = searchInput.value;
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(function () {
      filterCards(query);
      syncUrl(query);
    }, 150);
  });
})();
