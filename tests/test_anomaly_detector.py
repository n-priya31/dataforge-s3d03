from unittest.mock import Mock, patch

from app.anomaly_detector import SCENARIOS, detect_anomaly


def test_three_required_anomaly_scenarios():
    assert len(SCENARIOS) == 3
    assert "memory_leak" in SCENARIOS
    assert "throughput_degradation" in SCENARIOS
    assert "resource_starvation" in SCENARIOS


@patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"})
@patch("app.anomaly_detector.genai.Client")
def test_memory_leak_detection(mock_client):
    mock_response = Mock()
    mock_response.text = (
        "anomaly_detected: true\n"
        "scenario: Memory leak or abnormal memory growth\n"
        "explanation: Memory usage is increasing continuously.\n"
        "recommendation: Investigate memory growth and increase memory limits."
    )

    mock_client.return_value.models.generate_content.return_value = mock_response

    result = detect_anomaly({
        "memory_usage_mb": [500, 650, 800, 950],
        "throughput_records_per_second": 100
    })

    assert "anomaly_detected: true" in result
    assert "Memory leak" in result


@patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"})
@patch("app.anomaly_detector.genai.Client")
def test_throughput_degradation_detection(mock_client):
    mock_response = Mock()
    mock_response.text = (
        "anomaly_detected: true\n"
        "scenario: Throughput degradation\n"
        "explanation: Processing throughput has decreased significantly.\n"
        "recommendation: Increase worker capacity."
    )

    mock_client.return_value.models.generate_content.return_value = mock_response

    result = detect_anomaly({
        "throughput_records_per_second": [1000, 800, 500, 200],
        "cpu_percent": 70
    })

    assert "anomaly_detected: true" in result
    assert "Throughput degradation" in result


@patch.dict("os.environ", {"GEMINI_API_KEY": "test-key"})
@patch("app.anomaly_detector.genai.Client")
def test_resource_starvation_detection(mock_client):
    mock_response = Mock()
    mock_response.text = (
        "anomaly_detected: true\n"
        "scenario: Resource starvation\n"
        "explanation: CPU resources are insufficient for the workload.\n"
        "recommendation: Increase CPU allocation or worker replicas."
    )

    mock_client.return_value.models.generate_content.return_value = mock_response

    result = detect_anomaly({
        "cpu_percent": 98,
        "memory_percent": 95,
        "queue_depth": 500
    })

    assert "anomaly_detected: true" in result
    assert "Resource starvation" in result
