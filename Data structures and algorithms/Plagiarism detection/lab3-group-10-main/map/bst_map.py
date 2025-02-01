import sys
from typing import Generic

from .map import Map, Key, Value

# The standard recursion limit is 1000, but then we won't be able to even analyse
# the `small` directory, so we increase the limit to 5000:
sys.setrecursionlimit(5000)


class TreeNode(Generic[Key, Value]):
    """
    A generic class for BST nodes (and subclasses).
    We include the instance variables `size` and `height` for efficiency reasons
    (`height` is needed to calculate the balance in AVL trees).
    """
    key: Key
    value: Value
    left: 'TreeNode[Key, Value] | None'
    right: 'TreeNode[Key, Value] | None'
    size: int
    height: int

    # Setting the __slots__ reduces memory footprint and increases efficiency:
    # https://wiki.python.org/moin/UsingSlots
    __slots__ = "key", "value", "left", "right", "size", "height"

    def __init__(self, key: Key, value: Value):
        self.key = key
        self.value = value
        self.left = self.right = None
        self.size = self.height = 1


class BSTMap(Map[Key, Value]):
    """
    A simple map implemented as a Binary Search Tree.
    """
    root: TreeNode[Key, Value] | None = None


    def size(self) -> int:
        """Return the number of nodes in the tree."""
        return self._node_size(self.root)

    def _node_size(self, node: TreeNode[Key,Value]|None) -> int:
        """Return the number of nodes in the given subtree."""
        if node is None: return 0
        return node.size


    def height(self) -> int:
        """Return the height of the tree."""
        return self._node_height(self.root)

    def _node_height(self, node: TreeNode[Key,Value]|None) -> int:
        """Return the height of the given subtree."""
        if node is None: return 0
        return node.height


    def get(self, key: Key) -> Value | None:
        if key is None: # type: ignore
            raise ValueError("Key is None")
        return self._get_helper(self.root, key)

    def _get_helper(self, node: TreeNode[Key,Value]|None, key: Key) -> Value | None:
        #---------- TASK 3a: Implement BST get -------------------------------#
        # Note 1: you can implement this method using iteration or recursion.
        # Note 2: if the key does not exist, you should return None.

        """
        Key Properties of a BST:
        * Left Subtree: Contains nodes with keys less than the parent node's key.
        * Right Subtree: Contains nodes with keys greater than the parent node's key.
        * Binary Tree: Each node has at most two children (left and right).

        This function always gets the self.root as the node initially and the key to search for.
        """

        # Is essentially a while loop that traverses the tree until it finds the key
        while node is not None:
            if key < node.key: # If the key is less than the current node go left
                node = node.left
            elif key > node.key: # If the key is greater than the current node go right
                node = node.right 
            else: # If the key is equal the current node return the value
                return node.value
        return None # If the key is not found, return None

        #---------- END TASK 3a ----------------------------------------------#

    def put(self, key: Key, value: Value):
        if key is None: # type: ignore
            raise ValueError("Key is None")
        if value is None:
            raise ValueError("Value is None")
        self.root = self._put_helper(self.root, key, value)

    def _put_helper(self, node: TreeNode[Key,Value]|None, key: Key, value: Value) -> TreeNode[Key, Value]:
        #---------- TASK 3b: Implement BST put -------------------------------#
        # Note 1: you should implement this method using recursion.
        # Note 2: if the node is None you should return a new Node.
        # Note 3: you should call `_update_size_and_height` to update `node.size` and `node.height`.
        # Note 4: don't forget to implement `_update_size_and_height` too.

        if node is None:
            # If the current node is None, create and return a new node with the key and value
            return TreeNode(key, value)

        if key < node.key:
            # If the key is less than the current node's key, recursively insert in the left subtree
            node.left = self._put_helper(node.left, key, value)
        elif key > node.key:
            # If the key is greater than the current node's key, recursively insert in the right subtree
            node.right = self._put_helper(node.right, key, value)
        else:
            # If the key already exists, update its value
            node.value = value

        # Update the size and height of the current node after insertion
        self._update_size_and_height(node)
        return node

        #---------- END TASK 3b ----------------------------------------------#

    def _update_size_and_height(self, node: TreeNode[Key, Value]):
        """
        Make sure that `node.size` and `node.height` are correct.
        This assumes that the size and height for the children are already correct.
        """
        #---------- TASK 3c: Update size and height for a node ---------------#
        # Note: you can call `_node_size` and `_node_height`
        # to get the size and height of each of the children.

        # Size is the number of nodes in the subtree rooted at the current node
        node.size = 1 + self._node_size(node.left) + self._node_size(node.right)

        # Height is the length of the longest path from the current node to a leaf node
        node.height = 1 + max(self._node_height(node.left), self._node_height(node.right))

        #---------- END TASK 3c ----------------------------------------------#

    def clear(self):
        self.root = None

    def keys(self) -> tuple[Key, ...]:
        keylist: list[Key] = []
        self._collect_keys(self.root, keylist)
        return tuple(keylist)

    def _collect_keys(self, node: TreeNode[Key,Value]|None, keylist: list[Key]):
        if node is None: return
        self._collect_keys(node.left, keylist)
        keylist.append(node.key)
        self._collect_keys(node.right, keylist)


    def __str__(self) -> str:
        classname = type(self).__name__
        if self.size() == 0: return f"{classname}(empty)"
        return f"{classname}(size {self.size()}, height {self.height()})"

    def show(self, max_level: int) -> str:
        return f"{self}: {self._show_node(self.root, max_level)}"

    def _show_node(self, node: TreeNode[Key,Value]|None, max_level: int) -> str:
        if node is None: return "-"
        if max_level <= 0: return f"(...{node.size} nodes...)"
        left = self._show_node(node.left, max_level-1)
        right = self._show_node(node.right, max_level-1)
        return f"({left} {node.key}:{node.value} {right})"


    ###########################################################################
    # Validation

    def validate(self):
        self._validate_b_s_t(self.root, None, None)
        self._validate_size(self.root)
        self._validate_height(self.root)

    def _validate_b_s_t(self, node: TreeNode[Key,Value]|None, min: Key|None, max: Key|None):
        if node is None: return
        assert node.key is not None, "Key is None"
        assert node.value is not None, "Value is None"
        assert min is None or node.key > min, (
                    f"Node '{node.key}:{node.value}' not in BST order: "
                    f"rightmost left child ({min}) >= node ({node.key})")
        assert max is None or max > node.key, (
                    f"Node '{node.key}:{node.value}' not in BST order: "
                    f"node ({node.key}) >= leftmost right child ({max})")
        self._validate_b_s_t(node.left, min, node.key)
        self._validate_b_s_t(node.right, node.key, max)

    def _validate_size(self, node: TreeNode[Key,Value]|None):
        if node is None: return
        calculated = 1 + self._node_size(node.left) + self._node_size(node.right)
        assert node.size == calculated, (
                    f"Subtree size for node '{node.key}:{node.value}' not consistent: "
                    f"stored ({node.size}) != calculated ({calculated})")
        self._validate_size(node.left)
        self._validate_size(node.right)

    def _validate_height(self, node: TreeNode[Key,Value]|None):
        if node is None: return
        calculated = 1 + max(self._node_height(node.left), self._node_height(node.right))
        assert node.height == calculated, (
                    f"Subtree height for node '{node.key}:{node.value}' not consistent: "
                    f"stored ({node.height}) != calculated ({calculated})")
        self._validate_height(node.left)
        self._validate_height(node.right)


