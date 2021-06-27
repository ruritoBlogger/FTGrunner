from typing import List
import matplotlib.pyplot as plt

from .get_result import get_result


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


if __name__ == "__main__":
    create_graph("result.png")
