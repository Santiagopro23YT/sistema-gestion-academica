from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal, InvalidOperation

from modulos.aprendiz import Aprendiz
from modulos.calificacion import Calificacion
from modulos.curso import Curso
from modulos.inscripcion import Inscripcion
from modulos.profesor import Profesor


class RepositorioLectura(ABC):
    @abstractmethod
    def buscar(self, clave):
        pass

    @abstractmethod
    def listar(self):
        pass


class RepositorioEscritura(ABC):
    @abstractmethod
    def guardar(self, clave, objeto):
        pass


class RepositorioMemoria(RepositorioLectura, RepositorioEscritura):
    def __init__(self):
        self.__datos = {}

    def buscar(self, clave):
        return self.__datos.get(clave)

    def listar(self):
        return list(self.__datos.values())

    def guardar(self, clave, objeto):
        self.__datos[clave] = objeto


class GestionAcademica:
    def __init__(self, profesores, aprendices, cursos, inscripciones, modalidades, estados):
        self.__profesores = profesores
        self.__aprendices = aprendices
        self.__cursos = cursos
        self.__inscripciones = inscripciones
        self.modalidades = modalidades
        self.estados = estados

    def registrar_profesor(self, profesor):
        if self.__profesores.buscar(profesor.documento) is not None:
            raise ValueError("Ya existe un profesor con ese documento.")
        for p in self.__profesores.listar():
            if p.codigo == profesor.codigo:
                raise ValueError("Ya existe un profesor con ese código.")
        self.__profesores.guardar(profesor.documento, profesor)

    def listar_profesores(self):
        return self.__profesores.listar()

    def buscar_profesor(self, documento):
        profesor = self.__profesores.buscar(documento.strip())
        if profesor is None:
            raise ValueError("No se encontró el profesor.")
        return profesor

    def registrar_aprendiz(self, aprendiz):
        if self.__aprendices.buscar(aprendiz.documento) is not None:
            raise ValueError("Ya existe un aprendiz con ese documento.")
        self.__aprendices.guardar(aprendiz.documento, aprendiz)

    def listar_aprendices(self):
        return self.__aprendices.listar()

    def buscar_aprendiz(self, documento):
        aprendiz = self.__aprendices.buscar(documento.strip())
        if aprendiz is None:
            raise ValueError("No se encontró el aprendiz.")
        return aprendiz

    def registrar_curso(self, codigo, nombre, descripcion, duracion, modalidad, doc_profesor):
        codigo = codigo.strip()
        if self.__cursos.buscar(codigo) is not None:
            raise ValueError("Ya existe un curso con ese código.")
        if modalidad not in self.modalidades:
            raise ValueError("La modalidad seleccionada no existe.")
        profesor = self.buscar_profesor(doc_profesor)
        curso = Curso(codigo, nombre, descripcion, duracion, modalidad, profesor)
        self.__cursos.guardar(codigo, curso)

    def listar_cursos(self):
        return self.__cursos.listar()

    def buscar_curso(self, codigo):
        curso = self.__cursos.buscar(codigo.strip())
        if curso is None:
            raise ValueError("No se encontró el curso.")
        return curso

    def inscribir_aprendiz(self, doc_aprendiz, cod_curso, estado):
        aprendiz = self.buscar_aprendiz(doc_aprendiz)
        curso = self.buscar_curso(cod_curso)
        clave = (aprendiz.documento, curso.codigo)
        if self.__inscripciones.buscar(clave) is not None:
            raise ValueError("El aprendiz ya está inscrito en este curso.")
        if estado not in self.estados:
            raise ValueError("El estado de inscripción no existe.")
        inscripcion = Inscripcion(aprendiz, curso, date.today(), estado)
        self.__inscripciones.guardar(clave, inscripcion)

    def buscar_inscripcion(self, doc_aprendiz, cod_curso):
        clave = (doc_aprendiz.strip(), cod_curso.strip())
        inscripcion = self.__inscripciones.buscar(clave)
        if inscripcion is None:
            raise ValueError("No se encontró la inscripción.")
        return inscripcion

    def cursos_por_aprendiz(self, doc_aprendiz):
        aprendiz = self.buscar_aprendiz(doc_aprendiz)
        resultado = []
        for ins in self.__inscripciones.listar():
            if ins.aprendiz.documento == aprendiz.documento:
                resultado.append(ins)
        return resultado

    def aprendices_por_curso(self, cod_curso):
        curso = self.buscar_curso(cod_curso)
        resultado = []
        for ins in self.__inscripciones.listar():
            if ins.curso.codigo == curso.codigo:
                resultado.append(ins)
        return resultado

    def cursos_por_profesor(self, doc_profesor):
        profesor = self.buscar_profesor(doc_profesor)
        resultado = []
        for curso in self.__cursos.listar():
            if curso.profesor.documento == profesor.documento:
                resultado.append(curso)
        return resultado

    def registrar_nota(self, doc_aprendiz, cod_curso, valor):
        inscripcion = self.buscar_inscripcion(doc_aprendiz, cod_curso)
        inscripcion.registrar_calificacion(Calificacion(valor))
        self.__inscripciones.guardar((inscripcion.aprendiz.documento, inscripcion.curso.codigo), inscripcion)

    def modificar_nota(self, doc_aprendiz, cod_curso, numero_nota, valor):
        inscripcion = self.buscar_inscripcion(doc_aprendiz, cod_curso)
        inscripcion.modificar_calificacion(numero_nota, Calificacion(valor))
        self.__inscripciones.guardar((inscripcion.aprendiz.documento, inscripcion.curso.codigo), inscripcion)


