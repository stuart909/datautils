'''
Written by Stuart Anderson
Copyright 2022
linked list test program that merges two json payloads into one data structure according to customer spec
currently untested with large dataset
'''

import json


class Customer:
    def __init__(self,ID,name,index):
        self.ID = ID
        self.name = name
        self.index = index
        self.order = []

    def __repr__(self):
        return f'Customer Class | ID:{self.ID} | Name:{self.name}'

    def __call__(self):
        if self.order == []:
            return {"user_id": self.ID, "name": self.name, "event": {"type": "customer"}}
        else:
            return {"user_id": self.ID, "name": self.name, "event": {"type": "customer"}, "order":self.order}


class Order:
    def __init__(self,ID,order_ID,index):
        self.ID = ID
        self.order_ID = order_ID
        self.index = index

    def __repr__(self):
        return f'Order Class | ID:{self.ID} | order ID:{self.order_ID}'

    def __call__(self):
        return {"user_id": self.ID, "order_id": self.order_ID, "event": {"type": "order"}}


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __name__(self):
        return f'Node Class | node - self.data | child - self.next'
    
    def __repr__(self):
        return self.data

    def __call__(self):
        return self.data()


class LinkedList:
    def __init__(self, nodes=None):
        self.head = None
        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node
            for elem in nodes:
                node.next = Node(data=elem)
                node = node.next

    def append(self, obj):
        elem = Node(obj)
        if self.head == None:
            self.head = elem
        else:
            node = self.head
            while node.next != None:
                node = node.next
            node.next = elem

    def __getitem__(self, index):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node.data.index)
            node = node.next
        return nodes[index]

    def __repr__(self):
        node = self.head
        nodes = []
        while node is not None:
            nodes.append(node())
            node = node.next
        return str(nodes)

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
            

class DataConnector:
    def __init__(self,path):
        self.path = path
        self.data = LinkedList()
        self.get_data()
        
   
    def get_data(self):
        def order(i,j):
            msg = json.loads(j)
            if msg['event']['type'] == 'customer':
                customer = Customer(msg['user_id'],msg['name'],i)
                if self.data.head != None and customer in self.data:
                    self.data[self.data.index(customer)].index = i
                else:
                    self.data.append(customer)
                    
            elif msg['event']['type'] == 'order':
                u_id = msg['user_id']
                o_id = msg['order_id']
                customers,indexes = zip(*[[i.data,i.data.index] for i in self.data if u_id == i.data.ID])
                if len(customers) > 1:
                    customers[indexes.index(max(indexes))].order.append(Order(u_id,o_id,i))
                else:
                    customers[0].order.append(Order(u_id,o_id,i))
            else:
                self.data.append(i)

        return [order(i,j) for i,j in enumerate(open('bw_events.json'))]

    def __repr__(self):
        return f'path:{self.path} | len:{len(self.data)}'

    def __call__(self):
        return [i() for i in self.data]

if __name__ == "__main__":
    conn = DataConnector('bw_events.json')
    data = conn.data
    
