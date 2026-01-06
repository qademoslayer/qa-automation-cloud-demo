import concurrent.futures as cf
import pytest
from utils.perf import PerfResult, time_call

@pytest.mark.perf
def test_light_concurrency_and_latency(base_url, api):
    """
    performance light ：trigger GET endpoint，calculate latency
    """
    url = f"{base_url}/api/v1/health"

    def one_call():
        r = api.get(url, timeout=10)
        assert r.status_code == 200

    concurrency = 10
    total_requests = 50

    latencies = []
    with cf.ThreadPoolExecutor(max_workers=concurrency) as ex:
        futures = [ex.submit(lambda: time_call(one_call)) for _ in range(total_requests)]
        for f in cf.as_completed(futures):
            latencies.append(f.result())

    res = PerfResult(latencies_ms=latencies)

    # light tracking
    assert res.p95 < 1500, f"p95 too high: {res.p95:.1f}ms"
    assert res.avg < 800, f"avg too high: {res.avg:.1f}ms"

    print(f"Perf summary: n={len(latencies)} avg={res.avg:.1f}ms p50={res.p50:.1f}ms p95={res.p95:.1f}ms")
