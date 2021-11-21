import datetime
from typing import List
import pandas as pd
import re
import operator
from functools import reduce

from terms import ASSINATURAS_PRESIDENTE_E_DIRETORES


def keyword_search(
    df: pd.DataFrame, columns: List[pd.Series], keywords: List[str], where=None
) -> pd.DataFrame:

    base = r"^{}"
    expr = "(?=.*{})"
    search_regex = base.format("|".join(expr.format(w) for w in keywords))

    frames = [
        column.notnull()
        & column.str.contains(search_regex, flags=re.IGNORECASE, regex=True)
        for column in columns
    ]

    df = df[reduce(operator.iand, frames)]  # equivalente a => df[condition1 & c2 & c3]

    if where is None:
        return df

    return df[where]


def diretores_e_presidente(df: pd.DataFrame) -> pd.DataFrame:
    return keyword_search(
        df,
        [df.assinatura],
        ASSINATURAS_PRESIDENTE_E_DIRETORES,
        where=(df.data == datetime.date(2021, 11, 19)),
    )
