"""
Student information for this assignment:

On my/our honor, Christiana Ozuna and Jessica North, this
programming assignment is my own work and I have not provided this code to
any other student.

I have read and understand the course syllabus's guidelines regarding Academic
Integrity. I understand that if I violate the Academic Integrity policy (e.g.
copy code from someone else, have the code generated by an LLM, or give my
code to someone else), the case shall be submitted to the Office of the Dean of
Students. Academic penalties up to and including an F in the course are likely.

UT EID 1: cmo2388
UT EID 2: jan3557
"""

# TODO: Delete this import if you choose not to use it. Delete this comment when you are done.
import sys


class Node:
    """
    Represents a node in a singly linked list.

    Instance Variables:
        data: The value or data stored in the node.
        next: The reference to the next node in the linked list (None by default).
    """

    def __init__(self, data, next=None):
        """
        Initializes a new node with the given data and a reference to the next node.

        Args:
            data: The data to store in the node.
            next: Optional; the next node in the linked list (None by default).
        """
        self.data = data
        self.next = next


class StackError(Exception):
    pass


class Stack:
    def __init__(self):
        self._top = None
        self._size = 0

    def peek(self):
        if self.is_empty():
            raise StackError("Peek from empty stack.")
        return self._top.data

    def push(self, item):
        new_node = Node(item)
        new_node.next = self._top
        self._top = new_node
        self._size += 1

    def pop(self):
        if self.is_empty():
            raise StackError("Pop from empty stack.")
        removed_data = self._top.data
        self._top = self._top.next
        self._size -= 1
        return removed_data

    def is_empty(self):
        return self._top is None

    def size(self):
        return self._size


class QueueError(Exception):
    pass


class Queue:
    """
    A class that implements a queue using a singly linked list with a tail.

    Instance Variables:
        _front: The beginning node of the queue.
        _rear: The end node of the queue.
        _size: The number of elements in the queue.
    """

    def __init__(self):
        """
        Initializes an empty queue with no elements.
        """
        self._front = None
        self._rear = None
        self._size = 0

    def peek(self):
        """
        Returns the value at the front of the queue without removing it.

        Raises:
            QueueError: If the queue is empty, raises "Peek from empty queue.".

        Returns:
            The data stored in the front node of the queue.
        """
        if self.is_empty():
            raise QueueError("Peek from empty queue.")
        return self._front.data

    def enqueue(self, item):
        """
        Enqueues a new item at the end of the queue.

        Args:
            item: The data to put at the end of queue.
        """
        new_node = Node(item)
        if self.is_empty():
            self._front = new_node
        else:
            self._rear.next = new_node
        self._rear = new_node
        self._size += 1

    def dequeue(self):
        """
        Removes and returns the item at the front of the queue.

        Raises:
            QueueError: If the queue is empty, raises "Dequeue from empty queue.".

        Returns:
            The data from the front node of the queue.
        """
        if self.is_empty():
            raise QueueError("Dequeue from empty queue.")
        front_data = self._front.data
        self._front = self._front.next
        if self._front is None:  # If queue becomes empty
            self._rear = None
        self._size -= 1
        return front_data

    def is_empty(self):
        """
        Checks if the queue is empty.

        Returns:
            True if the queue is empty, False otherwise.
        """
        return self._size == 0

    def size(self):
        """
        Returns the number of items in the queue.

        Returns:
            The size of the queue as an integer.
        """
        return self._size


class Vertex:
    """Vertex Class using properties and setters for better encapsulation."""

    def __init__(self, label):
        self.__label = label
        self.visited = False

    @property
    def visited(self):
        """Property to get the visited status of the vertex."""
        return self.__visited

    @visited.setter
    def visited(self, value):
        """Setter to set the visited status of the vertex."""
        if isinstance(value, bool):
            self.__visited = value
        else:
            raise ValueError("Visited status must be a boolean value.")

    @property
    def label(self):
        """Property to get the label of the vertex."""
        return self.__label

    def __str__(self):
        """String representation of the vertex"""
        return str(self.__label)


