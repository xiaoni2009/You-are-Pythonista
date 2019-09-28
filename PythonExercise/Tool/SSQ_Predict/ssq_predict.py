from collections import Counter

# 画图工具-单数组的概率密度分布
# 原始画图工具，可以自己指定x,y
import matplotlib.pyplot as plt
# 数学工具
import numpy as np
import requests
from bs4 import BeautifulSoup

latest_red_right = ["04", "12", "14", "21", "27", "29"]
latest_blue_right = ["12"]


def get_reward(key, times):
    x = 0
    if key == "00":
        x = 0
    elif key == "21" or key == "11" or key == "01":
        x = 5 * times
    elif key == "40" or key == "31":
        x = 10 * times
    elif key == "50" or key == "41":
        x = 200 * times
    elif key == "51":
        x = 3000 * times
    elif key == "60":
        x = 50000 * times
    elif key == "61":
        x = 5000000 * times
    else:
        x = 0
    return x


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
    # filename = 'ssq.txt'  # txt文件和当前脚本在同一目录下，所以不用写具体路径
    filename = 'ssq_test.txt'  # txt文件和当前脚本在同一目录下，所以不用写具体路径
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
    # is_win(red1, blue1, latest_red_right, latest_blue_right)
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
    total_reword = is_win(np.append(red1, red2), np.append(blue1, blue2), latest_red_right, latest_blue_right)
    print('------------------------------------------------------------------------------')
    # 按照数字(非次数)升序排序
    total_red = len(red_num)
    total_blue = len(blue_num)
    red_sorted = sorted(red_count.items(), key=lambda x: x[0], reverse=False)
    blue_sorted = sorted(blue_count.items(), key=lambda x: x[0], reverse=False)
    # 计算归一化总概率
    x_red = list(map(lambda x: "r" + x[0], red_sorted))
    x_blue = list(map(lambda x: "b" + x[0], blue_sorted))
    red_rate = list(map(lambda x: x[1] * 100 / total_red, red_sorted))
    blue_rate = list(map(lambda x: x[1] * 100 / total_blue, blue_sorted))
    print(red_rate)
    print(blue_rate)

    # =================================================
    # 只能纯数字-画绘制核密度估计（KDE）KDE（Kernel density estimation）是核密度估计的意思，它用来估计随机变量的概率密度函数，可以将数据变得更平缓。
    # sns.set_style('darkgrid')
    # sns.distplot(red_rate)
    # sns.distplot(blue_rate)

    # =================================================
    #  matplotlib.axes.Axes.hist() 方法的接口，直方图是用面积表示各组频数的多少，矩形的高度表示每一组的频数或频率，宽度则表示各组的组距，因此其高度与宽度均有意义。
    # n, bins, patches = plt.hist(x=red_num, bins='auto', color='#0504aa',
    #                             alpha=0.7, rwidth=0.85)
    # plt.grid(axis='y', alpha=0.75)
    # plt.xlabel('Value')
    # plt.ylabel('Frequency')
    # plt.title('My Very Own Histogram')
    # plt.text(23, 45, r'$\mu=15, b=3$')
    # maxfreq = n.max()
    # # 设置y轴的上限
    # plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)

    # draw_bar_pic(np.append(x_red, x_blue),np.append(red_rate, blue_rate),'number','rate','predict','graph 1' )
    return red_rate, blue_rate, x_red, x_blue, total_reword


def predict_latest(red1s, red2s, red3s, red4s, red5s, red6s, blue1s, latest_term_num):
    red_latest = np.append(red1s[0:latest_term_num], red2s[0:latest_term_num])
    red_latest = np.append(red_latest, red3s[0:latest_term_num])
    red_latest = np.append(red_latest, red4s[0:latest_term_num])
    red_latest = np.append(red_latest, red5s[0:latest_term_num])
    red_latest = np.append(red_latest, red6s[0:latest_term_num])
    blue_latest = blue1s[0:latest_term_num]
    return predict(red_latest, blue_latest)


def predic_latest_total_diffs(red_latest_rate, red_total_rate,blue_latest_rate, blue_total_rate,x_red, x_blue):
    print("====================")
    red_diffs = variance(red_latest_rate, red_total_rate)
    blue_diffs = variance(blue_latest_rate, blue_total_rate)
    # print(red_diffs)
    # print(blue_diffs)
    draw_bar_pic(np.append(x_red, x_blue), np.append(red_diffs, blue_diffs), 'number', 'rate', 'variance', 'graph 3')

    print("====================")
    # keys = [1,2,3]
    # values = ["a","b","c"]
    # max_n_dict(keys, values, 1)
    max_n_red_keys, max_n_red_values = max_or_min_n_dict(x_red, red_diffs, 6, True)
    min_n_red_keys, min_n_red_values = max_or_min_n_dict(x_red, red_diffs, 6, False)
    print("====================")
    max_n_blue_keys, max_n_blue_values = max_or_min_n_dict(x_blue, blue_diffs, 3, True)
    min_n_blue_keys, min_n_blue_values = max_or_min_n_dict(x_blue, blue_diffs, 3, False)

    # is_win(["01","23","08","18"],["15","02"],["01","23"],["02"])
    diff_reward = is_win(np.append(max_n_red_keys, min_n_red_keys), np.append(max_n_blue_keys, min_n_blue_keys),
                         add_prefix(latest_red_right, "r"), add_prefix(latest_blue_right, "b"))
    return red_diffs, blue_diffs, x_red, x_blue, diff_reward


