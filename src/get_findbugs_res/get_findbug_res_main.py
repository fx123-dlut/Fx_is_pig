import src.get_findbugs_res.get_classes_by_mvninstall as gcbm
import src.get_findbugs_res.download_release_version_from_github as drvfg
import src.get_findbugs_res.use_findbugs_analysis_proj as ufap


def get_findbugs_res_main():
    # gcbm.get_classes_main_func()
    drvfg.get_classes_by_zip_main_func()
    ufap.get_findbugs_data_main()


if __name__ == "__main__":
    get_findbugs_res_main()