def pedir_texto(mensaje):
    texto = input(f"{mensaje}: ").strip()
    if not texto:
        raise ValueError(f"{mensaje} es obligatorio.")
    return texto


def pedir_entero(mensaje):
    texto = pedir_texto(mensaje)
    try:
        return int(texto)
    except ValueError:
        raise ValueError(f"{mensaje} debe ser un número entero.")


def pedir_nota():
    texto = pedir_texto("Nota (0.0 a 5.0)").replace(",", ".")
    try:
        return Decimal(texto)
    except InvalidOperation:
        raise ValueError("Ingrese una nota numérica válida.")


def elegir_opcion(titulo, lista):
    print(f"\n{titulo}:")
    for i in range(len(lista)):
        print(f"  {i + 1}. {lista[i]}")
    num = pedir_entero("Opción")
    if num < 1 or num > len(lista):
        raise ValueError("La opción seleccionada no existe.")
    return lista[num - 1]


def imprimir_personas(lista):
    if not lista:
        print("No hay registros.")
        return
    for persona in lista:
        print(persona.mostrar_informacion())


def mostrar_curso(curso):
    print(
        f"{curso.codigo} | {curso.nombre} | {curso.modalidad} | {curso.duracion_horas} horas\n"
        f"  Descripción: {curso.descripcion}\n"
        f"  Responsable: {curso.profesor.mostrar_informacion()}"
    )


def mostrar_rendimiento(inscripcion):
    notas = ", ".join(str(n.valor) for n in inscripcion.calificaciones)
    if not notas:
        notas = "Sin notas"
    promedio, resultado = inscripcion.evaluar()
    promedio_texto = f"{promedio:.2f}" if promedio is not None else "Pendiente"
    print(
        f"{inscripcion.curso.codigo} | {inscripcion.curso.nombre} | "
        f"{inscripcion.fecha.isoformat()} | {inscripcion.estado}\n"
        f"  {inscripcion.aprendiz.mostrar_informacion()}\n"
        f"  Calificaciones: {notas} | Promedio: {promedio_texto} | Resultado: {resultado}"
    )


