# Author: Yue Han
# Last modified: 20241209

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import Normalize
import openpyxl
import matplotlib.patches as patches

# 加载数据
name = 'Pro-1'
wb = openpyxl.load_workbook(f'{name}.xlsx')
sheet = wb.active

# 提取数据
data = pd.read_excel(f'{name}.xlsx', header=0, index_col=0)

numeric_data = data.values.astype(float)

# 初始化一个列表来存储红色标记数据的位置
red_data_positions = []
new_data = []

# 检测红色标记的数据并读取注释
for row in range(2, sheet.max_row + 1):
    for col in range(2, sheet.max_column + 1):
        cell = sheet.cell(row=row, column=col)
        if cell.font.color and cell.font.color.rgb == "FFFF0000":  # 红色
            red_data_positions.append((row - 2, col - 2))  # 减去偏移量，匹配DataFrame的索引

            # 读取注释
            if cell.comment:
                comment_text = cell.comment.text.strip()
                print(f"检测到红色标记，注释内容: {comment_text}, 单元格: ({row}, {col})")
                try:
                    # 读取格子中的原数据
                    original_value = numeric_data[row - 2, col - 2]
                    new_value = float(comment_text)

                    # 处理新数据
                    if new_value > 0:
                        processed_new_value = (267 - new_value) / 267
                    else:
                        processed_new_value = new_value / 100000

                    # 处理原数据
                    if original_value > 0:
                        processed_original_value = (267 - original_value) / 267
                    else:
                        processed_original_value = original_value / 100000

                    # 保持正数在右上方
                    if processed_original_value > processed_new_value:
                        new_data.append((processed_new_value, processed_original_value))
                    else:
                        new_data.append((processed_original_value, processed_new_value))
                except ValueError as e:
                    print(f"警告: 注释格式错误或数据无法解析，单元格: ({row}, {col}), 错误: {e}")

# 确保 new_data 的长度与 red_data_positions 匹配
if len(new_data) != len(red_data_positions):
    print(f"警告: new_data 长度 ({len(new_data)}) 与 red_data_positions 长度 ({len(red_data_positions)}) 不匹配")

# 更新指定位置的数据
for idx, pos in enumerate(red_data_positions):
    if idx < len(new_data):
        row, col = pos
        original_value, new_value = new_data[idx]
        # 使用更新后的值替换原数据
        numeric_data[row, col] = new_value
    else:
        print(f"警告: 索引超出范围，red_data_positions[{idx}] = {pos}")

# 对原始数据应用处理逻辑
for i, x in np.ndenumerate(numeric_data):
    if x > 0:
        numeric_data[i] = (267 - x) / 267
    else:
        numeric_data[i] = x / 100000

# 创建一个DataFrame来存储处理后的数据
transformed_data = pd.DataFrame(numeric_data, index=data.index, columns=data.columns)

# 创建基础热图
sns.set(font_scale=0.8, style='whitegrid')

fig, ax = plt.subplots(figsize=(12, 12), dpi=300)

# 创建标准化器和颜色映射器
norm = Normalize(vmin=-1, vmax=1)
cmap = plt.get_cmap('RdBu_r')

# 绘制基础热图
heatmap = sns.heatmap(
    transformed_data,
    ax=ax,
    cmap=cmap,
    vmax=1,
    vmin=-1,
    center=0,
    linewidths=0.5,
    # square=True,
    annot=False,
    cbar=False
)

ax.grid(False)

# 为红色标记数据添加双色格子
for idx, pos in enumerate(red_data_positions):
    if idx < len(new_data):
        row, col = pos
        positive_value = new_data[idx][0]
        negative_value = new_data[idx][1]

        # 根据新数据值映射颜色
        color_positive = cmap(norm(positive_value))
        color_negative = cmap(norm(negative_value))

        # 绘制双色格子
        ax.add_patch(patches.Polygon(
            [(col, row), (col, row + 1), (col + 1, row + 1)],
            color=color_positive
        ))
        ax.add_patch(patches.Polygon(
            [(col, row), (col + 1, row), (col + 1, row + 1)],
            color=color_negative
        ))

        ax.add_patch(patches.Polygon(
            [(col, row), (col, row + 1), (col + 1, row + 1)],
            edgecolor='white',
            linewidth=0.88,  # 边框宽度
            fill=False  # 不填充颜色，只绘制边框
        ))
        ax.add_patch(patches.Polygon(
            [(col, row), (col + 1, row), (col + 1, row + 1)],
            edgecolor='white',
            linewidth=0.88,  # 边框宽度
            fill=False  # 不填充颜色，只绘制边框
        ))

ax = plt.gca()

# # 绘制白色横线
# ax.hlines(
#     y=1,  # 横线的y位置（行索引之间的0.5位置，整数表示行的中间）
#     xmin=0,  # 横线起点的x轴位置
#     xmax=transformed_data.shape[1],  # 横线终点的x轴位置（列数）
#     colors='white',  # 横线的颜色
#     linewidth=8  # 横线的宽度
# )

# 设置x轴刻度标签
xticks = plt.gca().get_xticks()
plt.xticks(xticks[::2], rotation=0, horizontalalignment='center', fontsize=34)
plt.gca().xaxis.set_ticks_position('none')

# 设置y轴刻度标签
yticks = plt.gca().get_yticks()
# selected_yticks = yticks[[0, 1, 3, 5, 7, 9]]  # 选取特定的刻度
plt.yticks(yticks[::2], rotation=0, horizontalalignment='right', fontsize=34)#,
plt.gca().yaxis.set_ticks_position('none')

# Set x and y axis labels
plt.suptitle('Protected dsx Disruptor', size=42, x=0.535, y=0.99) # 0.555, 0.99
plt.title("Hetero. Release, Embryo Resistance Cut Rate = 0.0", size=32)

plt.xlabel("Germline Cut Rate", size=42)
plt.ylabel("Release Ratio", size=42)

plt.gca().xaxis.set_label_position('bottom')

# 设置x轴标题的位置，参数为(x,y)坐标，y=0表示在x轴刻度线上，向上增加数值
ax.xaxis.set_label_coords(0.5, -0.07)  # 调整列标题与热图边缘的距离

# 设置y轴标题的位置，参数为(x,y)坐标，x=0表示在y轴刻度线上，向左增加数值
ax.yaxis.set_label_coords(-0.09, 0.5)  # 调整行标题与热图边缘的距离
# -0.09 0.5
# -2 0.5

ax.set_position([0.17, 0.13, 0.77, 0.77])
# 0.17 0.13 0.77 0.77
# 0.52 0.13 0.035 0.77

# # 调整图片边距
# plt.subplots_adjust(left=None, bottom=0.2, right=None, top=None, wspace=None, hspace=None)
plt.savefig(f'{name}.png')

