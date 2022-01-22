import src.tools.write_to_xls as wtx
import os
import configure as c
import src.tools.time_operator as to


# 从文件获取数据，消除csv和xls文件的影响
def get_data(file_path):
    if not os.path.exists(file_path):
        return []
    if file_path[-3:] == 'xls':
        return wtx.get_from_xls(file_path,0)
    return wtx.get_from_csv(file_path)


# 获取所有的git bug信息
def get_git_res_by_release(path = c.res_path):
    file_path = path+'/res/2_3_2_bugs_split_by_release.csv'
    data = wtx.get_from_csv(file_path)
    res = {}
    rel_col = data[0].index('release version')
    for i in data[1:]:
        res.setdefault(i[rel_col])
        if res[i[rel_col]] == None:
            res[i[rel_col]] = []
        res[i[rel_col]].append(i)
    print(res.keys())
    return res


# 获取所有的commit release版本信息
def get_all_release_info(path):
    file_path = path+'/init_data/git_release_version_with_commitid.xls'
    data = wtx.get_from_xls(file_path)
    res = []
    for i in data:
        res.append([i[0].split('/')[-1],i[2]])
    return res


# def get_summary(path,tools_folders):
#     folders = os.listdir(path)
#     print(path)
#     headers = ['pro_name','release_name','checkstyle_fp_res','tp_diff_res','tp_fix_res','tp_combine_res','FN',
#                'pmd_fp_res','tp_diff_res','tp_fix_res','tp_combine_res','FN',
#                'findbugs_fp_res','tp_diff_res','tp_fix_res','tp_combine_res','FN']
#     all_res = []
#     res_map = {}
#     git_res = get_git_res_by_release()
#     for i in folders:
#         pro_res = []
#         pro_res.append(i)
#         pro_res_path = path+i+'/projs/'+i
#         print(pro_res_path)
#         for j in tools_folders:
#             csv_path = j[0]
#             try:
#                 files = os.listdir(pro_res_path+csv_path+"/")
#             except FileNotFoundError as e:
#                 print(repr(e))
#                 pro_res = pro_res + [0,0,0,0,0]
#                 continue
#             for f in files:
#                 pro_res =[]
#                 cnt = 0
#                 tp_fix_res = 0
#                 tp_diff_res = 0
#                 tp_combine_res = 0
#                 print("     now summary file is "+ pro_res_path+csv_path + '/' + f)
#                 try:
#                     this_rel_git_res = git_res[f.split('.csv')[0]]
#                 except Exception as e:
#                     try:
#                         this_rel_git_res = git_res[f.split('_')[0]]
#                     except Exception:
#                         continue
#                 all_git = len(this_rel_git_res)
#                 datas = get_data(pro_res_path+csv_path + '/' + f)
#                 for d in datas:
#                     cnt = cnt + 1
#                     if d[-2] == 'true' or d[-2] == 'new' or d[-2] == 'TRUE':
#                         tp_fix_res = tp_fix_res+1
#                     if d[-1] == 'true' or d[-1] == 'new' or d[-2] == 'TRUE':
#                         tp_diff_res = tp_diff_res+1
#                     if (d[-2] == 'true' or d[-2] == 'new' or d[-2] == 'TRUE') or\
#                             (d[-1] == 'true' or d[-1] == 'new' or d[-2] == 'TRUE'):
#                         tp_combine_res = tp_combine_res+1
#                 # if j[1] == '':
#                 #     others = all_git-tp_combine_res
#                 # else:
#                 #     others = max(len(get_data(pro_res_path+j[1] + '/not_used_gitline.xls'))-1,len(get_data(pro_res_path+j[1] + '/not_used_gitline.csv'))-1)
#                 if j[1] == '':
#                     others = all_git-tp_combine_res
#                 else:
#                     others = all_git-tp_fix_res
#                 pro_res.append(cnt-tp_combine_res)
#                 pro_res.append(tp_diff_res)
#                 pro_res.append(tp_fix_res)
#                 pro_res.append(tp_combine_res)
#                 pro_res.append(others)
#                 res_map.setdefault(f.split('.csv')[0].split('_')[0])
#                 if res_map[f.split('.csv')[0].split('_')[0]] == None:
#                     res_map[f.split('.csv')[0].split('_')[0]] = [i,f.split('.csv')[0].split('_')[0]]
#                     index = (int)(tools_folders.index(j)/2)
#                     res_map[f.split('.csv')[0].split('_')[0]] = res_map[f.split('.csv')[0].split('_')[0]] + [0 for i in range(index*5)]
#                 res_map[f.split('.csv')[0].split('_')[0]] = res_map[f.split('.csv')[0].split('_')[0]]+pro_res
#         print(res_map.values())
#     wtx.save_as_csv(headers,res_map.values(),path+'summary_datas.csv')


# 获取工具的详细统计信息


# 获取pmd和checkstyle这两种工具的正误报结果信息
def get_tools_res(path,rel_map,tool_path,tool_name):
    pmd_path = path + tool_path
    try:
        files = os.listdir(pmd_path)
    except FileNotFoundError as e:
        return
    for i in files:
        datas = get_data(pmd_path+i)
        git_num = 0
        diff_num = 0
        for d in datas[1:]:
            if d[-2] == 'true' or d[-2] == 'new' or d[-2] == 'TRUE':
                git_num+=1
            if d[-1] == 'true' or d[-1] == 'new' or d[-1] == 'TRUE':
                diff_num+=1
        file_rel = i.split('.csv')[0].split('.xls')[0]
        temp = rel_map.get(file_rel)
        all = len(datas)-1
        if all < 0:
            all = 0
        temp.setdefault(tool_name,[git_num,diff_num,all])
        rel_map.update({file_rel:temp})


