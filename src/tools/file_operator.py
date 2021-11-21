import os
import configure as c
import shutil


# 复制classes文件夹到目标地，linux下用，将目录下多个版本按照顺序分别copy到指定目录
def copy_classes_to_targetpath():
    respath = c.res_path+'projs/'+c.pro_name+'/'
    classpath = respath + 'classes_repos/'
    if not os.path.exists(classpath):
        os.mkdir(classpath)
    unzip_path = respath+'unzip_repos/'
    print('waiting for collecting classes......')
    classes_folders = get_all_directory(unzip_path,[],'classes')
    for i in classes_folders:
        file_name = i.split('unzip_repos')[1].replace('\\','/')
        cmdline = 'xcopy "' + i + '/*.*" "' + classpath + file_name + '/" /s /f /h'
        print(cmdline)
        os.system(cmdline)
        # # mac下用
        # tar_folder = i.split('unzip_repos')[1].split('src')[0].replace('\\','/')
        # print(tar_folder)
        # if not os.path.exists(classpath+tar_folder):
        #     now_path = classpath
        #     for i in tar_folder.split('/')[1:]:
        #         now_path = now_path+'/'+i
        #         if not os.path.exists(now_path):
        #             os.mkdir(now_path)
        # # cp -r folder1 folder2 将folder1复制到folder2中
        # os.system('cp -r ' + i + " " + classpath+tar_folder)


# 获取多层目录下所有名字的文件夹
def get_all_directory(path,all_file_full_path_list,target_folder):
    all_file_list = os.listdir(path)
    for file in all_file_list:
        file_path = os.path.join(path,file)
        if os.path.isdir(file_path):
            get_all_directory(file_path,all_file_full_path_list,target_folder)
        if file_path[-len(target_folder+'1'):].find(target_folder) > 0 and file_path.split(target_folder)[0][-1]!='-':
            all_file_full_path_list.append(file_path)
    return all_file_full_path_list


# 只获取文件夹名字
def get_only_directory(path):
    files = os.listdir(path)
    for i in files[::]:
        if os.path.isfile(os.path.join(path,i)):
            files.remove(i)
    print(files)
    print(len(files))
    return files


def test(path):
    res = os.listdir(path)
    for i in res:
        print(i)


# 复制单个版本classes文件到指定文件夹下
def copy_one_version_to_target_path(folder_name = 'tmp'):
    tarpath = c.res_path+'/projs/archiva/unzip_repos/'
    if not os.path.exists(tarpath):
        os.mkdir(tarpath)
    if os.path.exists(tarpath+folder_name):
        shutil.rmtree(tarpath+folder_name)
    print("classes file is : " + tarpath+folder_name)
    # 复制文件到指定文件夹下 http://www.xue51.com/tuwen/xcopy4444.html windows适用
    cmdline = 'xcopy "' + c.path + '/*.*" "' +tarpath+folder_name + '/" /s /f /h'
    cmdline2 = 'xcopy "' + c.path + '/src" "' +tarpath+folder_name + '/src/" /s /f /h'
    cmdline3 = 'xcopy "' + c.path + '/target" "' +tarpath+folder_name + '/target/" /s /f /h'
    print(cmdline)
    os.system(cmdline)
    os.system(cmdline2)
    os.system(cmdline3)
    # 不好用
    # shutil.copytree(c.path.replace('\\','/'),(tarpath+folder_name).replace('\\','/'))


# 复制单个版本classes文件到指定文件夹下
def copy_one_version_classes_to_target_path(folder_name = 'tmp'):
    tarpath = c.res_path+'/projs/archiva/classes_repos/'
    if not os.path.exists(tarpath):
        os.mkdir(tarpath)
    if os.path.exists(tarpath+folder_name):
        shutil.rmtree(tarpath+folder_name)
    classes_folders = get_all_directory(c.path,[],'classes')
    print("classes file is : " + str(classes_folders))
    # 复制文件到指定文件夹下
    for i in classes_folders:
        # print(i.split(c.path)[1])
        cmdline = 'xcopy "' + i.replace('\\','/') + '/*.*" "' +tarpath+folder_name+i.split(c.path)[1].replace('\\','/') + '\\" /s /h'
        cmdline.replace('\\','/')
        print(cmdline)
        os.system(cmdline)
    # 不好用
    # shutil.copytree(c.path.replace('\\','/'),(tarpath+folder_name).replace('\\','/'))


# 对文件的版本号进行排序
def sort_files_by_version(files):
    res = []
    files.sort(key = lambda x: len(x))
    head_files = get_target_lens_file_num(files,len(files[0]))
    index = len(head_files)
    for i in head_files:
        res.append(i)
        while files[index].split('xls')[0].find(i.split('xls')[0]) >= 0:
            res.append(files[index])
            index = index + 1
    return res


# 获取指定长度的文件数量
def get_target_lens_file_num(files,lens):
    res = []
    for i in files:
        if len(i) == lens:
            res.append(i)
    return res


# 判断文件夹下所有文件是否有着相同长度的版本信息
def file_equal_len(files):
    for i in range(len(files)-1):
        if len(files[i].split('.')) != len(files[i+1].split('.')):
            return False
    return True


def copy_all_version_to_target_path(version_list):
    for i in version_list:
        copy_one_version_to_target_path(i[0])
    copy_classes_to_targetpath()


if __name__ == "__main__":
    # test('/Users/mayang/PycharmProjects/FindbugsSuanfa/projs/')
    # get_only_directory('/Users/mayang/PycharmProjects/FindbugsSuanfa/projs/archiva/unzip_repos/archiva-1.0/archiva-archiva-1.0')
    # copy_classes_to_targetpath('/Users/mayang/PycharmProjects/FindbugsSuanfa/projs/archiva/unzip_repos')
    # print(get_all_directory('/Users/mayang/PycharmProjects/FindbugsSuanfa/projs/archiva/unzip_repos',[],'src'))
    # copy_one_version_classes_to_target_path('archiva')
    copy_one_version_to_target_path()
    # shutil.copytree(c.path.replace('\\','/'),'E:\\projects\\py\\shiwanhuoji\\Fx_is_pig\\projs\\archiva\\classes_repos/archiva'.replace('\\','/'))