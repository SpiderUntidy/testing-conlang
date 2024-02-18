from word_tree import WordTree
import json


def ler_words(path: str) -> dict[str, "WordTree"]:
    """Recebe o path de um arquivo de palavras e retorna seu WordTree."""
    with open(path) as file:
        read = json.load(file)
        words = {}

        read_divided = {}
        prev_words = [None]

        """
        Dividem-se as palavras com base em seus parents.
        Sem parents (primitiva) -> nível 0
        Ambos os parents nível 0 -> nível 1
        Algum parent nível n -> nível n + 1
        """

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

        # A WordTree é montada seguindo sequencialmente os níveis
        for _, level in read_divided.items():
            for w, word in level:
                parents = []
                for parent in word["parents"]:
                    if parent in words:
                        parents.append(words[parent])
                    else:
                        parents.append(None)
                words[w] = WordTree(word["word"], word["signif"], parents)
    
    words = dict(sorted(words.items()))
    return words


def ler_fonemas(path: str):
    """Recebe o path de um arquivo de fonemas e retorna seu texto."""
    with open(path, 'r', encoding='utf-8') as reader:
        fonemas = reader.read()

    return fonemas


class Vocabulario:
    """Classe que representa nosso vocabulário."""

    def __init__(self, path_words: str, path_sounds: str):
        """Lê os arquivos de palavras e fonemas para inicializar nosso vocabulário."""
        self.path_words = path_words
        self.path_sounds = path_sounds

        self.words = ler_words(self.path_words)
        self.sounds = ler_fonemas(self.path_sounds)


    def save_words(self):
        """Grava o vocabulário."""

        # Função que codifica o objetos WordTree para o formato JSON
        encoder = lambda word: {
            "word": word.word,
            "signif": word.signif,
            "parents": [str(parent) if parent is not None else None for parent in word.parents]
        }

        """
        Para evitar perda de dados em caso de erros de execução,
        O arquivo é salvo na variável backup, que é utilizada pelo exception handler caso necessário.
        """

        with open(self.path_words, 'r', encoding='utf-8') as file:
            backup = json.load(file)

        with open(self.path_words, 'w', encoding='utf-8') as file:
            try:
                s_words = dict(sorted(self.words.items()))
                json.dump(s_words, file, ensure_ascii=False, indent=4, default=encoder)
            except Exception as err:
                json.dump(backup, file, ensure_ascii=False, indent=4)
                print(f"Unexpected {err=}, {type(err)=}")
                raise


    def print_words(self):
        """Exibe as palavras do vocabulário."""
        print(f"\n{len(self.words)} palavras encontradas\n")
        for palavra in self.words.values():
            print(f"{palavra}: {', '.join(palavra.signif)}")
        print()


    def print_fonemas(self):
        """Exibe os fonemas do vocabulário."""
        print(self.sounds)


    def print_parents(self):
        """Exibe os ancestrais de uma palavra contida no vocabulário."""
        word = input("Insira a palavra: ")
        if not word in self.words.keys():
            print("Essa palavra não existe.")
        else:
            wt = self.words[word]
            wt.print_parents()
        print()


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

        if len(true_parents) != 2:
            print("Insira exatamente duas palavras para a composição.")
        elif comp in self.words.keys():
            print("Essa palavra já existe.")
        else:
            new_word = WordTree(comp, signif, parents=true_parents)
            self.words[comp] = new_word


    def del_word(self):  # Não deletar uma palavra pai de outra!!! (deve-se impossibilitar isso.)
        """Deleta uma palavra do vocabulário."""
        word = input("Insira a palavra a ser excluída: ")
        del self.words[word]
