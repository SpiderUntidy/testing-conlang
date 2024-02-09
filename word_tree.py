class WordTree:
    """Um tree node de palavras."""
    def __init__(self, word=None, parents=(None, None)):
        self.word = word
        self.left = parents[0]
        self.right = parents[1]

    def __str__(self):
        return self.word
