from src.utils import today_brazil_tz


class DataErradaNoDBError(Exception):
    def __init__(self, data_final_db):
        super().__init__(
            f"Tentou fazer a súmula do dia {data_final_db}, mas era para ser a do dia {today_brazil_tz()}"
        )


class SumulaVazia(Exception):
    def __init__(self, data_inicial, data_final):
        super().__init__(
            f"Não encontrou publicações nos DOUs do dia {data_inicial} (pub extra) e {data_final}"
        )
