from .persona import Persona


class Aprendiz(Persona):
    def __init__(self, nombre, documento, edad, contacto):
        super().__init__(nombre, documento, edad)
        if not contacto.strip():
            raise ValueError("El contacto es obligatorio.")
        self.__contacto = contacto.strip()

    @property
    def contacto(self):
        return self.__contacto

    def obtener_rol(self):
        return "Aprendiz"

    def mostrar_informacion(self):
        return f"{self._informacion_personal()} | Contacto: {self.__contacto}"
