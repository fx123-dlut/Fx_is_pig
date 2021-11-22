import src.get_findbugs_res.download_release_version_from_github as drvfg
import src.get_findbugs_res.use_findbugs_analysis_proj as ufap
import src.get_findbugs_res.analyse_findbugs_res as afr
import src.get_findbugs_res.mark_findbugs_res_by_gitres as mfrbg
import src.data_process.split_bugs_to_release as sbtr


def get_findbugs_res_main():
    # 获取release版本信息
    sbtr.split_by_release_main_func()

    # 下载zip包并解压编译获取classes
    drvfg.get_classes_by_zip_main_func()
    # 扫描classes获取xml文件
    ufap.get_findbugs_data_main()
    # 标记findbugs结果
    afr.analyse_findbugs_res_main_func()
    # 标记github结果
    mfrbg.mark_tp_findbugs_line_by_res()


if __name__ == "__main__":
    get_findbugs_res_main()
