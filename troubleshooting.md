# Troubleshooting Log - Cisco 3560 EtherChannel Lab

This file documents key issues encountered during the EtherChannel lab and their resolutions.

---

## Issue 1: West switch management on VLAN1 instead of VLAN999

### Symptoms
- East (10.10.99.2, VLAN999) could ping the RV340 gateway (10.10.99.254) successfully.
- East could NOT ping West (expected 10.10.99.3).
- West had obtained a DHCP address (`10.10.99.147`) on **VLAN1**.

### Root Cause
- Management interface on West (`Vlan1`) was active and running DHCP.
- VLAN999 was created but had no IP address assigned, so management traffic was not aligned.

### Resolution
On West switch:
```cisco
interface vlan 1
 shutdown
!
interface vlan 999
 ip address 10.10.99.3 255.255.255.0
 no shutdown
!
ip default-gateway 10.10.99.254
```

### Verification
```bash
West# show ip interface brief
Vlan1      administratively down
Vlan999    10.10.99.3   up   up
```

Ping tests after fix:
- East → West ✅ (10.10.99.2 → 10.10.99.3)
- East → RV340 ✅ (10.10.99.2 → 10.10.99.254)
- West → East ✅ (10.10.99.3 → 10.10.99.2)
- West → RV340 ✅ (10.10.99.3 → 10.10.99.254)

---

## Current Lab State
- **Po1 EtherChannel (East⇔West)**: Up, carrying VLANs 10 and 999.
- **Management VLAN (999)**: Consistent across East, West, and RV340.
- **Gateway (10.10.99.254)**: Reachable from both switches.
- **VLAN1**: Shutdown to prevent DHCP conflicts.
