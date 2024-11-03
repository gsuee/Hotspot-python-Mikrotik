import paramiko
import time
import re

# lista de ip's
routers = ["ip"]
# credenciales
username = "user"
password = "psswd"


def execute_command(client, command):
    stdin, stdout, stderr = client.exec_command(command)
    time.sleep(2) 
    return stdout.read().decode('utf-8', errors='replace')


def read_morosos_ips(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip()]

# lectura del archivo .txt
morosos_ips = read_morosos_ips('morosos.txt')

for router in routers:
    try:
        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(router, username=username, password=password, timeout=10)
            
            
            hotspot_users_output = execute_command(client, '/ip hotspot user print where dynamic=no')
            ip_hotspot = re.findall(r'10\.\d{1,3}\.\d{1,3}\.\d{1,3}', hotspot_users_output)
            
            
            for ip in ip_hotspot:
                if ip in morosos_ips:
                    cmd = f'/ip hotspot user disable [find comment="{ip}"]'
                    print(f"Desactivando {ip}")
                else:
                    cmd = f'/ip hotspot user enable [find comment="{ip}"]'
                    print(f"Activando {ip}")
                
                
                execute_command(client, cmd)

    except paramiko.AuthenticationException:
        print(f"Error de autenticación en {router}.")
    except paramiko.SSHException as e:
        print(f"Error de conexión o ejecución en {router}: {e}")
    except Exception as e:
        print(f"Error desconocido en {router}: {e}")
