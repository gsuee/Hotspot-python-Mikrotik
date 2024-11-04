import paramiko
import time
import re
import logging
import os
from concurrent.futures import ThreadPoolExecutor

# Configuración de logging
logging.basicConfig(level=logging.INFO)

# lista de ip's
routers = [""]
# credenciales
username = ""
password = ""

def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.recv_exit_status()  
    return stdout.read().decode('utf-8', errors='replace')

def read_morosos_ips(filename):
    if not os.path.exists(filename):
        logging.error(f"El archivo {filename} no existe.")
        return []
    
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def process_router(router):
    try:
        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(router, username=username, password=password, timeout=10)

            hotspot_users_output = execute_command(client, '/ip hotspot user print where dynamic=no')
            ip_hotspot = re.findall(r'10\.\d{1,3}\.\d{1,3}\.\d{1,3}', hotspot_users_output)

            morosos_ips = read_morosos_ips('morosos.txt')

            if not morosos_ips:
                logging.warning("No se encontraron IPs morosas en el archivo. Saliendo del proceso.")
                return

            for ip in ip_hotspot:
                if ip in morosos_ips:
                    cmd = f'/ip hotspot user disable [find comment="{ip}"]'
                    logging.info(f"Desactivando {ip}")
                else:
                    cmd = f'/ip hotspot user enable [find comment="{ip}"]'
                    logging.info(f"Activando {ip}")

                execute_command(client, cmd)

    except paramiko.AuthenticationException:
        logging.error(f"Error de autenticación en {router}.")
    except paramiko.SSHException as e:
        logging.error(f"Error de conexión o ejecución en {router}: {e}")
    except Exception as e:
        logging.error(f"Error desconocido en {router}: {e}")

if __name__ == "__main__":
    morosos_ips = read_morosos_ips('morosos.txt')
    
    if not morosos_ips:
        logging.warning("No se encontraron IPs morosas en el archivo. Saliendo del proceso.")
    else:
        with ThreadPoolExecutor() as executor:
            executor.map(process_router, routers)