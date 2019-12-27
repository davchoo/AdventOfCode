def deal(src_deck):
    return src_deck[::-1]


def cut(deck, n):
    a = deck[:n]
    b = deck[n:]
    return b + a


def deal_increment(deck, n, num_cards):
    new_deck = [0] * num_cards
    for i, number in enumerate(deck):
        new_deck[(i * n) % num_cards] = number

    return new_deck


def shuffle(process, n_cards=10007, times=1):
    cards = list(range(n_cards))
    for i in range(times):
        for line in process.splitlines():
            if "deal into new stack" in line:
                cards = deal(cards)
            elif "cut" in line:
                _, n = line.split(" ")
                cards = cut(cards, int(n))
            elif "deal with increment" in line:
                *_, n = line.split(" ")
                cards = deal_increment(cards, int(n), n_cards)
    return cards


def solve_a(data):
    cards = shuffle(data)
    return cards.index(2019)


def solve_b(data):
    return 0
