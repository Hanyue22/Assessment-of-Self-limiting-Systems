# Author: Yue Han
# Last modified: 20241209

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.styles import Color
import os
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

# 设置全局字体为内置的 'Arial Narrow'，或其他可用的字体
# plt.rcParams['font.family'] = 'Arial Narrow'  # 或 'SimHei' (黑体), 'DejaVu Sans', 'Songti SC' 等
# plt.rcParams['font.size'] = 20  # 设置字体大小
# plt.rcParams['font.weight'] = 'bold'  # 设置字体粗细

# 定义文件名列表
file_pairs = [

    ('DFFDemb0.0-con-rr-1.xlsx', 'Dominant Female Fertility Disruptor.xlsx'),
    ('FFDemb0.0-con-rr-1.xlsx', 'Female Fertility Disruptor.xlsx'),
    ('X-het-1.xlsx', 'Autosomal X-shredder.xlsx'),
    ('Pro-1.xlsx', 'Protected dsx Disruptor.xlsx'),
    ('YDFFD-1.xlsx', 'Y-linked Dominant Female Fertility Disruptor.xlsx'),
    ('YHD-1.xlsx', 'Y-linked X-haplolethal Disruptor.xlsx'),
    ('split-1.xlsx', 'Split Female Sterile Homing.xlsx'),
    ('RIDD-1.xlsx', 'RIDD.xlsx'),
    ('Dominant-1.xlsx', 'Dominant Female Sterile Homing.xlsx'),
    ('BLH-con-rr-1.xlsx', 'Both-sex Lethal Homing.xlsx'),
    ('FSH-con-rr-1.xlsx', 'FSH-congl-1.xlsx'),
    ('drive-fs-1.xlsx', 'Drive Late-fsRIDL.xlsx'),
    ('Early-fsRIDL-1.xlsx', 'Early-fsRIDL.xlsx'),
    ('SIT-1.xlsx', 'SIT.xlsx')
][::-1]

horizontal_lines = [0.902458464, 0.87823338, 0.81701216, 0.814215216,  0.8579848, 0.85841928,0.826201304, 0.83594456, 0.80626616, 0.80039236, 0.805667568, 0.82888472, 0.81938356, 0.827471064][::-1]


all_data = []

colors = {
    0: '#739AC8',  # 蓝色
    1: '#C87373'   # 红色
}


def read_excel_skip_red(filename_a, filename_b):
    path_a = os.path.join('Normal', filename_a)
    path_b = os.path.join('congl', filename_b)

    wb_a = load_workbook(path_a)
    ws_a = wb_a.active
    wb_b = load_workbook(path_b)
    ws_b = wb_b.active
    data_a = []
    data_b = []

    for row_a, row_b in zip(ws_a.iter_rows(min_row=2, min_col=2), ws_b.iter_rows(min_row=2, min_col=2)):
        for cell_a, cell_b in zip(row_a, row_b):
            # # 检查单元格的字体颜色
            # if cell_a.font.color and cell_a.font.color.rgb == "FFFF0000":  # 红色
            #     continue
            data_a.append(cell_a.value)
            data_b.append(cell_b.value)

    # 将数据转换为DataFrame
    df_a = pd.DataFrame(data_a)
    df_b = pd.DataFrame(data_b)

    return df_a, df_b


# 处理每对文件
for i, (file_a, file_b) in enumerate(file_pairs):
    df1, df2 = read_excel_skip_red(file_a, file_b)

    # 确保两个DataFrame的行数相同
    if df1.shape[0] != df2.shape[0]:
        print(f"Row mismatch in files: {file_a} and {file_b}")
        continue

    # 将第一个Excel文件的所有列合并为单列数据，并转换为1或0
    data1_combined = df1.values.flatten()  # 将所有列合并为单列
    binary_data = (data1_combined > 0).astype(int)  # 转换为1或0

    # 将第二个Excel文件的所有列合并为单列数据
    data2_combined = df2.values.flatten()  # 将所有列合并为单列

    # 为每组数据添加组号
    group_data = pd.DataFrame({
        'group': i,
        'binary_data': binary_data,
        'data_from_csv2': data2_combined
    })

    all_data.append(group_data)

# 合并所有数据
final_df = pd.concat(all_data, ignore_index=True)

# # Use a built-in font, like 'Arial Narrow' if available
# font_properties = fm.FontProperties(family='Arial Narrow', size=38, weight='bold')

# 创建一个图形和轴
fig, ax = plt.subplots(dpi=300, figsize=(40, 25))

# 定义每组数据的x轴偏移范围
group_ranges = np.linspace(0.24, 6.76, len(file_pairs))

