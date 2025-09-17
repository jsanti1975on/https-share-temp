
# Cisco Catalyst 3560 Lab Configurations (East + West)

This document contains the full clean configuration for both switches in the isolated RV340 lab.

---

## VLANs
- **VLAN 10** → `172.20.10.0/24` (VM Data)
- **VLAN 999** → `10.10.99.0/24` (Native/Management)

Both VLANs are routed by the Cisco RV340.  
Switches only need `ip default-gateway` for management.

---

## 🔹 East 3560 Config

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

! EtherChannel trunk to West
default interface range fa0/7 - 8
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
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999

! ESXi Client EtherChannel (vmnic2+vmnic3)
default interface range fa0/3 - 4
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

---

## 🔹 West 3560 Config

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

! EtherChannel trunk to East
default interface range fa0/7 - 8
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
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999

! ESXi Server EtherChannel (vmnic2+vmnic3)
default interface range fa0/1 - 2
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

## Verification Commands

On each switch:
```
show vlan brief
show interfaces trunk
show etherchannel summary
```

Expected results:
- `Po7(SU)` with Fa0/7–8 (P)
- `Po2(SU)` with ESXi NICs (P)
- VLAN 10 active, VLAN 999 native
```

---
