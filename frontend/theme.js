const toggleBtn = document.getElementById("themeToggle");
const menuBtn = document.getElementById("menuBtn");
const sidebar = document.getElementById("sidebar");

function setTheme(mode) {
  document.body.className = mode;
  localStorage.setItem("theme", mode);
  toggleBtn.textContent = mode === "dark" ? "☀️ Light" : "🌙 Dark";
}

toggleBtn?.addEventListener("click", () => {
  const newTheme = document.body.className === "dark" ? "light" : "dark";
  setTheme(newTheme);
});


const main = document.querySelector(".main");

menuBtn?.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  main.classList.toggle("with-sidebar");
});


const savedTheme = localStorage.getItem("theme") || "light";
setTheme(savedTheme);





