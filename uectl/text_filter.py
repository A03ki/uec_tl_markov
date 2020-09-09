from collections import OrderedDict
import emoji
import html
import neologdn
import pkgutil
import re
from typing import Dict, List, Union
import yaml


def remove_screen_name(text: str) -> str:
    "スクリーンネームを削除した文字列を返す"
    return re.sub(r"@[a-zA-Z0-9_]+", "", text)


def remove_url(text: str) -> str:
    "URLを削除した文字列を返す"
    return re.sub(r'http\S+', "", text)


def remove_hashtag(text: str) -> str:
    "ハッシュタグを削除した文字列を返す"
    return re.sub(r"#\S+", "", text)


def remove_emoji(text: str) -> str:
    "絵文字を削除した文字列を返す"
    return "".join([s for s in text if s not in emoji.UNICODE_EMOJI])


def _remove_brackets_and_quotations(text: str) -> str:
    "半角括弧と半角引用符(+“)を削除した文字列を返す"
    return re.sub(r"[()\[\]\"'“]", "", text)


def dump_text(text: str, word: str) -> str:
    "指定した単語が含まれていたとき, 空文字を返す"
    if word in text:
        return ""
    return text


def replace_words(text: str, words_dict: Dict[str, List[str]]) -> str:
    for new_word, old_words in words_dict.items():
        for old_word in old_words:
            text = text.replace(old_word, new_word)
    return text


def replace_orthographic_variants(text: str,
                                  ymal_path: Union[str, None] = None) -> str:
    "表記ゆれの単語を統一する"
    if ymal_path is None:
        _path = "data/orthographic_variants.yml"
        raw_data = pkgutil.get_data("uectl", _path).decode()
        words_dict = yaml.safe_load(raw_data)
    else:
        with open(ymal_path) as f:
            words_dict = yaml.safe_load(f)

    return replace_words(text,
                         OrderedDict(sorted(words_dict.items())))


def format_text(text: str) -> str:
    "文字列を整えた結果を返す"
    text = remove_screen_name(text)
    text = remove_hashtag(text)
    text = remove_url(text)
    text = html.unescape(text)
    text = text.replace("\\n", "").replace("\n", "")
    text = neologdn.normalize(text, repeat=5)
    text = _remove_brackets_and_quotations(text)
    text = remove_emoji(text)
    text = text.lower()
    text = replace_orthographic_variants(text)
    return text
