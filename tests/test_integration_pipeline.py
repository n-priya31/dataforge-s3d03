"""
Integration tests: run each job's main() end-to-end against temp files,
verifying the full read -> process -> write flow works correctly.
"""
import sys
import os
import json
import tempfile
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))


def test_ingestor_end_to_end(monkeypatch, tmp_path):
    input_csv = tmp_path / "input.csv"
    output_json = tmp_path / "output.json"
    input_csv.write_text(
        "order_id,customer,amount,region\n"
        "1,Alice,100.00,South\n"
        "2,Bob,-5,North\n"  # invalid, should be rejected
    )

    monkeypatch.setenv("INPUT_PATH", str(input_csv))
    monkeypatch.setenv("OUTPUT_PATH", str(output_json))
    monkeypatch.setenv("KEEP_ALIVE_SECONDS", "0")

    import ingestor
    importlib.reload(ingestor)
    ingestor.main()

    result = json.loads(output_json.read_text())
    assert len(result) == 1
    assert result[0]["customer"] == "Alice"


def test_transform_end_to_end(monkeypatch, tmp_path):
    input_json = tmp_path / "ingested.json"
    output_json = tmp_path / "report.json"
    input_json.write_text(json.dumps([
        {"amount": "100.00", "region": "South"},
        {"amount": "50.00", "region": "South"},
    ]))

    monkeypatch.setenv("INPUT_PATH", str(input_json))
    monkeypatch.setenv("OUTPUT_PATH", str(output_json))
    monkeypatch.setenv("KEEP_ALIVE_SECONDS", "0")

    import transform
    importlib.reload(transform)
    transform.main()

    result = json.loads(output_json.read_text())
    assert result["South"]["total_amount"] == 150.00


def test_feature_engineering_end_to_end(monkeypatch, tmp_path):
    input_json = tmp_path / "report.json"
    output_json = tmp_path / "features.json"
    input_json.write_text(json.dumps({
        "South": {"order_count": 2, "total_amount": 6000.00},
        "North": {"order_count": 1, "total_amount": 100.00},
    }))

    monkeypatch.setenv("INPUT_PATH", str(input_json))
    monkeypatch.setenv("OUTPUT_PATH", str(output_json))
    monkeypatch.setenv("KEEP_ALIVE_SECONDS", "0")

    import feature_engineering
    importlib.reload(feature_engineering)
    feature_engineering.main()

    result = json.loads(output_json.read_text())
    assert result["South"]["high_value_region"] is True
    assert result["_summary"]["top_region_by_revenue"] == "South"
