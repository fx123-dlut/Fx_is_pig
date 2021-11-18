import os

# *
def clone_file_from_git_files(path,pname,targetpath,pro_path):
    if (os.path.exists(pro_path + '/compare/datas/classes_file') == False):
        os.mkdir(pro_path + '/compare/datas/classes_file')
    if (os.path.exists(pro_path + '/compare/datas/classes_file/' + pname) == False):
        os.mkdir(pro_path + '/compare/datas/classes_file/' + pname)
    os.chdir(path)
    if (os.path.exists(targetpath) == False):
        os.mkdir(targetpath)
    sub_path = get_only_wenjianjia()
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

# *
def get_only_wenjianjia():
    files = os.listdir('.')
    for i in files[::]:
        if os.path.isfile(os.path.join('.',i)):
            files.remove(i)
    # print(len(files))
    return files


def main_step():
    # 项目名称
    proname = 'commons-vfs'
    # 项目存放的路劲
    ppath = 'E:/projects/git/java/commons-vfs-release'
    now_path = os.getcwd().split('get_fixed')[0]
    pro_path = now_path.split('compare\\')[0]
    classes_path = now_path+'datas/classes_file/'+proname
    # # 获取所有classes文件夹
    get_xml_from_findbugs(ppath,proname,classes_path,pro_path)
    print(now_path)
    # 根据文件夹获取xml文件
    get_xml(classes_path,now_path)

if __name__=="__main__":
    main_step()