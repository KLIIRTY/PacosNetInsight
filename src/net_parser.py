# src/net_parser.py
import pandas as pd
from datetime import datetime

try:
    from scapy.all import sniff, IP, TCP, UDP
    SCAPY_AVAILABLE = True
except ImportError:
    SCAPY_AVAILABLE = False
    print("Scapy not installed; live packet capture disabled")

def capture_packets(count=20, iface=None):
    """
    Capture live network packets. Returns a DataFrame.
    If scapy is not installed or running on Streamlit Cloud, returns empty DataFrame.
    """
    if not SCAPY_AVAILABLE:
        return pd.DataFrame()  # fallback for cloud / missing scapy

    packets_list = []

    def process_packet(packet):
        pkt_info = {
            "timestamp": datetime.now(),
            "source_ip": packet[IP].src if IP in packet else None,
            "destination_ip": packet[IP].dst if IP in packet else None,
            "port": packet[TCP].sport if TCP in packet else (packet[UDP].sport if UDP in packet else None),
            "packet_size": len(packet),
            "failed_logins": 0,  # placeholder, can extend with real logic
        }
        packets_list.append(pkt_info)

    sniff(iface=iface, prn=process_packet, count=count, store=False)
    return pd.DataFrame(packets_list)