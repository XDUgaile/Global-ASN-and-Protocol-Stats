import csv
from datetime import datetime, timedelta

# 定义起始日期和结束日期
start_date = datetime.strptime("20250101", "%Y%m%d")
end_date = datetime.strptime("20250306", "%Y%m%d")

# 循环遍历每一天
current_date = start_date
while current_date <= end_date:
    # 格式化日期
    date_str = current_date.strftime("%Y%m%d")

    # 输入文件路径
    input_file_v4 = fr'E:\全网AS及协议栈分布统计\2025IPv4\ipasn_{date_str}.dat'
    input_file_v6 = fr'E:\全网AS及协议栈分布统计\2025IPv6\ipasn_{date_str}.dat'

    # 初始化集合来存储来自IPv4和IPv6数据集的唯一AS号码
    unique_as_v4 = set()
    unique_as_v6 = set()


    # 定义一个函数从.dat文件中提取AS号码
    def extract_as_numbers(file_path, as_set):
        with open(file_path, 'r') as file:
            for line in file:
                # 跳过以';'开头的注释行和空行
                if line.startswith(';') or not line.strip():
                    continue
                # 按空格分割行内容
                parts = line.split()
                # 如果行内容分割后有两个部分，提取第二部分（AS号码）并添加到集合中
                if len(parts) == 2:
                    as_number = parts[1]
                    as_set.add(as_number)


    # 从IPv4和IPv6数据集中提取AS号码
    extract_as_numbers(input_file_v4, unique_as_v4)
    extract_as_numbers(input_file_v6, unique_as_v6)

    # 计算不同的AS数量
    total_unique_as = len(unique_as_v4.union(unique_as_v6))  # 总的唯一AS数量
    ipv6_only_as = len(unique_as_v6 - unique_as_v4)  # 仅存在于IPv6数据集的AS数量
    ipv4_only_as = len(unique_as_v4 - unique_as_v6)  # 仅存在于IPv4数据集的AS数量
    dual_stack_as = len(unique_as_v4.intersection(unique_as_v6))  # 同时存在于IPv4和IPv6数据集的AS数量

    # 选择性地输出具体的AS项
    output_individual_as = False  # 如果设置为True，则输出具体的AS项；否则仅输出汇总信息

    # 输出结果
    print(f"Processing date: {date_str}")
    print(f"Total unique AS numbers: {total_unique_as}")
    print(f"IPv6-only AS numbers: {ipv6_only_as}")
    print(f"IPv4-only AS numbers: {ipv4_only_as}")
    print(f"Dual-stack AS numbers: {dual_stack_as}")

    # 将结果写入CSV文件
    output_file = f'as_counts_{date_str}.csv'
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # 写入表头
        writer.writerow(['Date', 'Total_Unique_AS', 'IPv6_Only_AS', 'IPv4_Only_AS', 'Dual_Stack_AS'])
        # 写入数据行
        writer.writerow([date_str, total_unique_as, ipv6_only_as, ipv4_only_as, dual_stack_as])

        if output_individual_as:
            writer.writerow([])
            writer.writerow(['AS_Number', 'Category'])
            # 输出IPv6-only AS
            for as_number in sorted(unique_as_v6 - unique_as_v4):
                writer.writerow([as_number, 'IPv6-only'])
            # 输出IPv4-only AS
            for as_number in sorted(unique_as_v4 - unique_as_v6):
                writer.writerow([as_number, 'IPv4-only'])
            # 输出Dual-stack AS
            for as_number in sorted(unique_as_v4.intersection(unique_as_v6)):
                writer.writerow([as_number, 'Dual-stack'])

    print(f"AS counts and details have been written to {output_file}\n")  # 提示结果和具体项已写入CSV文件

    # 日期递增
    current_date += timedelta(days=1)
