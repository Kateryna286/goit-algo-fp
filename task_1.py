class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data: int) -> Node | None:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        parts = []
        current = self.head
        while current:
            parts.append(str(current.data))
            current = current.next
        print(" --> ".join(parts))

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next

    def to_list(self):
        return list(self)

    def reverse(self):
        reverse_linked_list(self)
        return self

    def sort(self):
        sort_linked_list(self)
        return self

    @staticmethod
    def merge_two(l1: "LinkedList", l2: "LinkedList") -> "LinkedList":
        return merge_sorted_linked_lists(l1, l2)


def reverse_linked_list(linked_list: LinkedList) -> LinkedList:
    prev = None
    current = linked_list.head
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
    linked_list.head = prev
    return linked_list


def merge_sorted_linked_lists(list1: LinkedList, list2: LinkedList) -> LinkedList:
    """Стабільне ін-плейс злиття двох відсортованих списків без копіювання вузлів."""
    a, b = list1.head, list2.head
    dummy = Node()
    tail = dummy
    while a and b:
        if a.data <= b.data:        # стабільність: рівні беремо з list1
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a or b

    merged = LinkedList()
    merged.head = dummy.next
    return merged


def sort_linked_list(linked_list: LinkedList) -> LinkedList:
    """Стабільний merge sort для однозв'язного списку (O(n log n), стек O(log n))."""
    if linked_list.head is None or linked_list.head.next is None:
        return linked_list

    def split(head: Node) -> Node:
        slow = head
        fast = head.next
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        middle = slow.next
        slow.next = None
        return middle

    def merge(left: Node, right: Node) -> Node:
        dummy = Node()
        tail = dummy
        while left and right:
            if left.data <= right.data:  
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next
            tail = tail.next
        tail.next = left or right       
        return dummy.next

    def merge_sort(head: Node) -> Node:
        if head is None or head.next is None:
            return head
        middle = split(head)
        left = merge_sort(head)
        right = merge_sort(middle)
        return merge(left, right)

    linked_list.head = merge_sort(linked_list.head)
    return linked_list


def main():
    # 1) Створюємо однозв'язний список l1
    l1 = LinkedList()
    for x in [10, 5, 25, 20, 15]:
        l1.insert_at_end(x)
    print("1) Створено список l1:")
    l1.print_list()

    # 2) Реверсуємо l1
    reverse_linked_list(l1)
    print("\n2) Реверсований l1:")
    l1.print_list()
    assert l1.to_list() == [15, 20, 25, 5, 10]

    # 3) Сортуємо l1
    sort_linked_list(l1)
    print("\n3) Відсортований l1:")
    l1.print_list()
    assert l1.to_list() == [5, 10, 15, 20, 25]

    # 4) Створюємо ще один список l2
    l2 = LinkedList()
    for x in [30, 40, 35]:
        l2.insert_at_end(x)
    print("\n4) Створено список l2:")
    l2.print_list()

    # 5) Сортуємо l2
    sort_linked_list(l2)
    print("\n5) Відсортований l2:")
    l2.print_list()
    assert l2.to_list() == [30, 35, 40]

    # 6) Зливаємо списки з пп.3 та пп.5
    merged = merge_sorted_linked_lists(l1, l2)
    print("\n6) Злитий відсортований список (l1 + l2):")
    merged.print_list()
    assert merged.to_list() == [5, 10, 15, 20, 25, 30, 35, 40]

    print("\n Усі перевірки пройдено.")


if __name__ == "__main__":
    main()
