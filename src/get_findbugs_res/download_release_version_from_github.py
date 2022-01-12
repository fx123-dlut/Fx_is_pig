import os.path
import configure as c
import src.tools.write_to_xls as wtx
import src.tools.compare_file as cf
import src.tools.web_operator as wo
import src.tools.file_operator as fo


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
        if os.path.exists(zip_path+c.pro_name+'-'+str(i[0])+'.zip') or os.path.exists(zip_path+ str(i[0])+'.zip'):
            print("existed : "+i[0]+'.zip')
            continue
        # https://github.com/apache/archiva/archive/refs/tags/archiva-2.2.5.zip
        url = 'https://github.com/apache/'+c.pro_name+'/archive/refs/tags/'+str(i[0])+'.zip'
        # url = 'https://codeload.github.com/apache/'+c.pro_name+'/archive/refs/tags/'+i[0]
        print(str(release_file_data.index(i)) + '/' +str(len(release_file_data))+" waiting for download url : "+url)
        wo.get_zip_from_url(url,zip_path)
        # sleep(5)
        print(url)
    return True


# 将zip文件解压到unzip_repos中
def unzip_files(zip_path):
    cf.unzip_all_zip_indict(zip_path,zip_path.split('zip_repos')[0]+"unzip_repos/",'zip')


def mvn_unzip_release():
    unzip_filepath = c.res_path+'projs/'+c.pro_name+'/unzip_repos/'
    rel_list = os.listdir(unzip_filepath)
    for i in rel_list:
        path = unzip_filepath+i
        folder = os.listdir(path)
        # print(path)
        # print(folder)
        try:
            os.chdir(path+'/'+folder[0])
            os.system('mvn clean install -DskipTests -Drat.skip=true')
        except IndexError as e:
            continue


def get_classes_from_unzip_folder():
    mvn_unzip_release()


# 从github下载到解压
def download_and_unzip_from_github_main():
    # 建立目录
    zip_path = mkdir_findbugs_repos()
    # 下载zip包
    download_zip_from_github(zip_path)
    # 解压zip包
    unzip_files(zip_path)


def get_classes_by_zip_main_func():
    # 下载解压zip包
    download_and_unzip_from_github_main()
    # 编译unzip
    get_classes_from_unzip_folder()
    # 提取classes到classses_repos文件夹
    fo.copy_classes_to_targetpath()


if __name__ == "__main__":
    get_classes_by_zip_main_func()