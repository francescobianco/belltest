"""Use Bell/CHSH probes as a measuring instrument for an unknown measure.

The unknown measure is represented as a black box with two measurement outputs.  We run it
under the four CHSH settings and summarize its internal anatomy from the
observable correlations.
"""

from __future__ import annotations

import random
from typing import Callable, Tuple

from bell_lab import (
    SETTINGS,
    TrialContext,
    anatomy_signature,
    chsh_value,
    classify_s_value,
    format_expectations,
)

UnknownMeasure = Callable[[int, int, float, random.Random], Tuple[int, int]]


def hidden_local_measure(
    setting_a: int,
    setting_b: int,
    hidden: float,
    rng: random.Random,
) -> Tuple[int, int]:
    del rng
    outcome_a = 1 if hidden > (0.2 if setting_a == 0 else 0.65) else -1
    outcome_b = 1 if hidden > (0.35 if setting_b == 0 else 0.50) else -1
    return outcome_a, outcome_b


def leaky_unknown_measure(
    setting_a: int,
    setting_b: int,
    hidden: float,
    rng: random.Random,
) -> Tuple[int, int]:
    del hidden, rng
    outcome_a = 1
    outcome_b = -1 if setting_a == 1 and setting_b == 1 else 1
    return outcome_a, outcome_b


def noisy_quantum_like_measure(
    setting_a: int,
    setting_b: int,
    hidden: float,
    rng: random.Random,
) -> Tuple[int, int]:
    del hidden
    target_products = {
        (0, 0): -0.707,
        (0, 1): -0.707,
        (1, 0): -0.707,
        (1, 1): 0.707,
    }
    product = 1 if rng.random() < (1.0 + target_products[(setting_a, setting_b)]) / 2.0 else -1
    outcome_a = 1 if rng.random() < 0.5 else -1
    return outcome_a, outcome_a * product


def measure_black_box(
    name: str,
    unknown: UnknownMeasure,
    trials: int = 20_000,
    seed: int = 19,
) -> None:
    rng = random.Random(seed)
    products = {setting: [] for setting in SETTINGS}
    a_marginals = {setting: [] for setting in SETTINGS}
    b_marginals = {setting: [] for setting in SETTINGS}

    for trial in range(trials):
        hidden = rng.random()
        for setting_a, setting_b in SETTINGS:
            ctx = TrialContext(trial, hidden, setting_a, setting_b, rng)
            del ctx
            outcome_a, outcome_b = unknown(setting_a, setting_b, hidden, rng)
            products[(setting_a, setting_b)].append(outcome_a * outcome_b)
            a_marginals[(setting_a, setting_b)].append(outcome_a)
            b_marginals[(setting_a, setting_b)].append(outcome_b)

    expectations = {
        setting: sum(values) / len(values) for setting, values in products.items()
    }
    s_value = chsh_value(expectations)
    anatomy = anatomy_signature(expectations, a_marginals, b_marginals)

    print(name)
    print("-" * len(name))
    print(f"S={s_value:.3f} classification={classify_s_value(s_value)}")
    print(format_expectations(expectations))
    print(
        "signature: "
        f"signalling={anatomy['signalling']:.3f} "
        f"curvature={anatomy['correlation_curvature']:+.3f} "
        f"contrast={anatomy['correlation_contrast']:.3f} "
        f"label={anatomy['diagnostic_label']}"
    )
    print()


def main() -> None:
    measure_black_box("hidden_local_measure", hidden_local_measure)
    measure_black_box("leaky_unknown_measure", leaky_unknown_measure)
    measure_black_box("noisy_quantum_like_measure", noisy_quantum_like_measure)


if __name__ == "__main__":
    main()
