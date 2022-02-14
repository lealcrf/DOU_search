import requests


def cria_email_sumula(sumula_seccionada, data, edicao):
    base = """<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
  <html>
    <head>
      <!-- Compiled with Bootstrap Email version: 1.1.2 --><meta http-equiv="x-ua-compatible" content="ie=edge">
      <meta name="x-apple-disable-message-reformatting">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <style type="text/css">
        body,table,td{font-family:Helvetica,Arial,sans-serif !important}.ExternalClass{width:100%}.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{line-height:150%}a{text-decoration:none}*{color:inherit}a[x-apple-data-detectors],u+#body a,#MessageViewBody a{color:inherit;text-decoration:none;font-size:inherit;font-family:inherit;font-weight:inherit;line-height:inherit}img{-ms-interpolation-mode:bicubic}table:not([class^=s-]){font-family:Helvetica,Arial,sans-serif;mso-table-lspace:0pt;mso-table-rspace:0pt;border-spacing:0px;border-collapse:collapse}table:not([class^=s-]) td{border-spacing:0px;border-collapse:collapse}@media screen and (max-width: 600px){*[class*=s-lg-]>tbody>tr>td{font-size:0 !important;line-height:0 !important;height:0 !important}}
      </style>
    </head>
    <body class="bg-light" style="outline: 0; width: 100%; min-width: 100%; height: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: Helvetica, Arial, sans-serif; line-height: 24px; font-weight: normal; font-size: 16px; -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box; color: #000000; margin: 0; padding: 0; border-width: 0;" bgcolor="#f7fafc">
      <table class="bg-light body" valign="top" role="presentation" border="0" cellpadding="0" cellspacing="0" style="outline: 0; width: 100%; min-width: 100%; height: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: Helvetica, Arial, sans-serif; line-height: 24px; font-weight: normal; font-size: 16px; -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box; color: #000000; margin: 0; padding: 0; border-width: 0;" bgcolor="#f7fafc">
        <tbody>
          <tr>
            <td valign="top" style="line-height: 24px; font-size: 16px; margin: 0;" align="left" bgcolor="#f7fafc">
            <img src="https://bacen-my.sharepoint.com/:i:/r/personal/matheus_santiago_bcb_gov_br/Documents/banner-dou.jpg?csf=1&web=1&e=SwOZza" class="img-fluid" style="height: auto; line-height: 100%; outline: none; text-decoration: none; display: block; max-width: 100%; width: 100%; border-style: none; border-width: 0;" width="100%">
            <p class="text-muted text-center" style="line-height: 24px; font-size: 16px; color: #718096; width: 100%; margin: 0;" align="center">Secretaria da Diretoria e do Conselho Monet&#225;rio Nacional &#8211; Sucon</p>
            <div style="height: 20px;"></div>
            <p class="text-center h5" style="font-weight: bold; color: #404040; line-height: 24px; font-size: 20px; padding-top: 0; padding-bottom: 0; vertical-align: baseline; width: 100%; margin: 0;" align="center">Publica&#231;&#245;es de {{{DATA}}} |
             {{{EDIÇÃO}}}</p>
            <div style="height: 30px;"></div>
          {{{CONTENT}}}
          </tr>
        </tbody>
      </table>
    </body>
  </html>"""
    content = []
    for escopo, publicacoes in sumula_seccionada.items():
        content.append(_add_table(escopo, publicacoes))

    email = (
        base.replace("{{{CONTENT}}}", "".join(content))
        .replace("{{{DATA}}}", data.strftime("%d/%m/%Y"))
        .replace("{{{EDIÇÃO}}}", edicao)
    )

    requests.post(
        "https://prod-13.brazilsouth.logic.azure.com:443/workflows/5ac567658c7544e7a354860ff7010607/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=lvnHRaaGkRBUnT4vb6-xXnkv8dDb9UV_h-VhxD33kEM",
        json={"sumula": email},
    )
    return email


def _add_table(escopo, publicacoes):
    return f"""<div style="margin: 0 12.5% 30px;">
        <p style="font-weight: bold; color: #404040; line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">{escopo}</p>

        <table class="table align-middle" border="0" cellpadding="0" cellspacing="0" style="width: 100%; max-width: 100%;">
            <thead>
                <th style="width: 20%; line-height: 24px; font-size: 16px; margin: 0;" align="left"></th>
                <th style="width: 50%; line-height: 24px; font-size: 16px; margin: 0;" align="left"></th>
                <th style="width: 30%; line-height: 24px; font-size: 16px; margin: 0;" align="left"></th>
            </thead>
            <tbody>
              {"".join([_add_publicacao(p["titulo"], p["url"], p["ementa"], p["motivos"]) for p in publicacoes])}
            </tbody>
        </table>
      </div>"""


def _add_publicacao(titulo, url, ementa, motivos):
    return """<tr>
                <td style="line-height: 24px; font-size: 16px; border-top-width: 1px; border-top-color: #e2e8f0; border-top-style: solid; margin: 0; padding: 12px 25px 12px 12px;" align="left" valign="top">
                    <u><a href="{url}" style="color: #551a8b;"> {titulo} </a></u>
                </td>
                <td style="line-height: 24px; font-size: 16px; border-top-width: 1px; border-top-color: #e2e8f0; border-top-style: solid; padding: 12px 25px;" align="left" valign="top">{ementa}</td>
                <td style="line-height: 24px; font-size: 16px; border-top-width: 1px; border-top-color: #e2e8f0; border-top-style: solid; margin: 0; padding: 12px 12px 12px 25px;" align="left" valign="top">
                <span style="white-space: pre-line">{motivos}</span>
                </td>
              </tr>""".format(
        url=url,
        titulo=titulo,
        ementa=ementa,
        motivos="\n".join(["● " + motivo.replace("\\", "") for motivo in motivos]),
    )
