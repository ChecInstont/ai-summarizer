const toggleBtn = document.getElementById("themeToggle");
const menuBtnLeft = document.getElementById("menuBtnLeft");
const sidebar = document.getElementById("sidebar");
const rightSidebar = document.getElementById('ai-config');
const menuBtnRight = document.getElementById('menuBtnRight');



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

menuBtnLeft?.addEventListener("click", () => {
  sidebar.classList.toggle("open");
  main.classList.toggle("with-sidebar");
});

menuBtnRight.addEventListener('click', () => {
  rightSidebar.classList.toggle('open');
  main.classList.toggle("with-ai-config-sidebar");
});


const savedTheme = localStorage.getItem("theme") || "light";
setTheme(savedTheme);





