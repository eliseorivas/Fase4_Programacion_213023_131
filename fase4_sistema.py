import tkinter as tk
from tkinter import messagebox

# CLASE CLIENTE
# Responsable: Eliseo Rivas Escobar
# Permite registrar y validar la información de los clientes.


class Cliente:

    def __init__(self, nombre, documento, telefono):

        # Validación del nombre
        if not nombre.strip():
            raise ValueError("El nombre del cliente no puede estar vacío.")

        # Validación del documento
        if not documento.strip():
            raise ValueError("El documento no puede estar vacío.")

        # Validación del teléfono
        if not telefono.strip():
            raise ValueError("El teléfono no puede estar vacío.")

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