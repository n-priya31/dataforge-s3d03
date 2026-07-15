"""
Unit tests for JOB-03: Feature Engineering logic.
Tests the actual app/feature_engineering.py code, not a copy of it.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from feature_engineering import compute_features


def test_average_order_value_calculated_correctly():
    report = {"South": {"order_count": 2, "total_amount": 300.00}}
    features = compute_features(report)
    assert features["South"]["avg_order_value"] == 150.00


def test_high_value_region_flagged_correctly():
    report = {"South": {"order_count": 1, "total_amount": 6000.00}}
    features = compute_features(report)
    assert features["South"]["high_value_region"] is True


def test_low_value_region_not_flagged():
    report = {"North": {"order_count": 1, "total_amount": 500.00}}
    features = compute_features(report)
    assert features["North"]["high_value_region"] is False


def test_zero_orders_does_not_divide_by_zero():
    report = {"East": {"order_count": 0, "total_amount": 0.0}}
    features = compute_features(report)
    assert features["East"]["avg_order_value"] == 0
