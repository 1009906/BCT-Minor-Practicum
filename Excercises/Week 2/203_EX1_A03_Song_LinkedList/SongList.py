#!/usr/bin/env python3

# Leco Hendriks 0993233
# Bram Vermeer 1009906
"""Linked Lists -> Song List Implementation: Exercise 1

The goal of this exercise is to learn how to create a custom linked list for songs.
Each node in this linked list represent a song.
This data structure consists of a collection of songs(node) which together represent a playlist.  
The SongList class contains methods to insert a song, and traversal through the list to print titles. 

Your task is to:
    * locate the TODOs in this file
    * complete the missing part from the code 
    * run the test of this tutorial located in same folder.

To test run 'SongList_t.py' in your command line

Notes:
    * do not change class structure or method signature to not break unit tests
    * visit this url for more information on linked list:
    https://realpython.com/linked-lists-python/
"""
class SongNode:
    def __init__(self, song_title=None, next = None):
        self.song_title = song_title
        self.next = next

class SongList:
    def __init__(self):  
        self.head = None
    # TODO 1: Traverse through the list and print every song titles
    def printSongs(self):
        head = self.head
        if (head == None):
            return
        while (head):
            print(head.song_title)
            head = head.next 

    # TODO 2: Insert a new song title to the end of the list
    def AddNewSong(self, new_song_title):
        currentNode = self.head
        if (currentNode == None):
            self.head = SongNode(new_song_title)
            return
        if (currentNode.next == None):
            currentNode.next = SongNode(new_song_title)
            return
        while (currentNode.next != None):
            currentNode = currentNode.next
        currentNode.next = SongNode(new_song_title)
