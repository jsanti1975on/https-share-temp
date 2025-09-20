# Day-End Report: EtherChannel Troubleshooting & Fix
<img width="1019" height="1454" alt="Issue-Resolved-Image" src="https://github.com/user-attachments/assets/94a013f9-d5a7-44ac-a90c-f2e6323efd1b" />


## ✅ Issue Resolved Today: ESXi Uplink EtherChannel

### Problem:
- On **East switch**, `Fa0/3` and `Fa0/4` were connected to **ESXi host vmnic2/vmnic3**.  
- These interfaces were originally configured for **LACP (active)**.  
- vSphere was set to **Route based on IP Hash** → requires a **static (mode on)** EtherChannel, not LACP.  
- Result: `Po2` was stuck in **(SD)** = "suspended," interfaces inactive.  

### Fix:
- Removed the incorrect LACP config.  
- Re-applied EtherChannel with **static mode (on)**.  

```cisco
conf t
 default interface fa0/3
 default interface fa0/4

interface range fa0/3 - 4
 description ESXi-Uplinks
 switchport mode access
 switchport access vlan 10
 channel-group 2 mode on
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
exit

interface port-channel 2
 description ESXi-Uplinks
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
```

### Verification:
```cisco
show etherchannel summary
```

✅ Output shows:  
- `Po2(SU)` with `Fa0/3(P), Fa0/4(P)` → both bundled and forwarding.  
- ESXi NIC team (vmnic2/vmnic3) can now properly load balance using IP hash.  

---

## 🔹 Commands to Apply on **West Switch** (Tomorrow)

The West switch also connects ESXi host uplinks (likely **Fa0/1–2**) and must mirror East.

```cisco
conf t
 default interface fa0/1
 default interface fa0/2

interface range fa0/1 - 2
 description ESXi-Server-Uplinks
 switchport mode access
 switchport access vlan 10
 channel-group 2 mode on
 spanning-tree portfast
 spanning-tree bpduguard enable
 no shutdown
exit

interface port-channel 2
 description ESXi-Server-Uplinks
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
```

### Verification:
```cisco
show etherchannel summary
show vlan brief
```

---
<img width="947" height="1406" alt="West-Config-VM-DATA" src="https://github.com/user-attachments/assets/3768cb8d-5c44-435a-b3c7-770525f5f14a" />

# Untagged the vlan on the vSphere Host machine & configured the IP addy and dns using 8.8.8.8 to get internet => Will get orkidz-west.arpa domain set up tommorrow!
<img width="1071" height="1646" alt="Untagged0" src="https://github.com/user-attachments/assets/c37b13bd-8bba-4efd-a047-74a1ba8df14c" />
<img width="1368" height="745" alt="Untagged1" src="https://github.com/user-attachments/assets/555afd16-84f2-45de-98b2-17ac09aa700e" />

