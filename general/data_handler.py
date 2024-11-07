import os
import re
from datetime import datetime


def storage_uploaded_image(file, upload_to):
    # 当前目录/media/upload_to/年/月/日
    storage_absolute_dir = f"{os.getcwd()}/media/{upload_to}{datetime.now().strftime('%Y')}/{datetime.now().strftime('%m')}"
    if not os.path.exists(storage_absolute_dir):
        os.makedirs(storage_absolute_dir)
    if file is None:
        return None
    file_name = file.name
    if len(file_name) > 6:
        file_name = file.name[-6:]
    storage_absolute_path = f"{storage_absolute_dir}/{str(datetime.now().strftime('%Y-%m-%d-%H-%M-%S-'))}{file_name}"
    with open(storage_absolute_path, "wb") as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    return storage_absolute_path.replace('media/', '')


def unload_image_from_server(url):
    if os.path.exists('media/' + url):
        os.remove('media/' + url)
    else:
        raise Exception('Image not found')


def get_image_urls_from_md_str(md_str):
    # 定义一个正则表达式，匹配!这样的格式
    pattern = r'!\[\]\((.+?)\)'
    # 使用re.findall函数，返回所有匹配的url
    image_urls = re.findall(pattern, md_str)
    # 打印结果
    if len(image_urls) > 0:
        return image_urls
    else:
        return None
