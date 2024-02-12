class WordTree:
    """Um tree node de palavras."""
    def __init__(self, word=None, signif=None, parents=(None, None)):
        self.word = word
        self.signif = signif
        self.parents = parents


    def __str__(self):
        return self.word
