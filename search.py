from repository import PublicacoesDB
from termos import TERMOS

with PublicacoesDB() as db:
    resp = db.query(
        """
        SELECT *
        FROM
            publicacoes
        WHERE
            MATCH (titulo , ementa , conteudo) AGAINST (%s)
                AND data="2021-11-12"
        """,
        (" ".join(["'" + '"' + termo + '"' + "'" for termo in TERMOS]),),
    )

    print(resp)
    
    
    


