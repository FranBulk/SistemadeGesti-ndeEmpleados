import random
import string

def generar_contraseña():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    contraseña = ''.join(random.choice(caracteres) for _ in range(8))
    return contraseña