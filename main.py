"""
H: ヒット
S: スタンド
D: ダブルダウン
R: サレンダー
"""
import random

basic_strategy = [
    ["H", "H", "H", "H", "H", "H", "H", "H", "H", "H"],
    ["H", "H", "D", "D", "D", "D", "H", "H", "H", "H"],
    ["H", "D", "D", "D", "D", "D", "D", "D", "D", "H"],
    ["H", "D", "D", "D", "D", "D", "D", "D", "D", "D"],
    ["H", "H", "H", "S", "S", "S", "H", "H", "H", "H"],
    ["H", "S", "S", "S", "S", "S", "H", "H", "H", "H"],
    ["H", "S", "S", "S", "S", "S", "H", "H", "H", "H"],
    ["H", "S", "S", "S", "S", "S", "H", "H", "H", "R"],
    ["R", "S", "S", "S", "S", "S", "H", "H", "R", "R"],
    ["S", "S", "S", "S", "S", "S", "S", "S", "S", "S"]
]

cards = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
] * 6

# カウンティング用カウンター
count_counter = 0


def card_list_count(card_list: list) -> int:
    global count_counter
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

        if value == 1 or value >= 10:
            count_counter -= 1
        elif value >= 7:
            pass
        else:
            count_counter += 1

    return card_count


def main():
    global count_counter
    # 総収益
    total = 0

    # 利用したカードの枚数
    card_cost_count = 0

    # プレイヤー勝利数
    player_win_count = 0

    # ディーラー勝利数
    dealer_win_count = 0

    # 引き分け数
    tie_count = 0

    card_ = random.sample(sum(cards, []), len(sum(cards, [])))

    for idx in range(100001):
        if idx != 0:
            print("\r{}戦目：   PlayerWin{} : Tie{} : DealerWin{}   勝率 : {}   勝ち額 ： {}  カウンティング : {}".format(
                idx+1,
                player_win_count, tie_count, dealer_win_count,
                player_win_count / sum([player_win_count, tie_count, dealer_win_count]),
                total,
                count_counter
            ), end='')

        # シャッフルする条件
        if len(sum(cards, [])) // 2 < card_cost_count:
            card_cost_count = 0
            card_ = random.sample(sum(cards, []), len(sum(cards, [])))

            count_counter = 0

        # ベットする金
        bet = 1

        if count_counter >= 30:
            bet *= 2

        # ブラックジャックのフラグ
        blackjack_flag = False

        # サレンダーのフラグ
        slender_flag = False

        # ディーラーのカードリスト
        dealer_card_list = []

        # プレイヤーのカードリスト
        player_card_list = []

        # ディーラーのカードを2枚引く　1枚目をオープンカードとする
        dealer_card_list.append(card_.pop())
        dealer_card_list.append(card_.pop())

        # プレイヤーのカードを2枚引く
        player_card_list.append(card_.pop())
        player_card_list.append(card_.pop())

        card_cost_count += 4

        # ディーラーの数を確認
        if dealer_card_list[0] == '1':
            dealer_open_card = 1
        elif dealer_card_list[0] >= 10:
            dealer_open_card = 10
        else:
            dealer_open_card = dealer_card_list[0]

        # プレイヤーのヒットターン
        while True:
            # プレイヤーの数をカウントする
            player_count = card_list_count(player_card_list)

            if player_count == 21 and len(player_card_list) == 2:
                blackjack_flag = True
                bet *= 1.5
                break

            # ベージックストラテジーに沿って選択
            basic_strategy_x_idx = player_count - 8
            if basic_strategy_x_idx <= 0:
                basic_strategy_x_idx = 0
            elif basic_strategy_x_idx >= 9:
                basic_strategy_x_idx = 9
            basic_strategy_y_idx = dealer_open_card - 1

            # 確率がずれすぎてif文で1から比較したい
            # if basic_strategy_x_idx <= 8:
            #     basic_strategy_x_idx = 0
            # elif basic_strategy_x_idx == 9:
            #     basic_strategy_x_idx = 1
            # elif basic_strategy_x_idx == 10:
            #     basic_strategy_x_idx = 2

            choice_strategy = basic_strategy[basic_strategy_x_idx][basic_strategy_y_idx]

            if choice_strategy == "H":
                # ヒット
                player_card_list.append(card_.pop())
                card_cost_count += 1
            elif choice_strategy == "S":
                # スタンド
                break
            elif choice_strategy == "D":
                # ダブルダウン
                bet *= 2
                player_card_list.append(card_.pop())
                card_cost_count += 1
                break
            elif choice_strategy == "R":
                # サレンダー
                bet /= 2
                slender_flag = True
                break

        # ディーラーのヒットターン
        while True:
            # プレイヤーの数をカウントする
            dealer_count = card_list_count(dealer_card_list)

            if blackjack_flag and len(dealer_card_list) == 2 and dealer_count != 21:
                break

            if dealer_count < 17:
                # ヒット
                dealer_card_list.append(card_.pop())
                card_cost_count += 1
            elif 17 <= dealer_count:
                break

        # プレイヤーが21を超えているかどうか確認
        # 超えていれば負けとして次のゲームへ
        if card_list_count(player_card_list) > 21 or slender_flag:
            total -= bet
            dealer_win_count += 1
            continue

        # ディーラーが21を超えているかどうか確認
        # 超えていれば負けとして次のゲームへ
        if card_list_count(dealer_card_list) > 21:
            total += bet
            player_win_count += 1
            continue

        # 勝敗を決める
        # プレイヤー > ディーラー　Win
        if player_count > dealer_count:
            total += bet
            player_win_count += 1
        elif player_count == dealer_count:
            tie_count += 1
        elif dealer_count > player_count:
            total -= bet
            dealer_win_count += 1
        else:
            pass


if __name__ == '__main__':
    main()
