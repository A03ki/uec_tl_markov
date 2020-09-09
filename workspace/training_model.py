import argparse

from uectl.models import MarkovChainModel


def main(input_filepath: str, output_json_path: str,
         state_size: int = 2) -> None:
    "マルコフ連鎖を用いた生成モデルを学習し, JSON形式で保存する"
    with open(input_filepath) as f:
        training_text = f.read()

    model = MarkovChainModel.train(training_text, state_size=state_size)
    model.compile()
    model.save_json(output_json_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_filepath", "-i", default="input.txt",
                        type=str, help="テキストのファイルパス")
    parser.add_argument("--output_json_path", "-o", default="model.json",
                        type=str, help="モデルの保存先のJSONファイルパス")
    parser.add_argument("--state_size", "-s", default=2,
                        type=int, help="現在から過去までの考慮する状態のサイズ")
    args = parser.parse_args()
    main(args.input_filepath, args.output_json_path)
