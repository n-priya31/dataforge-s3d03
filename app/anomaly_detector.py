import os
from google import genai

SCENARIOS = {
    "memory_leak": "Memory leak or abnormal memory growth",
    "throughput_degradation": "Throughput degradation",
    "resource_starvation": "Resource starvation",
}


def create_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable is not set")
    return genai.Client(api_key=api_key)


def detect_anomaly(metrics):
    client = create_client()

    prompt = f"""
You are an anomaly detection system for the DataForge containerized
data processing environment.

Analyze these processing metrics:

{metrics}

Determine whether an anomaly is present.

Possible anomaly scenarios:
1. Memory leak or abnormal memory growth
2. Throughput degradation
3. Resource starvation

Return:
- anomaly_detected: true or false
- scenario: one of the three scenarios above, or none
- explanation: brief explanation
- recommendation: resource optimization recommendation
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    return response.text
