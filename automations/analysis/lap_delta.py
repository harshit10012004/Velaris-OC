import pandas as pd
import numpy as np
import json
import os
import sys

def compute_lap_delta(file_a: str, file_b: str, out_file: str) -> dict:
    """
    Computes the time delta between two laps using track progress.
    Requires 'Time' and 'lap_progress' columns.
    """
    if not os.path.exists(file_a) or not os.path.exists(file_b):
        raise FileNotFoundError("One or both lap files are missing.")

    df_a = pd.read_csv(file_a)
    df_b = pd.read_csv(file_b)

    # Verify required columns exist
    for df, name in [(df_a, "Lap A"), (df_b, "Lap B")]:
        if 'Time' not in df.columns or 'lap_progress' not in df.columns:
            raise ValueError(f"{name} missing 'Time' or 'lap_progress' column.")

    # Ensure data is sorted by track progress
    df_a = df_a.sort_values('lap_progress')
    df_b = df_b.sort_values('lap_progress')

    # Create a common grid for comparison (100 points around the track: 0.0 to 1.0)
    grid = np.linspace(0, 1, 100)

    # Interpolate Time at each point on the grid
    # (np.interp requires x-coordinates to be monotonically increasing)
    time_a_interp = np.interp(grid, df_a['lap_progress'], df_a['Time'])
    time_b_interp = np.interp(grid, df_b['lap_progress'], df_b['Time'])

    # Calculate Delta (Lap B - Lap A)
    delta_trace = time_b_interp - time_a_interp
    total_delta = delta_trace[-1]

    # Calculate Sectors (thirds of the track)
    s1 = delta_trace[33] - delta_trace[0]
    s2 = delta_trace[66] - delta_trace[33]
    s3 = delta_trace[-1] - delta_trace[66]

    output = {
        "lap_a": os.path.basename(file_a),
        "lap_b": os.path.basename(file_b),
        "total_delta_seconds": round(float(total_delta), 3),
        "delta_by_sector": {
            "Sector 1": round(float(s1), 3),
            "Sector 2": round(float(s2), 3),
            "Sector 3": round(float(s3), 3)
        },
        "trace": [
            {"progress": round(float(p), 3), "delta": round(float(d), 3)} 
            for p, d in zip(grid, delta_trace)
        ]
    }

    with open(out_file, 'w') as f:
        json.dump(output, f, indent=2)

    return output

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python lap_delta.py <lap_a.csv> <lap_b.csv> <output.json>")
        sys.exit(2)

    try:
        result = compute_lap_delta(sys.argv[1], sys.argv[2], sys.argv[3])
        print(f"PASS: Delta computed. Total Delta: {result['total_delta_seconds']}s")
        sys.exit(0)
    except Exception as e:
        print(f"FAIL: {e}")
        sys.exit(1)