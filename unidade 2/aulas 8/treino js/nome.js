const nome = prompt("digite o seu nome:");
const saudacao = "bem vindo " + nome;

const elementoH2 = document.getElementById("nomeUsuario");
elementoH2.innerText =saudacao
