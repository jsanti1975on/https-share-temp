
# Isolated Lab Network - Cisco RV340 + Catalyst 3560 + ESXi Hosts

This lab isolates pfSense (on vmnic0) from the Cisco lab network.  
Only **vmnic2 + vmnic3** are used for the Cisco RV340 / Catalyst lab.  
**vmnic1 remains unused.**

---

## VLANs
- **VLAN 10** → `172.20.10.0/24` (VM Data, Clients + Servers)
- **VLAN 999** → `10.10.99.0/24` (Native/Management)

Both VLANs are routed by the **Cisco RV340**.

---

## RV340 Configuration

### VLANs
- VLAN 10 → IP: `172.20.10.1/24` (DHCP ON for VMs)
- VLAN 999 → IP: `10.10.99.1/24` (optional DHCP)

### LAN2 Port (Uplink to East Fa0/1)
- VLAN 999 = **Untagged**
- VLAN 10  = **Tagged**
- VLAN 1   = **Excluded**
- All others = Excluded

Save + reboot.

---

## East 3560 Config

```cisco
hostname East
no ip domain-lookup
vtp mode transparent

! VLANs
vlan 10
 name VM-Data
vlan 999
 name Native-Mgmt

! Management SVI (switch mgmt only)
interface vlan 999
 ip address 10.10.99.2 255.255.255.0
 no shutdown
ip default-gateway 10.10.99.1

! Uplink to RV340 (single trunk)
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

! ESXi CLIENT host (vmnic2+vmnic3) - VLAN 10
default interface range fa0/3 - 4
interface range fa0/3 - 4
 description ESXi-Client (vmnic2,vmnic3)
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

## West 3560 Config

```cisco
hostname West
no ip domain-lookup
vtp mode transparent

! VLANs
vlan 10
 name VM-Data
vlan 999
 name Native-Mgmt

! Management SVI (switch mgmt only)
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

! ESXi SERVER host (vmnic2+vmnic3) - VLAN 10
default interface range fa0/1 - 2
interface range fa0/1 - 2
 description ESXi-Server (vmnic2,vmnic3)
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

## ESXi Host Configuration

### vmnic0 → pfSense (isolated mgmt)
- Connected to pfSense switch/firewall
- Used for ESXi management / reservations
- **Not connected to Cisco 3560s**

### vmnic1 → Unused

### vmnic2 + vmnic3 → Cisco RV340 Lab
- Assigned to `vSwitch1` (or DVS)
- NIC Teaming = **LACP Active** (vDS) or **Route based on IP hash** (vSS)
- Port Group = `VM-Data`, VLAN ID = 10
- Windows VMs connect here → get DHCP from RV340

---

## Cabling Map

- **RV340 LAN2 ⇔ East Fa0/1** (trunk: VLAN 999 untagged, VLAN 10 tagged)
- **East Fa0/7 ⇔ West Fa0/7**
- **East Fa0/8 ⇔ West Fa0/8** (Po7 EtherChannel)
- **East Fa0/3 ⇔ ESXi-Client vmnic2**
- **East Fa0/4 ⇔ ESXi-Client vmnic3**
- **West Fa0/1 ⇔ ESXi-Server vmnic2**
- **West Fa0/2 ⇔ ESXi-Server vmnic3**

---

## Verification

On East/West:
```
show vlan brief
show interfaces trunk
show etherchannel summary
```

Expected:
- `Po7(SU)` with Fa0/7–8 (P)
- `Po2(SU)` for each ESXi host bundle
- VLAN 10 active, VLAN 999 native

On ESXi VMs:
- Client VM → IP `172.20.10.x`, GW `172.20.10.1`
- Server VM → IP `172.20.10.y`, GW `172.20.10.1`
- Test ping between Client ↔ Server

On Mgmt:
- East mgmt reachable at `10.10.99.2`

 ==============================================

# East 3560 (no L3 routing — RV340 does it)
```Yaml
hostname East
no ip domain-lookup
vtp mode transparent

vlan 10
 name VM-Data
vlan 999
 name Native-Mgmt

! mgmt SVI so you can reach the switch on the RV340 mgmt subnet
interface vlan 999
 ip address 10.10.99.2 255.255.255.0
 no shutdown
ip default-gateway 10.10.99.1

! trunk to RV340
interface fa0/1
 description Uplink-to-RV340
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 no shutdown

! LACP trunk to West
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

! ESXi CLIENT host uplinks (vmnic2+vmnic3) as ACCESS VLAN 10
default interface range fa0/3 - 4
interface range fa0/3 - 4
 description ESXi-Client (vmnic2,vmnic3)
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
- West mgmt reachable at `10.10.99.3`
```

# West 3560 (no L3 routing — RV340 does it)
```Yaml
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

! LACP trunk to East
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

! ESXi SERVER host uplinks (vmnic2+vmnic3) as ACCESS VLAN 10
default interface range fa0/1 - 2
interface range fa0/1 - 2
 description ESXi-Server (vmnic2,vmnic3)
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

ESXi hosts (how to avoid vmnic0)

vSwitch0 / Management (pfSense):

Only vmnic0 attached.

Management VMkernel (vmk0) stays here on the pfSense network.

This vSwitch is not connected to the Cisco 3560s.

vSwitch1 / Data for VMs (Cisco/RV340):

Uplinks = vmnic2 + vmnic3 (team them with LACP if using a vDS; on vSS use Route based on IP hash).

Port Group: VM-Data with VLAN ID 10.

Place your Windows VMs here (they’ll get DHCP from RV340 in 172.20.10.0/24).

Leave vmnic1 unused (no uplinks/port groups).

Bring-up checklist (quick)

RV340: confirm LAN2 shows 999=U, 10=T, 1=E.

East/West:

show interfaces trunk → Po7 as trunk (10,999; native 999)

show etherchannel summary → Po7(SU), Po2(SU) on each switch

show vlan brief → ports for ESXi Po2 not in VLAN 1

ESXi:

vSwitch1 has vmnic2+vmnic3 active; Port Group VLAN 10; IP-hash/LACP set

VMs get 172.20.10.x/24, GW 172.20.10.1

Mgmt reachability (optional): from your laptop on 10.10.99.0/24, ping East 10.10.99.2, West 10.10.99.3.
