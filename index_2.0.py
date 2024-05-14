import random
import os
from termcolor import colored
import threading

def menu_principal():
    print(colored("\nMenú Principal:", "magenta"))
    print(colored("1. Dar de alta un empleado", "white"))
    print(colored("2. Modificar nombre de un empleado", "white"))
    print(colored("3. Resetear contraseña de un empleado", "white"))
    print(colored("4. Eliminar un empleado", "white"))
    print(colored("5. Consultar empleado", "white"))
    print(colored("6. Salir", "white"))

    opcion = input("Ingrese el número de la opción que desee: ")
    os.system("cls")
    return opcion

class Empleado:
    def __init__(self, nombre, apellido, num_empleado, contraseña=None):
        self.nombre = nombre
        self.apellido = apellido
        self.num_empleado = num_empleado
        self.correo = self.generar_correo()
        self.contraseña = contraseña if contraseña else self.generar_contraseña()
    
    def generar_correo(self):
        apellidoB = self.apellido.replace(' ', '')
        apellidoC = apellidoB.lower()
        correo = self.nombre[0].lower() + apellidoC + '@macrohard.mx'
        return correo
    
    def generar_contraseña(self):
        # Lógica para generar la contraseña
        return "contraseña_generada"

class GestorEmpleados:
    def __init__(self):
        self.empleados = []
        self.empleados_baja = []
        self.numerosdeempleado = {}  # Es el diccionario donde se guardan las antiguedades de los empleados
        self.lock = threading.Lock()

    def dar_alta_empleado(self, nombre, apellido, num_empleado):
        with self.lock:
            num_empleado = int(num_empleado)  # Convertir a entero
            for empleado in self.empleados:
                if empleado.num_empleado == num_empleado:
                    raise ValueError("El número de empleado ya existe.")
            nuevo_empleado = Empleado(nombre, apellido, num_empleado)
            self.empleados.append(nuevo_empleado)
            print("Empleado dado de alta correctamente.")
            print("Nombre:",nombre)
            print("Apellido:",apellido)
            print("Numero de empleado:",num_empleado)

    def eliminar_empleado(self, num_empleado):
        with self.lock:
            try:
                empleado = next(emp for emp in self.empleados if emp.num_empleado == num_empleado)
                self.empleados.remove(empleado)
                self.empleados_baja.append(empleado)
                self.numerosdeempleado[num_empleado] = 0
                print("Empleado eliminado correctamente.")
            except StopIteration:
                print("No se encontró ningún empleado con ese número.")
            except Exception as e:
                print(f"Error al eliminar empleado: {e}")

    def consultar_empleado(self, num_empleado):
        with self.lock:
            for empleado in self.empleados:
                if empleado.num_empleado == num_empleado:
                    antiguedad = self.numero_antiguedad(num_empleado)
                    añosdeantiguedad = {'Novato':"NOVATO", 'Veterano':"VETERANO", 'Fundador':'FUNDADOR'} #Diccionario para la antiguedad
                    if ((antiguedad>1) and (antiguedad<=9)):
                        print(añosdeantiguedad["Novato"])
                    elif ((antiguedad>10) and (antiguedad<=30)):
                        print(añosdeantiguedad["Veterano"])
                    elif ((antiguedad>31) and (antiguedad<=50)):
                        print(añosdeantiguedad["Fundador"])
                    return f"Nombre: {empleado.nombre} {empleado.apellido}\nCorreo: {empleado.correo}\nAntigüedad: {antiguedad} años"
            return "No se encontró ningún empleado con ese número."

    def modificar_nombre_empleado(self, num_empleado, nuevo_nombre):
        with self.lock:
            empleado_encontrado = False
            for empleado in self.empleados:
                if empleado.num_empleado == num_empleado:
                    empleado.nombre = nuevo_nombre
                    empleado_encontrado = True
                    print("Nombre modificado correctamente.")
                    break
            if not empleado_encontrado:
                raise ValueError("No se encontró ningún empleado con ese número.")

    def resetear_contraseña(self, num_empleado):
        with self.lock:
            empleado_encontrado = False
            for empleado in self.empleados:
                if empleado.num_empleado == num_empleado:
                    empleado.contraseña = empleado.generar_contraseña()
                    empleado_encontrado = True
                    print("Contraseña reseteada correctamente.")
                    break
            if not empleado_encontrado:
                raise ValueError("No se encontró ningún empleado con ese número.")

    def numero_antiguedad(self, num):
        with self.lock:
            if (num not in self.numerosdeempleado or self.numerosdeempleado[num]==0):
                self.numerosdeempleado[num] = random.randint(1, 50)
            return self.numerosdeempleado[num]

