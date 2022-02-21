import requests
from datetime import date
from jinja2 import Template


def gerar_email_sumula(sumula_seccionada, titulo, titulo_email, enviar=False):
    with open("src/infrastructure/email/template.html", "r") as f:
        t = Template(f.read())

        email = t.render(
            titulo=titulo,
            sumula=sumula_seccionada,
        )

    if enviar:
        requests.post(
            "https://prod-13.brazilsouth.logic.azure.com:443/workflows/5ac567658c7544e7a354860ff7010607/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=lvnHRaaGkRBUnT4vb6-xXnkv8dDb9UV_h-VhxD33kEM",
            json={
                "titulo_email": titulo_email,
                "sumula": email,
            },
        )
    return email
