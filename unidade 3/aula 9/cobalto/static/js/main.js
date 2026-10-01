// Menu mobile: abre e fecha o menu principal.
(function () {
  var botao = document.querySelector(".topo__menu-btn");
  var menu = document.getElementById("menu-principal");
  if (!botao || !menu) return;

  function definir(aberto) {
    botao.setAttribute("aria-expanded", String(aberto));
    botao.querySelector(".sr-only").textContent = aberto ? "Fechar menu" : "Abrir menu";
    menu.classList.toggle("menu--aberto", aberto);
  }

  botao.addEventListener("click", function () {
    definir(botao.getAttribute("aria-expanded") !== "true");
  });

  // Fecha ao escolher um link ou ao apertar Esc.
  menu.addEventListener("click", function (e) {
    if (e.target.closest("a")) definir(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") definir(false);
  });
})();