# Funciones para hilos
def alta_empleado(gestor):
    nombre = input("Ingrese el nombre del empleado: ")
    apellido = input("Ingrese los apellidos del empleado: ")
    num_empleado = input("Ingrese el número de empleado: ")
    try:
        num_empleado = int(num_empleado)  # Convertir a entero
    except ValueError:
        print(colored("Error: El número de empleado debe ser un valor numérico.", "red"))
        return
    gestor.dar_alta_empleado(nombre, apellido, num_empleado)

def consulta_empleado(gestor):
    num_empleado = input("Ingrese el número de empleado que desea consultar: ")
    try:
        resultado = gestor.consultar_empleado(num_empleado)
    except ValueError as e:
        resultado = colored(str(e), "red")
    print(resultado)

# Función principal
def main():
    gestor = GestorEmpleados()

    # Autenticación de usuario
    print(colored("Bienvenido al sistema de gestión de empleados.", "cyan"))
    usuario_valido = "root"
    contraseña_valida = "admin"
    intentos = 3
    while intentos > 0:
        usuario_ingresado = input(colored("USUARIO: ", "green"))
        contraseña_ingresada = input(colored("CONTRASEÑA: ", "green"))
        if usuario_ingresado == usuario_valido and contraseña_ingresada == contraseña_valida:
            os.system("cls")
            print("Autenticación exitosa. Acceso concedido.")
            break
        else:
            print("Nombre de usuario o contraseña incorrectos. Por favor, intente nuevamente.")
            intentos -= 1
            print(f"Intentos restantes: {intentos}")
    else:
        os.system("cls")
        print(colored("Ha excedido el número máximo de intentos. Saliendo del programa.", "red", attrs=["bold"]))
        return

    # Acceso al menú principal
    while True:
        opcion = menu_principal()
        if opcion == "1":
            try:
                # Crear un hilo para dar de alta un empleado
                hilo_alta = threading.Thread(target=alta_empleado, args=(gestor,))
                hilo_alta.start()
                # Crear un hilo para consultar un empleado
                hilo_consulta = threading.Thread(target=consulta_empleado, args=(gestor,))
                hilo_consulta.start()
            except ValueError as e:
                print(colored(str(e), "red"))
            os.system("pause")
            os.system("cls")
        elif opcion == "2":
            num_empleado = input("Ingrese el número de empleado que desea modificar: ")
            if not any(empleado.num_empleado == num_empleado for empleado in gestor.empleados):
                print(colored("No se encontró ningún empleado con ese número.", "red"))
                os.system("pause")
                os.system("cls")
                continue
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            try:
                gestor.modificar_nombre_empleado(num_empleado, nuevo_nombre)
            except ValueError as e:
                print(colored(str(e), "red"))
            os.system("pause")
            os.system("cls")
        elif opcion == "3":
            num_empleado = input("Ingrese el número de empleado al que desea resetear la contraseña: ")
            try:
                gestor.resetear_contraseña(num_empleado)
            except ValueError as e:
                print(colored(str(e), "red"))
            os.system("pause")
            os.system("cls")
        elif opcion == "4":
            num_empleado = input("Ingrese el número de empleado que desea eliminar: ")
            gestor.eliminar_empleado(num_empleado)
            os.system("pause")
            os.system("cls")
        elif opcion == "5":
            num_empleado = input("Ingrese el número de empleado que desea consultar: ")
            try:
                consulta_empleado(gestor)
            except ValueError as e:
                print(colored(str(e), "red"))
            os.system("pause")
            os.system("cls")
        elif opcion == "6":
            print(colored("Saliendo del programa.", "red"))
            os.system("pause")
            os.system("cls")
            break
        else:
            print(colored("Opción no válida. Por favor, ingrese una opción válida.", "red"))


if __name__ == "__main__":
    main()
