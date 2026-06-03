from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Callable


SETTINGS = ((0, 0), (0, 1), (1, 0), (1, 1))
MeasureRule = Callable[[str, int, float], int]


@dataclass(frozen=True)
class Experiment:
    name: str
    rule: MeasureRule

    def measure(self, setting: int, hidden: float) -> int:
        return self.rule(self.name, setting, hidden)


def threshold_rule(role: str, setting: int, hidden: float) -> int:
    thresholds = {
        "alice": (0.25, 0.70),
        "bob": (0.40, 0.60),
    }
    threshold = thresholds[role][setting]
    return 1 if hidden >= threshold else -1


def run_chsh(n_trials: int = 100_000) -> tuple[float, dict[tuple[int, int], float]]:
    alice = Experiment("alice", threshold_rule)
    bob = Experiment("bob", threshold_rule)
    products = {setting: [] for setting in SETTINGS}

    for _ in range(n_trials):
        hidden = random.random()
        for setting_a, setting_b in SETTINGS:
            outcome_a = alice.measure(setting_a, hidden)
            outcome_b = bob.measure(setting_b, hidden)
            products[(setting_a, setting_b)].append(outcome_a * outcome_b)

    expectations = {key: sum(values) / len(values) for key, values in products.items()}
    s_value = abs(
        expectations[(0, 0)]
        + expectations[(0, 1)]
        + expectations[(1, 0)]
        - expectations[(1, 1)]
    )
    return s_value, expectations


if __name__ == "__main__":
    print(run_chsh())
