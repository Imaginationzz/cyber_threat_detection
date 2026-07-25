import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize Faker to generate realistic dummy data
fake = Faker()

def generate_synthetic_logs(num_records=10000):
    data = []
    start_time = datetime.now()

    for _ in range(num_records):
        # Determine the class based on our defined weights (75% Safe, 25% Threats)
        scenario = random.choices(
            ['Safe', 'DDoS', 'Brute_Force', 'Port_Scan', 'SQL_Injection'],
            weights=[0.75, 0.10, 0.05, 0.05, 0.05]
        )[0]

        # --- Base Variables (Assumes 'Safe' Traffic) ---
        timestamp = start_time + timedelta(seconds=random.randint(0, 3600))
        source_ip = fake.ipv4()
        dest_port = random.choice([80, 443]) # Standard HTTP/HTTPS ports
        packet_size = random.randint(100, 1500)
        failed_logins = 0
        status_code = 200
        label = scenario

        # --- Threat Overrides ---
        if scenario == 'DDoS':
            # DDoS: Same target port, uniform packet size to simulate a botnet script
            dest_port = 443
            packet_size = 512 
            
        elif scenario == 'Brute_Force':
            # Brute Force: Targeting SSH, high failed logins, unauthorized status
            dest_port = 22 
            failed_logins = random.randint(5, 50)
            status_code = 401
            
        elif scenario == 'Port_Scan':
            # Port Scan: Hitting random non-standard ports, usually getting forbidden/blocked
            dest_port = random.randint(1024, 65535) 
            status_code = 403
            
        elif scenario == 'SQL_Injection':
            # SQL Injection: Hitting web ports but with unusually large payloads (the SQL query)
            dest_port = 443
            packet_size = random.randint(2500, 5000) 
            status_code = 500 # Server often throws an error if the query breaks

        # Append the row to our dataset
        data.append([timestamp, source_ip, dest_port, packet_size, failed_logins, status_code, label])

    # Convert to a Pandas DataFrame
    columns = ['timestamp', 'source_ip', 'dest_port', 'packet_size', 'failed_logins', 'status_code', 'label']
    df = pd.DataFrame(data, columns=columns)
    
    return df

# Generate 10,000 records and save to CSV
if __name__ == "__main__":
    print("Generating synthetic network logs...")
    df_logs = generate_synthetic_logs(10000)
    df_logs.to_csv('./data/synthetic_network_traffic.csv', index=False)
    print(f"Success! Generated {len(df_logs)} records and saved to 'synthetic_network_traffic.csv'.")
    print("\nDataset Preview:")
    print(df_logs.head())