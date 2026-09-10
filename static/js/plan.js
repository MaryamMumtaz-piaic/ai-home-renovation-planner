/**
 * plan.js — shared by plan.html and project.html (identical DOM contract).
 * Renders a RenovationPlan into the workspace, and wires save/export/share/
 * adapt/what-if/shopping/timeline/execution interactions (sections 31-45,
 * 63-69).
 */

(function () {
  "use strict";

  var planContent = document.getElementById("plan-content");
  var emptyState = document.getElementById("plan-empty-state");
  if (!planContent || !emptyState) return; // not on a plan-rendering page

  var urlParams = new URLSearchParams(window.location.search);
  var projectId = urlParams.get("id");

  var state = {
    plan: null,
    brief: null,
    projectId: projectId || null,
  };

  /* ------------------------------------------------------------------ */
  /* Load plan + brief                                                    */
  /* ------------------------------------------------------------------ */

  function loadState() {
    if (projectId) {
      var project = window.Storage ? window.Storage.getProject(projectId) : null;
      if (project && project.plan) {
        state.plan = project.plan;
        state.brief = project.brief || null;
        return true;
      }
      return false;
    }

    try {
      var planRaw = window.sessionStorage.getItem("latest_renovation_plan");
      var briefRaw = window.sessionStorage.getItem("latest_renovation_brief");
      if (!planRaw) return false;
      state.plan = JSON.parse(planRaw);
      state.brief = briefRaw ? JSON.parse(briefRaw) : null;
      return true;
    } catch (e) {
      return false;
    }
  }

  function persist() {
    if (state.projectId) {
      window.Storage.updateProject(state.projectId, { plan: state.plan, brief: state.brief });
    } else {
      try {
        window.sessionStorage.setItem("latest_renovation_plan", JSON.stringify(state.plan));
      } catch (e) {
        /* ignore */
      }
    }
  }

  /* ------------------------------------------------------------------ */
  /* Formatting helpers                                                   */
  /* ------------------------------------------------------------------ */

  function fmtCurrency(amount, currency) {
    var n = Number(amount) || 0;
    var rounded = Math.round(n);
    var withCommas = rounded.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return (currency || state.plan.currency || "PKR") + " " + withCommas;
  }

  function titleCase(str) {
    if (!str) return "";
    return str.toString().replace(/_/g, " ").replace(/\b\w/g, function (c) {
      return c.toUpperCase();
    });
  }

  function setText(id, text) {
    var el = document.getElementById(id);
    if (el) el.textContent = text != null && text !== "" ? text : "—";
  }

  function fillList(id, items, formatter) {
    var el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = "";
    (items || []).forEach(function (item) {
      var li = document.createElement("li");
      li.textContent = formatter ? formatter(item) : item;
      el.appendChild(li);
    });
    if (!items || !items.length) {
      var li2 = document.createElement("li");
      li2.className = "field-help";
      li2.textContent = "Nothing to show here.";
      el.appendChild(li2);
    }
  }

  var COLOR_HEX = {
    warm_neutrals: "#D9C7A8",
    cool_neutrals: "#C7CDD1",
    earth_tones: "#A9825A",
    white_and_beige: "#EFE7D6",
    black_and_white: "#2B2621",
    green: "#6E7350",
    blue: "#5C7A8A",
    terracotta: "#BE6A41",
    natural_wood: "#8A5A34",
  };

  function isCssColor(value) {
    if (!value) return false;
    var s = String(value).trim();
    return /^#([0-9a-f]{3}|[0-9a-f]{6})$/i.test(s) || /^(rgb|hsl)a?\(/i.test(s) || COLOR_HEX[s.toLowerCase().replace(/ /g, "_")];
  }

  function colorToCss(value) {
    var key = String(value).toLowerCase().replace(/ /g, "_");
    return COLOR_HEX[key] || value;
  }

  /* ------------------------------------------------------------------ */
  /* Render: summary bar + before/after                                   */
  /* ------------------------------------------------------------------ */

  function renderSummary() {
    var plan = state.plan;
    setText("plan-concept-name", plan.concept_name);
    setText("plan-design-summary", plan.design_summary);
    setText("plan-estimated-budget", fmtCurrency(plan.estimated_budget, plan.currency));
    setText("plan-estimated-timeline", plan.estimated_timeline);
    setText("plan-style", plan.style);
    setText("plan-design-match", plan.design_match);
    setText("plan-budget-risk", plan.budget_risk);
  }

  function renderBeforeAfter() {
    var brief = state.brief;
    var plan = state.plan;

    var beforeDescEl = document.getElementById("before-current-description");
    if (beforeDescEl) {
      if (brief && brief.current_space) {
        var cs = brief.current_space;
        var bits = [];
        if (cs.current_condition) bits.push(cs.current_condition);
        if (cs.existing_flooring) bits.push("Flooring: " + cs.existing_flooring);
        if (cs.existing_walls) bits.push("Walls: " + cs.existing_walls);
        if (cs.existing_lighting) bits.push("Lighting: " + cs.existing_lighting);
        beforeDescEl.textContent = bits.length
          ? bits.join(". ")
          : "No detailed description of the current space was provided.";
      } else {
        beforeDescEl.textContent = "Original space details aren't available for this plan.";
      }
    }

    var issuesEl = document.getElementById("before-existing-issues");
    if (issuesEl) {
      issuesEl.innerHTML = "";
      if (brief && brief.current_space && brief.current_space.structural_constraints) {
        var p = document.createElement("p");
        p.className = "field-help";
        p.style.marginTop = "0.75rem";
        p.textContent = "Constraints: " + brief.current_space.structural_constraints;
        issuesEl.appendChild(p);
      }
    }

    setText("after-target-description", plan.design_summary);
  }

  /* ------------------------------------------------------------------ */
  /* Render: design concept                                               */
  /* ------------------------------------------------------------------ */

  function renderDesignConcept() {
    var dc = state.plan.design_concept || {};
    var headingEl = document.getElementById("design-concept-name-heading");
    if (headingEl) headingEl.textContent = dc.concept_name || "Design Concept";
    setText("design-concept-summary", dc.design_summary);

    var paletteEl = document.getElementById("design-concept-color-palette");
    if (paletteEl) {
      paletteEl.innerHTML = "";
      (dc.color_palette || []).forEach(function (color) {
        var chip = document.createElement("span");
        chip.className = "swatch-chip";
        if (isCssColor(color)) {
          var dot = document.createElement("span");
          dot.className = "swatch-dot";
          dot.style.background = colorToCss(color);
          chip.appendChild(dot);
          chip.appendChild(document.createTextNode(" " + color));
        } else {
          chip.textContent = color;
        }
        paletteEl.appendChild(chip);
      });
    }

    fillList("design-concept-materials", dc.materials);
    fillList("design-concept-furniture-direction", dc.furniture_direction);
    fillList("design-concept-lighting-direction", dc.lighting_direction);
    fillList("design-concept-decor-direction", dc.decor_direction);
    fillList("design-concept-priorities", dc.design_priorities);
  }

  /* ------------------------------------------------------------------ */
  /* Render: space plan                                                   */
  /* ------------------------------------------------------------------ */

  function renderSpacePlan() {
    var sp = state.plan.space_plan || {};
    setText("space-plan-dimensions-summary", sp.dimensions_summary);

    var zonesEl = document.getElementById("space-plan-zones");
    if (zonesEl) {
      zonesEl.innerHTML = "";
      (sp.zones || []).forEach(function (zone) {
        var card = document.createElement("div");
        var title = document.createElement("div");
        title.style.fontWeight = "700";
        title.textContent = zone.name;
        var purpose = document.createElement("div");
        purpose.className = "field-help";
        purpose.textContent = zone.purpose + (zone.notes ? " — " + zone.notes : "");
        card.appendChild(title);
        card.appendChild(purpose);
        zonesEl.appendChild(card);
      });
      if (!(sp.zones || []).length) {
        zonesEl.innerHTML = '<div class="field-help">No zones defined.</div>';
      }
    }

    fillList("space-plan-furniture-strategy", sp.furniture_strategy);
    fillList("space-plan-storage-strategy", sp.storage_strategy);
    setText("space-plan-movement-flow", sp.movement_flow);
    fillList("space-plan-lighting-zones", sp.lighting_zones);
    setText("space-plan-note", sp.planning_note);
  }

  /* ------------------------------------------------------------------ */
  /* Render: budget dashboard + scenarios                                  */
  /* ------------------------------------------------------------------ */

  function renderBudget() {
    var b = state.plan.budget || {};
    setText("budget-total-estimate", fmtCurrency(b.total_estimate, b.currency));

    var used = (b.categories || []).reduce(function (sum, c) {
      return sum + (c.amount || 0);
    }, 0);
    setText("budget-used", fmtCurrency(used, b.currency));
    setText("budget-remaining", fmtCurrency(Math.max((b.total_estimate || 0) - used, 0), b.currency));
    setText("budget-contingency", fmtCurrency(b.contingency, b.currency));

    var riskBadge = document.getElementById("budget-risk-badge");
    if (riskBadge) {
      riskBadge.textContent = b.budget_risk || "—";
      riskBadge.className = "stat-value badge badge-risk-" + String(b.budget_risk || "medium").toLowerCase();
    }

    var chart = document.getElementById("budget-chart");
    if (chart) {
      chart.innerHTML = "";
      (b.categories || []).forEach(function (cat) {
        var row = document.createElement("div");
        row.className = "budget-bar-row";

        var name = document.createElement("div");
        name.className = "budget-bar-name";
        name.textContent = cat.name;

        var track = document.createElement("div");
        track.className = "budget-bar-track";
        var fill = document.createElement("div");
        fill.className = "budget-bar-fill";
        fill.setAttribute("data-category", String(cat.name || "").toLowerCase());
        fill.style.width = Math.max(0, Math.min(100, cat.percentage || 0)) + "%";
        track.appendChild(fill);

        var amount = document.createElement("div");
        amount.className = "budget-bar-amount";
        amount.textContent = fmtCurrency(cat.amount, b.currency) + " (" + Math.round(cat.percentage || 0) + "%)";

        row.appendChild(name);
        row.appendChild(track);
        row.appendChild(amount);
        chart.appendChild(row);
      });
    }

    fillList("budget-savings-opportunities", b.savings_opportunities);
    fillList("budget-assumptions", b.assumptions);
    setText("budget-disclaimer", b.disclaimer);
  }

  function renderScenarios(containerId, scenarios) {
    var grid = document.getElementById(containerId);
    if (!grid) return;
    grid.innerHTML = "";
    (scenarios || []).forEach(function (s) {
      var card = document.createElement("div");
      card.className = "scenario-card";
      card.setAttribute("data-tier", s.tier || "");

      var label = document.createElement("div");
      label.className = "scenario-label";
      label.textContent = s.label || titleCase(s.tier);

      var total = document.createElement("div");
      total.className = "scenario-total";
      total.textContent = fmtCurrency(s.estimated_total, state.plan.currency);

      var desc = document.createElement("p");
      desc.className = "field-help";
      desc.textContent = s.description || "";

      var changes = document.createElement("ul");
      changes.style.marginTop = "0.75rem";
      changes.style.display = "flex";
      changes.style.flexDirection = "column";
      changes.style.gap = "0.3rem";
      (s.changes || []).forEach(function (c) {
        var li = document.createElement("li");
        li.className = "field-help";
        li.textContent = "• " + c;
        changes.appendChild(li);
      });

      card.appendChild(label);
      card.appendChild(total);
      card.appendChild(desc);
      card.appendChild(changes);
      grid.appendChild(card);
    });
    if (!(scenarios || []).length) {
      grid.innerHTML = '<div class="field-help">No scenarios available.</div>';
    }
  }

  /* ------------------------------------------------------------------ */
  /* Render: materials                                                    */
  /* ------------------------------------------------------------------ */

  function renderMaterials() {
    var mp = state.plan.materials || {};

    var recList = document.getElementById("material-recommendations-list");
    if (recList) {
      recList.innerHTML = "";
      (mp.recommendations || []).forEach(function (rec) {
        var card = document.createElement("div");
        card.className = "card";

        var badge = document.createElement("div");
        badge.className = "badge badge-neutral";
        badge.textContent = rec.category;

        var name = document.createElement("div");
        name.style.fontFamily = "var(--font-display)";
        name.style.fontSize = "var(--fs-md)";
        name.style.marginTop = ".6rem";
        name.textContent = rec.material_name;

        var why = document.createElement("p");
        why.className = "option-desc";
        why.style.marginTop = ".5rem";
        why.textContent = rec.why;

        var badges = document.createElement("div");
        badges.style.display = "flex";
        badges.style.gap = ".5rem";
        badges.style.marginTop = "1rem";
        badges.style.flexWrap = "wrap";
        badges.innerHTML =
          '<span class="badge badge-cost-' + String(rec.cost_level).toLowerCase() + '">' + rec.cost_level + ' cost</span>' +
          '<span class="badge badge-risk-' + String(rec.maintenance).toLowerCase() + '">' + rec.maintenance + ' maintenance</span>';

        card.appendChild(badge);
        card.appendChild(name);
        card.appendChild(why);
        card.appendChild(badges);

        if (rec.alternative) {
          var alt = document.createElement("p");
          alt.className = "field-help";
          alt.style.marginTop = ".75rem";
          alt.textContent = "Alternative: " + rec.alternative + (rec.trade_off ? " — " + rec.trade_off : "");
          card.appendChild(alt);
        }

        recList.appendChild(card);
      });
    }

    var compList = document.getElementById("material-comparisons-list");
    if (compList) {
      compList.innerHTML = "";
      (mp.comparisons || []).forEach(function (comp) {
        var wrap = document.createElement("div");
        wrap.className = "card";

        var heading = document.createElement("h4");
        heading.textContent = comp.category;
        wrap.appendChild(heading);

        var grid = document.createElement("div");
        grid.style.display = "grid";
        grid.style.gridTemplateColumns = "repeat(auto-fit,minmax(200px,1fr))";
        grid.style.gap = "1rem";
        grid.style.marginTop = "1rem";

        (comp.options || []).forEach(function (opt) {
          var optCard = document.createElement("div");
          optCard.className = "card card-muted";

          var optName = document.createElement("div");
          optName.style.fontWeight = "700";
          optName.textContent = opt.name;

          var meta = document.createElement("div");
          meta.className = "check-row-meta";
          meta.style.marginTop = ".5rem";
          var costSpan = document.createElement("span");
          costSpan.textContent = "Cost: " + opt.cost;
          var maintSpan = document.createElement("span");
          maintSpan.textContent = "Maintenance: " + opt.maintenance;
          meta.appendChild(costSpan);
          meta.appendChild(maintSpan);

          var styleFit = document.createElement("div");
          styleFit.className = "field-help";
          styleFit.style.marginTop = ".4rem";
          styleFit.textContent = "Style fit: " + opt.style_fit;

          optCard.appendChild(optName);
          optCard.appendChild(meta);
          optCard.appendChild(styleFit);

          if (opt.notes) {
            var notes = document.createElement("div");
            notes.className = "field-help";
            notes.style.marginTop = ".4rem";
            notes.textContent = opt.notes;
            optCard.appendChild(notes);
          }

          grid.appendChild(optCard);
        });

        wrap.appendChild(grid);

        var rec = document.createElement("p");
        rec.className = "field-help";
        rec.style.marginTop = "1rem";
        rec.textContent = "AI Recommendation: " + comp.ai_recommendation;
        wrap.appendChild(rec);

        compList.appendChild(wrap);
      });
    }
  }

  /* ------------------------------------------------------------------ */
  /* Render: shopping list                                                */
  /* ------------------------------------------------------------------ */

  var shoppingCategoryFilter = document.getElementById("shopping-filter-category");
  var shoppingPriorityFilter = document.getElementById("shopping-filter-priority");
  var shoppingShowOptional = document.getElementById("shopping-show-optional");

  function populateShoppingCategoryFilter() {
    if (!shoppingCategoryFilter) return;
    var items = (state.plan.shopping_list && state.plan.shopping_list.items) || [];
    var categories = Array.from(new Set(items.map(function (i) { return i.category; }))).sort();
    var current = shoppingCategoryFilter.value || "all";
    shoppingCategoryFilter.innerHTML = '<option value="all">All categories</option>';
    categories.forEach(function (cat) {
      var opt = document.createElement("option");
      opt.value = cat;
      opt.textContent = cat;
      shoppingCategoryFilter.appendChild(opt);
    });
    shoppingCategoryFilter.value = categories.includes(current) ? current : "all";
  }

  function renderShoppingList() {
    var listEl = document.getElementById("shopping-list");
    var template = document.getElementById("shopping-item-template");
    if (!listEl || !template) return;

    var items = (state.plan.shopping_list && state.plan.shopping_list.items) || [];
    var catFilter = shoppingCategoryFilter ? shoppingCategoryFilter.value : "all";
    var prioFilter = shoppingPriorityFilter ? shoppingPriorityFilter.value : "all";
    var showOptional = shoppingShowOptional ? shoppingShowOptional.checked : true;

    listEl.innerHTML = "";

    var filtered = items.filter(function (item) {
      if (catFilter !== "all" && item.category !== catFilter) return false;
      if (prioFilter !== "all" && item.priority !== prioFilter) return false;
      if (!showOptional && item.priority === "optional") return false;
      return true;
    });

    if (!filtered.length) {
      listEl.innerHTML = '<div class="field-help">No shopping items match these filters.</div>';
      return;
    }

    filtered.forEach(function (item) {
      var frag = template.content.cloneNode(true);
      var row = frag.querySelector(".shopping-item-row");
      var checkbox = frag.querySelector(".shopping-item-checkbox");
      var nameEl = frag.querySelector(".shopping-item-name");
      var qtyEl = frag.querySelector(".shopping-item-quantity");
      var catEl = frag.querySelector(".shopping-item-category");
      var prioEl = frag.querySelector(".shopping-item-priority");
      var costEl = frag.querySelector(".shopping-item-cost");
      var notesEl = frag.querySelector(".shopping-item-notes");

      checkbox.checked = !!item.checked;
      if (row && item.checked) row.classList.add("is-checked");
      nameEl.textContent = item.name;
      qtyEl.textContent = item.quantity;
      catEl.textContent = item.category;
      prioEl.textContent = titleCase(item.priority);
      prioEl.classList.add("badge-priority-" + item.priority);
      costEl.textContent = fmtCurrency(item.estimated_cost, state.plan.currency);
      notesEl.textContent = [item.alternative ? "Alt: " + item.alternative : "", item.notes || ""].filter(Boolean).join(" — ");

      checkbox.addEventListener("change", function () {
        item.checked = checkbox.checked;
        if (row) row.classList.toggle("is-checked", checkbox.checked);
        persist();
        if (checkbox.checked && window.showToast) window.showToast("Shopping item completed", "success");
      });

      listEl.appendChild(frag);
    });
  }

  [shoppingCategoryFilter, shoppingPriorityFilter, shoppingShowOptional].forEach(function (el) {
    if (el) el.addEventListener("change", renderShoppingList);
  });

  /* ------------------------------------------------------------------ */
  /* Render: timeline (phase-level status tracking)                       */
  /* ------------------------------------------------------------------ */

  var STATUS_CYCLE = ["not_started", "in_progress", "completed"];

  function renderTimeline() {
    var t = state.plan.timeline || {};
    setText("timeline-total-days", t.total_estimated_days);

    var container = document.getElementById("timeline-container");
    var phaseTemplate = document.getElementById("timeline-phase-template");
    var taskTemplate = document.getElementById("timeline-task-template");
    if (!container || !phaseTemplate || !taskTemplate) return;

    container.innerHTML = "";

    (t.phases || []).forEach(function (phase) {
      if (!phase.status) phase.status = "not_started";

      var frag = phaseTemplate.content.cloneNode(true);
      var phaseEl = frag.querySelector(".timeline-phase");
      phaseEl.setAttribute("data-status", phase.status);

      frag.querySelector(".timeline-phase-days").textContent = "Phase " + phase.phase_number + " · " + phase.duration_days;
      frag.querySelector(".timeline-phase-name").textContent = phase.name;
      frag.querySelector(".timeline-phase-description").textContent = phase.description || "";

      var tasksHost = frag.querySelector(".timeline-phase-tasks");
      var taskFrag = taskTemplate.content.cloneNode(true);
      taskFrag.querySelector(".timeline-task-name").textContent =
        phase.depends_on && phase.depends_on.length
          ? "Depends on: " + phase.depends_on.join(", ")
          : phase.can_run_in_parallel
          ? "Can run in parallel"
          : "Status";

      var btnGroupEl = taskFrag.querySelectorAll(".status-btn");
      btnGroupEl.forEach(function (btn) {
        var isCurrent = btn.getAttribute("data-status") === phase.status;
        btn.setAttribute("aria-pressed", isCurrent ? "true" : "false");
        btn.addEventListener("click", function () {
          phase.status = btn.getAttribute("data-status");
          phaseEl.setAttribute("data-status", phase.status);
          btnGroupEl.forEach(function (b) {
            b.setAttribute("aria-pressed", b === btn ? "true" : "false");
          });
          persist();
          if (window.showToast) window.showToast("Task completed", "success");
        });
      });

      tasksHost.appendChild(taskFrag);
      container.appendChild(frag);
    });

    fillList("timeline-critical-path", t.critical_path);
    setText("timeline-disclaimer", t.disclaimer);
  }

  /* ------------------------------------------------------------------ */
  /* Render: execution checklist                                          */
  /* ------------------------------------------------------------------ */

  var EXECUTION_STAGES = ["before_renovation", "during_renovation", "installation", "styling", "final_inspection"];

  function renderExecution() {
    var ep = state.plan.execution_plan || {};

    var prepList = document.getElementById("execution-preparation-checklist");
    if (prepList) {
      prepList.innerHTML = "";
      (ep.preparation_checklist || []).forEach(function (item) {
        var li = document.createElement("li");
        li.textContent = "☐ " + item;
        prepList.appendChild(li);
      });
    }

    var finalList = document.getElementById("execution-final-inspection-checklist");
    if (finalList) {
      finalList.innerHTML = "";
      (ep.final_inspection_checklist || []).forEach(function (item) {
        var li = document.createElement("li");
        li.textContent = "☐ " + item;
        finalList.appendChild(li);
      });
    }

    var taskTemplate = document.getElementById("execution-task-template");
    var stageGroups = {};
    EXECUTION_STAGES.forEach(function (stage) {
      var el = document.getElementById("execution-" + stage);
      if (el) {
        el.innerHTML = "";
        stageGroups[stage] = el;
      }
    });

    if (!taskTemplate) return;

    (ep.tasks || []).forEach(function (task) {
      var stage = task.stage || "during_renovation";
      var host = stageGroups[stage];
      if (!host) return;

      var frag = taskTemplate.content.cloneNode(true);
      var row = frag.querySelector(".execution-task-row");
      var checkbox = frag.querySelector(".execution-task-checkbox");
      var nameEl = frag.querySelector(".execution-task-name");
      var depsEl = frag.querySelector(".execution-task-dependencies");
      var matsEl = frag.querySelector(".execution-task-materials");
      var profEl = frag.querySelector(".execution-task-professional");

      checkbox.checked = task.status === "completed";
      if (row && checkbox.checked) row.classList.add("is-checked");
      nameEl.textContent = task.task;
      depsEl.textContent = task.dependencies && task.dependencies.length ? "Depends on: " + task.dependencies.join(", ") : "";
      matsEl.textContent = task.materials && task.materials.length ? "Materials: " + task.materials.join(", ") : "";

      if (task.requires_professional) {
        profEl.style.display = "inline-flex";
        if (task.recommended_skill_note) profEl.title = task.recommended_skill_note;
      }

      checkbox.addEventListener("change", function () {
        task.status = checkbox.checked ? "completed" : "not_started";
        if (row) row.classList.toggle("is-checked", checkbox.checked);
        persist();
        if (checkbox.checked && window.showToast) window.showToast("Task completed", "success");
      });

      host.appendChild(frag);
    });
  }

  /* ------------------------------------------------------------------ */
  /* Render: alternatives / recommendations / assumptions / warnings      */
  /* ------------------------------------------------------------------ */

  function renderListsSections() {
    renderScenarios("alternatives-list", state.plan.alternatives);
    fillList("ai-recommendations-list", state.plan.ai_recommendations);
    fillList("assumptions-list", state.plan.assumptions);
    fillList("warnings-list", state.plan.warnings);
  }

  /* ------------------------------------------------------------------ */
  /* Full render                                                          */
  /* ------------------------------------------------------------------ */

  function renderAll() {
    renderSummary();
    renderBeforeAfter();
    renderDesignConcept();
    renderSpacePlan();
    renderBudget();
    renderScenarios("budget-scenarios-grid", state.plan.alternatives);
    renderMaterials();
    populateShoppingCategoryFilter();
    renderShoppingList();
    renderTimeline();
    renderExecution();
    renderListsSections();
  }

  /* ------------------------------------------------------------------ */
  /* Top-bar actions                                                      */
  /* ------------------------------------------------------------------ */

  function wireTopBarActions() {
    var saveBtn = document.getElementById("save-project-btn");
    if (saveBtn) {
      saveBtn.addEventListener("click", function () {
        var saved = window.saveCurrentPlanAsProject(state.brief, state.plan, state.projectId);
        if (saved) {
          state.projectId = saved.id;
          if (window.showToast) window.showToast("Project saved", "success");
        }
      });
    }

    var downloadBtn = document.getElementById("download-pdf-btn");
    if (downloadBtn) {
      downloadBtn.addEventListener("click", function () {
        downloadBtn.disabled = true;
        fetch("/api/projects/export-pdf", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(state.plan),
        })
          .then(function (res) {
            if (!res.ok) throw new Error("Export failed");
            return res.blob();
          })
          .then(function (blob) {
            var url = URL.createObjectURL(blob);
            var a = document.createElement("a");
            a.href = url;
            a.download = "renovation-plan.pdf";
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            setTimeout(function () {
              URL.revokeObjectURL(url);
            }, 1000);
            if (window.showToast) window.showToast("Plan downloaded", "success");
          })
          .catch(function () {
            if (window.showToast) window.showToast("Could not generate the PDF. Please try again.", "error");
          })
          .finally(function () {
            downloadBtn.disabled = false;
          });
      });
    }

    var printBtn = document.getElementById("print-plan-btn");
    if (printBtn) {
      printBtn.addEventListener("click", function () {
        window.print();
      });
    }

    var shareBtn = document.getElementById("share-plan-btn");
    var copyLinkBtn = document.getElementById("copy-link-btn");
    if (shareBtn) {
      shareBtn.addEventListener("click", function () {
        var shareData = {
          title: state.plan.concept_name || "My Renovation Plan",
          text: state.plan.design_summary || "Check out my AI-generated renovation plan.",
          url: window.location.href,
        };
        if (navigator.share) {
          navigator.share(shareData).catch(function () {
            /* user cancelled — no-op */
          });
        } else if (navigator.clipboard) {
          navigator.clipboard
            .writeText(window.location.href)
            .then(function () {
              if (window.showToast) window.showToast("Link copied", "success");
            })
            .catch(function () {
              if (copyLinkBtn) copyLinkBtn.style.display = "inline-flex";
            });
        } else if (copyLinkBtn) {
          copyLinkBtn.style.display = "inline-flex";
        }
      });
    }
    if (copyLinkBtn) {
      copyLinkBtn.addEventListener("click", function () {
        if (navigator.clipboard) {
          navigator.clipboard.writeText(window.location.href).then(function () {
            if (window.showToast) window.showToast("Link copied", "success");
          });
        }
      });
    }
  }

  /* ------------------------------------------------------------------ */
  /* Adapt plan                                                           */
  /* ------------------------------------------------------------------ */

  function wireAdaptPanel() {
    var resultEl = document.getElementById("adapt-plan-result");
    document.querySelectorAll(".adapt-btn[data-adaptation]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var option = btn.getAttribute("data-adaptation");
        document.querySelectorAll(".adapt-btn").forEach(function (b) {
          b.setAttribute("data-loading", b === btn ? "true" : b.getAttribute("data-loading") || "false");
        });
        btn.setAttribute("data-loading", "true");

        fetch("/api/ai/adapt-plan", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ plan: state.plan, option: option, notes: null }),
        })
          .then(function (res) {
            if (!res.ok) throw new Error("Adaptation failed");
            return res.json();
          })
          .then(function (updatedPlan) {
            state.plan = updatedPlan;
            persist();
            renderAll();
            if (resultEl) {
              resultEl.setAttribute("data-active", "true");
              resultEl.innerHTML =
                '<div class="eyebrow">Plan Updated</div><p style="margin-top:.5rem;">Your plan has been adapted: <strong>' +
                titleCase(option) +
                '</strong>. All sections below now reflect the change.</p>';
            }
            if (window.showToast) window.showToast("Plan adapted", "success");
          })
          .catch(function () {
            if (window.showToast) window.showToast("Could not adapt the plan. Please try again.", "error");
          })
          .finally(function () {
            btn.setAttribute("data-loading", "false");
          });
      });
    });
  }

  /* ------------------------------------------------------------------ */
  /* What-if mode                                                         */
  /* ------------------------------------------------------------------ */

  function wireWhatIfPanel() {
    var submitBtn = document.getElementById("whatif-submit-btn");
    var input = document.getElementById("whatif-input");
    var resultEl = document.getElementById("whatif-result");
    if (!submitBtn || !input) return;

    submitBtn.addEventListener("click", function () {
      var question = input.value.trim();
      if (!question) {
        if (window.showToast) window.showToast("Please enter a what-if question.", "error");
        return;
      }
      submitBtn.disabled = true;

      fetch("/api/ai/what-if", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan: state.plan, question: question }),
      })
        .then(function (res) {
          if (!res.ok) throw new Error("What-if calculation failed");
          return res.json();
        })
        .then(function (impact) {
          if (resultEl) resultEl.setAttribute("data-active", "true");
          setText("whatif-budget-impact", impact.budget_impact || impact.budget);
          setText("whatif-timeline-impact", impact.timeline_impact || impact.timeline);
          setText("whatif-design-impact", impact.design_impact || impact.design);
          setText("whatif-functionality-impact", impact.functionality_impact || impact.functionality);
          var recEl = document.getElementById("whatif-recommendation");
          if (recEl) recEl.textContent = impact.recommendation || "";
          if (window.showToast) window.showToast("Scenario calculated", "success");
        })
        .catch(function () {
          if (window.showToast) window.showToast("Could not calculate this scenario. Please try again.", "error");
        })
        .finally(function () {
          submitBtn.disabled = false;
        });
    });
  }

  /* ------------------------------------------------------------------ */
  /* Init                                                                 */
  /* ------------------------------------------------------------------ */

  var ok = loadState();
  if (!ok || !state.plan) {
    emptyState.style.display = "block";
    planContent.style.display = "none";
    return;
  }

  emptyState.style.display = "none";
  planContent.style.display = "block";

  renderAll();
  wireTopBarActions();
  wireAdaptPanel();
  wireWhatIfPanel();
})();
