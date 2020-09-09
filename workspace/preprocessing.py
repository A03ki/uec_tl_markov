import argparse
import MeCab
from typing import List

from uectl.text_filter import dump_text, format_text


def dump_specific_text(text: str) -> str:
    "学習の邪魔になりそうな文字列のとき, 空文字を返す"
    ng_words = ["#匿名質問募集中", "のポスト数：", "ツイート数:", "前日比:", "#本田とじゃんけん",
                "Twitter家族:", "#NowPlaying", "I'm at", "事前登録",
                "人からブロックされています", "ツイ廃結果", "Twitter歴"]
    for ng_word in ng_words:
        text = dump_text(text, ng_word)
        if text == "":
            break
    return text


def preprocessing(lines: List[str]) -> List[str]:
    """各要素の文字列に対して前処理を行なった結果を返す

    Note:
        前処理した要素が空文字の時はその要素を結果に含めないので入力と出力の各要素が対応しないことがある
    """
    m = MeCab.Tagger("-Owakati")
    newlines = [format_text(dump_specific_text(line)) for line in lines]
    newlines = [m.parse(newline) for newline in newlines if newline != ""]
    return newlines


def main(input_filepath: str, output_filepath: str) -> None:
    """ファイルの各行を整えたあと, 分かち書きを行い, 結果をファイルに書き出す

    Note:
        整えた結果が空文字の時はその行を書き出さないので入力と出力ファイルの各行が対応しないことがある
    """
    with open(input_filepath, "r") as f:
        text = f.read()

    lines = text.split("\n")
    newlines = preprocessing(lines)

    with open(output_filepath, "w") as f:
        f.write("".join(newlines))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_filepath", "-i", default="input.txt",
                        type=str, help="テキストのファイルパス")
    parser.add_argument("--output_filepath", "-o", default="output.txt",
                        type=str, help="前処理後のテキストの出力先のファイルパス")
    args = parser.parse_args()
    main(args.input_filepath, args.output_filepath)
