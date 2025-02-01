#!/usr/bin/env python3

# A file for testing your implementations.
# Change this code however you want.
#
# Pro-tip: write proper unit tests, e.g. by using the unittest library:
# https://docs.python.org/3/library/unittest.html


def test():
    test_map()


###############################################################################
## Test map data structures.

def test_map():
    ## Select which map you want to test by (un)commenting these lines:
    from map.bst_map import BSTMap as Map
    # from map.avl_map import AVLMap as Map

    print("# A very simple", Map.__name__)
    insertion_order = [
        (2, "dog"),
        (3, "barked"),
        (5, "the"),
        (6, "mat"),
        (7, "on"),
        (2, "cat"),
        (1, "the"),
        (3, "sat"),
    ]
    tree: Map[int, str] = Map()
    gold: dict[int, str] = {}
    for k, word in insertion_order:
        tree.put(k, word); tree.validate()
        gold[k] = word
    for k in range(0, 8):
        assert tree.get(k) == gold.get(k), f"tree.get({k}) returns {tree.get(k)}, but should return {gold.get(k)}"
    print(tree.show(5))
    print()

    """
    # Wait with this until you're pretty certain that your code works.
    print(f"# A larger {Map.__name__}, testing performance.")
    tree3: Map[int, int] = Map()
    numbers = list(range(0, 2000))

    # Comment this to get an unbalanced tree:
    import random
    random.shuffle(numbers)

    for k in numbers:
        tree3.put(k, k*k)  # Map a number to its square
    tree3.validate()
    print(tree3.show(2))
    for k in numbers:
        assert k*k == tree3.get(k)
    print()
    """


if __name__ == "__main__":
    test()

