# Cisco 2504 WLC Configuration for Lab

This document outlines the Wireless LAN Controller (WLC) configuration to support the **Homework SSID**, integrated with the East/West 3560 switches and RV340.

---

## 🔹 Step 1: Management Interface (VLAN 999)

```plaintext
(Cisco Controller) config interface address management 10.10.99.10 255.255.255.0 10.10.99.254
(Cisco Controller) config interface vlan management 999
(Cisco Controller) save config
```

- WLC management IP: **10.10.99.10**
- VLAN: **999 (Native-Mgmt)**
- Default gateway: **10.10.99.254 (RV340)**

---

## 🔹 Step 2: Create Dynamic Interface for VLAN 10

```plaintext
(Cisco Controller) config interface create VM-Data 10
(Cisco Controller) config interface address VM-Data 172.20.10.10 255.255.255.0 172.20.10.254
(Cisco Controller) save config
```

- Interface: **VM-Data**
- VLAN: **10**
- IP: **172.20.10.10**
- Gateway: **172.20.10.254 (RV340)**

---

## 🔹 Step 3: WLAN Creation - SSID `Homework`

```plaintext
(Cisco Controller) wlan create 1 Homework Homework
(Cisco Controller) wlan interface 1 VM-Data
(Cisco Controller) wlan security wpa2 enable
(Cisco Controller) wlan security wpa2 ciphers aes enable
(Cisco Controller) wlan security wpa akm psk set-key ascii MyStrongPassword 1
(Cisco Controller) wlan enable 1
(Cisco Controller) save config
```

- SSID: **Homework**
- VLAN Mapping: **10 (VM-Data)**
- Security: **WPA2-PSK (AES)**

---

## 🔹 Step 4: Verify AP Registration

After cabling the Cisco AP to the West 3560 (PoE enabled):

```plaintext
(Cisco Controller) show ap summary
```

- APs should list here when successfully joined.

---

## ✅ Summary

- WLC Mgmt: **10.10.99.10 (VLAN 999)**
- SSID `Homework` bound to VLAN 10 (172.20.10.0/24)
- Wireless clients get DHCP from RV340
- Traffic passes through EtherChannel backbone between East & West

