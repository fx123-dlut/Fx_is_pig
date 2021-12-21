import src.tools.write_to_xls as wtx
import os
import configure as c


# 标记checkstyle结果
def mark_cs_res_by_git():
    git_res = wtx.get_from_csv(c.res_path+'/res/2_3_2_bugs_split_by_release.csv')
    headers = git_res[0]
    git_res = git_res[1:]
    fix_version_col,fix_file_col,fix_code_col = headers.index('release version'),headers.index('file'),headers.index('code')
    has_used = []

    reduced_path = c.res_path + '/projs/' + c.pro_name + '/checkstyle_res/csv_res/'
    cs_files = os.listdir(reduced_path)
    for file in cs_files:
        this_version = file.split(c.pro_name + '-', maxsplit=1)[-1].split('.csv')[0]
        cs_res = wtx.get_from_csv(reduced_path+file)
        this_headers = cs_res[0] + ['git status']
        cs_res = cs_res[1:]
        print('now analyse checkstyle file is : '+file)
        for fix_line in git_res:
            if fix_line[fix_version_col] == this_version:
                for cs_line in cs_res[1:]:
                    if cs_line[this_headers[0].index('file')].replace('\\', '/').find(fix_line[fix_file_col]) > 0 \
                            and fix_line[fix_code_col].strip() == cs_line[this_headers.index('code')].strip():
                        has_used.append(git_res.index(fix_line))
                        if cs_line[-1] != 'true':
                            cs_res[cs_res.index(cs_line)] = cs_line + ['true']
                            print([fix_line[fix_version_col], this_version] + [cs_line[4]] + [cs_line[this_headers.index('code')]])
                        break
        wtx.save_as_csv(this_headers, cs_res, reduced_path + file)
        get_no_find_git_res(headers, git_res, has_used)


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
    wtx.save_as_csv(headers,res,c.res_path+'/projs/'+c.pro_name+'/checkstyle_res/'+'not_used_gitline.csv')


if __name__ == "__main__":
    mark_cs_res_by_git()