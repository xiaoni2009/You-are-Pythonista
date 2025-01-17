from collections import Counter

# 画图工具-单数组的概率密度分布
# 原始画图工具，可以自己指定x,y
import matplotlib.pyplot as plt
# 数学工具
import numpy as np
import requests
from bs4 import BeautifulSoup


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
    global red_num, blue_num
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
        red_num = []
        blue_num = []

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
            # 将整行数据分割处理，如果分割符是空格，括号里就不用传入参数，如果是逗号， 则传入‘，'字符。
            split_lines = lines.split(',')
            date = split_lines[0]
            term = split_lines[1]
            red_nums = split_lines[2]
            # 去处换行符
            red_nums = red_nums.replace("\n", "")
            red_nums_split = red_nums.strip().split(' ')
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


def check_num(num, keys, count_data):
    dict_data = dict(count_data)
    if num not in keys:
        dict_data.update({num: 0})
    return dict_data


def predict(red_num, blue_num, correct_red, correct_blue):
    red_count = Counter(red_num)
    blue_count = Counter(blue_num)
    # 有可能某个数字没出现过，为保证长度一致，需要对没出现过的数字的Counter的key进行补全
    red_key_sorted = sorted(red_count.items(), key=lambda x: x[0], reverse=False)
    if len(red_key_sorted) < 33:
        # 对红球补全
        red_keys = list(map(lambda x: x[0], red_count.items()))
        red_count = check_num("01", red_keys, red_count)
        red_count = check_num("02", red_keys, red_count)
        red_count = check_num("03", red_keys, red_count)
        red_count = check_num("04", red_keys, red_count)
        red_count = check_num("05", red_keys, red_count)
        red_count = check_num("06", red_keys, red_count)
        red_count = check_num("07", red_keys, red_count)
        red_count = check_num("08", red_keys, red_count)
        red_count = check_num("09", red_keys, red_count)
        red_count = check_num("10", red_keys, red_count)
        red_count = check_num("11", red_keys, red_count)
        red_count = check_num("12", red_keys, red_count)
        red_count = check_num("13", red_keys, red_count)
        red_count = check_num("14", red_keys, red_count)
        red_count = check_num("15", red_keys, red_count)
        red_count = check_num("16", red_keys, red_count)
        red_count = check_num("17", red_keys, red_count)
        red_count = check_num("18", red_keys, red_count)
        red_count = check_num("19", red_keys, red_count)
        red_count = check_num("20", red_keys, red_count)
        red_count = check_num("21", red_keys, red_count)
        red_count = check_num("22", red_keys, red_count)
        red_count = check_num("23", red_keys, red_count)
        red_count = check_num("24", red_keys, red_count)
        red_count = check_num("25", red_keys, red_count)
        red_count = check_num("26", red_keys, red_count)
        red_count = check_num("27", red_keys, red_count)
        red_count = check_num("28", red_keys, red_count)
        red_count = check_num("29", red_keys, red_count)
        red_count = check_num("30", red_keys, red_count)
        red_count = check_num("31", red_keys, red_count)
        red_count = check_num("32", red_keys, red_count)
        red_count = check_num("33", red_keys, red_count)
        pass
    blue_key_sorted = sorted(blue_count.items(), key=lambda x: x[0], reverse=False)
    if len(blue_key_sorted) < 16:
        # 对篮球补全
        blue_keys = list(map(lambda x: x[0], blue_count.items()))
        blue_count = check_num("01", blue_keys, blue_count)
        blue_count = check_num("02", blue_keys, blue_count)
        blue_count = check_num("03", blue_keys, blue_count)
        blue_count = check_num("04", blue_keys, blue_count)
        blue_count = check_num("05", blue_keys, blue_count)
        blue_count = check_num("06", blue_keys, blue_count)
        blue_count = check_num("07", blue_keys, blue_count)
        blue_count = check_num("08", blue_keys, blue_count)
        blue_count = check_num("09", blue_keys, blue_count)
        blue_count = check_num("10", blue_keys, blue_count)
        blue_count = check_num("11", blue_keys, blue_count)
        blue_count = check_num("12", blue_keys, blue_count)
        blue_count = check_num("13", blue_keys, blue_count)
        blue_count = check_num("14", blue_keys, blue_count)
        blue_count = check_num("15", blue_keys, blue_count)
        blue_count = check_num("16", blue_keys, blue_count)
        pass

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
    predict_reds = np.append(red1, red2)
    predict_blues = np.append(blue1, blue2)
    total_reword = is_win(predict_reds, predict_blues, correct_red, correct_blue)
    print('------------------------------------------------------------------------------')
    # 按照数字(非次数)升序排序
    total_red = len(red_num)
    total_blue = len(blue_num)
    red_sorted = sorted(red_count.items(), key=lambda x: x[0], reverse=False)
    blue_sorted = sorted(blue_count.items(), key=lambda x: x[0], reverse=False)
    # 计算归一化总概率
    x_red = list(map(lambda x: x[0], red_sorted))
    x_blue = list(map(lambda x: x[0], blue_sorted))
    red_rate = list(map(lambda x: x[1] * 100 / total_red, red_sorted))
    blue_rate = list(map(lambda x: x[1] * 100 / total_blue, blue_sorted))

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
    return red_rate, blue_rate, x_red, x_blue, total_reword, predict_reds, predict_blues


