from dotenv import load_dotenv
import os


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

    def __init__(self) -> None:

        if not os.path.exists(".env"):
            raise FileNotFoundError(".envファイルが見つかりません. 作成してください.")

        load_dotenv()

        self.env_dir = os.getenv("ENV_DIR")

        self.self_player_name = os.getenv("SELF_PLAYER_NAME")
        self.opp_player_name = os.getenv("OPP_PLAYER_NAME")

        self.self_player_char = os.getenv("SELF_PLAYER_CHAR")
        self.opp_player_char = os.getenv("OPP_PLAYER_CHAR")

        self.episode = (int)(os.getenv("EPISODE"))
