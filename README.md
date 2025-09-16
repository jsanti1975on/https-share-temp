# September 16  - Reminder to match Native vlan on the router. It was not match and created flapping last night

## September 09-16-25 to do below: entire Cisco network config: Quik and Dirty Topo Below
<img width="1330" height="694" alt="Topo-Map" src="https://github.com/user-attachments/assets/542ca273-f579-4d94-afcd-8e83b40e389b" />

## Configs: East 3560 (WS-C3560-8PC-S) — “core/left” switch

### Reminder to use => *switchport trunk encapsulation dot1q* on these 3560s
```Yaml
! ===== Global =====
hostname East
no ip domain-lookup
service password-encryption
vtp mode transparent
spanning-tree mode pvst
spanning-tree portfast default
spanning-tree bpduguard default
errdisable recovery cause all
errdisable recovery interval 30

! ===== VLANs =====
vlan 10
 name VM-Network
vlan 999
 name Native-Transit

! ===== LACP to RV340 (Fa0/1-2 -> Po1) TRUNK =====
interface range fa0/1 - 2
 description Uplink-to-RV340
 switchport trunk encapsulation dot1q
 switchport mode trunk
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 channel-protocol lacp
 channel-group 1 mode active
 no shutdown

interface port-channel 1
 description LAG-to-RV340
 switchport trunk encapsulation dot1q
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 switchport mode trunk

! ===== Trunk to West switch =====
interface gi0/1
 description Trunk-to-West-3560
 switchport trunk encapsulation dot1q
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 switchport mode trunk
 no shutdown

! ===== ESXi/Test bundles as ACCESS VLAN 10 =====
interface range fa0/3 - 4
 description ESXi-Test-Bundle1-Members
 switchport mode access
 switchport access vlan 10
 channel-protocol lacp
 channel-group 2 mode active
 no shutdown
interface port-channel 2
 description ESXi-Test-Bundle1
 switchport mode access
 switchport access vlan 10

interface range fa0/5 - 6
 description ESXi-Test-Bundle2-Members
 switchport mode access
 switchport access vlan 10
 channel-protocol lacp
 channel-group 3 mode active
 no shutdown
interface port-channel 3
 description ESXi-Test-Bundle2
 switchport mode access
 switchport access vlan 10

interface range fa0/7 - 8
 description Spare-Lab-Bundle-Members
 switchport mode access
 switchport access vlan 10
 channel-protocol lacp
 channel-group 4 mode active
 no shutdown
interface port-channel 4
 description Spare-Lab-Bundle
 switchport mode access
 switchport access vlan 10

end
write memory
```

### West 3560 (WS-C3560-8PC-S) — “access/right” switch
```Yaml
! ===== Global =====
hostname West
no ip domain-lookup
service password-encryption
vtp mode transparent
spanning-tree mode pvst
spanning-tree portfast default
spanning-tree bpduguard default
errdisable recovery cause all
errdisable recovery interval 30

! ===== VLANs (mirror East) =====
vlan 10
 name VM-Network
vlan 999
 name Native-Transit

! ===== Trunk back to East =====
interface gi0/1
 description Trunk-to-East-3560
 switchport trunk encapsulation dot1q
 switchport trunk native vlan 999
 switchport trunk allowed vlan 10,999
 switchport mode trunk
 no shutdown

! ===== vSphere host LACP (Fa0/1-2 -> Po2) as ACCESS VLAN 10 =====
interface range fa0/1 - 2
 description vSphere-Host-Bundle
 switchport mode access
 switchport access vlan 10
 channel-protocol lacp
 channel-group 2 mode active
 no shutdown

interface port-channel 2
 description vSphere-Host-Bundle
 switchport mode access
 switchport access vlan 10

! ===== WLC on Fa0/8 (simple ACCESS on VLAN 10) =====
! If your 2504 is set with "Mgmt VLAN untagged" = VLAN 10, use ACCESS 10 as below.
! (If you later trunk multiple WLAN VLANs to the WLC, change this interface to a trunk.)
interface fa0/8
 description Cisco-2504-WLC-Port1
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown

end
write memory
```

### Quick health checks (run on both switches) => set the RV340 LAG native VLAN to 999 and tag VLAN 10
```Yaml
show etherchannel summary
show lacp neighbor
show interfaces trunk
show spanning-tree vlan 10,999
```

### Cisco 2504 WLC (Model 2504) — Configuration for SSID Homework
```Yaml
(Cisco Controller) > config interface create vmnetwork 10 10.0.10.1 255.255.255.0 10.0.10.254
```
- vmnetwork = name of dynamic interface
- 10 = VLAN ID
- 10.10.10.1/24 = IP address for WLC on VLAN 10
- 10.10.10.254 = gateway (probably the RV340)==> Yes I am using last usable addy!

### WLAN/SSID setup
```Yaml
(Cisco Controller) > config wlan create 1 Homework 10
(Cisco Controller) > config wlan interface 1 vmnetwork
(Cisco Controller) > config wlan security wpa2 enable 1
(Cisco Controller) > config wlan security wpa2 ciphers aes 1
(Cisco Controller) > config wlan security wpa akm psk set-key ascii 1 MyHomeworkPass
(Cisco Controller) > config wlan enable 1
```
📡 Cisco Aironet 2602i AP (Lightweight Mode)=> Dont copy paste config below - using 10.10.10.0/24 not 10.0.10.254

The 2602i is a CAPWAP lightweight AP, so you don’t usually configure SSIDs directly on it — it downloads its config from the WLC after it joins.
All it needs is:

IP address (DHCP from VLAN 10 or static in VLAN 10)

Reachability to the WLC management IP (10.10.10.1 in this case)

AP Boot CLI (if statically configured)
AP> enable
AP# configure terminal
AP(config)# interface BVI1
AP(config-if)# ip address 10.10.10.20 255.255.255.0
AP(config-if)# ip default-gateway 10.0.10.254
AP(config)# capwap ap controller ip address 10.0.10.1
AP(config)# end
AP# write memory


After this, the AP reboots, joins the WLC, and pulls the SSID Homework.

🔎 Verification

On WLC:

(Cisco Controller) > show wlan summary
(Cisco Controller) > show client summary
(Cisco Controller) > show ap summary


On AP (after joining):

AP# show capwap client rcb
AP# show capwap ip config


✅ Result:
Your Homework SSID is broadcast from the 2602i AP, mapped to VLAN 10 through the WLC, and secured with WPA2-PSK.




