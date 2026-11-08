#!/usr/bin/env python3
import os
import time

# Archivos compartidos con el servidor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPARTIDO = os.path.join(BASE_DIR, "..", "compartido")
ARCHIVO_ENTRADA = os.path.join(COMPARTIDO, "entrada_servidor.txt")
ARCHIVO_SALIDA = os.path.join(COMPARTIDO, "salida_servidor.txt")
TIEMPO_ESPERA = 3

def main():
    print("=== Cliente ===")
    
    # Solicite un mensaje al usuario
    mensaje = input("Ingrese mensaje: ")
    
    if not mensaje.strip():
        print("Mensaje vacío, cancelando.")
        return
    
    # Escriba el mensaje en entrada_servidor.txt
    with open(ARCHIVO_ENTRADA, 'a', encoding='utf-8') as f:
        f.write(mensaje + '\n')
    
    print(f"Mensaje enviado: {mensaje}")
    
    # Espere un tiempo (simulando latencia)
    print(f"Esperando respuesta del servidor... ({TIEMPO_ESPERA}s)")
    time.sleep(TIEMPO_ESPERA)
    
    # Lea la respuesta desde salida_servidor.txt
    if os.path.exists(ARCHIVO_SALIDA):
        with open(ARCHIVO_SALIDA, 'r', encoding='utf-8') as f:
            lineas = f.readlines()
        
        if lineas:
            ultima_respuesta = lineas[-1].strip()
            # Muestre el resultado en pantalla
            print(f"Respuesta del servidor: {ultima_respuesta}")
        else:
            print("No hay respuesta disponible.")
    else:
        print("Archivo de salida no existe.")

if __name__ == "__main__":
    main()
