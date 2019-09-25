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

if __name__ == '__main__':
    a = ["01", "02"]
    print(a + ["r"])
    b = []
    for ele in a:
        ele = "r" + ele
        b.append(ele)
    print(a)
    print(b)
    print(get_reward("40", 1))
    print(get_reward("00", 1))
