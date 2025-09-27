from typing import Dict, List, Tuple

Items = Dict[str, Dict[str, int]]  # {"pizza": {"cost": 50, "calories": 300}, ...}

def greedy_algorithm(items: Items, budget: int) -> Tuple[List[str], int, int]:
    """
    Жадібний алгоритм: беремо страви у порядку спадання calories/cost,
    доки вміщаємося у бюджет. (Не гарантує оптимуму для 0/1 задачі.)
    Повертає: (список_страв, сумарні_калорії, сумарна_вартість)
    """
    if budget <= 0:
        return [], 0, 0

    scored = []
    for name, props in items.items():
        cst, cal = props["cost"], props["calories"]
        if cst <= budget:
            scored.append((name, cst, cal, cal / cst))
    # ratio ↓, при рівності — за більшою калорійністю
    scored.sort(key=lambda t: (t[3], t[2]), reverse=True)

    chosen, total_cost, total_cal = [], 0, 0
    for name, cst, cal, _ in scored:
        if total_cost + cst <= budget:
            chosen.append(name)
            total_cost += cst
            total_cal += cal
    return chosen, total_cal, total_cost


def dynamic_programming(items: Items, budget: int) -> Tuple[List[str], int, int]:
    """
    0/1-рюкзак (DP): знаходить оптимальний набір страв, що максимізує калорійність.
    Складність: O(N * B) пам'яті й часу, де N — кількість страв, B — бюджет.
    Повертає: (список_страв, сумарні_калорії, сумарна_вартість)
    """
    if budget <= 0:
        return [], 0, 0

    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    cals  = [items[n]["calories"] for n in names]
    n = len(names)

    # dp[i][b] = макс. калорії, використовуючи перші i предметів при бюджеті b
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        ci, vi = costs[i - 1], cals[i - 1]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]
            if ci <= b:
                cand = dp[i - 1][b - ci] + vi
                if cand > dp[i][b]:
                    dp[i][b] = cand

    # Відновлення вибору
    chosen: List[str] = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(names[i - 1])
            b -= costs[i - 1]
    chosen.reverse()
    total_cal = dp[n][budget]
    total_cost = sum(items[name]["cost"] for name in chosen)
    return chosen, total_cal, total_cost


items = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}

budget = 60
g_set, g_cal, g_cost = greedy_algorithm(items, budget)
d_set, d_cal, d_cost = dynamic_programming(items, budget)

print("Greedy:    ", g_set, g_cal, g_cost)   # напр., ['cola','potato','pepsi'] 670 50
print("DP optimal:", d_set, d_cal, d_cost)   # оптимально: ['cola','potato','pepsi'] 670 50

budget = 100
print(dynamic_programming(items, budget))     # оптимум: ['pizza','potato','cola','pepsi'] 970 100
print(greedy_algorithm(items, budget))        # жадібний дасть гірше: 870 80
