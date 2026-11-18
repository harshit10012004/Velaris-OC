# Telemetry Samples — MoTeC CSV

## spa_gt3_lap_a.csv

- **Source**: Hugging Face dataset `Nasim435/spa-francorchamps-lap-data`
- **URL**: https://huggingface.co/datasets/Nasim435/spa-francorchamps-lap-data
- **Simulator**: Assetto Corsa
- **Car class**: GT3
- **Track**: Spa-Francorchamps
- **Session type**: (note what the dataset states)
- **Channels**: (list column headers from the CSV)
- **Units**: (note from CSV header or dataset card)
- **Sample rate**: (inspect time column delta)
- **Lap count**: (count lap segments or state "single lap")
- **Purpose**: Temporary golden sample v0 for parser and delta-logic testing
- **Known limitations**: Not MoTeC-native format; channel names may differ from a MoTeC i2 export. Will be replaced with native MoTeC CSV when available.

## Reproducibility

Re-download from the URL above. Do not commit the CSV to Git.