import tkinter as tk
from tkinter import font, ttk
from enum import Enum


class ColorPalette(Enum):
    """
    Paleta de colores estándar para el sistema.
    """
    FONDO = "#001F3F"  # Navy
    PRIMARIO = "#FFFFFF"  # Blanco
    TEXTO = "#000000"  # Texto negro
    BOTON_FONDO = "#FFFFFF"  # Fondo del botón blanco
    BOTON_TEXTO = "#000000"  # Texto del botón negro


class Estilos:
    def __init__(self):
        """
        Inicializa los estilos globales.
        """
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.colores = {
            "fondo": ColorPalette.FONDO.value,
            "primario": ColorPalette.PRIMARIO.value,
            "texto": ColorPalette.TEXTO.value,
            "boton_fondo": ColorPalette.BOTON_FONDO.value,
            "boton_texto": ColorPalette.BOTON_TEXTO.value,
        }
        self._configurar_fuentes()
        self._configurar_estilos()

    def _configurar_fuentes(self):
        """
        Configura las fuentes utilizadas en el sistema.
        """
        self.fuentes = {
            "global": font.Font(family="Arial", size=12),
            "titulo": font.Font(family="Arial", size=14, weight="bold"),
            "boton": font.Font(family="Arial", size=12, weight="bold"),
        }

    def _configurar_estilos(self):
        """
        Configura estilos para widgets específicos.
        """
        # Estilo para la ventana principal
        self.style.configure(
            "TFrame",
            background=self.colores["fondo"],
        )

        # Estilo para etiquetas
        self.style.configure(
            "TLabel",
            font=self.fuentes["global"],
            background=self.colores["fondo"],
            foreground=self.colores["texto"],
        )

        # Estilo para botones
        self.style.configure(
            "TButton",
            font=self.fuentes["boton"],
            background=self.colores["boton_fondo"],
            foreground=self.colores["boton_texto"],
            padding=10,
        )
        self.style.map(
            "TButton",
            background=[("active", self.colores["boton_fondo"])],
            foreground=[("active", self.colores["boton_texto"])],
        )