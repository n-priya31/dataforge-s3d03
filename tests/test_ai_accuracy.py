from app.anomaly_detector import detect_anomaly
import time


SCENARIOS = {
    "memory_leak": [
        {
            "memory_usage_mb": [500, 650, 800, 950],
            "throughput_records_per_second": 100,
            "cpu_percent": 60,
        }
    ] * 10,
    "throughput_degradation": [
        {
            "memory_usage_mb": [500, 510, 515, 520],
            "throughput_records_per_second": [1000, 800, 600, 400],
            "cpu_percent": 70,
        }
    ] * 10,
    "resource_starvation": [
        {
            "memory_usage_mb": [900, 920, 940, 950],
            "throughput_records_per_second": [100, 95, 90, 85],
            "cpu_percent": [98, 99, 99, 100],
        }
    ] * 10,
}


EXPECTED = {
    "memory_leak": "Memory leak or abnormal memory growth",
    "throughput_degradation": "Throughput degradation",
    "resource_starvation": "Resource starvation",
}


def run_accuracy_test():
    results = {}

    for scenario, metrics_list in SCENARIOS.items():
        correct = 0

        print(f"\nTesting {scenario}...")

        for i, metrics in enumerate(metrics_list, start=1):
            response = None

            for attempt in range(3):
                try:
                    response = detect_anomaly(metrics)
                    break
                except Exception as exc:
                    if attempt == 2:
                        print(f"  Run {i}/10: ERROR after 3 attempts: {exc}")
                        break
                    print(f"  Run {i}/10: temporary error, retrying ({attempt + 1}/3)...")
                    time.sleep(5)

            if response and EXPECTED[scenario].lower() in response.lower():
                correct += 1
                result = "PASS"
            else:
                result = "FAIL"

            print(f"  Run {i}/10: {result}")

        results[scenario] = correct

    print("\n=== AI ACCURACY RESULTS ===")

    total_correct = 0
    total_tests = 0

    for scenario, correct in results.items():
        accuracy = correct / 10 * 100
        total_correct += correct
        total_tests += 10
        print(f"{scenario}: {correct}/10 ({accuracy:.1f}%)")

    overall_accuracy = total_correct / total_tests * 100

    print("--------------------------------")
    print(f"Overall: {total_correct}/{total_tests} ({overall_accuracy:.1f}%)")


if __name__ == "__main__":
    run_accuracy_test()
