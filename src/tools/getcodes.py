import linecache

file_base_path = 'E:\projects\git\java\cayenne_release\cayenne-4.1.B2\cayenne-server\src\main\java/'


def get_one_line(file_path,line_number,encoding_method = 'utf-8'):
    f = open(file_path, 'r', encoding=encoding_method,errors='ignore')
    data = f.readlines()
    return data[line_number-1]


def get_one_error_code(file_path,start_line,end_line):
    f = open(file_base_path+file_path,'r')
    codes = ''
    for i in f.readlines()[start_line:end_line]:
        codes = codes + i.strip()
    res = codes.replace(' ','')
    return res


def get_one_error_code_from_root(file_path,start_line,end_line,no_space = 0):
    f = open(file_path,'r',encoding='utf-8')
    codes = ''
    for i in f.readlines()[start_line-1:end_line]:
        if(no_space):
            codes = codes + i.strip()
        else:
            codes = codes + i
    res = codes
    if(no_space):
        res = codes.replace(' ','')
    return res


if __name__=='__main__':
    file_path = 'E:/projects/git/java/commons-bcel/src/main/java/org/apache/bcel/classfile/Signature.java'
    get_one_error_code_from_root(file_path,132,133)