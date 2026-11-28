"""Clase abstracta para los datos comunes de una persona."""

from abc import ABC, abstractmethod


class Persona(ABC):
    # Datos personales. Valida y protege el nombre, el documento y la edad.
    def __init__(self, nombre: str, documento: str, edad: int):
        self.__nombre = nombre.strip()
        self.__documento = documento.strip()
        if not self.__nombre or not self.__documento:
            raise ValueError("El nombre y el documento son obligatorios.")
        if edad <= 0:
            raise ValueError("La edad debe ser mayor que cero.")
        self.__edad = edad

    @property
    def documento(self) -> str:
        return self.__documento

    # Contrato de Persona. Profesor y Aprendiz definen su rol y presentación.
    @abstractmethod
    def obtener_rol(self) -> str:
        ...

    @abstractmethod
    def mostrar_informacion(self) -> str:
        ...

    def _informacion_personal(self) -> str:
        return f"{self.obtener_rol()} {self.__nombre} - Documento: {self.documento} - Edad: {self.__edad}"
