import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox, simpledialog

FORMATO_FECHA = "%d-%m-%Y"

class Huesped:
    """Huésped del hotel."""

    def __init__(self, nombres, apellidos, documento_identidad):
        self.nombres = nombres
        self.apellidos = apellidos
        self.documento_identidad = documento_identidad
        self.fecha_ingreso = None
        self.fecha_salida = None

    def obtener_dias_alojamiento(self):
        return (self.fecha_salida - self.fecha_ingreso).days


class Habitacion:
    """Habitación del hotel."""

    def __init__(self, numero, disponible, precio_dia):
        self.numero = numero
        self.disponible = disponible
        self.precio_dia = precio_dia
        self.huesped = None


class Hotel:
    """Hotel con diez habitaciones: 1-5 a $120.000 y 6-10 a $160.000."""

    def __init__(self):
        self.lista_habitaciones = []
        for numero in range(1, 11):
            precio = 120000 if numero <= 5 else 160000
            self.lista_habitaciones.append(Habitacion(numero, True, precio))

    def buscar_habitacion(self, numero):
        for h in self.lista_habitaciones:
            if h.numero == numero:
                return h
        return None

    def buscar_habitacion_ocupada(self, numero):
        h = self.buscar_habitacion(numero)
        return h is not None and not h.disponible

    def buscar_fecha_ingreso_habitacion(self, numero):
        h = self.buscar_habitacion(numero)
        if h is not None and h.huesped is not None:
            return h.huesped.fecha_ingreso.strftime(FORMATO_FECHA)
        return ""
    
class VentanaIngreso:
    def __init__(self, padre, hotel, numero_habitacion):
        self.hotel = hotel
        self.numero_habitacion = numero_habitacion

        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Ingreso")
        self.ventana.resizable(False, False)

        marco = ttk.Frame(self.ventana, padding=10)
        marco.pack()

        ttk.Label(marco, text=f"Habitación: {numero_habitacion}").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=3)

        ttk.Label(marco, text="Fecha (dd-mm-aaaa):").grid(row=1, column=0, sticky="e", pady=3)
        self.campo_fecha = ttk.Entry(marco, width=20)
        self.campo_fecha.grid(row=1, column=1, sticky="ew", padx=3)

        ttk.Label(marco, text="Huésped").grid(row=2, column=0, columnspan=2, sticky="w", pady=3)

        ttk.Label(marco, text="Nombre:").grid(row=3, column=0, sticky="e", pady=3)
        self.campo_nombre = ttk.Entry(marco, width=20)
        self.campo_nombre.grid(row=3, column=1, sticky="ew", padx=3)

        ttk.Label(marco, text="Apellidos:").grid(row=4, column=0, sticky="e", pady=3)
        self.campo_apellidos = ttk.Entry(marco, width=20)
        self.campo_apellidos.grid(row=4, column=1, sticky="ew", padx=3)

        ttk.Label(marco, text="Doc. Identidad:").grid(row=5, column=0, sticky="e", pady=3)
        self.campo_documento = ttk.Entry(marco, width=20)
        self.campo_documento.grid(row=5, column=1, sticky="ew", padx=3)

        ttk.Button(marco, text="Aceptar", command=self.aceptar).grid(row=6, column=0, pady=10, sticky="ew", padx=3)
        ttk.Button(marco, text="Cancelar", command=self.ventana.destroy).grid(row=6, column=1, pady=10, sticky="ew", padx=3)

    def aceptar(self):
        nombre = self.campo_nombre.get().strip()
        apellidos = self.campo_apellidos.get().strip()
        documento = self.campo_documento.get().strip()
        fecha_texto = self.campo_fecha.get().strip()

        if not (nombre and apellidos and documento and fecha_texto):
            messagebox.showerror("Error", "Todos los campos son obligatorios",
                                 parent=self.ventana)
            return

        try:
            fecha = datetime.strptime(fecha_texto, FORMATO_FECHA)
        except ValueError:
            messagebox.showerror("Error", "La fecha no esta en el formato solicitado",
                                 parent=self.ventana)
            return

        try:
            documento_num = int(documento)
        except ValueError:
            messagebox.showerror("Error", "El documento de identidad debe ser numerico",
                                 parent=self.ventana)
            return

        huesped = Huesped(nombre, apellidos, documento_num)
        huesped.fecha_ingreso = fecha

        habitacion = self.hotel.buscar_habitacion(self.numero_habitacion)
        habitacion.huesped = huesped
        habitacion.disponible = False

        messagebox.showinfo("Mensaje", "El huesped ha sido registrado",
                            parent=self.ventana)
        self.ventana.destroy()
        
