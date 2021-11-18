import src.get_findbugs_res_tmp.Get_xls as gx
import src.tools.compare_xls as cx
import src.get_findbugs_res_tmp.auto_download_install_findbugs as adif
import src.tools.write_to_xls as wtx

def get_commit_list_in_time(pro_path):
    data = wtx.get_from_xls(pro_path+'/res/1_get_only_bug_version.xls')
    for i in data:
        print(i)

def get_fixed(pro_path):
    # 获取fixed信息
    # gxff.main_step()
    gx.get_xls(pro_path)
    cx.compare_xls(pro_path)

def auto_get_fixed(pro_path,target_path):
    adif.auto_git_checkout_to_xml(target_path)
    gx.auto_get_xls(pro_path)
    cx.auto_compare_xls(pro_path)

# *
def auto_get_fixed_by_commit(pro_path,tar_path):
    # 获取两年内所有commit id
    get_commit_list_in_time(pro_path)
    # # 获取xml以及xls文件
    # adif.auto_git_checkout_to_xls_with_codes(tar_path)
    # # 对比xls文件获取tp和fp,并获取commit id和文件对应的list：commit_name
    # commit_name = cx.auto_compare_xls(pro_path)
    # # 合并对比后的结果
    # combine_compare_res(pro_path,commit_name,1)