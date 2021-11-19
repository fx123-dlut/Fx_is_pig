import os.path
from time import sleep
import configure as c
import src.tools.write_to_xls as wtx
import src.tools.compare_file as cf
import src.tools.web_operator as wo


# 创建仓库
def mkdir_findbugs_repos():
    pro_save_path = c.res_path+"projs/"
    cf.my_mkdir(pro_save_path)
    pro_save_path = pro_save_path + c.pro_name + "/"
    cf.my_mkdir(pro_save_path)
    zip_mkdir = pro_save_path+"zip_repos/"
    cf.my_mkdir(zip_mkdir)
    unzip_mkdir = pro_save_path+"unzip_repos/"
    cf.my_mkdir(unzip_mkdir)
    return zip_mkdir


# 从github下载zip文件
def download_zip_from_github(zip_path):
    release_file_name = c.res_path+"init_data/git_release_version_with_commitid.xls"
    release_file_data = wtx.get_from_xls(release_file_name)
    for i in release_file_data:
        if os.path.exists(zip_path+i[0]+'.zip'):
            print("existed : "+i[0]+'.zip')
            continue
        url = 'https://github.com/apache/'+c.pro_name+'/archive/refs/tags/'+i[0]+'.zip'
        print("waiting for download url : "+url)
        wo.get_zip_from_url(url,zip_path)
        # sleep(5)
        print(url)
    return True


# 将zip文件解压到unzip_repos中
def unzip_files(zip_path):
    cf.unzip_all_zip_indict(zip_path,zip_path.split('zip_repos')[0]+"unzip_repos/",'zip')


# 从github下载到解压
def download_and_unzip_from_github_main():
    zip_path = mkdir_findbugs_repos()
    download_zip_from_github(zip_path)
    unzip_files(zip_path)


if __name__ == "__main__":
    print(download_and_unzip_from_github_main())