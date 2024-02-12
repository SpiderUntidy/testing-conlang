from word_tree import WordTree
import json


def ler_words(path):
    """Recebe o path de um arquivo de palavras e retorna seu WordTree."""
    with open(path) as file:
        read = json.load(file)
        words = {}

        read_divided = {}
        prev_words = [None]
        
        count = 0
        while read.items():
            actual_level = []
            read_divided[count] = []
            for w in list(read.keys()):
                
                if all(parent in prev_words for parent in read[w]["parents"]):
                    actual_level.append(read[w]["word"])
                    read_divided[count].append((w, read[w]))
                    del read[w]
            prev_words += actual_level
            count += 1

        for _, level in read_divided.items():
            for w, word in level:
                parents = []
                for parent in word["parents"]:
                    if parent in words:
                        parents.append(words[parent])
                    else:
                        parents.append(None)
                words[w] = WordTree(word["word"], word["signif"], parents)
    print()
    return words


def ler_fonemas(path):
    """Recebe o path de um arquivo de fonemas e retorna seu texto."""
    with open(path, 'r', encoding='utf-8') as reader:
        fonemas = reader.read()
        
    return fonemas


class Vocabulario:
    """Classe que representa nosso vocabulário."""

    def __init__(self, path_words, path_sounds):
        """Lê os arquivos de palavras e fonemas para inicializar nosso vocabulário."""
        self.path_words = path_words
        self.path_sounds = path_sounds
        
        self.words = ler_words(self.path_words)
        self.sounds = ler_fonemas(self.path_sounds)


    def write_words(self):
        """Grava o vocabulário."""
        encoder = lambda word: {
            "word": word.word,
            "signif": word.signif,
            "parents": [str(parent) if parent is not None else None for parent in word.parents]
        }
        with open(self.path_words, 'w', encoding='utf-8') as file:
            s_words = dict(sorted(self.words.items()))
            json.dump(s_words, file, ensure_ascii=False, indent=4, default=encoder)
  

    def print_words(self):
        """Exibe as palavras do vocabulário."""
        print(f"\n{len(self.words)} palavras encontradas\n")
        for palavra in self.words.values():
            print(f"{palavra}: {', '.join(palavra.signif)}")
        print()


    def print_fonemas(self):
        """Exibe os fonemas do vocabulário."""
        print(self.sounds)


    def add_primit(self):
        """Adiciona uma palavra primitiva ao vocabulário."""

        word = input("Insira a palavra: ")
        signif = input("Insira seu significado: ").split(", ")
        if word in self.words.keys():
            print("Essa palavra primitiva já existe.")
        else:
            new_word = WordTree(word, signif)
            self.words[word] = new_word


    def add_comp(self):
        """Adiciona uma palavra derivada de outras duas preexistentes no vocabulário."""

        parents = input("Insira as palavras-pai (na ordem da composição, separadas por espaço): ")
        signif = input("Insira o significado derivado: ").split(", ")
        
        sep_parents = parents.split(' ')
        true_parents = [word for word in self.words if str(word) in sep_parents]
        comp = '-'.join(sep_parents)

        if len(true_parents) == 2 and not comp in self.words.keys():
            new_word = WordTree(comp, signif, parents=true_parents)
            self.words[comp] = new_word
        else:
            print("Erro na composição.")
