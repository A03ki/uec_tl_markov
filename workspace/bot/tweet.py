import logging
import logging.config
import os

import tweepy
import yaml

from uectl.models import MarkovChainModel


def main(keys_and_tokens: dict, input_json_path: str) -> None:
    "学習済みモデルを読み込み, 生成した結果をツイートする"

    logger = logging.getLogger(__name__)

    api_key = keys_and_tokens["api_key"]
    api_secret_key = keys_and_tokens["api_secret_key"]
    access_token = keys_and_tokens["access_token"]
    access_token_secret = keys_and_tokens["access_token_secret"]

    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)

    ng_words = {"あほ", "アホ", "あほしね", "ばか", "バカ", "馬鹿", "死ね", "氏ね",
                "バーカ", "消えろ", "ゴミ", "ごみ", "きもい", "キモい", "キモイ",
                "アスペ", "池沼", "陰キャ", "社不", "クズ", "気持ち悪い", "カス", "爆破",
                "しばく", "しばいた", "うざい", "ウザイ", "ガイジ", "殺す", "コロス"}

    try:
        model = MarkovChainModel.load_json(input_json_path)
    except Exception:
        logger.error(f"モデルの読み込みに失敗しました: path={input_json_path}",
                     exc_info=True)
        return

    try:
        sentence = ""
        while sentence == "":
            sentence = model.generate_sentence(max_chars=140)
            for ng_word in ng_words:
                if ng_word in sentence:
                    logger.info(f"{ng_word}はNGワードです: {sentence}")
                    sentence = ""
    except Exception:
        logger.error("文章の生成に失敗しました", exc_info=True)
        return

    logger.debug(sentence)

    try:
        api.update_status(sentence)
        pass
    except Exception:
        logger.error("ツイートに失敗しました", exc_info=True)


if __name__ == "__main__":
    abs_dir_path = os.path.dirname(os.path.abspath(__file__))
    bot_config_path = os.path.join(abs_dir_path, "bot_config.yml")

    with open(bot_config_path, "r") as f:
        bot_config = yaml.safe_load(f)

    model_path = os.path.join(abs_dir_path, bot_config["model"]["filename"])
    logging_config_path = os.path.join(abs_dir_path,
                                       bot_config["log"]["config"])
    log_dir_path = os.path.join(abs_dir_path, bot_config["log"]["dirname"])
    output_log_path = os.path.join(log_dir_path, bot_config["log"]["filename"])

    os.makedirs(log_dir_path, exist_ok=True)

    with open(logging_config_path, "r") as f:
        logging_config = yaml.safe_load(f)

    logging_config["handlers"]["file_output"]["filename"] = output_log_path
    logging.config.dictConfig(logging_config)

    twitter_keys_and_tokens = bot_config["twitter_api"]

    main(twitter_keys_and_tokens, model_path)
