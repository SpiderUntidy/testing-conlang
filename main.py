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


def ler_fonemas(path):
    """Ler arquivo de fonemas."""
    with open(path, 'r', encoding='utf-8') as reader:
        fonemas = reader.read()
    
    return fonemas


def escrever_vocab(vocab, path):
    """Gravar vocabulário a um arquivo."""
    with open(path, 'w', encoding='utf-8') as writer:
        lines = []
        for orig, signif in vocab:
            partes = [orig, orig.left, orig.right, signif]
            line = " ".join(map(str, partes))
            lines.append(line + '\n')
        writer.writelines(sorted(lines))


def format_vocab(vocab):
    """Formata o vocabulário."""
    f_vocab = []

    f_vocab.append(f"\n{len(vocab)} palavras encontradas\n")
    for palavra in vocab:
        f_vocab.append(f"\n{palavra[0]}: {palavra[1]}")
    f_vocab.append("\n")

    return ''.join(f_vocab)


def add_root(word, signif, vocab):
    """Adiciona uma palavra primitiva ao vocabulário."""
    new_word = [(WordTree(word), signif)]
    new_vocab = vocab + new_word
    
    return new_vocab


def fazer_deriv(parents, signif, vocab):
    """Adiciona uma palavra derivada de outras duas preexistentes ao vocabulário."""
    sep_parents = parents.split(' ')
    true_parents = [word[0] for word in vocab if str(word[0]) in sep_parents]
    if len(true_parents) == 2:
        deriv = WordTree(word='-'.join(sep_parents), parents=true_parents)
        new_word = [(deriv, signif)]
        new_vocab = vocab + new_word
    else:
        raise Exception("Palavras não contidas no vocabulário.")
    
    return new_vocab


def comandos(vocab, fonemas):
    """Enclausura os comandos definidos."""
    option = input("Insira seu comando: ")
    print()

    if option == '0':
        return 0
    elif option == '1':
        print(format_vocab(vocab))
    elif option == '2':
        print(fonemas)
    elif option == '3':
        in_word = input("Insira a palavra: ")
        in_signif = input("Insira seu significado: ")
        vocab = add_root(in_word, in_signif, vocab)
    elif option == '4':
        in_parents = input("Insira as palavras-pai (em ordem de derivação, separadas por espaço): ")
        deriv_signif = input("Insira o significado derivado: ")
        vocab = fazer_deriv(in_parents, deriv_signif, vocab)
    else:
        print("Comando inválido.")

    return vocab


if __name__ == "__main__":
    # Lê o vocabulário, definindo sua tree
    vocabulario = ler_vocab("vocabulario.txt")
    fonemas = ler_fonemas("fonemas.txt")

    options = [
        "1 - exibir vocabulário",
        "2 - exibir fonemas",
        "3 - adicionar palavra primitiva",
        "4 - compor palavra derivada",
        "0 - sair"
    ]

    while True:
        # Exibe os comandos possíveis
        print('\n', *options, '\n', sep='\n')

        # Chama a função de comandos
        v_comando = comandos(vocabulario, fonemas)

        # Interrompe caso o comando seja 0
        if v_comando == 0:
            break
        # Do contrário atualiza o vocabulário
        vocabulario = v_comando

    # Por fim grava o vocabulário
    escrever_vocab(vocabulario, "vocabulario.txt")
