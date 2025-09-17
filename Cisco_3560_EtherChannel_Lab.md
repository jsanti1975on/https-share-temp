# Quick and Dirty Topo
<img width="1370" height="593" alt="Quick-Dirty-Topo" src="https://github.com/user-attachments/assets/19b9e796-98d5-447a-9cd0-e91d4a6f024e" />

# Cisco 3560 EtherChannel Lab Configs

This document contains the **fresh EtherChannel configurations** for the East and West 3560 switches.  
Layout uses **Po1 (backbone trunk)** and **Po2 (ESXi uplinks)**.  

---

## 🔹 East Switch (ESXI-CLIENTS side)

```cisco
! ==========================
! East 3560 Configuration
! ==========================
hostname East
no ip domain-lookup
vtp mode transparent

! VLANs
vlan 10
 name VM-Data
vlan 999
 name Native-Mgmt

! Management SVI
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

! EtherChannel Po1 - Trunk to West
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

! EtherChannel Po2 - ESXi Client uplinks
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

## 🔹 West Switch (ESXI-SERV side)

```cisco
! ==========================
! West 3560 Configuration
! ==========================
hostname West
no ip domain-lookup
vtp mode transparent

! VLANs
vlan 10
 name VM-Data
vlan 999
 name Native-Mgmt

! Management SVI
interface vlan 999
 ip address 10.10.99.3 255.255.255.0
 no shutdown
ip default-gateway 10.10.99.1

! EtherChannel Po1 - Trunk to East
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

! EtherChannel Po2 - ESXi Server uplinks
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

## 🔹 Verification Commands

On both East & West:

```cisco
show vlan brief              ! VLANs 10 + 999 present
show interfaces trunk        ! Po1 should show trunk, VLANs 10,999
show etherchannel summary    ! Po1(SU) and Po2(SU), members (P)
```

- Po1 = trunk between switches  
- Po2 = ESXi uplinks  
- Mgmt reachable: East = 10.10.99.2, West = 10.10.99.3  
- VMs in VLAN 10 can ping each other through the backbone  

---
