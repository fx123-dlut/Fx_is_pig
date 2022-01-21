from datetime import datetime


# time1早于time2返回false(建议希望早的时间放前面，满足会返回true)
def compare_time(time1, time2):
    time1 = time1.split('+')[0].split('-')[0].strip()
    time2 = time2.split('+')[0].split('-')[0].strip()
    x = datetime.strptime(time1, '%a %b %d %H:%M:%S %Y')
    y = datetime.strptime(time2, '%a %b %d %H:%M:%S %Y')
    return x < y


def sort_time_list(date):
    return datetime.strptime(date.split('+')[0].split('-')[0].strip(),'%a %b %d %H:%M:%S %Y').timestamp()

# 获得排序后的时间序列
def get_sort_res(arr):
    return sorted(arr, key=lambda date: sort_time_list(date))


if __name__ == "__main__":
    # arr = ['Fri Jan 20 08:22:32 2006 +0000','Fri Jan 20 08:22:31 2006 +0000']
    arr = ['Fri Jan 20 08:22:20 2006 +0000','Fri Jan 20 08:22:31 2007 +0000','Fri Jan 20 08:21:31 2006 +0000','Thu Jan 19 08:22:31 2006 +0000']
    list = get_sort_res(arr)
    print(compare_time(arr[0],arr[1]))
    print(list)