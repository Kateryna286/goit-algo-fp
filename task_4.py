import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from typing import Callable, Optional, List, Any

class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())

def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if not node:
        return graph

    graph.add_node(node.id, color=node.color, label=node.val)

    if node.left:
        lx = x - 1 / 2**layer
        graph.add_edge(node.id, node.left.id)
        pos[node.left.id] = (lx, y - 1)
        add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)

    if node.right:
        rx = x + 1 / 2**layer
        graph.add_edge(node.id, node.right.id)
        pos[node.right.id] = (rx, y - 1)
        add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)

    return graph

def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    add_edges(tree, tree_root, pos)

    colors = [data["color"] for _, data in tree.nodes(data=True)]
    labels = {n: data["label"] for n, data in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.tight_layout()
    plt.show()

def build_tree_from_heap(heap: List[Any], color_fn: Optional[Callable[[int, Any], str]] = None) -> Optional[Node]:
    if not heap:
        return None
    nodes = [Node(val, color=(color_fn(i, val) if color_fn else "skyblue")) for i, val in enumerate(heap)]
    for i, node in enumerate(nodes):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < len(nodes):
            node.left = nodes[li]
        if ri < len(nodes):
            node.right = nodes[ri]
    return nodes[0]

def draw_heap(heap: List[Any], color_fn: Optional[Callable[[int, Any], str]] = None) -> None:
    root = build_tree_from_heap(heap, color_fn=color_fn)
    if root is None:
        raise ValueError("Купа порожня")
    draw_tree(root)

# ---- Демонстрація ----
if __name__ == "__main__":
    # Візуалізація бінарного дерева
    root = Node(0)
    root.left = Node(4)
    root.left.left = Node(5)
    root.left.right = Node(10)
    root.right = Node(1)
    root.right.left = Node(3)
    draw_tree(root)

    # Візуалізація купи
    arr = [4, 10, 5, 1, 3, 0]
    heapq.heapify(arr)  # мін-купа
    draw_heap(arr)

    # Підсвічування кореня й останнього індексу
    def my_colors(i, val):
        if i == 0:
            return "violet"
        if i == len(arr) - 1:
            return "tomato"
        return "skyblue"
    draw_heap(arr, color_fn=my_colors)
