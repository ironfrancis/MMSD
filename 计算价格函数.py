# 计算价格函数
import numpy as np


def checkSteps(x):
    # 对x累进阶梯计价
    # 0-2的部分，价格为1
    # 2-20的部分，价格为0.5
    # 20-100的部分，价格为0.4
    # 100-200的部分，价格为0.3
    price = 0
    ori = x * 0.5
    if x > 2:
        price += 2
        x -= 2
    else:
        price += x

    if x - 18 > 0:
        price += 0.5 * 18
        x -= 18
    else:
        price += x * 0.5

    if x > 30:
        price += 0.4 * 30
        x -= 30
    else:
        price += x * 0.4

    if x > 50:  # 50-100的部分，价格为0.35
        price += 0.35 * 50
        x -= 50
    else:
        price += x * 0.35

    if x >= 100:  # 100-200的部分，价格为0.3
        price += 0.3 * 100
        x -= 100
    else:
        price += x * 0.25

    if x >= 0:  # >200的部分，价格为0.25
        price += 0.25 * x
    return price / ori

def checkSellPrice(x):         # 统一单价法
    price = 0
    if x < 40:
        price += x * 0.5       # 数量小于40，统一按照单价0.5元
    elif 40 <= x < 80:
        price = 0.45 * x       # 数量在40-80之间，统一按照单价0.45元
    elif 80 <= x < 200:
        price = 0.4 * x        # 数量在80-200之间，统一按照单价0.4元
    elif 200 <= x:
        price = 0.35 * x       # 数量大于200，统一按照单价0.35元

    return price / (x * 0.5), price



x = np.arange(1, 500, 1)
y = [checkSteps(i) for i in x]
y2 = [checkSellPrice(i) for i in x]

# 画出折线图，x轴为数量，y轴为价格
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Songti SC']
plt.title('打印收费与数量的关系 \n 以黑白A4打印为例', )
plt.xlim(0, 500)
plt.xlabel('数量')
plt.grid(True)
plt.ylabel('价格')

plt.plot(x, y2, 'r-', label=["统一单价法",'折扣'])
# plt.plot(x,y,'b-',label="阶梯计价法")
plt.legend(loc='upper left')
plt.show()
