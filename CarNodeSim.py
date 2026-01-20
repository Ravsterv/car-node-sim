# this will bea program that simulates a car traveling through a city.
import math
import random

# Will be changed later just here to hold for now
MAX_TURN_LARGE = 100
MAX_TURN_MEDIUM = 50
MAX_TURN_SMALL = 10
class Node:
    """


    self._neighbor_nodes = [NodeID, Weight]

    """
    def __init__(self, nodeid, x, y, neighbor_nodes):
        self._id = nodeid
        self._x = x
        self._y = y
        self._neighbors = neighbor_nodes  # Nodes that it can go towards
        self._weights = []

    def get_neighbors(self):
        return self._neighbors

    def get_weights(self):
        return self._weights

    def get_x_y(self):
        return self._x, self._y

    def get_x(self):
        return self._x


    def generate_weights(self, OtherNodes):
        """
        Other

        :param OtherNodes: List of all nodes in the map, passed by NodeMap
        :return:
        """
        for neighbor in self._neighbors:
            for node in OtherNodes:
                if neighbor == node:
                    x, y = node.get_x_y()
                    c = round(math.sqrt(math.pow((x - self._x), 2) + math.pow((y - self._y), 2)),1)
                    self._weights.append(c)
                    break

    def get_id(self):
        return self._id

    def __eq__(self, other):
        if other is Node:
            return self._id == other.get_id()
        else:
            return self._id == other

    def __str__(self):
        return f"ID: {self._id}, x:{self._x}, y:{self._y}, Neighbors:{self._neighbors}, Weights:{self._weights}"


class NodeMap:
    """
    NodeMap holds all the nodes and their connected neighbors allowing for easy access
    NodeMap will also contain the Dijkisrtrov algorithm allowing for it to easily access its own values
    It will be given a
    """

    def __init__(self):
        self._nodes = []

    def generate_node_weights(self):
        for node in self._nodes:
            node.generate_weights(self._nodes)

    def add_nodes(self, node_list):
        self._nodes = node_list

    def __str__(self):
        nodes = "NodeMap:\n"
        for node in self._nodes:
            nodes += str(node) + "\n"
        return nodes

    def find_node(self, targetNodeId):
        for node in self._nodes:
            if node == targetNodeId:
                return node

    def find_shortest_path(self, start, target):
        """


        :param start: The current Node the car is on
        :param target: The target node the car wants to travel to
        :return: Path of nodes to target node
        """
        #TODO Implement shortest path algo here

        # Will need a seperate array showing the weighting to the node
        # Use of dictionary might be useful
        # Will have to think how this will work
        # Will need array of already visited nodes
        # The checker ignores any visited Nodes

        # Steps
        # 1. Create temporary dictionary holding NodeID as key and the components being
        # Weighting: Weighting of current from source to now
        # Parent Node: Tracks the current Parent Node
        # 2. Start at starting node and all other nodes connected to starting are added to the toVisit list (weight, node)
        # 3. Sort the list in order of weight and then pop the first node out from it and use that node
        # 4. From this node, determine weights of connected nodes and repeat again

        # End condition: No more nodes exist in the toVisit list or Target node is identified
        # End Step: Start from beginning node and then progress following the trail of parents till it reaches
        # the target node after calculations
        # Save these nodes traveled to a list and pass that  to the car as the path

        toVisit = [[0, start.get_id()]]
        visited = []

        weight_parents = {}

        for node in self._nodes:
            weight_parents[node.get_id()] = [None, None] # Weight to node from start, parent Node

        while len(toVisit) != 0:
            # Do loop
            current_node = toVisit.pop(0)
            if current_node[1] == target:
                break

            neighbors = self.find_node(current_node[1]).get_neighbors()
            weights = self.find_node(current_node[1]).get_weights()

            for index, neighbor in enumerate(neighbors):
                # Skip neighbor if its already been visited
                if neighbor in visited:
                    continue

                # Set weight and parent node to current node if no previous
                # Will make duplicates if target node seen by another node in the toVisit list
                if weight_parents[neighbor][0] is None:
                    weight_parents[neighbor][0] = current_node[0] + weights[index]
                    weight_parents[neighbor][1] = current_node[1]
                    toVisit.append([weight_parents[neighbor][0], current_node[1]])

                else:
                    # Need to stop duplication of nodes
                    if current_node[0] + weights[index] < weight_parents[neighbor][0]:
                        toVisitIndex = toVisit.index([weight_parents[neighbor][0], neighbor])
                        weight_parents[neighbor][0] = current_node[0] + weights[index]
                        weight_parents[neighbor][1] = current_node[1]

                        toVisit[toVisitIndex] = [weight_parents[neighbor][0], current_node[1]]

            visited.append(current_node[1])
            toVisit = sorted(toVisit)

        # Now to process the parent tree saved in weights_parent

        path = [target.get_id()]
        selected_node = target.get_id()

        while selected_node != start:
            parent_node = weight_parents[selected_node][1]

            selected_node = parent_node

            path.append(parent_node)

        print(path)










    def select_random_node(self, current_node):
        chosen_node = random.choice(self._nodes)
        while chosen_node == current_node:
            chosen_node = random.choice(self._nodes)

        return chosen_node

class Initializer:

    """
    File will be
    N - NumberOfNodes
    D - Node description
    Formatted
    NodeID, x, y, Node1|Node2|Node3 (Neighbor Nodes equal to ID of other Nodes)

    """
    def __init__(self, file_path):
        self._file = file_path


    def create_nodelist(self, Map):
        """
        Will read a text file and save info to each Node and also save all nodes to the node map.
        :param Map:
        :return: Nothing actually
        """
        nodes = []
        with open(self._file, "r") as file:
            for line in file:
                new_line = line.strip()
                if new_line[0] == "D":
                    NodeId, x, y, neighbors = new_line[1:].split(",")
                    split_neighbors = neighbors.split("|")
                    new_node = Node(NodeId, int(x), int(y), split_neighbors)
                    nodes.append(new_node)

        Map.add_nodes(nodes)


class Car:
    """
    Car will be the class that defines the agent that follows a path given to it by the NodeMap


    """
    def __init__(self, x, y):
        self._current_node = ""
        self._target = ""
        self._x = x
        self._y = y
        self._heading = 0
        self._path = []
        self._acceleration = 1
        self._max_speed = 4

    # TODO Implement step to allow car to accelerate, turn towards current target node and tick nodes off its path


class Simulation:
    """
    Simulation will be the main process coordinating the steps of Car and also all the cars that will exist
    A car will have been past it chosen node if it passess in a small rectangle around the node as a sort of checkpoint
    """
    def __init__(self, nodeMap, cars):
        self._nodeMap = nodeMap
        self._cars = cars

    # TODO implement simulation ticks here and how car operates


if __name__ == "__main__":
    citymap = NodeMap()

    city_maker = Initializer("nodemaps/map1")

    city_maker.create_nodelist(citymap)

    citymap.generate_node_weights()

    print(citymap)


