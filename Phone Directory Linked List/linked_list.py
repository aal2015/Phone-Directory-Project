class Node:
    def __init__(self, name, contact_number, address, email):
        self.prev = None
        self.next = None
        self.name = name
        self.contact_number = contact_number
        self.email = email
        self.address = address

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.name_list, self.address_list, self.contact_number_list = [], [], []

    def return_head(self):
        return self.head

    def insert(self, name, contact_number, address, email):
        # Checking if the list is empty
        if self.head == None:
            self.head = Node(name, contact_number, address, email)
            self.tail = self.head
        # If not, insert new contact details at the end of the doubly linked list
        else:
            new_node = Node(name, contact_number, address, email)
            self.tail.next = new_node
            self.tail = new_node

    def delete_node(self, name, address, contact_number, email):
        prev, current = self.search(name, address, contact_number, email)
        if prev is None:
            self.head = current.next
        else:
            prev.next = current.next
        del current

    def update(self, prev_name, prev_address, prev_contact_number, prev_email, name, address, contact_number, email):
        prev, current = self.search(prev_name, prev_address, prev_contact_number, prev_email)
        current.name = name
        current.address = address
        current.contact_number = contact_number
        current.email = email

    def search(self, name, address, contact_number, email):
        current = self.return_head()
        prev = None
        while current is not None:
            if name == current.name and address == current.address and contact_number == current.contact_number and email == current.email:
                break
            prev = current
            current = current.next

        return prev, current