# Cobalto Software House

Site institucional em Django: Início, Soluções, Sobre nós e Contato.

## Rodando

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser  # para ver as mensagens de contato no /admin
python manage.py runserver
```

Abra http://127.0.0.1:8000

## Onde mexer

| O que | Onde |
|---|---|
| Textos (empresa, soluções, processo, cases, time) | `core/content.py` |
| HTML base (head, topo, rodapé) | `templates/base.html` e `templates/partials/` |
| Páginas | `templates/core/*.html` |
| Cores, fontes e espaçamentos | topo de `static/css/style.css` (variáveis em `:root`) |
| Mensagens do formulário de contato | `/admin` → Contatos |

## Antes de publicar

- Troque `SECRET_KEY`, defina `DEBUG = False` e preencha `ALLOWED_HOSTS` em `config/settings.py`.
- Rode `python manage.py collectstatic` e sirva `staticfiles/` (ex.: WhiteNoise ou Nginx).
- Configure o envio de e-mail se quiser notificação a cada contato recebido.

## Fontes

Bricolage Grotesque e Newsreader, hospedadas em `static/fonts/` (licença SIL OFL, incluída).
