def read_vocab():
    with open('vocabulario.txt') as reader:
        keys = []
        values = []

        line = reader.readline()[:-1]
        while line != '':
            line = line.split(': ')

            keys.append(line[0])
            values.append(line[1])

            line = reader.readline()[:-1]

    return dict(zip(keys, values))


if __name__ == '__main__':
    vocab = read_vocab()

    for k, v in vocab.items():
        print(f"{k}: {v}")
