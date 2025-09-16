🖥️ Lab Design Overview
East 3560 (Clients side)

Fa0/1 → RV340 (single trunk uplink, VLANs 10, 20, 999).

Fa0/7–8 → West 3560 (EtherChannel trunk Po7, VLANs 10, 20, 999).

Fa0/3–4 → vSphere Host1 (clients) (EtherChannel Po2, access VLAN 10).

Provides clients VLAN 10, routes to servers VLAN 20.

West 3560 (Servers + Wireless)

Fa0/7–8 → East 3560 (EtherChannel trunk Po7, VLANs 10, 20, 999).

Fa0/1–2 → Server LAG (Po2, access VLAN 20).

Fa0/8 → WLC (access VLAN 10 for simplicity; could trunk later if multiple SSIDs).

Provides servers VLAN 20, also extends VLAN 10 for wireless clients.

Routing

Both switches will do Inter-VLAN routing (SVIs).

VLAN 999 = native transit (management).

VLAN 10 = Clients (East, wireless users).

VLAN 20 = Servers (West).

Use OSPF between East and West for dynamic routing (so you practice).

🔹 VLAN Plan

VLAN 10 = Clients (East ESXi clients + Wireless users)

VLAN 20 = Servers (West server farm)

VLAN 999 = Native/Transit (for trunks, mgmt optional)

🔹 East 3560 Config
```Yaml
hostname East
no ip domain-lookup
ip routing

! VLANs
vlan 10
 name Clients
vlan 20
 name Servers
vlan 999
 name Transit

! SVIs for routing
interface vlan 10
 ip address 10.10.10.1 255.255.255.0
 no shutdown
interface vlan 20
 ip address 10.20.20.1 255.255.255.0
 no shutdown
interface vlan 999
 ip address 10.99.99.1 255.255.255.0
 no shutdown

! Trunk to RV340
interface fa0/1
 description Trunk-to-RV340
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,999
 no shutdown

! EtherChannel trunk to West
default interface range fa0/7 - 8
interface range fa0/7 - 8
 description Trunk-to-West
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,999
 channel-protocol lacp
 channel-group 7 mode active
 no shutdown

interface port-channel 7
 description Trunk-to-West
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,999

! EtherChannel to vSphere (clients VLAN 10)
default interface range fa0/3 - 4
interface range fa0/3 - 4
 description vSphere-Clients
 switchport mode access
 switchport access vlan 10
 channel-protocol lacp
 channel-group 2 mode active
 no shutdown

interface port-channel 2
 description vSphere-Clients
 switchport mode access
 switchport access vlan 10

! OSPF routing
router ospf 1
 network 10.10.10.0 0.0.0.255 area 0
 network 10.20.20.0 0.0.0.255 area 0
 network 10.99.99.0 0.0.0.255 area 0
```
🔹 West 3560 Config
```Yaml
hostname West
no ip domain-lookup
ip routing

! VLANs
vlan 10
 name Clients
vlan 20
 name Servers
vlan 999
 name Transit

! SVIs for routing
interface vlan 10
 ip address 10.10.10.2 255.255.255.0
 no shutdown
interface vlan 20
 ip address 10.20.20.2 255.255.255.0
 no shutdown
interface vlan 999
 ip address 10.99.99.2 255.255.255.0
 no shutdown

! EtherChannel trunk to East
default interface range fa0/7 - 8
interface range fa0/7 - 8
 description Trunk-to-East
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,999
 channel-protocol lacp
 channel-group 7 mode active
 no shutdown

interface port-channel 7
 description Trunk-to-East
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,20,999

! EtherChannel to Servers (VLAN 20)
default interface range fa0/1 - 2
interface range fa0/1 - 2
 description Server-Bundle
 switchport mode access
 switchport access vlan 20
 channel-protocol lacp
 channel-group 2 mode active
 no shutdown

interface port-channel 2
 description Server-Bundle
 switchport mode access
 switchport access vlan 20

! Wireless Controller (simple, VLAN 10 access)
interface fa0/8
 description WLC
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 no shutdown

! OSPF routing
router ospf 1
 network 10.10.10.0 0.0.0.255 area 0
 network 10.20.20.0 0.0.0.255 area 0
 network 10.99.99.0 0.0.0.255 area 0
```
🔎 Testing Plan

EtherChannel

show etherchannel summary → Po7(SU) with (P) members on East & West.

Shut Fa0/7 on East → Po7 stays up via Fa0/8.

Routing

Client VM in VLAN 10 on East → ping server in VLAN 20 on West (routed by the switches).

Wireless client (Homework SSID on WLC) → ping server in VLAN 20.

OSPF

show ip ospf neighbor → East & West adjacency on VLAN 999 SVI.

Verify route tables: show ip route ospf.

✅ With this design:

East = client side (ESXi bundles).

West = server side (server bundle + WLC).

RV340 = single trunk for Internet/L3 WAN edge.

Inter-VLAN routing + dynamic routing are fully demoed.

EtherChannel = practiced East⇔West, East⇔ESXi, West⇔Servers.
