import sys
import MeCab

# ipadic辞書を利用する
# install先は echo `mecab-config --dicdir`"/mecab-ipadic-neologd" コマンドで確認
mt = MeCab.Tagger("-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd")

# 名詞を返す(名詞が連続して並んでいる場合、全て結合して返す)(なければ空文字)
def returnNoun(input_text):
    input = mt.parseToNode(input_text)
    output = ''
    putting = False
    # input_textの品詞をひとつずつ解析、名詞を探す
    while input:
        if input.feature.split(",")[0] in ['名詞']:
            output += input.surface
            putting = True
        elif putting and input.feature.split(",")[0] in ['名詞']:
            output += input.surface
            break
        elif putting and input.feature.split(",")[0] not in ['名詞']:
            break
        input = input.next

    return output

# 固有名詞を返す(なければ空文字)
def returnProperNoun(input_text):
    input = mt.parseToNode(input_text)
    while input:
        # 理解できないアルファベット群は固有名詞の'組織'に分類されるので除外
        if input.feature.split(",")[1] in ['固有名詞'] and input.feature.split(",")[2] not in ['組織']:
            return input.surface
        else:
            input = input.next
    return ''
