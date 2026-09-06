import app.worker as worker


def test_burn_cpu_completes(monkeypatch):
    times = iter([0, 0, 0, 1])

    monkeypatch.setattr(worker.time, "time", lambda: next(times))

    worker.burn_cpu(1)
