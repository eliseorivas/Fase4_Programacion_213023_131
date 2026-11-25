"""Fachada que mantiene los datos en listas de objetos, sin base de datos."""

from entidades import Cliente
from servicios import Servicio
from reservas import Reserva
from excepciones import ClienteInvalidoError, ErrorValidacion, logger


class SistemaSoftwareFJ:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []

    def registrar_cliente(self, nombre, documento, telefono):
        cliente = Cliente(nombre, documento, telefono)
        if any(c.obtener_documento() == cliente.obtener_documento() for c in self.clientes):
            raise ClienteInvalidoError("Ya existe un cliente con ese documento.")
        self.clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.obtener_documento())
        return cliente

    def registrar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ErrorValidacion("Solo se pueden registrar servicios válidos.")
        self.servicios.append(servicio)
        logger.info("Servicio registrado: %s", servicio.nombre)
        return servicio

    def crear_reserva(self, cliente, servicio, duracion):
        if cliente not in self.clientes:
            raise ErrorValidacion("El cliente no está registrado en el sistema.")
        if servicio not in self.servicios:
            raise ErrorValidacion("El servicio no está registrado en el sistema.")
        reserva = Reserva(cliente, servicio, duracion)
        self.reservas.append(reserva)
        return reserva

    def resumen(self):
        return (f"Clientes: {len(self.clientes)} | Servicios: {len(self.servicios)} | "
                f"Reservas: {len(self.reservas)}")
