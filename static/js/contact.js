/**
 * contact.js — contact.html only.
 * Wires #contact-form to POST /api/contact (section 54, 56).
 */

(function () {
  "use strict";

  var form = document.getElementById("contact-form");
  if (!form) return;

  var nameInput = document.getElementById("contact-name");
  var emailInput = document.getElementById("contact-email");
  var subjectInput = document.getElementById("contact-subject");
  var messageInput = document.getElementById("contact-message");
  var submitBtn = document.getElementById("contact-submit-btn");
  var confirmation = document.getElementById("contact-confirmation");

  function setFieldError(input, hasError) {
    if (!input) return;
    var field = input.closest(".field");
    if (field) field.classList.toggle("has-error", !!hasError);
  }

  function isValidEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  function validate() {
    var valid = true;

    if (!nameInput || !nameInput.value.trim()) {
      setFieldError(nameInput, true);
      valid = false;
    } else {
      setFieldError(nameInput, false);
    }

    if (!emailInput || !isValidEmail(emailInput.value.trim())) {
      setFieldError(emailInput, true);
      valid = false;
    } else {
      setFieldError(emailInput, false);
    }

    if (!subjectInput || !subjectInput.value.trim()) {
      setFieldError(subjectInput, true);
      valid = false;
    } else {
      setFieldError(subjectInput, false);
    }

    if (!messageInput || !messageInput.value.trim()) {
      setFieldError(messageInput, true);
      valid = false;
    } else {
      setFieldError(messageInput, false);
    }

    return valid;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!validate()) return;

    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.classList.add("is-loading");
    }

    fetch("/api/contact", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: nameInput.value.trim(),
        email: emailInput.value.trim(),
        subject: subjectInput.value.trim(),
        message: messageInput.value.trim(),
      }),
    })
      .then(function (res) {
        if (!res.ok) throw new Error("Request failed");
        return res.json();
      })
      .then(function () {
        if (confirmation) confirmation.style.display = "block";
        form.reset();
        if (window.showToast) window.showToast("Message received.", "success");
      })
      .catch(function () {
        if (window.showToast) {
          window.showToast("Could not send your message. Please try again.", "error");
        }
      })
      .finally(function () {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.classList.remove("is-loading");
        }
      });
  });
})();
