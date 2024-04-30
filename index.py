import random
import os
import generador_contraseñas
from termcolor import colored

class Empleado:
    def __init__(self, nombre, apellido, num_empleado, contraseña=None,):
        self.nombre = nombre
        self.apellido = apellido
        self.num_empleado = num_empleado
        self.correo = self.generar_correo()
        self.contraseña = contraseña if contraseña else generador_contraseñas.generar_contraseña()
    
    def generar_correo(self):
        apellidoB=self.apellido.replace(' ', '')
        apellidoC=apellidoB.lower()
        correo = self.nombre[0].lower() + apellidoC + '@macrohard.mx'
        return correo
    
class GestorEmpleados:
    def __init__(self):
        self.empleados = []
        self.empleados_baja = []
        self.numerosdeempleado = {} #Es el diccionario donde se guardan las antiguedades de los empleados

    def dar_alta_empleado(self, nombre, apellido, num_empleado):
        for empleado in self.empleados:
            if empleado.num_empleado == num_empleado:
                print("El número de empleado ya existe.")
                return
        nuevo_empleado = Empleado(nombre, apellido, num_empleado)
        os.system("cls")
        print("Empleado dado de alta correctamente.")
        print("Nombre:",nombre)
        print("Apellido:",apellido)
        print("Numero de empleado:",num_empleado)
        self.empleados.append(nuevo_empleado)

    def modificar_nombre_empleado(self, num_empleado, nuevo_nombre):
        for empleado in self.empleados:
            if empleado.num_empleado == num_empleado:
                empleado.nombre = nuevo_nombre
                print("Nombre modificado correctamente.")
                return
        print("No se encontró ningún empleado con ese número.")

    def resetear_contraseña(self, num_empleado):
        for empleado in self.empleados:
            if empleado.num_empleado == num_empleado:
                empleado.contraseña = generador_contraseñas.generar_contraseña()
                print("Contraseña reseteada correctamente.")
                print(f"La nueva contraseña es: {empleado.contraseña}")
                return
        print("No se encontró ningún empleado con ese número.")

    def eliminar_empleado(self, num_empleado):
        for empleado in self.empleados:
            if empleado.num_empleado == num_empleado:
                self.empleados.remove(empleado)
                self.empleados_baja.append(empleado)
                self.numerosdeempleado[num_empleado]=0
                print("Empleado eliminado correctamente.")
                return
        print("No se encontró ningún empleado con ese número.")

    def consultar_empleado(self, num_empleado):
        for empleado in self.empleados:
            if empleado.num_empleado == num_empleado:
                antiguedad = numeroantiguedad(num_empleado, self.numerosdeempleado)
                os.system("cls")
                añosdeantiguedad = {'Novato':"NOVATO", 'Veterano':"VETERANO", 'Fundador':'FUNDADOR'} #Diccionario para la antiguedad
                if ((antiguedad>1) and (antiguedad<=9)):
                    print(añosdeantiguedad["Novato"])
                elif ((antiguedad>10) and (antiguedad<=30)):
                    print(añosdeantiguedad["Veterano"])
                elif ((antiguedad>31) and (antiguedad<=50)):
                    print(añosdeantiguedad["Fundador"])
                return f"Nombre: {empleado.nombre} {empleado.apellido}\nCorreo: {empleado.correo}\nAntigüedad: {antiguedad} años"
        return "No se encontró ningún empleado con ese número."

# Función aplicada para recibir datos del usuario
def ingresar_datos():
    nombre = input("Ingrese el nombre del empleado: ")
    apellido = input("Ingrese los apellidos del empleado: ")
    num_empleado = input("Ingrese el número de empleado: ")
    contraseña=generador_contraseñas.generar_contraseña()
    print(f"La contraseña para el empleado {nombre} {apellido} es: {contraseña}")
    return nombre, apellido, num_empleado

# Función aplicada para el menú principal
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

# Función para autenticar usuario
def autenticar_usuario():
    print(colored("USUARIO: ", "green"))
    usuario = input()
    print(colored("CONTRASEÑA: ", "green"))
    contraseña = input()
    return usuario, contraseña

def numeroantiguedad(num, numerosdeempleado):
    if (num not in numerosdeempleado or numerosdeempleado[num]==0):
        numerosdeempleado[num] = random.randint(1, 50)
    numero = numerosdeempleado[num]
    return numero

# Función principal
def main():
    gestor = GestorEmpleados()

    # Autenticación de usuario
    print(colored("Bienvenido al sistema de gestión de empleados.", "cyan"))
    usuario_valido = "root"
    contraseña_valida = "admin"
    intentos = 3
    while intentos > 0:
        usuario_ingresado, contraseña_ingresada = autenticar_usuario()
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
            nombre, apellido, num_empleado = ingresar_datos()
            gestor.dar_alta_empleado(nombre, apellido, num_empleado)
            os.system("pause")
            os.system("cls")
        elif opcion == "2":
            num_empleado = input("Ingrese el número de empleado que desea modificar: ")
            nuevo_nombre = input("Ingrese el nuevo nombre: ")
            gestor.modificar_nombre_empleado(num_empleado, nuevo_nombre)
            os.system("pause")
            os.system("cls")
        elif opcion == "3":
            num_empleado = input("Ingrese el número de empleado al que desea resetear la contraseña: ")
            gestor.resetear_contraseña(num_empleado)
            os.system("pause")
            os.system("cls")
        elif opcion == "4":
            num_empleado = input("Ingrese el número de empleado que desea eliminar: ")
            gestor.eliminar_empleado(num_empleado)
            os.system("pause")
            os.system("cls")
        elif opcion == "5":
            num_empleado = input("Ingrese el número de empleado que desea consultar: ")
            resultado = gestor.consultar_empleado(num_empleado)
            print(colored(resultado, "white"))
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