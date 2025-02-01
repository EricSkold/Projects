
from .bst_map import TreeNode, BSTMap, Key, Value


class AVLMap(BSTMap[Key, Value]):
    """
    A simple map implemented as an AVL tree.
    This inherits most functionality from BST, the only difference is
    that it rebalances the tree when adding new tree nodes.
    """

    def _put_helper(self, node: TreeNode[Key,Value]|None, key: Key, value: Value) -> TreeNode[Key, Value]:
        # Call `_put_helper` for normal BSTs, to insert the value into the tree,
        # and update the node to be the new parent.
        node = super()._put_helper(node, key, value)

        # Calculate the node (im)balance.
        node_balance = self._node_height(node.left) - self._node_height(node.right)

        #---------- TASK 4a: Implement AVL rebalancing -------------------#
        # Perform balance rotations if needed.
        # You do this by calling `_left_rotate` and `_right_rotate`.
        # Remember to return the new parent node if you balance the tree.

        if node_balance > 1:
            if self._node_height(node.left.left) < self._node_height(node.left.right):
                node.left = self._left_rotate(node.left)
            node = self._right_rotate(node)
        elif node_balance < -1:
            if self._node_height(node.right.right) < self._node_height(node.right.left):
                node.right = self._right_rotate(node.right)
            node = self._left_rotate(node)
        return node
        #---------- END TASK 4a ------------------------------------------#



    def _right_rotate(self, node: TreeNode[Key,Value]) -> TreeNode[Key, Value]:
        # The left child will be the new parent.
        parent = node.left
        # This must exist, otherwise we cannot rotate right.
        assert parent, "There must be a left child"

        # Perform right rotation.
        #---------- TASK 4b: Implement right rotation --------------------#

        # Don't forget to update the size and height for all nodes that need it.
        # You do this by calling the method `_update_size_and_height`.
        # Note: if you're changing several nodes you have to update them bottom-up
        # (first the children, then the parents).

        # Return the new parent after rotation.

        node.left = parent.right
        parent.right = node

        self._update_size_and_height(node)
        self._update_size_and_height(parent)

        return parent
        #---------- END TASK 4b -------------------------------------------#


    def _left_rotate(self, node: TreeNode[Key,Value]) -> TreeNode[Key, Value]:
        #---------- TASK 4c: Implement left rotation ---------------------#
        # This is a mirror of `_right_rotate`.

        # The right child will be the new parent.
        parent = node.right
        # This must exist, otherwise we cannot rotate left.
        assert parent, "There must be a right child"

        node.right = parent.left
        parent.left = node

        self._update_size_and_height(node)
        self._update_size_and_height(parent)

        return parent
        #---------- END TASK 4c ------------------------------------------#


    ###########################################################################
    # Validation

    def validate(self):
        super().validate()
        self._validate_balance(self.root)

    def _validate_balance(self, node: TreeNode[Key,Value]|None):
        if node is None: return
        node_balance = self._node_height(node.left) - self._node_height(node.right)
        assert -1 <= node_balance <= 1, (
                    f"Node '{node.key}:{node.value}' not properly balanced: "
                    f"balance factor is {node_balance}, not -1, 0 or 1")
        self._validate_balance(node.left)
        self._validate_balance(node.right)


