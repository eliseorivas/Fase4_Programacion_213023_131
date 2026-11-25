"""Interfaz por consola para el Sistema Integral Software FJ.

Ejecutar: python main.py
Para operaciones de evaluación: python demostracion.py
"""

from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipos, AsesoriaEspecializada
from sistema import SistemaSoftwareFJ
from excepciones import ejecutar_controlado, logger


def leer_numero(texto, tipo=float):
    """Convierte entradas y deja que el controlador capture los errores."""
    return tipo(input(texto).strip())


def seleccionar(lista, etiqueta):
    if not lista:
        print(f"No hay {etiqueta} registrados.")
        return None
    for numero, elemento in enumerate(lista, 1):
        if isinstance(elemento, Cliente):
            descripcion = elemento.mostrar_informacion()
        elif hasattr(elemento, "describir"):
            descripcion = elemento.describir()
        else:
            descripcion = elemento.resumen()
        print(f"{numero}. {descripcion}")
    indice = leer_numero(f"Número de {etiqueta}: ", int)
    if indice < 1 or indice > len(lista):
        raise ValueError("El número seleccionado está fuera de rango.")
    return lista[indice - 1]


def registrar_cliente(sistema):
    nombre = input("Nombre: ")
    documento = input("Documento: ")
    telefono = input("Teléfono: ")
    return sistema.registrar_cliente(nombre, documento, telefono).mostrar_informacion()


def registrar_servicio(sistema):
    print("1. Sala | 2. Equipos | 3. Asesoría")
    clase = leer_numero("Tipo de servicio: ", int)
    nombre = input("Nombre del servicio: ")
    if clase == 1:
        servicio = ReservaSala(nombre, leer_numero("Capacidad: ", int),
                               leer_numero("Tarifa por hora: "))
    elif clase == 2:
        servicio = AlquilerEquipos(nombre, leer_numero("Cantidad: ", int),
                                   leer_numero("Tarifa por equipo/hora: "))
    elif clase == 3:
        servicio = AsesoriaEspecializada(nombre, input("Especialidad: "),
                                        leer_numero("Tarifa por hora: "))
    else:
        raise ValueError("El tipo de servicio no existe.")
    return sistema.registrar_servicio(servicio).describir()


def crear_reserva(sistema):
    cliente = seleccionar(sistema.clientes, "clientes")
    if cliente is None:
        return "Primero registre un cliente."
    servicio = seleccionar(sistema.servicios, "servicios")
    if servicio is None:
        return "Primero registre un servicio."
    reserva = sistema.crear_reserva(cliente, servicio, leer_numero("Duración (horas): "))
    return reserva.resumen()


def procesar_reserva(sistema, cancelar=False):
    reserva = seleccionar(sistema.reservas, "reservas")
    if reserva is None:
        return "Todavía no hay reservas."
    if cancelar:
        return reserva.cancelar()
    descuento = leer_numero("Descuento % (0 si no aplica): ")
    impuesto = leer_numero("IVA % (0 si no aplica): ")
    return f"Reserva confirmada: ${reserva.confirmar(descuento, impuesto)}"


def mostrar_listas(sistema):
    print(sistema.resumen())
    for cliente in sistema.clientes:
        print("CLIENTE:", cliente.mostrar_informacion())
    for servicio in sistema.servicios:
        print("SERVICIO:", servicio.describir())
    for reserva in sistema.reservas:
        print("RESERVA:", reserva.resumen())
    return "Consulta terminada"


def menu():
    sistema = SistemaSoftwareFJ()
    opciones = {
        "1": ("Registrar cliente", registrar_cliente),
        "2": ("Registrar servicio", registrar_servicio),
        "3": ("Crear reserva", crear_reserva),
        "4": ("Confirmar reserva", procesar_reserva),
        "5": ("Cancelar reserva", lambda s: procesar_reserva(s, True)),
        "6": ("Consultar registros", mostrar_listas),
    }
    while True:
        print("\n=== SOFTWARE FJ - MENÚ PRINCIPAL ===")
        for opcion, (titulo, _) in opciones.items():
            print(f"{opcion}. {titulo}")
        print("0. Salir")
        seleccion = input("Elige una opción: ").strip()
        if seleccion == "0":
            logger.info("El usuario salió del programa.")
            print("Programa finalizado correctamente.")
            break
        if seleccion not in opciones:
            print("Opción inválida. Intenta de nuevo.")
            continue
        nombre, funcion = opciones[seleccion]
        ejecutar_controlado(nombre, funcion, sistema)


if __name__ == "__main__":
    try:
        menu()
    except (KeyboardInterrupt, EOFError):
        print("\nSesión cerrada.")
