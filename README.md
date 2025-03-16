# Global-ASN-and-Protocol-Stats
全网AS及协议栈分布统计 

IPv4 from http://archive.routeviews.org/bgpdata/

IPv6 from http://archive.routeviews.org/route-views6/bgpdata/

通过上面的资源，统计出当天全网的AS及协议栈分布。分为了四类AS：IPv4单栈AS、IPv6单栈AS、双栈AS和AS总数。下面是统计的2024数据折线图:

Through the above resources, the distribution of AS and protocol stacks on the entire network that day was counted. It is divided into four categories of AS: IPv4 Only AS, IPv6 Only AS, dual stack AS and total unique AS. Here's a line graph of the 2024 stats.

![img](/figure/2024.png)

上面的IPv4和IPv6文件夹中包含了下载当天数据的下载脚本和解压脚本。经本人测试，由于是从国外网址下载，设置代理过后下载速度会快得多，所以在下载脚本中包含了代理设置，各位可以参考个人情况进行修改。下载完成后可以使用解压脚本将数据正常解压。

The above IPv4 and IPv6 folders contain download scripts and decompression scripts for the data on the day of downloading. After my test, since I downloaded from a foreign website, the download speed will be much faster after setting up the proxy, so the proxy settings are included in the download script. You can refer to your personal situation to modify it. After the download is completed, you can use the decompression script to normally decompress the data.
