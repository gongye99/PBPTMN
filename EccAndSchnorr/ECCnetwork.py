import os

from keras.src.saving.saving_api import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
from SetEcc import ECC
from ModFuction import *

# 函数：检查椭圆曲线的合法性
def is_valid_curve(a, b, p):
    print(a,b,p)
    if p!=0:
        if is_prime(p) & (4 * a**3 + 27 * b**2) % p != 0:
            ellip = ECC(a, b, p)
            G = ellip.genG()
            (x, y) = G.point
            n = get_order(x, y, a, p)
            if n != 0 :
                m = HidenMessage(100,ellip)
                if m != 0:
                    return True
    return False


def is_prime(n):
    """ 检查一个数是否是素数 """
    if n == 0:
        return False
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def get_order(x0, y0, a, p):
    """
    计算椭圆曲线的阶  阶是椭圆曲线上点的数量
    """
    # 计算-p
    x1 = x0
    y1 = (-1 * y0) % p
    temp_x = x0
    temp_y = y0
    n = 1
    p_value_tmp = None
    for _ in range(p):
        n += 1
        if n % 2 == 1:
            p_value_tmp = p_value
        p_value = CalculateR(temp_x, temp_y, x0, y0, a, p)

        if p_value == p_value_tmp:
            return 0

        if p_value[0] == x1 and p_value[1] == y1:
            return n + 1

        temp_x = p_value[0]
        temp_y = p_value[1]

    return 0

def CalculateR(x1, y1, x2, y2, a, p):
    """
        计算p+q   计算两点相加的结果，并返回新点的坐标
        """
    flag = 1  # 定义符号位
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a  # 计算分子
        denominator = 2 * y1  # 计算分母
    else:
        member = y2 - y1
        denominator = x2 - x1
        if member * denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)

    # 将分子和分母化为最简
    gcd_value =gcd(member, denominator)
    member = int(member / gcd_value)
    denominator = int(denominator / gcd_value)
    # 求分母的逆元
    inverse_value = get_inverse_element(denominator, p)
    k = (member * inverse_value)
    if flag == 0:
        k = -k
    k = k % p
    # 计算x3,y3
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    # print("%d<=====>%d" % (x3, y3))
    return [x3, y3]

def HidenMessage(msg,curve):
    adjustment = 0  # 调整次数
    p = curve.p
    x = msg % p
    while True:
        rhs = x ** 3 + curve.a * x + curve.b
        # y是不是p的平方剩余，若y是，则求出y的值，有一对
        y = mod_sqrt(rhs, p)
        if y is not None:
            return 1
        x += 1
        if x > p :
            break
    return 0


