# East switch conf
```bash
!
hostname East
no ip domain-lookup
service password-encryption
!
spanning-tree mode pvst
spanning-tree portfast default
spanning-tree bpduguard default
errdisable recovery cause all
errdisable recovery interval 30
!
vlan 10
 name VM-Network
vlan 999
 name Native-Transit
!
! ====== Port-channel 1 (RV340 LAG1: Fa0/1-2) ======
interface range fa0/1 - 2
 description Uplink-to-RV340
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 channel-group 1 mode active
 no shutdown
!
interface port-channel 1
 description LAG-to-RV340
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
!
! ====== Port-channel 2 (ESXi / Test1: Fa0/3-4) ======
interface range fa0/3 - 4
 description ESXi-Test-Bundle1
 switchport mode access
 switchport access vlan 10
 channel-group 2 mode active
 no shutdown
!
interface port-channel 2
 description ESXi-Test-Bundle1
 switchport mode access
 switchport access vlan 10
!
! ====== Port-channel 3 (ESXi / Test2: Fa0/5-6) ======
interface range fa0/5 - 6
 description ESXi-Test-Bundle2
 switchport mode access
 switchport access vlan 10
 channel-group 3 mode active
 no shutdown
!
interface port-channel 3
 description ESXi-Test-Bundle2
 switchport mode access
 switchport access vlan 10
!
! ====== Port-channel 4 (Spare / Lab: Fa0/7-8) ======
interface range fa0/7 - 8
 description Spare-Lab-Bundle
 switchport mode access
 switchport access vlan 10
 channel-group 4 mode active
 no shutdown
!
interface port-channel 4
 description Spare-Lab-Bundle
 switchport mode access
 switchport access vlan 10
!
end
write memory
```
