from dataclasses import dataclass
from typing import List




x = """
# |-----------------------------------------|2|-----------------------------------------|
###### ✅ DO1 -- [LEI Nº 13.257](https://www.in.gov.br/en/web/dou/-/lei-n-14.257-de-1-de-dezembro-de-2021-364245086)
# |-----------------------------------------|6|-----------------------------------------|

###### ❌ DO1 -- [PORTARIA Nº 27](https://www.in.gov.br/en/web/dou/-/portaria-n-27-de-3-de-dezembro-de-2021-364691847)

###### ✅ DO1 -- [DESPACHO Nº 660 e DESPACHO Nº 661](https://www.in.gov.br/web/dou/-/despachos-do-presidente-da-republica-364679067)
# |-----------------------------------------|8|-----------------------------------------|
###### ✅ [PORTARIA Nº 112.182](https://www.in.gov.br/web/dou/-/portaria-n-112.182-de-7-de-dezembro-de-2021-365417725) -- DO2 -- `Assinatura do presidente do BC`
###### ✅ [PORTARIA Nº 112.184](https://www.in.gov.br/web/dou/-/portaria-n-112.184-de-7-de-dezembro-de-2021-365419679) -- DO2 -- `Assinatura do presidente do BC`
###### ✅ [PORTARIA DE PESSOAL COAF Nº 27](https://www.in.gov.br/en/web/dou/-/portaria-de-pessoal-coaf-n-27-de-7-de-dezembro-de-2021-365417179) -- DO2 -- `Portaria assinada pelo presidente do COAF`
###### ❌ [DECRETO Nº 10.886](https://www.in.gov.br/en/web/dou/-/decreto-n-10.886-de-7-de-dezembro-de-2021-365433440) -- DO1
###### ❌ [RESOLUÇÃO CICC Nº 2](https://www.in.gov.br/web/dou/-/resolucao-cicc-n-2-de-10-de-setembro-de-2021-365431584)
# |-----------------------------------------|9|-----------------------------------------|
###### ✅ [PORTARIA Nº 112.200](https://www.in.gov.br/en/web/dou/-/portaria-n-112.200-de-8-de-dezembro-de-2021-365733615) -- DO2 => `Despacho emitido pela Diretora de Administração do Banco Central do Brasil`
###### ✅ [PORTARIA COAF Nº 28](https://www.in.gov.br/en/web/dou/-/portaria-coaf-n-28-de-8-de-dezembro-de-2021-366016969) -- DO1 => `Publicação do Banco Central no DO1 que não é Instrução Normativa` 
###### ✅ [DESPACHO Nº 670](https://www.in.gov.br/en/web/dou/-/despachos-do-presidente-da-republica-366014424) -- DO1 => `"cargo de Diretor da Comissão de Valores Mobiliários" no conteúdo`

###### ❌ [PORTARIA ME Nº 14.384](https://www.in.gov.br/en/web/dou/-/portaria-me-n-14.384-de-7-de-dezembro-de-2021-366020075) -- DO1

###### ✅ [PORTARIA ME Nº 14.313](https://www.in.gov.br/web/dou/-/portaria-me-n-14.313-de-7-de-dezembro-de-2021-365732255) -- DO2 => `Afastamento dado pelo Ministro de Estado da Economia`

###### ✅ [PORTARIA DE PESSOAL SETO/ME Nº 14.540](https://www.in.gov.br/en/web/dou/-/portaria-de-pessoal-seto/me-n-14.540-de-7-de-dezembro-de-2021-365733455)  -- DO2 => `"cargo de Secretário do Tesouro Nacional" no conteúdo`

###### ❌ [RESOLUÇÃO CICC Nº 3](https://www.in.gov.br/en/web/dou/-/resolucao-cicc-n-3-de-7-de-dezembro-de-2021-366035485)
# |-----------------------------------------|10|-----------------------------------------|
###### ✅ [PORTARIA Nº 112.213](https://www.in.gov.br/en/web/dou/-/portaria-n-112.213-de-9-de-dezembro-de-2021-366110379) -- DO2 -- `Assinatura presidente/diretor BC`
###### ✅ [PORTARIA Nº 112.214](https://www.in.gov.br/en/web/dou/-/portaria-n-112.214-de-9-de-dezembro-de-2021-366067111) -- DO2 -- `Assinatura presidente/diretor BC`
###### ✅  [COMUNICADO Nº 38.023](https://www.in.gov.br/web/dou/-/comunicado-n-38.023-de-8-de-dezembro-de-2021-366228507) -- DO3 -- `Assinatura presidente/diretor BC`
###### ❌ [DECRETO Nº 10.888](https://www.in.gov.br/web/dou/-/decreto-n-10.888-de-9-de-dezembro-de-2021-366038343) 
###### ❌ [DECRETO Nº 10.889](https://www.in.gov.br/en/web/dou/-/decreto-n-10.889-de-9-de-dezembro-de-2021-366039278)
###### ❌ [DECRETO Nº 10.890](https://www.in.gov.br/en/web/dou/-/decreto-n-10.890-de-9-de-dezembro-de-2021-366038708)
###### ❌ [PORTARIA SEGES/ME Nº 14.399](https://www.in.gov.br/web/dou/-/portaria-seges/me-n-14.399-de-8-de-dezembro-de-2021-366051027)

# |-----------------------------------------|13|-----------------------------------------|
###### ✅ [PORTARIA Nº 112.231](https://www.in.gov.br/en/web/dou/-/portaria-n-112.231-de-9-de-dezembro-de-2021-366485810) --DO1 -- `Assinatura do presidente do BC`
###### ✅ [RESOLUÇÃO BCB Nº 171](https://www.in.gov.br/web/dou/-/resolucao-bcb-n-171-de-9-de-dezembro-de-2021-366541799) -- DO1 -- `publicação do BC no DO1 que não é instrução normativa`

# |-----------------------------------------|14|-----------------------------------------|
# [PORTARIA Nº 112.342](https://www.in.gov.br/web/dou/-/portaria-n-112.342-de-13-de-dezembro-de-2021-366877142)

# [PORTARIA Nº 112.320](https://www.in.gov.br/web/dou/-/portaria-n-112.320-de-13-de-dezembro-de-2021-366877302) 

# [INSTRUÇÃO NORMATIVA Nº 2](https://www.in.gov.br/en/web/dou/-/instrucao-normativa-n-2-de-13-de-dezembro-de-2021-366864794#wrapper)
# |-----------------------------------------|15|-----------------------------------------|
# [PORTARIA ME Nº 14.804](https://www.in.gov.br/en/web/dou/-/portaria-me-n-14.804-de-13-de-dezembro-de-2021-367164862)
# |-----------------------------------------|16|-----------------------------------------|
###### ✅ [RESOLUÇÃO BCB Nº 174](https://www.in.gov.br/en/web/dou/-/resolucao-bcb-n-174-de-14-de-dezembro-de-2021-367703856) 

###### ✅ [PORTARIA Nº 112.381](https://www.in.gov.br/en/web/dou/-/portaria-n-112.381-de-15-de-dezembro-de-2021-367554055)

# |-----------------------------------------|17|-----------------------------------------|
# [RESOLUÇÃO BCB Nº 175](https://www.in.gov.br/en/web/dou/-/resolucao-bcb-n-175-de-15-de-dezembro-de-2021-367953998)

# [PORTARIA Nº 112.404](https://www.in.gov.br/en/web/dou/-/portaria-n-112.404-de-16-de-dezembro-de-2021-367911490)

# [PORTARIA Nº 112.405](https://www.in.gov.br/en/web/dou/-/portaria-n-112.405-de-16-de-dezembro-de-2021-367907688)

# [DESPACHO DO PRESIDENTE](https://www.in.gov.br/web/dou/-/despacho-do-presidente-de-15-de-dezembro-de-2021-367907830)

# [LEI Nº 14.261](https://www.in.gov.br/en/web/dou/-/lei-n-14.261-de-16-de-dezembro-de-2021-367944672)

# [RESOLUÇÃO NORMATIVA ANEEL Nº 957](https://www.in.gov.br/en/web/dou/-/resolucao-normativa-aneel-n-957-de-7-de-dezembro-de-2021-367984284)
# |-----------------------------------------|20|-----------------------------------------|
# [RESOLUÇÃO CMN Nº 4.971](https://www.in.gov.br/web/dou/-/resolucao-cmn-n-4.971-de-16-de-dezembro-de-2021-368302041)

# [RESOLUÇÃO CMN Nº 4.972](https://www.in.gov.br/web/dou/-/resolucao-cmn-n-4.972-de-16-de-dezembro-de-2021-368306203)

# [RESOLUÇÃO CMN Nº 4.973](https://www.in.gov.br/en/web/dou/-/resolucao-cmn-n-4.973-de-16-de-dezembro-de-2021-368354350)

# [RESOLUÇÃO CMN Nº 4.974](https://www.in.gov.br/web/dou/-/resolucao-cmn-n-4.974-de-16-de-dezembro-de-2021-368302332)

# [RESOLUÇÃO CMN Nº 4.975](https://www.in.gov.br/web/dou/-/resolucao-cmn-n-4.975-de-16-de-dezembro-de-2021-368306767)

# [RESOLUÇÃO CMN Nº 4.976](https://www.in.gov.br/en/web/dou/-/resolucao-cmn-n-4.976-de-16-de-dezembro-de-2021-368305822)

# [RESOLUÇÃO CMN Nº 4.977](https://www.in.gov.br/web/dou/-/resolucao-cmn-n-4.977-de-16-de-dezembro-de-2021-368306285)

# [PORTARIA Nº 112.430](https://www.in.gov.br/web/dou/-/portaria-n-112.430-de-17-de-dezembro-de-2021-368306605)

# [DECRETO Nº 10.900](https://www.in.gov.br/web/dou/-/decreto-n-10.900-de-17-de-dezembro-de-2021-368282514)

# [PORTARIA SEGES/ME Nº 14.584](https://www.in.gov.br/en/web/dou/-/portaria-seges/me-n-14.584-de-13-de-dezembro-de-2021-368302986)

# [INSTRUÇÃO NORMATIVA SGP/SEDGG/ME Nº 113](https://www.in.gov.br/en/web/dou/-/instrucao-normativa-sgp/sedgg/me-n-113-de-14-de-dezembro-de-2021-368300001)
# |-----------------------------------------|21|-----------------------------------------|
# [PORTARIA Nº 112.497](https://www.in.gov.br/web/dou/-/portaria-n-112.497-de-20-de-dezembro-de-2021-368659451)


###### ❌ [PORTARIA CONJUNTA SETO-SEDGG/ME Nº 132](https://www.in.gov.br/en/web/dou/-/portaria-conjunta-seto-sedgg/me-n-132-de-10-de-dezembro-de-2021-368975509)

# [PORTARIA SOF/ME Nº 14.790](https://www.in.gov.br/en/web/dou/-/portaria-sof/me-n-14.790-de-17-de-dezembro-de-2021-368978374)
# |-----------------------------------------|22|-----------------------------------------|
# [PORTARIA ME Nº 14.817](https://www.in.gov.br/en/web/dou/-/portaria-me-n-14.817-de-20-de-dezembro-de-2021-369345454)
# |-----------------------------------------|23|-----------------------------------------|

# [PORTARIA Nº 112.543](https://www.in.gov.br/en/web/dou/-/portaria-n-112.543-de-22-de-dezembro-de-2021-369760000)

# [DESPACHO](https://www.in.gov.br/web/dou/-/despacho-do-presidente-da-republica-368623572)  *publicação de 21/12/2021

# [RESOLUÇÃO CVM Nº 59](https://www.in.gov.br/en/web/dou/-/resolucao-cvm-n-59-de-22-de-dezembro-de-2021-369780708)

# |-----------------------------------------|24|-----------------------------------------|
# [RESOLUÇÃO BCB Nº 176](https://www.in.gov.br/web/dou/-/resolucao-bcb-n-176-de-22-de-dezembro-de-2021-370002821)
# [RESOLUÇÃO BCB Nº 177](https://www.in.gov.br/web/dou/-/resolucao-bcb-n-177-de-22-de-dezembro-de-2021-370056064)
# [DESPACHO](https://www.in.gov.br/en/web/dou/-/despacho-de-22-de-dezembro-de-2021-369815724)
# [DESPACHO](https://www.in.gov.br/en/web/dou/-/despacho-de-22-de-dezembro-de-2021-369806199)
# [DECRETO Nº 10.912](https://www.in.gov.br/en/web/dou/-/decreto-n-10.912-de-23-de-dezembro-de-2021-370051785)
# [PORTARIA ME Nº 15.287](https://www.in.gov.br/web/dou/-/portaria-me-n-15.287-de-23-de-dezembro-de-2021-369805304)
# [PORTARIA ME Nº 15.310](https://www.in.gov.br/web/dou/-/portaria-me-n-15.310-de-23-de-dezembro-de-2021-369809954)
# [PORTARIA DE PESSOAL SETO/ME Nº 15.279](https://www.in.gov.br/web/dou/-/portaria-de-pessoal-seto/me-n-15.279-de-22-de-dezembro-de-2021-369806024)

# [RESOLUÇÃO CVM Nº 60](https://www.in.gov.br/en/web/dou/-/resolucao-cvm-n-60-de-23-de-dezembro-de-2021-370073233)

# |-----------------------------------------|27|-----------------------------------------|
# [PORTARIA Nº 112.562](https://in.gov.br/en/web/dou/-/portaria-n-112.562-de-24-de-dezembro-de-2021-370101068)

# [INSTRUÇÃO NORMATIVA Nº 6](https://www.in.gov.br/en/web/dou/-/instrucao-normativa-n-6-de-23-de-dezembro-de-2021-370081858)

# [PORTARIA SAJ/SG/PR Nº 2](https://www.in.gov.br/en/web/dou/-/portaria-saj/sg/pr-n-2-de-24-de-dezembro-de-2021-370100483)
"""

