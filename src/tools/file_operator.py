import os
import configure as c


# 复制classes文件夹到目标地
def copy_classes_to_targetpath(srcpath):
    respath = c.res_path+'projs/'+c.pro_name+'/'
    classpath = respath + 'classes_repos/'
    if not os.path.exists(classpath):
        os.mkdir(classpath)
    unzip_path = respath+'unzip_repos/'
    classes_folders = get_all_directory(unzip_path,[],'src')
    for i in classes_folders:
        tar_folder = i.split('unzip_repos')[1].split('src')[0]
        print(tar_folder)
        if not os.path.exists(classpath+tar_folder):
            now_path = classpath
            for i in tar_folder.split('/')[1:]:
                now_path = now_path+'/'+i
                if not os.path.exists(now_path):
                    os.mkdir(now_path)
        # cp -r folder1 folder2 将folder1复制到folder2中
        os.system('cp -r ' + i + " " + classpath+tar_folder)


# 获取多层目录下所有名字的文件夹
def get_all_directory(path,all_file_full_path_list,target_folder):
    all_file_list = os.listdir(path)
    for file in all_file_list:
        file_path = os.path.join(path,file)
        if os.path.isdir(file_path):
            get_all_directory(file_path,all_file_full_path_list,target_folder)
        if file_path[-len(target_folder+'1'):].find(target_folder) > 0:
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


if __name__ == "__main__":
    # test('/Users/mayang/PycharmProjects/FindbugsSuanfa/projs/')
    # get_only_directory('/Users/mayang/PycharmProjects/FindbugsSuanfa/projs/archiva/unzip_repos/archiva-1.0/archiva-archiva-1.0')
    copy_classes_to_targetpath('/Users/mayang/PycharmProjects/FindbugsSuanfa/projs/archiva/unzip_repos')
    # print(get_all_directory('/Users/mayang/PycharmProjects/FindbugsSuanfa/projs/archiva/unzip_repos',[],'src'))