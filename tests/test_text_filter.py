import pytest

from uectl.text_filter import (remove_screen_name, remove_url, remove_hashtag,
                               remove_emoji, _remove_brackets_and_quotations,
                               dump_text, replace_words,
                               replace_orthographic_variants, format_text)


def test_remove_screen_name():
    text = "@uec_tl「@puman03@単位が欲しい」"
    expected = "「@単位が欲しい」"
    assert remove_screen_name(text) == expected


def test_remove_url():
    text = "urlはhttps://twitter.com/uec_tlです"
    expected = "urlは"
    assert remove_url(text) == expected

    text2 = "urlはhttps://twitter.com/uec_tl です"
    expected2 = "urlは です"
    assert remove_url(text2) == expected2


def test_remove_hashtag():
    text1 = "楽しみですね#UEC18LT...緊張してきた"
    expected1 = "楽しみですね"
    assert remove_hashtag(text1) == expected1

    text2 = "楽しみですね#UEC18LT ...緊張してきた"
    expected2 = "楽しみですね ...緊張してきた"
    assert remove_hashtag(text2) == expected2


def test_remove_emoji():
    text = "まだスライド作ってないです😇(20/9/9)"
    expected = "まだスライド作ってないです(20/9/9)"
    assert remove_emoji(text) == expected


def test__remove_brackets_and_quotations():
    text = "@[uec_tl]は'マルコフ\"(連鎖)を使っています"
    expected = "@uec_tlはマルコフ連鎖を使っています"
    assert _remove_brackets_and_quotations(text) == expected


@pytest.mark.parametrize(("text", "ng_word", "expected"),
                         [("Hello World!", "world", "Hello World!"),
                          ("Hello World!", "World", "")])
def test_dump_text(text, ng_word, expected):
    assert dump_text(text, ng_word) == expected


def test_replace_words():
    text = "Hello World!"
    expected = "こんにちは 世界!"
    words_dict = {"こんにちは": ["Hello"], "世界": ["World"]}
    assert replace_words(text, words_dict) == expected


def test_replace_orthographic_variants_rui():
    text = "I類とII類とIII類は一類と二類と三類で1類と2類と3類がi類とii類とiii類です"
    expected = "I類とII類とIII類はI類とII類とIII類でI類とII類とIII類がI類とII類とIII類です"
    assert replace_orthographic_variants(text) == expected


def test_replace_orthographic_variants_gpa():
    text = "これらはgpaとGPAです"
    expected = "これらはGPAとGPAです"
    assert replace_orthographic_variants(text) == expected


def test_format_text_brackets_full_characters():
    "全角括弧と全角引用符はnormalize.normalizeで半角に変換し, _remove_brackets_and_quotationsで除去"
    text = "（私は”人間’だ）"
    expected = "私は人間だ"
    assert format_text(text) == expected
