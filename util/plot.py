import matplotlib.pyplot as plt

# 数据
time_cost = [11.802036237716675, 6.920340728759766, 4.254702281951904, 3.002729606628418, 2.271101093292236, 1.8032099723815918]
gas_cost = [7098.368, 6466.132, 5876.055, 5295.755, 4695.968, 4105.952]

# 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(time_cost, gas_cost, marker='o')

# 设置横轴和纵轴的标签
plt.xlabel('Time Cost')
plt.ylabel('')

# 设置横轴和纵轴的刻度
plt.xticks(range(int(min(time_cost)), int(max(time_cost))+2, 1))
plt.yticks(range(4000, int(max(gas_cost))+1000, 500))

# 显示网格
plt.grid(True)

# 显示图表
plt.show()
