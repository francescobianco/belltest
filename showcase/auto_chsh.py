"""Auto-CHSH: compare one function with itself in two measurement roles."""

from __future__ import annotations

import random
from typing import Callable

from bell_lab import (
    CHSHResult,
    ModelSpec,
    Outcome,
    TrialContext,
    format_expectations,
    quantum_like_joint,
    run_model,
    threshold_response,
)

AutoFunction = Callable[[str, int, TrialContext], Outcome]


def local_auto_function(role: str, setting: int, ctx: TrialContext) -> Outcome:
    """One local function reused as A and B, with different thresholds by role."""

    if role == "A":
        return threshold_response(0.25, 0.70)(setting, ctx)
    return threshold_response(0.40, 0.60)(setting, ctx)


def leaky_auto_function(role: str, setting: int, ctx: TrialContext) -> Outcome:
    """One function whose B role can inspect A's setting."""

    if role == "A":
        return 1
    if setting == 0:
        return 1
    return -1 if ctx.alice_setting == 1 else 1


def auto_model(name: str, fn: AutoFunction, description: str) -> ModelSpec:
    return ModelSpec(
        name=name,
        family="auto_chsh",
        description=description,
        alice=lambda setting, ctx: fn("A", setting, ctx),
        bob=lambda setting, ctx: fn("B", setting, ctx),
    )


def print_result(title: str, result: CHSHResult) -> None:
    anatomy = result.anatomy
    print(title)
    print("-" * len(title))
    print(f"S              : {result.s_value:.3f} ({result.classification})")
    print(f"correlations   : {format_expectations(result.expectations)}")
    print(
        "anatomy        : "
        f"signalling={anatomy['signalling']:.3f}, "
        f"contrast={anatomy['correlation_contrast']:.3f}, "
        f"label={anatomy['diagnostic_label']}"
    )
    print()


def main() -> None:
    local = run_model(
        auto_model(
            "auto_local",
            local_auto_function,
            "Single function reused locally in role A and role B.",
        ),
        trials=20_000,
        seed=77,
    )
    leaky = run_model(
        auto_model(
            "auto_leaky",
            leaky_auto_function,
            "Single function reused with access to the remote setting.",
        ),
        trials=20_000,
        seed=77,
    )
    quantum_reference = run_model(
        ModelSpec(
            name="auto_quantum_reference",
            family="auto_chsh_reference",
            description="One joint callable used as an auto-CHSH reference sampler.",
            joint=quantum_like_joint,
        ),
        trials=20_000,
        seed=77,
    )

    print("auto_chsh: one function measured against itself")
    print("=" * 48)
    print_result("same function, local roles", local)
    print_result("same function, remote-setting leak", leaky)
    print_result("single joint function, quantum-like reference", quantum_reference)
    print("Reading:")
    print("- auto_local stays under the Bell/CHSH limit")
    print("- auto_leaky exceeds the limit because one role reads the remote setting")
    print("- the quantum-like reference exceeds S > 2 without visible signalling")


if __name__ == "__main__":
    random.seed(77)
    main()
