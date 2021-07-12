from dotenv import load_dotenv
import os

from util import DotenvKeyNotFoundError


class Config:
    """学習設定を管理する
    .envから設定を取得する
    """

    # 実行環境のパス
    env_dir: str

    # 自分のAI名
    self_player_name: str
    # 相手のAI名
    opp_player_name: str

    # 自分のキャラ
    self_player_char: str
    # 相手のキャラ
    opp_player_char: str

    # 試行回数
    episode: int

    # 評価を行う際の試行回数
    # 各エピソードをこの変数回分試してみて平均値などを計算するイメージ
    evaluate_num: int

    # slackのwebhook
    slack_result_webhook: str
    slack_log_webhook: str

    def __init__(self) -> None:

        if not os.path.exists(".env"):
            raise FileNotFoundError(".envファイルが見つかりません. 作成してください.")

        load_dotenv()

        self.env_dir = self.get_param_from_env("ENV_DIR")

        self.self_player_name = self.get_param_from_env("SELF_PLAYER_NAME")
        self.opp_player_name = self.get_param_from_env("OPP_PLAYER_NAME")

        self.self_player_char = self.get_param_from_env("SELF_PLAYER_CHAR")
        self.opp_player_char = self.get_param_from_env("OPP_PLAYER_CHAR")

        self.episode = int(self.get_param_from_env("EPISODE"))

        self.evaluate_num = int(self.get_param_from_env("EVALUATE_NUM"))

        self.slack_result_webhook = self.get_param_from_env(
            "SLACK_API_RESULT_WEBHOOK_URL")
        self.slack_log_webhook = self.get_param_from_env(
            "SLACK_API_LOG_WEBHOOK_URL")

    @staticmethod
    def get_param_from_env(key: str) -> str:
        """.envファイルから情報を抽出する

        Args:
            key (str): 抽出したい.envのキー

        Raises:

        Returns:
            str: 抽出した情報
        """

        param = os.getenv(key)

        if param is None:
            raise DotenvKeyNotFoundError(
                ".envファイルに[{}]に対する値が設定されていません".format(key))
        else:
            return param
