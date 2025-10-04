# ---------- Дані ----------
items = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}

# ---------- Жадібний алгоритм ----------
def greedy_algorithm(items, budget):
    """
    Беремо страви у порядку спадання (calories / cost),
    доки не вичерпаємо бюджет.
    Повертає: (total_calories, spent_cost, chosen_items)
    """
    if budget <= 0:
        return 0, 0, []

    scored = []
    for name, p in items.items():
        cost, cal = p["cost"], p["calories"]
        if cost <= budget:
            scored.append((name, cost, cal, cal / cost))
    scored.sort(key=lambda t: (t[3], t[2]), reverse=True)

    total_cal, spent, chosen = 0, 0, []
    for name, cost, cal, _ in scored:
        if spent + cost <= budget:
            chosen.append(name)
            spent += cost
            total_cal += cal
    return total_cal, spent, chosen

# ---------- Динамічне програмування (0/1-рюкзак) ----------
def dynamic_programming(items, budget):
    """
    Максимізує калорії при обмеженні за вартістю.
    Повертає: (total_calories, spent_cost, chosen_items)
    """
    if budget <= 0:
        return 0, 0, []

    names  = list(items.keys())
    costs  = [items[n]["cost"]     for n in names]
    cals   = [items[n]["calories"] for n in names]
    n = len(names)

    # Таблиця dp[i][b] = макс. калорійність, яку можна отримати,
    # використовуючи перші i страв і бюджет b
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        ci, vi = costs[i - 1], cals[i - 1]
        for b in range(budget + 1):
            dp[i][b] = dp[i - 1][b]           
            if ci <= b:                       
                cand = dp[i - 1][b - ci] + vi
                if cand > dp[i][b]:
                    dp[i][b] = cand

    # Відновлення набору
    chosen = []
    b = budget
    for i in range(n, 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            chosen.append(names[i - 1])
            b -= costs[i - 1]
    chosen.reverse()

    total_cal = dp[n][budget]
    spent = sum(items[name]["cost"] for name in chosen)
    return total_cal, spent, chosen

def print_solution(label, result):
    total_cal, total_cost, chosen = result
    print(f"{label}: Набір = {chosen}; Калорійність = {total_cal}; Витрати = {total_cost}")

# ---- Демонстрація ----
if __name__ == "__main__":
    budget = 60
    g_res = greedy_algorithm(items, budget)
    d_res = dynamic_programming(items, budget)

    print(f"\nБюджет = {budget}")
    print_solution("Greedy", g_res)
    print_solution("DP optimal", d_res)

    budget = 100
    print(f"\nБюджет = {budget}")
    print_solution("Greedy", greedy_algorithm(items, budget))
    print_solution("DP optimal", dynamic_programming(items, budget))
