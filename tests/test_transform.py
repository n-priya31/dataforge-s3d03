"""
Unit tests for JOB-02: Transform Pipeline aggregation logic.
Tests the actual app/transform.py code, not a copy of it.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from transform import aggregate_regions


def test_single_region_aggregation():
    records = [
        {"amount": "100.00", "region": "South"},
        {"amount": "200.00", "region": "South"},
    ]
    report = aggregate_regions(records)
    assert report["South"]["order_count"] == 2
    assert report["South"]["total_amount"] == 300.00


def test_multiple_regions_separated_correctly():
    records = [
        {"amount": "100.00", "region": "South"},
        {"amount": "50.00", "region": "North"},
    ]
    report = aggregate_regions(records)
    assert report["South"]["total_amount"] == 100.00
    assert report["North"]["total_amount"] == 50.00


def test_empty_input_produces_empty_report():
    assert aggregate_regions([]) == {}


def test_unknown_region_handled():
    records = [{"amount": "10.00"}]
    report = aggregate_regions(records)
    assert report["unknown"]["order_count"] == 1
