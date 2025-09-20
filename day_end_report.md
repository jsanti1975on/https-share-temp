# Day-End Report: EtherChannel Troubleshooting & Fix

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