# def modular_sqrt(a, p):
#     """计算模p下的平方根，如果存在的话。"""
#     # 检查是否满足p ≡ 3 (mod 4)的特殊情况
#     if p % 4 == 3:
#         if pow(a, (p - 1) // 2, p) == 1:  # Euler's criterion
#             return pow(a, (p + 1) // 4, p)
#         else:
#             return None
#     else:
#         # 通用方法，适用于所有p，但效率可能较低
#         for y in range(1, p):
#             if (y * y) % p == a:
#                 return y
#         return None  # 如果没有找到平方根，则返回None
def mod_sqrt(a, p):
    """ 计算模 p 下的平方根，假设 p 是素数 """
    if legendre_symbol(a, p) != 1:
        return None  # 如果 a 不是平方剩余，则不存在平方根

    if p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

        # Tonelli-Shanks 算法
    q = p - 1
    s = 0
    while q % 2 == 0:
        s += 1
        q //= 2
    z = 2
    while legendre_symbol(z, p) != -1:
        z += 1
        if z > int(p ** 0.5) + 1:
            print(z)
            return None
    c = pow(z, q, p)
    r = pow(a, (q + 1) // 2, p)
    t = pow(a, q, p)
    m = s
    while t != 1:
        i = 0
        temp = t
        while temp != 1:
            temp = pow(temp, 2, p)
            i += 1
            if i == m:
                return None
        b = pow(c, 2 ** (m - i - 1), p)
        r = (r * b) % p
        t = (t * b * b) % p
        c = pow(b, 2, p)
        m = i
    return r
def legendre_symbol(a, p):
    """计算勒让德符号 (a/p) = a^(p-1)/2 mod p。"""
    return pow(a, (p - 1) // 2, p)

# 函数：生成训练数据
def generate_training_data(num_samples):
    data = []
    for _ in range(num_samples):
        a = np.random.randint(0, 500)
        b = np.random.randint(0, 500)
        p = np.random.randint(500, 1000)
        if is_valid_curve(a, b, p):
            data.append([a, b, p])
        print(np.array(data))
    return np.array(data)

def generate_and_save_data(file_name='train_data.npy', num_samples=100000):
    # 生成新的训练数据
    new_train_data = generate_training_data(num_samples)
    print("Generated data shape:", new_train_data.shape)

    # 检查文件是否存在且非空
    if os.path.isfile(file_name) and os.path.getsize(file_name) > 0:
        existing_data = np.load(file_name)
        # 检查 existing_data 是否为空
        if existing_data.size > 0:
            updated_data = np.vstack((existing_data, new_train_data))
        else:
            updated_data = new_train_data
    else:
        updated_data = new_train_data

    # 保存更新后的数据
    np.save(file_name, updated_data)


# 函数：将新数据添加到现有数据中，并保存
# def append_and_save_training_data(new_data, file_name='train_data.npy'):
#     if os.path.isfile(file_name):
#         existing_data = np.load(file_name)
#         updated_data = np.vstack((existing_data, new_data))
#     else:
#         updated_data = new_data
#     np.save(file_name, updated_data)

def load_training_data(file_name='train_data.npy', num_samples=100000):
    # 检查文件是否存在
    if os.path.isfile(file_name):
        # 从文件中加载数据
        return np.load(file_name)
    else:
        # 文件不存在，生成新的数据
        new_train_data = generate_training_data(num_samples)
        # 保存新数据到文件
        np.save(file_name, new_train_data)
        return new_train_data


if __name__ == '__main__':
    # 调用函数生成并保存数据
    # generate_and_save_data('train_data.npy', 1000000)
    # 加载或创建训练数据
    train_data = load_training_data()
    #
    # # # 生成并保存新的训练数据
    # # new_train_data = generate_training_data(100)
    # # append_and_save_training_data(new_train_data)

    model_file = 'elliptic_curve_model.keras'

    # 检查模型文件是否存在
    if os.path.exists(model_file):
        print("加载已存在的模型继续训练")
        model = load_model(model_file)
    else:
        print("创建新的模型")
        # 构建神经网络模型
        model = Sequential([
            Dense(64, activation='relu', input_shape=(3,)),
            Dense(1024, activation='relu'),
            Dense(3)
        ])
        # 编译模型
        model.compile(optimizer='adam', loss='mean_squared_error')

    # 训练模型
    model.fit(train_data, train_data, epochs=100000, batch_size=32)

    # 保存模型
    model.save(model_file)
# 生成椭圆曲线参数
def generate_curves(model, num_curves):
    curves = []
    while len(curves) < num_curves:
        prediction = model.predict(np.random.rand(1, 3) * 1000)
        a, b, p = map(int, prediction[0])
        if is_valid_curve(a, b, p):
            curves.append((a, b, p))
    return curves

def get_random_curve(file_name='train_data.npy', max_attempts=1000):
    if os.path.isfile(file_name):
        # 从文件中加载数据
        data = np.load(file_name)
        attempts = 0
        while attempts < max_attempts:
            # 随机选择一个样本
            random_index = np.random.randint(0, data.shape[0])
            curve_params = data[random_index]
            a, b, p = curve_params
            # 检查曲线是否有效
            if is_valid_curve(a, b, p):
                return curve_params
            attempts += 1
        print("Failed to find a valid curve after several attempts.")
        return None
    else:
        print("File not found: ", file_name)
        return None
def load_model_and_generate_curves(model_filename, num_curves):
    # 载入模型
    loaded_model = load_model(model_filename)
    # 生成椭圆曲线
    return generate_curves(loaded_model, num_curves)




