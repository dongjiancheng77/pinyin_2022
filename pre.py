import jieba
import numpy as np
from tensorflow.keras.models import load_model


def predict_1(generated_text, temperature):
    def sample(preds1, temperature1=1.0):
        """
        对模型得到的原始概率分布重新加权，并从中抽取一个 token 索引
        """
        preds1 = np.asarray(preds1).astype('float64')
        preds1 = np.log(preds1) / temperature1
        exp_preds = np.exp(preds1)
        preds1 = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds1, 1)
        return np.argmax(probas)

    path = 'data/article/4.txt'
    text = open(path, 'r', encoding='utf-8').read().lower()

    model = load_model('./new_model.h5')
    text_cut = jieba.cut(generated_text)
    sampled = []
    token_text = list(jieba.cut(text))

    tokens = list(set(token_text))
    tokens_indices = {token: tokens.index(token) for token in tokens}
    for i in text_cut:
        if i in tokens_indices:
            sampled.append(tokens_indices[i])
        else:
            sampled.append(0)
    preds = model.predict(sampled, verbose=0)[0]
    next_index = sample(preds, temperature)
    next_token = tokens[next_index]
    return next_token
