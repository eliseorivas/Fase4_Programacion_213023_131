"""Excepciones personalizadas y registro de eventos del sistema Software FJ."""

import logging
from pathlib import Path

RUTA_LOG = Path(__file__).resolve().parent / "logs" / "software_fj.log"
RUTA_LOG.parent.mkdir(parents=True, exist_ok=True)
logger = logging.getLogger("software_fj")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    manejador = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    manejador.setFormatter(logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    ))
    logger.addHandler(manejador)


class ErrorSistema(Exception):
    """Error base para la aplicación."""


class ErrorValidacion(ErrorSistema):
    """Datos inválidos o parámetros faltantes."""


class ClienteInvalidoError(ErrorValidacion):
    """Información inválida o duplicada de un cliente."""


class ServicioInvalidoError(ErrorValidacion):
    """Información inválida de un servicio."""


class ServicioNoDisponibleError(ErrorSistema):
    """El servicio está marcado como no disponible."""


class ReservaInvalidaError(ErrorSistema):
    """La reserva no puede crearse o cambiar de estado."""


class ErrorCalculoError(ErrorSistema):
    """Fallo al realizar un cálculo de costos."""


def ejecutar_controlado(nombre, funcion, *args, **kwargs):
    """Ejecuta sin terminar el programa y usa try/except/else/finally."""
    logger.info("INICIO: %s", nombre)
    try:
        resultado = funcion(*args, **kwargs)
    except ErrorSistema as error:
        logger.exception("ERROR CONTROLADO en %s: %s", nombre, error)
        print(f"[ERROR CONTROLADO] {nombre}: {error}")
        return None
    except Exception as error:
        logger.exception("ERROR IMPREVISTO en %s: %s", nombre, error)
        print(f"[ERROR IMPREVISTO] {nombre}: {type(error).__name__}")
        return None
    else:
        logger.info("OK: %s", nombre)
        print(f"[OK] {nombre}: {resultado}")
        return resultado
    finally:
        logger.info("FIN: %s", nombre)
