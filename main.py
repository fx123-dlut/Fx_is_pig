import src.data_process.get_git_jira_data_main_func as ggjdmf
import src.get_findbugs_res.get_findbug_res_main as gfrm


if __name__ == "__main__":
    # 获取github上的漏洞信息
    # ggjdmf.main_func()
    # 获取findbugs的漏洞信息
    gfrm.get_findbugs_res_main()
