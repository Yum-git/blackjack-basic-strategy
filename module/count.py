def card_list_count(card_list: list) -> int:
    card_count = 0

    card_list_sort = sorted(card_list, reverse=True)
    # プレイヤーの数を確認
    for value in card_list_sort:
        if value >= 10:
            card_count += 10
        elif value == 1:
            if card_count >= 11:
                card_count += 1
            else:
                card_count += 11
        else:
            card_count += value

    return card_count