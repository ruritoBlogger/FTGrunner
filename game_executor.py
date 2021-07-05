import platform
import subprocess
from subprocess import Popen
import time
from typing import Any
from py4j.java_gateway import JavaGateway, GatewayParameters, CallbackServerParameters, JavaObject, get_field

from util import Config, send_message


class GameExecutor:
    """FightingICEのゲームの実行を管理する
    """

    __gateway: Any
    __java_process: Popen

    __config: Config
    __exit_cnt: int

    def __init__(self, config: Config) -> None:
        self.__config = config

        self.__exit_cnt = 0

    def reset(self) -> None:
        self.__exit_cnt = 0

    def __start_java_process(self) -> None:
        """Java側でFTGを起動する
        subprocessを用いてJava側を起動する
        また, 実行環境によって起動方法が異なる
        """
        # TODO: 設定から画面表示を切り替えられるようにしておく

        if platform.system() == 'Windows':
            cmd = ["java", "-cp", "FightingICE.jar;./lib/lwjgl/*;./lib/natives/windows/*;./lib/*",
                   "Main", "--disable-window", "--py4j", "--mute", "--port", "4242"]
        elif platform.system() == 'Darwin':
            cmd = ["java", "-XstartOnFirstThread", "-cp", "FightingICE.jar:./lib/lwjgl/*:./lib/natives/macos/*:./lib/*",
                   "Main", "--disable-window", "--py4j", "--mute", "--port", "4242"]
        else:
            cmd = ["java", "-cp", "FightingICE.jar:./lib/lwjgl/*:./lib/natives/linux/*:./lib/*",
                   "Main", "--disable-window", "--py4j", "--mute", "--port", "4242"]
        self.__java_process = subprocess.Popen(cmd)

        time.sleep(3)

    def __start_game(self) -> None:
        """試合を行う
        起動しているFightingICEとpy4jを用いて接続を行う
        接続に成功したら試合を開始する

        TODO: Python側のAIを読み込めるようにしておく
        """

        # TODO: envから設定出来るようにしておく
        port = 4242
        self.__gateway = JavaGateway(gateway_parameters=GatewayParameters(
            port=port), callback_server_parameters=CallbackServerParameters(port=0))
        real_callback_port = self.__gateway.get_callback_server().get_listening_port()
        self.__gateway.java_gateway_server.resetCallbackClient(
            self.__gateway.java_gateway_server.getCallbackClient().getAddress(), real_callback_port)

        manager = self.__gateway.entry_point
        game = manager.createGame(self.__config.self_player_char, self.__config.opp_player_char,
                                  self.__config.self_player_name, self.__config.opp_player_name, 1)

        try:
            manager.runGame(game)
        except:
            # FIXME: 失敗したという内容は握り潰したくない
            self.__exit_cnt += 1

    def __close_game(self) -> None:
        self.__gateway.close_callback_server()
        self.__gateway.close()
        del self.__gateway

    def __close_java_process(self) -> None:
        self.__java_process.kill()
        del self.__java_process

    def train(self) -> None:

        self.__start_java_process()
        cnt = 0

        while not cnt - self.__exit_cnt >= self.__config.episode:
            cnt += 1
            send_message(self.__config, "{}回目の学習を行います.".format(
                cnt - self.__exit_cnt), True)
            self.__start_game()
            try:
                self.__close_game()
                self.__close_java_process()
                if not cnt - self.__exit_cnt >= self.__config.episode:
                    self.__start_java_process()
            except:
                raise SystemExit("ゲームの再起動に失敗しました")


if __name__ == "__main__":
    import os
    config = Config()
    os.chdir(config.env_dir)

    trainer = GameExecutor(config)
    trainer.train()
