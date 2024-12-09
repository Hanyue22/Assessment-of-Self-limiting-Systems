# Author: Yue Han
# Last modified: 20241209

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap

name = 'Protected dsx Disruptor'
data = pd.read_excel(f'{name}.xlsx', header=0, index_col=0)
data1 = pd.read_excel(f'{name}.xlsx', header=None, index_col=None)

# Extract the numeric data
numeric_data = data.values.astype(float)

# Create a DataFrame with the transformed numeric_data and set row and column labels
transformed_data = pd.DataFrame(numeric_data, index=data.index, columns=data.columns)

jet = plt.get_cmap('plasma')

# 定义一个新的映射函数，将 0-0.1 的部分扩展到 0-0.4
def new_mapping(x):
    if x < 0.6:
        return x / 6
    else:
        return 0.1 + (x - 0.6)*(0.9 / 0.4)

# 应用新的映射函数到整个范围
new_values = np.linspace(0, 1, 256)
mapped_values = np.array([new_mapping(x) for x in new_values])

# 生成新的 colormap 数据
new_colors = jet(mapped_values)

# 创建自定义的 colormap
new_cmap = LinearSegmentedColormap.from_list('new_jet', new_colors)

# Extract the numeric data
numeric_data = data.values.astype(float)

# Create a DataFrame with the transformed numeric_data and set row and column labels
transformed_data = pd.DataFrame(numeric_data, index=data.index, columns=data.columns)

# Create and save the heatmap without annotations (white numbers)
fig, ax = plt.subplots(dpi=300, figsize=(12, 12))

# Customize Seaborn style and color bar format
sns.set(font_scale=0.8, style='whitegrid')  # Adjust font size and remove vertical lines in column labels

heatmap = sns.heatmap(
    transformed_data,
    cmap=new_cmap,
    ax=ax,
    # center=0.4,
    vmax=1.0,
    vmin=0.0,
    linewidths=0.5,
    square=False,
    annot=False,
    cbar=False
)

ax.grid(False)

# # 创建colorbar对象
# cbar = plt.colorbar(heatmap.collections[0], format='%.2f')
#
# # 设置colorbar的刻度和标签
# cbar.ax.tick_params(width=0.5, length=3, colors='gray')
# # cbar.outline.set_linewidth(0.5)
# # cbar.set_ticks([0.0, 0.25, 0.5, 0.75, 1.0])  # 这里的数字是您想要在colorbar上显示的刻度
# # cbar.set_ticklabels(['0.0', '0.25', '0.5', '0.75', '1.0'], size=8, color='black')  # 这里的数字是您想要在colorbar上显示的标签

ax = plt.gca()

# Set x and y axis labels
plt.xlabel('Germline Cut Rate', size=42)
plt.ylabel('Release Ratio', size=42)
plt.gca().xaxis.set_label_position('bottom')
plt.gca().xaxis.tick_bottom()
plt.title("Hetero. Release, Embryo Resistance Rate = 0.0", size=32)
plt.suptitle("Protected dsx Disruptor", size=42, x=0.535, y=0.99)

# 设置x轴标题的位置，参数为(x,y)坐标，y=0表示在x轴刻度线上，向上增加数值
ax.xaxis.set_label_coords(0.5, -0.07)  # 调整列标题与热图边缘的距离

# 设置y轴标题的位置，参数为(x,y)坐标，x=0表示在y轴刻度线上，向左增加数值
ax.yaxis.set_label_coords(-0.09, 0.5)  # 调整行标题与热图边缘的距离
# -2 0.5
# -0.09 0.5

# 设置x轴刻度标签
xticks = plt.gca().get_xticks()
plt.xticks(xticks[::2], rotation=0, horizontalalignment='center', fontsize=34)
plt.gca().xaxis.set_ticks_position('none')

# 设置y轴刻度标签
yticks = plt.gca().get_yticks()
plt.yticks(yticks[::2], rotation=0, horizontalalignment='right', fontsize=34)
plt.gca().yaxis.set_ticks_position('none')

ax.set_position([0.15, 0.13, 0.77, 0.77])
# 0.52 0.13 0.035 0.77
# 0.15 0.13 0.77 0.77

# # 调整图片边距
# plt.subplots_adjust(left=None, bottom=0.2, right=None, top=None, wspace=None, hspace=None)

plt.savefig(f'{name}-congl.png')
