
# Cisco 3560 EtherChannel Lab with Homework Transfer Automation

This design uses **two Cisco Catalyst 3560s**, an **RV340 router**, and **two ESXi hosts** 
to simulate a lab where students upload homework to a **Web server (West)** 
and a Python script automatically transfers files nightly to a **Projects server (East)**.

---

## VLANs
- **VLAN 10** → `172.20.10.0/24` (VM Data, Clients + Servers)
- **VLAN 999** → `10.10.99.0/24` (Native / Management)

Both VLANs are routed by the **Cisco RV340**.  
Switches use `ip default-gateway` for management only.

---

## Lab Cabling

- **RV340 LAN2 ⇔ East Fa0/1** (trunk: VLAN 999 untagged, VLAN 10 tagged)
- **East Fa0/7 ⇔ West Fa0/7**
- **East Fa0/8 ⇔ West Fa0/8** (Po7 EtherChannel trunk)
- **East Fa0/3 ⇔ ESXi-Client vmnic2**
- **East Fa0/4 ⇔ ESXi-Client vmnic3**
- **West Fa0/1 ⇔ ESXi-Server vmnic2**
- **West Fa0/2 ⇔ ESXi-Server vmnic3**

---

## Switch Config Highlights

### East 3560
```cisco
hostname East
no ip domain-lookup
vtp mode transparent

vlan 10
 name VM-Data
vlan 999
 name Native-Mgmt

interface vlan 999
 ip address 10.10.99.2 255.255.255.0
 no shutdown
ip default-gateway 10.10.99.1

! Uplink to RV340
interface fa0/1
 description Uplink-to-RV340
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 no shutdown

! EtherChannel trunk to West
interface range fa0/7 - 8
 description Trunk-to-West
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 channel-protocol lacp
 channel-group 7 mode active
 no shutdown

interface port-channel 7
 description Trunk-to-West
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999

! ESXi Client host (vmnic2+vmnic3)
interface range fa0/3 - 4
 description ESXi-Client
 switchport mode access
 switchport access vlan 10
 channel-protocol lacp
 channel-group 2 mode active
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown

interface port-channel 2
 description ESXi-Client
 switchport mode access
 switchport access vlan 10
```

### West 3560
```cisco
hostname West
no ip domain-lookup
vtp mode transparent

vlan 10
 name VM-Data
vlan 999
 name Native-Mgmt

interface vlan 999
 ip address 10.10.99.3 255.255.255.0
 no shutdown
ip default-gateway 10.10.99.1

! EtherChannel trunk to East
interface range fa0/7 - 8
 description Trunk-to-East
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 channel-protocol lacp
 channel-group 7 mode active
 no shutdown

interface port-channel 7
 description Trunk-to-East
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999

! ESXi Server host (vmnic2+vmnic3)
interface range fa0/1 - 2
 description ESXi-Server
 switchport mode access
 switchport access vlan 10
 channel-protocol lacp
 channel-group 2 mode active
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown

interface port-channel 2
 description ESXi-Server
 switchport mode access
 switchport access vlan 10
```

---

## ESXi Host Setup

- **vmnic0 → pfSense (isolated mgmt)**  
- **vmnic1 → Unused**  
- **vmnic2 + vmnic3 → Cisco RV340/3560 lab**  
  - On vSS: Teaming = *Route based on IP hash*  
  - On vDS: LACP Active  
  - Port Group `VM-Data` → VLAN ID 10  

- **Web Server VM (West)**: `172.20.10.20/24`, GW `172.20.10.1`  
- **Projects Server VM (East)**: `172.20.10.30/24`, GW `172.20.10.1`  

---

## Automated Homework Transfer

Nightly job copies new uploads from **West (web server)** → **East (projects server)**.