# get pic
def draw_bar_pic(x, y, x_title, y_title, title, label_name):
    print("====================")
    # 画条形图：条形图是用条形的长度表示各类别频数的多少，其宽度（表示类别）则是固定的；
    plt.bar(x, y, label=label_name)
    plt.legend()
    plt.xlabel(x_title)
    plt.ylabel(y_title)
    plt.title(title)
    plt.show()


# 比较数组每个元素之间的方差
def variance(source, target):
    diffs = []
    for index, source_element in enumerate(source):
        target_element = target[index]
        diffs.append(source_element - target_element)
        pass
    return diffs


# get maximum or minimum n number key-value
# if_reverse = True, maximum; if_reverse = False, minimum
def max_or_min_n_dict(keys, values, n, if_reverse):
    data_map = {}
    for index in range(len(keys)):
        data_map[keys[index]] = values[index]
        pass
    # print(data_map)
    # reverse sort
    data_sorted = sorted(data_map.items(), key=lambda x: x[1], reverse=if_reverse)
    keys_sorted = list(map(lambda x: x[0], data_sorted))
    values_sorted = list(map(lambda x: x[1], data_sorted))
    keys_n = keys_sorted[0:n]
    values_n = values_sorted[0:n]
    print(keys_n)
    # print(values_n)
    # draw_bar_pic(keys_n,values_n,'key','value','max_n_dic' if if_reverse else 'min_n_dic','graph 4')
    return keys_n, values_n


def is_win(current_red, current_blue, correct_red, correct_blue):
    blue_right = 0
    red_right = 0
    for i in correct_blue:
        if i in current_blue:
            blue_right += 1
            pass
    for i in correct_red:
        if i in current_red:
            red_right += 1
        pass
    print(red_right)
    print(blue_right)
    print(get_reward(str(red_right) + str(blue_right), 1))
    pass


def add_prefix(list_data, prefix_str):
    b = []
    for ele in list_data:
        ele = prefix_str + ele
        b.append(ele)
    return b

def predict_and_compare(dates, terms, red1s, red2s, red3s, red4s, red5s, red6s, reds, blue1s):
    red_num = np.append(red1s, red2s)
    red_num = np.append(red_num, red3s)
    red_num = np.append(red_num, red4s)
    red_num = np.append(red_num, red5s)
    red_num = np.append(red_num, red6s)
    blue_num = blue1s
    # 分析数据并预测未来的开奖信息
    # 分析总概率分布-作为标准
    red_total_rate, blue_total_rate, x_red, x_blue, total_reward = predict(red_num, blue_num)
    print(red_total_rate)
    print(blue_total_rate)
    # 分析最近100期的概率分布-作为现实，计算离标准的期望
    latest_term_num = 100
    red_latest_rate, blue_latest_rate, x_red1, x_blue1, latest_reward = predict_latest(red1s, red2s, red3s, red4s,
                                                                                       red5s,
                                                                                       red6s, blue1s, latest_term_num)

    red_diffs, blue_diffs, x_red2, x_blue2, diff_reward = predic_latest_total_diffs(red_latest_rate, red_total_rate,
                                                                                    blue_latest_rate, blue_total_rate,
                                                                                    x_red, x_blue)

if __name__ == '__main__':
    # 定义两个变量, 用于记录历史开奖信息中的红球、蓝球号码信息
    # red_num = []
    # blue_num = []
    # 调用函数，用于获取并解析开奖的数据
    # pparser()

    dates, terms, red1s, red2s, red3s, red4s, red5s, red6s, reds, blue1s = read_file()
    red_num = np.append(red1s, red2s)
    red_num = np.append(red_num, red3s)
    red_num = np.append(red_num, red4s)
    red_num = np.append(red_num, red5s)
    red_num = np.append(red_num, red6s)
    blue_num = blue1s
    # 分析数据并预测未来的开奖信息
    # 分析总概率分布-作为标准
    red_total_rate, blue_total_rate, x_red, x_blue, total_reward = predict(red_num, blue_num)
    print(red_total_rate)
    print(blue_total_rate)
    # 分析最近100期的概率分布-作为现实，计算离标准的期望
    latest_term_num = 100
    red_latest_rate, blue_latest_rate, x_red1, x_blue1, latest_reward = predict_latest(red1s, red2s, red3s, red4s, red5s,
                                                                                     red6s, blue1s, latest_term_num)

    red_diffs, blue_diffs, x_red2, x_blue2, diff_reward = predic_latest_total_diffs(red_latest_rate, red_total_rate, blue_latest_rate, blue_total_rate, x_red, x_blue)