def menu_profesores(sistema):
    while True:
        print("\n--- PROFESORES ---")
        print("1. Registrar profesor")
        print("2. Listar profesores")
        print("3. Buscar por documento")
        print("0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                profesor = Profesor(
                    pedir_texto("Nombre"),
                    pedir_texto("Documento"),
                    pedir_entero("Edad"),
                    pedir_texto("Profesión"),
                    pedir_texto("Código de profesor"),
                    pedir_texto("Especialidad"),
                )
                sistema.registrar_profesor(profesor)
                print("Profesor registrado.")
            elif op == "2":
                imprimir_personas(sistema.listar_profesores())
            elif op == "3":
                doc = pedir_texto("Documento")
                print(sistema.buscar_profesor(doc).mostrar_informacion())
            elif op == "0":
                break
            else:
                print("Opción no válida.")
        except ValueError as e:
            print(f"Error: {e}")


def menu_aprendices(sistema):
    while True:
        print("\n--- APRENDICES ---")
        print("1. Registrar aprendiz")
        print("2. Listar aprendices")
        print("3. Buscar por documento")
        print("0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                aprendiz = Aprendiz(
                    pedir_texto("Nombre"),
                    pedir_texto("Documento"),
                    pedir_entero("Edad"),
                    pedir_texto("Contacto"),
                )
                sistema.registrar_aprendiz(aprendiz)
                print("Aprendiz registrado.")
            elif op == "2":
                imprimir_personas(sistema.listar_aprendices())
            elif op == "3":
                doc = pedir_texto("Documento")
                print(sistema.buscar_aprendiz(doc).mostrar_informacion())
            elif op == "0":
                break
            else:
                print("Opción no válida.")
        except ValueError as e:
            print(f"Error: {e}")


