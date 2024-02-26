from vocabulario import Vocabulario

if __name__ == "__main__":
    # Lê o vocabulário, definindo seu objeto
    vocabulario = Vocabulario("words.json", "sounds.txt")

    # Define os comandos possíveis
    filtro = lambda func: callable(getattr(vocabulario, func)) and not func.startswith("_")
    commands = [func for func in dir(vocabulario) if filtro(func)]
    commands = {**dict(zip(range(1, len(commands) + 1), commands)), 0: "exit"}

    # --- Loop de execução ---
    while True:
        # Exibe os comandos
        for k, v in commands.items():
            print(f"{k} - {v}")
        print()

        # Seleciona o comando a ser seguido
        try:
            comando = commands[int(input("Insira seu comando: "))]
            print()
            # Executa o comando
            if comando == "exit":
                break
            else:
                getattr(vocabulario, comando)()
                print()
        except (KeyError, ValueError):
            # Caso insira comando que não exista, apenas printar na tela e retornar ao loop
            print("Comando inválido.\n")

    # Por fim grava o vocabulário
    vocabulario.save_words()
