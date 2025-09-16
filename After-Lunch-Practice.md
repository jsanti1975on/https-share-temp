# Pratice Ether 
✅ Target Topology

East Fa0/1 → RV340 LAN2

Single trunk (dot1q), VLAN 999 native, VLANs 10 & 999 allowed.

East Fa0/7–Fa0/8 ⇔ West Fa0/7–Fa0/8

EtherChannel (Po7) as a trunk between the two switches.

VLAN 999 native, VLANs 10 & 999 allowed.

This gives you:

Router uplink: simple and stable.

East–West core link: EtherChannel trunk = great for practice.

ESXi/vSphere bundles: you can still do Po2/Po3/Po4 for access ports to VLAN 10.

# East 3560 Config
```Yaml
! ====== Uplink to RV340 (single trunk) ======
interface fa0/1
 description Trunk-to-RV340
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 no shutdown

! ====== EtherChannel trunk to West (Fa0/7-8) ======
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
```

# West 3560 Config
```Yaml
! ====== EtherChannel trunk to East (Fa0/7-8) ======
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
```

# 🔎 Verification

> On both East & West:
```Yaml
show etherchannel summary
show interfaces trunk
show spanning-tree vlan 10,999
```

# Expected:

Po7(SU) with Fa0/7(P) + Fa0/8(P)

Native VLAN = 999

Allowed VLANs = 10,999

STP sees Po7 as a single P2p trunk.

⚡ This setup keeps the lab progressing smoothly — RV340 is happy with its single trunk, and you get to practice LACP EtherChannel on your Catalyst switches.

👉 Do you also want me to give you a test plan (e.g. ping between VLANs, shut one member of Po7, watch traffic keep flowing) so you can prove EtherChannel resiliency in your lab?
