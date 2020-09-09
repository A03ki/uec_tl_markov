import json
import markovify


class MarkovChainModel:
    def __init__(self, model: markovify.NewlineText):
        self.model = model

    def generate_sentence(self, max_chars=140, **kwargs) -> str:
        "`max_chars` 以内の文字列を生成する"
        sentence = None
        while sentence is None:
            sentence = self.model.make_short_sentence(max_chars, **kwargs)
        return sentence.replace(" ", "")

    def generate_sentence_with_start(self, beginning: str, **kwargs) -> str:
        "`beginning` で始まる文字列を生成する"
        sentence = None
        while sentence is None:
            sentence = self.model.make_sentence_with_start(beginning, **kwargs)
        return sentence.replace(" ", "")

    @classmethod
    def load_json(cls, path: str) -> "MarkovChainModel":
        "JSON形式で学習済みモデルを読み込んだ後, 新しいクラスのインスタンスオブジェクトを作成して返す"
        with open(path, "r") as f:
            json_data = json.load(f)

        model = markovify.NewlineText.from_json(json_data)
        return cls(model)

    def save_json(self, path: str, indent: int = 4) -> None:
        "モデルをJSON形式で保存する"
        json_data = self.model.to_json()

        with open(path, "w") as f:
            json.dump(json_data, f, indent=indent)

    @classmethod
    def train(cls, training_text: str,
              state_size: int = 2) -> "MarkovChainModel":
        """モデルの学習後, 新しいクラスのインスタンスオブジェクトを作成して返す

        Args:
            training_text: モデルの学習に使用する文字列. 各単語は空白文字で
            区切られている必要があり, 改行ごとに学習する.
            state_size: Optional; 現在から過去までの考慮する状態のサイズ
        """
        model = markovify.NewlineText(training_text, state_size=state_size)
        return cls(model)

    def compile(self, inplace: bool = False) -> None:
        "モデルを軽量化する"
        self.model = self.model.compile(inplace=inplace)
