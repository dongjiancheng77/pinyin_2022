import json
from itertools import combinations


def split_pinyin(pinyin, intact_pinyin_set, all_pinyin_set):
    """
    话说学了一周根本想不到动态规划是干这个的
    """
    # 用于保存动态规划答案的字典
    intact_cut_pinyin_ans = {}
    all_cut_pinyin_ans = {}

    # 动态规划判断进行拼音划分
    def cut_pinyin(str1: str, is_intact=False, is_break=True):
        """
        进行拼音划分, 返回拼音划分结果列表
        str1: 无空格字符串
        """
        if is_intact:
            pinyin_set = intact_pinyin_set
            ans_dict = intact_cut_pinyin_ans
        else:
            pinyin_set = all_pinyin_set
            ans_dict = all_cut_pinyin_ans
        if str1 in ans_dict:
            return ans_dict[str1]
        if is_break and '\'' in str1:
            pinyins = str1.split('\'')
            components = [cut_pinyin(p, is_intact, False) for p in pinyins]
            an1 = components[0]
            for i in range(1, len(components)):
                an1 = [p1 + p2 for p1 in an1 for p2 in components[i]]
            return an1
        # 动态规划生成
        an2 = [] if str1 not in pinyin_set else [(str1,)]
        for i in range(1, len(str1)):
            if str1[:i] in pinyin_set:
                appendices = cut_pinyin(str1[i:], is_intact, is_break=False)
                for appendix in appendices:
                    an2.append((str1[:i],) + appendix)
        ans_dict[str1] = an2
        return an2

    def cut_error(str2):
        an3 = {}
        for i in range(1, len(str2) - 1):
            # 避免交换分词符
            if str2[i - 1] == '\'' or str2[i] == '\'' or str2[i + 1] == '\'':
                continue
            key = str2[:i] + str2[i + 1] + str2[i] + str2[i + 2:]
            value = cut_pinyin(key, is_intact=True)
            if value:
                an3[key] = value
        an3['all'] = [p for t in an3.values() for p in t]
        return an3

    '''
    纠错划分
    模糊划分
    '''
    ans = {
        'intact': cut_pinyin(pinyin, is_intact=True),
        'error_correction': cut_error(pinyin)['all'],
        'fuzzy': cut_pinyin(pinyin, is_intact=False)
    }

    if ans['intact']:
        return ans['intact']
    if ans['error_correction']:
        return ans['error_correction']
    sm = 'b,p,m,f,d,t,n,l,g,k,h,z,c,s,zh,ch,sh,y,w'.split(',')
    ym = 'r,j,q,x'.split(',')
    an = ans['fuzzy']
    anl = []
    for x in an:
        anl.append(list(x))
    for x in anl:
        for y in range(len(x)):
            if x[y] in sm:
                x[y] += 'a'
            if x[y] in ym:
                x[y] += 'i'

    return anl


def take_second_first(elem):
    return elem[1][0]


def take_first(elem):
    return elem[0]


def read(filename):
    with open('params/' + filename + '.json', 'r') as f:
        return json.load(f)


class HMM:
    def __init__(self):

        """
        加载参数
        pinyin_states: 同音字
        """
        self.min_f = -3.14e+100  # viterbi算法实现时为了防止出现精度爆炸现象，所以对每个概率都做了log平滑，且将乘法转换为加法防止数位溢出
        self.init_prob = read('init_prob')
        self.emiss_prob = read('emiss_prob')
        self.trans_prob = read('trans_prob')
        self.pinyin_states = read('pinyin_states')
        self.pyList = []
        self.intact_pinyin_set = set()
        with open('data/pinyin.txt', 'r', encoding='utf-8') as f:
            self.intact_pinyin_set = set(s for s in f.read().split('\n'))

        # 生成带残缺部分的拼音, 例如 'ruan' 对应的 'r', 'ru' 和 'rua', 共 504 个, 对应的拼音表为 data/all_pinyin.txt
        self.all_pinyin_set = set(s[:i] for s in self.intact_pinyin_set for i in range(1, len(s) + 1))

    def trans(self, strs):
        seq = split_pinyin(strs, self.intact_pinyin_set, self.all_pinyin_set)
        res = []

        for n in range(len(seq)):
            length = len(seq[n])
            viterbi = {}
            for i in range(length):
                viterbi[i] = {}

            for s in self.pinyin_states.get(seq[n][0]):
                viterbi[0][s] = (self.init_prob.get(s, self.min_f) +
                                 self.emiss_prob.get(s, {}).get(seq[n][0], self.min_f), -1)

            # P[i+1][s] = max(P[i][pre]P(s|pre)P(seq[n][i+1]|s))
            for i in range(length - 1):
                for s in self.pinyin_states.get(seq[n][i + 1]):
                    viterbi[i + 1][s] = max(
                        [(viterbi[i][pre][0] + self.emiss_prob.get(s, {}).get(seq[n][i + 1], self.min_f)
                          + self.trans_prob.get(s, {}).get(pre, self.min_f), pre) for pre in
                         self.pinyin_states.get(seq[n][i])])

            # P[length - 1][s] = P[length - 1][s]*P(EOS|s)
            for s in self.pinyin_states.get(seq[n][-1]):
                viterbi[length - 1][s] = (viterbi[length - 1][s][0] + self.trans_prob.get('EOS', {}).get(s, self.min_f),
                                          viterbi[length - 1][s][1])

            words_list = [x for x in viterbi[length - 1].items()]
            words_list.sort(key=take_second_first, reverse=True)
            for i in range(min(len(words_list), 100)):
                words = [None] * length
                words[-1] = words_list[i][0]

                for x in range(length - 2, -1, -1):
                    words[x] = viterbi[x + 1][words[x + 1]][1]

                res.append((i, ''.join(w for w in words)))
        res = list(set(res))
        res.sort(key=take_first)
        return [x[1] for x in res]
