import sys
import time
import logging
from instagrapi import Client
import os
from datetime import datetime

# ⚡ COLORES TERMINAL
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"

# 🚀 Contraseña que quieres
CONTRASENA_CORRECTA = "MintToolInstagram"

# 🎯 Pide contraseña antes de arrancar
password = input(f"{YELLOW}Introduce la contraseña para usar la herramienta: {RESET}").strip()

if password != CONTRASENA_CORRECTA:
    print(f"{RED}❌ Contraseña incorrecta. Cerrando el programa...{RESET}")
    time.sleep(1)
    sys.exit()

print(f"{GREEN}✅ Contraseña correcta. Bienvenid@ 🔥{RESET}\n")

# Continuamos con el programa
logging.getLogger("instagrapi").setLevel(logging.CRITICAL)

def silent_public_request(self, url, data=None, params=None, headers=None):
    try:
        return self.private_request(url, data=data, params=params, headers=headers)
    except Exception:
        return None

Client.public_request = silent_public_request

cl = Client()

print(f"{YELLOW}Bienvenido a {GREEN}INSTAGRAMTOOL{YELLOW} by {GREEN}Mint{RESET}")

# Intentamos cargar el session_id desde el archivo
if os.path.exists("session.txt"):
    with open("session.txt", "r") as f:
        session_id = f.read().strip()
    cl.set_sessionid(session_id)
    print(f"{GREEN}✅ Session ID cargado con éxito.{RESET}\n")
else:
    # Si no existe el archivo de sesión, pedimos los datos de login
    try:
        print(f"\n{YELLOW}Introduce tus datos de Instagram:{RESET}")
        username = input(f"{YELLOW}Usuario: {RESET}").strip()
        password = input(f"{YELLOW}Contraseña: {RESET}").strip()

        cl.login(username, password)
        session_id = cl.sessionid
        print(f"\n{GREEN}Inicio de sesión exitoso!{RESET}")
        print(f"{YELLOW}Tu SESSION ID es: {GREEN}{session_id}{RESET}\n")

        # Guardamos session_id automáticamente
        with open("session.txt", "w") as f:
            f.write(session_id)

    except Exception as e:
        print(f"{RED}Error al iniciar sesión: {e}{RESET}")
        sys.exit()

# Después de iniciar sesión, damos la opción de ingresar el session_id manualmente
while True:
    ingresar_session_id = input(f"{YELLOW}¿Quieres ingresar un session_id manualmente? (s/n): {RESET}").strip().lower()
    
    if ingresar_session_id == 's':
        session_id_manual = input(f"{YELLOW}Introduce tu SESSION ID: {RESET}").strip()
        cl.set_sessionid(session_id_manual)
        print(f"{GREEN}✅ Session ID actualizado. Ahora puedes usar la herramienta.{RESET}\n")
        break
    elif ingresar_session_id == 'n':
        break
    else:
        print(f"{RED}❌ Opción no válida. Por favor, elige 's' o 'n'.{RESET}")

# Aquí puedes continuar con el resto de la funcionalidad de la herramienta.
try:
    threads = cl.direct_threads()
except Exception as e:
    print(f"{RED}Error al obtener los hilos de mensajes: {e}{RESET}")
    sys.exit()

ultimas_5_personas = []

for thread in threads[:5]:
    if len(thread.users) == 1:
        usuario = thread.users[0].username
    else:
        usuario = ", ".join([user.username for user in thread.users])
    ultimas_5_personas.append(usuario)

print(f"\n{GREEN}Últimas 5 personas con las que has hablado:{RESET}")
for idx, usuario in enumerate(ultimas_5_personas, start=1):
    print(f"{idx}. {usuario}")

nombre_buscado = input(f"\n{YELLOW}Ingresa el nombre de usuario para ver los últimos mensajes: {RESET}").strip()

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
    print(f"\nÚltimos mensajes con {nombre_buscado} (Total de mensajes: {total_mensajes}):\n")
    
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
    print(f"\n{RED}No se encontró una conversación con '{nombre_buscado}'.{RESET}")

input(f"\n{YELLOW}Presiona Enter para salir...{RESET}")