class Graph:
    """A Class to present Graph."""

    def __init__(self):
        self.vertices = []  # a list of vertex objects
        self.adjacency_matrix = []  # adjacency matrix of edges

    def has_vertex(self, label):
        """Check if a vertex is already in the graph"""
        num_vertices = len(self.vertices)
        for i in range(num_vertices):
            if label == self.vertices[i].label:
                return True
        return False

    def get_index(self, label):
        """Given a label get the index of a vertex"""
        num_vertices = len(self.vertices)
        for i in range(num_vertices):
            if label == self.vertices[i].label:
                return i
        return -1

    def add_vertex(self, label):
        """Add a Vertex with a given label to the graph"""
        if self.has_vertex(label):
            return

        # add vertex to the list of vertices
        self.vertices.append(Vertex(label))

        # add a new column in the adjacency matrix
        num_vertices = len(self.vertices)
        for i in range(num_vertices - 1):
            self.adjacency_matrix[i].append(0)

        # add a new row for the new vertex
        new_row = []
        for i in range(num_vertices):
            new_row.append(0)
        self.adjacency_matrix.append(new_row)

    def add_edge(self, start, finish):
        """Add unweighted directed edge to graph"""
        self.adjacency_matrix[start][finish] = 1

    def get_adjacent_vertices(self, vertex_index):
        """Return adjacent vertex indices to vertex_index"""
        vertices = []
        num_vertices = len(self.vertices)
        for j in range(num_vertices):
            if self.adjacency_matrix[vertex_index][j]:
                vertices.append(j)
        return vertices

    # WORKS
    def has_cycle(self):
        """
        Determine whether or not the graph has a cycle.
        
        post: returns True if there is a cycle and False otherwise.
        """
        # defining recursive function
        def dfs(vertex, visited, stack):
            # adding to visited
            visited[vertex] = True
            # add to stack
            stack[vertex] = True

            # check neighbors
            for adjacent in self.get_adjacent_vertices(vertex):
                # if not explored yet
                if not visited[adjacent]:
                    # add to stack and explore
                    if dfs(adjacent, visited, stack):
                        return True
                # if neighbor already exolored
                elif stack[adjacent]:
                    return True
                
            # remove vertex from stack
            stack[vertex] = False
            # know, no cycle
            return False

        num_vertices = len(self.vertices)
        visited = [False] * num_vertices
        stack = [False] * num_vertices

        # iterate
        for vertex in range(num_vertices):
            if not visited[vertex]:
                # recursive call
                if dfs(vertex, visited, stack):
                    return True

        return False

    # WORKS
    def get_registration_plan(self):
        """
        Return a valid ordering of courses to take for registration as a 2D
        list of vertex labels, where each inner list will be a maximum of 4.

        pre: a valid registration plan exists.
        post: returns a 2D list of strings, where each inner list represents a semester
        """

        # Because we don't want to destroy the original graph,
        # we have defined helper functions that work with a copy of the
        # adjacency matrix and vertices. This is also a hint that we
        # suggest you to manipulate the graph copy to solve this method.
        temp_vertices = list(self.vertices)
        temp_matrix = []
        for row in self.adjacency_matrix:
            temp_matrix.append(list(row))

        def get_index_from_copy(label, vertices_copy):
            """Given a label get the index of a vertex in the copy of the vertices list"""
            num_vertices = len(vertices_copy)
            for i in range(num_vertices):
                if label == vertices_copy[i].label:
                    return i
            return -1

        def delete_vertex_from_copy(vertex_label, adjacency_matrix_copy, vertices_copy):
            """delete vertex from the copy of the adjacency matrix and vertices list"""
            index = get_index_from_copy(vertex_label, vertices_copy)

            for row in adjacency_matrix_copy:
                row.pop(index)
            adjacency_matrix_copy.pop(index)
            vertices_copy.pop(index)

        courses = []

        while temp_vertices:
            semester_courses = []
        
            # finding vertices w no incoming edges
            for i, vertex in enumerate(temp_vertices):
                # no prereq
                if all(temp_matrix[j][i] == 0 for j in range(len(temp_vertices))):
                    semester_courses.append(vertex.label)

            # only 4 courses per sem
            semester_courses = semester_courses[:4]

            # add to plan
            courses.append(semester_courses)

            # Remove the courses from the graph (delete them from both adjacency matrix and vertices list)
            for course_label in semester_courses:
                delete_vertex_from_copy(course_label, temp_matrix, temp_vertices)

        return courses


# WORKS
def main():
    """
    The main function to retrieve a registration plan.
    The output code has been written for you.
    """

    # create a Graph object
    graph = Graph()

    # read the number of vertices
    num_vertices = int(input().strip())

    # read the vertices and add them into the graph
    for _ in range(num_vertices):
        course_label = input().strip()
        graph.add_vertex(course_label)

    # read the number of edges
    num_edges = int(input().strip())

    # read the edges and insert them into the graph
    # you will need to call the method to convert them from their labels to their index
    for _ in range(num_edges):
        prereq, course = input().strip().split()
        start_index = graph.get_index(prereq)
        finish_index = graph.get_index(course)
        graph.add_edge(start_index, finish_index)

    ####################################################################################
    # DO NOT CHANGE ANYTHING BELOW THIS
    if graph.has_cycle():
        print("Registration plan invalid because a cycle was detected.")
    else:
        print("Valid registration plan detected.")

        courses = graph.get_registration_plan()
        print()
        print("Registration plan: ")
        for semester in courses:
            print(semester)

if __name__ == "__main__":
    main()