custom_labels = [
    'Dominant Female Fertility Disruptor',
    'Female Fertility Disruptor',
    'Autosomal X-shredder',
    'Protected dsx Disruptor',
    'Y-linked Dominant Female Fertility Disruptor',
    'Y-linked X-haplolethal Disruptor',
    'Split Female Sterile Homing',
    'RIDD',
    'Dominant Female Sterile Homing',
    'Both-sex Lethal Homing',
    'Female Sterile Homing',
    'Drive fsRIDL',
    'Early fsRIDL',
    'SIT/Early RIDL'
][::-1]

# 绘制每组数据之前，在各组之间添加竖线
for i in range(len(group_ranges) - 1):
    ax.vlines(x=(group_ranges[i] + group_ranges[i+1]) / 2, ymin=0.3, ymax=1.005, colors='gray', linestyles='dashed', linewidth=2)

# 绘制每组数据
for i, group in enumerate(group_ranges):
    group_data = final_df[final_df['group'] == i]
    binary_data = group_data['binary_data'].to_numpy()
    data_from_csv2 = group_data['data_from_csv2'].to_numpy()
    horizontal_line_y = horizontal_lines[i]

    # 计算准确度
    correct_points = (
        ((data_from_csv2 >= horizontal_line_y) & (binary_data == 1)).sum() +  # 高于横线且为红色
        ((data_from_csv2 < horizontal_line_y) & (binary_data == 0)).sum()    # 低于横线且为蓝色
    )
    total_points = len(binary_data)
    accuracy = correct_points / total_points * 100

    print(f"Group {i} ({custom_labels[i]}): {total_points} data points, Accuracy: {accuracy:.2f}%")

    # 为每个点在x轴方向上添加一个随机偏移量，以减少重叠
    x_offsets = np.random.uniform(group - 0.2, group + 0.2, len(binary_data))

    # 根据binary_data的值绘制不同颜色的点
    for j in range(len(binary_data)):
        color = colors[binary_data[j]]  # 从颜色字典中获取颜色代码
        ax.scatter(x_offsets[j], data_from_csv2[j], color=color, alpha=0.7, s=80)

    ax.hlines(horizontal_line_y, group - 0.21, group + 0.21, colors='black', linestyles='dashed', linewidths=4)

    # 在图片上方标注信息
    ax.text(group, 1.03, f'{horizontal_line_y:.3f}', ha='center', fontsize=38, fontweight='bold')
    ax.text(group, 1.01, f'{accuracy:.1f}%', ha='center', fontsize=34, fontweight='bold') # n={total_points},
    ax.text(-0.55,1.032,"Threshold", fontsize=32, fontweight='bold')
    ax.text(-0.55, 1.012, "Accuracy", fontsize=32, fontweight='bold')

# 移除顶部和右侧框线
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.spines['bottom'].set_linewidth(4)
ax.spines['left'].set_linewidth(4)

# 调整左侧y轴的长度
ax.spines['left'].set_bounds(0.3, 1.005)

# 调整底部x轴的长度
ax.spines['bottom'].set_bounds(0, 7)

# 设置x轴和y轴的范围
ax.set_xlim(0, 7)
# 设置y轴范围，只显示0.3到1.005之间的部分
ax.set_ylim(0.3, 1.005)

# 设置x轴刻度和标签
ax.set_xticks(group_ranges)

# 设置x轴刻度和标签，使用更紧凑的字体
ax.set_xticklabels(custom_labels, fontproperties='Arial Narrow', size=38, rotation=30, ha='right', weight = 'bold')

# 隐藏x轴的刻度，但保留刻度标签
ax.tick_params(axis='x', which='both', bottom=False, top=False)

# 设置y轴刻度，只显示0到1之间的刻度
ax.set_yticks(np.linspace(0.3, 1, 8))
ax.tick_params(axis='y', labelsize=45)
labels = ax.get_yticklabels()

# 使用 set_fontproperties 来设置字体大小和粗细
for label in labels:
    label.set_fontsize(45)
    label.set_fontweight('bold')

# 更新 y 轴标签
ax.set_yticklabels(labels)

# 隐藏y轴1到1.05之间的刻度标签
ax.yaxis.set_minor_locator(plt.NullLocator())

# 隐藏主刻度之间的次刻度
ax.tick_params(axis='y', which='minor', length=0)

# 隐藏y轴1到1.05之间的网格线（如果需要）
ax.yaxis.grid(False)

# 添加图表标题和坐标轴标签
ax.set_title(' ')
ax.set_xlabel(' ')
ax.set_ylabel('Constant-population Genetic Load', fontsize=60, labelpad=10, fontweight='bold')

plt.subplots_adjust(left=None, bottom=0.2, right=None, top=None, wspace=None, hspace=None)

# 显示图形
plt.savefig("TF.png")