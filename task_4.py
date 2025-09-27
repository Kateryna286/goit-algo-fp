import uuid

import networkx as nx
import matplotlib.pyplot as plt
from typing import Callable, Optional, List, Any
import heapq


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4()) # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val) # Використання id та збереження значення вузла
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root):
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)} # Використовуйте значення вузла для міток

    plt.figure(figsize=(8, 5))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()

def build_tree_from_heap(
    heap: List[Any],
    color_fn: Optional[Callable[[int, Any], str]] = None
) -> Optional[Node]:
    """
    Створює бінарне дерево з масиву-купи (0-індексація: діти i -> 2*i+1, 2*i+2).
    color_fn(i, value) — опціонально повертає колір вузла за індексом/значенням.
    """
    if not heap:
        return None

    nodes = [
        Node(val, color=(color_fn(i, val) if color_fn else "skyblue"))
        for i, val in enumerate(heap)
    ]

    for i, node in enumerate(nodes):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < len(nodes):
            node.left = nodes[li]
        if ri < len(nodes):
            node.right = nodes[ri]

    return nodes[0]


def draw_heap(
    heap: List[Any],
    color_fn: Optional[Callable[[int, Any], str]] = None
) -> None:
    """
    Візуалізує бінарну купу (масив) як дерево, використовуючи наявну draw_tree().
    """
    root = build_tree_from_heap(heap, color_fn=color_fn)
    if root is None:
        raise ValueError("Купа порожня — нічого малювати.")
    draw_tree(root)



# Створення дерева
root = Node(0)
root.left = Node(4)
root.left.left = Node(5)
root.left.right = Node(10)
root.right = Node(1)
root.right.left = Node(3)

# Відображення дерева
draw_tree(root)

# 1) Маємо довільний список — перетворимо на мін-купу й намалюємо.
arr = [4, 10, 5, 1, 3, 0]
heapq.heapify(arr)   # тепер arr — коректна мін-купа у вигляді масиву
draw_heap(arr)

# 2) (опціонально) Підсвітити корінь і, скажімо, останній елемент:
def my_colors(i, val):
    if i == 0:
        return "lightgreen"   # корінь
    if i == len(arr) - 1:
        return "salmon"       # останній індекс
    return "skyblue"

draw_heap(arr, color_fn=my_colors)



