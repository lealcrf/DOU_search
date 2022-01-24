import unicodedata
from datetime import date, datetime, timedelta


def tirar_acentuacao(string: str):
    if string is not None:
        return "".join(
            c
            for c in unicodedata.normalize("NFD", string)
            if unicodedata.category(c) != "Mn"
        )


def str_to_date(string: str) -> date:
    return datetime.strptime(string, r"\d{4}-\d{2}-\d{2}").date()


class DateRange:
    def __init__(self, inicio: date, fim: date):
        self.inicio = inicio
        self.fim = fim

    @staticmethod
    def same_day(day=date.today().day, month=date.today().month, year=date.today().year):
        data = date(year, month, day)
        return DateRange(data, data)


    @staticmethod
    def all_dates():
        return DateRange(date.min, date.max)

    @staticmethod
    def from_ultimos_n_dias(n_dias: int, ultimo_dia=date.today()):
        return DateRange(
            inicio=ultimo_dia - timedelta(days=n_dias),
            fim=ultimo_dia,
        )
