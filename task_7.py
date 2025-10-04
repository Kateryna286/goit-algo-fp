import math
import random
from collections import Counter
from typing import Dict, Tuple, List

def simulate_two_dice(n_rolls: int, seed: int = 123) -> Dict[int, int]:
    """Імітує n_rolls кидків двох кубиків. Повертає лічильники сум 2..12."""
    if n_rolls <= 0:
        raise ValueError("n_rolls має бути > 0")
    random.seed(seed)
    cnt = Counter()
    for _ in range(n_rolls):
        s = random.randint(1, 6) + random.randint(1, 6)
        cnt[s] += 1
    return {s: cnt.get(s, 0) for s in range(2, 13)}

def analytic_distribution() -> Tuple[Dict[int, int], Dict[int, float]]:
    """Кількість способів і аналітичні ймовірності для сум 2..12."""
    ways = {2:1, 3:2, 4:3, 5:4, 6:5, 7:6, 8:5, 9:4, 10:3, 11:2, 12:1}
    total = 36
    probs = {s: ways[s] / total for s in range(2, 13)}
    return ways, probs

def build_table(counts_mc: Dict[int, int], n_rolls: int):
    """Готує табличні рядки з порівнянням MC vs аналітика."""
    _, p_an = analytic_distribution()
    rows: List[Tuple[int, float, float, float, float, int]] = []
    sse = 0.0
    for s in range(2, 13):
        p_mc = counts_mc[s] / n_rolls
        pA = p_an[s]
        abs_err = abs(p_mc - pA)
        rel_err = (abs_err / pA) * 100.0
        sse += (p_mc - pA) ** 2
        rows.append((s, p_mc, pA, abs_err, rel_err, counts_mc[s]))
    rmse = math.sqrt(sse / len(rows))
    return rows, rmse

def print_table(rows):
    print(f"{'Sum':>3} | {'MC prob':>9} | {'Analytic':>9} | {'Abs err':>9} | {'Rel err %':>9} | {'MC count':>8}")
    print("-" * 64)
    for s, p_mc, p_an, ae, re, c in rows:
        print(f"{s:>3} | {p_mc:9.5f} | {p_an:9.5f} | {ae:9.5f} | {re:9.3f} | {c:8d}")

def plot(rows, title="Two dice: Monte Carlo vs Analytic"):
    try:
        import matplotlib.pyplot as plt
    except Exception:
        return  
    xs = [r[0] for r in rows]
    mc = [r[1] for r in rows]
    an = [r[2] for r in rows]

    plt.figure(figsize=(10, 5))
    # Стовпчики Монте-Карло 
    plt.bar(xs, mc, width=0.7, label="Monte Carlo")

    # Підписи відсотків над стовпчиками
    for x, p in zip(xs, mc):
        plt.text(x, p, f"{p*100:.2f}%", ha='center', va='bottom', fontsize=9)

    # Лінія аналітики
    plt.plot(xs, an, marker="o", linewidth=2, color="#FFA500", label="Analytic")

    plt.xlabel("Сума двох кубиків")
    plt.ylabel("Ймовірність")
    plt.title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ---- Демонстрація ----
if __name__ == "__main__":
    N = 1_000_000 # кількість кидків
    counts = simulate_two_dice(N, seed=123)
    rows, rmse = build_table(counts, N)
    print_table(rows)
    print(f"\nRMSE (Monte Carlo vs аналітика): {rmse:.6f}")
    plot(rows, title=f"Two dice: Monte Carlo vs Analytic (N={N:,})")

# Висновки 
# • Розподіл Монте-Карло відтворює аналітичний: максимум на сумі 7 (~16.67%), симетричне спадання до 2 і 12 (~2.78%).
# • За великого N похибка мала; типовий масштаб зменшення похибки ~ 1/√N.
# • RMSE зростає/спадає відповідно до N; при N≈10^6 — зазвичай порядку 10^-4.
# Більш детально в файлі README.md
