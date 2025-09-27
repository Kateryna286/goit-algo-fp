from typing import Dict, Hashable, List, Tuple, Optional
import heapq

Graph = Dict[Hashable, List[Tuple[Hashable, float]]]

def build_graph_from_edges(
    edges: List[Tuple[Hashable, Hashable, float]],
    directed: bool = True
) -> Graph:
    """Формує список суміжності з переліку ребер (u, v, w)."""
    g: Graph = {}
    for u, v, w in edges:
        g.setdefault(u, []).append((v, w))
        if not directed:
            g.setdefault(v, []).append((u, w))
        else:
            g.setdefault(v, [])  # щоб мати вузол навіть без вих. ребер
    return g

def dijkstra_heap(graph: Graph, source: Hashable) -> Tuple[Dict[Hashable, float], Dict[Hashable, Optional[Hashable]]]:
    """
    Алгоритм Дейкстри з використанням бінарної купи (heapq).
    Повертає:
      dist[v] — мінімальна відстань від source до v,
      parent[v] — попередник v у найкоротшому шляху (для відновлення маршруту).
    """
    INF = float("inf")
    dist: Dict[Hashable, float] = {v: INF for v in graph}
    parent: Dict[Hashable, Optional[Hashable]] = {v: None for v in graph}
    dist[source] = 0.0

    # Куча з кортежів (поточна_відстань, вузол)
    heap: List[Tuple[float, Hashable]] = [(0.0, source)]

    while heap:
        d_u, u = heapq.heappop(heap)
        # Пропускаємо застарілий запис (класичний прийом без decrease-key)
        if d_u != dist[u]:
            continue

        for v, w in graph[u]:
            alt = d_u + w
            if alt < dist[v]:
                dist[v] = alt
                parent[v] = u
                heapq.heappush(heap, (alt, v))

    return dist, parent

def reconstruct_path(parent: Dict[Hashable, Optional[Hashable]], target: Hashable) -> List[Hashable]:
    """Відновлює найкоротший шлях до target із parent-таблиці."""
    path: List[Hashable] = []
    cur: Optional[Hashable] = target
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()
    return path

# Демонстрація
# Ребра графа (u, v, вага). За замовчуванням — орієнтований граф.
edges = [
    ("A", "B", 4),
    ("A", "C", 2),
    ("C", "B", 1),
    ("B", "D", 5),
    ("C", "D", 8),
    ("C", "E", 10),
    ("E", "D", 2),
]

g = build_graph_from_edges(edges, directed=True)
dist, parent = dijkstra_heap(g, source="A")

print("Відстані від A:", dist)              # мінімальні вартості до кожної вершини
print("Шлях A→D:", reconstruct_path(parent, "D"))  # наприклад, найкоротший шлях до D



