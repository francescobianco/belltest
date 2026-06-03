"""Immediate demo: CHSH local hidden variable vs Bell violation."""

from bell_lab import MODELS, CHSHResult, format_expectations, run_model


def find_result(name: str) -> CHSHResult:
    for model in MODELS:
        if model.name == name:
            return run_model(model, trials=20_000, seed=42)
    raise ValueError(f"missing model: {name}")


def print_result(title: str, result: CHSHResult) -> None:
    anatomy = result.anatomy
    print(title)
    print("-" * len(title))
    print(f"model          : {result.name}")
    print(f"family         : {result.family}")
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
    hidden = find_result("shared_thresholds")
    no_local_hidden = find_result("quantum_singlet_sampler")

    print("Bell/CHSH demo: local hidden variable vs S > 2")
    print("=" * 52)
    print_result("LOCAL hidden-variable model", hidden)
    print_result("NO local hidden-variable model", no_local_hidden)
    print("Reading:")
    print("- the local hidden-variable model has structure but stays inside S <= 2")
    print("- the quantum-like model violates the Bell/CHSH bound with S > 2")
    print("- low signalling means the violation is not explained by visible remote leakage")


if __name__ == "__main__":
    main()