# 根据findbugs的compare file name查询release 版本并返回对应的version
def from_compare_to_file_version(file_path,compare_file_name):
    data = get_data(file_path.split('/projs/')[0]+'/init_data/git_release_version_with_commitid.xls')
    for i in data:
        if compare_file_name.find(i[0].split('/')[-1]) > 0:
            return i[0].split('/')[-1]
    return None


# 根据findbugs的compare file name 获取对应的release version
def get_version(path,file_name):
    if len(file_name.split("@")) == 2:
        return file_name.split('.csv')[0].split('.xls')[0].split('@')[1]
    elif len(file_name.split('_')) == 2:
        return file_name.split('.csv')[0].split('.xls')[0].split('_')[1]
    elif len(file_name.split('@')) == 1 and len(file_name.split('_')) == 1:
        return file_name.split('.csv')[0].split('.xls')[0]
    return from_compare_to_file_version(path,file_name)


# 获取findbugs的详细统计信息
def get_findbugs_res(path,rel_map,tool_path,tool_name):
    fb_path = path + tool_path
    try:
        files = os.listdir(fb_path)
    except FileNotFoundError as e:
        return
    for i in files:
        datas = get_data(fb_path + i)
        git_num = 0
        diff_num = 0
        for d in datas[1:]:
            if d[-2] == 'true' or d[-2] == 'new' or d[-2] == 'TRUE':
                diff_num += 1
            if d[-1] == 'true' or d[-1] == 'new' or d[-1] == 'TRUE':
                git_num += 1
        file_rel = get_version(path,i)
        temp = rel_map.get(file_rel)
        all = len(datas) - 1
        if all < 0:
            all = 0
        try:
            temp.setdefault(tool_name, [git_num, diff_num, all])
        except AttributeError as e:
            print(path+ " " + i)
            print(repr(e))
            continue
        rel_map.update({file_rel: temp})


# 将结果保存到文件中
def save_to_csv(res,pro_names):
    body = []
    headers = ['pro_name','release name','bug num','pmd git compared sum','pmd self compared sum','pmd all sum',
               'checkstyle git compared sum', 'checkstyle self compared sum', 'checkstyle all sum',
               'findbugs git compared sum', 'findbugs self compared sum', 'findbugs all sum']
    for i in res:
        rel_keys = i.keys()
        for k in rel_keys:
            now_res = [k]
            data = i.get(k)
            tools_name = data.keys()
            now_res.append(data.get('bug_num'))
            if 'pmd' in tools_name:
                now_res += data.get('pmd')
            else:
                now_res += [0,0,0]
            if 'checkstyle' in tools_name:
                now_res += data.get('checkstyle')
            else:
                now_res += [0,0,0]
            if 'findbugs' in tools_name:
                now_res += data.get('findbugs')
            else:
                now_res += [0,0,0]
            body.append([pro_names[res.index(i)]] + now_res)
    wtx.save_as_csv(headers,body,c.res_path.split(c.pro_name)[0]+'summary_datas.csv')


# 获取每个release对应的bugfix版本的commit数量
def get_bugs_nums(root_path,rel_map,releases):
    pro_root_path = root_path.split('/projs/')[0]
    commit_path = pro_root_path + '/res/1_get_only_bug_version_all_match.xls'
    commit_data = get_data(commit_path)
    cnt = 0
    index = 0
    now_release_version = releases[index][0]
    temp = rel_map.get(now_release_version)
    for i in commit_data[1:]:
        commit_time = i[1]
        cnt += 1
        if not to.compare_time(releases[index][1],commit_time):
            temp.setdefault('bug_num',cnt)
            rel_map.update({now_release_version: temp})
            cnt = 0
            index += 1
            if index >= len(releases):
                break
            now_release_version = releases[index][0]
            temp = rel_map.get(now_release_version)
    print(pro_root_path)


# 获取单个项目的具体信息
def get_datas_from_tool_res(path,releases):
    rel_map = {}
    for i in releases:
        rel_map.setdefault(i[0],{})
    get_bugs_nums(path,rel_map,releases)
    print(rel_map)
    get_tools_res(path,rel_map,'/pmd_res/diff_data/','pmd')
    get_tools_res(path,rel_map,'/checkstyle_res/diff_res/','checkstyle')
    get_findbugs_res(path,rel_map,'/findbugs_res/compared/','findbugs')
    return rel_map


# 获取所有项目的所有工具信息
def get_all_data(path):
    folders = os.listdir(path)
    res = []
    for folder in folders:
        now_path = path+folder
        if os.path.isdir(now_path):
            res_path = now_path+'/projs/'+folder+'/'
            print("now summary project path is "+res_path)
            try:
                releases = get_all_release_info(now_path)
            except FileNotFoundError as e:
                print(repr(e))
                continue
            res.append(get_datas_from_tool_res(res_path,releases))
    save_to_csv(res,folders)


def test():
    data = get_data('G:/fx/data/reef/projs/reef/checkstyle_res/diff_res/reef-project-0.10.0-incubating.csv')
    for i in data:
        print(i[-2])


if __name__=="__main__":
    path = c.res_path.split(c.pro_name)[0]
    # print(path)

    # tools_folder = [['/checkstyle_res/diff_res/','/checkstyle_res/'],['/pmd_res/diff_data/','/pmd_res/'],['/findbugs_res/compared','']]
    # get_summary(path,tools_folder)
    # get_git_res_by_release()

    get_all_data(path)
    # test()
