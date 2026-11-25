"""Clase abstracta Servicio y tres servicios con herencia/polimorfismo."""

from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_UP
from entidades import Entidad
from excepciones import logger
from validaciones import (
    validar_entero_positivo, validar_numero, validar_porcentaje, validar_texto
)


class Servicio(Entidad, ABC):
    """Cada subclase sobrescribe descripción, validación y cálculo."""

    def __init__(self, nombre, tarifa_hora, disponible=True):
        super().__init__()
        self._nombre = validar_texto(nombre, "Nombre del servicio")
        self._tarifa_hora = validar_numero(tarifa_hora, "Tarifa por hora")
        if not isinstance(disponible, bool):
            raise ValueError("La disponibilidad debe ser True o False.")
        self._disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def disponible(self):
        return self._disponible

    def actualizar_disponibilidad(self, estado):
        if not isinstance(estado, bool):
            raise ValueError("La disponibilidad debe ser True o False.")
        self._disponible = estado
        logger.info("Disponibilidad de %s: %s", self.nombre, estado)

    def mostrar_informacion(self):
        return self.describir()

    def __str__(self):
        return self.describir()

    def _ajustar_precio(self, subtotal, descuento=0, impuesto=0):
        """Admite variantes con argumentos opcionales (descuento/IVA)."""
        rebaja = validar_porcentaje(descuento, "Descuento")
        iva = validar_porcentaje(impuesto, "Impuesto")
        total = subtotal * (Decimal("1") - rebaja / 100)
        total *= Decimal("1") + iva / 100
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @abstractmethod
    def validar_parametros(self):
        """Verifica parámetros particulares del servicio."""

    @abstractmethod
    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        """Devuelve el costo en pesos colombianos (Decimal)."""

    @abstractmethod
    def describir(self):
        """Describe el servicio y sus características."""


class ReservaSala(Servicio):
    """Reserva de un espacio por horas."""

    def __init__(self, nombre, capacidad, tarifa_hora, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        self.capacidad = capacidad
        self.validar_parametros()

    def validar_parametros(self):
        validar_entero_positivo(self.capacidad, "Capacidad")
        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        horas = validar_numero(duracion, "Duración")
        return self._ajustar_precio(self._tarifa_hora * horas, descuento, impuesto)

    def describir(self):
        return f"Sala: {self.nombre}; aforo: {self.capacidad}; ${self._tarifa_hora}/hora"


class AlquilerEquipos(Servicio):
    """Alquiler de un conjunto de equipos por horas."""

    def __init__(self, nombre, cantidad, tarifa_equipo_hora, disponible=True):
        super().__init__(nombre, tarifa_equipo_hora, disponible)
        self.cantidad = cantidad
        self.validar_parametros()

    def validar_parametros(self):
        validar_entero_positivo(self.cantidad, "Cantidad de equipos")
        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        horas = validar_numero(duracion, "Duración")
        base = self._tarifa_hora * self.cantidad * horas
        return self._ajustar_precio(base, descuento, impuesto)

    def describir(self):
        return f"Equipos: {self.nombre}; cantidad: {self.cantidad}; ${self._tarifa_hora}/equipo/hora"


class AsesoriaEspecializada(Servicio):
    """Servicio profesional de asesoría por horas."""

    def __init__(self, nombre, especialidad, tarifa_hora, disponible=True):
        super().__init__(nombre, tarifa_hora, disponible)
        self.especialidad = especialidad
        self.validar_parametros()

    def validar_parametros(self):
        self.especialidad = validar_texto(self.especialidad, "Especialidad")
        return True

    def calcular_costo(self, duracion, descuento=0, impuesto=0):
        horas = validar_numero(duracion, "Duración")
        return self._ajustar_precio(self._tarifa_hora * horas, descuento, impuesto)

    def describir(self):
        return f"Asesoría: {self.nombre}; especialidad: {self.especialidad}; ${self._tarifa_hora}/hora"
