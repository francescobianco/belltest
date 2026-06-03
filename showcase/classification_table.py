"""Print a compact taxonomy of CHSH function families."""

from bell_lab import format_expectations, iter_results


def main() -> None:
    print("CHSH classification table")
    print("=" * 98)
    print(
        f"{'model':<24} {'family':<28} {'S':>6} "
        f"{'classification':<22} {'anatomy':<28} expectations"
    )
    print("-" * 98)
    for result in iter_results():
        print(
            f"{result.name:<24} "
            f"{result.family:<28} "
            f"{result.s_value:>6.3f} "
            f"{result.classification:<22} "
            f"{result.anatomy['diagnostic_label']:<28} "
            f"{format_expectations(result.expectations)}"
        )


if __name__ == "__main__":
    main()
