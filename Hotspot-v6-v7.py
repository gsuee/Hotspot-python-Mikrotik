import paramiko 
import time
import re 
#lista de ip's (router's)
routers = ["ip", "ip","ip"]
#datos de acceso
username = "usuarios"
password = "clave"
#--------------------------------------------------------------------------------

for router in routers:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(router, username=username, password=password, timeout=10)
        
        try:
            channel = client.invoke_shell()
            time.sleep(3)
            stdin, stdout, stderr = client.exec_command('/ip firewall/address-list/print where list=morosos') #v7 - modificar para v6
            time.sleep(2) 
            morosos_output = stdout.read().decode()
            
            ip_morosos = re.findall(r'10\.\d{1,3}\.\d{1,3}\.\d{1,3}', morosos_output)
            
            stdin, stdout, stderr = client.exec_command('/ip hotspot user print where dynamic=no')
            time.sleep(2)  
            hotspot_users_output = stdout.read().decode('utf-8', errors='replace')
            
            ip_hotspot = re.findall(r'10\.\d{1,3}\.\d{1,3}\.\d{1,3}', hotspot_users_output)
            
            for ip in ip_hotspot:
                
                if ip in ip_morosos:
                    cmd = f'/ip hotspot user disable [find comment="{ip}"]'
                    print(f"Desactivando {ip}")
                else:
                    cmd = f'/ip hotspot user enable [find comment="{ip}"]'
                    print(f"Activando {ip}")
                stdin, stdout, stderr = client.exec_command(cmd)
                time.sleep(2)  
                
        except paramiko.SSHException as e:
            print(f"Error ejecutando comandos en {router}: {e}")
        finally:
            client.close()
    
    except paramiko.AuthenticationException as e:
        print(f"Error de autenticación en {router}: {e}")
    except Exception as e:
        print(f"Error desconocido en {router}: {e}")



        