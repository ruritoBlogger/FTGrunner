from typing import List
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import numpy as np


def create_win_rate(dirname: str) -> None:
    """勝率のログから計算し表示する
    """
    result: List[float] = get_win_rate(dirname)
    print(result)


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


def create_evaluate_graph(dirname: str) -> None:
    """AIの評価結果をグラフにする

    Args:
        dirname (str): logの保存先.
    """

    result: DataFrame = get_evaluate_result(dirname)

    x = range(len(result.columns))

    y: List[float] = [0.0] * len(result.columns)
    y_mean: List[float] = [0.0] * len(result.columns)
    y_std: List[float] = [0.0] * len(result.columns)

    # 各試合の平均や分散を計算する
    for i in range(len(result.columns)):
        # TODO: 最適なパラメータを設定する
        # NOTE: rolling(n)は直近n回分から平均などを計算する
        n = 3
        episode_mean = result[i].mean()
        episode_std = result[i].std()

        y_mean[i] = episode_mean
        y_std[i] = episode_std

    # TODO: ログのファイル名からタイトルなどを決定する
    our_AI = "ERHEA_PI"
    opp_AI = "MctsAi"

    plt.plot(x, y_mean, color="0.3")
    y_mean = np.array(y_mean)
    y_std = np.array(y_std)
    plt.fill_between(x, y_mean - y_std, y_mean + y_std, color="0.7")
    plt.title("the result of learning with {} vs {}".format(our_AI, opp_AI))
    plt.xlabel("episode")
    plt.ylabel("win rate")
    # plt.show()
    plt.savefig("result.png")


if __name__ == "__main__":
    from get_result import get_result, get_evaluate_result, get_win_rate
    # create_graph("result.png")
    # create_evaluate_graph("result.png", "log/log.csv")
    create_win_rate("log/winrate.csv")

else:
    from .get_result import get_result, get_evaluate_result, get_win_rate
