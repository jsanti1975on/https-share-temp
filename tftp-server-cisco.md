# 🛠 Windows Server TFTP Setup (for Cisco AP Recovery)

This guide explains how to install and configure a **TFTP server** on your Windows Server (e.g., DM-STRAPPED with FSRM role) to recover Cisco Aironet APs.

---

## 🔹 1. Download a TFTP Server
Windows Server does **not** include a built-in TFTP server role.  
You must install a third-party tool. Recommended options:

- [SolarWinds Free TFTP Server](https://www.solarwinds.com/free-tools/free-tftp-server)  
- [Tftpd64 / Tftpd32 by Ph. Jounin](http://tftpd32.jounin.net/)  

For this lab, **SolarWinds Free TFTP Server** is preferred.

---

## 🔹 2. Install SolarWinds TFTP Server
1. Download the installer from SolarWinds.  
2. Run the installer and accept the defaults.  
3. Launch **SolarWinds TFTP Server**.  
4. Right-click the tray icon → **Configure**.

---

## 🔹 3. Configure TFTP Root Directory
1. Create a folder, e.g. `C:\TFTP-Root`.  
2. Place the AP firmware file inside, e.g.  
ap3g2-k9w8-tar.153-3.JD16.tar

markdown
Copy code
3. In SolarWinds TFTP Config:  
- **Root Directory** → `C:\TFTP-Root`  
- **Server Interfaces** → Bind to the NIC `172.20.10.102` (FSRM server).  
- **Security** → Allow *Transmit and Receive*.  

---

## 🔹 4. Configure Windows Firewall
Allow inbound TFTP traffic (UDP/69):

```powershell
New-NetFirewallRule -DisplayName "TFTP Server" -Direction Inbound -Protocol UDP -LocalPort 69 -Action Allow
```

🔹 5. Verify TFTP Server is Running
From another machine (or the AP console once IP is set), test:

```bash
tftp 172.20.10.102 GET testfile.txt
```
🔹 6. Recovery Workflow for Cisco AP
Connect to AP via console.

Assign IP settings in bootloader:

```bash
set IP_ADDR 172.20.10.150
set NETMASK 255.255.255.0
set DEFAULT_ROUTER 172.20.10.254
set TFTP_SERVER 172.20.10.102
Initialize TFTP and extract the firmware:

```bash
tftp_init
tar -xtract tftp://172.20.10.102/ap3g2-k9w8-tar.153-3.JD16.tar flash:
Set boot variable and reload:
```

```bash
set BOOT flash:/ap3g2-k9w8-mx.153-3.JD16/ap3g2-k9w8-mx.153-3.JD16
boot
```

### Summary

Install SolarWinds TFTP on Windows Server.

Place the .tar firmware file in C:\TFTP-Root.

Allow UDP/69 through the firewall.

From the AP, pull and extract the firmware via TFTP.

After reboot, the AP should enter Lightweight (CAPWAP) mode and join your WLC.

