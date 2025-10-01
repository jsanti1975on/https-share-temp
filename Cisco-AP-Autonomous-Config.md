# Cisco Aironet AP Autonomous Mode Configuration

This document provides the configuration and workflow steps for setting up a **Cisco Aironet AP** in autonomous mode, including firmware installation, SSID setup, VLAN mapping, and troubleshooting.

---

## 1. Firmware Flashing Notes

- Firmware image used:
  - Lightweight Mode: `ap3g2-k9w8-tar.153-3.JD14.tar`
  - Autonomous Mode: `ap3g2-k9w7-tar.153-3.JD14.tar`
- Direct connection from AP ➝ Cisco RV340 LAN port 1 was used for speed and reliability.
- Verified flash initialization and successful image load.

---

## 2. Initial Setup Commands: We used to pfsence to route for practice

<img width="1032" height="956" alt="Take-Note" src="https://github.com/user-attachments/assets/0a13fbdd-51ea-4fe8-8fd5-3852078d29f9" />


## 2.1 Config on native vlan - Also place the unextrated file in the solarwinds app. Practice a Mesh config private comms.
```cisco
set IP_ADDR 10.10.99.109
set NETMASK 255.255.255.0
set DEFAULT_ROUTER 10.10.99.254
ether_init
flash_init
tftp_init
tar -xtract tftp://10.10.10.45/ap3g2-k9w7-tar.153-3.JD14.tar flash:
```

---

## 3. Enabling Radios

```cisco
conf t
interface Dot11Radio0
 no shutdown
!
interface Dot11Radio1
 no shutdown
!
end
write memory
```

---

## 4. SSID Configuration (Autonomous Mode)

```cisco
dot11 ssid Homework
   authentication open
   authentication key-management wpa version 2
   wpa-psk ascii 0 YourStrongPassword123
```

- Replace `YourStrongPassword123` with a secure passphrase.
- SSID will be bound to both 2.4GHz and 5GHz radios.

---

## 5. Binding SSID to Interfaces

```cisco
interface Dot11Radio0
 ssid Homework
 channel 6
 station-role root
!
interface Dot11Radio1
 ssid Homework
 channel 36
 station-role root
!
end
write memory
```

---

## 6. VLAN Binding (Optional)

If `Homework` should map to **VLAN 5 (10.10.20.0/24)**:

```cisco
interface FastEthernet0
 switchport mode access
 switchport access vlan 5
 no shutdown
```

---

## 7. Troubleshooting Notes

- Ensure DHCP reservations on Cisco RV340 for:
  - AP: `10.10.99.109`
  - WLC (when in lightweight mode): `10.10.99.10`
- DTLS/Certificate errors appear in lightweight mode when CAPWAP cannot authenticate — **expected** if not using a valid WLC.
- In autonomous mode, these errors no longer apply.
- Hidden SSID issue was resolved by verifying **Admin Status = Enabled** and **Broadcast SSID = Enabled**.

---

## 8. Integration with Lab Network

- **East Switch**: Provides EtherChannel uplinks (fa0/3-4) toward ESXi host `poweredge.dubz-vault`.
- **VLANs Routed by RV340**:
  - VLAN 10 (Production)
  - VLAN 999 (Native Mgmt)
  - VLAN 5 (machine.ai domain / 10.10.20.0/24)

---

## 9. Next Steps

- Finalize SSID mapping for VLAN 5 once machine.ai domain services are online.
- Use DHCP from **GAN server** (secondary scope) for redundancy.
- Document and record YouTube demo with EtherChannel, playbooks, and AP configuration.
