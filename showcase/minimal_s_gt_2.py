"""Constructive minimal measure with S > 2 from one input parameter.

The input x encodes the four CHSH rows:

    x = 0 -> A0,B0
    x = 1 -> A0,B1
    x = 2 -> A1,B0
    x = 3 -> A1,B1

The whole construction is the product pattern:

    + + + -

That last minus is the single line that gives S > 2.
"""


def local_measure_product(x: int) -> int:
    """Baseline: same product in all four rows, so S = 2."""

    del x
    return 1


def bell_breaking_measure_product(x: int) -> int:
    """Minimal constructive violation: + + + - gives S = 4."""

    return -1 if x == 3 else 1
    #      ^^^^^^^^^^^^^^^^^
    # This is the property-giving line: the last CHSH row becomes negative.


def response_pair(product: int) -> tuple[int, int]:
    """Build two outputs whose product is the requested correlation."""

    a = 1
    b = product
    return a, b


def chsh_from_one_parameter(measure_product) -> tuple[float, list[int]]:
    products = [measure_product(x) for x in range(4)]
    s_value = abs(products[0] + products[1] + products[2] - products[3])
    return float(s_value), products


def print_case(name: str, measure_product) -> None:
    s_value, products = chsh_from_one_parameter(measure_product)
    print(name)
    print("-" * len(name))
    print("x rows         : 0  1  2  3")
    print("meaning        : 00 01 10 11")
    print("products       : " + " ".join(f"{p:+d}" for p in products))
    print(f"S              : {s_value:.1f}")
    print()


def main() -> None:
    print("Minimal constructive CHSH measure")
    print("=" * 42)
    print_case("baseline measure: S <= 2", local_measure_product)
    print_case("one-line modified measure: S > 2", bell_breaking_measure_product)
    print("The measure line that creates the violation is:")
    print()
    print("    return -1 if x == 3 else 1")
    print()
    print("Why it works:")
    print("    S = |p0 + p1 + p2 - p3|")
    print("    S = |+1 + +1 + +1 - (-1)| = 4")


if __name__ == "__main__":
    main()
