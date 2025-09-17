# 🚀 Day 2 Kickoff Checklist – Cisco WLC + AP Lab

## ✅ Already Completed (Day 1)
- East/West 3560 switches reconfigured with EtherChannel.  
- RV340 VLANs aligned → **VLAN 10 (172.20.10.0/24)**, **VLAN 999 (10.10.99.0/24)**.  
- WLC GUI accessible at **https://10.10.99.10** (Mgmt VLAN, untagged).  
- VM in **VLAN999-Mgmt** can reach WLC GUI.  
- Documentation generated:  
  - `recap_wlc_vlan_with_notes.md`  
  - `troubleshooting.md`  
  - `master_lab_report.md`  

---

## 🔹 Next Steps (Day 2 Tasks)

1. **Verify WLC Management Interface**
   - Console: `show interface summary` → confirm `10.10.99.10/24`.
   - From VM: `ping 10.10.99.10`.

2. **Connect & Verify AP**
   - Ensure AP is cabled to West 3560 with PoE.  
   - Switchport config:  
     ```cisco
     interface Fa0/x
      description AP-Uplink
      switchport trunk encapsulation dot1q
      switchport mode trunk
      switchport trunk native vlan 999
      switchport trunk allowed vlan 10,999
      spanning-tree portfast trunk
     ```  
   - WLC: `show ap summary` → AP should appear as **Registered**.

3. **Create SSID `Homework`**
   - GUI → **WLANs > Create New**.  
   - SSID: `Homework`.  
   - Interface: `VLAN10 (172.20.10.0/24)`.  
   - Security: WPA2-PSK, AES.  
   - Enable WLAN.

4. **Test Wireless Client**
   - Laptop/VM → connect to **SSID Homework**.  
   - Should receive DHCP from RV340 (`172.20.10.x`).  
   - Verify connectivity:  
     - Ping `172.20.10.254` (gateway).  
     - Ping VM on East side.  
     - Ping server on West side.

5. **Document Results**
   - Screenshot: `show ap summary`.  
   - Screenshot: Wireless client connected with `172.20.10.x` IP.  
   - Add notes to GitHub.  

---

## 🔹 Stretch Goals (if time permits)
- Configure ACLs to restrict management access.  
- Test roaming if you have multiple APs.  
- Test client upload (Homework file → server) and automation script.  

---

⚡ With this checklist, you’ll be able to start **Day 2** by verifying the AP joins, then move right into **SSID creation and client testing**.  
