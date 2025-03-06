# mantenimiento.manual.py
import tkinter as tk
from tkinter import ttk, scrolledtext

# Contenido completo del manual
CONTENIDO_COMPLETO = """
1. INTRODUCCIÓN
1.1 Propósito del Sistema
- Controlar asistencia del personal docente y administrativo.
- Generar reportes mensuales automatizados.
- Centralizar información institucional.
1.2 Requisitos Mínimos
- Sistema operativo: Windows 10+ o Ubuntu 22.04+.
- Memoria RAM: 4 GB mínimo (8 GB recomendado).
- Espacio en disco: 500 MB libres.
- Conexión a Internet para actualizaciones.
1.3 Beneficios del Sistema
- Reducción de errores humanos en el registro de asistencias.
- Mayor transparencia en la gestión de datos.
- Facilidad de acceso a reportes históricos.

2. REGISTRO DE USUARIOS
2.1 Crear Nuevo Usuario
- Paso 1: Ir a 'Usuarios > Nuevo'.
- Paso 2: Completar formulario con datos personales.
- Paso 3: Asignar rol (Administrador/Usuario).
- Paso 4: Generar contraseña temporal.
2.2 Editar Usuario Existente
- Doble clic en el registro deseado.
- Campos editables: Nombre, Correo, Teléfono.
- Restricción: No se puede cambiar el RUT.
2.3 Eliminar Usuario
- Requiere confirmación adicional.
- Solo administradores pueden eliminar usuarios.

3. GESTIÓN DE ASISTENCIA
3.1 Registrar Hora de Entrada (HE)
- Seleccionar empleado de la lista activa.
- Hora automática del sistema (+ geolocalización).
- Comentarios opcionales (ej: reunión externa).
3.2 Registrar Hora de Salida (HS)
- Validación: Debe existir HE previa.
- Sistema alerta si HS es antes de las 18:00.
- Campos obligatorios: Actividades realizadas.
3.3 Visualizar Asistencias
- Filtrar por rango de fechas.
- Exportar a PDF o Excel.
- Estadísticas de puntualidad y ausencias.

4. GENERACIÓN DE REPORTES
4.1 Reporte Mensual Individual
- Filtrar por empleado y mes.
- Incluye: Horas trabajadas, atrasos, ausencias.
- Opciones exportación: PDF (formato oficial) o Excel.
4.2 Reporte Departamento
- Estadísticas comparativas por área.
- Gráficos de barras interactivos.
- Firma electrónica del encargado.
4.3 Reporte Anual
- Resumen de asistencia anual.
- Comparativa mensual.
- Indicadores de desempeño.

5. RESPALDOS DE SEGURIDAD
5.1 Crear Respaldo Manual
- Menú: Herramientas > Respaldos.
- Seleccionar ruta de destino (local o red).
- Formato comprimido .BAK con encriptación.
5.2 Restaurar Respaldo
- Requiere permisos de nivel administrador.
- Seleccionar archivo .BAK válido.
- Verificación de integridad automática.

6. CONFIGURACIÓN DEL SISTEMA
6.1 Parámetros Generales
- Establecer hora de cierre diario.
- Definir días festivos institucionales.
- Umbral para alertas de atrasos (15 min default).
6.2 Personalización de Interfaz
- Selección de tema (claro/oscuro).
- Ajustar tamaño de fuente global.
- Idioma: Español/Inglés (requiere reinicio).
6.3 Configuración de Notificaciones
- Activar/desactivar notificaciones por correo.
- Configurar frecuencia de notificaciones.
- Personalizar contenido de las notificaciones.

7. PROBLEMAS COMUNES
7.1 Error al Iniciar Sesión
- Verificar conexión a Internet.
- Restablecer contraseña (link olvidé mi clave).
- Contactar soporte si bloquea cuenta.
7.2 Reportes no Generados
- Revisar permisos de escritura en carpeta.
- Verificar espacio en disco disponible.
- Reiniciar servicio de reportes.
7.3 Problemas de Conexión
- Verificar configuración de red.
- Probar con otra conexión a Internet.
- Contactar al administrador de red.

8. PREGUNTAS FRECUENTES (FAQs)
8.1 ¿Cómo restablecer mi contraseña?
- Usar link 'Recuperar contraseña' en login.
- Solicitar ayuda al administrador del sistema.
- Tiempo máximo para cambio: 24 horas.
8.2 ¿Exportar datos a Excel?
- Versión Pro permite exportación completa.
- Formato .xlsx con fórmulas precalculadas.
- Límite de 10,000 registros por exportación.
8.3 ¿Cómo cambiar mi correo electrónico?
- Ir a 'Perfil > Editar'.
- Ingresar el nuevo correo y guardar cambios.
- Verificar cambio con el correo de confirmación.
"""

