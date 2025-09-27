import uuid
import colorsys
from collections import deque
from typing import List, Optional, Literal

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # колір вузла (hex)
        self.id = str(uuid.uuid4())  # унікальний ідентифікатор


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree_once(tree_root, title: Optional[str] = None, block: bool = False):
    """Малює дерево з поточними кольорами вузлів (НЕ блокує цикл, якщо block=False)."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    if title:
        plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors)
    plt.show(block=block)


# ---------- Допоміжні утиліти для обходів і кольорів ----------

def iter_all_nodes_bfs(root: Node) -> List[Node]:
    """Повертає всі вузли дерева в порядку BFS (щоб мати стабільний перелік усіх вузлів)."""
    out, seen = [], set()
    q = deque([root])
    while q:
        n = q.popleft()
        if n is None or n.id in seen:
            continue
        seen.add(n.id)
        out.append(n)
        if n.left:
            q.append(n.left)
        if n.right:
            q.append(n.right)
    return out


def gradient_hex(n: int,
                 hue: float = 0.58,     # ~синій відтінок
                 sat: float = 0.75,
                 v_min: float = 0.25,   # темний старт
                 v_max: float = 0.95) -> List[str]:
    """
    Генерує n кольорів #RRGGBB від темного до світлого (стала H,S; змінюємо V).
    """
    if n <= 0:
        return []
    if n == 1:
        vals = [v_max]
    else:
        vals = [v_min + (v_max - v_min) * i / (n - 1) for i in range(n)]
    colors = []
    for v in vals:
        r, g, b = colorsys.hsv_to_rgb(hue, sat, v)
        colors.append('#{:02X}{:02X}{:02X}'.format(int(r * 255), int(g * 255), int(b * 255)))
    return colors


def reset_colors(root: Node, hex_color: str = "#D3D3D3"):
    """Фарбування всіх вузлів у базовий (невідвіданий) колір."""
    for n in iter_all_nodes_bfs(root):
        n.color = hex_color


# ---------- Візуалізація обходів (ітеративно, без рекурсії) ----------

def visualize_traversal(root: Node,
                        mode: Literal["bfs", "dfs"] = "bfs",
                        pause_sec: float = 0.8,
                        hue: float = 0.58):
    """
    Візуалізує кроки обходу:
      - BFS: черга (queue)
      - DFS: стек (stack)
    Кожен відвіданий вузол отримує унікальний hex-колір, що світлішає з кроком.
    """
    if root is None:
        raise ValueError("Порожнє дерево")

    # 1) Отримаємо порядок відвідувань (ітеративно)
    order: List[Node] = []
    visited = set()

    if mode == "bfs":
        q = deque([root])
        while q:
            u = q.popleft()
            if u is None or u.id in visited:
                continue
            visited.add(u.id)
            order.append(u)
            if u.left:
                q.append(u.left)
            if u.right:
                q.append(u.right)

    elif mode == "dfs":
        stack = [root]
        while stack:
            u = stack.pop()
            if u is None or u.id in visited:
                continue
            visited.add(u.id)
            order.append(u)
            # Щоб іти "зліва-направо", спочатку кладемо right, потім left
            if u.right:
                stack.append(u.right)
            if u.left:
                stack.append(u.left)
    else:
        raise ValueError("mode має бути 'bfs' або 'dfs'")

    # 2) Підготуємо градієнт для усіх кроків
    step_colors = gradient_hex(len(order), hue=hue, sat=0.80, v_min=0.25, v_max=0.95)

    # 3) Поетапне фарбування та малювання
    reset_colors(root, "#E0E0E0")  # невідвідані — світло-сірі
    plt.ion()
    for i, node in enumerate(order, start=1):
        node.color = step_colors[i - 1]
        title = f"{mode.upper()} крок {i}/{len(order)} — відвідуємо вузол: {node.val}"
        draw_tree_once(root, title=title, block=False)
        plt.pause(pause_sec)
        plt.close()  # закриваємо кадр, щоб не накопичувались вікна
    plt.ioff()
    draw_tree_once(root, title=f"{mode.upper()} завершено", block=True)


# --------------------------- Приклад ---------------------------

if __name__ == "__main__":
    # Побудова прикладового дерева (як у твоєму коді)
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    # BFS (черга): темний → світлий у порядку відвідування
    visualize_traversal(root, mode="bfs", pause_sec=0.7, hue=0.58)

    # DFS (стек): інший відтінок (напр., фіолет)
    visualize_traversal(root, mode="dfs", pause_sec=0.7, hue=0.76)
