import json
import math
import pypinyin
import re

"""
init_prob.json: 初始概率矩阵

emiss_prob.json: 发射概率矩阵

trans_prob.json: 转移概率矩阵

pinyin_state: 存储同一个拼音的多个汉字，供计算时遍历使用
"""


def load():
    chinese = re.compile(r'[\u4e00-\u9fa5]{2,}')
    with open('../data/mer.txt', 'r', encoding='utf-8') as f:
        chi = chinese.findall(f.read())
    return chi


def count_init(seqs1):
    init_prob = {}
    num = 0
    len_ = len(seqs1)

    for seq in seqs1:
        num += 1
        if not num % 10000:
            print('{}/{}'.format(num, len_))
        if len(seq) == 0:
            continue

        init_prob[seq[0]] = init_prob.get(seq[0], 0) + 1

    for key in init_prob.keys():
        init_prob[key] = math.log(init_prob.get(key) / len(seqs1))

    save('init_prob', init_prob)


def count_trans(seqs2):
    trans_prob = {}
    num = 0  # counter of sequences

    for seq in seqs2:
        num += 1
        if len(seq) == 0:
            continue
        seq = [w for w in seq]

        seq.insert(0, 'BOS')
        seq.append('EOS')

        for index, post in enumerate(seq):
            if index:
                pre = seq[index - 1]
                if not trans_prob.get(post, None):
                    trans_prob[post] = {}
                trans_prob[post][pre] = trans_prob[post].get(pre, 0) + 1

    for word in trans_prob.keys():
        total = sum(trans_prob.get(word).values())
        for pre in trans_prob.get(word).keys():
            trans_prob[word][pre] = math.log(trans_prob[word].get(pre) / total)

    save('trans_prob', trans_prob)


def count_emission(seqs3):
    emiss_prob = {}
    num = 0  # counter of sequences
    len_ = len(seqs3)

    for seq in seqs3:
        num += 1
        if not num % 10000:
            print('{}/{}'.format(num, len_))
        if len(seq) == 0:
            continue

        pinyin = pypinyin.lazy_pinyin(seq)

        for py, word in zip(pinyin, seq):
            if not emiss_prob.get(word, None):
                emiss_prob[word] = {}
            emiss_prob[word][py] = emiss_prob[word].get(py, 0) + 1

    # use log to normalize the observation probability
    for word in emiss_prob.keys():
        total = sum(emiss_prob.get(word).values())
        for key in emiss_prob.get(word):
            emiss_prob[word][key] = math.log(emiss_prob[word][key] / total)

    save('emiss_prob', emiss_prob)


def count_pinyin_states():
    with open('emiss_prob.json') as f:
        emiss_prob = json.load(f)

    data = {}
    for key in emiss_prob.keys():
        for pinyin in emiss_prob.get(key):
            if not data.get(pinyin, None):
                data[pinyin] = []
            data[pinyin].append(key)

    with open('pinyin_states.json', 'w') as f:
        json.dump(data, f)


def save(filename, data):
    with open(filename + '.json', 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    seqs = load()
    count_init(seqs)
    count_emission(seqs)
    count_trans(seqs)
    count_pinyin_states()
