from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter
import statistics as stats
from typing import Callable, Any

@dataclass
class PerfResult:
    latencies_ms: list[float]

    @property
    def p50(self): return stats.median(self.latencies_ms)
    @property
    def p95(self): return stats.quantiles(self.latencies_ms, n=100)[94] if len(self.latencies_ms) >= 100 else sorted(self.latencies_ms)[int(len(self.latencies_ms)*0.95)-1]
    @property
    def avg(self): return stats.mean(self.latencies_ms)

def time_call(fn: Callable[[], Any]) -> float:
    t0 = perf_counter()
    fn()
    t1 = perf_counter()
    return (t1 - t0) * 1000
