# coding:utf-8
import requests
from lxml import html
from random import choice
import src.tools.write_to_xls as wtx
import configure as c
from time import sleep


pro_name = c.pro_name
max = c.max_jira
base_url = c.base_url
res_name = c.pro_name+'_issue_info'
max_conn = 10
headers=[
"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36 SE 2.X MetaSr 1.0",
"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36]"
]
file_headers = ['title','type','status','priority','resolution','affect version','fix version']

project_init_data_path = c.res_path+'init_data/'

def get_info(res):
    for i in range(len(res),max):
        try:
            this_url = base_url+str(i+1)
            header = {"User-Agent":choice(headers)}
            print(str(i)+"/"+str(max)+" "+this_url)
            req = requests.get(this_url,headers=header,timeout = 7)
            web = req.text
            etree = html.etree
            root = etree.HTML(web)
            req.close()
            this_res = []

            title1 = root.xpath('//title/text()')[-1].strip()
            if(title1[0:6]=='Log in'):
                continue
            type = root.xpath('//span[@id="type-val"]/text()')[-1].strip()
            status = root.xpath('//span[@id="status-val"]/span/text()')[-1].strip()
            priority = root.xpath('//span[@id="priority-val"]/text()')[-1].strip()
            resolution = root.xpath('//span[@id="resolution-val"]/text()')[-1].strip()
            affect_v = root.xpath('//span[@id="versions-val"]/text()')[-1].strip()
            fix_v = root.xpath('//span[@id="fixfor-val"]/text()')[-1].strip()
            if(affect_v == ''):
                affect_v = root.xpath('//span[@id="versions-val"]/span/span/text()')[-1].strip()
            if(fix_v == ''):
                fix_v = root.xpath('//span[@id="fixfor-val"]/span/a/text()')[-1].strip()
            this_res.append(title1)
            this_res.append(type)
            this_res.append(status)
            this_res.append(priority)
            this_res.append(resolution)
            this_res.append(affect_v)
            this_res.append(fix_v)

            res.append(this_res)
            print(this_res)
            # print(res)
        except Exception:
            print('connection wrong ,waiting 5 seconds and try again...')
            sleep(5)
            get_info(res)
    return res

def get_only_bug_version(info):
    res = []
    for i in info:
        if i[1] == 'Bug' and (i[2] == 'Closed' or i[2] == 'Resolved'):
            res.append(i)
    wtx.save_to_init_xls(file_headers,res,'only_bug',res_name+'_only_bug_version')

def get_jira_info():
    res = []
    get_info(res)
    get_only_bug_version(res)
    wtx.save_to_init_xls(file_headers,res,pro_name,res_name)

if __name__ == '__main__':
    get_jira_info()