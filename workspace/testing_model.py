import argparse

from uectl.models import MarkovChainModel


def main(input_json_path: str, beginning: str, count: int = 100,
         rejection_origin_text: bool = False) -> None:
    "`count` で指定した回数だけマルコフ連鎖を用いて文字列を生成し, 標準出力する"
    model = MarkovChainModel.load_json(input_json_path)
    for _ in range(count):
        sentence = model.generate_sentence_with_start(beginning=beginning,
                                                      test_output=rejection_origin_text)
        print(sentence)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json_path", "-i", default="model.json",
                        type=str, help="学習済みモデルJSONファイルパス")
    parser.add_argument("--beginning", "-b", type=str, default="___BEGIN__",
                        help="文章を生成し始める文字列(各単語は空白文字で区切る)")
    parser.add_argument("--count", "-c", default=100,
                        type=int, help="文章を生成する回数")
    parser.add_argument("--rejection_origin_text", "-r", action="store_true",
                        help="学習データとほぼ一致する文章を生成しないようにする")
    args = parser.parse_args()
    main(args.input_json_path, args.beginning, count=args.count,
         rejection_origin_text=args.rejection_origin_text)
