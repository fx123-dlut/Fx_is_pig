import os
# github上项目名称
pro_name = 'maven-dependency-plugin'

# jira上项目名称
jira_name = 'MDEP'
# jira上版本数量
max_jira = 780





# jira项目路径
base_url = 'https://issues.apache.org/jira/browse/'+jira_name+'-'
# base_url = 'https://issues.apache.org/jira/browse/TIKA-'

# 本地项目路径
# path = 'E:/projects/git/java/sis/'
path = 'G:/fx/pro/'+pro_name+"/"
# 输出文件保存路径

# res_path = 'E:/projects/py/shiwanhuoji/Fx_is_pig/'
res_path = 'G:/fx/data/'+pro_name+'/'

pmd_path = 'E:/tools/漏洞检测/PMD/pmd-bin-6.36.0/bin/pmd.bat'

now_pro_path = os.getcwd().replace('\\','/').split('src')[0]