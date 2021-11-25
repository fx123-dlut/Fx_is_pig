def get_one_error_code_from_root(file_path,start_line,end_line,no_space = 0):
    f = open(file_path,'r',encoding='utf-8',errors='ignore')
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
    print(get_one_error_code_from_root(file_path,10,16))