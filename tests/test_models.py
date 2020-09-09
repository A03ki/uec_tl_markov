from unittest.mock import call, Mock, mock_open, patch
from uectl.models import MarkovChainModel


class TestMarkovChainModel:
    def test_generate_text(self):
        sentence = "12 3  4 "
        expected = "1234"
        max_chars = 200
        sentences = [None, None, sentence]
        _model = Mock(**{"make_short_sentence.side_effect": sentences})
        model = MarkovChainModel(_model)
        assert model.generate_sentence(max_chars) == expected
        _model.make_short_sentence.assert_has_calls([call(max_chars)])
        _model.make_short_sentence.call_count == len(sentences)

    def test_generate_text_with_start(self):
        sentence = "1  2 34   5"
        expected = "12345"
        beginning = "UEC"
        sentences = [None, None, None, sentence]
        _model = Mock(**{"make_sentence_with_start.side_effect": sentences})
        model = MarkovChainModel(_model)
        assert model.generate_sentence_with_start(beginning) == expected
        _model.make_sentence_with_start.assert_has_calls([call(beginning)])
        _model.make_sentence_with_start.call_count == len(sentences)

    @patch("json.load", return_value="This is JSON!")
    @patch("builtins.open", new_callable=mock_open)
    @patch("markovify.NewlineText.from_json", return_value="json model")
    def test_load_json(self, markovify_NewlineText_from_json, open, json_load):
        path = "test/model.json"
        json_data = json_load.return_value
        model = MarkovChainModel.load_json(path)
        assert isinstance(model, MarkovChainModel)
        assert model.model == markovify_NewlineText_from_json.return_value
        open.assert_called_once_with(path, "r")
        json_load.assert_called_once_with(open())
        markovify_NewlineText_from_json.assert_called_once_with(json_data)

    @patch("json.dump")
    @patch("builtins.open", new_callable=mock_open)
    def test_save_json(self, open, json_dump):
        json_data = "This is JSON!"
        _model = Mock(**{"to_json.return_value": json_data})
        model = MarkovChainModel(_model)
        path = "test/model.json"
        indent = 100
        model.save_json(path, indent=indent)
        open.assert_called_once_with(path, "w")
        json_dump.assert_called_once_with(json_data, open(), indent=indent)

    @patch("markovify.NewlineText", return_value="trained!")
    def test_train(self, markovify_NewlineText):
        training_text = "test test \n"
        state_size = 5
        model = MarkovChainModel.train(training_text, state_size=state_size)
        assert isinstance(model, MarkovChainModel)
        assert model.model == markovify_NewlineText.return_value
        markovify_NewlineText.assert_called_once_with(training_text,
                                                      state_size=state_size)

    def test_compile(self):
        expected = "compile!"
        _model = Mock(**{"compile.return_value": expected})
        model = MarkovChainModel(_model)
        inplace = True
        model.compile(inplace=inplace)
        assert model.model == expected
        _model.compile.assert_called_once_with(inplace=inplace)
