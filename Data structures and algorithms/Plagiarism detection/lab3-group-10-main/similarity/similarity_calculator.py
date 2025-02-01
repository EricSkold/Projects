import math
from pathlib import Path
import re

from .ngram import Ngram
from map.multimap import Multimap
from utilities.progress_bar import ProgressBar
import random

PathPair = tuple[Path, Path]


class SimilarityCalculator:
    file_ngrams: Multimap[Path, Ngram]
    ngram_index: Multimap[Ngram, Path]
    intersections: Multimap[PathPair, Ngram]

    def read_ngrams_from_files(self, paths: list[Path], N: int):
        """
        Phase 1: Read in each file and chop it into n-grams.
        Stores the result in the instance variable `file_ngrams`.
        """
        # random.shuffle(paths)
        for path in paths:
            text = path.read_text(encoding="utf-8").lower()
            # Parse the input into lower-case words.
            # A "word" is here a sequence of letters and digits and underscores,
            # which is completely wrong but an ok approximation.
            contents = re.findall(r"\w+", text)
            for ngram in Ngram.ngrams(contents, N):
                self.file_ngrams.add_value(path, ngram)


    def build_ngram_index(self):
        """
        Phase 2: Build index of n-grams.
        This naive version doesn't do anything,
        you should implement it in `faster_similarity_calculation.py`.
        """


    def compute_intersections(self):
        """
        Phase 3: Count which n-grams each pair of files has in common.
        This is the naive, slow version,
        to be improved in `faster_similarity_calculation.py`.
        Uses the instance varable `file_ngrams`.
        Stores the result in the instance variable `intersections`.
        """
        for path1 in ProgressBar(self.file_ngrams, description="Computing intersections"):
            for path2 in self.file_ngrams:
                # Since intersection is a commutative operation (i.e., A & B == B & A),
                # it's enough to only compute the intersection for path pairs (p,q) where p < q:
                if path1 < path2:
                    for ngram1 in self.file_ngrams.get_values(path1):
                        for ngram2 in self.file_ngrams.get_values(path2):
                            if ngram1 == ngram2:
                                pair = (path1, path2)
                                self.intersections.add_value(pair, ngram1)


    def find_most_similar(self, M: int, measure: str) -> list[PathPair]:
        """
        Phase 4: find all pairs, sorted in descending order of similarity.
        Returns a list of the M path pairs that are most similar.
        Uses the instance variables `file_ngrams` and `intersections`.
        """
        return sorted(
            self.intersections,
            key=lambda pair: self.similarity(pair, measure),
            reverse=True
        ) [:M]


    similarity_measures = [
        "absolute", "jaccard", "cosine", "average",
        "weighted-jaccard", "weighted-cosine", "weighted-average",
    ]

    def similarity(self, pair: PathPair, measure: str) -> float:
        """
        Calculates a similarity score between the ngrams in A and B. The following are implemented:

        Absolute number of common ngrams:
            absolute(A, B)  =  |A & B|

        Jaccard index: https://en.wikipedia.org/wiki/Jaccard_index
        This is the proportion of ngrams from A or B that are in both.
            jaccard(A, B)  =  |A & B| / |A v B|
                           =  |A & B| / (|A| + |B| - |A & B|)

        Cosine similarity, or Otsuka-Ochiai coefficient.
        This is the same as the geometric mean of p(B|A) and p(A|B)
        https://en.wikipedia.org/wiki/Cosine_similarity
            cosine(A, B)  =  |A & B| / sqrt(|A|*|B|)
                          =  p(A,B) / sqrt(p(A)*p(B))
                          =  sqrt( |A&B|/|A| * |A&B|/|B| )
                          =  sqrt( p(B|A) * p(A|B) )

        Arithmetic mean of p(B|A) and p(A|B):
            average(A, B)  =  ( |A&B|/|A| + |A&B|/|B| ) / 2
                           =  ( p(B|A) + p(A|B) ) / 2

        Weighted variants of all the above (except absolute):
            weighted-X(A, B)  =  |A&B| * X(A, B)
        """
        if measure not in self.similarity_measures:
            raise ValueError(f"Unknown simliarity measure: {measure}")

        n_AB = len(list(self.intersections.get_values(pair)))

        score: float = n_AB
        if measure == "absolute":
            return score

        n_A = len(list(self.file_ngrams.get_values(pair[0])))
        n_B = len(list(self.file_ngrams.get_values(pair[1])))

        if "jaccard" in measure:
            n_A_or_B = n_A + n_B - n_AB
            score = n_AB / n_A_or_B
        elif "cosine" in measure:
            score = math.sqrt(n_AB/n_A * n_AB/n_B)
        elif "average" in measure:
            score = (n_AB/n_A + n_AB/n_B)/2

        if "weighted" in measure:
            return n_AB * score
        else:
            return score


