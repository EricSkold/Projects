
from .similarity_calculator import SimilarityCalculator
from utilities.progress_bar import ProgressBar

class FasterSimilarityCalculator(SimilarityCalculator):

    def build_ngram_index(self):
        """
        Phase 2: Build index of n-grams.
        Uses the instance varable `file_ngrams`.
        Stores the result in the instance variable `ngram_index`.
        """

        """
        file_ngrams: Multimap[Path, Ngram]
        {
            file1: [ngram1, ngram2, ...],
            file2: [ngram3, ngram4, ...],
            ...
        }

        ngram_index: Multimap[Ngram, Path]
        {
            ngram1: [file1, file2, file3, file6 ...],
            ngram2: [file3, file4, ...],
            ngram3: [file1, file3, ...],
            ...
        }
        """

        for file_path in ProgressBar(self.file_ngrams, description="Building index"):
            ngrams = self.file_ngrams.get_values(file_path)
            for ngram in ngrams:
                self.ngram_index.add_value(ngram, file_path)

    def compute_intersections(self):
        """
        Phase 3: Count how many n-grams each pair of files has in common.
        This version should use the `ngram_index` to make this function much more efficient.
        Stores the result in the instance variable `intersections`.
        """


        """
        intersections: Multimap[PathPair, Ngram]
        {
            (file1, file2): [ngram3, ngram1, ...],
            (file2, file3): [ngram1, ngram2, ...],
            ...
        }
        """

        for ngram in ProgressBar(self.ngram_index, description="Computing intersections"):
            paths = self.ngram_index.get_values(ngram)
            # All pairs of files
            for path1 in paths:
                for path2 in paths:
                    # Symmetric
                    if path1 < path2:
                        pair = (path1, path2)
                        self.intersections.add_value(pair, ngram)
