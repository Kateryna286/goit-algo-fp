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
        current = self.head
        while current:
            print(current.data)
            current = current.next

llist = LinkedList()

"""
Для реалізації однозв'язного списку (приклад реалізації можна взяти з конспекту) необхідно:
- написати функцію, яка реалізує реверсування однозв'язного списку, змінюючи посилання між вузлами;
- розробити алгоритм сортування для однозв'язного списку, наприклад, сортування вставками або злиттям;
- написати функцію, що об'єднує два відсортовані однозв'язні списки в один відсортований список.
"""

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
    merged_list = LinkedList()
    dummy = Node()
    tail = dummy

    current1 = list1.head
    current2 = list2.head

    while current1 and current2:
        if current1.data <= current2.data:
            tail.next = Node(current1.data)
            current1 = current1.next
        else:
            tail.next = Node(current2.data)
            current2 = current2.next
        tail = tail.next

    while current1:
        tail.next = Node(current1.data)
        current1 = current1.next
        tail = tail.next

    while current2:
        tail.next = Node(current2.data)
        current2 = current2.next
        tail = tail.next

    merged_list.head = dummy.next
    return merged_list

def sort_linked_list(linked_list: LinkedList) -> LinkedList:
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
            if left.data < right.data:
                tail.next = left
                left = left.next
            else:
                tail.next = right
                right = right.next
            tail = tail.next
        if left:
            tail.next = left
        elif right:
            tail.next = right
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

# ===== Демонстрація =====
llist = LinkedList()
llist.insert_at_beginning(5)
llist.insert_at_beginning(10)
llist.insert_at_beginning(15)
llist.insert_at_end(20)
llist.insert_at_end(25)

print("Зв'язний список (llist):")
llist.print_list()

llist1 = LinkedList()
for x in (1, 3, 5, 7):
    llist1.insert_at_end(x)

llist2 = LinkedList()
for x in (2, 4, 6):
    llist2.insert_at_end(x)

print("\nЗв'язний список1:")
llist1.print_list()
print("Зв'язний список2:")
llist2.print_list()

merged_list = merge_sorted_linked_lists(llist1, llist2)
print("\nОб'єднаний відсортований список:")
merged_list.print_list()

reversed_list = reverse_linked_list(merged_list)
print("\nРеверсований список:")
reversed_list.print_list()

sorted_list = sort_linked_list(reversed_list)
print("\nВідсортований список (після реверсу):")
sorted_list.print_list()