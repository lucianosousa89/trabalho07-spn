"""Resultados obtidos no Jupiter (simulação estacionária, 10.000 s) e teoria M/M/c/K."""
from math import factorial

MU = 20.0  # req/s por servidor

# (experimento, nível, lambda, c, K, DP%, TP req/s, U%, MRT s)  -> valores do Jupiter
JUPITER = [
    ("E1", "λ=20",  20, 3, 20, 0.0000, 20.0122, 33.3537, 0.0523),
    ("E1", "λ=40",  40, 3, 20, 0.0150, 39.9890, 66.6483, 0.0721),
    ("E1", "λ=60",  60, 3, 20, 5.0135, 56.9878, 94.9797, 0.1851),
    ("E1", "λ=80",  80, 3, 20, 25.0774, 59.9324, 99.8874, 0.2847),
    ("E1", "λ=100", 100, 3, 20, 40.0012, 59.9982, 99.9970, 0.3084),
    ("E2", "c=2", 40, 2, 20, 4.8436, 38.0473, 95.1182, 0.2688),
    ("E2", "c=3", 40, 3, 20, 0.0150, 39.9890, 66.6483, 0.0721),
    ("E2", "c=4", 40, 4, 20, 0.0001, 40.0036, 50.0045, 0.0544),
    ("E3", "K=5",  40, 3, 5,  7.5871, 36.9624, 61.6041, 0.0572),
    ("E3", "K=10", 40, 3, 10, 0.8801, 39.6608, 66.1013, 0.0684),
    ("E3", "K=20", 40, 3, 20, 0.0150, 39.9890, 66.6483, 0.0721),
    ("E4", "A (20, 2)", 20, 2, 20, 0.000076, 20.005445, 50.013612, 0.066690),
    ("E4", "B (40, 3)", 40, 3, 20, 0.014987, 39.989005, 66.648341, 0.072072),
    ("E4", "C (80, 5)", 80, 5, 20, 0.392406, 79.703866, 79.703866, 0.074274),
]


def mmck(lam, mu, c, K):
    """Fila M/M/c/K: devolve (DP%, TP, U%, MRT em s)."""
    a = lam / mu
    p = [a ** n / factorial(n) if n <= c else a ** n / (factorial(c) * c ** (n - c)) for n in range(K + 1)]
    s = sum(p)
    p = [x / s for x in p]
    Lq = sum((n - c) * p[n] for n in range(c + 1, K + 1))
    Ls = sum(n * p[n] for n in range(K + 1))
    pb = p[K]
    tp = lam * (1 - pb)
    return pb * 100, tp, (Ls - Lq) / c * 100, Ls / tp

# Nível extra executado no Jupiter (não usado no artigo, que segue os 3 limites do enunciado)
EXTRA_E3_K15 = ("E3", "K=15", 40, 3, 15, 0.1153, 39.9718, 66.6196, 0.0714)
