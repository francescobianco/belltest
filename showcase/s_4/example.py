import random


settings = ((0, 0), (0, 1), (1, 0), (1, 1))
context = {"hidden": 0, "a": 0, "b": 0, "rng": random.Random(44)}


class Experiment:
    def measure(self, setting):
        product = {
            (0, 0): 1,
            (0, 1): 1,
            (1, 0): 1,
            (1, 1): -1 if context["a"] == 1 else 1,
        }[(context["side"], setting)]
        return product


def chsh(trials=20000):
    e0 = Experiment()
    e1 = Experiment()
    products = {pair: [] for pair in settings}

    for _ in range(trials):
        context["hidden"] = context["rng"].random()
        for a, b in settings:
            context["a"] = a
            context["b"] = b
            context["side"] = 0
            outcome_a = e0.measure(a)
            context["side"] = 1
            outcome_b = e1.measure(b)
            products[(a, b)].append(outcome_a * outcome_b)

    e = {pair: sum(values) / len(values) for pair, values in products.items()}
    s = abs(e[(0, 0)] + e[(0, 1)] + e[(1, 0)] - e[(1, 1)])
    return s, e


s, e = chsh()
print("s_4: 3 <= S <= 4")
print("S =", round(s, 3))
print(e)
