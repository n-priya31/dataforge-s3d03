"""
Unit tests for JOB-01: Batch Ingestor validation logic.
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))
from ingestor import validate_row


def test_valid_row_passes():
    row = {"order_id": "1001", "amount": "2450.50", "region": "South"}
    assert validate_row(row) is True


def test_negative_amount_rejected():
    row = {"order_id": "1002", "amount": "-50.00", "region": "North"}
    assert validate_row(row) is False


def test_zero_amount_rejected():
    row = {"order_id": "1003", "amount": "0", "region": "East"}
    assert validate_row(row) is False


def test_non_numeric_amount_rejected():
    row = {"order_id": "1004", "amount": "not_a_number", "region": "West"}
    assert validate_row(row) is False


def test_missing_order_id_rejected():
    row = {"amount": "100.00", "region": "South"}
    assert validate_row(row) is False


def test_zero_order_id_rejected():
    row = {"order_id": "0", "amount": "100.00", "region": "South"}
    assert validate_row(row) is False
