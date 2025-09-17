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
