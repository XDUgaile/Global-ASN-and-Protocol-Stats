import os
from datetime import datetime, timedelta

# 设置起始日期和结束日期
start_date = datetime.strptime("20241212", "%Y%m%d")
end_date = datetime.strptime("20241231", "%Y%m%d")

# 循环遍历每一天
current_date = start_date
while current_date <= end_date:
    # 格式化日期
    date_str = current_date.strftime("%Y%m%d")

    # 构建命令
    command = f"python pyasn_util_convert.py --single .\\rib.{date_str}.0000.bz2 ipasn_{date_str}.dat"

    # 执行命令
    os.system(command)

    # 日期递增
    current_date += timedelta(days=1)
