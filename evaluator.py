from typing import List
import shutil
import os
import csv
import time

from util import *
from train import train


def evaluate_agent(config: Config) -> None:
    """AIの評価を行う
    具体的にはEPISODE * EVALUATE_NUM回試合をやる
    各EPISODE毎の勝率の平均値・最大値・最小値をplotして評価するみたいな感じ

    Args:
        config (Config): 評価や学習に用いる設定
    """

    result = List[List[float]]

    log_dir: str = config.env_dir + "/log/point"
    output_dir: str = "/log/"

    shutil.rmtree(log_dir)
    os.mkdir(log_dir)

    for key in range(config.evaluate_num):

        print("{}回目の学習です".format(key+1))

        train(config)
        print("evaluator 学習終了")
        time.sleep(10)
        episode_result: List[float] = get_result(
            config.env_dir + "/log/point/")
        result.append(episode_result)

        shutil.rmtree(log_dir)
        os.mkdir(log_dir)

    # TODO: 対戦相手や実行時間などをファイル名に含める
    # TODO: 書き込み部分は分離させたい
    with open(output_dir + 'log.csv') as f:
        writer = csv.writer(f)
        for episode_result in result:
            writer.writerow(episode_result)


if __name__ == "__main__":
    config = Config()
    evaluate_agent(config)
