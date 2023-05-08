

pinyin为源代码，report为报告

1.运行源代码所需要执行的命令

1）程序界面运行main_pinyin.py即可，操作见gui中的按钮。（注意由于要调用tf，故速度较慢）

2）运行data/data_preprocessing.py，处理merge.txt得到mer.txt。

3）运行params_create.py，计算HMM模型所需要的参数，即params下的四个文件

4）运行lstm.py，得到文本生成模型，可以得到使用抽取的样本作为种子在不同temperature下生成的文本


2.环境依赖

pyqt5,pyqt5_tools,numpy,tensorflow,jieba

1）解释器版本为3.8，但是3.10也能跑，主要原因是3.10打不开qt designer。

2）Tensorflow：2.80 CUDA：11.1 cuDNN：8.1.0 RTX3060

需要注意，tensorflow版本和CUDA，cuDNN版本要相互匹配，不然无法训练，与提取。
