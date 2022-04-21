import uuid
'''
Written by: Stuart Anderson
Copyright: Tobu Pengin, LLC, 2022
'''

class Node:
    def __init__(self, data):
        self.ID = str(uuid.uuid1())
        self.price = data['price']
        self.name = data['name']
        self.gender = data['gender']
        self.next = None

    def __repr__(self):
        return f'ID:{self.ID} | Name:{self.name}'

    def __call__(self):
        return {'id':self.ID, 'name':self.name, 'gender':self.gender, 'price':self.price}

class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next

    def __getitem__(self, index):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node())
            node = node.next
        return nodes[index]

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node)
            node = node.next
        return str(nodes)

    def __len__(self):
        return sum(1 for _ in self.__iter__())

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def search(self, val, **kw):
        def sub(rv):
            if len(rv) == 1:
                return rv[0]
            else:
                return rv
        if kw is None:
            print(val)
            return sub([i for i in self if i.ID == val or i.price == val or i.name == val])
        else:
            print(kw)
            print(val)
            return sub([i for i in self if kw.values() in i])



data = [{'name': 'Tom', 'gender': 'male', 'price': 33.99},
        {'name': 'Tasha', 'gender': 'female', 'price': 53.99},
        {'name': 'Bob', 'gender': 'male', 'price': 13.99},
        {'name': 'Sara', 'gender': 'female', 'price': 22.99}]
db = LinkedList(data)
