/**
 * planner.js — planner.html only.
 * Drives the 8-step renovation planner wizard (task.md sections 12-20, 73-76).
 */

(function () {
  "use strict";

  var form = document.getElementById("planner-form");
  if (!form) return;

  var TOTAL_STEPS = 8;
  var currentStep = 1;
  var maxCompletedStep = 1; // highest step the user has validly reached

  var stepper = document.getElementById("planner-stepper");
  var prevBtn = document.getElementById("planner-prev-btn");
  var nextBtn = document.getElementById("planner-next-btn");
  var plannerNav = document.getElementById("planner-nav");

  var stepPanels = Array.prototype.slice.call(
    document.querySelectorAll(".planner-step[data-step]")
  );

  /* ------------------------------------------------------------------ */
  /* Step navigation                                                      */
  /* ------------------------------------------------------------------ */

  function showStep(step) {
    currentStep = step;
    stepPanels.forEach(function (panel) {
      var isActive = Number(panel.getAttribute("data-step")) === step;
      if (isActive) {
        panel.setAttribute("data-active", "true");
      } else {
        panel.removeAttribute("data-active");
      }
    });

    if (stepper) {
      var stepEls = stepper.querySelectorAll(".stepper-step");
      stepEls.forEach(function (el) {
        var target = Number(el.getAttribute("data-step-target"));
        if (target === step) {
          el.setAttribute("data-state", "active");
        } else if (target < step || target <= maxCompletedStep) {
          el.setAttribute("data-state", "complete");
        } else {
          el.setAttribute("data-state", "upcoming");
        }
      });
    }

    if (plannerNav) {
      plannerNav.style.display = step === TOTAL_STEPS ? "none" : "flex";
    }
    if (prevBtn) prevBtn.style.display = step === 1 ? "none" : "inline-flex";
    if (nextBtn) {
      nextBtn.textContent = step === TOTAL_STEPS - 1 ? "Review" : "Continue";
    }

    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  function clearStepError() {
    var err = document.getElementById("planner-validation-error");
    if (err) {
      err.style.display = "none";
      err.textContent = "";
    }
  }

  function showStepError(message) {
    var err = document.getElementById("planner-validation-error");
    if (err) {
      err.textContent = message;
      err.style.display = "block";
    } else if (window.showToast) {
      window.showToast(message, "error");
    }
  }

  /* ------------------------------------------------------------------ */
  /* Per-step validation                                                  */
  /* ------------------------------------------------------------------ */

  function validateStep(step) {
    if (step === 1) {
      var roomChecked = form.querySelector('input[name="room_type"]:checked');
      if (!roomChecked) {
        showToastOrInline("Please select a room type.");
        return false;
      }
      return true;
    }
    if (step === 4) {
      var amount = document.getElementById("budget-max-amount");
      var val = amount ? parseFloat(amount.value) : NaN;
      if (!val || val <= 0) {
        showToastOrInline("Please enter a maximum budget greater than 0.");
        if (amount) amount.focus();
        return false;
      }
      return true;
    }
    return true;
  }

  function showToastOrInline(message) {
    if (window.showToast) window.showToast(message, "error");
    else window.alert(message);
  }

  /* ------------------------------------------------------------------ */
  /* Next / Prev / Stepper click                                          */
  /* ------------------------------------------------------------------ */

  if (nextBtn) {
    nextBtn.addEventListener("click", function () {
      if (!validateStep(currentStep)) return;
      if (currentStep >= TOTAL_STEPS - 1) {
        // Moving into Review (step 7): populate the summary.
        populateReview();
        maxCompletedStep = Math.max(maxCompletedStep, 7);
        showStep(7);
        return;
      }
      var next = currentStep + 1;
      maxCompletedStep = Math.max(maxCompletedStep, next);
      showStep(next);
    });
  }

  if (prevBtn) {
    prevBtn.addEventListener("click", function () {
      if (currentStep <= 1) return;
      showStep(currentStep - 1);
    });
  }

  if (stepper) {
    stepper.addEventListener("click", function (e) {
      var stepEl = e.target.closest(".stepper-step");
      if (!stepEl) return;
      var target = Number(stepEl.getAttribute("data-step-target"));
      if (!target || target === 8) return; // step 8 only reachable via Generate
      if (target <= maxCompletedStep || target <= currentStep) {
        showStep(target);
      }
    });
  }

  document.querySelectorAll(".review-edit-btn").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var target = Number(btn.getAttribute("data-edit-step"));
      if (target) showStep(target);
    });
  });

  /* ------------------------------------------------------------------ */
  /* Step 1: dynamic existing-furniture rows                              */
  /* ------------------------------------------------------------------ */

  var furnitureList = document.getElementById("existing-furniture-list");
  var addFurnitureBtn = document.getElementById("add-furniture-btn");
  var furnitureTemplate = document.getElementById("furniture-row-template");

  function addFurnitureRow(name, action) {
    if (!furnitureList || !furnitureTemplate) return;
    var frag = furnitureTemplate.content.cloneNode(true);
    var nameInput = frag.querySelector(".furniture-name-input");
    var actionSelect = frag.querySelector(".furniture-action-select");
    var removeBtn = frag.querySelector(".remove-furniture-btn");
    if (name && nameInput) nameInput.value = name;
    if (action && actionSelect) actionSelect.value = action;
    if (removeBtn) {
      removeBtn.addEventListener("click", function () {
        var row = removeBtn.closest(".furniture-row");
        if (row) row.remove();
      });
    }
    furnitureList.appendChild(frag);
  }

  if (addFurnitureBtn) {
    addFurnitureBtn.addEventListener("click", function () {
      addFurnitureRow("", "unsure");
    });
  }

  /* ------------------------------------------------------------------ */
  /* Step 3: custom style description show/hide                          */
  /* ------------------------------------------------------------------ */

  var styleCustomWrap = document.getElementById("style-custom-wrap");

  function syncStyleCustomVisibility() {
    if (!styleCustomWrap) return;
    var checked = form.querySelector('input[name="style"]:checked');
    var show = checked && checked.value === "custom";
    styleCustomWrap.style.display = show ? "block" : "none";
  }

  form.addEventListener("change", function (e) {
    if (e.target && e.target.name === "style") syncStyleCustomVisibility();
  });
  syncStyleCustomVisibility();

  /* ------------------------------------------------------------------ */
  /* Step 4: live budget allocation preview (cosmetic only)               */
  /* ------------------------------------------------------------------ */

  var budgetAmountInput = document.getElementById("budget-max-amount");
  var budgetCurrencySelect = document.getElementById("budget-currency-select");
  var budgetPreviewChart = document.getElementById("budget-preview-chart");
  var PREVIEW_ALLOCATION = [
    ["Materials", 0.35],
    ["Furniture", 0.25],
    ["Labor", 0.2],
    ["Lighting", 0.1],
    ["Decor", 0.05],
    ["Contingency", 0.05],
  ];

  function formatCurrency(amount, currency) {
    var n = Number(amount) || 0;
    var rounded = Math.round(n);
    var withCommas = rounded.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return (currency || "PKR") + " " + withCommas;
  }

  function updateBudgetPreview() {
    if (!budgetPreviewChart) return;
    var total = parseFloat(budgetAmountInput ? budgetAmountInput.value : "") || 0;
    var currency = budgetCurrencySelect ? budgetCurrencySelect.value : "PKR";
    var rows = budgetPreviewChart.querySelectorAll(".budget-bar-row");
    rows.forEach(function (row, i) {
      var entry = PREVIEW_ALLOCATION[i];
      if (!entry) return;
      var amountEl = row.querySelector(".budget-bar-amount");
      if (amountEl) {
        amountEl.textContent = total > 0 ? formatCurrency(total * entry[1], currency) : Math.round(entry[1] * 100) + "%";
      }
    });
  }

  if (budgetAmountInput) budgetAmountInput.addEventListener("input", updateBudgetPreview);
  if (budgetCurrencySelect) budgetCurrencySelect.addEventListener("change", updateBudgetPreview);

  /* ------------------------------------------------------------------ */
  /* Building the RenovationBrief payload                                 */
  /* ------------------------------------------------------------------ */

  function buildBrief() {
    var roomType = (form.querySelector('input[name="room_type"]:checked') || {}).value || "living_room";

    var dimUnknown = document.getElementById("dim-unknown");
    var unknown = !!(dimUnknown && dimUnknown.checked);
    var lengthVal = parseFloat(document.getElementById("dim-length").value);
    var widthVal = parseFloat(document.getElementById("dim-width").value);
    var heightVal = parseFloat(document.getElementById("dim-height").value);

    var existingFurniture = [];
    if (furnitureList) {
      furnitureList.querySelectorAll(".furniture-row").forEach(function (row) {
        var nameInput = row.querySelector(".furniture-name-input");
        var actionSelect = row.querySelector(".furniture-action-select");
        var name = nameInput ? nameInput.value.trim() : "";
        if (!name) return;
        existingFurniture.push({
          name: name,
          action: actionSelect ? actionSelect.value : "unsure",
          notes: null,
        });
      });
    }

    var goals = Array.prototype.slice
      .call(form.querySelectorAll('input[name="goals"]:checked'))
      .map(function (el) {
        return el.value;
      });

    var styleChecked = form.querySelector('input[name="style"]:checked');
    var styleVal = styleChecked ? styleChecked.value : "modern";
    var styleCustomDesc = document.getElementById("style-custom-description");

    var colorsWanted = Array.prototype.slice
      .call(form.querySelectorAll('input[name="colors_wanted"]:checked'))
      .map(function (el) {
        return el.value;
      });
    var colorsAvoided = Array.prototype.slice
      .call(form.querySelectorAll('input[name="colors_avoided"]:checked'))
      .map(function (el) {
        return el.value;
      });

    var budgetTierChecked = form.querySelector('input[name="budget_tier"]:checked');
    var budgetTier = budgetTierChecked ? budgetTierChecked.value : "moderate";

    var materialCategories = [
      "flooring",
      "wall_finish",
      "paint",
      "countertops",
      "cabinet_materials",
      "hardware",
      "lighting",
      "furniture_materials",
    ];
    var materials = materialCategories.map(function (cat) {
      var select = document.getElementById("material-pref-" + cat);
      return {
        category: cat,
        preference: select ? select.value : "budget_friendly",
        custom_notes: null,
      };
    });

    var targetDaysInput = document.getElementById("timeline-target-days");
    var targetDays = targetDaysInput && targetDaysInput.value ? parseInt(targetDaysInput.value, 10) : null;
    var flexibleInput = document.getElementById("timeline-flexible");
    var timelineNotes = document.getElementById("timeline-notes");

    var brief = {
      room_type: roomType,
      current_space: {
        dimensions: {
          length: unknown || isNaN(lengthVal) ? null : lengthVal,
          width: unknown || isNaN(widthVal) ? null : widthVal,
          height: unknown || isNaN(heightVal) ? null : heightVal,
          unit: document.getElementById("dim-unit").value || "ft",
          unknown: unknown,
        },
        current_condition: valOrNull("current-condition"),
        existing_furniture: existingFurniture,
        existing_flooring: valOrNull("existing-flooring"),
        existing_walls: valOrNull("existing-walls"),
        existing_lighting: valOrNull("existing-lighting"),
        windows_doors: valOrNull("windows-doors"),
        structural_constraints: valOrNull("structural-constraints"),
      },
      goals: goals,
      goal_description: valOrNull("goal-description"),
      style: {
        style: styleVal,
        custom_description: styleCustomDesc ? valOrNullEl(styleCustomDesc) : null,
      },
      colors: {
        colors_wanted: colorsWanted,
        colors_avoided: colorsAvoided,
        custom_notes: valOrNull("color-custom-notes"),
      },
      budget: {
        tier: budgetTier,
        currency: budgetCurrencySelect ? budgetCurrencySelect.value : "PKR",
        max_budget: parseFloat(budgetAmountInput ? budgetAmountInput.value : "0") || 0,
      },
      materials: materials,
      timeline: {
        target_days: targetDays,
        flexible: !!(flexibleInput && flexibleInput.checked),
        notes: timelineNotes ? valOrNullEl(timelineNotes) : null,
      },
    };

    return brief;
  }

  function valOrNull(id) {
    var el = document.getElementById(id);
    return valOrNullEl(el);
  }
  function valOrNullEl(el) {
    if (!el) return null;
    var v = el.value ? el.value.trim() : "";
    return v ? v : null;
  }

  /* ------------------------------------------------------------------ */
  /* Review step population                                               */
  /* ------------------------------------------------------------------ */

  var GOAL_LABELS = {
    modernize: "Modernize",
    brighten: "Make it brighter",
    increase_storage: "Increase storage",
    improve_functionality: "Improve functionality",
    feel_larger: "Make it feel larger",
    luxury_look: "Create a luxury look",
    reduce_maintenance: "Reduce maintenance",
    improve_lighting: "Improve lighting",
    improve_organization: "Improve organization",
    increase_comfort: "Increase comfort",
    prepare_for_resale: "Prepare for resale",
    complete_makeover: "Complete makeover",
    partial_renovation: "Partial renovation",
  };

  function titleCase(str) {
    if (!str) return "";
    return str
      .toString()
      .replace(/_/g, " ")
      .replace(/\b\w/g, function (c) {
        return c.toUpperCase();
      });
  }

  function setText(id, text) {
    var el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  function populateReview() {
    var brief = buildBrief();
    window.__plannerBrief = brief;

    setText("review-room-type", titleCase(brief.room_type));

    var dims = brief.current_space.dimensions;
    if (dims.unknown || (!dims.length && !dims.width)) {
      setText("review-dimensions", "Not specified");
    } else {
      var parts = [dims.length, dims.width];
      if (dims.height) parts.push(dims.height);
      setText(
        "review-dimensions",
        parts.filter(Boolean).join(" × ") + " " + dims.unit
      );
    }

    var currentSpaceBits = [];
    if (brief.current_space.current_condition) currentSpaceBits.push(brief.current_space.current_condition);
    if (brief.current_space.existing_flooring) currentSpaceBits.push("Flooring: " + brief.current_space.existing_flooring);
    if (brief.current_space.existing_walls) currentSpaceBits.push("Walls: " + brief.current_space.existing_walls);
    setText("review-current-space", currentSpaceBits.length ? currentSpaceBits.join(" · ") : "Not specified");

    var furnitureBits = brief.current_space.existing_furniture.map(function (f) {
      return f.name + " (" + titleCase(f.action) + ")";
    });
    setText("review-keep-furniture", furnitureBits.length ? furnitureBits.join(", ") : "None specified");

    var goalLabels = brief.goals.map(function (g) {
      return GOAL_LABELS[g] || titleCase(g);
    });
    setText("review-goals", goalLabels.length ? goalLabels.join(" + ") : "Not specified");

    var styleText = brief.style.style === "custom" && brief.style.custom_description
      ? brief.style.custom_description
      : titleCase(brief.style.style);
    setText("review-style", styleText);

    var colorBits = [];
    if (brief.colors.colors_wanted.length) colorBits.push("Want: " + brief.colors.colors_wanted.map(titleCase).join(", "));
    if (brief.colors.colors_avoided.length) colorBits.push("Avoid: " + brief.colors.colors_avoided.map(titleCase).join(", "));
    setText("review-colors", colorBits.length ? colorBits.join(" · ") : "No preference");

    setText(
      "review-budget",
      formatCurrency(brief.budget.max_budget, brief.budget.currency) + " (" + titleCase(brief.budget.tier) + ")"
    );

    var matBits = brief.materials
      .filter(function (m) {
        return m.preference !== "budget_friendly";
      })
      .map(function (m) {
        return titleCase(m.category) + ": " + titleCase(m.preference);
      });
    setText("review-materials", matBits.length ? matBits.join(", ") : "Default preferences");

    var timelineText = brief.timeline.target_days
      ? brief.timeline.target_days + " days" + (brief.timeline.flexible ? " (flexible)" : "")
      : brief.timeline.flexible
      ? "Flexible"
      : "Not specified";
    setText("review-timeline", timelineText);
  }

  /* ------------------------------------------------------------------ */
  /* Step 8: AI generation                                                */
  /* ------------------------------------------------------------------ */

  var LOADING_STEPS = ["space", "design", "materials", "budget", "shopping", "timeline", "execution", "review"];
  var loadingTimer = null;
  var loadingIndex = 0;

  function resetLoadingChecklist() {
    document.querySelectorAll(".loading-item[data-loading-step]").forEach(function (item, i) {
      item.setAttribute("data-state", i === 0 ? "active" : "pending");
    });
    loadingIndex = 0;
  }

  function advanceLoadingChecklist() {
    if (loadingIndex >= LOADING_STEPS.length - 1) return;
    var currentEl = document.querySelector('.loading-item[data-loading-step="' + LOADING_STEPS[loadingIndex] + '"]');
    if (currentEl) currentEl.setAttribute("data-state", "done");
    loadingIndex += 1;
    var nextEl = document.querySelector('.loading-item[data-loading-step="' + LOADING_STEPS[loadingIndex] + '"]');
    if (nextEl) nextEl.setAttribute("data-state", "active");
  }

  function finishLoadingChecklist() {
    LOADING_STEPS.forEach(function (id) {
      var el = document.querySelector('.loading-item[data-loading-step="' + id + '"]');
      if (el) el.setAttribute("data-state", "done");
    });
  }

  function startGeneration() {
    var loadingPanel = document.getElementById("ai-loading-panel");
    var errorPanel = document.getElementById("ai-generation-error");
    var readyPanel = document.getElementById("ai-plan-ready-panel");

    if (loadingPanel) loadingPanel.style.display = "block";
    if (errorPanel) errorPanel.style.display = "none";
    if (readyPanel) readyPanel.style.display = "none";

    resetLoadingChecklist();
    if (loadingTimer) clearInterval(loadingTimer);
    loadingTimer = setInterval(advanceLoadingChecklist, 900);

    var brief = window.__plannerBrief || buildBrief();

    fetch("/api/ai/create-plan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ brief: brief }),
    })
      .then(function (res) {
        if (!res.ok) {
          return res
            .json()
            .catch(function () {
              return {};
            })
            .then(function (body) {
              throw new Error(body.detail || "AI generation failed, please try again.");
            });
        }
        return res.json();
      })
      .then(function (plan) {
        clearInterval(loadingTimer);
        finishLoadingChecklist();

        try {
          window.sessionStorage.setItem("latest_renovation_plan", JSON.stringify(plan));
          window.sessionStorage.setItem("latest_renovation_brief", JSON.stringify(brief));
        } catch (e) {
          /* sessionStorage unavailable — plan still shown in the ready panel */
        }

        setTimeout(function () {
          if (loadingPanel) loadingPanel.style.display = "none";
          showPlanReady(plan);
        }, 400);
      })
      .catch(function (err) {
        clearInterval(loadingTimer);
        if (loadingPanel) loadingPanel.style.display = "none";
        if (errorPanel) {
          errorPanel.style.display = "block";
          var msgEl = document.getElementById("ai-generation-error-message");
          if (msgEl) {
            msgEl.textContent =
              err && err.message
                ? err.message
                : "Please try again — your answers have been kept.";
          }
        }
        if (window.showToast) window.showToast("Plan generation failed. Please try again.", "error");
      });
  }

  function showPlanReady(plan) {
    var readyPanel = document.getElementById("ai-plan-ready-panel");
    if (!readyPanel) return;
    readyPanel.style.display = "block";
    setText("result-concept-name", plan.concept_name || "");
    setText("result-budget", formatCurrency(plan.estimated_budget, plan.currency));
    setText("result-timeline", plan.estimated_timeline || "");
    setText("result-design-match", plan.design_match || "");
    setText("result-budget-risk", plan.budget_risk || "");
  }

  var retryBtn = document.getElementById("retry-generation-btn");
  if (retryBtn) {
    retryBtn.addEventListener("click", function () {
      startGeneration();
    });
  }

  var generateBtn = document.getElementById("generate-plan-btn");
  if (generateBtn) {
    generateBtn.addEventListener("click", function () {
      clearStepError();
      var brief = buildBrief();
      if (!brief.budget.max_budget || brief.budget.max_budget <= 0) {
        showStepError("Please set a maximum budget before generating your plan.");
        showStep(4);
        return;
      }
      window.__plannerBrief = brief;
      maxCompletedStep = Math.max(maxCompletedStep, 8);
      showStep(8);
      startGeneration();
    });
  }

  /* ------------------------------------------------------------------ */
  /* Ready-panel actions: save project / adapt plan                      */
  /* ------------------------------------------------------------------ */

  var saveFromPlannerBtn = document.getElementById("save-project-from-planner-btn");
  if (saveFromPlannerBtn) {
    saveFromPlannerBtn.addEventListener("click", function () {
      var planRaw = window.sessionStorage.getItem("latest_renovation_plan");
      var briefRaw = window.sessionStorage.getItem("latest_renovation_brief");
      if (!planRaw) {
        if (window.showToast) window.showToast("No plan available to save yet.", "error");
        return;
      }
      var plan = JSON.parse(planRaw);
      var brief = briefRaw ? JSON.parse(briefRaw) : window.__plannerBrief;
      window.saveCurrentPlanAsProject(brief, plan, null);
      if (window.showToast) window.showToast("Project saved", "success");
      window.location.href = "/projects";
    });
  }

  var adaptFromPlannerBtn = document.getElementById("adapt-plan-from-planner-btn");
  if (adaptFromPlannerBtn) {
    adaptFromPlannerBtn.addEventListener("click", function () {
      // Adaptation happens on the full plan workspace page.
      window.location.href = "/plan";
    });
  }

  /* ------------------------------------------------------------------ */
  /* Init                                                                 */
  /* ------------------------------------------------------------------ */

  addFurnitureRow("", "unsure");
  showStep(1);
})();
