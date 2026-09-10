/**
 * materials.js — materials.html only.
 * Progressive enhancement: instant client-side search-as-you-type over the
 * already server-rendered grid, syncing ?q= via history.replaceState so the
 * URL stays shareable without a full page reload (section 63, 49).
 */

(function () {
  "use strict";

  var searchInput = document.getElementById("materials-search-input");
  var grid = document.getElementById("materials-grid");
  var searchForm = document.getElementById("materials-search-form");
  if (!searchInput || !grid) return;

  var cards = Array.prototype.slice.call(grid.querySelectorAll(".material-card"));
  if (!cards.length) return;

  if (searchForm) {
    searchForm.addEventListener("submit", function (e) {
      e.preventDefault();
    });
  }

  var debounceTimer = null;

  function filterCards(query) {
    var q = query.trim().toLowerCase();
    var visibleCount = 0;

    cards.forEach(function (card) {
      var text = card.textContent.toLowerCase();
      var matches = !q || text.indexOf(q) !== -1;
      card.style.display = matches ? "" : "none";
      if (matches) visibleCount += 1;
    });

    return visibleCount;
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
