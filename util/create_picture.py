from typing import List
import matplotlib.pyplot as plt
import glob
import csv


def create_graph(output_file: str, dirname: str = "env") -> None:
    """学習結果をグラフにする
    試合のログから試合の勝率を取得してグラフにする

    Args:
        output_file (str): グラフの保存先
        dirname (str, optional): 実行環境のパス. デフォルトは"env".
    """

    result: List[float] = read_data(dirname + "/log/point/")
    plt.plot(result)
    plt.savefig(output_file)


def read_data(dir_path: str) -> List[float]:
    """試合のログ(csv)から勝敗データを抽出する

    Args:
        file_path (str): 抽出したい試合のログが格納されているパス

    Returns:
        List[bool]: 勝率データ
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


if __name__ == "__main__":
    create_graph("result.png")
