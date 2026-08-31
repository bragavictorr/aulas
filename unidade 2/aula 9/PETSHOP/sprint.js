
    /* ----------------------------------------------------------
       4. BOTÃO FLUTUANTE DO WHATSAPP
       Criado inteiramente por JS, não precisa mexer no HTML.
       Troque o número no lugar indicado.
    ---------------------------------------------------------- */
    const numeroWhatsapp = "5522999999999"; // formato: DDI + DDD + número, só dígitos
    const mensagemPadrao = "Olá! Gostaria de saber mais sobre o PetSpa.";
  
    const botaoWhats = document.createElement("a");
    botaoWhats.href = `https://wa.me/${numeroWhatsapp}?text=${encodeURIComponent(mensagemPadrao)}`;
    botaoWhats.target = "_blank";
    botaoWhats.rel = "noopener";
    botaoWhats.setAttribute("aria-label", "Falar no WhatsApp");
    botaoWhats.id = "botao-whatsapp-flutuante";
    botaoWhats.innerHTML = "&#9990;"; // ícone simples de telefone (troque por um ícone real se preferir)
    botaoWhats.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 56px;
      height: 56px;
      background-color: #25D366;
      color: #ffffff;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 26px;
      text-decoration: none;
      box-shadow: 0 4px 10px rgba(0,0,0,0.3);
      z-index: 1000;
    `;
    document.body.appendChild(botaoWhats);
  