def predict_latest(red1s, red2s, red3s, red4s, red5s, red6s, blue1s, latest_term_num, correct_red, correct_blue):
    red_latest = np.append(red1s[0:latest_term_num], red2s[0:latest_term_num])
    red_latest = np.append(red_latest, red3s[0:latest_term_num])
    red_latest = np.append(red_latest, red4s[0:latest_term_num])
    red_latest = np.append(red_latest, red5s[0:latest_term_num])
    red_latest = np.append(red_latest, red6s[0:latest_term_num])
    blue_latest = blue1s[0:latest_term_num]
    return predict(red_latest, blue_latest, correct_red, correct_blue)


def predic_latest_total_diffs(red_latest_rate, red_total_rate, blue_latest_rate, blue_total_rate, x_red, x_blue,
                              correct_red, correct_blue):
    print("====================")
    red_diffs = variance(red_latest_rate, red_total_rate)
    blue_diffs = variance(blue_latest_rate, blue_total_rate)
    # print(red_diffs)
    # print(blue_diffs)
    # draw_bar_pic(np.append(x_red, x_blue), np.append(red_diffs, blue_diffs), 'number', 'rate', 'variance', 'graph 3')

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
    diff_predict_reds = np.append(max_n_red_keys, min_n_red_keys)
    diff_predict_blues = np.append(max_n_blue_keys, min_n_blue_keys)
    diff_reward = is_win(diff_predict_reds, diff_predict_blues,
                         correct_red, correct_blue)
    return red_diffs, blue_diffs, x_red, x_blue, diff_reward, diff_predict_reds, diff_predict_blues


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
        diff = source_element - target_element
        diffs.append(diff.__str__())
        pass
    return diffs


# get maximum or minimum n number key-value
# if_reverse = True, maximum; if_reverse = False, minimum
def max_or_min_n_dict(keys, values, n, if_reverse):
    data_map = {}
    # print("max_or_min_n_dict")
    # print(keys)
    # print(values)
    # print(range(len(keys)))
    for index in range(len(keys)):
        # print(keys[index])
        # print(values[index])
        data_map[keys[index]] = values[index]
        pass
    # print(data_map)
    # reverse sort
    data_sorted = sorted(data_map.items(), key=lambda x: x[1], reverse=if_reverse)
    keys_sorted = list(map(lambda x: x[0], data_sorted))
    values_sorted = list(map(lambda x: x[1], data_sorted))
    keys_n = keys_sorted[0:n]
    values_n = values_sorted[0:n]
    # print(keys_n)
    # print(values_n)
    # draw_bar_pic(keys_n,values_n,'key','value','max_n_dic' if if_reverse else 'min_n_dic','graph 4')
    return keys_n, values_n


def is_win(current_red, current_blue, correct_red, correct_blue):
    blue_right = 0
    red_right = 0
    if correct_red is None or correct_blue is None:
        return 0
    for i in correct_blue:
        if i in current_blue:
            blue_right += 1
            pass
    for i in correct_red:
        if i in current_red:
            red_right += 1
        pass
    reward = get_reward(str(red_right) + str(blue_right), 1)
    pass
    return reward


def add_prefix(list_data, prefix_str):
    b = []
    for ele in list_data:
        ele = prefix_str + ele
        b.append(ele)
    return b


