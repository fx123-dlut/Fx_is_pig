import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
import src.tools.get_all_file_path as gafp
import src.tools.write_to_xls as wtx
import src.tools.getcodes as gc

# def get_all_fixed_data(pro_path,version_num = 5):
#     res = []
#     for i in range(version_num):
#         file_path = pro_path+'/compare/datas/xml_xls/'+str(i)+'.xls'
#         d = wtx.get_from_xls(file_path)
#         # print(str(i)+" version file : "+file_path)
#         res.append(d)
#     return res
#
# # 获取指定路径下所有文件的绝对路径
# def match_paths(pro_path,file_path,file_type,save = 0):
#     res = []
#     long_file_path = []
#     os.chdir(file_path)
#     pro_names = os.listdir('.')
#     for i in pro_names:
#         long_file_path.append(gafp.get_all_file_path(file_path+'/'+i,file_type))
#     compare_res = get_all_fixed_data(pro_path)
#     for i in range(5):
#         this_v_fb = compare_res[i]
#         for j in this_v_fb:
#             for long in long_file_path[i]:
#                 long = long.replace('\\','/')
#                 if(j[2] in long):
#                     res.append([i]+j+[long])
#     if(save):
#         wtx.save_as_csv([],res,pro_path+'compare/datas/res/2_fixed_data_with_long_path.csv')
#     return res
#
# def get_findbugs_code_lines(findbugs_with_path,pro_path):
#     res = []
#     res_block = []
#     for i in findbugs_with_path:
#         # print([i[-5]]+[i[-4]]+[i[-1]])
#         code = gc.get_one_error_code_from_root(i[-1],int(i[-5]),int(i[-4]))
#         res_block.append(i+[code])
#         for line in range(int(i[-4])-int(i[-5])+1):
#             res.append(i+[code.split('\n')[line].strip(),int(i[-5])+line])
#     # for i in res:
#     #     print(i)
#     wtx.save_as_csv([], res, pro_path + 'compare/datas/res/2_fixed_data_with_code_line.csv')
#     wtx.save_as_csv([], res_block, pro_path + 'compare/datas/res/2_fixed_data_with_code_block.csv')
#     return res
#
# def conversion_format(fixed_init_code_data,tar_path,pro_path):
#     res = []
#     headers = ['belong to release_time','release_num','file_name','line_number','line']
#     for i in fixed_init_code_data[1:]:
#         this_data = ['',i[0],i[-3].split(tar_path)[1].split('/',2)[2],i[-1],i[-2]]
#         res.append(this_data)
#     wtx.save_as_csv(headers, res, pro_path + 'compare/datas/res/2_fixed_conversion_format.csv')
#     return res
#
# def get_fixed_with_code_line(pro_path,target_path,rewrite = 0):
#     if(rewrite or os.path.exists(pro_path + 'compare/datas/res/2_fixed_data_with_code_line.csv')==False):
#         fb_with_path = match_paths(pro_path,target_path,"java",1)
#         fb_with_codes = get_findbugs_code_lines(fb_with_path,pro_path)
#     else:
#         fb_with_codes = wtx.get_from_csv(pro_path + 'compare/datas/res/2_fixed_data_with_code_line.csv')
#     fixed_info = conversion_format(fb_with_codes,target_path,pro_path)
#     return fixed_info
#
# def get_fixed_tp(pro_path):
#     fixed_blocks = [[],[],[],[],[]]
#     data = wtx.get_from_csv(pro_path + 'compare/datas/res/2_fixed_data_with_code_block.csv')
#     for i in data[1:]:
#         fixed_blocks[int(i[0])].append(i)
#     for i in range(4):
#         for now in fixed_blocks[i]:
#             print(fixed_blocks[i][1][-1])
#             for next in fixed_blocks[i+1]:
#                 if(now[3]==next[3] and now[-1]==next[-1]):
#                     now[-1] = 'fp'
#                     break
#             if(now[-1]!='fp'):
#                 now[-1] = 'tp'
#     res = []
#     for i in fixed_blocks:
#         res = res + i
#     wtx.save_as_csv([],res,pro_path + 'compare/datas/res/1_fixed_tp.csv')

#########################################################################################

# 9月14号后修改
# get_commit_code(xls_file_path,tar_path):
# 对单个commit获取代码行
# 输入xls数据，扫码项目的根路径

#########################################################################################

# 获取commit下所有的指定后缀类型的文件,并匹配xls文件中的数据
def match_commit_path(xls_data,tar_path,file_type='java',save = 0):
    fnames = gafp.get_all_file_path(tar_path, file_type)
    for i in xls_data:
        for j in fnames:
            if i[2] in j:
                i.append(j)
    return xls_data

# *
def get_commit_error_code_lines(headers,findbugs_with_path,pro_path):
    res = []
    res_block = []
    for i in findbugs_with_path:
        code = gc.get_one_error_code_from_root(i[-1],int(i[4]),int(i[5]))
        res_block.append(i+[code])
    wtx.save_as_xls_to_path(headers, res_block,'with_code_line', pro_path)
    return res

# 获取该commit下的代码行
def get_commit_code(xls_file_path,tar_path):
    xls_data = wtx.get_from_xls(xls_file_path,0)
    data_with_file_names = match_commit_path(xls_data[1:],tar_path)
    get_commit_error_code_lines(xls_data[0]+['file path','codes'],data_with_file_names, xls_file_path)

if __name__=="__main__":
    pro_path = 'E:/projects/py/numpytest/test/venv/Include/find_bug_lines/Thesis_2022/'
    target_path = "E:/projects/git/java/commons-vfs-release"
    tar_path = 'E:/projects/git/java/commons-bcel'
    get_commit_code(pro_path+'compare/datas/xml_xls/res1_190dee5fa3b5374f95ae8b3673705802789ed0a7.xls',tar_path)
    # get_fixed_with_code_line(pro_path,target_path)
    # get_fixed_tp(pro_path)