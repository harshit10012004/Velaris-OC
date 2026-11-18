# MoTeC CSV Input Contract — GT3 v1

## Mandatory channels

| Channel | Unit | Rule |
|---------|------|------|
| Time | s | First column, strictly increasing |
| Speed | km/h or mph | Declared in header; not all-zero |
| Throttle | % or 0–1 | Declared in metadata |
| Brake | bar or switch | Declared in metadata |
| Gear | integer | No gaps inside a lap |

## Beacon markers

Beacon markers are seconds since log start, 3 decimal places.[3]  
If absent, `validate_file.py` falls back to time-window lap extraction  
and flags the file as `beacon_missing: true`.

## Sample rate

MoTeC CSV can export each channel at its own rate, up-sample all to the  
fastest rate, or re-sample to a fixed rate.[4]  
For v1, accept mixed rates but document the resampling rule in the output.
