(function () {
  const root = document.documentElement;
  const keys = {
    theme: "studentspot-theme",
    contrast: "studentspot-contrast",
    font: "studentspot-font",
  };

  function apply() {
    root.dataset.theme = localStorage.getItem(keys.theme) || "light";
    root.dataset.contrast = localStorage.getItem(keys.contrast) || "normal";
    root.dataset.font = localStorage.getItem(keys.font) || "normal";
    updateButtons();
  }

  function updateButtons() {
    document.querySelectorAll("[data-toggle-pref]").forEach((button) => {
      const pref = button.dataset.togglePref;
      const value = button.dataset.toggleValue;
      button.setAttribute("aria-pressed", String(localStorage.getItem(keys[pref]) === value));
    });
  }

  document.addEventListener("click", (event) => {
    const button = event.target.closest("[data-toggle-pref]");
    if (!button) return;
    const pref = button.dataset.togglePref;
    const value = button.dataset.toggleValue;
    const current = localStorage.getItem(keys[pref]);
    localStorage.setItem(keys[pref], current === value ? "normal" : value);
    apply();
  });

  function createLightbox() {
    const backdrop = document.createElement("div");
    backdrop.className = "lightbox-backdrop";
    backdrop.setAttribute("role", "dialog");
    backdrop.setAttribute("aria-modal", "true");
    backdrop.innerHTML = `
      <div class="lightbox-dialog">
        <button class="lightbox-close" type="button" aria-label="Close">×</button>
        <img src="" alt="">
      </div>
    `;
    document.body.appendChild(backdrop);
    const image = backdrop.querySelector("img");
    const close = backdrop.querySelector(".lightbox-close");

    function hide() {
      backdrop.classList.remove("is-open");
      image.setAttribute("src", "");
    }

    close.addEventListener("click", hide);
    backdrop.addEventListener("click", (event) => {
      if (event.target === backdrop) hide();
    });
    document.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && backdrop.classList.contains("is-open")) hide();
    });

    return {
      show(src, alt) {
        image.setAttribute("src", src);
        image.setAttribute("alt", alt || "");
        backdrop.classList.add("is-open");
        close.focus();
      },
    };
  }

  const lightbox = createLightbox();
  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-lightbox-src]");
    if (!trigger) return;
    lightbox.show(trigger.dataset.lightboxSrc, trigger.dataset.lightboxAlt);
  });

  function showWelcomePopup(force) {
    if (!document.body.classList.contains("app-guest")) return;
    const key = "studentspot-welcome-popup-seen";
    if (!force && localStorage.getItem(key) === "1") return;
    const backdrop = document.createElement("div");
    backdrop.className = "lightbox-backdrop is-open welcome-popup";
    backdrop.setAttribute("role", "dialog");
    backdrop.setAttribute("aria-modal", "true");
    backdrop.innerHTML = `
      <div class="lightbox-dialog">
        <button class="lightbox-close" type="button" aria-label="Close">×</button>
        <img src="/static/media/visuals/welcome-popup.png" alt="StudentSpot welcome">
      </div>
    `;
    document.body.appendChild(backdrop);
    const close = backdrop.querySelector(".lightbox-close");
    function hide() {
      localStorage.setItem(key, "1");
      backdrop.remove();
    }
    close.addEventListener("click", hide);
    backdrop.addEventListener("click", (event) => {
      if (event.target === backdrop) hide();
    });
    document.addEventListener("keydown", function onKeydown(event) {
      if (event.key !== "Escape") return;
      document.removeEventListener("keydown", onKeydown);
      hide();
    });
    close.focus();
  }

  document.addEventListener("click", (event) => {
    const trigger = event.target.closest("[data-show-welcome-popup]");
    if (!trigger) return;
    showWelcomePopup(true);
  });

  function setupBackToTop() {
    const button = document.querySelector("[data-back-to-top]");
    if (!button) return;
    function sync() {
      button.classList.toggle("is-visible", window.scrollY > 520);
    }
    button.addEventListener("click", () => {
      const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      window.scrollTo({ top: 0, behavior: reducedMotion ? "auto" : "smooth" });
    });
    window.addEventListener("scroll", sync, { passive: true });
    sync();
  }

  function setupRegistrationSteps() {
    const form = document.querySelector("[data-registration-form]");
    if (!form) return;
    const steps = Array.from(form.querySelectorAll("[data-registration-step]"));
    const indicators = Array.from(form.querySelectorAll("[data-step-indicator]"));
    function show(stepNumber) {
      steps.forEach((step) => {
        step.hidden = step.dataset.registrationStep !== String(stepNumber);
      });
      indicators.forEach((indicator) => {
        indicator.classList.toggle("is-active", indicator.dataset.stepIndicator === String(stepNumber));
      });
    }
    form.addEventListener("click", (event) => {
      if (event.target.closest("[data-next-registration-step]")) show(2);
      if (event.target.closest("[data-prev-registration-step]")) show(1);
    });
    const firstInvalidStep = steps.find((step) => step.querySelector(".error"));
    if (firstInvalidStep) show(firstInvalidStep.dataset.registrationStep);
  }

  apply();
  setupBackToTop();
  setupRegistrationSteps();
  showWelcomePopup();
})();
