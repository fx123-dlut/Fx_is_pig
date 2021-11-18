import requests


# 从.zip的url中下载zip文件
def download_zip_from_url(url,download_path):
    response = requests.get(url,stream=True)
    with open(download_path+url.split('/')[-1],'wb') as f:
        print("waiting for download url : "+url)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
            break

if __name__ == "__main__":
    download_zip_from_url('http://www.downza.cn/soft/74999.html','/Users/mayang/PycharmProjects/FindbugsSuanfa/projs/archiva/zip_repos/')