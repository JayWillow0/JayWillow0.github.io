(function () {
  "use strict";
  window.Snackbar = window.Snackbar || {
    show: function (options) {
      var current = document.querySelector(".lab-snackbar");
      if (current) current.remove();
      var notice = document.createElement("div");
      notice.className = "lab-snackbar";
      notice.setAttribute("role", "status");
      notice.textContent = options && options.text ? options.text : "";
      document.body.appendChild(notice);
      requestAnimationFrame(function () { notice.classList.add("is-visible"); });
      window.setTimeout(function () {
        notice.classList.remove("is-visible");
        window.setTimeout(function () { notice.remove(); }, 220);
      }, (options && options.duration) || 2400);
    }
  };
}());
