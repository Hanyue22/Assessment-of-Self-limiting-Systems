import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, Color
import numpy as np
from openpyxl import Workbook
from openpyxl import load_workbook
from zipfile import BadZipFile

# 获取当前文件夹下所有文件
# files = [f for f in os.listdir() if f.endswith('.xlsx') and not f.startswith('~$')]
files = ['Pro-congl.xlsx']

# 遍历所有符合条件的文件
for name in files:
    xlsx = pd.ExcelFile(name, engine='openpyxl')
    output_name = name.replace('.xlsx', '-1.xlsx')
    writer = pd.ExcelWriter(output_name, engine='openpyxl')  # 输出文件名添加后缀'-1'

    results = {}
    index_values = []

    # 遍历每个sheet
    for sheet_name in xlsx.sheet_names:
        df = pd.read_excel(xlsx, sheet_name=sheet_name)
        queue = []

        # 对每个数据块（每5行）进行处理
        for i in range(0, len(df), 5):
            block = df.iloc[i:i+5]

            # 如果是第一个sheet，计算索引列的值
            if sheet_name == xlsx.sheet_names[0]:
                index_avg = block.iloc[:, 2].mean()  # 计算第3列的平均值
                index_values.append(index_avg)

            avg = block.iloc[:, 3].mean()  # 计算第4列的平均值
            queue.append(avg)
        results[sheet_name] = queue

    # 找到最长的列表
    max_len = max(len(lst) for lst in results.values())

    # 确保所有列表的长度都相同
    for key in results:
        if len(results[key]) < max_len:
            results[key] += [np.nan] * (max_len - len(results[key]))

    # 确保索引列的长度与结果一致
    if len(index_values) < max_len:
        index_values += [np.nan] * (max_len - len(index_values))

    # 将结果写入新的Excel文件
    result_df = pd.DataFrame(results)

    # 在最左侧插入索引列
    result_df.insert(0, '', index_values)  # 插入索引列，但不指定列名

    # 按照索引列进行倒序排序
    result_df = result_df.sort_values(by='', ascending=False)

    # 将数据写入Excel文件
    result_df.to_excel(writer, sheet_name='Results', index=False)

    writer._save()