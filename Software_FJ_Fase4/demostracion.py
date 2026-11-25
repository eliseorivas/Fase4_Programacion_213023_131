"""Demostración automatizada con 16 operaciones válidas e inválidas.

Ejecutar: python demostracion.py
"""

from entidades import Cliente
from servicios import ReservaSala, AlquilerEquipos, AsesoriaEspecializada
from sistema import SistemaSoftwareFJ
from excepciones import ejecutar_controlado, RUTA_LOG, logger


def main():
    sistema = SistemaSoftwareFJ()
    print("=" * 66)
    print("SOFTWARE FJ - FASE 4 | DEMOSTRACIÓN DE OPERACIONES")
    print("=" * 66)
    cliente = ejecutar_controlado("01. Cliente válido", sistema.registrar_cliente,
                                  "Ana Pérez", "123456789", "3001234567")
    ejecutar_controlado("02. Cliente con nombre vacío", sistema.registrar_cliente,
                        "", "123456781", "3001234567")
    ejecutar_controlado("03. Documento con letras", sistema.registrar_cliente,
                        "José Ruiz", "AB12345", "3001234567")
    sala = ejecutar_controlado("04. Registrar sala válida", sistema.registrar_servicio,
                                ReservaSala("Sala de reuniones", 10, 50000))
    equipo = ejecutar_controlado("05. Registrar equipos válidos", sistema.registrar_servicio,
                                  AlquilerEquipos("Portátiles", 3, 15000))
    ejecutar_controlado("06. Equipos con cantidad inválida", AlquilerEquipos,
                        "Portátiles", 0, 15000)
    asesoria = ejecutar_controlado("07. Registrar asesoría válida", sistema.registrar_servicio,
                                    AsesoriaEspecializada("Asesoría Python", "Python", 80000))
    ejecutar_controlado("08. Asesoría con especialidad vacía", AsesoriaEspecializada,
                        "Asesoría", "", 80000)
    reserva_sala = ejecutar_controlado("09. Crear reserva de sala", sistema.crear_reserva,
                                       cliente, sala, 2)
    ejecutar_controlado("10. Confirmar reserva de sala", reserva_sala.confirmar)
    ejecutar_controlado("11. Duración negativa", sistema.crear_reserva,
                        cliente, sala, -2)
    sala.actualizar_disponibilidad(False)
    reserva_no_disp = sistema.crear_reserva(cliente, sala, 1)
    ejecutar_controlado("12. Servicio no disponible", reserva_no_disp.confirmar)
    reserva_equipo = sistema.crear_reserva(cliente, equipo, 2)
    ejecutar_controlado("13. Costo con descuento 10% e IVA 19%", reserva_equipo.confirmar,
                        10, 19)
    ejecutar_controlado("14. Cancelar reserva", reserva_equipo.cancelar)
    ejecutar_controlado("15. Cancelación repetida", reserva_equipo.cancelar)
    ejecutar_controlado("16. Cliente duplicado", sistema.registrar_cliente,
                        "Ana Pérez", "123456789", "3001234567")
    print("\nRESUMEN DEL SISTEMA")
    print(sistema.resumen())
    for item in sistema.reservas:
        print("  -", item.resumen())
    print("\nREGISTRO DE ERRORES Y EVENTOS:", RUTA_LOG)
    logger.info("Demostración completada con 16 operaciones numeradas.")


if __name__ == "__main__":
    main()
