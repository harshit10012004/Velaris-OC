import pandas as pd
import io
import os

file_path = 'samples/motec_csv/full_stint.csv'

if not os.path.exists(file_path):
    print(f"Error: {file_path} not found.")
    exit(1)

with open(file_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
    lines = f.readlines()

# 1. Find the header line by checking if the FIRST column is exactly "Time"
header_idx = -1
for i, line in enumerate(lines):
    first_col = line.split(',')[0].strip().replace('"', '').strip()
    if first_col == 'Time':
        header_idx = i
        break

if header_idx == -1:
    print("Error: Could not find the header row.")
    exit(1)

print(f"Found actual header at line {header_idx + 1}.")

# 2. Extract everything from the header down, ignoring completely empty lines
csv_data = "".join([line for line in lines[header_idx:] if line.strip()])

# 3. Read with pandas, skipping any bad lines (like the random quote mark MoTeC adds)
df = pd.read_csv(io.StringIO(csv_data), low_memory=False, on_bad_lines='skip')
df.columns = df.columns.str.strip()

# 4. Ensure 'Time' is numeric.
df['Time'] = pd.to_numeric(df['Time'], errors='coerce')
df = df.dropna(subset=['Time']).reset_index(drop=True)

print(f"Total session time: {df['Time'].max():.2f} seconds")
print(f"Channels found: {len(df.columns)}")

# 5. Rename channels to standard Velaris names
df = df.rename(columns={
    'speed_kmh': 'Speed',
    'throttle': 'Throttle',
    'brake': 'Brake',
    'gear': 'Gear'
})

# 6. Split the laps (10s to 150s for Lap A, 150s to 290s for Lap B)
lap_a = df[(df['Time'] >= 10) & (df['Time'] <= 150)].copy()
lap_b = df[(df['Time'] >= 150) & (df['Time'] <= 290)].copy()

if len(lap_a) == 0 or len(lap_b) == 0:
    print("Error: Could not extract laps.")
    exit(1)

# Reset time to start at 0 for each lap
lap_a['Time'] = lap_a['Time'] - lap_a['Time'].min()
lap_b['Time'] = lap_b['Time'] - lap_b['Time'].min()

# 7. Save
out_a = 'samples/motec_csv/spa_gt3_lap_a.csv'
out_b = 'samples/motec_csv/spa_gt3_lap_b.csv'

lap_a.to_csv(out_a, index=False)
lap_b.to_csv(out_b, index=False)

print(f"\nSuccess! Created {out_a} (Rows: {len(lap_a)}) and {out_b} (Rows: {len(lap_b)})")
print("You can now open spa_gt3_lap_a.csv in VS Code to verify.")