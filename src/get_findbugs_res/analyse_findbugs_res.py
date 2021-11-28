import configure as c
import os
import xml.dom.minidom as dom
import src.tools.write_to_xls as wtx
import src.tools.file_operator as fo
import src.get_findbugs_res.get_codes_by_findbugs_res as gcbfr
import src.tools.list_operator as lo


def get_xls_by_true_filename(xml_path,file_name,res_path):
    heads = ["method_name","method_sig","file_path","class_name","lstart","lend","priority","catogeray","codes"]
    for filename in file_name:
        res = []
        filename = str(filename)
        try:
            tree = dom.parse(xml_path+filename)
        except Exception:
            continue
        root = tree.documentElement
        print("filename _ "+ filename)

        bugs = root.getElementsByTagName("BugInstance")

        for bug in bugs:
            desc = bug.getAttribute("type")
            priority = bug.getAttribute("priority")
            if bug.getElementsByTagName("Method"):
                croot = bug.getElementsByTagName("Method")[0]
                classname = croot.getAttribute("classname")
                signature = croot.getAttribute("signature")
                method_name = croot.getAttribute("name")
                root2 = croot.getElementsByTagName("SourceLine")[0]
                sourcepath = root2.getAttribute("sourcepath")
                start = root2.getAttribute("start")
                end = root2.getAttribute("end")
            res.append([method_name,signature,sourcepath,classname,start,end,priority,desc])
        wtx.save_to_targetpath_xls(heads,res,c.pro_name,filename.split('.xml')[0],res_path)


# 根据xml获取xls文件
def auto_get_xls():
    pro_path = c.res_path
    folder_path = pro_path+'/projs/'+c.pro_name+'/findbugs_res/'
    xls_path = folder_path+'xls/'
    print(xls_path)
    if not os.path.exists(xls_path):
        os.mkdir(xls_path)
    file_name = os.listdir(folder_path+'xml')
    get_xls_by_true_filename(folder_path+'xml/',file_name,xls_path)


# 使用findbugs后一版本标记前一版本
def auto_compare_xls_by_filename(release_list):
    all_file_names = release_list
    pro_path = c.res_path
    res_path = pro_path+'/projs/' + c.pro_name+'/findbugs_res/compared/'
    src_path = pro_path+'/projs/' + c.pro_name+'/findbugs_res/xls/'
    if not os.path.exists(res_path):
        os.mkdir(res_path)
    for i in range(len(all_file_names)-1):
        old_file_name = src_path+all_file_names[i]+'.xls'
        new_file_name = src_path+all_file_names[i+1]+'.xls'
        file_name = all_file_names[i].split('.xls')[0]+"_"+all_file_names[i+1].split('.xls')[0]
        res_file = res_path+file_name
        print("old : "+old_file_name)
        print("new : "+new_file_name)
        print("res : "+res_file)
        res = []
        old_data = wtx.get_from_xls(old_file_name,0)
        new_data = wtx.get_from_xls(new_file_name)
        headers = old_data[0]+['status']

        for old_rownum in old_data[1:]:
            flag = 1
            for new_rownum in new_data:
                if(old_rownum[0] == new_rownum[0] and old_rownum[2] == new_rownum[2] and
                        old_rownum[-1] == new_rownum[-1]):
                    res.append(old_rownum+['fp'])
                    flag = 0
                    break
            if flag == 1:
                res.append(old_rownum+['new'])
        wtx.save_to_targetpath_xls(headers,res,'compare_res',file_name,res_path)


def compare_xls_inorder(rel_list):
    auto_compare_xls_by_filename(rel_list)


def compare_xls(release_liat):
    xls_path = c.res_path+ '/projs/' + c.pro_name+'/findbugs_res/xls'
    xls_files = os.listdir(xls_path)
    exist_xls_files = []
    for i in release_liat:
        if lo.judge_in_list(xls_files,i+'.xls'):
            exist_xls_files.append(i)
    # 根据版本号进行排序
    # unzip_files = c.res_path + '/projs/' + c.pro_name + '/unzip_repos/'
    # unzip_files = os.listdir(unzip_files)
    # files = []
    # for i in unzip_files:
    #     files.append(i+'.xls')
    print(exist_xls_files)
    print(xls_files)
    compare_xls_inorder(exist_xls_files)
    return release_liat


def analyse_findbugs_res_main_func(release_list):
    # 从xml中提取信息到xls
    auto_get_xls()

    # 获取findbugs中对应的缺陷代码行
    gcbfr.get_codes_from_unzip_repos()

    # 比较结果
    release_list = compare_xls(release_list)
    return release_list


if __name__ == "__main__":
    analyse_findbugs_res_main_func()