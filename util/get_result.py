import glob
import csv
from typing import List
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
    print(get_evaluate_result("log/log.csv"))
