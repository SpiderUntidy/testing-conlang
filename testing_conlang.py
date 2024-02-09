from vocabulario import Vocabulario


if __name__ == "__main__":
    # Lê o vocabulário, definindo seu objeto
    vocabulario = Vocabulario("vocabulario.txt", "fonemas.txt")

    # Define os comandos possíveis
    options = [
        "1 - exibir vocabulário",
        "2 - exibir fonemas",
        "3 - adicionar palavra primitiva",
        "4 - compor palavra derivada",
        "0 - sair"
    ]

    command_list = {
        1: vocabulario.print_vocab,
        2: vocabulario.print_fonemas,
        3: vocabulario.add_primit,
        4: vocabulario.add_comp,
        0: 0
    }

    # --- Loop de execução ---
    while True:
        # Exibe os comandos possíveis
        print('\n', *options, '\n', sep='\n')

        # Seleciona o comando a ser seguido
        try:
            comando = command_list[int(input("Insira seu comando: "))]
            print()
            # Executa o comando
            if comando == 0:
                break
            else:
                comando()
        except:
            # Em caso de erro, apenas printar na tela e retornar ao loop
            print("Comando inválido.")

    # Por fim grava o vocabulário
    vocabulario.write_vocab()
