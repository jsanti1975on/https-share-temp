# Cisco Lab Master Report

This document combines the **lab configurations** and **troubleshooting notes** into a single reference.

---

# 🔹 Lab Topology Overview

- **East Switch (ESXi Clients)**
- **West Switch (ESXi Servers)**
- **Cisco RV340 Router**
- **Cisco 2504 WLC + AP**
- **vSphere Hosts / VMs**

VLANs:
- VLAN 10 → `172.20.10.0/24` (VM Data)
- VLAN 999 → `10.10.99.0/24` (Management, Native VLAN)

---

# 🔹 East Switch Config

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
ip default-gateway 10.10.99.254

interface range fa0/7 - 8
 description Trunk-to-West
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 channel-protocol lacp
 channel-group 1 mode active
 no shutdown

interface port-channel 1
 description Trunk-to-West
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999

interface range fa0/3 - 4
 description ESXi-Clients
 switchport mode access
 switchport access vlan 10
 channel-protocol lacp
 channel-group 2 mode active
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown

interface port-channel 2
 description ESXi-Clients
 switchport mode access
 switchport access vlan 10
```

---

# 🔹 West Switch Config

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
ip default-gateway 10.10.99.254

interface range fa0/7 - 8
 description Trunk-to-East
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 channel-protocol lacp
 channel-group 1 mode active
 no shutdown

interface port-channel 1
 description Trunk-to-East
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999

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

# 🔹 WLC Configuration (Summary)

- **Management IP:** `10.10.99.10/24`  
- **Default Gateway:** `10.10.99.254`  
- **VLAN:** Untagged (mapped to VLAN 999)  
- **GUI:** Accessible at `https://10.10.99.10`  
- **SSID Homework (planned):**  
  - VLAN Mapping: VLAN 10  
  - WPA2-PSK, AES encryption  

---

# 🔹 Troubleshooting Log

## Issue 1 – Switch-to-Switch & Router Native VLAN Mismatch
- **Symptom:** Native VLAN mismatch messages on trunks.
- **Action:** Standardized all trunks to use **VLAN 999** as the native VLAN.
- **Outcome:** CDP mismatch messages cleared.

## Issue 2 – EtherChannel (LACP) not bundling correctly
- **Symptom:** Ports in **(I) individual** state instead of **(P) bundled**.
- **Action:** Erased configs, reloaded, rebuilt Po1 and Po2 with LACP active.
- **Outcome:** EtherChannel formed successfully `(SU)`.

## Issue 3 – West switch VLAN interface misconfigured
- **Symptom:** West switch picked up DHCP IP on VLAN1 (10.10.99.147).
- **Action:** Disabled VLAN1, created VLAN999 with static IP **10.10.99.3**.
- **Outcome:** East (10.10.99.2) ↔ West (10.10.99.3) ping successful.

## Issue 4 – WLC not reachable on Management VLAN
- **Symptom:** WLC showed mgmt on VLAN999 but unreachable.
- **Actions:** Attempted IP changes (rejected until WLAN disabled).  
  Disabled WLANs, reassigned mgmt IP.  
- **Outcome:** Reset to **untagged VLAN999 (10.10.99.10)**, GUI became reachable.

## Issue 5 – VM-to-WLC communication
- **Symptom:** VM could ping gateway but not WLC. WLC couldn’t ping VM.  
- **Action:** Adjusted ESXi Port Group: `VLAN999-Mgmt` set to untagged.  
- **Outcome:** VM successfully reached WLC GUI.

---

# 🔹 Verification

- East Switch: `10.10.99.2` ✅  
- West Switch: `10.10.99.3` ✅  
- RV340 Router: `10.10.99.254` ✅  
- WLC GUI: `10.10.99.10` ✅  
- VM (Mgmt VLAN): `10.10.99.x` ✅  

---

# 🔹 Next Steps

1. Configure WLAN/SSID `Homework` on WLC.  
2. Verify AP joins the WLC.  
3. Test client connectivity over Wi-Fi.  
4. Lock down management (ACLs, firewall rules).  

---
