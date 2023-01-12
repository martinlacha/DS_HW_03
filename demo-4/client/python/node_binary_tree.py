from mylog import log
from threading import Lock

class Node:
    def __init__(self, ip, parent_node):
        self._ip_address = ip
        self._left_node = None
        self._right_node = None
        self._parent_node = parent_node

    # Check if is free left or right child node
    def is_child_node_free(self):
        return self._left_node is None or self._right_node is None

    # Add new child node
    def add_new_child_node(self, child):
        if self._left_node is None:
            log.info(f"Adding node with ip {child._ip_address} as left child.")
            self._left_node = child
        elif self._right_node is None:
            log.info(f"Adding node with ip {child._ip_address} as right child.")
            self._right_node = child
        else:
            log.error(f'Error both children nodes are assigned!')
        

class Tree:
    # Construktor
    def __init__(self, root):
        self._root = root       # root node
        self._lock = Lock()     # lock

    # Method to add new node to the tree and return parent node
    def add_new_node(self, ip):
        self._lock.acquire()
        log.info(f'Adding new node with ip: {ip}')
        nodes_list = list()
        nodes_list.append(self._root)
        while len(nodes_list) > 0:
            current_node = nodes_list.pop()
            left_node = current_node._left_node
            right_node = current_node._right_node

            if left_node is not None:
                if left_node._ip_address == ip:
                    log.info(f'Already in tree as left child of node with ip: {left_node._ip_address}. Return parent node.')
                    self._lock.release()
                    return current_node
                log.info(f'Add node under left child node for node with IP: {current_node._ip_address}')
                nodes_list.insert(0, left_node)
            if right_node is not None:
                if right_node._ip_address == ip:
                    log.info(f'Already in tree as right child of node with ip: {right_node._ip_address}. Return parent node.')
                    self._lock.release()
                    return current_node
                log.info(f'Add node under right child node for node with IP: {current_node._ip_address}')
                nodes_list.insert(0, current_node._right_node)

            if current_node.is_child_node_free():
                log.info(f'Found free node')
                child = Node(ip, current_node)
                current_node.add_new_child_node(child)
                self._lock.release()
                return current_node
        self._lock.release()
        # Return None for root node
        return None