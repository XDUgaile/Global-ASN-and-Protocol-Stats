import os
import requests
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor


def download_file(url, save_path, proxies=None):
    """下载文件并保存到指定路径，同时显示下载速度和进度百分比。

    Args:
        url (str): 文件的URL。
        save_path (str): 保存文件的路径。
        proxies (dict, optional): 代理设置，格式为 {"http": "http://ip:port", "https": "http://ip:port"}。
    """
    try:
        response = requests.get(url, stream=True, proxies=proxies)
        response.raise_for_status()  # 检查是否成功获取响应

        # 获取文件大小
        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        start_time = datetime.now()

        # 创建保存路径的目录（如果不存在）
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # 如果chunk不为空
                    file.write(chunk)
                    downloaded_size += len(chunk)

                    # 计算下载进度和速度
                    percent = (downloaded_size / total_size) * 100 if total_size else 0
                    elapsed_time = (datetime.now() - start_time).total_seconds()
                    speed = (downloaded_size / elapsed_time / 1024) if elapsed_time > 0 else 0  # 转换为KB/s

                    print(f"\r下载中: {percent:.2f}% | 已下载: {downloaded_size / 1024:.2f} KB | 速度: {speed:.2f} KB/s",
                          end="")

        print(f"\n文件已成功下载并保存到: {save_path}")
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")


def generate_urls(base_url_template, start_date, end_date):
    """生成一系列按照日期顺序的URL。

    Args:
        base_url_template (str): 基础URL模板，包含年份和月份的占位符，例如 "http://archive.routeviews.org/route-views6/bgpdata/{year}.{month:02d}/RIBS"。
        start_date (str): 起始日期，格式为"YYYYMMDD"。
        end_date (str): 结束日期，格式为"YYYYMMDD"。

    Returns:
        list: 包含所有生成URL的列表。
    """
    urls = []
    current_date = datetime.strptime(start_date, "%Y%m%d")
    end_date = datetime.strptime(end_date, "%Y%m%d")

    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        base_url = base_url_template.format(year=year, month=month)
        for hour in ["0000"]:  # 下载每天00:00
            file_name = f"rib.{current_date.strftime('%Y%m%d')}.{hour}.bz2"
            urls.append(f"{base_url}/{file_name}")
        current_date += timedelta(days=1)

    return urls


def download_all_files(urls, save_directory, proxies=None, max_workers=4):
    """并行下载所有文件。

    Args:
        urls (list): 要下载的URL列表。
        save_directory (str): 保存文件的目录。
        proxies (dict, optional): 代理设置。
        max_workers (int): 并行下载的线程数。
    """
    os.makedirs(save_directory, exist_ok=True)

    def download_task(url):
        file_name = os.path.basename(url)  # 获取URL中的文件名
        save_path = os.path.join(save_directory, file_name)
        print(f"正在下载: {url}")
        download_file(url, save_path, proxies=proxies)

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        executor.map(download_task, urls)


if __name__ == "__main__":
    # 基础URL模板
    base_url_template = "http://archive.routeviews.org/bgpdata/{year}.{month:02d}/RIBS"

    # 指定日期范围
    start_date = "20210101"
    end_date = "20211231"

    # 生成URL列表
    urls = generate_urls(base_url_template, start_date, end_date)

    # 指定保存文件的目录
    save_directory = r"E:\v4download"

    # 代理设置
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890"
    }

    # 并行下载所有文件
    download_all_files(urls, save_directory, proxies=proxies, max_workers=3)
