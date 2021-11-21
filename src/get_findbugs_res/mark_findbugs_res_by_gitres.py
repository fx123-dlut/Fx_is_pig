import configure as c
import src.tools.write_to_xls as wtx
import os
import src.get_findbugs_res.analyse_findbugs_res as afr


def get_target_compared_file(version):
    compare_path = c.res_path + 'projs/archiva/findbugs_res/compared/'
    compare_files = os.listdir(compare_path)
    for i in compare_files:
        if i.split('_')[0].find(version) > 0:
            return compare_path + i,compare_path
    return None


def init_git_mark_res(git_res):
    for i in git_res:
        git_res[git_res.index(i)].append('fp')


def mark_tp_findbugs_line_by_res():
    root_path = c.res_path
    generate_bug_line_path = root_path+'res/2_3_2_bugs_split_by_release.xls'
    generate_bug_lines = wtx.get_from_xls(generate_bug_line_path,0)
    headers = generate_bug_lines[0]
    old_version = ''
    index = 1
    while index < len(generate_bug_lines):
        i = generate_bug_lines[index]
        version = i[headers.index('release version')]
        git_mark_res = []
        # print(version)
        if old_version != version:
            old_version = version
            compare_path,compare_root_path = get_target_compared_file(version)
            if compare_path == None:
                continue
            print(compare_path)
            compare_data = wtx.get_from_xls(compare_path,0)
            compare_headers = compare_data[0]
            # print(compare_headers)
            if compare_headers[-1] != 'git status':
                res_headers = compare_headers + ['git status']
                git_mark_res = compare_data[1:]
                init_git_mark_res(git_mark_res)
            else:
                res_headers = compare_headers
                git_mark_res = compare_data[1:]
        while old_version == version:
            git_code = generate_bug_lines[index][headers.index('code')]
            for i in git_mark_res:
                if i[compare_data[0].index('codes')].find(git_code) >= 0 and i[res_headers.index('git status')]!='fp'\
                        and i[compare_data[0].index('file_path')] == generate_bug_lines[index][headers.index('file')]:
                    i[-1] = 'tp'
                    print('asdasd')
            index = index + 1
            if index >= len(generate_bug_lines):
                break
            version = generate_bug_lines[index][headers.index('release version')]
        wtx.save_to_targetpath_xls(res_headers,git_mark_res,c.pro_name,compare_path.split('compared/')[1].split('.xls')[0],compare_root_path)
        index = index+ 1


if __name__ == "__main__":
    mark_tp_findbugs_line_by_res()