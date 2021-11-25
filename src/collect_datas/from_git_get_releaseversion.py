import os
import src.tools.write_to_xls as wtx
import src.tools.cmd_tool as ct
import configure as c

release_file = 'git_release_version_with_commitid'


def get_all_tag_name(path,filter = 0):
    os.chdir(path)
    cmd = 'git tag'
    run_res = os.popen(cmd).readlines()
    tags = []
    for i in run_res:
        if  filter == 1 and (i.find('alpha') > 0 or i.find('beta') > 0 or i.find(c.pro_name+'-') < 0 or len(i.split('.')) == 1) :
            continue
        print(i)
        tags.append(i.replace('\n',''))
    print('all tags is :')
    print(tags)
    return tags


def get_all_tag_with_commitid(path):
    res = []
    headers = ['release version','commit id','commit time']
    tags = get_all_tag_name(path)
    for i in tags:
        cmd = 'cd '+path + " && git show "+i
        print(cmd)
        run_res = ct.run_command(cmd)
        comid = ''
        date = ''
        for line in run_res:
            if line[:7] == 'commit ':
                comid = line.split('commit ')[1].replace('\n','').strip()
            if line[:6] == 'Date: ':
                date = line.split('Date: ')[1].replace('\n','').strip()
            if comid != '' and date != '':
                res.append([i,comid,date])
                break

    res.reverse()
    print(res)
    wtx.save_to_init_xls(headers,res,c.pro_name,release_file)


def get_release_all_info(re_write = 1):
    res = []
    release_file_path = c.res_path+"init_data/"+release_file+'.xls'
    all_commit_path = c.res_path+"init_data/git_log_info.xls"
    if not os.path.exists(release_file_path) or re_write == 1:
        get_all_tag_with_commitid(c.path)
    all_release_commit_id = wtx.get_from_xls(release_file_path)
    # print(all_release_commit_id)
    all_commit_id = wtx.get_from_xls(all_commit_path)
    for i in all_release_commit_id:
        for j in all_commit_id:
            if i[1] == j[1]:
                print(i[1] + " " + j[1])
                res.append([i[0]]+j)
                break
    for i in res:
        print(i)
    wtx.save_to_init_xls('',res,c.pro_name,'2_release_all_info')


if __name__ == "__main__":
    get_release_all_info(1)