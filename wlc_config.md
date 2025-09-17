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

### Below are my notes.

> I had to first get into the device by locating the default reset creds.
> After I logged in the device - I came to understand the CLI is not like IOS on my 3560
>  switches or RV340.
> configure directly in exec mode


<img width="1033" height="443" alt="8" src="https://github.com/user-attachments/assets/e88fac3d-29bf-4c68-802f-20916c035f41" />
<img width="1050" height="316" alt="9" src="https://github.com/user-attachments/assets/9db0111a-8439-49e2-ab85-6e6eafac055a" />

> After some simple commands I wanted to test the web Gui - just to view it and came to realize I am on a different subnet.
<img width="1078" height="1117" alt="10" src="https://github.com/user-attachments/assets/2453a0c4-9e7c-4455-99fc-19bcf4842832" />
> Working in a remote virtualized environment can get a bit tricky  but can be learned with every day practice.
> Image below shows the VLANs to Port Table. We also need to consider the vSphere 8 host and how the configurations are mapped.
<img width="1081" height="956" alt="11" src="https://github.com/user-attachments/assets/fa6ae92a-73a3-454f-9276-dd32a675b3cc" />
<img width="698" height="312" alt="12" src="https://github.com/user-attachments/assets/ef1672e1-b043-4179-af00-5295fe4360aa" />









