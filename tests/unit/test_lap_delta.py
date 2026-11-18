import pytest
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from automations.analysis.lap_delta import compute_lap_delta

def test_lap_delta_computation(tmp_path):
    # Setup paths
    file_a = 'samples/motec_csv/spa_gt3_lap_a.csv'
    file_b = 'samples/motec_csv/spa_gt3_lap_b.csv'
    out_file = tmp_path / "test_delta.json"

    # Run script
    result = compute_lap_delta(file_a, file_b, str(out_file))

    # Assertions
    assert "total_delta_seconds" in result
    assert "delta_by_sector" in result
    assert len(result["trace"]) == 100
    assert os.path.exists(out_file)

    # Check that the sectors sum up approximately to the total delta
    sector_sum = sum(result["delta_by_sector"].values())
    assert abs(sector_sum - result["total_delta_seconds"]) < 0.01