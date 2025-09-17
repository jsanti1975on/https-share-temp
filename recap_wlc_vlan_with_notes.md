# Cisco WLC + VLAN Recap with Troubleshooting Notes

This recap documents how the Cisco WLC management interface was configured and verified for access via VLAN 999.

---

## 🔹 Final Working State

- **WLC Management IP:** `10.10.99.10/24`
- **Default Gateway:** `10.10.99.254` (Cisco RV340)
- **VLAN:** Untagged (mapped to VLAN 999 in RV340)
- **Access:** Web GUI available at `https://10.10.99.10`

---

## 🔹 Troubleshooting Notes

- **Initial Issue:**  
  The WLC was originally configured with VLAN 999 and IP `172.20.10.200`. The VM was unable to reach the WLC GUI because of VLAN tagging/untagging mismatch.

- **First Attempt:**  
  Tried to assign `10.10.99.10` on VLAN 999 directly → failed due to "Active WLAN using interface" message.  
  This showed the WLC doesn’t allow direct IP change while WLAN is active.

- **Next Step:**  
  Disabled WLANs with `wlan disable all`. Then reconfigured the management interface to `10.10.99.10/24` on **untagged VLAN**.  
  After enabling WLAN again, `show interface summary` confirmed:  
  - Management → VLAN 1 (untagged), IP `10.10.99.10`  
  - Virtual → `192.0.2.1`

- **Verification:**  
  - Ping **from VM → WLC** worked (`10.10.99.10`).  
  - Ping **from WLC → VM** failed, which is expected in some WLC builds since management-to-client ICMP is often disabled.  
  - Web GUI at `https://10.10.99.10` was successful (screenshot shows login page).  

- **Key Lesson:**  
  The WLC **expects its management IP to be untagged (native VLAN)** when placed behind the RV340. Tagged config caused isolation.

---

## 🔹 Next Steps

- Add screenshots of:  
  1. WLC interface summary  
  2. Ping tests (VM → WLC, WLC → VM)  
  3. Successful Web GUI login page  

- Test AP join process once WLC management IP is stable.  
- Add wireless SSID configuration and client test.

---
<img width="1045" height="1322" alt="22-wlan-untagged" src="https://github.com/user-attachments/assets/5d205ec4-ade7-418f-ba64-d5e1bf3123dc" />
<img width="1069" height="1263" alt="23-Recap-Image" src="https://github.com/user-attachments/assets/76ffbf2e-ca1e-48de-8a25-81ff1662be5d" />
<img width="1078" height="1868" alt="24-Success-WLC-Gui" src="https://github.com/user-attachments/assets/caea2254-4219-4ec0-82f9-02adf719f053" />


