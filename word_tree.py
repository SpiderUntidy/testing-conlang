class WordTree:
    """Um tree node de palavras."""

    def __init__(self, word: str, signif: str, parents: tuple["WordTree", "WordTree"] = (None, None)):
        """Define as propriedades definidoras da WordTree, mais as variáveis auxilares."""
        self.word = word
        self.signif = signif
        self.parents = parents
        
        self.__to_print = {}
        self.__level = 0


    def __str__(self):
        return self.word


    def __all_parents(self, aux: "WordTree"):
        """Preenche o dict __to_print com seus ancestrais, identificando as gerações anteriores."""
        self.__to_print.setdefault(aux.__level, [])
        self.__to_print[aux.__level].append(aux.word)
        
        if not None in aux.parents:
            for parent in aux.parents:
                parent.__level = aux.__level + 1
                self.__all_parents(parent)


    def print_parents(self):
        """Exibe os ancestrais da WordTree."""
        if not self.__to_print:
            self.__level = 0
            self.__all_parents(self)
        
        for _, gen in self.__to_print.items():
            print(*gen, sep=" ")
