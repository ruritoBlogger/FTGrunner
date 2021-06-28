from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.frame import DataFrame
import seaborn as sns

from .get_result import get_result, get_evaluate_result


def create_graph(output_file: str, dirname: str = "env") -> None:
    """学習結果をグラフにする
    試合のログから試合の勝率を取得してグラフにする

    Args:
        output_file (str): グラフの保存先
        dirname (str, optional): 実行環境のパス. デフォルトは"env".
    """

    result: List[float] = get_result(dirname + "/log/point/")
    plt.plot(result)
    plt.savefig(output_file)


def create_evaluate_graph(output_file: str, dirname: str) -> None:
    """AIの評価結果をグラフにする

    Args:
        output_file (str): グラフの保存先
        dirname (str, optional): logの保存先.
    """

    result: DataFrame = get_evaluate_result(dirname)

    x: List[int] = list(range(len(ave_result)))

    deviation: List[float] = []

    fig = plt.figure()
    plt.plot(x, ave_result)
    plt.fill_between(x, )


if __name__ == "__main__":
    create_graph("result.png")
    create_evaluate_graph("log/log.csv")