class Ventana(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Manual del Sistema")
        self.geometry("1024x768")
        self.configure(background="#001F3F")  # Fondo navy
        self.resizable(False, False)

        # Configurar estilos
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self._configurar_estilos()

        # Crear pestañas
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=5, pady=5)

        # Pestaña de Contenido
        self.crear_pestana_contenido()

        # Centrar la ventana
        self.centrar_ventana()

        # Mostrar la introducción al iniciar
        self.mostrar_seccion("1. Introducción")

    def _configurar_estilos(self):
        """Configura los estilos para los widgets."""
        self.style.configure(
            "TNotebook",
            background="#001F3F",  # Fondo navy
            bordercolor="#001F3F"
        )
        self.style.configure(
            "TNotebook.Tab",
            foreground="white",
            background="#001F3F",
            padding=[20, 5],
            font=("Arial", 10, "bold")
        )
        self.style.map("TNotebook.Tab", background=[("selected", "#1A5276")])

    def centrar_ventana(self):
        """
        Centra la ventana en la pantalla.
        """
        self.update_idletasks()
        ancho = 1024  # Ancho fijo de la ventana
        alto = 768    # Alto fijo de la ventana
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")

    def crear_pestana_contenido(self):
        """
        Crea la pestaña de contenido del manual.
        """
        marco_contenido = ttk.Frame(self.notebook)
        self.notebook.add(marco_contenido, text="Contenido")

        # Panel Índice
        marco_indice = tk.Frame(marco_contenido, bg="#001F3F", width=220)
        marco_indice.pack(side="left", fill="y", padx=0)

        tk.Label(
            marco_indice,
            text="ÍNDICE",
            bg="#001F3F",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=15, padx=10)

        secciones = [
            "1. Introducción", "2. Registro",
            "3. Asistencia", "4. Reportes",
            "5. Respaldos", "6. Configuración",
            "7. Problemas", "8. FAQs"
        ]

        for seccion in secciones:
            btn = tk.Button(
                marco_indice,
                text=seccion,
                bg="white",
                fg="black",
                activebackground="#E0E0E0",
                font=("Arial", 10),
                relief="flat",
                bd=1,
                command=lambda s=seccion: self.mostrar_seccion(s)
            )
            btn.pack(fill="x", pady=3, padx=10)

        # Panel Texto
        marco_texto = ttk.Frame(marco_contenido)
        marco_texto.pack(side="right", fill="both", expand=True)

        self.texto = scrolledtext.ScrolledText(
            marco_texto,
            wrap=tk.WORD,
            font=("Arial", 10),
            padx=20,
            pady=20,
            bg="white",
            state="normal"
        )
        self.texto.insert(tk.INSERT, CONTENIDO_COMPLETO)
        self.texto.configure(state="disabled")
        self.texto.pack(fill="both", expand=True)

    def mostrar_seccion(self, seccion):
        """
        Muestra una sección específica del manual.
        """
        contenido = {
            "1. Introducción": self.obtener_seccion("1. INTRODUCCIÓN", "2. REGISTRO DE USUARIOS"),
            "2. Registro": self.obtener_seccion("2. REGISTRO DE USUARIOS", "3. GESTIÓN DE ASISTENCIA"),
            "3. Asistencia": self.obtener_seccion("3. GESTIÓN DE ASISTENCIA", "4. GENERACIÓN DE REPORTES"),
            "4. Reportes": self.obtener_seccion("4. GENERACIÓN DE REPORTES", "5. RESPALDOS DE SEGURIDAD"),
            "5. Respaldos": self.obtener_seccion("5. RESPALDOS DE SEGURIDAD", "6. CONFIGURACIÓN DEL SISTEMA"),
            "6. Configuración": self.obtener_seccion("6. CONFIGURACIÓN DEL SISTEMA", "7. PROBLEMAS COMUNES"),
            "7. Problemas": self.obtener_seccion("7. PROBLEMAS COMUNES", "8. PREGUNTAS FRECUENTES (FAQs)"),
            "8. FAQs": CONTENIDO_COMPLETO.split("8. PREGUNTAS FRECUENTES (FAQs)")[1]
        }.get(seccion, "Contenido no disponible")

        self.texto.configure(state="normal")
        self.texto.delete(1.0, tk.END)
        self.texto.insert(tk.INSERT, contenido)
        self.texto.configure(state="disabled")

    def obtener_seccion(self, inicio, fin):
        """
        Obtiene una sección específica del contenido completo.
        """
        try:
            contenido = CONTENIDO_COMPLETO.split(inicio)[1].split(fin)[0]
            return f"{inicio}{contenido}"  # Agregamos el título de la sección al contenido
        except Exception as e:
            print(f"Error al obtener sección: {e}")
            return "Sección en desarrollo"

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana raíz
    app = Ventana(root)
    app.mainloop()