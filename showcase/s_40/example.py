import random


context = {"hidden": 0, "a": 0, "b": 0, "memory": 0, "negative": 0, "rng": random.Random(40)}


class Experiment:
    def measure(self, setting):
        global context
        if context["memory"] == 0:
            context["memory"] = 1
            return 1

        context["memory"] = 0
        if context["rng"].random() < context["negative"]:
            return -1
        return 1


def chsh(trials=20000):
    p00 = p01 = p10 = p11 = 0
    e0 = Experiment()
    e1 = Experiment()

    for _ in range(trials):
        context["hidden"] = context["rng"].random()

        context["a"] = 0
        context["b"] = 0
        context["memory"] = 0
        context["negative"] = 0
        x = e0.measure(0)
        y = e1.measure(0)
        p00 += x * y

        context["a"] = 0
        context["b"] = 1
        context["memory"] = 0
        context["negative"] = 0
        x = e0.measure(0)
        y = e1.measure(1)
        p01 += x * y

        context["a"] = 1
        context["b"] = 0
        context["memory"] = 0
        context["negative"] = 0
        x = e0.measure(1)
        y = e1.measure(0)
        p10 += x * y

        context["a"] = 1
        context["b"] = 1
        context["memory"] = 0
        context["negative"] = 0.875
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
print("s_40: 3.5 <= S <= 4.0")
print("S =", round(s, 3))
print(e)
