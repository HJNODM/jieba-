import pandas as pd
import numpy
import json
import os


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


def find_key_word(csv_name, key_word, tag):
    """
    关键词匹配
    :param csv_name: 读取文件名
    :param key_word: 关键词
    :param tag: 包含还是不包含
    :return:关键词，数量
    """
    ans_sex = []
    num_sex = 0
    for it in csv_name:
        df = pd.read_csv(os.path.join(path, it))
        data = list(df['关键词提取'])
        num = list(df['数量'])
        for j in range(len(data)):
            jj = eval(data[j])
            if tag:
                for i in key_word:
                    if i in jj and '维修' not in jj:  # 一个特殊点(维修)，将其去掉
                        ans_sex += jj
                        num_sex += num[j]
                        break
            if not tag:
                ad = True
                for i in key_word:
                    if i in jj:
                        ad = False
                        break
                if ad:
                    ans_sex += jj
                    num_sex += num[j]
    return ans_sex, num_sex


def to_json(data, json_name):
    dic = {}
    for it in data:
        if it in dic:
            dic[it] += 1
        else:
            dic[it] = 1

    dic = sorted(dic.items(), key=lambda x: x[1], reverse=True)[:20]
    ans = []
    for it in dic:
        di = {"text": "{}".format(it[0]), "size": "{}".format(it[1])}
        ans.append(di)
    b = json.dumps(ans,ensure_ascii=False)
    with open('{}.json'.format(json_name), 'w', encoding='utf-8') as f:
        f.write(b)


if __name__ == '__main__':
    path = 'data_processed'
    csv_name = file_name(path)
    l_sex, n_sex = find_key_word(csv_name, ['上门服务', '空姐', '少妇', '模特'], True)
    l_money, n_money = find_key_word(csv_name, ['建设银行', '工商银行', '农业银行', '信用卡', '我行', '发票', '还款'], True)
    l_gamble, n_gamble = find_key_word(csv_name, ['澳门', '百家乐', '葡京', '投注'], True)
    l_trash, n_trash = find_key_word(csv_name,
                                     ['上门服务', '空姐', '少妇', '建设银行', '工商银行', '农业银行', '信用卡', '我行',
                                      '发票', '还款','模特',
                                      '澳门', '百家乐', '葡京', '投注'],
                                     False)
    to_json(l_sex, 'sex.json')
    to_json(l_money, 'money.json')
    to_json(l_gamble, 'gamble.json')
    to_json(l_trash, 'trash.json')

