"""
DataForge Worker — demo service for HPA auto-scaling.
Alternates between a CPU-intensive burst and an idle period so you can
observe Horizontal Pod Autoscaler scale up during load and back down
once load subsides.
"""
import hashlib
import os
import time

BUSY_SECONDS = int(os.environ.get("BUSY_SECONDS", "120"))
IDLE_SECONDS = int(os.environ.get("IDLE_SECONDS", "120"))


def burn_cpu(duration):
    end = time.time() + duration
    data = b"dataforge"
    while time.time() < end:
        data = hashlib.sha256(data).digest()


def main():
    print("[worker] starting CPU load/idle cycle", flush=True)
    while True:
        print(f"[worker] BUSY for {BUSY_SECONDS}s", flush=True)
        burn_cpu(BUSY_SECONDS)
        print(f"[worker] IDLE for {IDLE_SECONDS}s", flush=True)
        time.sleep(IDLE_SECONDS)


if __name__ == "__main__":
    main()
