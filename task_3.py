import heapq
import networkx as nx
import matplotlib.pyplot as plt

# -------- Дейкстра на бінарній купі --------
def dijkstra(G, start):
    dist = {v: float("inf") for v in G}
    prev = {v: None for v in G}
    dist[start] = 0.0
    pq = [(0.0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:
            continue
        for v, data in G[u].items():
            w = data.get("weight", 1.0)
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    return dist, prev

def get_path(prev, s, t):
    path = []
    cur = t
    while cur is not None:
        path.append(cur)
        if cur == s:
            break
        cur = prev[cur]
    path.reverse()
    return path if path and path[0] == s else []

# -------- Візуалізація --------
def draw_graph_with_tree(G, dist, prev, start):
    pos = nx.spring_layout(G, seed=42, k=1.1)

    # базовий граф
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color="#E8F0FE")
    nx.draw_networkx_edges(G, pos, width=2, edge_color="#C0C0C0")

    # ребра дерева НКШ (prev[v] -> v), підсвічуються товстіше
    tree_edges = [(p, v) for v, p in prev.items() if p is not None]
    nx.draw_networkx_edges(G, pos, edgelist=tree_edges, width=3, edge_color="#1296F0")

    # ваги ребер
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels=edge_labels, label_pos=0.58, font_size=11,
        bbox=dict(boxstyle="round,pad=0.22", fc="white", ec="none", alpha=0.9)
    )

    # підписи вузлів: ім'я + відстань
    labels = {v: f"{v}\n{dist[v] if dist[v] != float('inf') else '∞'}" for v in G.nodes}
    nx.draw_networkx_labels(
        G, pos, labels=labels, font_size=10,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.7)
    )

    plt.title(f"Дерево найкоротших шляхів від {start}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()

# -------- Демонстрація --------
def main():
    # Неорієнтований граф з вагами ребер
    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("C", "B", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("E", "D", 2),
        ("B", "E", 7),
        ("D", "F", 1),
        ("E", "F", 3),
    ]
    G = nx.Graph()
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    start = "A"
    dist, prev = dijkstra(G, start)

    target = "F"
    print("Відстані від", start, ":", dist)
    print(f"Шлях {start}→{target}:", get_path(prev, start, target))

    draw_graph_with_tree(G, dist, prev, start)

if __name__ == "__main__":
    main()
