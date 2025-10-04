import uuid
from collections import deque

import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)  # Використання id та збереження значення вузла
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


def draw_tree_once(tree_root, title=None, block=False):
    """Малює дерево з поточними кольорами вузлів"""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)} 

    plt.figure(figsize=(8, 5))
    if title:
        plt.title(title)
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.tight_layout()
    plt.show(block=block)


def iter_all_nodes_bfs(root):
    """Повертає всі вузли дерева в порядку BFS (щоб мати стабільний перелік та лічити кроки)."""
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


def gradient_from_base_hex(n, base_hex="#1296F0", dark=0.35, light=1.0):
    """
    Генерує n кольорів у форматі #RRGGBB від темнішого до світлішого відтінку базового кольору.
    Просте масштабування компонент RGB (без зовн. бібліотек).
    """
    base_hex = base_hex.lstrip("#")
    r0 = int(base_hex[0:2], 16)
    g0 = int(base_hex[2:4], 16)
    b0 = int(base_hex[4:6], 16)
    if n <= 0:
        return []
    if n == 1:
        factors = [light]
    else:
        factors = [dark + (light - dark) * i / (n - 1) for i in range(n)]
    colors = []
    for f in factors:
        r = max(0, min(255, int(r0 * f)))
        g = max(0, min(255, int(g0 * f)))
        b = max(0, min(255, int(b0 * f)))
        colors.append(f"#{r:02X}{g:02X}{b:02X}")
    return colors


def reset_colors(root, hex_color="#E0E0E0"):
    for n in iter_all_nodes_bfs(root):
        n.color = hex_color


# ---------- Ітеративні обходи з візуалізацією ----------

def visualize_bfs(root, pause_sec=0.8):
    if root is None:
        return
    order = []
    visited = set()
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

    # кольори: темний -> світлий
    step_colors = gradient_from_base_hex(len(order), base_hex="#1296F0", dark=0.35, light=1.0)

    reset_colors(root, "#E0E0E0")
    plt.ion()
    for i, node in enumerate(order, start=1):
        node.color = step_colors[i - 1]
        title = f"BFS крок {i}/{len(order)} — {node.val}"
        draw_tree_once(root, title=title, block=False)
        plt.pause(pause_sec)
        plt.close()
    plt.ioff()
    draw_tree_once(root, title="BFS завершено", block=True)


def visualize_dfs(root, pause_sec=0.8):
    if root is None:
        return
    order = []
    visited = set()
    stack = [root]

    while stack:
        u = stack.pop()
        if u is None or u.id in visited:
            continue
        visited.add(u.id)
        order.append(u)
        if u.right:
            stack.append(u.right)
        if u.left:
            stack.append(u.left)

    step_colors = gradient_from_base_hex(len(order), base_hex="#BF47DA", dark=0.35, light=1.0)  # інший колір

    reset_colors(root, "#E0E0E0")
    plt.ion()
    for i, node in enumerate(order, start=1):
        node.color = step_colors[i - 1]
        title = f"DFS крок {i}/{len(order)} — {node.val}"
        draw_tree_once(root, title=title, block=False)
        plt.pause(pause_sec)
        plt.close()
    plt.ioff()
    draw_tree_once(root, title="DFS завершено", block=True)


# --------------------------- Приклад ---------------------------

if __name__ == "__main__":
    # Створення дерева
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)

    # Відображення початкового дерева
    draw_tree_once(root, title="Початкове дерево", block=True)

    # BFS (черга): від темного до світлого синього
    visualize_bfs(root, pause_sec=0.7)

    # DFS (стек): від темного до світлого рожевого
    visualize_dfs(root, pause_sec=0.7)
