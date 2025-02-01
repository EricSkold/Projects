#!/usr/bin/env python3

"""
Command-line tool for detecting similar files.
"""

from pathlib import Path
from typing import Any

from similarity.similarity_calculator import SimilarityCalculator
from similarity.faster_similarity_calculator import FasterSimilarityCalculator

from map.map import Map
from map.list_map import ListMap
from map.bst_map import BSTMap
from map.avl_map import AVLMap
from map.multimap import Multimap

from utilities.command_parser import CommandParser
from utilities.stopwatch import Stopwatch


map_implementations: dict[str, type[Map[Any, Any]]] = {
    "list": ListMap,
    "bst": BSTMap,
    "avl": AVLMap,
}

parser = CommandParser(description=(__doc__ or "").strip())
parser.add_argument("--documents", "-d", required=True, type=Path,
                    help="path to directory of documents")
parser.add_argument("--index", "-i", action="store_true",
                    help="use the optimised file index (default: use the slow version)")
parser.add_argument("--map", "-m", choices=list(map_implementations), default="list",
                    help="map implementation (default: use key-value list)")
parser.add_argument("--ngram", "-n", type=int, default=5,
                    help="ngram size (default: 5)")
parser.add_argument("--limit", "-l", type=int, default=10,
                    help="limit the number of similar file pairs (default: 10)")
parser.add_argument("--similarity", "-s", choices=SimilarityCalculator.similarity_measures, default='absolute',
                    help="similarity measure to sort by (default: 'absolute')")


def main():
    options = parser.parse_args()
    if not options.documents.is_dir():
        raise FileNotFoundError(f"The directory '{options.documents}' does not exist")

    calculator = SimilarityCalculator()
    if options.index: calculator = FasterSimilarityCalculator()

    # Initialise the maps.
    map_class = map_implementations[options.map]
    calculator.file_ngrams = Multimap(map_class, map_class)
    calculator.ngram_index = Multimap(map_class, map_class)
    calculator.intersections = Multimap(map_class, map_class)

    # Find all .txt files in the directory and sort the filenames.
    paths = sorted(options.documents.glob('*.txt'))
    if not paths:
        raise FileNotFoundError("Empty directory")

    # Create stopwatches time the execution of each phase of the program.
    stopwatch_total = Stopwatch()
    stopwatch = Stopwatch()

    # Phase 1: Read n-grams from all input files.
    calculator.read_ngrams_from_files(paths, options.ngram)
    calculator.file_ngrams.validate()
    stopwatch.finished("Reading all input files")

    # Phase 2: Build index of n-grams.
    if options.index:
        calculator.build_ngram_index()
        calculator.ngram_index.validate()
        stopwatch.finished("Building n-gram index")

    # Phase 3: Compute the n-gram intersections of all file pairs.
    calculator.compute_intersections()
    calculator.intersections.validate()
    stopwatch.finished("Computing intersections")

    # Phase 4: Find the L most similar file pairs, arranged in decreasing order of similarity.
    most_similar = calculator.find_most_similar(options.limit, measure=options.similarity)
    stopwatch.finished("Finding the most similar files")

    stopwatch_total.finished("In total the program")

    # Print out some statistics.
    print()
    print("Balance statistics:")
    print(f"  file_ngrams: {calculator.file_ngrams}")
    if options.index:
        print(f"  ngram_index: {calculator.ngram_index}")
    print(f"  intersections: {calculator.intersections}")

    # Print out the plagiarism report!
    print()
    print("Plagiarism report:")
    print("".join(f"{measure.rpartition('-')[0]:>10s}" for measure in calculator.similarity_measures))
    print("".join(f"{measure.rpartition('-')[-1]:>10s}" for measure in calculator.similarity_measures))
    max_filename_size = max((len(pair[0].name) for pair in most_similar), default=0)
    for pair in most_similar:
        for measure in calculator.similarity_measures:
            decimals = 0 if measure == 'absolute' else 2 if 'weighted' in measure else 3
            print(f"{calculator.similarity(pair, measure):>10.{decimals}f}", end="")
        print(f"  {pair[0].name:{max_filename_size}s} {pair[1].name:s}")


if __name__ == '__main__':
    main()


