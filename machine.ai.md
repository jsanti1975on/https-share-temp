# 🌐 machine.ai Domain – VLAN Design & DHCP Workflow

This document outlines the network design and build workflow for the  
**`machine.ai` Active Directory domain** hosted in the **10.10.20.0/24** subnet,  
with routing and VLAN segmentation provided by the **Cisco RV340**.

---

## 📍 Why a New Subnet?

- `10.10.10.0/24` = **Firewall/WAN transport** (pfSense ↔ RV340 uplink).  
- `172.20.10.0/24` = **West VLAN** (existing domain services, production lab).  
- `10.10.20.0/24` = **New VLAN** dedicated to the `machine.ai` project.  

👉 This separation avoids mixing infrastructure services with the WAN and keeps the domain
clean, portable, and realistic for enterprise documentation.

---

## 🖧 Subnet Plan

| Subnet         | Purpose             | Gateway         |
|----------------|--------------------|-----------------|
| `10.10.10.0/24` | Firewall transport | pfSense ↔ RV340 |
| `172.20.10.0/24` | West VLAN (existing) | `172.20.10.1`   |
| `10.10.20.0/24` | New `machine.ai` domain | `10.10.20.254` |

---

## 🖥️ Server IP Assignments (10.10.20.0/24)

| Hostname | Role(s)             | IP Address   | Notes |
|----------|---------------------|--------------|-------|
| ANN      | AD DS, DNS          | 10.10.20.1   | First DC, forest root |
| GAN      | AD DS, DHCP         | 10.10.20.2   | Secondary DC, DHCP relay target |
| NLG      | File Server (FSRM)  | 10.10.20.3   | Quotas, file screening |
| EXCH01   | Exchange Mailbox    | 10.10.20.50  | (Optional) Exchange 2019 |
| Clients  | Workstations        | 10.10.20.100+ | DHCP leases |

---

## 🔄 DHCP Workflow

### Phase 1 – VM Installation (DHCP on RV340)
- VLAN5 (10.10.20.0/24) created on RV340.  
- DHCP Scope (temporary):  
  - Start: `10.10.20.100`  
  - End: `10.10.20.149`  
  - Gateway: `10.10.20.254`  
  - DNS: ISP DNS (temporary)  

➡️ VMs (ANN, GAN, NLG, EXCH01, clients) install and patch using RV340 leases.

---

### Phase 2 – Static IP Assignment
After patching and VMware Tools install:
- Assign static IPs to servers (see table above).  
- Set **DNS = 10.10.20.1** on all servers and clients.  

---

### Phase 3 – Domain Promotion
- ANN (10.10.20.1): Promote to new forest `machine.ai`.  
- GAN (10.10.20.2): Join domain, promote to secondary DC.  

---

### Phase 4 – DHCP Handoff
- **RV340**: Change VLAN5 → DHCP mode: **Relay**, target = `10.10.20.2`.  
- **GAN**: Add DHCP role, create scope:  
  - Start: `10.10.20.100`  
  - End: `10.10.20.200`  
  - Gateway: `10.10.20.254`  
  - DNS: `10.10.20.1`  
- Authorize DHCP in AD DS.  

---

### Phase 5 – Client Verification
- Boot Windows 10/11 client in VLAN5.  
- Confirm DHCP lease from GAN scope.  
- Join domain `machine.ai`.  
- Access file shares on NLG (`\\NLG\DeptShare`).  

---

## ✅ Key Takeaways

- The **RV340 handles DHCP during build** for easy setup.  
- The **DHCP role is later transferred to Windows Server (GAN)** for realistic AD integration.  
- `machine.ai` is fully isolated on **10.10.20.0/24**, routed by RV340, while WAN and other VLANs remain untouched.  
