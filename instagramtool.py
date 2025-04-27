import sys
import time
import logging
from instagrapi import Client
import os
from datetime import datetime

# ⚡ COLORES TERMINAL personalizados
MORADO = "\033[38;5;99m"
ROSA = "\033[38;5;204m"
AMARILLO = "\033[38;5;226m"
NARANJA = "\033[38;5;214m"
ROJO = "\033[38;5;196m"
RESET = "\033[0m"

# 🚀 Contraseña que quieres
CONTRASENA_CORRECTA = "MintToolInstagram"

# 🎯 Pide contraseña antes de arrancar
password = input(f"{MORADO}Introduce la contraseña para usar la herramienta: {RESET}").strip()

if password != CONTRASENA_CORRECTA:
    print(f"{ROSA}❌ Contraseña incorrecta. Cerrando el programa...{RESET}")
    time.sleep(1)
    sys.exit()

print(f"{NARANJA}✅ Contraseña correcta. Bienvenid@ 🔥{RESET}\n")

# Banner con los colores personalizados
print(f"{ROSA}  _______  ____    ____   _        _____  _____ ")
print(f"{NARANJA} |__   __|/ __ \  / __ \ | |      |_   _|/ ____|")
print(f"{ROSA}    | |  | |  | || |  | || |        | | | |  __ ")
print(f"{NARANJA}    | |  | |  | || |  | || |        | | | | |_ |")
print(f"{ROSA}    | |  | |__| || |__| || |____   _| |_| |__| |")
print(f"{NARANJA}    |_|   \____/  \____/ |______| |_____|\_____|")
print(f"{MORADO}                 :) {RESET}")
print(f"{MORADO}              Created by Mint{RESET}\n")

# Continuamos con el programa
logging.getLogger("instagrapi").setLevel(logging.CRITICAL)

def silent_public_request(self, url, data=None, params=None, headers=None):
    try:
        return self.private_request(url, data=data, params=params, headers=headers)
    except Exception:
        return None

Client.public_request = silent_public_request

cl = Client()

# Pedimos sesión manualmente (sin necesidad de session_id)
try:
    print(f"\n{MORADO}Introduce tus datos de Instagram:{RESET}")
    username = input(f"{MORADO}Usuario: {RESET}").strip()
    password = input(f"{MORADO}Contraseña: {RESET}").strip()

    cl.login(username, password)
    print(f"\n{NARANJA}Inicio de sesión exitoso!{RESET}\n")

except Exception as e:
    print(f"{ROSA}Error al iniciar sesión: {e}{RESET}")
    sys.exit()

# Solución para evitar el error 'NoneType' object has no attribute 'get' en los mensajes directos
try:
    # Intentamos obtener los mensajes directos
    threads = cl.direct_threads()
    
    # Verificamos si 'threads' está vacío o es None
    if not threads or threads is None:
        print(f"{ROSA}No se encontraron hilos de mensajes directos. Asegúrate de estar conectado y de que tienes mensajes.{RESET}")
        sys.exit()

except Exception as e:
    print(f"{ROSA}Error al obtener los hilos de mensajes directos: {e}{RESET}")
    sys.exit()

ultimas_5_personas = []

# Evitar errores si no hay mensajes o hilos
if threads:
    for thread in threads[:5]:  # Limita a los 5 primeros hilos de conversación
        if len(thread.users) == 1:
            usuario = thread.users[0].username
        else:
            usuario = ", ".join([user.username for user in thread.users])
        ultimas_5_personas.append(usuario)

    print(f"\n{NARANJA}Últimas 5 personas con las que has hablado:{RESET}")
    for idx, usuario in enumerate(ultimas_5_personas, start=1):
        print(f"{idx}. {usuario}")

    nombre_buscado = input(f"\n{MORADO}Ingresa el nombre de usuario para ver los últimos mensajes: {RESET}").strip()

    def encontrar_thread(threads, nombre):
        for thread in threads:
            if len(thread.users) == 1 and thread.users[0].username.lower() == nombre.lower():
                return thread
            elif len(thread.users) > 1:
                usernames = [user.username.lower() for user in thread.users]
                if nombre.lower() in usernames:
                    return thread
        return None

    thread_encontrado = encontrar_thread(threads, nombre_buscado)

    if thread_encontrado:
        messages = thread_encontrado.messages
        total_mensajes = len(messages)
        print(f"\n{NARANJA}Últimos mensajes con {nombre_buscado} (Total de mensajes: {total_mensajes}):{RESET}")
        
        num_mensajes_a_mostrar = 10
        mensajes_a_mostrar = (
            messages[-num_mensajes_a_mostrar:] if total_mensajes >= num_mensajes_a_mostrar else messages
        )
        
        mensajes_a_mostrar = sorted(mensajes_a_mostrar, key=lambda msg: msg.timestamp)
        
        for msg in mensajes_a_mostrar:
            try:
                sender_username = cl.user_info(msg.user_id).username if msg.user_id else 'Desconocido'
            except Exception:
                sender_username = "Desconocido"
            timestamp = msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            if hasattr(msg, "text") and msg.text:
                text = msg.text
            elif hasattr(msg, "media"):
                text = "[Archivo multimedia: Foto, Video o Audio]"
            else:
                text = "[Mensaje sin texto]"

            print(f"[{timestamp}] {sender_username}: {text}")
    else:
        print(f"\n{ROSA}No se encontró una conversación con '{nombre_buscado}'.{RESET}")
else:
    print(f"{ROSA}No se encontraron hilos de mensajes para mostrar.{RESET}")

input(f"\n{MORADO}Presiona Enter para salir...{RESET}")
