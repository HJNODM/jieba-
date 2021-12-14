# -*- coding: utf-8 -*-
import os
import pandas as pd
import jieba
import jieba.analyse as ana


def file_name(file_dir):
    """
    读取数据
    :param file_dir:路径名称
    :return:该路径下的所有文件
    """
    files = None
    for root, dirs, files in os.walk(file_dir):
        pass
    return files


def count_content(df):
    ans = []
    df_d = df.drop_duplicates()
    for i in df_d:
        ans.append(df[df == i].shape[0])
    return df_d, ans


def divide_words(texts):
    """
    jieba对文本进行分词，关键词提取
    :param texts:
    :return:
    """
    remove_text_tags = []
    normal_text_tags = []
    text_list = texts
    for i in range(len(text_list)):
        its = jieba.lcut(text_list[i])  # 正常分词
        its = [it for it in its if it not in ['”', '？', '。', '，', '.', '【', '】', '\n', '-', '：', '、', '/']]
        normal_text_tags.append(its)
        it = ana.extract_tags(text_list[i], topK=10)  # 关键词提取
        remove_text_tags.append(it)
    return normal_text_tags, remove_text_tags


if __name__ == '__main__':
    path = 'data'
    path_2 = 'data_processed'
    csv_name = file_name(path)
    for it in csv_name:
        print(it)
        df = pd.read_csv(os.path.join(path, it))
        df_d, num = count_content(df['content'])
        data = list(df_d)
        a, b = divide_words(data)
        df_t = pd.DataFrame([a, b, num]).T
        df_t.columns = ['正常分词', '关键词提取', '数量']
        print(df_t)
        df_t.to_csv(os.path.join(path_2, it), index=False)
