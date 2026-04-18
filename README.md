# dot1x-macsec-bypass

> Proof-of-concept for bypassing 802.1X port security and downgrading 
> MACsec through MKPDU suppression. Developed as part of academic 
> research on wired network security controls.

⚠️ **For authorized testing and educational purposes only.**

---

## Tested Environment

- Switch: Cisco Catalyst (802.1X + MACsec enabled)
- Auth method: EAP / PEAP
- Attacker OS: Kali Linux
- Python: 3.11

## How It Works

This tool exploits a weakness in MACsec's key agreement protocol (MKA).
By suppressing MACsec Key Agreement PDUs (MKPDUs) — the frames 
responsible for establishing and maintaining MACsec sessions — the 
switch is forced to fall back to unencrypted 802.1X EAP, effectively 
downgrading the security of the link.

Combined with MAC spoofing of a previously authenticated supplicant, 
this allows an external device to gain unauthorized network access 
without triggering reauthentication.

### Attack Flow
1. Attacker obtains MAC address of a legitimate, authenticated host
2. Attacker spoofs that MAC address on their interface
3. Script suppresses MKPDUs — MACsec session never establishes
4. Switch falls back to plain 802.1X (or no auth if disabled)
5. Attacker obtains IP via DHCP and gains network access

---

## Requirements

- Linux (tested on Kali Linux)
- Python 3.x
- Scapy

```bash
pip install scapy
```

---

## Usage

### Step 1 — Obtain legitimate MAC address

On the authorized host before disconnecting it:

```bash
ip link show eth0
```

### Step 2 — Spoof MAC address

```bash
ip link set eth1 down
ip link set eth1 address AA:BB:CC:DD:EE:FF
ip link set eth1 up
```

### Step 3 — Run the downgrade script

```bash
python3 macsec_downgrade.py &
```

### Step 4 — Request IP and verify access

```bash
dhclient eth1
ping <target-ip>
```

---

## Expected Output
---

## Tested Environment

- Switch: Cisco Catalyst (802.1X + MACsec enabled)
- Auth method: EAP / PEAP
- Attacker OS: Kali Linux
- Python: 3.11

---

## Mitigations

| Control | Description |
|---|---|
| MACsec `must-secure` | Rejects any fallback — link drops if MKA fails |
| 802.1X with MAB disabled | Prevents MAC-only authentication fallback |
| Port security | Detects multiple MACs on the same switch port |
| RADIUS accounting | Flags session anomalies and unexpected reauthentications |

---

> ⚠️ **Compatibility notice:** This tool has only been tested against 
> Cisco Catalyst switches. Behavior against other vendors (Juniper, 
> HP/Aruba, Huawei, etc.) is unknown and results may vary depending 
> on how the vendor implements MKA negotiation and fallback policies.
> Use at your own risk.

---

## References

- [IEEE 802.1X-2010 Standard](https://standards.ieee.org/ieee/802.1X/4520/)
- [IEEE 802.1AE MACsec](https://standards.ieee.org/ieee/802.1AE/4572/)
- [Bypassing Port Security in 2018 - Gabriel Ryan, DEF CON 26](https://www.researchgate.net/publication/327402715)
- [Silentbridge Toolkit](https://github.com/s0lst1c3/silentbridge)

---

## Disclaimer

Unauthorized use against networks 
you do not own or have explicit 
written permission to test is illegal 
and unethical.