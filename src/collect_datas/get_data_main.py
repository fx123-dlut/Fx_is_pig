import src.collect_datas.from_gitlog_get_info as fggi
import src.collect_datas.from_web_get_jira_Data as fwgjd
import src.collect_datas.combine_jira_gitlog as cjg
import os
import configure as c


def get_data():
    if not os.path.exists(c.res_path):
        os.mkdir(c.res_path)
    if not os.path.exists(c.res_path + '/init_data'):
        os.mkdir(c.res_path+'/init_data')
    if not os.path.exists(c.res_path+'/res'):
        os.mkdir(c.res_path+'/res')
    fggi.get_log_info()
    # fwgjd.get_jira_info()
    cjg.combine_git_jira()


if __name__ == "__main__":
    get_data()