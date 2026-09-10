/**
 * projects.js — projects.html only.
 * Renders saved projects (localStorage) into #projects-grid (section 46-47).
 */

(function () {
  "use strict";

  var grid = document.getElementById("projects-grid");
  var emptyState = document.getElementById("projects-empty-state");
  var template = document.getElementById("project-card-template");
  if (!grid || !template || !window.Storage) return;

  function fmtCurrency(amount, currency) {
    var n = Number(amount) || 0;
    var rounded = Math.round(n);
    var withCommas = rounded.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return (currency || "PKR") + " " + withCommas;
  }

  function titleCase(str) {
    if (!str) return "";
    return str.toString().replace(/_/g, " ").replace(/\b\w/g, function (c) {
      return c.toUpperCase();
    });
  }

  function fmtDate(iso) {
    if (!iso) return "";
    try {
      var d = new Date(iso);
      return d.toLocaleDateString(undefined, { year: "numeric", month: "short", day: "numeric" });
    } catch (e) {
      return "";
    }
  }

  function closeAllMenus() {
    document.querySelectorAll(".project-card-menu").forEach(function (m) {
      m.style.display = "none";
    });
    document.querySelectorAll(".project-card-menu-btn").forEach(function (b) {
      b.setAttribute("aria-expanded", "false");
    });
  }

  function render() {
    var projects = window.Storage.getProjects();
    grid.innerHTML = "";

    if (!projects.length) {
      if (emptyState) emptyState.style.display = "block";
      grid.style.display = "none";
      return;
    }

    if (emptyState) emptyState.style.display = "none";
    grid.style.display = "grid";

    // Most recently updated first.
    projects
      .slice()
      .sort(function (a, b) {
        return new Date(b.updated_at || 0) - new Date(a.updated_at || 0);
      })
      .forEach(function (project) {
        var frag = template.content.cloneNode(true);

        frag.querySelector(".project-card-room").textContent = titleCase(project.room_type);
        frag.querySelector(".project-card-name").textContent = project.name || "Untitled Project";
        frag.querySelector(".project-card-budget").textContent = fmtCurrency(project.budget, project.currency);
        frag.querySelector(".project-card-timeline").textContent = project.timeline || "—";

        var progress = Math.max(0, Math.min(100, project.progress || 0));
        var fillEl = frag.querySelector(".project-card-progress-fill");
        if (fillEl) fillEl.style.width = progress + "%";
        var labelEl = frag.querySelector(".project-card-progress-label");
        if (labelEl) labelEl.textContent = progress + "% complete";
        var updatedEl = frag.querySelector(".project-card-updated");
        if (updatedEl) updatedEl.textContent = fmtDate(project.updated_at);

        var openLink = frag.querySelector(".project-card-open-link");
        if (openLink) openLink.href = "/project?id=" + encodeURIComponent(project.id);

        var menuBtn = frag.querySelector(".project-card-menu-btn");
        var menu = frag.querySelector(".project-card-menu");
        if (menuBtn && menu) {
          menuBtn.addEventListener("click", function (e) {
            e.stopPropagation();
            var isOpen = menu.style.display === "block";
            closeAllMenus();
            menu.style.display = isOpen ? "none" : "block";
            menuBtn.setAttribute("aria-expanded", isOpen ? "false" : "true");
          });
        }

        var openBtn = frag.querySelector(".project-card-open-btn");
        if (openBtn) {
          openBtn.addEventListener("click", function () {
            window.location.href = "/project?id=" + encodeURIComponent(project.id);
          });
        }

        var renameBtn = frag.querySelector(".project-card-rename-btn");
        if (renameBtn) {
          renameBtn.addEventListener("click", function () {
            closeAllMenus();
            var newName = window.prompt("Rename project", project.name || "");
            if (newName && newName.trim() && newName.trim() !== project.name) {
              window.Storage.updateProject(project.id, { name: newName.trim() });
              if (window.showToast) window.showToast("Project updated", "success");
              render();
            }
          });
        }

        var deleteBtn = frag.querySelector(".project-card-delete-btn");
        if (deleteBtn) {
          deleteBtn.addEventListener("click", function () {
            closeAllMenus();
            var confirmed = window.confirm('Delete "' + (project.name || "this project") + '"? This cannot be undone.');
            if (confirmed) {
              window.Storage.deleteProject(project.id);
              if (window.showToast) window.showToast("Project deleted", "success");
              render();
            }
          });
        }

        grid.appendChild(frag);
      });
  }

  document.addEventListener("click", closeAllMenus);

  render();
})();
