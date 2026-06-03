"""Use Bell/CHSH probes as a measuring instrument for an unknown function.

The unknown function is represented as a black box with two outputs.  We run it
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

UnknownFunction = Callable[[int, int, float, random.Random], Tuple[int, int]]


def hidden_local_function(
    alice_setting: int,
    bob_setting: int,
    hidden: float,
    rng: random.Random,
) -> Tuple[int, int]:
    del rng
    alice = 1 if hidden > (0.2 if alice_setting == 0 else 0.65) else -1
    bob = 1 if hidden > (0.35 if bob_setting == 0 else 0.50) else -1
    return alice, bob


def leaky_unknown_function(
    alice_setting: int,
    bob_setting: int,
    hidden: float,
    rng: random.Random,
) -> Tuple[int, int]:
    del hidden, rng
    alice = 1
    bob = -1 if alice_setting == 1 and bob_setting == 1 else 1
    return alice, bob


def noisy_quantum_like_function(
    alice_setting: int,
    bob_setting: int,
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
    product = 1 if rng.random() < (1.0 + target_products[(alice_setting, bob_setting)]) / 2.0 else -1
    alice = 1 if rng.random() < 0.5 else -1
    return alice, alice * product


def measure_unknown(
    name: str,
    unknown: UnknownFunction,
    trials: int = 20_000,
    seed: int = 19,
) -> None:
    rng = random.Random(seed)
    products = {setting: [] for setting in SETTINGS}
    alice_marginals = {setting: [] for setting in SETTINGS}
    bob_marginals = {setting: [] for setting in SETTINGS}

    for trial in range(trials):
        hidden = rng.random()
        for alice_setting, bob_setting in SETTINGS:
            ctx = TrialContext(trial, hidden, alice_setting, bob_setting, rng)
            del ctx
            alice, bob = unknown(alice_setting, bob_setting, hidden, rng)
            products[(alice_setting, bob_setting)].append(alice * bob)
            alice_marginals[(alice_setting, bob_setting)].append(alice)
            bob_marginals[(alice_setting, bob_setting)].append(bob)

    expectations = {
        setting: sum(values) / len(values) for setting, values in products.items()
    }
    s_value = chsh_value(expectations)
    anatomy = anatomy_signature(expectations, alice_marginals, bob_marginals)

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
    measure_unknown("hidden_local_function", hidden_local_function)
    measure_unknown("leaky_unknown_function", leaky_unknown_function)
    measure_unknown("noisy_quantum_like_function", noisy_quantum_like_function)


if __name__ == "__main__":
    main()
