#!/usr/bin/env python3

# Leco Hendriks 0993233
# Bram Vermeer 1009906
"""Linked List -> Extended Linked List Implementation: Homework

The goal of this homework is to implement a singly linked list data structure with additional functionalities. 
In previous tutorials you have learned how a node and a linked list data structure in its basic form can be created.
However, a LinkedList class can have more methods to perform additional operations on a linked list,
such as: insertion (begin, end, or after a specific element), deletion, traversal, and sorting.

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code 
    * run the test of this homework located in same folder.

To test run LinkedList_t.py in your command line'

Notes:
    * do not change class structure or method signature to not break unit tests
    * visit this url for more information on linked list:
    https://realpython.com/linked-lists-python/
"""

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    #TODO 1: Insert at the beginning of the list
    def insertBeg(self, new_data):
        if (self.head == None):
            self.head = Node(new_data)
            return

        head = self.head
        self.head = Node(new_data)
        self.head.next = head
    
    #TODO 2: Insert at the end
    def insertEnd(self, new_data):
        if (self.head == None):
            self.head = Node(new_data)
            return
        node = self.head
        while (node.next != None):
            node = node.next
        node.next = Node(new_data)



    #TODO 3: Insert after a specific node
    def insertAfter(self, data, new_data):
        node = self.head
        if(node == None):
            return
        while (node.data != data):
            node = node.next
        nextNode = node.next
        node.next = Node(new_data)
        node.next.next = nextNode
        

    #TODO 4: Deleting a node at a specific index
    def deleteIndex(self, index):
        node = self.head
        if (node == None):
            return
        x = 0
        while (x < index-1):
            node = node.next
            x += 1
        nodeToDelete = node.next
        node.next = nodeToDelete.next
        nodeToDelete = None

            

    #TODO 5: Search an element
    def find(self, key):
        node = self.head
        counter = 0
        if(node == None):
            return -1
        while (node.next != None):
            if(node.data == key):
                return counter
            node = node.next
            counter += 1
        return -1

    #TODO 6: Sort the linked list
    def sort(self, head):
        node = head
        index = None

        if(self.head == None):
            return
        else:
            while(node != None):
                #Node index will point to node next to node
                index = node.next

                while(index != None):
                    #If node node's data is greater than index's node data, swap the data between them
                    if(node.data > index.data):
                        temp = node.data
                        node.data = index.data
                        index.data = temp
                    index = index.next
                node = node.next

            

    #TODO 7: Print the linked list
    def printList(self):
        head = self.head
        if (head == None):
            return
        while (head):
            print(head.data)
            head = head.next 