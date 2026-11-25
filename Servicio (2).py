
from abc import ABC, abstractmethod
import math


# =====================================================
# 1. EXCEPCION PERSONALIZADA
# =====================================================

class ServicioError(Exception):
    """Errores relacionados con la gestion de servicios."""
    pass


# =====================================================
# 2. CLASE ABSTRACTA SERVICIO
# =====================================================

class Servicio(ABC):
    """
    Clase padre de todos los servicios de Software FJ.
    Define las caracteristicas y metodos comunes.
    """

    def __init__(self, nombre, tarifa_hora):

        # Validar el nombre
        if not isinstance(nombre, str) or not nombre.strip():
            raise ServicioError(
                "El nombre del servicio no puede estar vacio."
            )

        # Validar la tarifa
        if (isinstance(tarifa_hora, bool)
                or not isinstance(tarifa_hora, (int, float))
                or not math.isfinite(tarifa_hora)
                or tarifa_hora <= 0):
            raise ServicioError(
                "La tarifa por hora debe ser un numero mayor que cero."
            )

        # Encapsulamiento
        self._nombre = nombre.strip()
        self._tarifa_hora = tarifa_hora

    # Propiedades para consultar los atributos

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    # Validacion de horas

    def validar_horas(self, horas):

        if (isinstance(horas, bool)
                or not isinstance(horas, (int, float))
                or not math.isfinite(horas)):
            raise ServicioError(
                "Las horas deben ser un numero valido."
            )

        if horas <= 0:
            raise ServicioError(
                "Las horas deben ser mayores que cero."
            )

    # Validacion de impuestos y descuentos

    def validar_porcentaje(self, porcentaje, nombre):

        if (isinstance(porcentaje, bool)
                or not isinstance(porcentaje, (int, float))
                or not math.isfinite(porcentaje)
                or porcentaje < 0
                or porcentaje > 1):
            raise ServicioError(
                f"El {nombre} debe estar entre 0 y 1."
            )

    # Metodo comun para calcular el costo

    def calcular_total(self, horas, impuesto=0.0, descuento=0.0):

        self.validar_horas(horas)
        self.validar_porcentaje(impuesto, "impuesto")
        self.validar_porcentaje(descuento, "descuento")

        subtotal = self._tarifa_hora * horas

        valor_descuento = subtotal * descuento
        subtotal -= valor_descuento

        valor_impuesto = subtotal * impuesto
        total = subtotal + valor_impuesto

        if not math.isfinite(total):
            raise ServicioError("El costo final del servicio no es un valor finito.")

        return total

    # Metodos abstractos

    @abstractmethod
    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):
        pass

    @abstractmethod
    def describir(self):
        pass


# =====================================================
# 3. SERVICIO ESPECIALIZADO: RESERVA DE SALAS
# =====================================================

class ReservaSala(Servicio):
    """Servicio de alquiler y reserva de salas."""

    def __init__(self, nombre, capacidad, tarifa_hora):

        super().__init__(nombre, tarifa_hora)

        if (isinstance(capacidad, bool)
                or not isinstance(capacidad, int)
                or capacidad <= 0):
            raise ServicioError(
                "La capacidad debe ser un entero mayor que cero."
            )

        self._capacidad = capacidad

    @property
    def capacidad(self):
        return self._capacidad

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):

        return self.calcular_total(horas, impuesto, descuento)

    def describir(self):

        return (
            f"Reserva de sala: {self._nombre} | "
            f"Capacidad: {self._capacidad} personas | "
            f"Tarifa: ${self._tarifa_hora:,.0f} por hora"
        )


# =====================================================
# 4. SERVICIO ESPECIALIZADO: ALQUILER DE EQUIPOS
# =====================================================

