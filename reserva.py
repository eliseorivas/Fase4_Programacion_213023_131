
# CLASE RESERVA
# Aporte asignado: Samuel
# Apoyo para integración: equipo de trabajo
# Fase 4 - Programación 213023



from datetime import datetime


class ReservaError(Exception):
    """Error controlado relacionado con una reserva."""
    pass


class Reserva:
    """Relaciona un cliente con un servicio y controla el estado de la reserva."""

    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "CANCELADA", "FINALIZADA")

    def __init__(self, codigo, cliente, servicio, fecha, horas):
        if not isinstance(codigo, str) or not codigo.strip():
            raise ReservaError("El codigo de la reserva no puede estar vacio.")

        # Compatibilidad con la clase Cliente de fase4_sistema.py
        metodos_cliente = (
            "obtener_nombre",
            "obtener_documento",
            "obtener_telefono",
        )
        if cliente is None or not all(
            callable(getattr(cliente, metodo, None))
            for metodo in metodos_cliente
        ):
            raise ReservaError("El cliente de la reserva no es valido.")

        # Compatibilidad con las clases de Servicio de Lina
        if (servicio is None
                or not callable(getattr(servicio, "calcular_costo", None))
                or not callable(getattr(servicio, "describir", None))):
            raise ReservaError("El servicio de la reserva no es valido.")

        if not isinstance(fecha, str) or not fecha.strip():
            raise ReservaError("La fecha de la reserva no puede estar vacia.")

        try:
            datetime.strptime(fecha.strip(), "%Y-%m-%d")
        except ValueError as error:
            raise ReservaError(
                "La fecha debe tener el formato AAAA-MM-DD."
            ) from error

        if (isinstance(horas, bool)
                or not isinstance(horas, (int, float))
                or horas <= 0):
            raise ReservaError("Las horas deben ser un numero mayor que cero.")

        # El propio servicio realiza sus validaciones adicionales.
        try:
            servicio.calcular_costo(horas)
        except Exception as error:
            raise ReservaError(
                "No fue posible validar el servicio para la reserva."
            ) from error

        self._codigo = codigo.strip()
        self._cliente = cliente
        self._servicio = servicio
        self._fecha = fecha.strip()
        self._horas = horas
        self._estado = "PENDIENTE"

    @property
    def codigo(self):
        return self._codigo

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def fecha(self):
        return self._fecha

    @property
    def horas(self):
        return self._horas

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        if self._estado != "PENDIENTE":
            raise ReservaError(
                "Solo una reserva pendiente puede ser confirmada."
            )
        self._estado = "CONFIRMADA"

    def cancelar(self):
        if self._estado in ("CANCELADA", "FINALIZADA"):
            raise ReservaError(
                "La reserva no puede cancelarse en su estado actual."
            )
        self._estado = "CANCELADA"

    def finalizar(self):
        if self._estado != "CONFIRMADA":
            raise ReservaError(
                "Solo una reserva confirmada puede finalizarse."
            )
        self._estado = "FINALIZADA"

    def esta_disponible(self):
        """Indica si la reserva sigue activa y disponible para procesarse."""
        return self._estado in ("PENDIENTE", "CONFIRMADA")

    def calcular_total(self, impuesto=0.0, descuento=0.0):
        try:
            return self._servicio.calcular_costo(
                self._horas,
                impuesto=impuesto,
                descuento=descuento,
            )
        except Exception as error:
            raise ReservaError(
                "No fue posible calcular el costo de la reserva."
            ) from error

    def mostrar_informacion(self):
        return (
            f"Reserva: {self._codigo} | "
            f"Cliente: {self._cliente.obtener_nombre()} | "
            f"Servicio: {self._servicio.nombre} | "
            f"Fecha: {self._fecha} | "
            f"Horas: {self._horas} | "
            f"Estado: {self._estado}"
        )


if __name__ == "__main__":
    print("Clase Reserva cargada correctamente.")
    print("Lista para integrarse con Cliente y Servicio.")
