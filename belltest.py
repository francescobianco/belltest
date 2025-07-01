import random


def hidden_variable():
    return random.random()

def alice(setting, hidden):
    global q
    if setting == 0:
        v = q
        q = q - v
        return 1 if v > 10 else -1
    else:
        return 1 #if hidden < 0.5 else -1
        #v = random.random() * q
        #q = q - v
        #return 1 if v > 10 else -1
    #return 1

def bob(setting, hidden):
    global q
    if setting == 0:
        v = q
        q = q - v
        return 1 if v > 10 else -1
    else:
        return 1 #if hidden > 0.8 else -1
        #v = random.random() * q
        #q = q - v
        #return 1 if v > 10 else -1
    #return -1

def run_chsh(n_trials=1000000):
    global q
    settings = [(0,0), (0,1), (1,0), (1,1)]
    results = {s: [] for s in settings}
    for _ in range(n_trials):
        hidden = hidden_variable()
        q = 20
        for a_set, b_set in settings:
            a = alice(a_set, hidden)
            b = bob(b_set, hidden)
            results[(a_set, b_set)].append(a * b)

    E = {k: sum(v)/len(v) for k,v in results.items()}
    S = abs(E[(0,0)] + E[(0,1)] + E[(1,0)] - E[(1,1)])

    return S, E

q = 20

print(run_chsh())
