"""Auto-CHSH: compare one function with itself in two measurement roles."""

from __future__ import annotations

import random
from bell_lab import (
    CHSHResult,
    ModelSpec,
    Outcome,
    TrialContext,
    format_expectations,
    quantum_like_joint,
    run_model,
    Experiment,
    threshold_response,
)

def local_measure_rule(role: str, setting: int, ctx: TrialContext) -> Outcome:
    """One measure rule reused by two Experiment instances."""

    if role == "alice":
        return threshold_response(0.25, 0.70)(role, setting, ctx)
    return threshold_response(0.40, 0.60)(role, setting, ctx)


def leaky_measure_rule(role: str, setting: int, ctx: TrialContext) -> Outcome:
    """One measure rule whose second instance can inspect the first setting."""

    if role == "alice":
        return 1
    if setting == 0:
        return 1
    return -1 if ctx.setting_a == 1 else 1


def auto_model(name: str, measure_rule, description: str) -> ModelSpec:
    return ModelSpec(
        name=name,
        family="auto_chsh",
        description=description,
        experiment_a=Experiment("alice", measure_rule),
        experiment_b=Experiment("bob", measure_rule),
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
            local_measure_rule,
            "Single Experiment.measure rule reused by two instances.",
        ),
        trials=20_000,
        seed=77,
    )
    leaky = run_model(
        auto_model(
            "auto_leaky",
            leaky_measure_rule,
            "Single Experiment.measure rule reused with access to the remote setting.",
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

    print("auto_chsh: one Experiment.measure rule measured against itself")
    print("=" * 48)
    print_result("same measure rule, local roles", local)
    print_result("same measure rule, remote-setting leak", leaky)
    print_result("single joint measure, quantum-like reference", quantum_reference)
    print("Reading:")
    print("- auto_local stays under the Bell/CHSH limit")
    print("- auto_leaky exceeds the limit because one role reads the remote setting")
    print("- the quantum-like reference exceeds S > 2 without visible signalling")


if __name__ == "__main__":
    random.seed(77)
    main()
