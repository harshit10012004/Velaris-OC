import pytest
import os
import sys

# Ensure Python can find the automations folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from automations.intake.validate_file import validate_telemetry

def test_valid_lap_passes():
    """Golden sample should pass validation."""
    assert validate_telemetry('samples/motec_csv/spa_gt3_lap_a.csv') is True

def test_missing_file_raises():
    """Validator should reject a non-existent file."""
    with pytest.raises(ValueError, match="File not found"):
        validate_telemetry('samples/motec_csv/non_existent.csv')