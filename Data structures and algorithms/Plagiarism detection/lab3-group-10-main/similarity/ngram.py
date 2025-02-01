
class Ngram(tuple[str, ...]):
    """
    An n-gram is just a tuple of tokens (strings).
    """

    def __str__(self) -> str:
        return "+".join(self)

    @staticmethod
    def ngrams(input: list[str], n: int) -> list['Ngram']:
        """
        Return all n-grams of a given list of tokens.
        """
        count = len(input) - n + 1
        return [Ngram(input[i : i+n]) for i in range(count)]

