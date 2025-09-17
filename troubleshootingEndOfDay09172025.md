# Troubleshooting Log – Cisco RV340, 3560, WLC, and ESXi Lab

This document captures the troubleshooting process, based on screenshots and test logs.

---

## 🔹 Issue 1 – Switch-to-Switch & Router Native VLAN Mismatch

- **Symptom:** Native VLAN mismatch messages on trunks.
- **Action:** Standardized all trunks to use **VLAN 999** as the native VLAN.
- **Outcome:** CDP mismatch messages cleared.

---

## 🔹 Issue 2 – EtherChannel (LACP) not bundling correctly

- **Symptom:** `show etherchannel summary` showed ports in **(I) individual** state instead of **(P) bundled**.
- **Action:**  
  - Cleared old configs (`write erase`, `delete vlan.dat`, reload).  
  - Reconfigured Po1 for East <-> West trunk.  
  - Reconfigured Po2 for ESXi uplinks.  
- **Outcome:** EtherChannel successfully formed with `(SU)` state.

---

## 🔹 Issue 3 – West switch VLAN interface misconfigured

- **Symptom:** West switch had IP assigned to `VLAN1` via DHCP (10.10.99.147).  
- **Action:** Shut `VLAN1`, created `VLAN999` with static IP **10.10.99.3/24**.  
- **Outcome:** East (10.10.99.2) ↔ West (10.10.99.3) ping successful. Both can reach RV340 at **10.10.99.254**.

---

## 🔹 Issue 4 – WLC not reachable on Management VLAN

- **Symptom:** WLC showed management interface on VLAN 999 but didn’t respond to pings.  
- **Actions Tried:**  
  - Set WLC to 172.20.10.x address (failed).  
  - Tried forcing VLAN ID changes (rejected until WLAN disabled).  
  - Disabled WLANs, reassigned management IP.  
- **Outcome:** After resetting to **untagged VLAN999 (10.10.99.10)**, WLC became reachable. GUI accessible at:  
  `https://10.10.99.10`

---

## 🔹 Issue 5 – VM-to-WLC communication

- **Symptom:** VM could ping RV340 gateway but not WLC. WLC could not ping VM.  
- **Action:** Adjusted ESXi Port Group settings:  
  - Created `VLAN999-Mgmt` untagged.  
  - Assigned VM NIC to new port group.  
- **Outcome:** VM successfully reached WLC GUI.

---

## 🔹 Verification

- East Switch: `10.10.99.2` ✅  
- West Switch: `10.10.99.3` ✅  
- RV340 Router: `10.10.99.254` ✅  
- WLC GUI: `10.10.99.10` ✅ (access via browser)  
- VM (Mgmt VLAN): `10.10.99.x` ✅

---

## Next Steps

1. Configure WLAN/SSID on WLC (`Homework`).  
2. Verify AP joins the WLC.  
3. Test client connectivity over Wi-Fi.  
4. Lock down management access (ACLs, firewall rules).

