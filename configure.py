import os
# github上项目名称
pro_name = 'archiva'
# jira上项目名称
jira_name = 'MRM'
# jira上版本数量
max_jira = 2021
# jira项目路径
base_url = 'https://issues.apache.org/jira/browse/MRM-'
# 本地项目路径
path = '/Users/mayang/PycharmProjects/projs/archiva'
# 输出文件保存路径

res_path = os.popen('pwd').readline().split('src')[0].replace('\n','/')
print(res_path)