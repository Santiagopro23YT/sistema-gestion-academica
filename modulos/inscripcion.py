"""Relación entre un aprendiz y un curso y sus notas."""

from datetime import date
from decimal import Decimal

from .aprendiz import Aprendiz
from .calificacion import Calificacion
from .curso import Curso


class Inscripcion:
    # Reglas de evaluación. Fijan la cantidad mínima de notas y la aprobación.
    MINIMO_CALIFICACIONES = 3
    NOTA_APROBACION = Decimal("3.0")

    def __init__(self, aprendiz: Aprendiz, curso: Curso, fecha: date, estado: str):
        self.__aprendiz = aprendiz
        self.__curso = curso
        self.__fecha = fecha
        self.__estado = estado
        self.__calificaciones: list[Calificacion] = []

    # Consultas. Permiten leer los datos guardados y obtener una copia de las notas.
    @property
    def aprendiz(self) -> Aprendiz:
        return self.__aprendiz

    @property
    def curso(self) -> Curso:
        return self.__curso

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def calificaciones(self) -> tuple[Calificacion, ...]:
        return tuple(self.__calificaciones)

    # Cambios de notas. Agrega una calificación o reemplaza la posición indicada.
    def registrar_calificacion(self, calificacion: Calificacion) -> None:
        self.__calificaciones.append(calificacion)

    def modificar_calificacion(
        self, numero_calificacion: int, calificacion: Calificacion
    ) -> None:
        if not 1 <= numero_calificacion <= len(self.__calificaciones):
            raise ValueError("El número de calificación no existe.")
        posicion = numero_calificacion - 1
        self.__calificaciones[posicion] = calificacion

    # Evaluación. Calcula el promedio y determina el resultado del aprendiz.
    def promedio(self) -> Decimal | None:
        cantidad_calificaciones = len(self.__calificaciones)
        if cantidad_calificaciones < self.MINIMO_CALIFICACIONES:
            return None
        suma_calificaciones = sum(nota.valor for nota in self.__calificaciones)
        return suma_calificaciones / cantidad_calificaciones

    def evaluar(self) -> tuple[Decimal | None, str]:
        promedio = self.promedio()
        if promedio is None:
            return None, "Pendiente"
        resultado = "Aprobado" if promedio >= self.NOTA_APROBACION else "Reprobado"
        return promedio, resultado

    def resultado(self) -> str:
        _, resultado = self.evaluar()
        return resultado