def menu_cursos(sistema):
    while True:
        print("\n--- CURSOS ---")
        print("1. Registrar curso y asignar profesor")
        print("2. Listar cursos")
        print("3. Consultar por código")
        print("0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                codigo = pedir_texto("Código del curso")
                nombre = pedir_texto("Nombre")
                descripcion = pedir_texto("Descripción")
                duracion = pedir_entero("Duración en horas")
                modalidad = elegir_opcion("Modalidad", sistema.modalidades)
                doc_prof = pedir_texto("Documento del profesor responsable")
                sistema.registrar_curso(codigo, nombre, descripcion, duracion, modalidad, doc_prof)
                print("Curso registrado.")
            elif op == "2":
                cursos = sistema.listar_cursos()
                if not cursos:
                    print("No hay cursos registrados.")
                for c in cursos:
                    mostrar_curso(c)
            elif op == "3":
                mostrar_curso(sistema.buscar_curso(pedir_texto("Código del curso")))
            elif op == "0":
                break
            else:
                print("Opción no válida.")
        except ValueError as e:
            print(f"Error: {e}")


def menu_inscripciones(sistema):
    while True:
        print("\n--- INSCRIPCIONES ---")
        print("1. Inscribir aprendiz")
        print("2. Ver cursos de un aprendiz")
        print("3. Ver aprendices de un curso")
        print("0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                doc = pedir_texto("Documento del aprendiz")
                cod = pedir_texto("Código del curso")
                estado = elegir_opcion("Estado", sistema.estados)
                sistema.inscribir_aprendiz(doc, cod, estado)
                print("Inscripción registrada.")
            elif op == "2":
                lista = sistema.cursos_por_aprendiz(pedir_texto("Documento del aprendiz"))
                if not lista:
                    print("No hay inscripciones.")
                for ins in lista:
                    print(f"{ins.curso.codigo} | {ins.curso.nombre} | {ins.fecha.isoformat()} | {ins.estado}")
            elif op == "3":
                lista = sistema.aprendices_por_curso(pedir_texto("Código del curso"))
                if not lista:
                    print("No hay aprendices inscritos.")
                for ins in lista:
                    print(f"{ins.aprendiz.mostrar_informacion()} | {ins.fecha.isoformat()} | {ins.estado}")
            elif op == "0":
                break
            else:
                print("Opción no válida.")
        except ValueError as e:
            print(f"Error: {e}")


def menu_profesor_responsable(sistema):
    try:
        doc_prof = pedir_texto("Documento del profesor")
        profesor = sistema.buscar_profesor(doc_prof)
    except ValueError as e:
        print(f"Error: {e}")
        return

    while True:
        print(f"\n--- {profesor.mostrar_informacion()} ---")
        print("1. Consultar mis cursos")
        print("2. Consultar aprendices de un curso mío")
        print("3. Registrar calificación")
        print("4. Modificar calificación")
        print("5. Consultar calificaciones y promedio")
        print("6. Generar informe académico del curso")
        print("0. Volver")
        op = input("Opción: ").strip()
        try:
            if op == "1":
                cursos = sistema.cursos_por_profesor(doc_prof)
                if not cursos:
                    print("No tiene cursos asignados.")
                for c in cursos:
                    mostrar_curso(c)
            elif op in ("2", "3", "4", "5", "6"):
                cod = pedir_texto("Código del curso")
                curso = sistema.buscar_curso(cod)
                if curso.profesor.documento != doc_prof.strip():
                    print("Error: El curso no está asignado a este profesor.")
                    continue
                if op == "2":
                    lista = sistema.aprendices_por_curso(cod)
                    if not lista:
                        print("No hay aprendices inscritos.")
                    for ins in lista:
                        print(f"{ins.aprendiz.mostrar_informacion()} | {ins.fecha.isoformat()} | {ins.estado}")
                elif op == "3":
                    doc_ap = pedir_texto("Documento del aprendiz")
                    sistema.registrar_nota(doc_ap, cod, pedir_nota())
                    print("Calificación registrada.")
                elif op == "4":
                    doc_ap = pedir_texto("Documento del aprendiz")
                    ins = sistema.buscar_inscripcion(doc_ap, cod)
                    notas = ins.calificaciones
                    if not notas:
                        print("La inscripción aún no tiene calificaciones.")
                        continue
                    for i in range(len(notas)):
                        print(f"{i + 1}. {notas[i].valor}")
                    num = pedir_entero("Número de calificación")
                    sistema.modificar_nota(doc_ap, cod, num, pedir_nota())
                    print("Calificación modificada.")
                elif op == "5":
                    doc_ap = pedir_texto("Documento del aprendiz")
                    ins = sistema.buscar_inscripcion(doc_ap, cod)
                    mostrar_rendimiento(ins)
                elif op == "6":
                    lista = sistema.aprendices_por_curso(cod)
                    print(f"\nInforme académico del curso {cod}")
                    if not lista:
                        print("No hay registros.")
                    for ins in lista:
                        mostrar_rendimiento(ins)
            elif op == "0":
                break
            else:
                print("Opción no válida.")
        except ValueError as e:
            print(f"Error: {e}")


def consultar_rendimiento_aprendiz(sistema):
    try:
        doc = pedir_texto("Documento del aprendiz")
        lista = sistema.cursos_por_aprendiz(doc)
        print(f"\nInforme de rendimiento del aprendiz {doc}")
        if not lista:
            print("No hay registros.")
        for ins in lista:
            mostrar_rendimiento(ins)
    except ValueError as e:
        print(f"Error: {e}")


def main():
    sistema = GestionAcademica(
        profesores=RepositorioMemoria(),
        aprendices=RepositorioMemoria(),
        cursos=RepositorioMemoria(),
        inscripciones=RepositorioMemoria(),
        modalidades=("Formación titulada", "Formación complementaria"),
        estados=("Activa", "Retirada", "Finalizada"),
    )

    while True:
        print("\n=== SISTEMA DE GESTIÓN ACADÉMICA ===")
        print("1. Profesores")
        print("2. Aprendices")
        print("3. Cursos")
        print("4. Inscripciones")
        print("5. Consultar rendimiento por aprendiz")
        print("6. Cursos del profesor")
        print("0. Salir")
        op = input("Opción: ").strip()

        if op == "1":
            menu_profesores(sistema)
        elif op == "2":
            menu_aprendices(sistema)
        elif op == "3":
            menu_cursos(sistema)
        elif op == "4":
            menu_inscripciones(sistema)
        elif op == "5":
            consultar_rendimiento_aprendiz(sistema)
        elif op == "6":
            menu_profesor_responsable(sistema)
        elif op == "0":
            print("Sesión finalizada.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
