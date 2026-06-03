from __future__ import annotations

from dataclasses import dataclass
import random
from typing import Callable


SETTINGS = ((0, 0), (0, 1), (1, 0), (1, 1))
MeasureRule = Callable[[str, int], int]


@dataclass
class Environment:
    hidden: float = 0.0
    setting_a: int = 0
    setting_b: int = 0


ENV = Environment()


@dataclass(frozen=True)
class Experiment:
    name: str
    rule: MeasureRule

    def measure(self, setting: int) -> int:
        return self.rule(self.name, setting)


def threshold_rule(role: str, setting: int) -> int:
    thresholds = {
        "alice": (0.25, 0.70),
        "bob": (0.40, 0.60),
    }
    threshold = thresholds[role][setting]
    return 1 if ENV.hidden >= threshold else -1


def run_chsh(n_trials: int = 100_000) -> tuple[float, dict[tuple[int, int], float]]:
    alice = Experiment("alice", threshold_rule)
    bob = Experiment("bob", threshold_rule)
    products = {setting: [] for setting in SETTINGS}

    for _ in range(n_trials):
        ENV.hidden = random.random()
        for setting_a, setting_b in SETTINGS:
            ENV.setting_a = setting_a
            ENV.setting_b = setting_b
            outcome_a = alice.measure(setting_a)
            outcome_b = bob.measure(setting_b)
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
