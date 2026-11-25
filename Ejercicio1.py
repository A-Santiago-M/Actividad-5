import os
import tkinter as tk
from enum import Enum
from tkinter import ttk, messagebox, filedialog

class TipoCargo(Enum):
    DIRECTIVO = "Directivo"
    ESTRATEGICO = "Estratégico"
    OPERATIVO = "Operativo"


class TipoGenero(Enum):
    MASCULINO = "Masculino"
    FEMENINO = "Femenino"


class Empleado:
    """Empleado de una empresa."""

    def __init__(self, nombre, apellidos, cargo, genero, salario_dia,
                 dias_trabajados, otros_ingresos, pagos_salud, aporte_pensiones):
        self.nombre = nombre
        self.apellidos = apellidos
        self.cargo = cargo
        self.genero = genero
        self.salario_dia = salario_dia
        self.dias_trabajados = dias_trabajados
        self.otros_ingresos = otros_ingresos
        self.pagos_salud = pagos_salud
        self.aporte_pensiones = aporte_pensiones

    def calcular_nomina(self):
        """Salario mensual = (días * sueldo por día) + otros ingresos
        - pagos por salud - aporte pensiones"""
        
        return (self.salario_dia * self.dias_trabajados
                + self.otros_ingresos
                - self.pagos_salud
                - self.aporte_pensiones)


class ListaEmpleados:
    """Lista de empleados de la empresa."""

    def __init__(self):
        self.lista = []

    def agregar_empleado(self, empleado):
        self.lista.append(empleado)

    def calcular_total_nomina(self):
        return sum(e.calcular_nomina() for e in self.lista)

    def obtener_matriz(self):
        return [(e.nombre, e.apellidos, f"{e.calcular_nomina():,.2f}")
                for e in self.lista]

    def convertir_texto(self):
        texto = ""
        for e in self.lista:
            texto += (f"Nombre = {e.nombre}\n"
                      f"Apellidos = {e.apellidos}\n"
                      f"Cargo = {e.cargo.value}\n"
                      f"Género = {e.genero.value}\n"
                      f"Salario por día = ${e.salario_dia}\n"
                      f"Días trabajados = {e.dias_trabajados}\n"
                      f"Otros ingresos = ${e.otros_ingresos}\n"
                      f"Pagos salud = ${e.pagos_salud}\n"
                      f"Aportes pensiones = ${e.aporte_pensiones}\n"
                      f"Sueldo mensual = ${e.calcular_nomina():,.2f}\n"
                      f"---------\n")
        texto += f"Total nómina = ${self.calcular_total_nomina():,.2f}"
        return texto
class VentanaAgregarEmpleado:
    def __init__(self, padre, lista):
        self.lista = lista
        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Agregar Empleado")
        self.ventana.geometry("320x400")
        self.ventana.resizable(False, False)

        marco = ttk.Frame(self.ventana, padding=10)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Nombre:").grid(row=0, column=0, sticky="e", pady=4)
        self.campo_nombre = ttk.Entry(marco, width=22)
        self.campo_nombre.grid(row=0, column=1)

        ttk.Label(marco, text="Apellidos:").grid(row=1, column=0, sticky="e", pady=4)
        self.campo_apellidos = ttk.Entry(marco, width=22)
        self.campo_apellidos.grid(row=1, column=1)

        ttk.Label(marco, text="Cargo:").grid(row=2, column=0, sticky="e", pady=4)
        self.campo_cargo = ttk.Combobox(
            marco, width=19, state="readonly",
            values=[c.value for c in TipoCargo])
        self.campo_cargo.current(0)
        self.campo_cargo.grid(row=2, column=1)

        ttk.Label(marco, text="Género:").grid(row=3, column=0, sticky="e", pady=4)
        self.var_genero = tk.StringVar(value=TipoGenero.MASCULINO.value)
        marco_gen = ttk.Frame(marco)
        marco_gen.grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(marco_gen, text="Masculino", value=TipoGenero.MASCULINO.value,
                        variable=self.var_genero).pack(anchor="w")
        ttk.Radiobutton(marco_gen, text="Femenino", value=TipoGenero.FEMENINO.value,
                        variable=self.var_genero).pack(anchor="w")

        ttk.Label(marco, text="Salario por día:").grid(row=4, column=0, sticky="e", pady=4)
        self.campo_salario = ttk.Entry(marco, width=22)
        self.campo_salario.grid(row=4, column=1)

        ttk.Label(marco, text="Días trabajados:").grid(row=5, column=0, sticky="e", pady=4)
        self.campo_dias = ttk.Spinbox(marco, from_=1, to=31, width=5)
        self.campo_dias.set(30)
        self.campo_dias.grid(row=5, column=1, sticky="w")

        ttk.Label(marco, text="Otros ingresos:").grid(row=6, column=0, sticky="e", pady=4)
        self.campo_otros = ttk.Entry(marco, width=22)
        self.campo_otros.grid(row=6, column=1)

        ttk.Label(marco, text="Pagos por salud:").grid(row=7, column=0, sticky="e", pady=4)
        self.campo_salud = ttk.Entry(marco, width=22)
        self.campo_salud.grid(row=7, column=1)

        ttk.Label(marco, text="Aporte pensiones:").grid(row=8, column=0, sticky="e", pady=4)
        self.campo_pensiones = ttk.Entry(marco, width=22)
        self.campo_pensiones.grid(row=8, column=1)

        marco_botones = ttk.Frame(marco)
        marco_botones.grid(row=9, column=0, columnspan=2, pady=15)
        ttk.Button(marco_botones, text="Agregar", command=self.anadir_empleado).pack(side="left", padx=5)
        ttk.Button(marco_botones, text="Borrar", command=self.limpiar_campos).pack(side="left", padx=5)

    def limpiar_campos(self):
        for campo in (self.campo_nombre, self.campo_apellidos, self.campo_salario,
                      self.campo_otros, self.campo_salud, self.campo_pensiones):
            campo.delete(0, tk.END)
        self.campo_dias.set(30)

    def anadir_empleado(self):
        try:
            nombre = self.campo_nombre.get().strip()
            apellidos = self.campo_apellidos.get().strip()
            if not nombre or not apellidos:
                raise ValueError("Nombre y apellidos son obligatorios")

            cargo = next(c for c in TipoCargo if c.value == self.campo_cargo.get())
            genero = next(g for g in TipoGenero if g.value == self.var_genero.get())

            salario = float(self.campo_salario.get())
            dias = int(self.campo_dias.get())
            if not 1 <= dias <= 31:
                raise ValueError("Los días deben estar entre 1 y 31")
            otros = float(self.campo_otros.get())
            salud = float(self.campo_salud.get())
            pensiones = float(self.campo_pensiones.get())

            empleado = Empleado(nombre, apellidos, cargo, genero, salario,
                                dias, otros, salud, pensiones)
            self.lista.agregar_empleado(empleado)
            messagebox.showinfo("Mensaje", "El empleado ha sido agregado",
                                parent=self.ventana)
            self.limpiar_campos()
        except ValueError:
            messagebox.showerror("Error", "Campo nulo o error en formato de número",
                                 parent=self.ventana)
