import sys
from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters, get_field
from py4j.protocol import Py4JError
import time
from typing import Any
import subprocess
import os
import platform

from util import Config


def train(config: Config) -> None:
    """学習を実行する

    Args:
        config (Config): 学習設定
    """

    os.chdir(config.env_dir)
    if platform.system() == 'Windows':
        cmd = "java -cp FightingICE.jar;./lib/lwjgl/*;./lib/natives/windows/*;./lib/*  Main --py4j --mute --port 4242"
    else:
        cmd = "java -cp FightingICE.jar;./lib/lwjgl/*;./lib/natives/linux/*;./lib/*  Main --py4j --mute --port 4242"
    proc = subprocess.Popen(cmd)

    print("学習を開始します.")
    print("試合数は{}です.".format(config.episode))
    print("味方のAIは{}, キャラは{}です.".format(
        config.self_player_name, config.self_player_char))
    print("敵のAIは{}, キャラは{}です.".format(
        config.opp_player_name, config.opp_player_char))

    gateway: JavaGateway = initialize()

    for i in range(config.episode):
        print("######### {}試合目 ###########".format(i+1))
        run_game(gateway, config.self_player_name, config.opp_player_name,
                 config.self_player_char, config.opp_player_char)
        time.sleep(5)
        sys.stdout.flush()

    # FIXME: このやり方だとエラーが出る(終了はする)ので解決するべき
    cmd = "taskkill /F /PID {} /T".format(proc.pid)
    subprocess.run(cmd)
    print("学習を終了します.")


def initialize() -> JavaGateway:
    """ゲームの実行環境を生成する
    内部ではJavaのプロジェクトを起動してあれこれやってるらしいですね
    知らんけど

    Returns:
        JavaGateway: 実行環境
    """
    gateway_port = 4242
    gateway = JavaGateway(gateway_parameters=GatewayParameters(
        port=gateway_port), callback_server_parameters=CallbackServerParameters(port=0))
    real_callback_port = gateway.get_callback_server().get_listening_port()
    gateway.java_gateway_server.resetCallbackClient(
        gateway.java_gateway_server.getCallbackClient().getAddress(), real_callback_port)

    return gateway


def run_game(gateway: JavaGateway, self: str, opp: str, self_char: str, opp_char: str) -> None:
    """試合を行う

    Args:
        gateway (JavaGateway): 試合の実行に必要なもの(内部でJavaを実行してて, その実行しているJavaとの通信などを担当してそう)
        self (str): 自分のAIの名前(/data/ai/名前.jar)
        opp (str): 相手のAIの名前(/data/ai/名前.jar)
        self_char (str): 自分のキャラ.
        opp_char (str): 相手のキャラ.
    """

    manager = gateway.entry_point
    game = manager.createGame(self_char, opp_char, self, opp, 1)

    try:
        manager.runGame(game)
    except Py4JError:
        # FIXME: 握り潰すのは良くない. 誰か直して(懇願)
        pass

    gateway.close_callback_server()
    gateway.close()


if __name__ == "__main__":
    config = Config()
    train(config)
