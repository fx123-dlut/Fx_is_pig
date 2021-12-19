import os
import configure as c
import src.tools.write_to_xls as wtx
from time import sleep
import src.tools.file_operator as fo


def get_all_release_version_after_maven():
    all_release_version_file = c.res_path + "init_data/git_release_version_with_committime.xls"
    all_release_version_data = wtx.get_from_xls(all_release_version_file)
    for i in all_release_version_data:
        #  window下用此命令
        # os.system('cd '+c.path.split(':')[0])
        # 切换到对应项目目录
        os.chdir(c.path)
        # git checkout archiva1.1 切换到指定的release
        cmdline = 'git checkout -f ' + i[0]
        print("now run : " + cmdline)
        os.system(cmdline)
        sleep(5)
        # maven编译项目
        os.system('mvn clean install -DskipTests -Drat.skip=true')
        fo.copy_one_version_to_target_path(i[0])


def get_classes_main_func():
    get_all_release_version_after_maven()
    fo.copy_classes_to_targetpath()


if __name__ == "__main__":
    get_classes_main_func()