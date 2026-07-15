"""
JOB-03: Feature Engineering
Reads JOB-02's regional report and derives simple features:
average sale per region, highest region by revenue, and a
"high-value region" flag for reporting/anomaly-detection use later.
"""
import json
import os
import time

INPUT_PATH = os.environ.get("INPUT_PATH", "/data/transformed_report.json")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/data/feature_report.json")
HIGH_VALUE_THRESHOLD = float(os.environ.get("HIGH_VALUE_THRESHOLD", "5000"))


def main():
    print(f"[feature-eng] starting, reading from {INPUT_PATH}", flush=True)

    with open(INPUT_PATH) as f:
        report = json.load(f)

    features = {}
    for region, stats in report.items():
        count = stats["order_count"]
        total = stats["total_amount"]
        avg = total / count if count else 0
        features[region] = {
            "order_count": count,
            "total_amount": total,
            "avg_order_value": round(avg, 2),
            "high_value_region": total >= HIGH_VALUE_THRESHOLD,
        }

    top_region = max(features, key=lambda r: features[r]["total_amount"])
    features["_summary"] = {"top_region_by_revenue": top_region}

    with open(OUTPUT_PATH, "w") as f:
        json.dump(features, f, indent=2)

    print(f"[feature-eng] wrote feature report to {OUTPUT_PATH}: {features}", flush=True)
    time.sleep(int(os.environ.get("KEEP_ALIVE_SECONDS", "30")))


if __name__ == "__main__":
    main()