def predict_and_compare(dates, terms, red1s, red2s, red3s, red4s, red5s, red6s, reds, blue1s, correct_red, correct_blue,
                        correct_date, correct_term):

    red_num = np.append(red1s, red2s)
    red_num = np.append(red_num, red3s)
    red_num = np.append(red_num, red4s)
    red_num = np.append(red_num, red5s)
    red_num = np.append(red_num, red6s)
    blue_num = blue1s
    # 分析数据并预测未来的开奖信息
    # 分析总概率分布-作为标准
    red_total_rate, blue_total_rate, x_red, x_blue, total_reward, total_predict_reds, total_predict_blues = predict(
        red_num,
        blue_num,
        correct_red,
        correct_blue)
    # 分析最近100期的概率分布-作为现实，计算离标准的期望
    latest_term_num = 100
    red_latest_rate, blue_latest_rate, x_red1, x_blue1, latest_reward, latest_predict_reds, latest_predict_blues = predict_latest(
        red1s, red2s, red3s, red4s,
        red5s,
        red6s, blue1s, latest_term_num,
        correct_red, correct_blue)

    red_diffs, blue_diffs, x_red2, x_blue2, diff_reward, diff_predict_reds, diff_predict_blues = predic_latest_total_diffs(
        red_latest_rate, red_total_rate,
        blue_latest_rate, blue_total_rate,
        x_red, x_blue, correct_red,
        correct_blue)

    print("diff_predict_reds,diff_predict_blues===================================")
    print(diff_predict_reds)
    print(diff_predict_blues)

    latest_total_common_reward = is_win(get_common_list(total_predict_reds, latest_predict_reds),
                                        get_common_list(total_predict_blues, latest_predict_blues), correct_red,
                                        correct_blue)
    diff_total_common_reward = is_win(get_common_list(total_predict_reds, diff_predict_reds),
                                      get_common_list(total_predict_blues, diff_predict_blues), correct_red,
                                      correct_blue)
    diff_latest_common_reward = is_win(get_common_list(latest_predict_reds, diff_predict_reds),
                                       get_common_list(latest_predict_blues, diff_predict_blues), correct_red,
                                       correct_blue)

    latest_total_combine_reward = is_win(combine_list_no_duiplicate(total_predict_reds, latest_predict_reds),
                                         combine_list_no_duiplicate(total_predict_blues, latest_predict_blues),
                                         correct_red,
                                         correct_blue)

    diff_total_combine_reds = combine_list_no_duiplicate(total_predict_reds, diff_predict_reds)
    diff_total_combine_blues = combine_list_no_duiplicate(total_predict_blues, diff_predict_blues)
    print("diff_total_combine_reds,diff_total_combine_blues=====================================")
    print(diff_total_combine_reds)
    print(diff_total_combine_blues)
    diff_total_combine_reward = is_win(diff_total_combine_reds,
                                       diff_total_combine_blues,
                                       correct_red,
                                       correct_blue)
    diff_latest_combine_reward = is_win(combine_list_no_duiplicate(latest_predict_reds, diff_predict_reds),
                                        combine_list_no_duiplicate(latest_predict_blues, diff_predict_blues),
                                        correct_red,
                                        correct_blue)

    all_combine_list_no_duiplicate_red = combine_list_no_duiplicate(combine_list_no_duiplicate(latest_predict_reds, diff_predict_reds), total_predict_reds)
    all_combine_list_no_duiplicate_blue = combine_list_no_duiplicate(combine_list_no_duiplicate(latest_predict_blues, diff_predict_blues),total_predict_blues)
    print("all_combine_list_no_duiplicate_red,all_combine_list_no_duiplicate_blue==============================")
    print(all_combine_list_no_duiplicate_red)
    print(all_combine_list_no_duiplicate_blue)
    diff_latest_total_combine_reward = is_win(all_combine_list_no_duiplicate_red,
                                        all_combine_list_no_duiplicate_blue,
                                        correct_red,
                                        correct_blue)

    if correct_date is None:
        correct_date = "-"
    if correct_term is None:
        correct_term = "-"
    if correct_red is None:
        correct_red = "-"
    if correct_blue is None:
        correct_blue = "-"
    append_result_to_file("|" + correct_date + "|" + correct_term + "|" + list_to_str(correct_red) + "," + list_to_str(
        correct_blue) + "|" + diff_reward.__str__() + "|" + latest_reward.__str__() + "|" + total_reward.__str__()
                          + "|" + latest_total_common_reward.__str__() + "|" + diff_total_common_reward.__str__() + "|" + diff_latest_common_reward.__str__() + "|"
                          + latest_total_combine_reward.__str__() + "|" + diff_total_combine_reward.__str__() + "|" + diff_latest_combine_reward.__str__() + "|"
                          + diff_latest_total_combine_reward.__str__() + "|")
    return diff_reward, latest_reward, total_reward, latest_total_common_reward, diff_total_common_reward, diff_latest_common_reward, latest_total_combine_reward, diff_total_combine_reward, diff_latest_combine_reward, diff_latest_total_combine_reward


