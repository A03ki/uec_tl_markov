# UECTL
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/uectl?color=004D80)](https://www.python.org)
[![PyPI Version](https://img.shields.io/pypi/v/uectl?color=B51700)](https://pypi.org/project/uectl/)
[![GitHub LICENSE](https://img.shields.io/github/license/A03ki/uec_tl_markov?color=00AB8E)](https://github.com/A03ki/uec_tl_markov/blob/master/LICENSE)

[@uec_tl](https://twitter.com/uec_tl)に使用するマルコフ連鎖モデルとテキスト処理のためのパッケージです.


## インストール

uectl本体:

```bash
$ pip install uectl
```

uectl本体+前処理用(MeCabが必要):

```bash
$ pip install uectl[preprocessing]
```

## Dockerによる環境構築
マルコフ連鎖で文章を学習させる際, 文章を単語ごとに分ける必要があります.  この単語ごとに区切る処理はMeCabというソフトウェアを使います. MeCabを各OSに応じて導入するのは少し面倒なので, Dockerで環境構築できるようにしました.  ちなみにMeCabが必要なのは前処理の項だけです. uectl本体だけでも, 前処理済みのサンプルファイル`sample_output.txt`を使って, モデルの学習と文章生成を行うことができます.

### セットアップ(初回時)とコンテナの立ち上げ

```bash
$ docker-compose up -d
```
`uec_tl_markov`という名前のイメージと`uec_tl_markov`という名前のコンテナが作成されます.

### コンテナに移動

```bash
$ docker-compose exec app /bin/sh -c "[ -e /bin/bash ] && /bin/bash || /bin/sh"
root@コンテナID:/home/uec_tl_markov#
```


## 前処理

`workspace`ディレクトリに移動した後, `preprocessing.py`を使って, テキストを前処理します.

```bash
$ cd workspace
```

`sample_input.txt`というサンプルファイルがあるので, それを使って試してみます.

```bash
$ cat sample_input.txt
私は電通大が好きです
調布が好きでした
好きな店は食神です
```

```bash
$ python preprocessing.py -i sample_input.txt -o sample_output.txt
```

前処理の結果は`sample_output.txt`に保存しました.

```bash
$ cat sample_output.txt
私 は 電通大 が 好き です 
調布 が 好き でし た 
好き な 店 は 食 神 です 
```

`食 神`以外は予想通りに区切れていますね.


## モデルの学習

次に`sample_output.txt`の各行を学習データとして, N階マルコフ連鎖(N=2)のモデルを作成します.

```bash
$ python training_model.py -i sample_output.txt -o sample_model.json -s 2
```

 学習したモデルは`sample_model.json`として保存しました.

## 文章生成

最後に, 先ほど学習したモデル`sample_model.json`を使って, どのような文章を生成するかを確かめてみます.

```bash
$ python testing_model.py -i sample_model.json -c 5
調布が好きでした
好きな店は食神です
調布が好きでした
好きな店は食神です
私は電通大が好きでした
```

`私は電通大が好きでした`という学習データには存在しない文章の生成を確認できました！

文章を生成し始める単語の指定もできます. 指定する単語数は1からNのいずれかです(今回の例ではN=2). それぞれの単語は空白文字で区切る必要があります.

```bash
$ python testing_model.py -i sample_model.json -c 5 -b "電通大 が"
電通大が好きでした
電通大が好きでした
電通大が好きです
電通大が好きでした
電通大が好きです
```

## UEC18LT会登壇資料

[電通大生の呟きを基に電通大生を錬成してみた](https://drive.google.com/file/d/1ikgyyDTF_J_rWt-zv61FHH-gi1kVQL89/view?usp=sharing)
