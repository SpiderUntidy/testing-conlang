class WordTree:
    """Um tree node de palavras."""
    def __init__(self, word=None, parents=(None, None)):
        self.word = word
        self.left = parents[0]
        self.right = parents[1]

    def __str__(self):
        return self.word


def ler_vocab(path):
    """Ler arquivo de palavras."""
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


def escrever_vocab(vocab, path):
    """Gravar vocabulário a um arquivo."""
    with open(path, 'w', encoding='utf-8') as writer:
        lines = []
        for orig, signif in vocab:
            partes = [orig, orig.left, orig.right, signif]
            line = " ".join(map(str, partes))
            lines.append(line + '\n')
        writer.writelines(lines)


def print_options():
    """Exibe as opções de comando."""
    print("1 - exibir vocabulário")
    print("2 - adicionar palavra raíz")
    print("3 - compor palavra derivada")
    print("0 - sair")
    print()


def comandos(vocab):
    """Enclausura os comandos definidos."""
    option = input("Insira seu comando: ")

    if option == '0':
        return 0
    elif option == '1':
        print(f"\n{len(vocab)} palavras encontradas\n")
        for palavra in vocab:
            print(f"{palavra[0]}: {palavra[1]}")
        print()
    elif option == '2':
        in_word = WordTree(word=input("Insira a palavra: "))
        in_signif = input("Insira seu significado: ")

        vocab.append((in_word, in_signif))
        print()
    elif option == '3':
        in_parents = input("Insira as palavras-pai (em ordem de derivação, separadas por espaço): ")
        deriv_signif = input("Insira o significado derivado: ")

        sep_parents = in_parents.split(' ')
        true_parents = [word[0] for word in vocab if str(word[0]) in sep_parents]
        if len(true_parents) == 2:
            deriv = WordTree(word='-'.join(sep_parents), parents=true_parents)
            vocab.append((deriv, deriv_signif))
        else:
            print("Palavras não contidas no vocabulário.")
        print()
    else:
        print("Comando inválido.")

    return True


if __name__ == '__main__':
    vocabulario = ler_vocab('vocabulario.txt')  # Lê o vocabulário, definindo sua tree

    while True:
        print_options()  # Exibe os comandos possíveis
        if comandos(vocabulario) == 0:  # Executa os comandos
            break

    escrever_vocab(vocabulario, 'vocabulario.txt')  # Por fim grava o vocabulário
