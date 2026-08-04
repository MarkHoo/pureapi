(function () {
  "use strict";

  var zhToEn = {
    "index.html": "en/index.html",
    "installation.html": "en/installation.html",
    "quickstart.html": "en/quickstart.html",
    "routing.html": "en/routing.html",
    "requests.html": "en/requests-responses.html",
    "responses.html": "en/requests-responses.html",
    "openapi.html": "en/openapi.html",
    "deployment.html": "en/deployment.html",
    "contributing.html": "en/contributing.html",
  };

  var enToZh = {
    "index.html": "../index.html",
    "installation.html": "../installation.html",
    "quickstart.html": "../quickstart.html",
    "routing.html": "../routing.html",
    "requests-responses.html": "../requests.html",
    "openapi.html": "../openapi.html",
    "deployment.html": "../deployment.html",
    "contributing.html": "../contributing.html",
  };

  function currentFile() {
    var path = window.location.pathname;
    if (path.endsWith("/")) {
      return "index.html";
    }
    return path.substring(path.lastIndexOf("/") + 1) || "index.html";
  }

  function isEnglishPage() {
    return window.location.pathname.indexOf("/en/") !== -1;
  }

  function targetUrl(targetLanguage) {
    var file = currentFile();
    var hash = window.location.hash || "";

    if (targetLanguage === "en") {
      if (isEnglishPage()) {
        return file + hash;
      }
      return (zhToEn[file] || "en/index.html") + hash;
    }

    if (isEnglishPage()) {
      return (enToZh[file] || "../index.html") + hash;
    }
    return file + hash;
  }

  function createLink(label, href, isCurrent) {
    var link = document.createElement("a");
    link.className = "pureapi-language-switcher__link";
    link.href = href;
    link.textContent = label;
    if (isCurrent) {
      link.setAttribute("aria-current", "true");
    }
    return link;
  }

  function init() {
    if (document.querySelector(".pureapi-language-switcher")) {
      return;
    }

    var currentIsEnglish = isEnglishPage();
    var switcher = document.createElement("div");
    var button = document.createElement("button");
    var menu = document.createElement("div");

    switcher.className = "pureapi-language-switcher";
    button.className = "pureapi-language-switcher__button";
    button.type = "button";
    button.setAttribute("aria-haspopup", "true");
    button.setAttribute("aria-expanded", "false");
    button.textContent = currentIsEnglish ? "English" : "中文";

    menu.className = "pureapi-language-switcher__menu";
    menu.setAttribute("role", "menu");
    menu.appendChild(createLink("中文", targetUrl("zh"), !currentIsEnglish));
    menu.appendChild(createLink("English", targetUrl("en"), currentIsEnglish));

    button.addEventListener("click", function () {
      var isOpen = switcher.classList.toggle("is-open");
      button.setAttribute("aria-expanded", String(isOpen));
    });

    document.addEventListener("click", function (event) {
      if (!switcher.contains(event.target)) {
        switcher.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") {
        switcher.classList.remove("is-open");
        button.setAttribute("aria-expanded", "false");
      }
    });

    switcher.appendChild(button);
    switcher.appendChild(menu);
    document.body.appendChild(switcher);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
