# 各種モジュール
from re import M
import MeCab
import random
from nltk import ngrams
from collections import Counter, defaultdict
# テストデータのわかち書き、加工
def parse_words(test_data):

    # テストデータ読み込み
    with open(test_data, 'r', encoding="utf-16") as f:
        lines = f.readlines()

    # わかち書き
    t = MeCab.Tagger('-Owakati')
    datas = []
    for line in lines:
        data = t.parse(line).strip()
        datas.append(data)

    # 各行の先頭と末尾に目印を付与
    datas = [f'__BEGIN__ {data} __END__' for data in datas]
    datas = [data.split() for data in datas]    

    return datas
# ３単語とその出現回数辞書作成
def create_words_cnt_dic(datas):

    # 行ごとにトライグラム作成し、１つに連結
    words = []
    for data in datas:
        words.extend(list(ngrams(data, 3)))

    # ３単語とその出現回数辞書
    words_cnt_dic = Counter(words)

    return words_cnt_dic    


# マルコフ用辞書
def create_m_dic(words_cnt_dic):

    # 空のマルコフ辞書
    m_dic = {}
    for k, v in words_cnt_dic.items():
        # 先頭２単語、その次の単語
        two_words, next_word = k[:2], k[2]

        # 存在しなければ作る
        if two_words not in m_dic:
            m_dic[two_words] = {'words': [], 'weights': []}

        # 先頭２単語に対し、次に来る単語とその重み
        m_dic[two_words]['words'].append(next_word)
        m_dic[two_words]['weights'].append(v)

    return m_dic    
# 文章開始単語リストとその重みリスト作成
def create_begin_words_weights(words_cnt_dic):

    begin_words_dic = defaultdict(int) 
    for k, v in words_cnt_dic.items():
        if k[0] == '__BEGIN__':
            next_word = k[1]
            begin_words_dic[next_word] = v

    begin_words = [k for k in begin_words_dic.keys()]
    begin_weights = [v for v in begin_words_dic.values()]

    return begin_words, begin_weights
def create_sentences(m_dic, begin_words, begin_weights):
    
    # 開始単語の抽選
    begin_word = random.choices(begin_words, weights=begin_weights, k=1)[0]

    # 作成文章の格納
    sentences = ['__BEGIN__', begin_word]

    # 作成文章の後方２単語をもとに、次の単語を抽選する
    while True:
        # 後方２単語
        back_words = tuple(sentences[-2:])
        # print("back_word",back_words)
        # print("m_dic[back_words]",m_dic[back_words])
        # # マルコフ用辞書から抽選
        words, weights = m_dic[back_words]['words'], m_dic[back_words]['weights']
        next_word = random.choices(words, weights=weights, k=1)[0]

        # 終了の目印が出たら抜ける
        if next_word == '__END__':
            break

        # 取得単語を追加
        sentences.append(next_word)

    # 開始マークより後ろを連結
    return ''.join(sentences[1:])    
# テストデータのわかち書き、加工
datas = parse_words('test.txt')

# ３単語の出現回数辞書作成
words_cnt_dic = create_words_cnt_dic(datas)

# マルコフ用辞書作成
m_dic = create_m_dic(words_cnt_dic)

# 開始単語とその重みリスト作成
begin_words, begin_weights = create_begin_words_weights(words_cnt_dic)

# 20回 文章生成
for i in range(20):
    text = create_sentences(m_dic, begin_words, begin_weights)
    print(str(i).zfill(2), text, sep=': ')