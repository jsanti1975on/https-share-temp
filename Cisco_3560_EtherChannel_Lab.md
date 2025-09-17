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

! Global STP Best Practices
spanning-tree mode pvst
spanning-tree portfast default
spanning-tree bpduguard default

! VLANs
vlan 10
 name VM-Data
vlan 999
 name Native-Mgmt

! Management SVI
interface vlan 999
 ip address 10.10.99.2 255.255.255.0
 no shutdown
ip default-gateway 10.10.99.254

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
 description Backbone-Trunk-East-West
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
 description ESXi-Clients-Uplink
 switchport mode access
 switchport access vlan 10

end
write memory

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

! Global STP Best Practices
spanning-tree mode pvst
spanning-tree portfast default
spanning-tree bpduguard default

! VLANs
vlan 10
 name VM-Data
vlan 999
 name Native-Mgmt

! Management SVI
interface vlan 999
 ip address 10.10.99.3 255.255.255.0
 no shutdown
ip default-gateway 10.10.99.254

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
 description Backbone-Trunk-East-West
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
 description ESXi-Server-Uplink
 switchport mode access
 switchport access vlan 10

end
write memory

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

'=== Break: Morning Meal and after start below ===

# vSphere Host Configuration for Cisco EtherChannel Lab

This document outlines how to configure ESXi hosts to integrate with the Cisco 3560 EtherChannel lab.

---

## 🔹 Uplinks

- **East ESXi Host** → `vmnic2 + vmnic3` (connected to East Po2: Fa0/3–4)  
- **West ESXi Host** → `vmnic2 + vmnic3` (connected to West Po2: Fa0/1–2)  
- Avoid `vmnic0` (pfSense mgmt) and leave `vmnic1` unused.  

---

## 🔹 Create a vSwitch

1. Log into **vSphere Web Client**.  
2. Go to **Networking → Virtual Switches**.  
3. Create a **new standard vSwitch (vSwitch1)**.  
4. Add uplinks: `vmnic2` + `vmnic3`.  

---

## 🔹 Set NIC Teaming Policy

### For Standard vSwitch:
- Go to **vSwitch1 Properties → NIC Teaming**.  
- Change **Load Balancing** to:  
  ✅ **Route based on IP hash**.  
- Failback: Yes.  
- Notify switches: Yes.  

### For Distributed vSwitch (vDS):
- On the **LAG uplink group**, set **Mode = LACP Active**.  

👉 This ensures consistency with Cisco EtherChannel/LACP which requires **IP hash** load balancing.

---

## 🔹 Create Port Group

- Port Group Name: `VM-Data`  
- VLAN ID: **10**  
- Assign test VMs (Client on East, Server on West) to this port group.  

---

## 🔹 Assign VM IPs

- **East Client VM**  
  - IP: `172.20.10.20`  
  - Mask: `255.255.255.0`  
  - GW: `172.20.10.254`  

- **West Server VM**  
  - IP: `172.20.10.30`  
  - Mask: `255.255.255.0`  
  - GW: `172.20.10.254`  

---

## 🔹 Test Connectivity

On each VM:
- Ping each other (`172.20.10.20 ↔ 172.20.10.30`).  
- Ping default gateway (`172.20.10.254`).  

On Cisco switches:
```cisco
show etherchannel summary
show interfaces port-channel 2
```
- Expect **Po2 (SU)** with member links in **P** (bundled).  

---

✅ At this point:  
- Po1 = backbone trunk (East⇔West).  
- Po2 = ESXi uplinks (per side).  
- VLAN 10 = end-to-end for VMs.  
- VLAN 999 = management, isolated.
