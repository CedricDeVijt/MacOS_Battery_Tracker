import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import subprocess
import os
from datetime import datetime

def get_battery_data():
    """Get battery cycle count and maximum capacity using system_profiler"""
    cmd = ["/usr/sbin/system_profiler", "SPPowerDataType"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = result.stdout

    cycle_count = None
    max_capacity = None

    for line in output.split('\n'):
        if "Cycle Count" in line:
            cycle_count = line.split(':')[1].strip()
        elif "Maximum Capacity" in line:
            max_capacity = line.split(':')[1].strip().rstrip('%')

    if cycle_count is None or max_capacity is None:
        raise ValueError("Could not retrieve battery data")

    return cycle_count, max_capacity

def update_csv(file_path):
    """Update the CSV file with new battery data if cycle count has changed"""
    current_date = datetime.now().strftime("%Y/%m/%d")
    cycle_count, max_capacity = get_battery_data()

    if not os.path.exists(file_path):
        with open(file_path, 'w') as f:
            f.write("Date,Cycle Count,Maximum Capacity (%)\n")

    df = pd.read_csv(file_path)
    
    if df.empty or df['Cycle Count'].iloc[-1] != int(cycle_count):
        new_row = pd.DataFrame({
            'Date': [current_date],
            'Cycle Count': [cycle_count],
            'Maximum Capacity (%)': [max_capacity]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(file_path, index=False)

def plot_data(df, column, color, title, filename):
    """Create and save a plot for the given data"""
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df[column], color=color, marker='o', linestyle='-', markersize=4, label=column)
    plt.xlabel('Date')
    plt.ylabel(column)
    plt.title(f'{title} Over Time')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
    plt.gcf().autofmt_xdate()

    plt.tight_layout()
    plt.savefig(filename, dpi=500)
    plt.close()

def main():
    file_path = "../data/battery_health_tracker.csv"
    update_csv(file_path)

    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%Y/%m/%d', errors='coerce')
    mask = df['Date'].isna()
    df.loc[mask, 'Date'] = pd.to_datetime(df.loc[mask, 'Date'], format='%Y-%m-%d', errors='coerce')
    df = df.sort_values('Date').dropna(subset=['Date'])

    plot_data(df, 'Cycle Count', 'blue', 'Cycle Count', '../graphs/battery_cycle_count_over_time.png')
    plot_data(df, 'Maximum Capacity (%)', 'red', 'Maximum Capacity', '../graphs/battery_capacity_over_time.png')

if __name__ == "__main__":
    main()