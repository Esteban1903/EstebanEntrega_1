import tkinter as tk
import random

dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

class Mesero:
    def __init__(self, nombre: str, correo: str):
        self.nombre = nombre
        self.correo = correo
        self.dias_descanso = 0
        self.horas_trabajadas = 0
        self.dia_descanso_personalizado = None

    def asignar_descanso_personalizado(self, dia_descanso: str):
        self.dia_descanso_personalizado = dia_descanso

    def tiene_dia_descanso_personalizado(self, dia: str):
        return self.dia_descanso_personalizado == dia

    def enviar_correo(self, dia: str, turno: str):
        mensaje = f"Hola {self.nombre}, tu turno para el día {dia} es: {turno}."
        print(f"Enviando correo a {self.correo}: {mensaje}")

class Restaurante:
    def __init__(self):
        self.meseros = []
        self.horas_trabajadas = 0

    def agregar_mesero(self, nombre: str, correo: str):
        mesero = Mesero(nombre, correo)
        self.meseros.append(mesero)

    def generar_horarios(self):
        global mesero
        turnos = [
            "11:00 am - 18:00 pm",
            "11:00 am - 15:00 pm - 18:00 pm - cierre",
            "12:00 pm - 15:00 pm - 18:00 pm - cierre",
            "12:00 pm - cierre"
        ]
        horarios = {dia: [] for dia in dias_semana}
        meseros_disponibles = self.meseros.copy()

        for dia in dias_semana:
            if dia in ["Lunes", "Martes", "Miércoles"]:
                max_meseros_descanso = 3
            else:
                max_meseros_descanso = 2

            meseros_descanso = []
            for mesero in meseros_disponibles:
                if mesero.tiene_dia_descanso_personalizado(dia):
                    meseros_descanso.append(mesero)
                    mesero.dias_descanso += 1

            if len(meseros_descanso) < max_meseros_descanso:
                for _ in range(max_meseros_descanso - len(meseros_descanso)):
                    mesero_descanso = random.choice(meseros_disponibles)
                    meseros_descanso.append(mesero)
                    mesero_descanso.dias_descanso += 1

            for mesero in meseros_disponibles:
                if mesero in meseros_descanso:
                    horarios[dia].append(f"{mesero.nombre}: Descanso")
                    mesero.enviar_correo(dia, "Descanso")
                else:
                    turno = random.choice(turnos)
                    horas_turno = 0
                    if turno == "11:00 am - 18:00 pm":
                        horas_turno = 7
                    elif turno == "11:00 am - 15:00 pm - 18:00 pm - cierre":
                        horas_turno = 9
                    elif turno == "12:00 pm - 15:00 pm - 18:00 pm - cierre":
                        horas_turno = 8
                    else:
                        horas_turno = 10

                    if mesero.horas_trabajadas + horas_turno <= 48:
                        horarios[dia].append(f"{mesero.nombre}: {turno}")
                        mesero.horas_trabajadas += horas_turno
                        self.horas_trabajadas += horas_turno
                        mesero.enviar_correo(dia, turno)
                    else:
                        horarios[dia].append(f"{mesero.nombre}: Descanso (Exceso de horas)")
                        mesero.enviar_correo(dia, "Descanso (Exceso de horas)")

            meseros_disponibles = self.meseros.copy()

        return horarios


ventana = tk.Tk()
ventana.title("Gestión de Restaurante")

#Función para agregar un mesero a la lista
def agregar_mesero():
    nombre = nombre_entry.get()
    correo = correo_entry.get()
    restaurante.agregar_mesero(nombre, correo)
    nombre_entry.delete(0, tk.END)
    correo_entry.delete(0, tk.END)

#Función para generar horarios y mostrarlos en el cuadro de texto
def generar_horarios():
    horarios = restaurante.generar_horarios()
    horarios_textbox.delete(1.0, tk.END)
    for dia, turnos in horarios.items():
        horarios_textbox.insert(tk.END, f"{dia}:\n")
        for turno in turnos:
            horarios_textbox.insert(tk.END, f"- {turno}\n")

# Elementos de la GUI
nombre_label = tk.Label(ventana, text="Nombre del Mesero:")
nombre_label.pack()
nombre_entry = tk.Entry(ventana)
nombre_entry.pack()

correo_label = tk.Label(ventana, text="Correo Electrónico:")
correo_label.pack()
correo_entry = tk.Entry(ventana)
correo_entry.pack()

agregar_button = tk.Button(ventana, text="Agregar Mesero", command=agregar_mesero)
agregar_button.pack()

generar_button = tk.Button(ventana, text="Generar Horarios", command=generar_horarios)
generar_button.pack()

horarios_textbox = tk.Text(ventana, height=10, width=40)
horarios_textbox.pack()

restaurante = Restaurante()

ventana.mainloop()