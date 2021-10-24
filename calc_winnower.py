from typing import Tuple, List
import shutil
import os
import csv
import datetime

from util import *
from game_executor import GameExecutor
from util.get_result import get_result_with_round_rate


def calc_win_rate(config: Config) -> None:
    """AIの勝率計算を行う
    指定された試合数(EPISODE * EVALUATE_NUM回)行い、全体の勝率をplotする
    # TODO: 

    Args:
        config (Config): 評価の対象などの設定
    """

    result: Tuple[float, float, float, float]
    log_dir: str = "log/point/"
    output_dir: str = "log/"

    # FIXME: ここでディレクトリ移動したくない
    os.chdir(config.env_dir)

    shutil.rmtree(log_dir)
    os.mkdir(log_dir)
    # TODO: 学習したモデルの情報を削除しておく

    # NOTE: logファイルの名前を固定
    dt_now = datetime.datetime.now()
    file_name: str = "winrate_" + config.self_player_name + "_" + \
        config.opp_player_name + "_" + dt_now.strftime("%m%d") + ".csv"

    trainer = GameExecutor(config)
    send_message(
        config, "勝率計算を開始します.\n 味方は{}, 敵は{}, 味方のキャラは{}, 敵のキャラは{}.\n 試合数は{}回です".format(config.self_player_name, config.opp_player_name, config.self_player_char, config.opp_player_char, config.episode * config.evaluate_num), False)

    for _ in range(config.evaluate_num):

        trainer.reset()
        trainer.train()

        result: List[Tuple[int, int, int, int]] = get_result_with_round_rate(
            log_dir)

        # 定期的にログを残しておく
        os.chdir("../FTGrunner")
        with open(output_dir + file_name, mode='a', newline="") as f:
            writer = csv.writer(f)
            for episode_result in result:
                send_message(config, "debug: episode_result: {}".format(
                    episode_result), False)
                writer.writerow(episode_result)
        os.chdir(config.env_dir)

        # ログの削除
        shutil.rmtree(log_dir)
        os.mkdir(log_dir)


if __name__ == "__main__":
    config = Config()
    calc_win_rate(config)
