from word_tree import WordTree


def ler_vocab(path):
        """Recebe o path de um arquivo de palavras e retorna seu WordTree."""
        with open(path, 'r', encoding='utf-8') as reader:
            line = reader.readline()[:-1]
            vocab = []
            while line != '':
                orig, orig_left, orig_right, *signif = line.split(' ')

                word = WordTree(orig, parents=(orig_left, orig_right))
                signif = ' '.join(signif)
                vocab.append((word, signif))

                line = reader.readline()[:-1]

        return vocab

 
def ler_fonemas(path):
    """Recebe o path de um arquivo de fonemas e retorna seu texto."""
    with open(path, 'r', encoding='utf-8') as reader:
        fonemas = reader.read()
        
    return fonemas


class Vocabulario:
    """Classe que representa nosso vocabulário."""

    def __init__(self, path_v, path_f):
        self.path_v = path_v
        self.path_f = path_f
        
        self.words = ler_vocab(self.path_v)
        self.sounds = ler_fonemas(self.path_f)


    def write_vocab(self):
        """Grava o vocabulário a um arquivo."""
        with open(self.path_v, 'w', encoding='utf-8') as writer:
            lines = []
            for orig, signif in self.words:
                partes = [orig, orig.left, orig.right, signif]
                line = " ".join(map(str, partes))
                lines.append(line + '\n')
            writer.writelines(sorted(lines))
    

    def print_vocab(self):
        """Exibe as palavras do vocabulário."""
        print(f"\n{len(self.words)} palavras encontradas\n")
        for palavra in self.words:
            print(f"{palavra[0]}: {palavra[1]}")
        print()
    

    def print_fonemas(self):
        """Exibe os fonemas do vocabulário."""
        print(self.sounds)

    
    def add_primit(self):
        """Adiciona uma palavra primitiva ao vocabulário."""

        word = input("Insira a palavra: ")
        signif = input("Insira seu significado: ")
        
        new_word = WordTree(word), signif
        self.words.append(new_word)

    
    def add_comp(self):
        """Adiciona uma palavra derivada de outras duas preexistentes no vocabulário."""

        parents = input("Insira as palavras-pai (na ordem da composição, separadas por espaço): ")
        signif = input("Insira o significado derivado: ")
        
        sep_parents = parents.split(' ')
        true_parents = [word[0] for word in self.words if str(word[0]) in sep_parents]
        if len(true_parents) == 2:
            deriv = WordTree(word='-'.join(sep_parents), parents=true_parents)
            new_word = deriv, signif
            self.words.append(new_word)
        else:
            raise Exception("Palavras não contidas no vocabulário.")
