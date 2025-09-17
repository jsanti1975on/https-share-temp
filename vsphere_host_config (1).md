# vSphere Host Configuration for Cisco EtherChannel Lab

This document explains how to configure ESXi hosts to integrate with the Cisco 3560 EtherChannel lab.

---

## 🔹 vSwitch and Port Groups

1. On ESXi, open **Networking → vSwitch0**.
2. Create two port groups:

- **VM Network**
  - VLAN ID: 10
  - Used for client VMs (East) and server VMs (West).

- **VLAN999-Mgmt**
  - VLAN ID: 999
  - Used for management, including WLC GUI access.

3. Attach both port groups to the uplink NICs participating in EtherChannel (vmnic2/vmnic3).

---

## 🔹 EtherChannel Setup

- Configure **Port Channel 2** on East for ESXi-Clients (Fa0/3-4).
- Configure **Port Channel 2** on West for ESXi-Server (Fa0/1-2).
- In vSphere, set the **Load Balancing policy** on the port groups to:

```
Route based on IP hash
```

- Ensure **both vmnics** are active.

---

## 🔹 VM Dual-NIC Config (Data + Management)

Example from lab testing (Windows VM):

- **Ethernet0 (VM Network / VLAN 10 – Data Network)**
  - IPv4: `172.20.10.148/24`
  - Gateway: `172.20.10.254` (RV340 VLAN10 SVI)
  - DHCP Server: `172.20.10.254`
  - DNS: `10.10.10.30`, `8.8.8.8`

- **Ethernet1 (Mgmt VLAN 999 – GUI/Control Network)**
  - IPv4: `10.10.99.50/24`
  - Gateway: `10.10.99.254` (RV340 VLAN999 SVI)
  - DHCP/Static from RV340

✅ With this configuration:
- VM can reach **workload/data network** (VLAN 10) via Ethernet0.
- VM can reach **WLC GUI / management network** (VLAN 999) via Ethernet1.
- Verified by successful ping to `10.10.99.254` from `10.10.99.50`.

# vSwitch Topology Notes
- SW_vNIC01 has two port groups:
- Pnic01 (VLAN 10) → Tagged for VM data network (172.20.10.0/24).
- VLAN999-Mgmt (VLAN 999) → Added today for testing WLC web GUI access.

## Physical uplinks:
- vmnic1 is connected to the RV340.
- Pnic01 is tagged for VLAN 10.
- VLAN999-Mgmt is untagged/native on VLAN 999.

### Purpose of VLAN999-Mgmt:
- Allows direct VM-to-WLC management communication.
- Configured with a test IP (e.g. 10.10.99.50/24).
- Can be disabled or removed when not needed.
  - **This ensures:**
  - VM workloads run normally on VLAN 10.
  - WLC GUI is accessible on VLAN 999 without disrupting production traffic.
  - *Ref. Images Below*
 
<img width="839" height="452" alt="15" src="https://github.com/user-attachments/assets/ce3af335-6929-4e47-8570-a0495b6ce987" />
<img width="1089" height="1704" alt="14" src="https://github.com/user-attachments/assets/33ff6927-797d-4d18-bbb7-34fcdbfd3498" />



