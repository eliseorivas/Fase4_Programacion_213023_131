"""Abstracción principal y entidad Cliente con información encapsulada."""

from abc import ABC, abstractmethod
from uuid import uuid4
from excepciones import logger
from validaciones import validar_texto, validar_documento, validar_telefono


class Entidad(ABC):
    """Interfaz abstracta común a clientes y servicios."""

    def __init__(self):
        self._codigo = uuid4().hex[:8].upper()

    @property
    def codigo(self):
        return self._codigo

    @abstractmethod
    def mostrar_informacion(self):
        """Devuelve una representación legible de la entidad."""


class Cliente(Entidad):
    """Registra un cliente; no permite modificar directamente sus datos."""

    def __init__(self, nombre, documento, telefono):
        super().__init__()
        self.__nombre = validar_texto(nombre, "Nombre")
        self.__documento = validar_documento(documento)
        self.__telefono = validar_telefono(telefono)
        logger.info("Cliente creado: %s", self.__documento)

    def obtener_nombre(self):
        return self.__nombre

    def obtener_documento(self):
        return self.__documento

    def obtener_telefono(self):
        return self.__telefono

    def mostrar_informacion(self):
        return f"{self.__nombre} | CC {self.__documento} | Tel. {self.__telefono}"

    def __str__(self):
        return self.mostrar_informacion()
