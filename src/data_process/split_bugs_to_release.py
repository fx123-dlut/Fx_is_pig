import src.tools.write_to_xls as wtx
import src.tools.time_operator as to
import configure as c
import os
import src.collect_datas.from_git_get_releaseversion as fggr


# 给所有的bug line信息中增加commit id和一些其他的信息
def get_every_bug_time(re_write = 0):
    res = []
    all_init_bugs_filename = c.res_path + "/res/2_3_from_show_every_lines.csv"
    all_init_bugs_data = wtx.get_from_csv(all_init_bugs_filename)
    all_commit_id_file = c.res_path+ "/res/combine.xls"
    all_commit_id_data = wtx.get_from_xls(all_commit_id_file,0)
    headers = all_init_bugs_data[0]+all_commit_id_data[0][0:2]
    if re_write == 0 and os.path.exists(c.res_path + "/res/2_3_1_oneline_onebug_more_detail.csv"):
        return wtx.get_from_csv(c.res_path + "/res/2_3_1_oneline_onebug_more_detail.csv")[1:],headers
    for i in all_init_bugs_data[1:]:
        for j in all_commit_id_data[1:]:
            if i[0][0:8] == j[0][0:8]:
                this_res = i+j[0:2]
                # print(this_res)
                res.append(this_res)
                # return
                break
    wtx.save_as_csv(headers,res,c.res_path + "/res/2_3_1_oneline_onebug_more_detail.csv")
    return res,headers


def split_bug_to_release_by_time():
    res = []
    release_file = c.res_path + "init_data/git_release_version_with_commitid.xls"
    release_info = wtx.get_from_xls(release_file,0)
    tag_res = []
    for i in release_info[1:]:
        tag_res.append(i[0])
    all_bug_info,headers1 = get_every_bug_time()
    headers = headers1 + release_info[0]
    index = 1

    if os.path.exists(release_file):
        return wtx.get_from_xls(release_file),tag_res

    for i in all_bug_info:
        while to.compare_time(i[-1],release_info[index][-1]) and index < len(release_info)-1:
            index = index + 1
        if index == 1:
            res.append(i+['','',''])
            continue
        res.append(i+release_info[index-1])
        print(i+release_info[index-1])
    wtx.save_as_csv(headers,res,c.res_path + "/res/2_3_2_bugs_split_by_release.csv")
    return res,tag_res


def split_by_release_main_func():
    res ,release_info=split_bug_to_release_by_time()
    return release_info


if __name__ == "__main__":
    split_bug_to_release_by_time()