class VentanaHabitaciones:
    def __init__(self, padre, hotel):
        self.padre = padre
        self.hotel = hotel

        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Habitaciones")
        self.ventana.resizable(False, False)

        marco = ttk.Frame(self.ventana, padding=15)
        marco.pack()

        for i, h in enumerate(hotel.lista_habitaciones):
            fila, columna = divmod(i, 5)
            celda = ttk.Frame(marco, padding=8)
            celda.grid(row=fila, column=columna, padx=8, pady=8)
            ttk.Label(celda, text=f"Habitacion {h.numero}").pack()
            estado = "Disponible" if h.disponible else "No disponible"
            color = "green" if h.disponible else "red"
            tk.Label(celda, text=estado, fg=color).pack()

        marco_sel = ttk.Frame(marco)
        marco_sel.grid(row=2, column=0, columnspan=5, pady=10)
        ttk.Label(marco_sel, text="Habitación a reservar:").pack(side="left", padx=5)
        self.campo_habitacion = ttk.Spinbox(marco_sel, from_=1, to=10, width=5)
        self.campo_habitacion.set(1)
        self.campo_habitacion.pack(side="left", padx=5)
        ttk.Button(marco_sel, text="Aceptar", command=self.aceptar).pack(side="left", padx=10)

    def aceptar(self):
        try:
            numero = int(self.campo_habitacion.get())
        except ValueError:
            messagebox.showerror("Error", "Campo nulo o error en formato de número",
                                 parent=self.ventana)
            return

        if not 1 <= numero <= 10:
            messagebox.showerror("Error", "El número de habitación debe estar entre 1 y 10",
                                 parent=self.ventana)
            return

        if self.hotel.buscar_habitacion_ocupada(numero):
            messagebox.showerror("Mensaje", "La habitación está ocupada",
                                 parent=self.ventana)
        else:
            self.ventana.destroy() 
            VentanaIngreso(self.padre, self.hotel, numero)
class VentanaSalida:
    def __init__(self, padre, hotel, numero_habitacion):
        self.hotel = hotel
        self.numero_habitacion = numero_habitacion
        self.habitacion = hotel.buscar_habitacion(numero_habitacion)

        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Salida huéspedes")
        self.ventana.resizable(False, False)

        marco = ttk.Frame(self.ventana, padding=10)
        marco.pack()

        fecha_ingreso = hotel.buscar_fecha_ingreso_habitacion(numero_habitacion)

        ttk.Label(marco, text=f"Habitacion: {numero_habitacion}").grid(row=0, column=0, sticky="w", pady=3)
        ttk.Label(marco, text=f"Fecha de ingreso: {fecha_ingreso}").grid(row=1, column=0, sticky="w", pady=3)
        ttk.Label(marco, text="Fecha de salida (dd-mm-aaaa):").grid(row=2, column=0, sticky="w", pady=3)

        self.campo_fecha_salida = ttk.Entry(marco, width=25)
        self.campo_fecha_salida.grid(row=3, column=0, sticky="ew", pady=3)

        ttk.Button(marco, text="Calcular", command=self.calcular).grid(row=4, column=0, sticky="ew", pady=5)

        self.etiqueta_dias = ttk.Label(marco, text="Cantidad de dias: ")
        self.etiqueta_dias.grid(row=5, column=0, sticky="w", pady=3)

        self.etiqueta_total = ttk.Label(marco, text="Total: $")
        self.etiqueta_total.grid(row=6, column=0, sticky="w", pady=3)
        #main in medellin 
        self.boton_registrar = ttk.Button(marco, text="Registrar salida",
                                     command=self.registrar_salida, state="disabled")
        self.boton_registrar.grid(row=7, column=0, sticky="ew", pady=5)

    def calcular(self):
        self.boton_registrar.config(state="disabled")
        try:
            fecha_salida = datetime.strptime(self.campo_fecha_salida.get().strip(), FORMATO_FECHA)
        except ValueError:
            messagebox.showerror("Mensaje", "La fecha no está en el formato solicitado",
                                 parent=self.ventana)
            return

        huesped = self.habitacion.huesped
        if fecha_salida <= huesped.fecha_ingreso:
            messagebox.showerror("Mensaje", "La fecha de salida es menor que la de ingreso",
                                 parent=self.ventana)
            return

        huesped.fecha_salida = fecha_salida
        dias = huesped.obtener_dias_alojamiento()
        total = dias * self.habitacion.precio_dia

        self.etiqueta_dias.config(text=f"Cantidad de días: {dias}")
        self.etiqueta_total.config(text=f"Total: ${total:,.0f}")
        self.boton_registrar.config(state="normal")

    def registrar_salida(self):
        self.habitacion.huesped = None
        self.habitacion.disponible = True
        messagebox.showinfo("Mensaje", "Se ha registrado la salida del huesped",
                            parent=self.ventana)
        self.ventana.destroy()
class VentanaPrincipal:
    def __init__(self, hotel):
        self.hotel = hotel

        self.ventana = tk.Tk()
        self.ventana.title("Hotel")
        self.ventana.geometry("280x120")
        self.ventana.resizable(False, False)

        barra_menu = tk.Menu(self.ventana)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(label="Consultar habitaciones", command=self.consultar_habitaciones)
        menu_opciones.add_command(label="Salida de huespedes", command=self.salida_huespedes)
        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.ventana.config(menu=barra_menu)

        ttk.Label(self.ventana, text="Seleccione una opción del meno").pack(pady=40)

    def consultar_habitaciones(self):
        VentanaHabitaciones(self.ventana, self.hotel)

    def salida_huespedes(self):
        numero = simpledialog.askinteger(
            "Salida de huespedes", "Ingrese número de habitacion",
            parent=self.ventana)
        if numero is None:
            return

        if not 1 <= numero <= 10:
            messagebox.showinfo("Mensaje", "El numero de habitación debe estar entre 1 y 10")
        elif self.hotel.buscar_habitacion_ocupada(numero):
            VentanaSalida(self.ventana, self.hotel, numero)
        else:
            messagebox.showinfo("Mensaje", "La habitacion ingresada no ha sido ocupada")

    def iniciar(self):
        self.ventana.mainloop()


app = VentanaPrincipal(Hotel())
app.iniciar()