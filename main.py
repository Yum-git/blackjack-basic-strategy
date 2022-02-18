import random
import traceback
from typing import List

from module.count import card_list_count
from module.strategy import split_strategy, hard_strategy, soft_strategy


cards: List[List[int]] = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
] * 6


def main():
    # 総収益
    total: int = 0

    # 利用したカードの枚数
    card_cost_count: int = 0

    # プレイヤー勝利数
    player_win_count: int = 0

    # ディーラー勝利数
    dealer_win_count: int = 0

    # 引き分け数
    tie_count: int = 0

    # エラー数（デバッグ用）
    error_counter: int = 0

    card_: List[int] = random.sample(sum(cards, []), len(sum(cards, [])))

    for idx in range(100000):
        try:
            if idx != 0:
                print("\r{}戦目：   PlayerWin{} : Tie{} : DealerWin{}   勝率 : {}  引き分け率 ： {}   負率 : {}   勝ち額 ： {}  例外処理数 : {}".format(
                    idx+1,
                    player_win_count, tie_count, dealer_win_count,
                    player_win_count / sum([player_win_count, tie_count, dealer_win_count]),
                    tie_count / sum([player_win_count, tie_count, dealer_win_count]),
                    dealer_win_count / sum([player_win_count, tie_count, dealer_win_count]),
                    total,
                    error_counter
                ), end='')

            # シャッフルする条件
            if len(sum(cards, [])) // 2 < card_cost_count:
                card_cost_count = 0
                card_ = random.sample(sum(cards, []), len(sum(cards, [])))

            bj_flag: bool = True

            # プレイヤーの状態を示すリスト
            player_information_list: list = []
            # ディーラーの状態を示す辞書
            dealer_information_dict: dict = dict()

            # プレイヤーの状態にカードリストとベットをリスト内辞書に記載
            player_information_list.append({
                "card_list": [card_.pop(), card_.pop()],
                "bet": 1,
                "bj_flag": False,
                "sur_flag": False
            })

            # ディーラーの状態にカードリストを記載
            dealer_information_dict["card_list"] = [
                card_.pop(), card_.pop()
            ]

            card_cost_count += 4

            dealer_open_card: int = dealer_information_dict["card_list"][0]

            # プレイヤーのターン
            for index, player_information in enumerate(player_information_list):
                # プレイヤー
                while True:
                    player_information = player_information_list[index]
                    player_count: int = card_list_count(player_information["card_list"])

                    if len(player_information["card_list"]) == 2:
                        if player_count == 21:
                            player_information["bet"] *= 1.5
                            player_information["bj_flag"] = True
                            break
                        bj_flag = False
                        if player_information["card_list"][0] == player_information["card_list"][1]:
                            split_player_count = player_information["card_list"][0]
                            choice_strategy = split_strategy(player_count=split_player_count, dealer_open_card=dealer_open_card)
                        elif 1 in player_information["card_list"]:
                            soft_player_count = player_count - 11
                            choice_strategy = soft_strategy(player_count=soft_player_count, dealer_open_card=dealer_open_card)
                        else:
                            hard_player_count = player_count
                            choice_strategy = hard_strategy(player_count=hard_player_count, dealer_open_card=dealer_open_card)
                    else:
                        hard_player_count = player_count
                        choice_strategy = hard_strategy(player_count=hard_player_count, dealer_open_card=dealer_open_card)

                    if choice_strategy == "R" and len(player_information["card_list"]) > 2:
                        choice_strategy = "H"

                    match choice_strategy:
                        case "H":
                            player_information["card_list"].append(card_.pop())
                            card_cost_count += 1
                        case "S":
                            break
                        case "D":
                            player_information["bet"] *= 2
                            player_information["card_list"].append(card_.pop())
                            card_cost_count += 1
                            break
                        case "R":
                            player_information["bet"] /= 2
                            player_information["sur_flag"] = True
                            break
                        case "P":
                            player_information_list[index] = {
                                "card_list": [player_information["card_list"][0], card_.pop()],
                                "bet": 1,
                                "bj_flag": False,
                                "sur_flag": False
                            }
                            player_information_list.append(
                                {
                                    "card_list": [player_information["card_list"][0], card_.pop()],
                                    "bet": 1,
                                    "bj_flag": False,
                                    "sur_flag": False
                                }
                            )
                            card_cost_count += 2
                        case _:
                            raise Exception

            # ディーラーのターン
            while True:
                if bj_flag:
                    break
                else:
                    dealer_count: int = card_list_count(card_list=dealer_information_dict["card_list"])

                    if dealer_count < 17:
                        dealer_information_dict["card_list"].append(card_.pop())
                        card_cost_count += 1
                    else:
                        break


            # 勝敗
            dealer_count = card_list_count(card_list=dealer_information_dict["card_list"])
            for player_information in player_information_list:
                player_count = card_list_count(player_information["card_list"])
                bet = player_information["bet"]

                player_sur_flag = player_information["sur_flag"]
                player_bj_flag = player_information["bj_flag"]

                if player_count >= 22:
                    dealer_win_count += 1
                    total -= bet
                elif player_sur_flag:
                    dealer_win_count += 1
                    total -= bet
                elif dealer_count >= 22:
                    player_win_count += 1
                    total += bet
                elif player_count > dealer_count:
                    player_win_count += 1
                    total += bet
                elif player_count < dealer_count:
                    dealer_win_count += 1
                    total -= bet
                elif player_count == dealer_count and player_bj_flag and len(dealer_information_dict["card_list"]) != 2:
                    player_win_count += 1
                    total += bet
                else:
                    tie_count += 1
        except Exception:
            print(traceback.format_exc())
            error_counter += 1

if __name__ == '__main__':
    main()

