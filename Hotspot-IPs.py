import paramiko
import re

# Datos de conexión 
hostname = 'ip'
username = 'user'
password = 'psswd'

# Comando MikroTik
command = '/ip firewall address-list print where list=morosos' # modificar para las versiones

# Función para conectar y ejecutar comandos
def connect_and_execute(hostname, username, password, command):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname,username=username, password=password)

    stdin, stdout, stderr = client.exec_command(command)
    output = stdout.read().decode('utf-8')
    client.close()
    return output

# Obtener la salida del comando
output = connect_and_execute(hostname, username, password, command)

# Extraer las direcciones IP - ajusta la expresión regular si es necesario
ip_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
ips = re.findall(ip_pattern, output)

# Guardar las IPs en un archivo .txt
with open('morosos.txt', 'w') as f:
    for ip in ips:
        f.write(ip + '\n')

print("Las direcciones IP se han guardado en morosos.txt")