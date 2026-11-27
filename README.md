# Sistema de gestión académica

Aplicación de consola en Python para administrar profesores, aprendices, cursos de formación, inscripciones y calificaciones usando programación orientada a objetos, principios SOLID y datos temporales en memoria.

## Cómo ejecutar

Desde la carpeta del proyecto, ejecutar:

```powershell
python -B gestion_academica.py
```

## Estructura

- `gestion_academica.py`: archivo principal con la consola, `GestionAcademica` y el almacenamiento en memoria.
- `modulos/persona.py`: clase abstracta `Persona`.
- `modulos/profesor.py`: clase `Profesor`.
- `modulos/aprendiz.py`: clase `Aprendiz`.
- `modulos/curso.py`: clase `Curso`.
- `modulos/calificacion.py`: clase `Calificacion`.
- `modulos/inscripcion.py`: clase `Inscripcion`.

## Pilares de POO y SOLID

- **Encapsulamiento:** atributos privados (`__`) con propiedades y validaciones.
- **Abstracción y Herencia:** `Persona` es abstracta (`ABC` y `@abstractmethod`) y la heredan `Profesor` y `Aprendiz`.
- **Polimorfismo:** `Profesor` y `Aprendiz` sobrescriben `obtener_rol()` y `mostrar_informacion()`.
- **SOLID:** separación de responsabilidades por módulo, modalidades y estados configurables, sustitución de `Persona` al listar, repositorios separados de lectura y escritura, e inyección de dependencias en memoria en `GestionAcademica`.
