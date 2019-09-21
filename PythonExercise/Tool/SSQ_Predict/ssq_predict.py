from collections import Counter

import numpy as np
import requests
from bs4 import BeautifulSoup


def pparser():
    # 发起请求
    basic_url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    response = requests.get(basic_url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    htm = response.text

    # 解析内容
    soup = BeautifulSoup(htm, 'html.parser')
    # 获取页数信息
    page = int(soup.find('p', attrs={"class": "pg"}).find_all('strong')[0].text)

    # url前缀
    url_part = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list'

    # 分页获取每一页的开奖信息
    for i in range(1, page + 1):
        url = url_part + '_' + str(i) + '.html'

        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        context = res.text
        soups = BeautifulSoup(context, 'html.parser')

        if soups.table is None:
            continue
        elif soups.table:
            table_rows = soups.table.find_all('tr')
            for row_num in range(2, len(table_rows) - 1):
                row_tds = table_rows[row_num].find_all('td')
                ems = row_tds[2].find_all('em')
                result = row_tds[0].string + ', ' + row_tds[1].string + ', ' + ems[0].string + ' ' + ems[
                    1].string + ' ' + ems[2].string + ' ' + ems[3].string + ' ' + ems[4].string + ' ' + ems[
                             5].string + ', ' + ems[6].string
                print(result)

                save_to_file(result)

                red_num.append(ems[0].string)  # 红色球1
                red_num.append(ems[1].string)  # 红色球2
                red_num.append(ems[2].string)  # 红色球3
                red_num.append(ems[3].string)  # 红色球4
                red_num.append(ems[4].string)  # 红色球5
                red_num.append(ems[5].string)  # 红色球6
                blue_num.append(ems[6].string)  # 蓝色球
        else:
            continue

    return red_num, blue_num


def save_to_file(content):
    with open('ssq.txt', 'a', encoding='utf-8') as f:
        f.write(content + '\n')


def read_file():
    filename = 'ssq.txt'  # txt文件和当前脚本在同一目录下，所以不用写具体路径
    dates = []
    terms = []
    red_one = []
    red_two = []
    red_three = []
    red_four = []
    red_five = []
    red_six = []
    red_all = []
    blue_one = []
    with open(filename, 'r') as file_to_read:
        while True:
            lines = file_to_read.readline()  # 整行读取数据
            if not lines:
                break
            pass
            print(lines)
            # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            split_lines = lines.split(',')
            print(split_lines)
            date = split_lines[0]
            term = split_lines[1]
            red_nums = split_lines[2]
            # 去处换行符
            red_nums = red_nums.replace("\n", "")
            print(red_nums)
            red_nums_split = red_nums.strip().split(' ')
            print(red_nums_split)
            # 拆分成红球数字
            red1, red2, red3, red4, red5, red6 = [str(i) for i in red_nums_split]
            blue1 = split_lines[3].strip().replace("\n", "")
            # 添加新读取的数据
            dates.append(date)  # 添加新读取的数据
            terms.append(term)
            red_one.append(red1)
            red_two.append(red2)
            red_three.append(red3)
            red_four.append(red4)
            red_five.append(red5)
            red_six.append(red6)
            red_all.append(red1)
            red_all.append(red2)
            red_all.append(red3)
            red_all.append(red4)
            red_all.append(red5)
            red_all.append(red6)
            blue_one.append(blue1)
        pass
        dates = np.array(dates)  # 将数据从list类型转换为array类型。
        terms = np.array(terms)
        red_one = np.array(red_one)
        red_two = np.array(red_two)
        red_three = np.array(red_three)
        red_four = np.array(red_four)
        red_five = np.array(red_five)
        red_six = np.array(red_six)
        red_all = np.array(red_all)
        blue_one = np.array(blue_one)
        pass
    return dates, terms, red_one, red_two, red_three, red_four, red_five, red_six, red_all, blue_one


def predict(red_num, blue_num):
    red_count = Counter(red_num)
    blue_count = Counter(blue_num)
    print(red_count)
    print(blue_count)
    print('------------------------------------------------------------------------------')
    # 按照出现频率倒序
    # python 使用 lambda 来创建匿名函数lambda [arg1 [,arg2,.....argn]]:expression
    red_sorted = sorted(red_count.items(), key=lambda x: x[1], reverse=True)
    blue_sorted = sorted(blue_count.items(), key=lambda x: x[1], reverse=True)
    red = red_sorted[0:6]
    blue = blue_sorted[0:3]

    # map() 会根据提供的函数对指定序列做映射。map(function, iterable, ...)
    red1 = list(map(lambda x: x[0], red))
    blue1 = list(map(lambda x: x[0], blue))
    red1.sort()
    blue1.sort()
    print('号码低频-1注：' + str(red1) + ' | ' + blue1[0])
    print('号码低频-2注：' + str(red1) + ' | ' + blue1[1])
    print('号码低频-3注：' + str(red1) + ' | ' + blue1[2])
    print('------------------------------------------------------------------------------')
    # 按照出现频率顺序
    red_sorted = sorted(red_count.items(), key=lambda x: x[1], reverse=False)
    blue_sorted = sorted(blue_count.items(), key=lambda x: x[1], reverse=False)
    red = red_sorted[0:6]
    blue = blue_sorted[0:3]

    red2 = list(map(lambda x: x[0], red))
    blue2 = list(map(lambda x: x[0], blue))
    red2.sort()
    blue2.sort()
    print('号码高频-1注：' + str(red2) + ' | ' + blue2[0])
    print('号码高频-2注：' + str(red2) + ' | ' + blue2[1])
    print('号码高频-3注：' + str(red2) + ' | ' + blue2[2])
    print('------------------------------------------------------------------------------')
    # 按照数字(非次数)升序排序
    total_red = len(red_num)
    total_blue = len(blue_num)
    red_sorted = sorted(red_count.items(), key=lambda x: x[0], reverse=False)
    blue_sorted = sorted(blue_count.items(), key=lambda x: x[0], reverse=False)
    # 计算归一化概率
    x_red = list(map(lambda x: x[0], red_sorted))
    x_blue = list(map(lambda x: x[0], blue_sorted))
    red_rate = list(map(lambda x: x[1] * 100 / total_red, red_sorted))
    blue_rate = list(map(lambda x: x[1] * 100 / total_blue, blue_sorted))
    print(red_rate)
    print(blue_rate)


if __name__ == '__main__':
    # 定义两个变量, 用于记录历史开奖信息中的红球、蓝球号码信息
    # red_num = []
    # blue_num = []
    # 调用函数，用于获取并解析开奖的数据
    # pparser()

    dates, terms, red1s, red2s, red3s, red4s, red5s, red6s, reds, blue1s = read_file()
    print(dates)
    print(terms)
    print(red1s)
    print(red2s)
    print(red3s)
    print(red4s)
    print(red5s)
    print(red6s)
    print(reds)
    print(blue1s)
    red_num = np.append(red1s, red2s)
    red_num = np.append(red_num, red3s)
    red_num = np.append(red_num, red4s)
    red_num = np.append(red_num, red5s)
    red_num = np.append(red_num, red6s)
    blue_num = blue1s
    # 分析数据并预测未来的开奖信息
    predict(red_num, blue_num)
