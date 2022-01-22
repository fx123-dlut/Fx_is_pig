import src.data_process.get_git_jira_data_main_func as ggjdmf
import src.get_findbugs_res.get_findbug_res_main as gfrm
import src.get_checkstyle_res.get_checkstyle_data as gcd
import src.get_pmd_res.get_pmd_data as gpd


def main():
    # 获取github上的漏洞信息
    ggjdmf.main_func()
    # 获取find0bugs的漏洞信息并获取相关代码段
    # myfaces-core-module-2.3-next-M6
    gfrm.get_findbugs_res_main()
    # 获取checkstyle并进行分析
    gpd.get_pmd_res_main_func()
    # 获取checkstyle并进行分析
    gcd.get_checkstyle_data_main_func()


if __name__ == "__main__":
    main()