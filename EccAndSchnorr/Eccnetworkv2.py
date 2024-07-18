import numpy as np

# 加载数据
train_data = np.load('train_data.npy')

# 获取数据的数量
num_samples = train_data.shape[0]  # 第一维度的大小代表样本数量

print(f"Number of samples in train_data.npy: {num_samples}")