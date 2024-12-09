import pandas as pd
import openpyxl
from openpyxl.styles import Font
from openpyxl.comments import Comment
import numpy as np
import os

files = [f for f in os.listdir() if f.endswith('.xlsx') and not f.startswith('~$')]

# 遍历所有符合条件的文件
for name in files:

    xlsx = pd.ExcelFile(name, engine='openpyxl')
    output_name = name.replace('.xlsx', '-1.xlsx')
    writer = pd.ExcelWriter(output_name, engine='openpyxl')  # 输出文件名添加后缀'-1'

    # 读取xlsx文件

    results = {}
    tagged = {}
    index_values = []
    prev_condition = None

    # 遍历每个sheet
    for sheet_name in xlsx.sheet_names:
        df = pd.read_excel(xlsx, sheet_name=sheet_name)
        queue = []

        # 对每个数据块（每10行）进行处理
        for i in range(0, len(df), 10):
            block = df.iloc[i:i + 10]

            if sheet_name == xlsx.sheet_names[0]:
                index_avg = block.iloc[:, 5].mean()  # 计算第6列的平均值
                index_values.append(index_avg)

            # 检查第一列0和1的数量
            zeros = (block.iloc[:, 0] == 0).sum()
            ones = (block.iloc[:, 0] == 1).sum()

            # 根据0和1的数量，计算不同列的平均值
            if zeros > 5:
                avg = block[block.iloc[:, 0] == 0].iloc[:, 4].mean() * -1
                prev_condition = 'zeros'
            else:
                avg = block[block.iloc[:, 0] == 1].iloc[:, 1].mean()
                prev_condition = 'ones'

            queue.append(avg)

            # 检查是否需要打标签
            if zeros > 0 and ones > 0:
                if sheet_name not in tagged:
                    tagged[sheet_name] = []
                tagged[sheet_name].append(len(queue) - 1)

        results[sheet_name] = queue

    # 找到最长的列表
    max_len = max(len(lst) for lst in results.values())

    # 确保所有列表的长度都相同
    for key in results:
        if len(results[key]) < max_len:
            results[key] += [np.nan] * (max_len - len(results[key]))

    if len(index_values) < max_len:
        index_values += [np.nan] * (max_len - len(index_values))

    # 将结果写入新的Excel文件
    result_df = pd.DataFrame(results)
    result_df.insert(0, '', index_values)  # 插入索引列，但不指定列名

    result_df.to_excel(writer, sheet_name='Results', index=False)

    # 对带标签的数据进行标红处理，并添加注释
    wb = writer.book
    ws = wb['Results']
    red_font = Font(color="00FF0000")

    for sheet_name, tags in tagged.items():
        df = pd.read_excel(xlsx, sheet_name=sheet_name)  # 重新读取数据以便进行新的计算

        for i in tags:
            cell = ws.cell(row=i + 2, column=list(results.keys()).index(sheet_name) + 2)  # 列从第2列开始
            cell.font = red_font

            # 找到数据块的起始行
            block_start_row = i * 10
            block_end_row = block_start_row + 10
            block = df.iloc[block_start_row:block_end_row]
            print(block)
            # 获取之前的计算条件

            zeros = (block.iloc[:, 0] == 0).sum()
            print(zeros)
            # 根据之前的条件计算新的均值
            if zeros > 5:
                print(block[block.iloc[:, 0] == 1].iloc[:, 1])
                new_avg = block[block.iloc[:, 0] == 1].iloc[:, 1].mean()
                print(new_avg)
            else:
                new_avg = block[block.iloc[:, 0] == 0].iloc[:, 4].mean() * -1
                print(new_avg)
            # 添加注释
            comment_text = f"{new_avg}"
            cell.comment = Comment(comment_text, "Python Script")

    writer._save()