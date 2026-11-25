"""Administración de reservas, transiciones de estado y manejo de errores."""

from decimal import Decimal
from entidades import Cliente
from excepciones import (
    ErrorSistema, ErrorCalculoError, ReservaInvalidaError,
    ServicioNoDisponibleError, logger
)
from servicios import Servicio
from validaciones import validar_numero, validar_porcentaje
from uuid import uuid4


class Reserva:
    """Relaciona Cliente + Servicio + duración + estado, sin base de datos."""

    def __init__(self, cliente, servicio, duracion):
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un objeto Cliente.")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un objeto Servicio.")
        self.__duracion = validar_numero(duracion, "Duración")
        self.__cliente = cliente
        self.__servicio = servicio
        self.__estado = "pendiente"
        self.__costo = Decimal("0.00")
        self.__codigo = "RES-" + uuid4().hex[:8].upper()
        logger.info("Reserva creada: %s", self.__codigo)

    @property
    def codigo(self):
        return self.__codigo

    @property
    def estado(self):
        return self.__estado

    @property
    def costo(self):
        return self.__costo

    def procesar(self, descuento=0, impuesto=0):
        """Valida disponibilidad y calcula costo con excepción encadenada."""
        if self.__estado == "cancelada":
            raise ReservaInvalidaError("Una reserva cancelada no puede procesarse.")
        if not self.__servicio.disponible:
            raise ServicioNoDisponibleError("El servicio no está disponible.")
        # Se realizan validaciones incluso si el costo se calcula de nuevo.
        validar_porcentaje(descuento, "Descuento")
        validar_porcentaje(impuesto, "Impuesto")
        try:
            resultado = self.__servicio.calcular_costo(
                self.__duracion, descuento=descuento, impuesto=impuesto
            )
            self.__costo = validar_numero(resultado, "Costo", permite_cero=True)
        except ErrorSistema:
            raise
        except Exception as error:
            logger.exception("Error interno de cálculo: %s", self.__codigo)
            raise ErrorCalculoError("No se pudo calcular la reserva.") from error
        else:
            logger.info("Reserva %s procesada: %s", self.__codigo, self.__costo)
            return self.__costo
        finally:
            logger.info("Finalizó intento de procesamiento de %s", self.__codigo)

    def confirmar(self, descuento=0, impuesto=0):
        if self.__estado != "pendiente":
            raise ReservaInvalidaError(f"No se puede confirmar una reserva {self.__estado}.")
        total = self.procesar(descuento, impuesto)
        self.__estado = "confirmada"
        logger.info("Reserva confirmada: %s", self.__codigo)
        return total

    def cancelar(self):
        if self.__estado == "cancelada":
            raise ReservaInvalidaError("La reserva ya está cancelada.")
        self.__estado = "cancelada"
        logger.info("Reserva cancelada: %s", self.__codigo)
        return self.__estado

    def resumen(self):
        return (f"{self.__codigo} | {self.__cliente.obtener_nombre()} | "
                f"{self.__servicio.nombre} | {self.__duracion} h | "
                f"{self.__estado} | ${self.__costo}")

    def __str__(self):
        return self.resumen()
