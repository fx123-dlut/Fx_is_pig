import src.data_process.get_git_jira_data_main_func as ggjdmf
import src.get_findbugs_res.mark_findbugs_res_by_gitres as mfrbg
import src.data_process.split_bugs_to_release as sbtr
import src.get_pmd_res.get_pmd_data as gpd
import src.get_checkstyle_res.mark_checkout_res as mcr
import configure as c
from get_summary import summary_the_res
import os


# 获取data下所有已存在的项目名
def get_exist_data():
    pro_names = os.listdir(c.base_res_path)
    res = []
    for i in pro_names:
        if 'csv' in i or 'xls' in i:
            continue
        res.append(i)
    return res


# 需要执行的重复运行的操作
def fix_old_version_genericbugline():
    ggjdmf.main_func(True)
    sbtr.split_bug_to_release_by_time()
    mfrbg.mark_tp_findbugs_line_by_res()
    gpd.use_git_remark_pmd_res()
    mcr.mark_cs_res_by_git()


# 根据data目录里面的项目，修改configure文件，并对每个项目进行对应的操作
def auto_fix_exist_pro():
    pro_names = get_exist_data()
    for name in pro_names:
        print('now fix project name is '+ name +"; now position is "+str(pro_names.index(name))+"/"+str(len(pro_names)))
        c.pro_name = name
        c.res_path = c.base_res_path+name+"/"
        c.path = c.base_pro_path+name+'/'
        try:
            fix_old_version_genericbugline()
        except Exception as e:
            print(repr(e))
            continue
    summary_the_res.get_all_data(c.base_res_path)


if  __name__ == '__main__':
    auto_fix_exist_pro()