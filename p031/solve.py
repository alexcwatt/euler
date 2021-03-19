COINS = (1, 2, 5, 10, 20, 50, 100, 200)


def count_combos(coins, total):
    """ Return the number of combinations of *coins* to make *total* """
    coin = coins[-1]
    if len(coins) == 1:
        can_create_total = total % coin == 0
        return int(can_create_total)

    other_coins = coins[:-1]
    coin_counts = int(total / coin)
    combos = 0
    for i in range(coin_counts + 1):
        combos += count_combos(other_coins, total - i * coin)
    return combos


if __name__ == "__main__":
    print(count_combos(COINS, 200))
