import MeCab
import markovify


def main():

    mecab = MeCab.Tagger("-Owakati")

    # 上手く解釈できない文字列を定義しておく
    breaking_chars = ['(', ')', '[', ']', '"', "'","！"]
    # 最終的に1文に収めるための変数
    splitted_meigen = ''

    with open("test.txt","r",encoding="utf-16") as f:
        for line in f:
            print('Line : ', line)
            # lineの文字列をパースする
            parsed_nodes = mecab.parseToNode(line)

            while parsed_nodes:
                try:
                    # 上手く解釈できない文字列は飛ばす
                    if parsed_nodes.surface not in breaking_chars:
                        splitted_meigen += parsed_nodes.surface
                    # 句読点以外であればスペースを付与して分かち書きをする
                    if parsed_nodes.surface != '。' and parsed_nodes.surface != '、':
                        splitted_meigen += ' '
                    # 句点が出てきたら文章の終わりと判断して改行を付与する
                    if parsed_nodes.surface == '。':
                        splitted_meigen += '\n'
                except UnicodeDecodeError as error:
                    print('Error : ', line)
                finally:
                    # 次の形態素に上書きする。なければNoneが入る
                    parsed_nodes = parsed_nodes.next

    print('解析結果 :\n', splitted_meigen)

    # マルコフ連鎖のモデルを作成
    model = markovify.NewlineText(splitted_meigen, state_size=2)

    # 文章を生成する
    sentence = model.make_sentence(tries=100)
    if sentence is not None:
        # 分かち書きされているのを結合して出力する
        print('---------------------------------------------------')
        print(''.join(sentence.split()))

    else:
        print('None')


if __name__ == "__main__":
    main()