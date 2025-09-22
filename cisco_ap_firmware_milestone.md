
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


### Images and notes: => My eyes are very red and I am very tired. But persistance paid off. It is 2:45 AM 
> I poked around the base os - and practiced every command
> I reviewed about 5 YouTube videos and all of the set up were not like mine
> I used skills developed in my Cyber Security and Network Engineering program along with my A.A. degree
> I combined bits of information from all sources to figure this one out.
> The AP shiped without firmware and the image requires a subscription so I nneded to ethically control the device.
> The wireless controller is useless without this AP
> Now I can can continue dev ops with a wireless mesh and practice using the WLC that was covered in Information Security.

### Screenshots.

<img width="901" height="548" alt="Success2" src="https://github.com/user-attachments/assets/51284801-d769-4756-afda-5d3f59a88356" />
<img width="910" height="1212" alt="Success3" src="https://github.com/user-attachments/assets/c9dd2227-90af-4dd1-a8b2-e3791a50342c" />
<img width="924" height="1226" alt="Success4" src="https://github.com/user-attachments/assets/ef75f363-c6e8-4eda-be9f-08433dec18d6" />
<img width="1009" height="1709" alt="Success5" src="https://github.com/user-attachments/assets/496b3bf5-ae08-488b-bcac-73f8f3dd3194" />

