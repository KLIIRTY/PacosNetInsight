import pandas as pd
import random
from datetime import datetime, timedelta
import os


def generate_sample_network_log(output_path: str, num_entries: int = 500) -> str:
    """Generate a synthetic network log CSV file."""
    normal_ports = [80, 443, 8080, 53]
    anomaly_ports = [22, 3389, 23]

    rows = []
    current_time = datetime(2026, 3, 1, 10, 0, 0)

    for _ in range(num_entries):
        current_time += timedelta(seconds=random.randint(1, 5))
        src_ip = f"192.168.1.{random.randint(2,254)}"
        dst_ip = f"10.0.0.{random.randint(1,254)}"

        if random.random() < 0.05:
            port = random.choice(anomaly_ports)
            packet_size = random.randint(3000, 10000)
            failed_logins = random.randint(3, 7)
        else:
            port = random.choice(normal_ports)
            packet_size = random.randint(50, 1500)
            failed_logins = 0

        rows.append([current_time, src_ip, dst_ip, port, packet_size, failed_logins])

    df = pd.DataFrame(
        rows,
        columns=['timestamp', 'source_ip', 'destination_ip', 'port', 'packet_size', 'failed_logins']
    )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_file = os.path.join(base_dir, "data", "network_log.csv")
    generate_sample_network_log(output_file)
    print(f"Synthetic network log generated at {output_file}")
