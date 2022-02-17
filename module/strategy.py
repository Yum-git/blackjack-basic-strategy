import yaml

SETTING_FILE = "strategy.yaml"
# 設定ファイルから設定を読みだし
with open(SETTING_FILE, mode="r", encoding="utf-8") as f:
    settings_data = yaml.safe_load(f)


def hard_strategy(player_count: int, dealer_open_card: int) -> str:
    if 8 <= player_count <= 16:
        basic_strategy_x_idx = player_count
    elif player_count < 8:
        basic_strategy_x_idx = 8
    else:
        basic_strategy_x_idx = 17
    basic_strategy_y_idx = dealer_open_card if dealer_open_card <= 10 else 10

    choice_strategy = settings_data["hard_hand"][basic_strategy_x_idx][basic_strategy_y_idx]

    return choice_strategy


def soft_strategy(player_count: int, dealer_open_card: int) -> str:
    basic_strategy_x_idx = player_count
    basic_strategy_y_idx = dealer_open_card if dealer_open_card <= 10 else 10

    choice_strategy = settings_data["soft_hand"][basic_strategy_x_idx][basic_strategy_y_idx]

    return choice_strategy


def split_strategy(player_count: int, dealer_open_card: int) -> str:
    basic_strategy_x_idx = player_count if player_count <= 10 else 10
    basic_strategy_y_idx = dealer_open_card if dealer_open_card <= 10 else 10

    choice_strategy = settings_data["split_hand"][basic_strategy_x_idx][basic_strategy_y_idx]

    return choice_strategy
