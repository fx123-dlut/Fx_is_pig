import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# 从.zip的url中下载zip文件
# def get_zip_from_url(url,download_path):
#     response = requests.get(url,stream=True)
#     with open(download_path+url.split('/')[-1],'wb') as f:
#         print("waiting for download url : "+url)
#         for chunk in response.iter_content(chunk_size=1024):
#             if chunk:
#                 f.write(chunk)
def get_zip_from_url(url,down_path):
    s = requests.session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    s.mount('https://', adapter)
    s.keep_alive = False
    response = s.get(url)
    data = response.content
    with open(down_path+url.split('/')[-1],'wb') as f:
        f.write(data)
    s.close()


if __name__ == "__main__":
    get_zip_from_url('https://github.com/apache/archiva/archive/refs/tags/archiva-1.1.zip',
                          '/Users/mayang/PycharmProjects/FindbugsSuanfa/projs/archiva/zip_repos/')