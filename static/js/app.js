(function () {
  const root = document.documentElement;
  const btn = document.querySelector("[data-theme-toggle]");
  const key = "plex_theme";

  function setTheme(t) {
    root.setAttribute("data-theme", t);
    localStorage.setItem(key, t);
  }

  const saved = localStorage.getItem(key);
  if (saved === "light" || saved === "dark") setTheme(saved);

  if (btn) {
    btn.addEventListener("click", () => {
      const current = root.getAttribute("data-theme") || "light";
      setTheme(current === "light" ? "dark" : "light");
    });
  }
})(); 
