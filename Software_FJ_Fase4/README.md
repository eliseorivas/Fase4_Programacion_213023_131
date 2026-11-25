# Software FJ - Sistema Integral de Gestión de Clientes, Servicios y Reservas

**UNAD - Programación 213023 - Fase 4 | Grupo 213023_131 | Proyecto integral**

Proyecto completo e independiente que implementa los cinco aportes funcionales exigidos por el Anexo 3. **La entrega individual debe ser autorizada por el tutor**, ya que la guía establece una actividad colaborativa. Es una implementación integral de referencia, no una afirmación de autoría de los aportes realizados por otros estudiantes.

## Cobertura completa de los cinco aportes
| Aporte | Implementación | Archivos |
|---|---|---|
| 1. Clase Cliente | Validación y encapsulación de nombre, documento y teléfono | `entidades.py`, `validaciones.py` |
| 2. Servicio abstracto y un servicio | Métodos abstractos, tarifa y servicio de sala | `servicios.py` |
| 3. Otros dos servicios | Alquiler de equipos y asesoría especializada con herencia, polimorfismo y sobrescritura | `servicios.py` |
| 4. Clase Reserva | Integración de cliente, servicio, duración, estado, costos, confirmación y cancelación | `reservas.py`, `sistema.py` |
| 5. Excepciones, validaciones y logs | Errores personalizados, validaciones, try/except/else/finally y log | `excepciones.py`, `validaciones.py`, `logs/software_fj.log` |

Además, `main.py` ofrece un menú interactivo; `demostracion.py` ejecuta 16 operaciones y `test_sistema.py` verifica 22 casos automatizados.

## Qué hace
- Registra clientes validando nombre, documento y teléfono.
- Ofrece tres servicios: reserva de salas, alquiler de equipos y asesorías especializadas.
- Crea, procesa, confirma y cancela reservas.
- Calcula tarifas por horas con descuentos e impuestos opcionales.
- Mantiene todos los datos en memoria mediante objetos y listas. **No usa bases de datos**.
- Registra eventos y errores en `logs/software_fj.log`.
- Maneja errores personalizados, `try/except`, `try/except/else/finally` y encadenamiento de excepciones.

## Requisitos
- Python 3.10 o posterior (sin bibliotecas externas).

## Cómo abrir en Visual Studio Code
1. Descomprime `Software_FJ_Fase4.zip`.
2. En VS Code, elige **Archivo > Abrir carpeta** y selecciona `Software_FJ_Fase4`.
3. Abre **Terminal > Nueva terminal**.
4. Escribe lo siguiente según la operación deseada:

```bash
python main.py
```

Este comando abre un menú interactivo de registro de clientes, servicios y reservas.

```bash
python demostracion.py
```

Este comando ejecuta 16 operaciones numeradas (válidas e inválidas) y deja evidencia en el archivo de logs.

```bash
python -m unittest test_sistema.py -v
```

Este comando ejecuta las pruebas automatizadas; debe terminar con `OK`.

En algunos equipos Windows el comando es `py` en lugar de `python`.

## Archivos del proyecto
- `main.py`: menú de usuario.
- `entidades.py`: clase abstracta Entidad y clase Cliente.
- `servicios.py`: clase abstracta Servicio y los tres servicios concretos.
- `reservas.py`: clase Reserva y estados pendiente, confirmada, cancelada.
- `excepciones.py`: tipos de error y ejecución controlada con logs.
- `validaciones.py`: validaciones compartidas.
- `sistema.py`: coordinación de listas de clientes, servicios y reservas.
- `demostracion.py`: las 16 operaciones de demostración.
- `test_sistema.py`: comprobaciones automáticas independientes.
- `logs/software_fj.log`: evidencia de los eventos y errores generados.
- `EVIDENCIA_EJECUCION.txt`: salida real obtenida en esta sesión.
- `Informe_Fase4_Software_FJ.pdf`: documento grupal modelo; actualizar el enlace y los integrantes conforme al resultado autorizado.

## Ejemplos de polimorfismo y variaciones de costos
Los tres servicios implementan el mismo método `calcular_costo(duracion, descuento=0, impuesto=0)`, pero calculan el valor de manera diferente. En Python, los parámetros opcionales permiten variantes de llamada; no es sobrecarga por firma como en otros lenguajes.

## Repositorio personal de entrega propuesto
https://github.com/wilmeradrianrh/Software_FJ_Fase4_Programacion

El enlace es el destino de publicación indicado por el estudiante. **No confirma por sí mismo que el código haya sido subido**. Para que sea una evidencia válida, deben aparecer allí todos los archivos del proyecto. La aprobación de una entrega individual corresponde al tutor.

## Evidencias sugeridas para el foro
Capturar pantalla de `main.py`, `servicios.py`, `reservas.py`, `demostracion.py`, la terminal con las 16 operaciones, la terminal de pruebas con `OK` y `logs/software_fj.log`.

## Documentación y fuentes
- UNAD (2026). Guía del componente práctico, Fase 4.
- UNAD (2026). Anexo 3 - Problema a desarrollar Fase 4.
- Python Software Foundation. Documentación oficial del manejo de errores en Python: https://docs.python.org/es/3.12/tutorial/errors.html
- GitHub Docs: https://docs.github.com/es
