from datetime import datetime


# time1早于time2返回false
def compare_time(time1, time2):
    time1 = time1.split('+')[0].split('-')[0].strip()
    time2 = time2.split('+')[0].split('-')[0].strip()
    x = datetime.strptime(time1, '%a %b %d %H:%M:%S %Y')
    y = datetime.strptime(time2, '%a %b %d %H:%M:%S %Y')
    return x < y


if __name__ == "__main__":
    print(compare_time('Fri Jan 20 08:22:31 2006 +0000', 'Fri Jan 20 08:22:32 2006 +0000'))
