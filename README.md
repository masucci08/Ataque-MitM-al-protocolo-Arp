# Ejecucion de Script-Scapy MitM al protocolo Arp 

**Estudiante:** Masucci Franco Rincón  
**Matrícula:** 2024-1250  
**Asignatura:** Seguridad de Redes  
**Fecha:** 6/02/2026  

**Link del video**: https://itlaedudo-my.sharepoint.com/:v:/g/personal/20241250_itla_edu_do/IQAIbt-8mo5xRI39xOkHBtAoAUHMBDqzml5fk1mCWopYizk?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=oDB39Q
 
 ## 1. Descripción y Topología 

El laboratorio se ha desplegado en un entorno virtualizado utilizando **GNS3**, simulando una infraestructura de red corporativa vulnerada desde el interior.

### Detalles de la Topología
* **Segmentación de Red:** Se ha configurado la **VLAN 1** (basada en los últimos 4 dígitos de la matrícula).
* **Direccionamiento IP:** Subred `10.20.12.0/24`.
* **Infraestructura:**
    * **Gateway (R1):** Configurado como *Router-on-a-Stick* en la interfaz `e0/0` con IP `10.20.12.1`.
    * **Switch (Sw1):** Puertos de acceso configurados en la VLAN 1.
* **Recursos:**
    * **Atacante:** gns3attack (IP asignada: `10.20.12.254`).
    * **Víctima:** VPCS 1 (IP asignada: `10.20.12.50`).

<img width="649" height="341" alt="topo" src="https://github.com/user-attachments/assets/8dc6a173-aca5-490b-ba0d-bfff1e6e42e5" />


### Tabla de Direccionamiento

| Dispositivo | Interfaz | Dirección IP | Máscara de Subred | Gateway Predeterminado |
| :--- | :--- | :--- | :--- | :--- |
| **R1** | e0/0 | 10.20.12.1 | 255.255.255/24 |    |
| **Sw1** | VLAN 1 | 10.20.12.2 (Gestión) | 255.255.255.0/24 | 10.20.12.1 |
| **gns3attack (vtacante)** | eth0 | 10.20.12.254 | 255.255.255.0/24 | 10.20.12.1 |
| **VPCS (víctima)** | e0/0 | 10.29.12.50  | 255.255.255.0/24 | 10.20.12.1 |

---

## 2. Requisitos Previos y Herramientas

Para la ejecución exitosa de estos scripts, se requiere el siguiente entorno:

* **Sistema Operativo:** Kali Linux o cualquier distribución Linux basada en Debian.
* **Lenguaje:** Python 3.x.
* **Librerías:** `Scapy` (Instalación: `sudo apt install python3-scapy`).
* **Privilegios:** Acceso **Root** (sudo) es obligatorio para la inyección de paquetes en crudo y la manipulación de interfaces de red.

---
 Man-in-the-Middle (ARP Spoofing)

### Objetivo del Script
El script `arp_attack.py` intercepta el tráfico confidencial entre la víctima (PC1) y la puerta de enlace (Gateway). Aprovecha la naturaleza "sin estado" (stateless) del protocolo ARP para envenenar la caché ARP de ambos objetivos.



### Evidencia de Ejecución
## 1- 
<img width="301" height="241" alt="ejecucion scapy" src="https://github.com/user-attachments/assets/b1f06929-f0c5-489c-a7ca-588747c05629" />


## 2- 
<img width="304" height="244" alt="arpexe1" src="https://github.com/user-attachments/assets/ac8ef7cf-bafc-4715-8a10-1aa97ec74cd2" />
<img width="302" height="224" alt="arpexe2" src="https://github.com/user-attachments/assets/6d045e5d-81a9-465b-92fd-9263e94104ae" />


## 3-
<img width="620" height="318" alt="arpcap" src="https://github.com/user-attachments/assets/ca6a5a30-b5a1-4f9a-92f3-7fb7582ad80d" />






---

## 5. Medidas de Mitigación


### Contra ARP Spoofing
1.  **Dynamic ARP Inspection (DAI):** Característica de seguridad en switches Cisco que inspecciona paquetes ARP y descarta aquellos que no coinciden con la base de datos de asignación de DHCP.
    ```bash
    Enable
    conf t
     ip arp inspection vlan 1
     interface e0/0 (Uplink)
    ip arp inspection trust
