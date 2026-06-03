import random


context = {"hidden": 0, "a": 0, "b": 0, "side": 0, "rng": random.Random(44)}


class Experiment:
    def __init__(self, side):
        self.side = side

    def measure(self, setting):
        global context
        if self.side == 0:
            return 1
        if setting == 0:
            return 1
        if context["a"] == 1:
            return -1
        return 1


def chsh(trials=20000):
    p00 = p01 = p10 = p11 = 0
    e0 = Experiment(0)
    e1 = Experiment(1)

    for _ in range(trials):
        context["hidden"] = context["rng"].random()

        context["a"] = 0
        context["b"] = 0
        x = e0.measure(0)
        y = e1.measure(0)
        p00 += x * y

        context["a"] = 0
        context["b"] = 1
        x = e0.measure(0)
        y = e1.measure(1)
        p01 += x * y

        context["a"] = 1
        context["b"] = 0
        x = e0.measure(1)
        y = e1.measure(0)
        p10 += x * y

        context["a"] = 1
        context["b"] = 1
        x = e0.measure(1)
        y = e1.measure(1)
        p11 += x * y

    e00 = p00 / trials
    e01 = p01 / trials
    e10 = p10 / trials
    e11 = p11 / trials
    s = abs(e00 + e01 + e10 - e11)
    return s, {"00": e00, "01": e01, "10": e10, "11": e11}


s, e = chsh()
print("s_4: 3 <= S <= 4")
print("S =", round(s, 3))
print(e)
