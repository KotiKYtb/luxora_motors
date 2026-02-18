(function () {
  "use strict";

  if (typeof gsap === "undefined" || typeof ScrollTrigger === "undefined") {
    // Fallback si GSAP non chargé
    var revealEls = document.querySelectorAll(".reveal");
    if (revealEls.length && "IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) entry.target.classList.add("visible");
        });
      }, { threshold: 0.1 });
      revealEls.forEach(function (el) { observer.observe(el); });
    }
    return;
  }

  gsap.registerPlugin(ScrollTrigger);

  // ----- Hero (page d'accueil) — une ligne + CTA type Moteur & Sens
  var heroContent = document.querySelector(".hero-content");
  if (heroContent) {
    var heroLine1 = heroContent.querySelector(".hero-line1");
    var heroCta = heroContent.querySelector(".hero-cta");

    gsap.timeline({ defaults: { ease: "power3.out" } })
      .fromTo(heroLine1, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 1 }, 0.2)
      .fromTo(heroCta, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.7 }, 0.5);
  }

  // ----- Section "Nos services" — titre et items en révélation
  var servicesSection = document.querySelector("#nos-services");
  if (servicesSection) {
    var servicesTitleWrap = servicesSection.querySelector(".section-title-wrap");
    var serviceItems = servicesSection.querySelectorAll(".service-item.card-reveal");
    if (servicesTitleWrap) {
      gsap.timeline({
        scrollTrigger: {
          trigger: servicesSection,
          start: "top 82%",
          toggleActions: "play none none none",
        },
        defaults: { ease: "power3.out" },
      })
        .fromTo(servicesTitleWrap, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8 })
        .fromTo(serviceItems, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5, stagger: 0.1 }, "-=0.4");
    }
  }

  // ----- Section "Les dernières nouveautés" — titre puis cartes en révélation séquentielle
  var sectionHeader = document.querySelector("#vedettes .section-header");
  if (sectionHeader) {
    var sectionTitleWrap = sectionHeader.querySelector(".section-title-wrap");
    if (sectionTitleWrap) {
      gsap.timeline({
        scrollTrigger: {
          trigger: sectionHeader,
          start: "top 82%",
          toggleActions: "play none none none",
        },
        defaults: { ease: "power3.out" },
      }).fromTo(sectionTitleWrap, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.8 });
    }
  }

  // Cartes : apparition en décalé (type Moteur & Sens — révélations séquentielles)
  var cards = document.querySelectorAll(".vehicules-grid .vehicule-card.card-reveal");
  if (cards.length) {
    cards.forEach(function (card) {
      var body = card.querySelector(".card-body");
      if (!body) return;
      var title = body.querySelector(".card-title");
      var marque = body.querySelector(".card-marque");
      var specsLine = body.querySelector(".card-specs-line");
      var cta = body.querySelector(".card-cta");
      var innerEls = [title, marque, specsLine, cta].filter(Boolean);

      gsap.set(card, { opacity: 0, y: 36 });
      gsap.set(innerEls, { opacity: 0, y: 12 });

      var cardTl = gsap.timeline({
        scrollTrigger: {
          trigger: card,
          start: "top 90%",
          toggleActions: "play none none none",
        },
        defaults: { ease: "power3.out" },
      });
      cardTl.to(card, { opacity: 1, y: 0, duration: 0.6 });
      if (title) cardTl.to(title, { opacity: 1, y: 0, duration: 0.35 }, "-=0.3");
      if (marque) cardTl.to(marque, { opacity: 1, y: 0, duration: 0.3 }, "-=0.2");
      if (specsLine) cardTl.to(specsLine, { opacity: 1, y: 0, duration: 0.3 }, "-=0.2");
      if (cta) cardTl.to(cta, { opacity: 1, y: 0, duration: 0.25 }, "-=0.15");
    });
  }

  // ----- Contact strip
  var contactStrip = document.querySelector(".contact-strip");
  if (contactStrip) {
    var contactTitle = contactStrip.querySelector(".contact-strip-title");
    var contactDesc = contactStrip.querySelector(".contact-strip-desc");
    var contactMethods = contactStrip.querySelector(".contact-methods");
    if (contactTitle) {
      gsap.timeline({
        scrollTrigger: {
          trigger: contactStrip,
          start: "top 88%",
          toggleActions: "play none none none",
        },
        defaults: { ease: "power3.out" },
      })
        .fromTo(contactTitle, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.7 })
        .fromTo(contactDesc, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.6 }, "-=0.5")
        .fromTo(contactMethods, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.5 }, "-=0.4");
    }
  }

  // ----- Page liste véhicules (page-hero)
  var pageHero = document.querySelector(".page-hero");
  if (pageHero) {
    var pageHeroTitle = pageHero.querySelector(".page-hero-title");
    var pageHeroDesc = pageHero.querySelector(".page-hero-desc");
    if (pageHeroTitle) {
      gsap.timeline({ defaults: { ease: "power3.out" } })
        .fromTo(pageHeroTitle, { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.8 }, 0.2)
        .fromTo(pageHeroDesc, { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.6 }, 0.4);
    }
  }

  // ----- Footer (révélation légère)
  var footer = document.querySelector(".site-footer");
  if (footer) {
    gsap.fromTo(footer, { opacity: 0 }, {
      opacity: 1,
      duration: 1,
      scrollTrigger: {
        trigger: footer,
        start: "top 95%",
        toggleActions: "play none none none",
      },
    });
  }

  // ----- Micro-interactions boutons (scale au clic)
  document.querySelectorAll(".btn, .cta-header").forEach(function (btn) {
    btn.addEventListener("mousedown", function () {
      gsap.to(btn, { scale: 0.97, duration: 0.1 });
    });
    btn.addEventListener("mouseup", function () {
      gsap.to(btn, { scale: 1, duration: 0.2, ease: "power2.out" });
    });
    btn.addEventListener("mouseleave", function () {
      gsap.to(btn, { scale: 1, duration: 0.2, ease: "power2.out" });
    });
  });

  // ----- Parallax léger sur le hero background
  var hero = document.querySelector(".hero");
  if (hero && window.innerWidth > 768) {
    gsap.to(".hero-bg-glow", {
      y: -30,
      ease: "none",
      scrollTrigger: {
        trigger: ".hero",
        start: "top top",
        end: "bottom top",
        scrub: 1,
      },
    });
  }

  // ----- Menu mobile (hamburger)
  var navToggle = document.getElementById("nav-toggle");
  var navOverlay = document.getElementById("nav-overlay");
  var navMobile = document.getElementById("nav-mobile");
  var body = document.body;

  function openNav() {
    body.classList.add("nav-open");
    if (navToggle) {
      navToggle.setAttribute("aria-expanded", "true");
      navToggle.setAttribute("aria-label", "Fermer le menu");
      navToggle.classList.add("is-open");
    }
    if (navMobile) navMobile.setAttribute("aria-hidden", "false");
    document.documentElement.style.overflow = "hidden";
  }

  function closeNav() {
    body.classList.remove("nav-open");
    if (navToggle) {
      navToggle.setAttribute("aria-expanded", "false");
      navToggle.setAttribute("aria-label", "Ouvrir le menu");
      navToggle.classList.remove("is-open");
    }
    if (navMobile) navMobile.setAttribute("aria-hidden", "true");
    document.documentElement.style.overflow = "";
  }

  if (navToggle) {
    navToggle.addEventListener("click", function () {
      if (body.classList.contains("nav-open")) closeNav();
      else openNav();
    });
  }
  if (navOverlay) {
    navOverlay.addEventListener("click", closeNav);
  }
  if (navMobile) {
    var mobileLinks = navMobile.querySelectorAll(".nav-mobile-link, .nav-mobile-cta");
    mobileLinks.forEach(function (link) {
      link.addEventListener("click", closeNav);
    });
  }

  window.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && body.classList.contains("nav-open")) closeNav();
  });

  // ----- Dropdown Marques (page À vendre) — checkboxes personnalisé
  var marqueDropdown = document.getElementById("marque-dropdown");
  if (marqueDropdown) {
    var marqueTrigger = document.getElementById("marque-dropdown-trigger");
    var marqueValue = document.getElementById("marque-dropdown-value");
    var marquePanel = document.getElementById("marque-dropdown-panel");
    var marqueCheckboxes = marquePanel ? marquePanel.querySelectorAll(".filter-dropdown-checkbox") : [];

    function updateMarqueLabel() {
      var labels = [];
      marqueCheckboxes.forEach(function (cb) {
        if (cb.checked) labels.push(cb.getAttribute("data-label") || cb.value);
      });
      marqueValue.textContent = labels.length ? labels.join(", ") : "Toutes les marques";
    }

    function closeMarqueDropdown() {
      marqueDropdown.classList.remove("is-open");
      if (marqueTrigger) marqueTrigger.setAttribute("aria-expanded", "false");
      if (marquePanel) marquePanel.setAttribute("aria-hidden", "true");
    }

    if (marqueTrigger && marquePanel) {
      marqueTrigger.addEventListener("click", function (e) {
        e.preventDefault();
        var isOpen = marqueDropdown.classList.toggle("is-open");
        marqueTrigger.setAttribute("aria-expanded", isOpen);
        marquePanel.setAttribute("aria-hidden", !isOpen);
      });
    }
    marqueCheckboxes.forEach(function (cb) {
      cb.addEventListener("change", updateMarqueLabel);
    });

    document.addEventListener("click", function (e) {
      if (marqueDropdown.classList.contains("is-open") && !marqueDropdown.contains(e.target)) closeMarqueDropdown();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && marqueDropdown.classList.contains("is-open")) closeMarqueDropdown();
    });
  }

  // ----- Filtres AJAX (page À vendre) — mise à jour dynamique de la grille
  var filtersForm = document.getElementById("filters-form");
  var vehiculesGrid = document.getElementById("vehicules-grid");
  var vehiculesSection = document.getElementById("vehicules-section");

  if (filtersForm && vehiculesGrid && vehiculesSection) {
    var filtersWrap = document.getElementById("filters-wrap");
    var filtersToggle = document.getElementById("filters-toggle");
    var filtersCollapsible = document.getElementById("filters-collapsible");
    if (filtersToggle && filtersWrap && filtersCollapsible) {
      filtersToggle.addEventListener("click", function () {
        var collapsed = filtersWrap.classList.toggle("is-collapsed");
        filtersToggle.setAttribute("aria-expanded", !collapsed);
      });
    }

    var baseUrl = (filtersForm.getAttribute("action") || window.location.pathname).replace(/\?.*$/, "").trim();
    if (baseUrl.indexOf("/") !== 0) baseUrl = "/" + baseUrl;

    function applyFilters(queryString) {
      var sep = queryString && queryString.length ? "?" : "";
      var url = baseUrl + sep + (queryString || "");
      if (url.indexOf("ajax=") === -1) {
        url += (url.indexOf("?") !== -1 ? "&" : "?") + "ajax=1";
      }
      vehiculesSection.classList.add("is-loading");
      fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(function (r) {
          if (!r.ok) throw new Error(r.status);
          return r.text();
        })
        .then(function (html) {
          vehiculesGrid.innerHTML = html;
          vehiculesSection.classList.remove("is-loading");
          var cleanQs = (queryString || "").replace(/&?ajax=1&?/g, "").replace(/^&|&$/g, "");
          history.pushState({}, "", cleanQs ? baseUrl + "?" + cleanQs : baseUrl);
        })
        .catch(function () {
          vehiculesSection.classList.remove("is-loading");
        });
    }

    function applyFiltersFromForm() {
      var fd = new FormData(filtersForm);
      var params = new URLSearchParams();
      fd.forEach(function (value, key) {
        if (value != null) params.append(key, String(value).trim());
      });
      if (!params.has("tri")) params.set("tri", "recent");
      params.set("ajax", "1");
      applyFilters(params.toString());
    }

    var filterDebounceTimer;
    function scheduleApplyFilters() {
      clearTimeout(filterDebounceTimer);
      filterDebounceTimer = setTimeout(applyFiltersFromForm, 400);
    }

    filtersForm.addEventListener("submit", function (e) {
      e.preventDefault();
      applyFiltersFromForm();
    });

    filtersForm.addEventListener("change", function () {
      applyFiltersFromForm();
    });

    var numberInputs = filtersForm.querySelectorAll('input[name="annee_min"], input[name="annee_max"], input[name="prix_min"], input[name="prix_max"], input[name="km_max"]');
    numberInputs.forEach(function (input) {
      input.addEventListener("input", scheduleApplyFilters);
    });

    var btnApply = document.getElementById("btn-filters-apply");
    if (btnApply) btnApply.addEventListener("click", applyFiltersFromForm);

    var resetBtn = filtersForm.querySelector(".btn-filters-reset");
    if (resetBtn) {
      resetBtn.addEventListener("click", function (e) {
        e.preventDefault();
        filtersForm.reset();
        var marqueValueEl = document.getElementById("marque-dropdown-value");
        if (marqueValueEl) marqueValueEl.textContent = "Toutes les marques";
        var triValueEl = document.getElementById("tri-value");
        if (triValueEl) triValueEl.value = "recent";
        syncTriDisplay("recent");
        applyFilters("ajax=1");
      });
    }

    var triDropdown = document.getElementById("tri-dropdown");
    var triTrigger = document.getElementById("tri-dropdown-trigger");
    var triPanel = document.getElementById("tri-dropdown-panel");
    var triValueInput = document.getElementById("tri-value");
    var triValueDisplay = document.getElementById("tri-dropdown-value");
    var triLabels = { recent: "Plus récents", prix_asc: "Prix croissant", prix_desc: "Prix décroissant", annee_desc: "Année récente", annee_asc: "Année ancienne", km_asc: "Kilométrage croissant" };

    function syncTriDisplay(value) {
      var v = value || "recent";
      if (triValueDisplay) triValueDisplay.textContent = triLabels[v] || triLabels.recent;
      if (triPanel) {
        triPanel.querySelectorAll(".filter-dropdown-option-tri").forEach(function (opt) {
          opt.classList.toggle("is-selected", opt.getAttribute("data-value") === v);
          opt.setAttribute("aria-selected", opt.getAttribute("data-value") === v ? "true" : "false");
        });
      }
    }

    function closeTriDropdown() {
      if (triDropdown) triDropdown.classList.remove("is-open");
      if (triTrigger) triTrigger.setAttribute("aria-expanded", "false");
      if (triPanel) triPanel.setAttribute("aria-hidden", "true");
    }

    if (triTrigger && triPanel && triValueInput) {
      triTrigger.addEventListener("click", function (e) {
        e.preventDefault();
        var isOpen = triDropdown.classList.toggle("is-open");
        triTrigger.setAttribute("aria-expanded", isOpen);
        triPanel.setAttribute("aria-hidden", !isOpen);
      });
      triPanel.querySelectorAll(".filter-dropdown-option-tri").forEach(function (opt) {
        opt.addEventListener("click", function (e) {
          e.preventDefault();
          var val = opt.getAttribute("data-value");
          triValueInput.value = val;
          syncTriDisplay(val);
          closeTriDropdown();
          applyFiltersFromForm();
        });
      });
    }
    document.addEventListener("click", function (e) {
      if (triDropdown && triDropdown.classList.contains("is-open") && !triDropdown.contains(e.target)) closeTriDropdown();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && triDropdown && triDropdown.classList.contains("is-open")) closeTriDropdown();
    });

    window.addEventListener("popstate", function () {
      var params = new URLSearchParams(window.location.search);
      var marques = params.getAll("marque");
      filtersForm.querySelectorAll('input[name="marque"]').forEach(function (cb) {
        cb.checked = marques.indexOf(cb.value) !== -1;
      });
      var marqueValueEl = document.getElementById("marque-dropdown-value");
      if (marqueValueEl) {
        var labels = [];
        filtersForm.querySelectorAll('input[name="marque"]:checked').forEach(function (cb) {
          labels.push(cb.getAttribute("data-label") || cb.value);
        });
        marqueValueEl.textContent = labels.length ? labels.join(", ") : "Toutes les marques";
      }
      ["annee_min", "annee_max", "prix_min", "prix_max", "km_max", "tri"].forEach(function (name) {
        var el = filtersForm.querySelector('[name="' + name + '"]');
        if (el) el.value = params.get(name) || "";
      });
      syncTriDisplay(params.get("tri") || "recent");
      params.set("ajax", "1");
      applyFilters(params.toString());
    });
  }
})();
