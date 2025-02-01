
import sys
import math

from .edge import Edge
from .graph import Graph


# Python does not have a separate type of characters.
# So the below types are both just aliases for strings.
Word = str
Char = str

class WordLadder(Graph[Word]):
    """
    A graph that encodes word ladders.

    The class does not store the full graph in memory, just a dictionary of words.
    The edges are then computed on demand.
    """
    dictionary: set[Word]
    alphabet: set[Char]

    def __init__(self, graph: str|None = None):
        self.dictionary = set()
        self.alphabet = set()
        if graph:
            self.init(graph)

    def init(self, graph: str):
        """
        Creates a new word ladder graph from the given dictionary file.
        The file should contain one word per line, except lines starting with "#".
        """
        with open(graph, encoding="utf-8") as IN:
            for line in IN:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.add_word(line)

    def add_word(self, word: Word):
        """
        Adds a word to the dictionary if it only contains letters.
        The word is converted to lowercase.
        """
        if word.isalpha():
            word = word.lower()
            self.dictionary.add(word)
            self.alphabet.update(word)

    def nodes(self) -> frozenset[Word]:
        return frozenset(self.dictionary)

    def outgoing_edges(self, v: Word) -> list[Edge[Word]]:
        """
        Returns a list of the graph edges that originate from `word`.
        """
        #---------- TASK 2: Outgoing edges, Wordladder -----------------------#
        edges = []
        word_length = len(v)

        for i in range(word_length):
            for char in self.alphabet:
                # No substitution => skip
                if char == v[i]:
                    continue
                
                # Create a new word by substituting the character
                new_word = v[:i] + char + v[i + 1:]

                # If new word is in the dictionary, add it as an edge 
                if new_word in self.dictionary:
                    edges.append(Edge(v, new_word))
        
        return edges

        # Important note:
        # `self.alphabet` and `self.dictionary` use Python's built-in `set` type.
        # This is very efficient but iterating over the sets is unpredictable,
        # which might lead to some variations in the results.
        # See the lab description for more information.
        #---------- END TASK 2 -----------------------------------------------#

    def is_weighted(self) -> bool:
        return False

    def guess_cost(self, v: Word, w: Word) -> float:
        """
        Returns the guessed best cost for getting from a word to another.
        (the number of differing character positions)
        """
        #---------- TASK 4: Guessing the cost, Wordladder --------------------#
        # TODO: Replace these lines with your solution!
        # Don't forget to handle the case where the lengths differ.
        if len(v) != len(w):
            return float('inf') 

        differences = 0

        for i in range(len(v)):
            if v[i] != w[i]:
                differences += 1

        return differences
        #---------- END TASK 4 -----------------------------------------------#

    def parse_node(self, s: str) -> Word:
        word = s.lower()
        if word not in self.dictionary:
            raise ValueError(f"Unknown word: {word}")
        return word

    def __str__(self) -> str:
        return (
            f"Word ladder graph with {self.num_nodes()} words.\n" +
            "Alphabet: " +
            "".join(sorted(self.alphabet)) +
            "\n\nRandom example nodes with outgoing edges:\n" +
            self.example_outgoing_edges(8)
        )


if __name__ == '__main__':
    _, dictionary = sys.argv
    ladder = WordLadder(dictionary)
    print(ladder)

