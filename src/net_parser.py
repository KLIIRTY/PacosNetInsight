from scapy.all import sniff, IP, TCP, UDP
import pandas as pd
from datetime import datetime

def capture_packets(count=20, iface=None):
    packets = sniff(count=count, iface=iface, timeout=2)

    data = []
    for pkt in packets:
        if IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            sport = pkt[TCP].sport if TCP in pkt else (pkt[UDP].sport if UDP in pkt else 0)
            dport = pkt[TCP].dport if TCP in pkt else (pkt[UDP].dport if UDP in pkt else 0)
            size = len(pkt)
            failed_logins = 0  # placeholder, in real scenario get from logs
            timestamp = datetime.now()
            data.append({
                "timestamp": timestamp,
                "source_ip": src,
                "destination_ip": dst,
                "port": dport,
                "packet_size": size,
                "failed_logins": failed_logins
            })
    return pd.DataFrame(data)