class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos tecnologicos."""

    def __init__(self, nombre, cantidad, tarifa_hora):

        super().__init__(nombre, tarifa_hora)

        if (isinstance(cantidad, bool)
                or not isinstance(cantidad, int)
                or cantidad <= 0):
            raise ServicioError(
                "La cantidad de equipos debe ser un entero positivo."
            )

        self._cantidad = cantidad

    @property
    def cantidad(self):
        return self._cantidad

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):

        costo_unitario = self.calcular_total(
            horas, impuesto, descuento
        )

        costo_total = costo_unitario * self._cantidad

        if not math.isfinite(costo_total):
         raise ServicioError("El costo final del alquiler de equipos no es un valor finito.")

        return costo_total  

    def describir(self):

        return (
            f"Alquiler de equipos: {self._nombre} | "
            f"Cantidad: {self._cantidad} | "
            f"Tarifa: ${self._tarifa_hora:,.0f} por hora y equipo"
        )


# =====================================================
# 5. SERVICIO ESPECIALIZADO: ASESORIAS
# =====================================================

class AsesoriaEspecializada(Servicio):
    """Servicio de asesorias profesionales."""

    def __init__(self, nombre, especialidad, tarifa_hora):

        super().__init__(nombre, tarifa_hora)

        if (not isinstance(especialidad, str)
                or not especialidad.strip()):
            raise ServicioError(
                "La especialidad no puede estar vacia."
            )

        self._especialidad = especialidad.strip()

    @property
    def especialidad(self):
        return self._especialidad

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0):

        return self.calcular_total(horas, impuesto, descuento)

    def describir(self):

        return (
            f"Asesoria: {self._nombre} | "
            f"Especialidad: {self._especialidad} | "
            f"Tarifa: ${self._tarifa_hora:,.0f} por hora"
        )


# =====================================================
# 6. FUNCION PARA REALIZAR LAS PRUEBAS
# =====================================================

def ejecutar_pruebas():

    print("\n========================================")
    print(" SISTEMA DE SERVICIOS - SOFTWARE FJ")
    print("========================================")

    # Crear servicios validos

    try:

        sala = ReservaSala("Sala Bogota", 20, 50000)

        equipo = AlquilerEquipo("Computadores", 3, 15000)

        asesoria = AsesoriaEspecializada(
            "Asesoria empresarial",
            "Administracion",
            80000
        )

        servicios = [sala, equipo, asesoria]

        # Pruebas de polimorfismo

        print("\n--- SERVICIOS REGISTRADOS ---")

        for servicio in servicios:

            print("\n" + servicio.describir())

            costo = servicio.calcular_costo(2)

            print(f"Costo por 2 horas: ${costo:,.0f}")

        # Prueba con impuesto y descuento

        print("\n--- PRUEBA DE DESCUENTO E IMPUESTO ---")

        total = sala.calcular_costo(
            2,
            impuesto=0.19,
            descuento=0.10
        )

        print(f"Total con descuento e impuesto: ${total:,.0f}")

    except ServicioError as error:

        print("Error al crear o calcular servicios:", error)

    # Pruebas de horas incorrectas

    print("\n--- PRUEBAS DE HORAS INVALIDAS ---")

    for horas in (0, -2, "abc"):

        try:

            sala.calcular_costo(horas)

        except ServicioError as error:

            print(f"Prueba con horas {horas}: {error}")

    # Prueba de tarifa incorrecta

    print("\n--- PRUEBA DE TARIFA INVALIDA ---")

    try:

        ReservaSala("Sala de prueba", 10, -50000)

    except ServicioError as error:

        print("Error controlado:", error)

    # Prueba de capacidad incorrecta

    print("\n--- PRUEBA DE CAPACIDAD INVALIDA ---")

    try:

        ReservaSala("Sala de prueba", 0, 50000)

    except ServicioError as error:

        print("Error controlado:", error)

    # Prueba de descuento incorrecto

    print("\n--- PRUEBA DE DESCUENTO INVALIDO ---")

    try:

        sala.calcular_costo(2, descuento=1.5)

    except ServicioError as error:

        print("Error controlado:", error)

    print("\n========================================")
    print(" FIN DE LAS PRUEBAS")
    print(" El programa continua funcionando.")
    print("========================================")


# =====================================================
# 7. EJECUCION PRINCIPAL
# =====================================================

if __name__ == "__main__":

    ejecutar_pruebas()


    # PRUEBA 1: Nombre del servicio vacio

    print("\n--- PRUEBA DE NOMBRE VACIO ---")

    try:
        ReservaSala("   ", 10, 50000)

    except ServicioError as error:
        print("Error controlado:", error)


    # PRUEBA 2: Cantidad de equipos igual a cero

    print("\n--- PRUEBA DE CANTIDAD DE EQUIPOS ---")

    try:
        AlquilerEquipo("Computadores", 0, 15000)

    except ServicioError as error:
        print("Error controlado:", error)


    # PRUEBA 3: Especialidad vacia

    print("\n--- PRUEBA DE ESPECIALIDAD VACIA ---")

    try:
        AsesoriaEspecializada(
            "Asesoria empresarial",
            "   ",
            80000
        )

    except ServicioError as error:
        print("Error controlado:", error)
        
    # PRUEBA 4: Resultado no finito por valores muy grandes
print("\n--- PRUEBA DE RESULTADO NO FINITO ---")

try:
    equipo_grande = AlquilerEquipo("Computadores", 10**200, 1e200)
    print(equipo_grande.calcular_costo(2))
except ServicioError as error:
    print("Error controlado:", error)