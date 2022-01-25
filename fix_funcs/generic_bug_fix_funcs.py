import src.data_process.get_git_jira_data_main_func as ggjdmf
import src.get_findbugs_res.mark_findbugs_res_by_gitres as mfrbg
import src.get_findbugs_res.analyse_findbugs_res as afr
import src.data_process.split_bugs_to_release as sbtr
import src.get_pmd_res.get_pmd_data as gpd
import src.get_checkstyle_res.mark_checkout_res as mcr
import src.get_checkstyle_res.get_checkstyle_data as gcd
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


# 需要执行的findbugs修复操作
def fix_findbugs(release_list):
    afr.analyse_findbugs_res_main_func(release_list)
    mfrbg.mark_tp_findbugs_line_by_res()


# 需要执行的pmd修复操作
def fix_pmd():
    gpd.get_code_from_csv()
    gpd.remove_same_line(True)
    gpd.use_git_remark_pmd_res()
    gpd.use_self_remark_pmd_res(True)


# 需要执行的checkstyle修复操作
def fix_checkstyle():
    gcd.from_cs_xml_to_csv()
    gcd.get_code_from_csv()
    mcr.mark_cs_res_by_git()
    gcd.use_self_remark_checkstyle_res(True)


# 需要执行的重复运行的操作
def fix_old_version_genericbugline():
    # ggjdmf.main_func(True)
    release_list = sbtr.split_by_release_main_func()
    fix_findbugs(release_list)
    fix_pmd()
    fix_checkstyle()


# 根据data目录里面的项目，修改configure文件，并对每个项目进行对应的操作
def auto_fix_exist_pro():
    # 重新將结果中的项目挨个识别
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

    # fix_old_version_genericbugline()
    # 統計結果信息
    summary_the_res.get_all_data(c.base_res_path)
    # summary_the_res.test_summary()


if __name__ == '__main__':
    auto_fix_exist_pro()