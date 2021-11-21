import src.get_findbugs_res.download_release_version_from_github as drvfg
import src.get_findbugs_res.use_findbugs_analysis_proj as ufap
import src.get_findbugs_res.analyse_findbugs_res as afr


def get_findbugs_res_main():
    drvfg.get_classes_by_zip_main_func()
    ufap.get_findbugs_data_main()
    afr.analyse_findbugs_res_main_func()

if __name__ == "__main__":
    get_findbugs_res_main()