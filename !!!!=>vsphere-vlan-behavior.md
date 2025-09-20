# vSphere VLAN Tagging vs Untagged Behavior in Lab Setup

This document explains why the **Linux VM (`servera`) on VLAN 10** successfully routed to the internet after configuring a new vSwitch/port group as **untagged** in vSphere, and why tagging failed earlier.

---

## 🔹 Working Setup (Untagged VLAN in vSphere)

- **VM IP**: `172.20.10.119/24`
- **Gateway**: `172.20.10.254`
- **DHCP**: RV340 (scope `172.20.10.100–149`)
- **Connectivity**:
  - ✅ Ping to `172.20.10.254` (RV340 gateway)
  - ✅ Ping to external (`google.com`)

### Why It Worked
1. **RV340 expects untagged traffic on VLAN 10**  
   - The RV340 LAN interface for VLAN 10 is configured as *untagged*.
   - DHCP on VLAN 10 is provided directly by the RV340.

2. **vSphere Port Group set to VLAN ID = 0 (untagged)**  
   - VM frames were sent untagged into the switch.
   - Switch uplink port to RV340 was an *access VLAN 10* port.
   - The RV340 recognized the traffic, assigned DHCP, and provided internet routing.

3. **Bridging via East ⇄ West Switches**  
   - VLAN 10 is trunked between East/West switches.
   - VM traffic flowed through the Port-Channel uplinks correctly.

---

## 🔹 Why Tagging VLAN 10 in vSphere Failed

When the vSphere port group was set to **VLAN ID = 10**:
- vSphere tagged traffic with VLAN 10.
- The switch port to RV340 was configured as *native VLAN 10 (untagged)*.
- Result: **double tagging / mismatch** → RV340 dropped the traffic.
- DHCP and internet access failed.

---

## 🔹 Key Takeaways

- **Untagged vSphere Port Group** = correct in this lab.
  - Matches RV340 expectation (access VLAN 10).
  - DHCP + routing works directly.

- **Tagged vSphere Port Group** would only work if:
  - The switch port to RV340 was a trunk, **and**
  - The RV340 interface was explicitly expecting tagged VLAN 10 traffic.

- **Rule of Thumb**:
  - If your upstream device (router/firewall) owns DHCP for the VLAN → keep vSphere untagged.  
  - If vSphere (via pfSense or Windows DHCP) owns the VLAN → tag inside vSphere.

---

## 🔹 Diagram (Simplified)

```
VM (Untagged VLAN 10) ---> vSphere vSwitch (untagged)
    ---> East/West Switch Port (Access VLAN 10)
    ---> RV340 VLAN 10 Interface (untagged)
    ---> DHCP + Internet
```

---

✅ **Current setup is correct for your lab.**  
VMs on VLAN 10 will receive DHCP from the RV340 and route to the internet successfully.  

If you later migrate DHCP/routing into vSphere (pfSense, Windows DC), then VLAN tagging should be reintroduced.
