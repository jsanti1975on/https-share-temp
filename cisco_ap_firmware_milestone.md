
# Cisco AP Firmware Installation and WLC Join Milestone

## Overview
This milestone documents the successful installation of a Cisco lightweight (`k9w8`) image onto an AP and preparing it to join the Cisco 2504 Wireless LAN Controller (WLC).  

The key tasks included:
- Preparing a TFTP server on Windows 10 (SolarWinds TFTP).
- Configuring pfSense to properly allow DHCP and TFTP services.
- Loading the AP firmware via console (`tar -xtract`).
- Ensuring DHCP reservations for both AP and TFTP server.

---

## Network Setup
- **TFTP Server (SolarWinds)**: `10.10.10.45`  
- **Access Point (AP)**: Reserved DHCP address `10.10.10.10`  
- **Default Router (pfSense)**: `10.10.10.1`  
- **WLC**: Cisco 2504  

### pfSense Configuration
1. Removed DNS sinkhole to avoid AP discovery issues.
2. Added **DHCP reservations** for:
   - The Cisco AP.
   - The Windows 10 machine running SolarWinds.
3. Configured pfSense to recognize the TFTP server (`10.10.10.45`) as authoritative for file transfer.

---

## AP Bootloader Commands
The AP was connected via console (using PuTTY/Tera Term) and powered through PoE.  
From the `ap:` bootloader prompt:

```plaintext
set IP_ADDR 10.10.10.10
set DEFAULT_ROUTER 10.10.10.1
set NETMASK 255.255.255.0
ether_init
flash_init
tftp_init
tar -xtract tftp://10.10.10.45/ap3g2-k9w8-tar.153-3.JD14.tar flash:
```

- `flash_init`: Initializes AP flash memory.  
- `tftp_init`: Initializes TFTP subsystem.  
- `tar -xtract`: Extracts the firmware archive into flash memory.  

---

## Results
- The AP successfully extracted `ap3g2-k9w8-tar.153-3.JD14.tar` into flash.  
- Dots (`...`) in console output confirm progress of file extraction.  
- The AP now has a **lightweight image (k9w8)**, meaning it will attempt to join the WLC (`2504`) after reboot.  

---

## Next Steps
1. Reboot AP:
   ```plaintext
   reset
   ```
2. Verify AP boots into lightweight IOS and begins discovery process.  
3. Confirm that AP joins the WLC:
   - `show ap summary` on the WLC should list the AP.  
   - If not, configure WLC discovery methods (DHCP option 43, DNS `CISCO-CAPWAP-CONTROLLER`, or Layer 2 broadcast).  

---

## Key Takeaway
This process demonstrated end-to-end **firmware recovery and deployment** of a Cisco AP using TFTP and pfSense integration. It confirms readiness for controller-based management and is a critical milestone toward completing the wireless infrastructure lab.
