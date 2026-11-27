"""Datos y rol del profesor."""

from .persona import Persona


class Profesor(Persona):
    # Datos del profesor. Valida la profesión, el código y la especialidad.
    def __init__(
        self, nombre: str, documento: str, edad: int, profesion: str, codigo: str, especialidad: str
    ):
        super().__init__(nombre, documento, edad)
        self.__profesion = profesion.strip()
        self.__codigo = codigo.strip()
        self.__especialidad = especialidad.strip()
        if not all((self.__profesion, self.__codigo, self.__especialidad)):
            raise ValueError("La profesión, el código y la especialidad son obligatorios.")

    @property
    def codigo(self) -> str:
        return self.__codigo

    # Presentación. Agrega los datos propios del profesor al resumen personal.
    def obtener_rol(self) -> str:
        return "Profesor"

    def mostrar_informacion(self) -> str:
        return (
            f"{self._informacion_personal()} | Profesión: {self.__profesion} "
            f"| Código: {self.codigo} | Especialidad: {self.__especialidad}"
        )
