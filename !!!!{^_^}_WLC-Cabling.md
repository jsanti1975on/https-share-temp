# Understood cabling of the Cisco Wireless Controller


<img width="525" height="399" alt="WLC-CONNECT-IMAGE" src="https://github.com/user-attachments/assets/34d3bc37-21ce-4e26-b302-8e0f198a536d" />

# Cisco AIR-CAP2602I-A-K9 Aironet 2602I Wireless Access Point 

```bash
set IP_ADDR 10.10.99.120
set NETMASK 255.255.255.0
set DEFAULT_ROUTER 10.10.99.254
ether_init
flash_init
tftp_init
tar -xtract tftp://10.10.99.105/ap3g2-k9w7-tar.153-3.JD14.tar flash:
reset
```