### Python Script (West Web Server)
```python
import os, time, shutil
import paramiko

SRC_DIR = "/var/www/uploads"
DST_HOST = "172.20.10.30"
DST_DIR  = "/srv/projects/incoming"
ARCHIVE  = "/var/www/uploads_archive"
USER     = "labsvc"
KEYFILE  = "/home/labsvc/.ssh/id_rsa"

def sftp_put_dir(sftp, src_dir, dst_dir):
    for root, _, files in os.walk(src_dir):
        rel = os.path.relpath(root, src_dir)
        remote_root = dst_dir if rel == "." else f"{dst_dir}/{rel}"
        try:
            sftp.stat(remote_root)
        except IOError:
            sftp.mkdir(remote_root)
        for f in files:
            local_f = os.path.join(root, f)
            remote_f = f"{remote_root}/{f}"
            sftp.put(local_f, remote_f)

if __name__ == "__main__":
    if not any(os.scandir(SRC_DIR)):
        exit(0)
    k = paramiko.RSAKey.from_private_key_file(KEYFILE)
    t = paramiko.Transport((DST_HOST, 22))
    t.connect(username=USER, pkey=k)
    sftp = paramiko.SFTPClient.from_transport(t)
    sftp_put_dir(sftp, SRC_DIR, DST_DIR)
    sftp.close(); t.close()

    stamp = time.strftime("%Y%m%d")
    dest = f"{ARCHIVE}/{stamp}"
    os.makedirs(dest, exist_ok=True)
    for entry in os.scandir(SRC_DIR):
        shutil.move(os.path.join(SRC_DIR, entry.name), os.path.join(dest, entry.name))
```

### Schedule (Linux)
```
crontab -e
0 23 * * * /usr/bin/python3 /opt/mover/move_homework.py
```

---

## Validation Checklist

1. **Switch EtherChannel**
```
show etherchannel summary
show interfaces trunk
show vlan brief
```
- Expect Po7(SU) with Fa0/7–8(P)
- Expect Po2(SU) on each switch for ESXi hosts

2. **IP Connectivity**
- Web server VM → ping Projects VM  
- Both VMs → ping gateway `172.20.10.1` (RV340)  
- Switch mgmt reachable at `10.10.99.2` (East), `10.10.99.3` (West)

3. **Resiliency Demo**
- Start large upload  
- On East: `shutdown fa0/7`  
- Transfer continues over Fa0/8  
- `no shutdown fa0/7` → bundle recovers

# Cisco 2504 WLC Configuration for Lab

This document outlines the Wireless LAN Controller (WLC) configuration to support the **Homework SSID**, integrated with the East/West 3560 switches and RV340.

---

## 🔹 Step 1: Management Interface (VLAN 999)

```plaintext
(Cisco Controller) config interface address management 10.10.99.10 255.255.255.0 10.10.99.254
(Cisco Controller) config interface vlan management 999
(Cisco Controller) save config
```

- WLC management IP: **10.10.99.10**
- VLAN: **999 (Native-Mgmt)**
- Default gateway: **10.10.99.254 (RV340)**

---

## 🔹 Step 2: Create Dynamic Interface for VLAN 10

```plaintext
(Cisco Controller) config interface create VM-Data 10
(Cisco Controller) config interface address VM-Data 172.20.10.10 255.255.255.0 172.20.10.254
(Cisco Controller) save config
```

- Interface: **VM-Data**
- VLAN: **10**
- IP: **172.20.10.10**
- Gateway: **172.20.10.254 (RV340)**

---

## 🔹 Step 3: WLAN Creation - SSID `Homework`

```plaintext
(Cisco Controller) wlan create 1 Homework Homework
(Cisco Controller) wlan interface 1 VM-Data
(Cisco Controller) wlan security wpa2 enable
(Cisco Controller) wlan security wpa2 ciphers aes enable
(Cisco Controller) wlan security wpa akm psk set-key ascii MyStrongPassword 1
(Cisco Controller) wlan enable 1
(Cisco Controller) save config
```

- SSID: **Homework**
- VLAN Mapping: **10 (VM-Data)**
- Security: **WPA2-PSK (AES)**

---

## 🔹 Step 4: Verify AP Registration

After cabling the Cisco AP to the West 3560 (PoE enabled):

```plaintext
(Cisco Controller) show ap summary
```

- APs should list here when successfully joined.

---

## ✅ Summary

- WLC Mgmt: **10.10.99.10 (VLAN 999)**
- SSID `Homework` bound to VLAN 10 (172.20.10.0/24)
- Wireless clients get DHCP from RV340
- Traffic passes through EtherChannel backbone between East & West



---

This completes the lab where homework uploads are collected on the **West Web Server VM**, 
then **automatically moved nightly** to the **East Projects VM**, across an **EtherChannel-backed Cisco network**.
