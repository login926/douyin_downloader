# -*- coding: utf-8 -*-
import os
from urllib.request import urlopen
import requests
from tqdm import tqdm
import re
#导入模块

# download 函数处的代码参考了 Zeropython 在知乎的回答：https://www.zhihu.com/question/41132103/answer/279584095 非常感谢作者提供的帮助
def download(url, dst, name):
    """
    @param: url to download file
    @param: dst place to put the file
    """
    file_size = int(urlopen(url).info().get('Content-Length', -1))

    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return file_size
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    pbar = tqdm(
        total=file_size, initial=first_byte,
        unit='B', unit_scale=True, desc=name)
    req = requests.get(url, headers=header, stream=True)
    with(open(dst, 'ab')) as f:
        for chunk in req.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                pbar.update(1024)
    pbar.close()
    return file_size


print("输入抖音链接：")
douyin_url = input()
#获取抖音视频链接，此处未做链接的校验功能
headers = {'User-Agnet': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36', 'Connection': 'keep-alive'}
# Requests 的请求头部，可以根据需求修改
html_r = requests.get(douyin_url,headers=headers)
html_data = html_r.text
#使用 Requests 获得抖音分享页面的网页源代码
video_id = re.findall("(?<=video_id=).+?(?=\\\\u0026line=0)",html_data)[0]
#在网页源代码中使用正则获得视频的 video_id
video_name = re.findall("(?<=class=\"desc\">).+?(?=</p>)",html_data)[0] + " " + re.findall("(?<=崇拜).+?(?=，从)",html_data)[0]
#在网页源代码中使用正则匹配并拼接视频的 video_name ，video_name 参数用于下载时显示文件名，此处video_name 格式：视频名+@用户名
file_name = "./" + video_name + ".mp4"
#视频文件在本地的存储位置及文件名
video_download_url = 'https://aweme.snssdk.com/aweme/v1/play/?video_id=' + video_id
#获得视频的下载链接
download(video_download_url, file_name , video_name)
#开始下载
