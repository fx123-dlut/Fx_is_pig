import src.tools.write_to_xls as wtx
import os
import configure as c


def get_data(file_path):
    if not os.path.exists(file_path):
        return []
    if file_path[-3:] == 'xls':
        return wtx.get_from_xls(file_path,0)
    return wtx.get_from_csv(file_path)


def get_git_res_by_release():
    file_path = c.res_path+'/res/2_3_2_bugs_split_by_release.csv'
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


def get_summary(path,tools_folders):
    folders = os.listdir(path)
    print(path)
    headers = ['pro_name','release_name','checkstyle_fp_res','tp_diff_res','tp_fix_res','tp_combine_res','FN',
               'pmd_fp_res','tp_diff_res','tp_fix_res','tp_combine_res','FN',
               'findbugs_fp_res','tp_diff_res','tp_fix_res','tp_combine_res','FN']
    all_res = []
    res_map = {}
    git_res = get_git_res_by_release()
    for i in folders:
        pro_res = []
        pro_res.append(i)
        pro_res_path = path+i+'/projs/'+i
        print(pro_res_path)
        for j in tools_folders:
            csv_path = j[0]
            try:
                files = os.listdir(pro_res_path+csv_path+"/")
            except FileNotFoundError as e:
                print(repr(e))
                pro_res = pro_res + [0,0,0,0,0]
                continue
            for f in files:
                pro_res =[]
                cnt = 0
                tp_fix_res = 0
                tp_diff_res = 0
                tp_combine_res = 0
                print("     now summary file is "+ pro_res_path+csv_path + '/' + f)
                try:
                    this_rel_git_res = git_res[f.split('.csv')[0]]
                except Exception as e:
                    try:
                        this_rel_git_res = git_res[f.split('_')[0]]
                    except Exception:
                        continue
                all_git = len(this_rel_git_res)
                datas = get_data(pro_res_path+csv_path + '/' + f)
                for d in datas:
                    cnt = cnt + 1
                    if d[-2] == 'true' or d[-2] == 'new' or d[-2] == 'TRUE':
                        tp_fix_res = tp_fix_res+1
                    if d[-1] == 'true' or d[-1] == 'new' or d[-2] == 'TRUE':
                        tp_diff_res = tp_diff_res+1
                    if (d[-2] == 'true' or d[-2] == 'new' or d[-2] == 'TRUE') or\
                            (d[-1] == 'true' or d[-1] == 'new' or d[-2] == 'TRUE'):
                        tp_combine_res = tp_combine_res+1
                # if j[1] == '':
                #     others = all_git-tp_combine_res
                # else:
                #     others = max(len(get_data(pro_res_path+j[1] + '/not_used_gitline.xls'))-1,len(get_data(pro_res_path+j[1] + '/not_used_gitline.csv'))-1)
                if j[1] == '':
                    others = all_git-tp_combine_res
                else:
                    others = all_git-tp_fix_res
                pro_res.append(cnt-tp_combine_res)
                pro_res.append(tp_diff_res)
                pro_res.append(tp_fix_res)
                pro_res.append(tp_combine_res)
                pro_res.append(others)
                res_map.setdefault(f.split('.csv')[0].split('_')[0])
                if res_map[f.split('.csv')[0].split('_')[0]] == None:
                    res_map[f.split('.csv')[0].split('_')[0]] = [i,f.split('.csv')[0].split('_')[0]]
                    index = (int)(tools_folders.index(j)/2)
                    res_map[f.split('.csv')[0].split('_')[0]] = res_map[f.split('.csv')[0].split('_')[0]] + [0 for i in range(index*5)]
                res_map[f.split('.csv')[0].split('_')[0]] = res_map[f.split('.csv')[0].split('_')[0]]+pro_res
        print(res_map.values())
    wtx.save_as_csv(headers,res_map.values(),path+'summary_datas.csv')


if __name__=="__main__":
    path = c.res_path.split(c.pro_name)[0]
    tools_folder = [['/checkstyle_res/diff_res/','/checkstyle_res/'],['/pmd_res/diff_data/','/pmd_res/'],['/findbugs_res/compared','']]
    get_summary(path,tools_folder)
    # get_git_res_by_release()