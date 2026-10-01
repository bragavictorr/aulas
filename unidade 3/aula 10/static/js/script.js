// ============================================
// VELDORA
// JAVASCRIPT
// ============================================


// ============================================
// CABEÇALHO AO ROLAR
// ============================================

const cabecalho = document.querySelector(".cabecalho");


window.addEventListener("scroll", function () {

    if (!cabecalho) {
        return;
    }

    if (window.scrollY > 50) {

        cabecalho.classList.add("rolando");

    } else {

        cabecalho.classList.remove("rolando");

    }

});


// ============================================
// ANIMAÇÃO DOS ELEMENTOS
// ============================================

const elementosAnimados = document.querySelectorAll(
    ".produto, .valor, .sobre-conteudo, .sobre-card"
);


const observador = new IntersectionObserver(

    function (elementos) {

        elementos.forEach(function (elemento) {

            if (elemento.isIntersecting) {

                elemento.target.classList.add("aparecer");

                observador.unobserve(elemento.target);

            }

        });

    },

    {
        threshold: 0.15
    }

);


elementosAnimados.forEach(function (elemento) {

    observador.observe(elemento);

});


// ============================================
// BOTÃO "EXPLORAR PRODUTOS"
// ============================================

const botaoExplorar = document.querySelector(
    ".hero .botao"
);


if (botaoExplorar) {

    botaoExplorar.addEventListener(
        "click",
        function (evento) {

            evento.preventDefault();

            const produtos = document.querySelector(
                "#produtos"
            );

            if (produtos) {

                produtos.scrollIntoView({
                    behavior: "smooth",
                    block: "start"
                });

            }

        }
    );

}


// ============================================
// EFEITO NOS CARDS DOS PRODUTOS
// ============================================

const produtos = document.querySelectorAll(
    ".produto"
);


produtos.forEach(function (produto) {

    produto.addEventListener(
        "mouseenter",
        function () {

            produto.style.transform =
                "translateY(-8px)";

        }
    );


    produto.addEventListener(
        "mouseleave",
        function () {

            produto.style.transform =
                "";

        }
    );

});


// ============================================
// EFEITO DE MOVIMENTO NO HERO
// ============================================

const hero = document.querySelector(".hero");


if (hero) {

    hero.addEventListener(
        "mousemove",
        function (evento) {

            const x =
                (evento.clientX / window.innerWidth - 0.5) * 10;

            const y =
                (evento.clientY / window.innerHeight - 0.5) * 10;


            const elementoV =
                hero.querySelector("::before");


            hero.style.backgroundPosition =
                `${50 + x}% ${50 + y}%`;

        }
    );

}


// ============================================
// ANIMAÇÃO DO BOTÃO
// ============================================

const botoes = document.querySelectorAll(
    ".botao"
);


botoes.forEach(function (botao) {

    botao.addEventListener(
        "mouseenter",
        function () {

            botao.style.transform =
                "translateY(-3px)";

        }
    );


    botao.addEventListener(
        "mouseleave",
        function () {

            botao.style.transform =
                "";

        }
    );

});


// ============================================
// LOG NO CONSOLE
// ============================================

console.log(
    "Veldora carregada com sucesso."
);