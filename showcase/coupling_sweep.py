"""Sweep an information-leak parameter and observe the CHSH phase change."""

from __future__ import annotations

from bell_lab import (
    ModelSpec,
    TrialContext,
    deterministic_table,
    format_expectations,
    run_model,
)


def make_partial_leak_model(leak_probability: float) -> ModelSpec:
    def bob(setting: int, ctx: TrialContext) -> int:
        if setting == 0:
            return 1
        if ctx.rng.random() < leak_probability:
            return -1 if ctx.alice_setting == 1 else 1
        return 1

    return ModelSpec(
        name=f"partial_leak_{leak_probability:.2f}",
        family="non_local_leak_sweep",
        description="Bob reads Alice's setting with tunable probability.",
        alice=deterministic_table((1, 1)),
        bob=bob,
    )


def main() -> None:
    print("Information coupling sweep")
    print("=" * 86)
    print(f"{'leak':>6} {'S':>6} {'classification':<22} {'signature':<28} expectations")
    print("-" * 86)
    for step in range(0, 11):
        leak = step / 10
        result = run_model(make_partial_leak_model(leak), trials=20_000, seed=101)
        print(
            f"{leak:>6.2f} "
            f"{result.s_value:>6.3f} "
            f"{result.classification:<22} "
            f"{result.anatomy['diagnostic_label']:<28} "
            f"{format_expectations(result.expectations)}"
        )


if __name__ == "__main__":
    main()
