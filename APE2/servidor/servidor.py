#!/usr/bin/env python3
import os
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COMPARTIDO = os.path.join(BASE_DIR, "..", "compartido")
ARCHIVO_ENTRADA = os.path.join(COMPARTIDO, "entrada_servidor.txt")
ARCHIVO_SALIDA = os.path.join(COMPARTIDO, "salida_servidor.txt")
ARCHIVO_ESTADO = os.path.join(COMPARTIDO, ".ultima_posicion.txt")
TIEMPO_REVISION = 2

def leer_ultima_posicion():
    if os.path.exists(ARCHIVO_ESTADO):
        with open(ARCHIVO_ESTADO, 'r', encoding='utf-8') as f:
            return int(f.read().strip() or 0)
    return 0

def guardar_ultima_posicion(posicion):
    with open(ARCHIVO_ESTADO, 'w', encoding='utf-8') as f:
        f.write(str(posicion))

def procesar_mensaje(texto):
    texto = texto.strip()
    if not texto:
        return ""
    # Ejemplo: convertir a mayúsculas e invertir
    return texto.upper()[::-1]

def main():
    posicion_leida = leer_ultima_posicion()
    
    # Debe ejecutarse continuamente (simulación de servicio activo)
    while True:
        try:
            # Revise periódicamente el archivo entrada_servidor.txt
            if os.path.exists(ARCHIVO_ENTRADA):
                with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                
                posicion_actual = len(contenido)

                # Si el archivo se vació o truncó, reiniciar la posición
                if posicion_actual < posicion_leida:
                    posicion_leida = 0

                # Detecte si existe contenido nuevo
                if posicion_actual > posicion_leida:
                    # Obtener solo lo nuevo
                    with open(ARCHIVO_ENTRADA, 'r', encoding='utf-8') as f:
                        f.seek(posicion_leida)
                        nuevo = f.read()

                    # Procesar cada línea nueva (se ignoran las vacías)
                    for linea in nuevo.splitlines():
                        if linea.strip():
                            resultado = procesar_mensaje(linea)

                            # Escriba el resultado en salida_servidor.txt
                            with open(ARCHIVO_SALIDA, 'a', encoding='utf-8') as f:
                                f.write(resultado + '\n')

                    # Guardar posición para no reprocesar
                    guardar_ultima_posicion(posicion_actual)
                    posicion_leida = posicion_actual
                
        except Exception as e:
            print(f"Error en el servidor: {e}")
        
        # No debe reprocesar el mismo mensaje
        time.sleep(TIEMPO_REVISION)

if __name__ == "__main__":
    main()
