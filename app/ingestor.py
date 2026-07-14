"""
JOB-01: Batch Ingestor
Reads raw CSV input, validates rows, writes cleaned JSON output.
Runs identically regardless of environment (local / container / k8s)
because all dependencies are pinned in the Docker image.
"""
import csv
import json
import os
import time

INPUT_PATH = os.environ.get("INPUT_PATH", "/app/sample_input.csv")
OUTPUT_PATH = os.environ.get("OUTPUT_PATH", "/data/ingested_output.json")


def validate_row(row):
    try:
        row["amount"] = float(row["amount"])
        row["order_id"] = int(row["order_id"])
        return row["amount"] > 0 and row["order_id"] > 0
    except (ValueError, KeyError):
        return False


def main():
    print(f"[ingestor] starting, reading from {INPUT_PATH}", flush=True)
    records = []
    rejected = 0

    with open(INPUT_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if validate_row(row):
                records.append(row)
            else:
                rejected += 1

    with open(OUTPUT_PATH, "w") as f:
        json.dump(records, f, indent=2)

    print(f"[ingestor] processed {len(records)} valid rows, "
          f"{rejected} rejected, wrote {OUTPUT_PATH}", flush=True)

    time.sleep(int(os.environ.get("KEEP_ALIVE_SECONDS", "30")))


if __name__ == "__main__":
    main()