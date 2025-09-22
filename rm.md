# AP ↔ WLC ↔ Router Address Mapping

| Device | Role                 | IP Address   | MAC Address    | Notes                                  |
|--------|----------------------|--------------|----------------|----------------------------------------|
| AP     | Lightweight AP       | 10.10.99.109 | 1005.ca68.**** | BV11 interface, DHCP assigned/reserved |
| WLC    | Wireless LAN Ctrl.   | 10.10.99.10  | 5006.04ca.**** | Controller for CAPWAP join             |
| Router | RV340 (Gateway)      | 10.10.99.254 | 28ac.9e0d.**** | Default gateway for VLAN99             |

---

## Verification Commands

### On AP (console)
```plaintext
show arp
```

### On Cisco Switch (West 3560)
```plaintext
show mac address-table dynamic
show mac address-table interface gi0/1
```

### RV340
```plaintext
Check ARP table (UI/CLI).

Confirm DHCP reservations:

AP → 10.10.99.109

WLC → 10.10.99.10

Gateway → 10.10.99.254
```


