from fase4_sistema import Cliente

from Servicio import (
    ReservaSala,
    AlquilerEquipo,
    AsesoriaEspecializada
)

from reserva import Reserva, ReservaError

from aporte4_excepciones_validaciones import (
    ejecutar_operacion,
    validar_documento,
    validar_telefono
)

def ejecutar_sistema():

    print("========================================")
    print(" SISTEMA INTEGRADO - SOFTWARE FJ")
    print("========================================")

    # Registrar cliente 
    print("\n--- 1. REGISTRO DEL CLIENTE ---")

    cliente = Cliente(
        "Eliseo Rivas",
        "123456789",
        "3001234567"
    )

    print(cliente.mostrar_informacion())

    # Crea los servicios
    print("\n--- 2. SERVICIOS DISPONIBLES ---")

    sala = ReservaSala("Sala Bogota", 20, 50000)

    equipos = AlquilerEquipo(
        "Computadores",
        3,
        15000
    )

    asesoria = AsesoriaEspecializada(
        "Asesoria empresarial",
        "Administracion",
        80000
    )

    servicios = [sala, equipos, asesoria]

    for servicio in servicios:
        print(servicio.describir())

    # Crea una reserva
    print("\n--- 3. CREACION DE RESERVA ---")

    reserva = Reserva(
        "R001",
        cliente,
        sala,
        "2026-11-25",
        2
    )

    print(reserva.mostrar_informacion())
    print("Disponible:", reserva.esta_disponible())
    print(f"Costo inicial: ${reserva.calcular_total():,.0f}")

        # Calcula descuento e impuesto
    print("\n--- 4. DESCUENTO E IMPUESTO ---")

    total = reserva.calcular_total(
        impuesto=0.19,
        descuento=0.10
    )

    print(f"Total con descuento e impuesto: ${total:,.0f}")

    # Cambia el estado de la reserva
    print("\n--- 5. ESTADO DE LA RESERVA ---")

    reserva.confirmar()
    print("Estado:", reserva.estado)

    reserva.finalizar()
    print("Estado:", reserva.estado)

    print("Disponible:", reserva.esta_disponible())


        # Valida los datos del cliente
    print("\n--- 6. VALIDACIONES ---")

    ejecutar_operacion(
        "Documento valido",
        validar_documento,
        cliente.obtener_documento()
    )

    ejecutar_operacion(
        "Telefono valido",
        validar_telefono,
        cliente.obtener_telefono()
    )

    # Prueba un error controlado
    print("\n--- 7. ERROR CONTROLADO ---")

    try:
        Reserva(
            "R002",
            cliente,
            sala,
            "2026-11-26",
            0
        )

    except ReservaError as error:
        print("Error controlado:", error)

    # Inicia el sistema
if __name__ == "__main__":
    ejecutar_sistema()