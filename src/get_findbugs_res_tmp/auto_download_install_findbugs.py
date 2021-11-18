import os
import src.tools.cmd_tool as ct
import src.get_findbugs_res_tmp.get_xml_from_findbugs as gxff
import src.tools.write_to_xls as wtx
import src.get_findbugs_res_tmp.Get_xls as gx
import src.get_findbugs_res_tmp.get_fixed_all_path as gfap
import configure as c

# *
def git_checkout(commit_id_list,path,is_commit=0):
    now_path = sys.path[0]
    os.chdir(path)
    data_path = c.res_path + '/datas/'
    data_path.replace('\\','/').replace('\\','/')
    print("data path : "+ data_path)
    if(os.path.exists(data_path+'xml_res')==False):
        os.mkdir(data_path+'xml_res')
    if(os.path.exists(data_path+'xml_xls')==False):
        os.mkdir(data_path+'xml_xls')
    print("now path is : " + os.getcwd())
    index = 1
    for commit_id in commit_id_list:
        # 切换分支
        print("now path is : " + os.getcwd())
        print('mvn clean install -DskipTests')
        ct.run_command('git checkout '+commit_id)
        while os.system('mvn clean install -DskipTests'):
            print("mvn clean install path : " +os.getcwd())
            if(os.getcwd().split('\\')[-1] == 'target'):
                os.chdir(os.getcwd().split('target')[0])

        pro_name = path.split('\\')[-1]
        pro_name = pro_name.split('/')[-1]
        this_path = data_path+'classes_file/'+pro_name+'/'+str(index)+'_'+commit_id
        pro_names = os.listdir('.')

        # 将classes文件夹内容拷贝到目标地
        gxff.clone_file_from_git_files(path,pro_name,this_path,this_path.split('\\compare')[0])

        print("now commit id is : "+commit_id)
        # 获取findbugs xml文件
        # findbugs_line = 'findbugs.bat -textui -progress -xml -output '+data_path + 'xml_res/res'+str(index)+'_'+commit_id + '.xml ' + os.getcwd()+'/target/classes'
        findbugs_line = 'findbugs.bat -textui -progress -xml -output '+data_path + 'xml_res/res'+str(index)+'_'+commit_id + '.xml ' + this_path
        print(findbugs_line)
        ct.run_command(findbugs_line)
        res_xml_path = data_path + 'xml_res/res'+str(index)+'_'+commit_id + '.xml '

        if(is_commit==1):
            gx.auto_get_one_xls(res_xml_path)
            gfap.get_commit_code(data_path + 'xml_xls/res'+str(index)+'_'+commit_id + '.xls ',path)
        index = index+1
    os.chdir(now_path)
    print("now path is : " + os.getcwd())

# *
def get_all_commit_between_time():
    res = []
    data = wtx.get_from_xls('get_fixed/1_get_only_bug_version.xls')
    for i in data:
        res.append(i[0])
    return res

# def auto_git_checkout_to_xml(path):
#     cids = get_all_commit_between_time()
#     git_checkout(cids,path)

# *
def auto_git_checkout_to_xls_with_codes(path):
    cids = get_all_commit_between_time()
    git_checkout(cids,path,1)


if __name__=="__main__":
    path = 'E:\projects\git\java\commons-bcel'
    auto_git_checkout_to_xls_with_codes(path)