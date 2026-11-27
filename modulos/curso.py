"""Datos y modalidad de un curso de formación."""

from dataclasses import dataclass

from .profesor import Profesor


@dataclass(frozen=True)
class Curso:
    codigo: str
    nombre: str
    descripcion: str
    duracion_horas: int
    modalidad: str
    profesor: Profesor

    # Validación. Comprueba los datos obligatorios y la duración del curso.
    def __post_init__(self):
        campos_obligatorios = (self.codigo, self.nombre, self.descripcion, self.modalidad)
        if not all(campo.strip() for campo in campos_obligatorios):
            raise ValueError("El código, el nombre, la descripción y la modalidad son obligatorios.")
        if self.duracion_horas <= 0:
            raise ValueError("La duración debe ser mayor que cero.")
