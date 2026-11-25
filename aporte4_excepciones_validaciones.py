"""Aporte 4 - Manejo de excepciones y validaciones.

Proyecto: Sistema Integral de Gestión de Clientes, Servicios y Reservas
Grupo: Fase4_Programacion_213023_131
Responsable del aporte: Luis Abel Esquivel Pacheco

Este módulo reúne excepciones personalizadas, validaciones reutilizables,
registro de eventos/errores y ejecución controlada de operaciones.
Puede integrarse desde fase4_sistema.py mediante importaciones.
"""

import logging
from pathlib import Path


# ----------------------------------------------------------------------
# Registro de eventos y errores
# ----------------------------------------------------------------------

RUTA_LOG = Path(__file__).with_name("software_fj.log")
logger = logging.getLogger("software_fj")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    formato = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    manejador.setFormatter(formato)
    logger.addHandler(manejador)


# ----------------------------------------------------------------------
# Excepciones personalizadas del sistema
# ----------------------------------------------------------------------

class ErrorSistema(Exception):
    """Clase base para los errores controlados del sistema Software FJ."""


class ErrorValidacion(ErrorSistema):
    """Se genera cuando un dato no cumple las reglas de validación."""


class ClienteInvalidoError(ErrorValidacion):
    """Se genera cuando la información de un cliente es incorrecta."""


class ServicioInvalidoError(ErrorValidacion):
    """Se genera cuando la información de un servicio es incorrecta."""


class ReservaInvalidaError(ErrorSistema):
    """Se genera cuando no se puede crear o procesar una reserva."""


class ServicioNoDisponibleError(ErrorSistema):
    """Se genera cuando se intenta reservar un servicio no disponible."""


# ----------------------------------------------------------------------
# Funciones de validación reutilizables
# ----------------------------------------------------------------------

def validar_texto(valor, nombre_campo):
    """Comprueba que el campo sea texto y que no esté vacío."""
    if not isinstance(valor, str) or not valor.strip():
        raise ErrorValidacion(
            f"El campo '{nombre_campo}' debe ser texto y no puede estar vacío."
        )
    return valor.strip()


def validar_documento(documento):
    """Comprueba que el documento contenga únicamente números."""
    documento = validar_texto(documento, "documento")
    if not documento.isdigit():
        raise ClienteInvalidoError("El documento debe contener solo números.")
    return documento


def validar_telefono(telefono):
    """Comprueba que el teléfono tenga exactamente diez dígitos."""
    telefono = validar_texto(telefono, "teléfono")
    if not telefono.isdigit() or len(telefono) != 10:
        raise ClienteInvalidoError(
            "El teléfono debe contener exactamente 10 dígitos numéricos."
        )
    return telefono


def validar_duracion(duracion):
    """Comprueba que la duración sea un número positivo."""
    if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
        raise ErrorValidacion("La duración debe ser un número.")
    if duracion <= 0:
        raise ErrorValidacion("La duración debe ser mayor que cero.")
    return duracion


def validar_costo(costo):
    """Comprueba que el costo sea numérico y no negativo."""
    if isinstance(costo, bool) or not isinstance(costo, (int, float)):
        raise ServicioInvalidoError("El costo debe ser un valor numérico.")
    if costo < 0:
        raise ServicioInvalidoError("El costo no puede ser negativo.")
    return costo


def validar_reserva(cliente, servicio, duracion):
    """Valida los datos mínimos para una reserva.

    El encadenamiento 'raise ... from error' conserva la causa original
    del problema para facilitar su diagnóstico.
    """
    try:
        validar_texto(cliente, "cliente")
        validar_texto(servicio, "servicio")
        validar_duracion(duracion)
    except ErrorSistema as error:
        logger.exception("Falló la validación de una reserva.")
        raise ReservaInvalidaError(
            "No fue posible crear la reserva debido a datos incorrectos."
        ) from error

    logger.info("Validación de reserva realizada correctamente.")
    return True


# ----------------------------------------------------------------------
# Ejecución controlada: try / except / else / finally
# ----------------------------------------------------------------------

def ejecutar_operacion(nombre, funcion, *args, **kwargs):
    """Ejecuta una operación sin detener el programa ante errores previstos."""
    logger.info("Inicio de la operación: %s", nombre)
    try:
        resultado = funcion(*args, **kwargs)
    except ErrorSistema as error:
        logger.exception("Error controlado en '%s': %s", nombre, error)
        print(f"[ERROR CONTROLADO] {nombre}: {error}")
        return None
    except Exception as error:
        # Se conserva la excepción original como causa del error del sistema.
        logger.exception("Error inesperado en '%s'.", nombre)
        error_controlado = ErrorSistema(
            f"Ocurrió un error inesperado durante la operación '{nombre}'."
        )
        error_controlado.__cause__ = error
        print(f"[ERROR INESPERADO] {nombre}: {error_controlado}")
        return None
    else:
        logger.info("Operación '%s' finalizada correctamente.", nombre)
        print(f"[OK] {nombre}: {resultado}")
        return resultado
    finally:
        logger.info("Finalización del intento de operación: %s", nombre)


# ----------------------------------------------------------------------
# Pruebas del aporte 4 (casos válidos e inválidos)
# ----------------------------------------------------------------------

def ejecutar_pruebas():
    """Ejecuta diez validaciones y un caso adicional de reserva."""
    pruebas = [
        ("1. Nombre válido", validar_texto, ("Ana Pérez", "nombre")),
        ("2. Nombre vacío", validar_texto, ("   ", "nombre")),
        ("3. Documento válido", validar_documento, ("123456789",)),
        ("4. Documento con letras", validar_documento, ("12AB56",)),
        ("5. Teléfono válido", validar_telefono, ("3001234567",)),
        ("6. Teléfono incompleto", validar_telefono, ("300123",)),
        ("7. Duración válida", validar_duracion, (2,)),
        ("8. Duración cero", validar_duracion, (0,)),
        ("9. Costo válido", validar_costo, (150000,)),
        ("10. Costo negativo", validar_costo, (-5000,)),
    ]

    for nombre, funcion, argumentos in pruebas:
        ejecutar_operacion(nombre, funcion, *argumentos)

    # Caso adicional para demostrar excepciones encadenadas.
    ejecutar_operacion(
        "11. Reserva con duración inválida",
        validar_reserva,
        "Ana Pérez",
        "Sala de reuniones",
        0,
    )


if __name__ == "__main__":
    print("PRUEBAS DEL APORTE 4 - EXCEPCIONES Y VALIDACIONES")
    ejecutar_pruebas()
    print(f"\nLos eventos y errores se registraron en: {RUTA_LOG}")
