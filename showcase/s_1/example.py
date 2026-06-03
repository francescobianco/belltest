import random


settings = ((0, 0), (0, 1), (1, 0), (1, 1))
context = {"hidden": 0, "a": 0, "b": 0, "rng": random.Random(11)}


class Experiment:
    def measure(self, setting):
        return 1 if context["rng"].random() < 0.5 else -1


def chsh(trials=20000):
    e0 = Experiment()
    e1 = Experiment()
    products = {pair: [] for pair in settings}

    for _ in range(trials):
        context["hidden"] = context["rng"].random()
        for a, b in settings:
            context["a"] = a
            context["b"] = b
            products[(a, b)].append(e0.measure(a) * e1.measure(b))

    e = {pair: sum(values) / len(values) for pair, values in products.items()}
    s = abs(e[(0, 0)] + e[(0, 1)] + e[(1, 0)] - e[(1, 1)])
    return s, e


s, e = chsh()
print("s_1: S < 1")
print("S =", round(s, 3))
print(e)
