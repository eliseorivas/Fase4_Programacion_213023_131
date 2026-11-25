"""Pruebas automáticas: python -m unittest test_sistema.py -v"""

import math
import unittest
from contextlib import redirect_stdout
from io import StringIO
from decimal import Decimal
from entidades import Cliente
from excepciones import (
    ClienteInvalidoError, ErrorValidacion, ReservaInvalidaError,
    ServicioNoDisponibleError, ErrorSistema, RUTA_LOG, ejecutar_controlado
)
from servicios import ReservaSala, AlquilerEquipos, AsesoriaEspecializada, Servicio
from sistema import SistemaSoftwareFJ


class TestSistemaSoftwareFJ(unittest.TestCase):
    def setUp(self):
        self.sistema = SistemaSoftwareFJ()
        self.cliente = self.sistema.registrar_cliente("Ana Pérez", "123456789", "3001234567")
        self.sala = self.sistema.registrar_servicio(ReservaSala("Sala Azul", 8, 50000))

    def test_cliente_valido(self):
        self.assertEqual(self.cliente.obtener_nombre(), "Ana Pérez")

    def test_nombre_vacio(self):
        with self.assertRaises(ErrorValidacion):
            Cliente("", "123456789", "3001234567")

    def test_documento_con_letras(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Ana", "12AB", "3001234567")

    def test_telefono_invalido(self):
        with self.assertRaises(ClienteInvalidoError):
            Cliente("Ana", "123456789", "123")

    def test_cliente_duplicado(self):
        with self.assertRaises(ClienteInvalidoError):
            self.sistema.registrar_cliente("Otra Ana", "123456789", "3001234567")

    def test_abstraccion(self):
        with self.assertRaises(TypeError):
            Servicio("Servicio", 1000)

    def test_sala_polimorfismo(self):
        self.assertEqual(self.sala.calcular_costo(2), Decimal("100000.00"))

    def test_equipos_costo(self):
        equipo = AlquilerEquipos("Portátiles", 3, 15000)
        self.assertEqual(equipo.calcular_costo(2), Decimal("90000.00"))

    def test_asesoria_costo(self):
        consulta = AsesoriaEspecializada("Asesoría", "Python", 80000)
        self.assertEqual(consulta.calcular_costo(2), Decimal("160000.00"))

    def test_cantidad_equipo_invalida(self):
        with self.assertRaises(ErrorValidacion):
            AlquilerEquipos("PC", 0, 15000)

    def test_especialidad_vacia(self):
        with self.assertRaises(ErrorValidacion):
            AsesoriaEspecializada("Consulta", " ", 80000)

    def test_reserva_confirmar(self):
        reserva = self.sistema.crear_reserva(self.cliente, self.sala, 2)
        self.assertEqual(reserva.confirmar(), Decimal("100000.00"))
        self.assertEqual(reserva.estado, "confirmada")

    def test_reserva_duracion_negativa(self):
        with self.assertRaises(ErrorValidacion):
            self.sistema.crear_reserva(self.cliente, self.sala, -1)

    def test_no_disponible(self):
        reserva = self.sistema.crear_reserva(self.cliente, self.sala, 2)
        self.sala.actualizar_disponibilidad(False)
        with self.assertRaises(ServicioNoDisponibleError):
            reserva.confirmar()

    def test_descuento_e_impuesto(self):
        equipo = self.sistema.registrar_servicio(AlquilerEquipos("PC", 3, 15000))
        reserva = self.sistema.crear_reserva(self.cliente, equipo, 2)
        self.assertEqual(reserva.confirmar(10, 19), Decimal("96390.00"))

    def test_cancelar(self):
        reserva = self.sistema.crear_reserva(self.cliente, self.sala, 2)
        self.assertEqual(reserva.cancelar(), "cancelada")

    def test_doble_cancelacion(self):
        reserva = self.sistema.crear_reserva(self.cliente, self.sala, 2)
        reserva.cancelar()
        with self.assertRaises(ReservaInvalidaError):
            reserva.cancelar()

    def test_doble_confirmacion(self):
        reserva = self.sistema.crear_reserva(self.cliente, self.sala, 2)
        reserva.confirmar()
        with self.assertRaises(ReservaInvalidaError):
            reserva.confirmar()

    def test_porcentaje_invalido(self):
        with self.assertRaises(ErrorValidacion):
            self.sala.calcular_costo(2, descuento=101)

    def test_duracion_infinita(self):
        with self.assertRaises(ErrorValidacion):
            self.sistema.crear_reserva(self.cliente, self.sala, math.inf)

    def test_cliente_no_registrado(self):
        with self.assertRaises(ErrorValidacion):
            self.sistema.crear_reserva(Cliente("Pedro", "987654321", "3009876543"), self.sala, 1)

    def test_control_de_errores_continua(self):
        with redirect_stdout(StringIO()):
            self.assertIsNone(ejecutar_controlado("prueba fallida", lambda: 1/0))
        self.assertTrue(RUTA_LOG.exists())


if __name__ == "__main__":
    unittest.main()
