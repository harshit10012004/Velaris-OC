import pandas as pd
import os
import sys

def validate_telemetry(file_path: str) -> bool:
    """
    Validates a MoTeC CSV file against Velaris v1 contracts.
    Returns True if valid, raises ValueError if invalid.
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File not found: {file_path}")

    try:
        df = pd.read_csv(file_path, low_memory=False)
    except Exception as e:
        raise ValueError(f"Could not parse CSV: {e}")

    # 1. Check mandatory channels
    mandatory_channels = ['Time', 'Speed', 'Throttle', 'Brake', 'Gear']
    missing = [ch for ch in mandatory_channels if ch not in df.columns]
    if missing:
        raise ValueError(f"Missing mandatory channels: {missing}")

    # 2. Check Time is strictly increasing
    if not df['Time'].is_monotonic_increasing:
        raise ValueError("Time column is not strictly increasing. Check for data corruption.")

    # 3. Check for all-zero channels (sensor failure)
    for ch in mandatory_channels[1:]: # Skip Time
        if (df[ch] == 0).all():
            raise ValueError(f"Channel '{ch}' is all zeros. Sensor likely failed.")

    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_file.py <path_to_csv>")
        sys.exit(2)

    file_path = sys.argv[1]
    
    try:
        validate_telemetry(file_path)
        print(f"PASS: {file_path} is valid.")
        sys.exit(0)
    except ValueError as e:
        print(f"REJECT: {e}")
        # In a full pipeline, this is where you would write to the dead_letter/ folder
        sys.exit(1)