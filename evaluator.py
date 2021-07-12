from typing import List
import shutil
import os
import csv
import datetime

from util import *
from game_executor import GameExecutor


def evaluate_agent(config: Config) -> None:
    """AIの評価を行う
    具体的にはEPISODE * EVALUATE_NUM回試合をやる
    各EPISODE毎の勝率の平均値・最大値・最小値をplotして評価するみたいな感じ

    Args:
        config (Config): 評価や学習に用いる設定
    """

    result: List[List[float]] = []

    log_dir: str = "log/point/"
    output_dir: str = "log/"

    # FIXME: ここでディレクトリ移動したくない
    os.chdir(config.env_dir)

    shutil.rmtree(log_dir)
    os.mkdir(log_dir)
    # TODO: 学習したモデルの情報を削除しておく

    trainer = GameExecutor(config)
    send_message(
        config, "評価を開始します.\n 味方は{}, 敵は{}, 味方のキャラは{}, 敵のキャラは{}.\n エピソード数は{}で各エピソードを{}回評価します".format(config.self_player_name, config.opp_player_name, config.self_player_char, config.opp_player_char, config.episode, config.evaluate_num), False)

    for key in range(config.evaluate_num):

        send_message(config, "{}回目の評価を行います.".format(key+1), False)
        trainer.reset()
        trainer.train()
        episode_result: List[float] = get_result(
            log_dir)
        print(episode_result)
        result.append(episode_result)

        shutil.rmtree(log_dir)
        os.mkdir(log_dir)

        # TODO: 学習したモデルの情報のバックアップを作成しておく
        # TODO: また、学習したモデルの情報を削除しておく

    # TODO: 学習が終了したという内容を通知する
    # TODO: 書き込み部分は分離させたい
    os.chdir("../")
    dt_now = datetime.datetime.now()
    file_name: str = config.self_player_char + "_" + \
        config.opp_player_name + "_" + dt_now.strftime("%m%d") + ".csv"
    with open(output_dir + file_name, mode='w', newline="") as f:
        writer = csv.writer(f)
        for episode_result in result:
            writer.writerow(episode_result)


if __name__ == "__main__":
    config = Config()
    evaluate_agent(config)