# get same element
def get_common_list(a_list, b_list):
    result = []
    for c in a_list:
        if c in b_list:
            result.append(c)
        pass
    return result


def combine_list_no_duiplicate(a_list, b_list):
    return list(set(np.append(a_list, b_list)))


def list_to_str(list):
    temp_str = ''
    for c in list:
        temp_str += (' ' + c)
        pass
    return temp_str


def write_all_result(dates, terms, red1s, red2s, red3s, red4s, red5s, red6s, red_all, blue1s):
    length = len(red1s)
    all_diff_reward = 0
    all_latest_reward = 0
    all_total_reward = 0
    all_latest_total_common_reward = 0
    all_diff_total_common_reward = 0
    all_diff_latest_common_reward = 0
    all_latest_total_combine_reward = 0
    all_diff_total_combine_reward = 0
    all_diff_latest_combine_reward = 0
    all_diff_latest_total_combine_reward = 0
    append_result_to_file(
        "|correct_date|correct_term|correct_red,correct_blue|diff_reward|latest_reward|total_reward|"
        "all_latest_total_common_reward|all_diff_total_common_reward|all_diff_latest_common_reward|all_latest_total_combine_reward|all_diff_total_combine_reward|all_diff_latest_combine_reward|all_diff_latest_total_combine_reward|")
    append_result_to_file(
        "|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|:-------:|")
    for i in range(length):
        correct_red = [red1s[i], red2s[i], red3s[i], red4s[i], red5s[i], red6s[i]]
        correct_blue = [blue1s[i]]
        correct_date = dates[i]
        correct_term = dates[i]
        remain_index = i + 1
        # 因为最后需要至少3个蓝球和6红球去估计，差分需要最近100个，所以预留200注作为底数
        if remain_index > length - 20:
            break
        diff_reward, latest_reward, total_reward, latest_total_common_reward, diff_total_common_reward, diff_latest_common_reward, latest_total_combine_reward, diff_total_combine_reward, diff_latest_combine_reward,diff_latest_total_combine_reward = predict_and_compare(
            dates[remain_index: length],
            terms[remain_index: length],
            red1s[remain_index: length],
            red2s[remain_index: length],
            red3s[remain_index: length],
            red4s[remain_index: length],
            red5s[remain_index: length],
            red6s[remain_index: length], red_all,
            blue1s[remain_index: length], correct_red,
            correct_blue,
            correct_date, correct_term)
        all_diff_reward += diff_reward
        all_latest_reward += latest_reward
        all_total_reward += total_reward
        all_latest_total_common_reward += latest_total_common_reward
        all_diff_total_common_reward += diff_total_common_reward
        all_diff_latest_common_reward += diff_latest_common_reward
        all_latest_total_combine_reward += latest_total_combine_reward
        all_diff_total_combine_reward += diff_total_combine_reward
        all_diff_latest_combine_reward += diff_latest_combine_reward
        all_diff_latest_total_combine_reward += diff_latest_total_combine_reward
        pass
    append_result_to_file(
        "| 0 |0 |0,|" + all_diff_reward.__str__() + "|" + all_latest_reward.__str__() + "|" + all_total_reward.__str__() + "|"
        + all_latest_total_common_reward.__str__() + "|" + all_diff_total_common_reward.__str__() + "|" + all_diff_latest_common_reward.__str__() + "|"
        + all_latest_total_combine_reward.__str__() + "|" + all_diff_total_combine_reward.__str__() + "|" + all_diff_latest_combine_reward.__str__() + "|"
    + all_diff_latest_total_combine_reward.__str__() + "|")


def append_result_to_file(content):
    # a 模式open file,指针在文件末尾，追加写入
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(content + '\n')
        f.close()


if __name__ == '__main__':
    # 定义两个变量, 用于记录历史开奖信息中的红球、蓝球号码信息
    # red_num = []
    # blue_num = []
    # 调用函数，用于获取并解析开奖的数据
    # pparser()

    dates, terms, red1s, red2s, red3s, red4s, red5s, red6s, reds, blue1s = read_file()

    # write_all_result(dates, terms, red1s, red2s, red3s, red4s, red5s, red6s, reds, blue1s)

    predict_and_compare(dates, terms, red1s, red2s, red3s, red4s, red5s, red6s, reds, blue1s, None, None,
                        None, None)
