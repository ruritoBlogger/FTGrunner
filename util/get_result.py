import glob
import csv
from typing import List, Tuple
import pandas as pd
from pandas.core.frame import DataFrame


def get_result(dir_path: str) -> List[float]:
    """試合のログ(csv)から勝敗データを抽出する

    Args:
        file_path (str): 抽出したい試合のログが格納されているパス

    Returns:
        List[float]: 勝率データ
    """

    files = glob.glob(dir_path + "*.csv")
    result = []

    for file in files:
        csv_file = open(file, "r")
        csv_data = csv.reader(csv_file, delimiter=",", doublequote=True,
                              lineterminator="\r\n", quotechar='"', skipinitialspace=True)

        win = 0
        lose = 0
        for data in csv_data:
            if int(data[1]) >= int(data[2]):
                win += 1
            else:
                lose += 1
        result.append(win/(win+lose))

    return result


def get_result_with_round_rate(dir_path: str) -> List[Tuple[int, int, int, int]]:
    """試合のログ(csv)から勝敗データを抽出する
    各ラウンドの勝率及び全体の勝率を抽出する

    Args:
        file_path (str): 抽出したい試合のログが格納されているパス

    Returns:
        List[Tuple[int, int, int, int]]: 勝率データ
        [1R目は勝利したか, 2R目は勝利したか, 3R目は勝利したか, 試合は勝利したか]
    """

    files = glob.glob(dir_path + "*.csv")
    result: List[Tuple[int, int, int, int]] = []

    for file in files:
        csv_file = open(file, "r")
        csv_data = csv.reader(csv_file, delimiter=",", doublequote=True,
                              lineterminator="\r\n", quotechar='"', skipinitialspace=True)

        win = 0
        lose = 0
        episode_result: Tuple[int, int, int, int] = [0, 0, 0, 0]
        for key, data in enumerate(csv_data):
            if int(data[1]) >= int(data[2]):
                episode_result[key] = 1
                win += 1
            else:
                episode_result[key] = -1
                lose += 1

        episode_result[3] = 1 if win > lose else -1
        result.append(episode_result)

    return result


def get_evaluate_result(dir_path: str) -> DataFrame:
    """評価データを取得する
    評価データはcsvで保存されている

    Args:
        dir_path (str): 評価データのパス

    Returns:
        DataFrame: 評価データ
    """

    df: DataFrame = pd.read_csv(dir_path, header=None)
    df = df.transpose()
    return df


if __name__ == "__main__":
    # print(get_result("env/log/point/"))
    # print(get_evaluate_result("log/log.csv"))
    print(get_result_with_round_rate("FTG4.50/log/point/"))
