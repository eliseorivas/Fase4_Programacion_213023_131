import tkinter as tk
from tkinter import messagebox

# CLASE CLIENTE
# Responsable: Eliseo Rivas Escobar
# Permite registrar y validar la información de los clientes.


class Cliente:

    def __init__(self, nombre, documento, telefono):

        # Validación del nombre
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre del cliente debe ser un texto válido y no puede estar vacío")

        # Validación del documento
        if not isinstance(documento, str) or not documento.strip():
            raise ValueError("El documento debe ser un texto válido y no puede estar vacío.")

        # Validación del teléfono
        if not isinstance(telefono, str) or not telefono.strip():
            raise ValueError("El teléfono debe ser un texto válido y no puede estar vacío.")

        # Encapsulación de los datos del cliente
        self.__nombre = nombre
        self.__documento = documento
        self.__telefono = telefono

    # Devuelve el nombre del cliente
    def obtener_nombre(self):
        return self.__nombre

    # Devuelve el documento del cliente
    def obtener_documento(self):
        return self.__documento

    # Devuelve el teléfono del cliente
    def obtener_telefono(self):
        return self.__telefono

    # Muestra la información del cliente
    def mostrar_informacion(self):
        return (
            f"Cliente: {self.__nombre} - "
            f"Documento: {self.__documento} - "
            f"Teléfono: {self.__telefono}"
        )

    # PRUEBA 1: Cliente con datos válidos
try:
    cliente1 = Cliente("Eliseo Rivas", "123456789", "3001234567")
    print(cliente1.mostrar_informacion())
except ValueError as error:
    print("Error:", error)