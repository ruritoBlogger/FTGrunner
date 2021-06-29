from typing import List
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame


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

    x = range(len(result["data"]))

    y = result["data"]
    y_mean = result["data"].rolling(3).mean()
    y_std = result["data"].rolling(3).std()

    plt.plot(x, y)
    plt.fill_between(x, y_mean - y_std, y_mean + y_std)
    plt.show()


if __name__ == "__main__":
    from get_result import get_result, get_evaluate_result
    # create_graph("result.png")
    create_evaluate_graph("result.png", "log/log.csv")

else:
    from .get_result import get_result, get_evaluate_result
