import configure as c
import os
import src.tools.get_codes_from_file as gcff
import src.tools.write_to_xls as wtx
import src.tools.file_operator as fo


def get_codes_from_unzip_repos():
    src_path = c.res_path+'projs/'+c.pro_name+'/unzip_repos/'
    findbugs_path = c.res_path + 'projs/' + c.pro_name + '/findbugs_res/xls/'
    version_list = os.listdir(src_path)
    findbugs_res = os.listdir(findbugs_path)
    for i in findbugs_res:
        unzip_folder = src_path+i.split('.xls')[0]
        file_info = wtx.get_from_xls(findbugs_path+i,0)
        headers = file_info[0]
        all_files = []
        fo.get_all_file(unzip_folder,all_files,'java')
        for j in file_info[1:]:
            # print(j[2])
            for k in all_files:
                if k.find(j[2]) > 0:
                    print("get code line from file : "+k)
                    start = int(j[headers.index('lstart')])
                    end = int(j[headers.index('lend')])
                    codes = gcff.get_one_error_code_from_root(k,start,end)
                    j[-1] = codes
                    break
        wtx.save_to_targetpath_xls(headers,file_info[1:],c.pro_name,i.split('.xls')[0],findbugs_path)

if __name__ == "__main__":
    get_codes_from_unzip_repos()