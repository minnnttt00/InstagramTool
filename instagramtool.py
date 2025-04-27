import sys
import time
import logging
from instagrapi import Client
import os
from datetime import datetime

# ⚡ COLORES TERMINAL de Instagram
INSTAGRAM_PINK = "\033[38;5;204m"
INSTAGRAM_ORANGE = "\033[38;5;214m"
INSTAGRAM_PURPLE = "\033[38;5;99m"
RESET = "\033[0m"

# 🚀 Contraseña que quieres
CONTRASENA_CORRECTA = "MintToolInstagram"

# 🎯 Pide contraseña antes de arrancar
password = input(f"{INSTAGRAM_PURPLE}Introduce la contraseña para usar la herramienta: {RESET}").strip()

if password != CONTRASENA_CORRECTA:
    print(f"{INSTAGRAM_PINK}❌ Contraseña incorrecta. Cerrando el programa...{RESET}")
    time.sleep(1)
    sys.exit()

print(f"{INSTAGRAM_ORANGE}✅ Contraseña correcta. Bienvenid@ 🔥{RESET}\n")

# Banner con los colores de Instagram
print(f"{INSTAGRAM_PINK}████████╗██████╗░░█████╗░██╗░░░██╗██╗░░░░░")
print(f"{INSTAGRAM_ORANGE}╚══██╔══╝██╔══██╗██╔══██╗██║░░░██║██║░░░░░")
print(f"{INSTAGRAM_PINK}░░░██║░░░██████╔╝██║░░██║██║░░░██║██║░░░░░")
print(f"{INSTAGRAM_ORANGE}░░░██║░░░██╔══██╗██║░░██║██║░░░██║██║░░░░░")
print(f"{INSTAGRAM_PINK}░░░██║░░░██║░░██║╚█████╔╝╚██████╔╝███████╗")
print(f"{INSTAGRAM_ORANGE}░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚═════╝░╚══════╝")
print(f"{INSTAGRAM_PURPLE}                  IG{RESET}")
print(f"{INSTAGRAM_PURPLE}              Created by Mint{RESET}\n")

# Continuamos con el programa
logging.getLogger("instagrapi").setLevel(logging.CRITICAL)

def silent_public_request(self, url, data=None, params=None, headers=None):
    try:
        return self.private_request(url, data=data, params=params, headers=headers)
    except Exception:
        return None

Client.public_request = silent_public_request

cl = Client()

# Pedimos sesión manualmente
try:
    print(f"\n{INSTAGRAM_PURPLE}Introduce tus datos de Instagram:{RESET}")
    username = input(f"{INSTAGRAM_PURPLE}Usuario: {RESET}").strip()
    password = input(f"{INSTAGRAM_PURPLE}Contraseña: {RESET}").strip()

    cl.login(username, password)
    session_id = cl.sessionid
    print(f"\n{INSTAGRAM_ORANGE}Inicio de sesión exitoso!{RESET}")
    print(f"{INSTAGRAM_PURPLE}Tu SESSION ID es: {INSTAGRAM_ORANGE}{session_id}{RESET}\n")

    # Guardamos session_id automáticamente
    with open("session.txt", "w") as f:
        f.write(session_id)

except Exception as e:
    print(f"{INSTAGRAM_PINK}Error al iniciar sesión: {e}{RESET}")
    sys.exit()

# Solución para evitar el error 'NoneType' object has no attribute 'get' en los hilos de mensajes
try:
    threads = cl.direct_threads()
    if threads is None:
        print(f"{INSTAGRAM_PINK}No se encontraron hilos de mensajes.{RESET}")
        sys.exit()
except Exception as e:
    print(f"{INSTAGRAM_PINK}Error al obtener los hilos de mensajes: {e}{RESET}")
    sys.exit()

ultimas_5_personas = []

for thread in threads[:5]:
    if len(thread.users) == 1:
        usuario = thread.users[0].username
    else:
        usuario = ", ".join([user.username for user in thread.users])
    ultimas_5_personas.append(usuario)

print(f"\n{INSTAGRAM_ORANGE}Últimas 5 personas con las que has hablado:{RESET}")
for idx, usuario in enumerate(ultimas_5_personas, start=1):
    print(f"{idx}. {usuario}")

nombre_buscado = input(f"\n{INSTAGRAM_PURPLE}Ingresa el nombre de usuario para ver los últimos mensajes: {RESET}").strip()

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
    print(f"\n{INSTAGRAM_ORANGE}Últimos mensajes con {nombre_buscado} (Total de mensajes: {total_mensajes}):{RESET}")
    
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
    print(f"\n{INSTAGRAM_PINK}No se encontró una conversación con '{nombre_buscado}'.{RESET}")

input(f"\n{INSTAGRAM_PURPLE}Presiona Enter para salir...{RESET}") 
