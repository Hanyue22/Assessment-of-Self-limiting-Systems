# Author: Yue Han
# Last modified: 20241209

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import openpyxl  # 需要使用openpyxl来处理Excel中的字体颜色

# 读取Excel文件
df_A = pd.read_excel('Pro-1.xlsx', index_col=0, header=0)
df_B = pd.read_excel('Protected dsx Disruptor.xlsx', index_col=0, header=0)
print(f"df_A shape: {df_A.shape}")
print(f"df_B shape: {df_B.shape}")

# 使用openpyxl打开Excel文件来检查单元格颜色
wb = openpyxl.load_workbook('Pro-1.xlsx')
ws = wb.active  # 获取活动工作表

# 设置阈值
threshold = 0.814215216

# 创建一个空的颜色矩阵
color_matrix = np.empty(df_A.shape, dtype=object)

# 定义颜色
deep_pink = '#CD6889'
light_pink = '#FFB5C5'
dark_blue = '#4F94CD'
light_blue = '#C6E2FF'
clear = 'clear'
white = '#FFFFFF'

# 遍历数据框，按条件设置颜色
for i in range(df_A.shape[0]):
    for j in range(df_A.shape[1]):
        cell_a = ws.cell(row=i+2, column=j+2)  # 需要加上偏移量以跳过索引行列
        if df_A.iat[i, j] > 0 and df_B.iat[i, j] > threshold:
            color_matrix[i, j] = deep_pink
        elif df_A.iat[i, j] > 0 and df_B.iat[i, j] <= threshold:
            color_matrix[i, j] = light_pink
        elif df_A.iat[i, j] < 0 and df_B.iat[i, j] <= threshold:
            color_matrix[i, j] = dark_blue
        elif df_A.iat[i, j] < 0 and df_B.iat[i, j] > threshold:
            color_matrix[i, j] = light_blue
        else:
            color_matrix[i, j] = white  # 其他情况用白色填充

# 绘制热图
plt.grid(True)

plt.figure(dpi=300, figsize=(12, 12))

# 调整单元格大小
cell_width = 1
cell_height = 1

# 使用带颜色的网格图
for i in range(df_A.shape[0]):
    for j in range(df_A.shape[1]):
        if color_matrix[i, j] != clear:  # 只绘制非"clear"的单元格
            plt.gca().add_patch(plt.Rectangle((j, i), cell_width, cell_height,
                                              facecolor=color_matrix[i, j],
                                              edgecolor='white', linewidth=1.5))

plt.xlim(0, df_A.shape[1])
plt.ylim(0, df_A.shape[0])

# 反转y轴使其从上往下显示
plt.gca().invert_yaxis()

# 设置刻度，每隔一个格子显示
plt.xticks(ticks=np.arange(0.5, df_A.shape[1], 2), labels=df_A.columns[::2], fontsize=30)
plt.yticks(ticks=np.arange(0.5, df_A.shape[0], 2), labels=df_A.index[::2], fontsize=30)

plt.xlabel('X-shred Rate', size=35, labelpad=20)
plt.ylabel('Release Ratio', size=35)

# 设置正方形格子
plt.gca().set_aspect('equal', adjustable='box')

# 添加星星
plt.text(10.5, 11, '*', fontsize=35, color='black', ha='center', fontweight='bold')

plt.title('Protected dsx Disruptor', size=40, pad=20)
plt.savefig('Protected dsx Disruptor0.8.png')
