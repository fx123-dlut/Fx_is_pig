import xml.dom.minidom as dom
import xlwt
import os

def get_all_file_name(path):
    res = []
    files = os.listdir(path+'compare/datas/xml_res')
    for i in files:
        res.append(i)
    return res


# *
def get_xls_by_true_filename(pro_path,file_path):
    if(type(file_path)!='list'):
        file_path = [file_path]
    for filename in file_path:
        line = 0 #有几列
        row = 0 #目前第几行

        #创建表格
        xls = xlwt.Workbook()
        sht1 = xls.add_sheet('version1')
        heads = ["method_name","method_sig","file_path","class_name","lstart","lend","priority","catogeray","codes"]

        for head in heads:
            sht1.write(row,line,head)
            line = line+1
        row = row+1
        #读取信息
        filename = str(filename)
        tree = dom.parse(pro_path+"compare/datas/xml_res/"+filename)
        root = tree.documentElement
        #proname = root.getElementsByTagName("Project")[0].getAttribute("projectName")
        print("filename _ "+ filename)

        bugs = root.getElementsByTagName("BugInstance")

        for bug in bugs:
            line = 0
            #print("---------------------BugInstance--------------------")
            desc = bug.getAttribute("type")
            priority = bug.getAttribute("priority")

            #print(desc + " " + priority+" ",end='')



            if bug.getElementsByTagName("Method"):
                croot = bug.getElementsByTagName("Method")[0]
                classname = croot.getAttribute("classname")
                signature = croot.getAttribute("signature")
                method_name = croot.getAttribute("name")

              #  print(classname+" "+signature+" "+method_name+" ",end='/n')

                root2 = croot.getElementsByTagName("SourceLine")[0]
                sourcepath = root2.getAttribute("sourcepath")
                start = root2.getAttribute("start")
                end = root2.getAttribute("end")
                #print(sourcepath+" "+ start+" "+end)
                sht1.write(row,line,method_name)
                line = line+1
                sht1.write(row,line,signature)
                line = line+1
                sht1.write(row,line,sourcepath)
                line = line+1
                sht1.write(row,line,classname)
                line = line+1
                sht1.write(row,line,start)
                line = line+1
                sht1.write(row,line,end)
                line = line+1
                sht1.write(row,line,priority)
                line = line+1
                sht1.write(row,line,desc)
                line = line+1
                row = row+1
        if (os.path.exists(pro_path+'compare/datas/xml_xls') == False):
            os.mkdir(pro_path+'compare/datas/xml_xls')
        xls.save(pro_path+"compare/datas/xml_xls/"+filename.split('.xml')[0]+".xls")

def auto_get_xls(pro_path):
    if(os.path.exists(pro_path+'compare/datas/xml_xls') == False):
        os.mkdir(pro_path+'compare/datas/xml_xls')
    file_name = get_all_file_name(pro_path)
    get_xls_by_true_filename(pro_path,file_name)

# *
def auto_get_one_xls(pro_path):
    get_xls_by_true_filename(pro_path.split('compare')[0].replace('\\','/'),pro_path.split('xml_res/')[1])

if __name__ == "__main__":
    pro_path = 'E:/projects/py/numpytest/test/venv/Include/find_bug_lines/Thesis_2022/'
    auto_get_xls(pro_path)