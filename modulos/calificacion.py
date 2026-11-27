from decimal import Decimal, InvalidOperation


class Calificacion:
    def __init__(self, valor):
        try:
            nota = Decimal(str(valor))
        except InvalidOperation:
            raise ValueError("La calificación debe ser un número válido.")
        if not nota.is_finite() or nota < Decimal("0.0") or nota > Decimal("5.0"):
            raise ValueError("La calificación debe estar entre 0.0 y 5.0.")
        self.__valor = nota

    @property
    def valor(self):
        return self.__valor
