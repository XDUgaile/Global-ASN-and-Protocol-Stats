import os
import pandas as pd

# 定义文件夹路径
folder_path = r'E:\全网AS及协议栈分布统计\2022CSV'  # 请替换为您的CSV文件夹路径

# 定义结果存储的DataFrame
result_df = pd.DataFrame(columns=['Total_Unique_AS', 'IPv6_Only_AS', 'IPv4_Only_AS', 'Dual_Stack_AS'])

# 遍历文件夹中的所有CSV文件
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)

        try:
            # 读取CSV文件
            data = pd.read_csv(file_path, header=None)
            if len(data) > 1:  # 确保CSV有至少两行
                second_row = data.iloc[1, :min(4, data.shape[1])]  # 提取最多四列
                # 补齐列数
                missing_cols = len(result_df.columns) - len(second_row)
                if missing_cols > 0:
                    second_row = pd.concat([second_row, pd.Series([None] * missing_cols)], ignore_index=True)

                # 添加到结果DataFrame
                new_row = pd.DataFrame([second_row.values], columns=result_df.columns)
                result_df = pd.concat([result_df, new_row], ignore_index=True)
            else:
                print(f"{file_name} 文件行数不足，跳过处理。")
        except Exception as e:
            print(f"处理文件 {file_name} 时出错: {e}")

# 保存提取的数据到新的CSV文件
result_csv_path = 'extracted_data2.csv'  # 请替换为您希望保存的路径
result_df.to_csv(result_csv_path, index=False)

print(f"数据提取完成，结果已保存到 {result_csv_path}")
