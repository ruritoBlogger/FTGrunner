from typing import List
import shutil
import os
import csv

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

    for key in range(config.evaluate_num):

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

    # TODO: 対戦相手や実行時間などをファイル名に含める
    # TODO: 書き込み部分は分離させたい
    os.chdir("../")
    with open(output_dir + 'log.csv', mode='w', newline="") as f:
        writer = csv.writer(f)
        for episode_result in result:
            writer.writerow(episode_result)


if __name__ == "__main__":
    config = Config()
    evaluate_agent(config)
