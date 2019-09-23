from collections import Counter

# 画图工具-单数组的概率密度分布
# 原始画图工具，可以自己指定x,y
import matplotlib.pyplot as plt
# 数学工具
import numpy as np

# 因为6+1的规则是3个起连续红球 + 蓝才能得奖，所以需要计算三个连续以上的组合及概率密度函数
# C(33,6)=1107568
# C(33,5)=237336
# C(33,4)=40920
# C(33,3)=5456
# k!(6)=720
# A(33,6)=797448960
# A(33,5)=28480320
# A(33,4)=982080
# A(33,3)=32736
# A(16,1)=16
# 33取6的全排列，到现在20190924只出现了2469种，也就是还有8亿的可能没出来，够玩10000年了
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

# 每一位数组的长度是相同的
def get_continuous_num(continuous_num, red1, red2, red3, red4, red5, red6):
    # 不能要求连续数超过6
    if continuous_num > 6:
        return
    result = []
    length = len(red1)
    go_max_num = 6 - continuous_num + 1
    for index in range(length):
        # 原数字是2位，加个逗号，凑3位
        sequence = str(red1[index]) + "," + str(red2[index])+ "," + str(red3[index])+ "," + str(red4[index])+ "," + str(red5[index])+ "," + str(red6[index])+ ";"
        print(sequence)
        for j in range(go_max_num):
            # print(j)
            x = sequence[3*j:3*(j + continuous_num)]
            # print(x)
            result.append(x)
        pass
    pass
    # print(result)
    return result

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
    # 计算归一化总概率
    x_red = list(map(lambda x: "r" + x[0], red_sorted))
    x_red_int = list(map(lambda x: int(x[0]), red_sorted))
    x_blue = list(map(lambda x: "b" + x[0], blue_sorted))
    x_blue_int = list(map(lambda x: int(x[0]), blue_sorted))
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

    # 画条形图：条形图是用条形的长度表示各类别频数的多少，其宽度（表示类别）则是固定的；
    plt.bar(np.append(x_red, x_blue), np.append(red_rate, blue_rate), label='graph 1')
    plt.legend()
    plt.xlabel('number')
    plt.ylabel('rate')
    plt.title('test')
    plt.show()

    return red_rate, blue_rate, x_red, x_blue

def predict_single(red_num):
    red_count = Counter(red_num)
    print(red_count)
    print('------------------------------------------------------------------------------')
    # 按照出现频率倒序
    # python 使用 lambda 来创建匿名函数lambda [arg1 [,arg2,.....argn]]:expression
    red_sorted = sorted(red_count.items(), key=lambda x: x[1], reverse=True)
    red = red_sorted[0:6]

    # map() 会根据提供的函数对指定序列做映射。map(function, iterable, ...)
    red1 = list(map(lambda x: x[0], red))
    red1.sort()
    print('------------------------------------------------------------------------------')
    # 按照出现频率顺序
    red_sorted = sorted(red_count.items(), key=lambda x: x[1], reverse=False)
    red = red_sorted[0:6]

    red2 = list(map(lambda x: x[0], red))
    red2.sort()
    print('------------------------------------------------------------------------------')
    # 按照次数倒叙序排序（多的在前）
    total_red = len(red_num)
    red_sorted = sorted(red_count.items(), key=lambda x: x[1], reverse=True)
    # 计算归一化总概率
    x_red = list(map(lambda x: "r" + x[0], red_sorted))
    red_rate = list(map(lambda x: x[1] * 100 / total_red, red_sorted))
    print(red_rate)

    # 画条形图：条形图是用条形的长度表示各类别频数的多少，其宽度（表示类别）则是固定的；
    x_20 = x_red[0:20]
    red_rate_20 = red_rate[0:20]
    print(x_20)
    print(red_rate_20)
    plt.bar(x_20, red_rate_20, label='graph 1')
    plt.legend()
    plt.xlabel('number')
    plt.ylabel('rate')
    plt.title('test')
    plt.show()

    print('------------------------------------------------------------------------------')
    # 按照次数倒正序排序(少的在前)
    total_red = len(red_num)
    red_sorted = sorted(red_count.items(), key=lambda x: x[1], reverse=False)
    # 计算归一化总概率
    x_red = list(map(lambda x: "r" + x[0], red_sorted))
    red_rate = list(map(lambda x: x[1] * 100 / total_red, red_sorted))
    print(red_rate)

    # 画条形图：条形图是用条形的长度表示各类别频数的多少，其宽度（表示类别）则是固定的；
    x_20 = x_red[0:20]
    red_rate_20 = red_rate[0:20]
    print(x_20)
    print(red_rate_20)
    plt.bar(x_20, red_rate_20, label='graph 1')
    plt.legend()
    plt.xlabel('number')
    plt.ylabel('rate')
    plt.title('test')
    plt.show()

    return red_rate, x_red

# 比较数组每个元素之间的方差
def variance(source, target):
    diffs = []
    for index, source_element in enumerate(source):
        target_element = target[index]
        diffs.append(source_element - target_element)
        pass
    return diffs


if __name__ == '__main__':

    # get_continuous_num(3, ['01','02'] ,['02','03'],['03','04'],['04','05'],['05','06'],['06','07'])
    # get_continuous_num(4, ['01'] ,['02'],['03'],['04'],['05'],['06'])
    # get_continuous_num(5, ['01'] ,['02'],['03'],['04'],['05'],['06'])
    # get_continuous_num(6, ['01'] ,['02'],['03'],['04'],['05'],['06'])

    dates, terms, red1s, red2s, red3s, red4s, red5s, red6s, reds, blue1s = read_file()

    red_3_group = get_continuous_num(3, red1s, red2s, red3s, red4s, red5s, red6s)
    predict_single(red_3_group)
    predict_single(get_continuous_num(4, red1s, red2s, red3s, red4s, red5s, red6s))
    predict_single(get_continuous_num(5, red1s, red2s, red3s, red4s, red5s, red6s))
    predict_single(get_continuous_num(6, red1s, red2s, red3s, red4s, red5s, red6s))
