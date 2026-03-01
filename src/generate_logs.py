import pandas as pd
import random
from datetime import datetime, timedelta
import os

# Set file path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "network_log.csv")

# Parameters
NUM_ENTRIES = 500  # total logs
normal_ports = [80, 443, 8080, 53]  # normal traffic ports
anomaly_ports = [22, 3389, 23]  # suspicious ports

rows = []
current_time = datetime(2026, 3, 1, 10, 0, 0)

for i in range(NUM_ENTRIES):
    # Randomly increment timestamp
    current_time += timedelta(seconds=random.randint(1,5))
    
    # Random source IP
    src_ip = f"192.168.1.{random.randint(2,254)}"
    dst_ip = f"10.0.0.{random.randint(1,254)}"
    
    # Decide if this is normal or anomalous
    if random.random() < 0.05:  # 5% anomalies
        port = random.choice(anomaly_ports)
        packet_size = random.randint(3000, 10000)
        failed_logins = random.randint(3, 7)
    else:
        port = random.choice(normal_ports)
        packet_size = random.randint(50, 1500)
        failed_logins = 0
    
    rows.append([current_time, src_ip, dst_ip, port, packet_size, failed_logins])

# Save to CSV
df = pd.DataFrame(rows, columns=['timestamp', 'source_ip', 'destination_ip', 'port', 'packet_size', 'failed_logins'])
df.to_csv(DATA_PATH, index=False)

print(f"Synthetic network log generated: {NUM_ENTRIES} rows at {DATA_PATH}")
