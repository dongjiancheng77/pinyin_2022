import random
import tensorflow as tf
from tensorflow.keras import optimizers
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow import keras
import numpy as np

import jieba  # 使用 jieba 做中文分词
import os

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

# 导入文本

path = 'data/article/4.txt'
text = open(path, 'r', encoding='utf-8').read().lower()
print('Corpus length:', len(text))

# 将文本序列向量化

maxlen = 60  # 每个序列的长度
step = 3  # 每 3 个 token 采样一个新序列
sentences = []  # 保存所提取的序列
next_tokens = []  # sentences 的下一个 token

token_text = list(jieba.cut(text))

tokens = list(set(token_text))
tokens_indices = {token: tokens.index(token) for token in tokens}
print('Number of tokens:', len(tokens))

for i in range(0, len(token_text) - maxlen, step):
    sentences.append(
        list(map(lambda t: tokens_indices[t], token_text[i: i + maxlen])))
    next_tokens.append(tokens_indices[token_text[i + maxlen]])
print('Number of sequences:', len(sentences))

# 将目标 one-hot 编码
next_tokens_one_hot = []
for i in next_tokens:
    y = np.zeros((len(tokens),), dtype=np.bool)
    y[i] = 1
    next_tokens_one_hot.append(y)

# 做成数据集
dataset = tf.data.Dataset.from_tensor_slices((sentences, next_tokens_one_hot))
dataset = dataset.shuffle(buffer_size=4096)
dataset = dataset.batch(128)
dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

# 构建、编译模型

model = models.Sequential([
    layers.Embedding(len(tokens), 256),
    layers.LSTM(256),
    layers.Dense(len(tokens), activation='softmax')
])

optimizer = optimizers.RMSprop(lr=0.1)
model.compile(loss='categorical_crossentropy',
              optimizer=optimizer)


# 采样函数

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


# 训练模型

callbacks_list = [
    keras.callbacks.ModelCheckpoint(  # 在每轮完成后保存权重
        filepath='text_gen.h5',
        monitor='loss',
        save_best_only=True,
    ),
    keras.callbacks.ReduceLROnPlateau(  # 不再改善时降低学习率
        monitor='loss',
        factor=0.5,
        patience=1,
    ),
    keras.callbacks.EarlyStopping(  # 不再改善时中断训练
        monitor='loss',
        patience=3,
    ),
]

model.fit(dataset, epochs=30, callbacks=callbacks_list)

# 文本生成

start_index = random.randint(0, len(text) - maxlen - 1)
generated_text = text[start_index: start_index + maxlen]
print(f' 📖 Generating with seed: "{generated_text}"')

for temperature in [0.2, 0.5, 1.0, 1.2]:
    print('\n  temperature:', temperature)
    print(generated_text, end='')
    for _ in range(100):  # 生成 100 个 token
        # 编码当前文本
        text_cut = jieba.cut(generated_text)
        sampled = []
        for i in text_cut:
            if i in tokens_indices:
                sampled.append(tokens_indices[i])
            else:
                sampled.append(0)

        # 预测，采样，生成下一个 token
        preds = model.predict(sampled, verbose=0)[0]
        next_index = sample(preds, temperature)
        next_token = tokens[next_index]
        print(next_token, end='')

        generated_text = generated_text[1:] + next_token
model.save('new_model.h5')
del model
