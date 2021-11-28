import os
import src.tools.write_to_xls as wtx
import src.tools.getcodes as gc
import configure as c

# cmd = [pmd.bat path] output_path -f xml -R [rule path] -r filepath

pmd_path = c.pmd_path


# 制作结果文件
def mkdir_pmd():
    root_path = c.res_path+'/projs/' + c.pro_name
    if not os.path.exists(root_path+'/pmd_res/'):
        os.mkdir(root_path+'/pmd_res/')
    if not os.path.exists(root_path+"/pmd_res/init_data"):
        os.mkdir(root_path+"/pmd_res/init_data")
    if not os.path.exists(root_path+"/pmd_res/reduced_data"):
        os.mkdir(root_path+"/pmd_res/reduced_data")


# 使用pmd语句分析项目
def pmd_analysis_project(pro_name,format = 'csv'):
    pro_path = c.res_path+'/projs/' + c.pro_name + '/unzip_repos/'+pro_name
    res_path = c.res_path+'/projs/' + c.pro_name + '/pmd_res/init_data/' + pro_name+'.'+format
    cmd = pmd_path + " -d " + pro_path + ' -f '+ format +' -R '+c.now_pro_path+'/src/get_pmd_data/rules/rules.xml -r '+ res_path
    print(cmd)
    os.system(cmd)


# 分析所有的release版本
def anaylyse_all_release():
    rel_path = c.res_path + '/projs/' + c.pro_name + "/unzip_repos/"
    files = os.listdir(rel_path)
    for i in files:
        pmd_analysis_project(i)


# 使用pmd结果获取相应的带吗行
def get_code_from_csv():
    csv_path = c.res_path+'/projs/'+c.pro_name+'/pmd_res/init_data/'
    files = os.listdir(csv_path)
    for i in files[8:]:
        print("now get codes file is : " + i)
        data = wtx.get_from_csv(csv_path+i)
        headers = data[0]
        res = []
        has_code = False
        res_headers = headers
        if headers[-1] == 'code':
            has_code = True
        else:
            res_headers = headers+['code']
        for line in data[1:]:
            filepath = line[data[0].index('File')]
            start_line = int(line[data[0].index('Line')])
            code = gc.get_one_line(filepath, start_line)
            if not has_code:
                res.append(line + [code])
            else:
                res.append(line)
        wtx.save_as_csv(res_headers,res,csv_path+i)


# 移除pmd中相同的行（文件名代码行相同）
def remove_same_line():
    csv_path = c.res_path+'/projs/'+c.pro_name+'/pmd_res/init_data/'
    files = os.listdir(csv_path)
    res_path = c.res_path+'/projs/'+c.pro_name+'/pmd_res/reduced_data/'
    for i in files:
        print('removing the same line in files : '+i)
        data = wtx.get_from_csv(csv_path+i)
        pre = data[1]
        res = [data[1]]
        for j in data[2:]:
            if pre[1:5] == j[1:5]:
                continue
            else:
                pre = j
                res.append(j)
        wtx.save_as_csv(data[0],res,res_path+i)


# 使用fix的结果标记pmd的结果
def use_git_remark_pmd_res():
    git_res = wtx.get_from_xls(c.res_path+'/res/2_3_2_bugs_split_by_release.xls',0)
    headers = git_res[0]
    git_res = git_res[1:]
    reduced_path = c.res_path + '/projs/' + c.pro_name + '/pmd_res/reduced_data/'
    fix_version_col = headers.index('release version')
    fix_file_col = headers.index('file')
    fix_code_col = headers.index('code')
    has_used = []

    red_fils = os.listdir(reduced_path)
    for file in red_fils:
        this_version = file.split(c.pro_name+'-',maxsplit=1)[1].split('.csv')[0]
        pmd_res = wtx.get_from_csv(reduced_path+file)
        this_headers = pmd_res[0]+['git status']
        print('now analyse pmd  file is : '+file)
        for fix_line in git_res:
            # print(fix_line)
            if fix_line[fix_version_col] == this_version:
                for pmd_line in pmd_res[1:]:
                    if pmd_line[pmd_res[0].index('File')].replace('\\','/').find(fix_line[fix_file_col])>0 \
                            and fix_line[fix_code_col].strip() == pmd_line[pmd_res[0].index('code')].strip():
                        has_used.append(git_res.index(fix_line))
                        if pmd_line[-1] != 'true':
                            pmd_res[pmd_res.index(pmd_line)] = pmd_line+['true']
                            print([fix_line[fix_version_col],this_version]+[pmd_line[4]]+[pmd_line[pmd_res[0].index('code')]])
                        break
        wtx.save_as_csv(this_headers,pmd_res,reduced_path+file)
    get_no_find_git_res(headers,git_res,has_used)


# 查看那些fix没被发现
def get_no_find_git_res(headers,git_res,has_used_list):
    index = 0
    res = []
    while index < len(git_res):
        if has_used_list.count(index) > 0:
            index = index+1
            continue
        res.append(git_res[index])
        index = index + 1
    wtx.save_to_targetpath_xls(headers,res,c.pro_name,'not_used_gitline',c.res_path+'/projs/'+c.pro_name+'/pmd_res/')


# 压缩pmd结果，将相邻的行和并（没用到）
def compression_xls(filename):
    pmd_data_set = wtx.get_from_csv(filename)
    res = []
    compare_tmp = pmd_data_set[1]
    for i in pmd_data_set[1:]:
        if i[0:2] + i[4:6] == compare_tmp[0:2] + compare_tmp[4:6] and \
                int(compare_tmp[3])+1 >= int(i[2]):
            # print(res[compare_tmp.index(now)][3])
            # print(i[3])
            if(int(i[2]) > int(compare_tmp[3])):
                compare_tmp[3] = i[3]
                # print(str(pmd_data_set.index(i))+ str(now))
            continue
        res.append(compare_tmp)
        compare_tmp = i

    print(len(pmd_data_set))
    print(len(res))
    wtx.save_as_csv(pmd_data_set[0],res,'res/1_compression_data.csv')


def get_pmd_res_main_func():
    mkdir_pmd()
    anaylyse_all_release()
    get_code_from_csv()
    remove_same_line()
    use_git_remark_pmd_res()


if __name__=="__main__":
    get_pmd_res_main_func()