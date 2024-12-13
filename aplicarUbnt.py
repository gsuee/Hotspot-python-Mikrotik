import ipaddress
import paramiko

def configure_system(ip_address, url):
    # Configuración de la conexión SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        ssh.connect(ip_address, username='admin', password='tecomcliente1.')
        
        # Crear el archivo de configuración
        commands = f"echo -e 'unms.uri={url}\\nunms.status=enabled' > /tmp/system.cfg"
        stdin, stdout, stderr = ssh.exec_command(commands)
        stdin.close()
        
        # Esperar a que se complete el comando
        stdout.channel.recv_exit_status()
        
        # Ejecutar los comandos de guardado y reinicio
        restart_command = '/usr/etc/rc.d/rc.softrestart save && reboot'
        stdin, stdout, stderr = ssh.exec_command(restart_command)
        stdin.close()
        
        # Esperar a que se complete el comando
        stdout.channel.recv_exit_status()
        
    except paramiko.SSHException as e:
        print(f"Error de conexión SSH a {ip_address}: {e}")
    except Exception as e:
        print(f"Error al configurar {ip_address}: {e}")
    finally:
        ssh.close()

# Rango de IP
ip_network = ipaddress.ip_network('10.101.8.10')  # Cambiado a un rango válido
url = "wss://planotelecom.uisp.com:443+uKqKRzIArDPIP5vrl9MX2mjucPRZ04xbZqRUQsjklp5ST1sp+allowSelfSignedCertificate"

# Iterar sobre las direcciones IP y configurar
for ip in ip_network.hosts():
    configure_system(str(ip), url)