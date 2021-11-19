import os
import configure as c
import src.tools.write_to_xls as wtx
from time import sleep
import src.tools.file_operator as fo


def get_classes_main_func():
    all_release_version_file = c.res_path+"init_data/git_release_version_with_committime.xls"
    all_release_version_data = wtx.get_from_xls(all_release_version_file)
    for i in all_release_version_data:
        #  window下用此命令
        # os.system('cd '+c.path.split(':')[0])
        # 切换到对应项目目录
        os.chdir(c.path)
        # git checkout archiva1.1 切换到指定的release
        cmdline = 'git checkout '+i[0]
        print("now run : " + cmdline)
        os.system(cmdline)
        sleep(5)
        # maven编译项目
        os.system('mvn clean install -DskipTests')
        fo.copy_one_version_to_target_path(i[0])
    fo.copy_classes_to_targetpath()


def clone_file_from_git_files(path,pname,targetpath,pro_path):
    if (os.path.exists(c.res_path + '/projs/datas/classes_file') == False):
        os.mkdir(pro_path + '/compare/datas/classes_file')
    if (os.path.exists(c.pro_path + '/compare/datas/classes_file/' + pname) == False):
        os.mkdir(pro_path + '/compare/datas/classes_file/' + pname)
    os.chdir(path)
    if (os.path.exists(targetpath) == False):
        os.mkdir(targetpath)
    sub_path = fo.get_all_directory(c.path)
    for j in sub_path:
        if (os.path.isfile(j) or j == '.gitignore'):
            continue
        # print(j)
        os.chdir(path+'/'+j)
        print(path+'/'+j)
        # print(os.path)
        if (os.path.exists('classes')):
            if (os.path.exists(targetpath + "/" + j) == False):
                os.mkdir(targetpath + '/' + j)
            # print('target path : '+targetpath+'/'+j)
            cmdline = 'xcopy "' + path + '/' + j + '/' + 'classes"' + ' "' + targetpath + '/' + j + '" /s /f /h'
            # print(cmdline)
            os.system(cmdline)


if __name__ == "__main__":
    get_classes_main_func()