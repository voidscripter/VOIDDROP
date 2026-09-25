"""Upload stream persistence and in-memory transfer counters."""

from dataclasses import dataclass
import time


@dataclass
class Transfer:
    name: str
    received: int = 0
    started: float = 0.0

    @property
    def speed(self) -> float:
        elapsed = max(time.monotonic() - self.started, 0.001)
        return self.received / elapsed
