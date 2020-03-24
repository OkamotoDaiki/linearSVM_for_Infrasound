import pandas as pd
import os
import shutil
import glob
import OperateFpath


def main():
    output_csv_fpath = "./output_csv_against_mag"
    try:
        shutil.rmtree(output_csv_fpath)
        os.mkdir(output_csv_fpath)
    except FileNotFoundError:
        os.mkdir(output_csv_fpath)

    score_fpath = "./output_csv"
    score_folders = OperateFpath.GetAllMultiFolder(score_fpath)
    print(score_folders)
    for score_folder in score_folders:
        output_score_fpath = output_csv_fpath + "/" + score_folder
        os.mkdir(output_score_fpath)

        feature_mode_fpath = score_fpath + "/" + score_folder
        feature_mode_folders = OperateFpath.GetAllMultiFolder(feature_mode_fpath)
        for feature_mode_folder in feature_mode_folders:
            output_feature_mode_fpath = output_score_fpath + "/" + feature_mode_folder
            os.mkdir(output_feature_mode_fpath)

            threshold_mag_fpath = feature_mode_fpath + "/" + feature_mode_folder
            threshold_mag_folders = OperateFpath.GetAllMultiFolder(threshold_mag_fpath)
            csv_list = []
            for threshold_mag_folder in threshold_mag_folders:
                get_csv_fpath = threshold_mag_fpath + "/" + threshold_mag_folder + "/*.csv"
                csv_names = glob.glob(get_csv_fpath)
                for csv_name in csv_names:
                    csv_list.append(csv_name)
            #copy csv
            for csv_fpath in csv_list:
                shutil.copy(csv_fpath, output_feature_mode_fpath)
            print("copy {}, {}".format(score_folder, feature_mode_folder))

if __name__=="__main__":
    main()