class VentanaNomina:
    def __init__(self, padre, lista):
        self.lista = lista
        self.ventana = tk.Toplevel(padre)
        self.ventana.title("Nómina de Empleados")
        self.ventana.geometry("430x300")
        self.ventana.resizable(False, False)

        ttk.Label(self.ventana, text="Lista de empleados:").pack(anchor="w", padx=10, pady=(10, 0))

        self.tabla = ttk.Treeview(self.ventana, columns=("nombre", "apellidos", "sueldo"),
                                  show="headings", height=8)
        self.tabla.heading("nombre", text="NOMBRE")
        self.tabla.heading("apellidos", text="APELLIDOS")
        self.tabla.heading("sueldo", text="SUELDO")
        self.tabla.column("nombre", width=130)
        self.tabla.column("apellidos", width=130)
        self.tabla.column("sueldo", width=120, anchor="e")
        self.tabla.pack(padx=10, pady=5)

        for fila in self.lista.obtener_matriz():
            self.tabla.insert("", tk.END, values=fila)

        total = self.lista.calcular_total_nomina()
        self.etiqueta_total = ttk.Label(
            self.ventana, text=f"Total nómina mensual = $ {total:,.2f}")
        self.etiqueta_total.pack(anchor="w", padx=10, pady=5)
        
class VentanaPrincipal:
    def __init__(self):
        self.empleados = ListaEmpleados()

        self.ventana = tk.Tk()
        self.ventana.title("Nómina")
        self.ventana.geometry("280x120")
        self.ventana.resizable(False, False)

        barra_menu = tk.Menu(self.ventana)
        menu_opciones = tk.Menu(barra_menu, tearoff=0)
        menu_opciones.add_command(label="Agregar empleado", command=self.agregar_empleado)
        menu_opciones.add_command(label="Calcular nómina", command=self.calcular_nomina)
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Guardar archivo", command=self.guardar_archivo)
        barra_menu.add_cascade(label="Menú", menu=menu_opciones)
        self.ventana.config(menu=barra_menu)

        ttk.Label(self.ventana, text="Seleccione una opción del menú").pack(pady=40)

    def agregar_empleado(self):
        VentanaAgregarEmpleado(self.ventana, self.empleados)

    def calcular_nomina(self):
        VentanaNomina(self.ventana, self.empleados)

    def guardar_archivo(self):
        directorio = filedialog.askdirectory(title="Seleccione la carpeta")
        if not directorio:
            return
        try:
            ruta = os.path.join(directorio, "Nómina.txt")
            with open(ruta, "w", encoding="utf-8") as archivo:
                archivo.write(self.empleados.convertir_texto())
            messagebox.showinfo("Mensaje",
                                f"El archivo de la nómina Nómina.txt se ha creado en {directorio}")
        except OSError:
            messagebox.showerror("Error", "No se pudo escribir el archivo")

    def iniciar(self):
        self.ventana.mainloop()


app = VentanaPrincipal()
app.iniciar()