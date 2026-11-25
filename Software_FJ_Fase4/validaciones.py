"""Funciones reutilizables de validación para clientes, servicios y reservas."""

from decimal import Decimal, InvalidOperation
from math import isfinite
from excepciones import ErrorValidacion, ClienteInvalidoError


def validar_texto(valor, campo):
    if not isinstance(valor, str) or not valor.strip():
        raise ErrorValidacion(f"{campo} debe ser texto y no puede estar vacío.")
    return valor.strip()


def validar_documento(valor):
    texto = validar_texto(valor, "Documento")
    if not texto.isdigit() or not 5 <= len(texto) <= 15:
        raise ClienteInvalidoError("El documento debe contener entre 5 y 15 dígitos.")
    return texto


def validar_telefono(valor):
    texto = validar_texto(valor, "Teléfono")
    if not texto.isdigit() or len(texto) != 10:
        raise ClienteInvalidoError("El teléfono debe contener 10 dígitos numéricos.")
    return texto


def validar_entero_positivo(valor, campo):
    if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
        raise ErrorValidacion(f"{campo} debe ser un entero positivo.")
    return valor


def validar_numero(valor, campo, *, permite_cero=False):
    if isinstance(valor, bool) or not isinstance(valor, (int, float, Decimal)):
        raise ErrorValidacion(f"{campo} debe ser numérico.")
    if isinstance(valor, float) and not isfinite(valor):
        raise ErrorValidacion(f"{campo} debe ser un número finito.")
    try:
        numero = Decimal(str(valor))
    except (InvalidOperation, ValueError) as exc:
        raise ErrorValidacion(f"{campo} no es un número válido.") from exc
    if not numero.is_finite() or numero < 0 or (numero == 0 and not permite_cero):
        regla = "no negativo" if permite_cero else "mayor que cero"
        raise ErrorValidacion(f"{campo} debe ser {regla} y finito.")
    return numero


def validar_porcentaje(valor, campo):
    numero = validar_numero(valor, campo, permite_cero=True)
    if numero > 100:
        raise ErrorValidacion(f"{campo} no puede superar el 100%.")
    return numero
