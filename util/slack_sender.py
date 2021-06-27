from slack_sdk.webhook import WebhookClient

from config import Config


def send_message(config: Config, msg: str, is_logged: bool) -> None:
    """指定されたチャンネルにメッセージを送信する

    Args:
        config (Config): Slack APIのキーなどの設定
        msg (str): 送信しない内容
        is_logged (bool): logかどうか
    """

    if is_logged:
        webhook = WebhookClient(config.slack_log_webhook)
    else:
        webhook = WebhookClient(config.slack_result_webhook)

    response = webhook.send(text=msg)


if __name__ == "__main__":
    config = Config()
    send_message(config, "test", False)
