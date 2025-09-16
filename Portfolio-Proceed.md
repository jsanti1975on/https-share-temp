# Revised Lab Design => Review below later after reconfig => this file is just for a time stamp and to move on with portfolio
Router (RV340)

Use one physical uplink (say Fa0/1 on East 3560 → LAN2 on RV340).

Configure it as a trunk:

Native VLAN = 999

Allowed VLANs = 10,999

This avoids the LACP headaches entirely. You’ll still be able to test routing, VLAN handoff, and DHCP from the RV340.

East & West 3560s

Keep Gi0/1 ⇔ Gi0/1 as your primary trunk between the switches.

Native VLAN = 999

Allowed VLANs = 10,999

This gives you a proper “distribution/backbone” link between East and West.

EtherChannel Practice (vSphere hosts)

Bundle Fa0/3–4 (Po2), Fa0/5–6 (Po3), etc., on East or West.

Keep them as access ports on VLAN 10.

LACP mode = active.

This lets you practice EtherChannel without involving the RV340.

You’ll get to see (SU) with (P) members, which is what you want for hands-on.

🎯 Benefits of this approach

Stable baseline — your LACP experience will be “true Cisco,” not limited by the quirks of the RV340.

Keeps VLAN design consistent — VLAN 999 = native, VLAN 10 = data.

Still realistic — many production networks uplink SMB routers/firewalls with just a single trunk port, especially when redundancy/LAG isn’t critical.

You still cover EtherChannel — using the switch-to-host bundles.

⚡ How to write it up (if this is for a report or class)

“Due to interoperability quirks between the Cisco RV340 (SMB platform) and Catalyst 3560 (IOS), the EtherChannel could not be established on the router uplink. As a workaround, a single trunk uplink was used to the RV340, while EtherChannel configuration and verification were successfully practiced between Catalyst switches and ESXi servers.”

That explanation shows you understand the problem and made a deliberate engineering decision, which is exactly what instructors/managers want to see.
