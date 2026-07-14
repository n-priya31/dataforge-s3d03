"""
JOB-02: Transform Pipeline
Reads the ingestor's output and produces an aggregated report
(total sales and order count per region).
"""
import json
import os
import time
from collections import defaultdict

INPUT_PATH = os.environ.get("INPUT_PATH", "/data/ingested_output.json")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/data/transformed_report.json")


def main():
    print(f"[transform] starting, reading from {INPUT_PATH}", flush=True)

    with open(INPUT_PATH) as f:
        records = json.load(f)

    totals = defaultdict(lambda: {"order_count": 0, "total_amount": 0.0})
    for r in records:
        region = r.get("region", "unknown")
        totals[region]["order_count"] += 1
        totals[region]["total_amount"] += float(r["amount"])

    report = {region: stats for region, stats in totals.items()}

    with open(OUTPUT_PATH, "w") as f:
        json.dump(report, f, indent=2)

    print(f"[transform] wrote regional report to {OUTPUT_PATH}: {report}", flush=True)
    time.sleep(int(os.environ.get("KEEP_ALIVE_SECONDS", "30")))


if __name__ == "__main__":
    main()