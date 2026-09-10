/**
 * main.js — loaded on every page (base.html).
 *
 * Provides:
 *  - Navbar scroll shadow + mobile menu toggle
 *  - window.showToast(message, type) reusable toast system
 *  - window.Storage — localStorage helpers for saved projects (section 46)
 *  - window.saveCurrentPlanAsProject(brief, plan, existingId) — shared save-to-project logic
 *  - Contact form wiring is intentionally NOT here (see static/js/contact.js,
 *    referenced directly by contact.html's {% block scripts %}).
 */

(function () {
  "use strict";

  /* ------------------------------------------------------------------ */
  /* Navbar: scroll shadow + mobile menu                                  */
  /* ------------------------------------------------------------------ */

  var navbar = document.getElementById("navbar");
  if (navbar) {
    var onScroll = function () {
      if (window.scrollY > 10) {
        navbar.classList.add("scrolled");
      } else {
        navbar.classList.remove("scrolled");
      }
    };
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  var navToggle = document.getElementById("navbar-toggle");
  var mobileMenu = document.getElementById("mobile-menu");
  if (navToggle && mobileMenu && navbar) {
    navToggle.addEventListener("click", function () {
      var isOpen = navbar.getAttribute("data-menu-open") === "true";
      var next = !isOpen;
      navbar.setAttribute("data-menu-open", next ? "true" : "false");
      navToggle.setAttribute("aria-expanded", next ? "true" : "false");
      mobileMenu.classList.toggle("is-open", next);
    });

    // Close the mobile menu when a link inside it is clicked.
    mobileMenu.addEventListener("click", function (e) {
      if (e.target && e.target.closest("a")) {
        navbar.setAttribute("data-menu-open", "false");
        navToggle.setAttribute("aria-expanded", "false");
        mobileMenu.classList.remove("is-open");
      }
    });
  }

  /* ------------------------------------------------------------------ */
  /* Toast system                                                        */
  /* ------------------------------------------------------------------ */

  var TOAST_ICONS = {
    success:
      '<svg width="18" height="18" viewBox="0 0 20 20" fill="none"><path d="M4 10.5 8 14.5 16 6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    error:
      '<svg width="18" height="18" viewBox="0 0 20 20" fill="none"><path d="M10 6v5M10 14h.01" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.6"/></svg>',
    info:
      '<svg width="18" height="18" viewBox="0 0 20 20" fill="none"><path d="M10 9v5M10 6.5h.01" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><circle cx="10" cy="10" r="8" stroke="currentColor" stroke-width="1.6"/></svg>',
  };

  window.showToast = function showToast(message, type) {
    var container = document.getElementById("toast-container");
    if (!container) return;
    var variant = type === "error" || type === "info" ? type : "success";

    var toast = document.createElement("div");
    toast.className = "toast";
    toast.setAttribute("data-variant", variant);
    toast.setAttribute("role", "status");

    var icon = document.createElement("span");
    icon.className = "toast-icon";
    icon.innerHTML = TOAST_ICONS[variant] || TOAST_ICONS.success;

    var msg = document.createElement("span");
    msg.className = "toast-message";
    msg.textContent = message;

    var close = document.createElement("button");
    close.type = "button";
    close.className = "toast-close";
    close.setAttribute("aria-label", "Dismiss notification");
    close.innerHTML =
      '<svg width="14" height="14" viewBox="0 0 20 20" fill="none"><path d="m5 5 10 10M15 5 5 15" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>';

    toast.appendChild(icon);
    toast.appendChild(msg);
    toast.appendChild(close);
    container.appendChild(toast);

    var dismissTimer = setTimeout(dismiss, 3500);

    function dismiss() {
      if (toast.classList.contains("is-leaving")) return;
      clearTimeout(dismissTimer);
      toast.classList.add("is-leaving");
      setTimeout(function () {
        if (toast.parentNode) toast.parentNode.removeChild(toast);
      }, 220);
    }

    close.addEventListener("click", dismiss);
    toast.addEventListener("click", function (e) {
      if (e.target === close || close.contains(e.target)) return;
      dismiss();
    });
  };

  /* ------------------------------------------------------------------ */
  /* Storage: saved projects (localStorage, section 46-47)                */
  /* ------------------------------------------------------------------ */

  var PROJECTS_KEY = "renovation_projects";

  function readProjects() {
    try {
      var raw = window.localStorage.getItem(PROJECTS_KEY);
      var parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function writeProjects(list) {
    try {
      window.localStorage.setItem(PROJECTS_KEY, JSON.stringify(list));
      return true;
    } catch (e) {
      return false;
    }
  }

  function genId() {
    return (
      "proj_" +
      Date.now().toString(36) +
      "_" +
      Math.random().toString(36).slice(2, 9)
    );
  }

  window.Storage = {
    getProjects: function () {
      return readProjects();
    },
    getProject: function (id) {
      if (!id) return null;
      var list = readProjects();
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === id) return list[i];
      }
      return null;
    },
    saveProject: function (project) {
      var list = readProjects();
      if (!project.id) project.id = genId();
      var now = new Date().toISOString();
      if (!project.created_at) project.created_at = now;
      project.updated_at = now;
      list.push(project);
      writeProjects(list);
      return project;
    },
    updateProject: function (id, patch) {
      var list = readProjects();
      var found = null;
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === id) {
          list[i] = Object.assign({}, list[i], patch, {
            updated_at: new Date().toISOString(),
          });
          found = list[i];
          break;
        }
      }
      if (found) writeProjects(list);
      return found;
    },
    deleteProject: function (id) {
      var list = readProjects();
      var next = list.filter(function (p) {
        return p.id !== id;
      });
      var changed = next.length !== list.length;
      if (changed) writeProjects(next);
      return changed;
    },
  };

  /* ------------------------------------------------------------------ */
  /* Shared: build/save a SavedProject from a brief + plan                */
  /* Used by planner.js ("Save Project" from the ready panel) and         */
  /* plan.js ("Save Project" / "Save Changes" on the plan workspace).     */
  /* ------------------------------------------------------------------ */

  function fmtTimeline(plan) {
    return (plan && plan.estimated_timeline) || (plan && plan.timeline && plan.timeline.total_estimated_days) || "";
  }

  function computeProgress(plan) {
    if (!plan || !plan.execution_plan || !Array.isArray(plan.execution_plan.tasks)) return 0;
    var tasks = plan.execution_plan.tasks;
    if (!tasks.length) return 0;
    var done = tasks.filter(function (t) {
      return t.status === "completed";
    }).length;
    return Math.round((done / tasks.length) * 100);
  }

  window.saveCurrentPlanAsProject = function saveCurrentPlanAsProject(brief, plan, existingId) {
    if (!plan) return null;
    var name =
      (plan.concept_name && plan.concept_name.trim()) ||
      ((brief && brief.room_type) ? brief.room_type.replace(/_/g, " ") : "Renovation Project");

    var payload = {
      name: name,
      room_type: (brief && brief.room_type) || "",
      style: plan.style || (brief && brief.style && brief.style.style) || "",
      budget: plan.estimated_budget || (brief && brief.budget && brief.budget.max_budget) || 0,
      currency: plan.currency || (brief && brief.budget && brief.budget.currency) || "PKR",
      timeline: fmtTimeline(plan),
      progress: computeProgress(plan),
      brief: brief || null,
      plan: plan,
    };

    if (existingId) {
      var updated = window.Storage.updateProject(existingId, payload);
      if (updated) return updated;
      // Fall through to create if the id no longer exists.
    }

    payload.id = existingId || undefined;
    return window.Storage.saveProject(payload);
  };
})();
