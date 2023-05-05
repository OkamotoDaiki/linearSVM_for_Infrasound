from subscript import operate_fpath
import glob
import sys
import shutil
import os
import json
"""
/output_plot_data
    ├ mfcc
    │　└ Place
    │       └ /*.csv
    ├ delta-ceps
    └ mfcc_and_delta-ceps
"""
def generate_save_directory(save_fpath, read_fpath, feature_modes):
    """ 
    ├ mfcc
    │　└ /*.csv written place_name and performanceValue
    │
    ├ delta-ceps
    └ mfcc_and_delta-ceps
    """
    def get_place_name_wildcard(csv_list):
        place_names = []
        for csv_fpath in csv_list:
            place_name = csv_fpath.split("/")[-1].split("_")[0] + "_" +  csv_fpath.split("/")[-1].split("_")[1]
            place_names.append(place_name)
        return place_names

    def get_place(read_fpath):
        read_score_folders = operate_fpath.get_all_multi_folder(read_fpath)
        for score_folder in read_score_folders:
            read_score_fpath = read_fpath + "/" + score_folder
            feature_mode_folders = operate_fpath.get_all_multi_folder(read_score_fpath)
            for feature_mode_folder in feature_mode_folders:
                read_feature_mode_fpath = read_score_fpath + "/" + feature_mode_folder
                if feature_mode_folder == feature_modes[2]:
                    csv_place_name_list = glob.glob(read_feature_mode_fpath + "/*.csv")
                    place_names = get_place_name_wildcard(csv_place_name_list)
                    break
        return place_names

    try:
        shutil.rmtree(save_fpath)
        os.mkdir(save_fpath)
    except FileNotFoundError:
        os.mkdir(save_fpath)

    place_names = get_place(read_fpath)

    for feature_mode in feature_modes:
        save_feature_mode_fpath = save_fpath + "/" + feature_mode
        os.mkdir(save_feature_mode_fpath)
        for place_name in place_names:
            save_place_fpath = save_feature_mode_fpath + "/" + place_name
            os.mkdir(save_place_fpath)

    print("Generate Save Directory")
    return 0


def get_place_name(save_fpath, feature_modes):
    feature_mode_folders = operate_fpath.get_all_multi_folder(save_fpath)
    for feature_mode in feature_mode_folders:
        save_feature_mode_fpath = save_fpath + "/" + feature_mode
        if feature_mode == feature_modes[2]:
            place_names = operate_fpath.get_all_multi_folder(save_feature_mode_fpath)
    return place_names


def search_place_name(csv_list, place_name):
    for i in range(len(csv_list)):
        csv_fpath = csv_list[i]
        if place_name in csv_fpath:
            pass
        else:
            csv_list[i] = 0
    
    unique_name_or_zero = list(set(csv_list))
    print(unique_name_or_zero)

    for i in range(len(unique_name_or_zero)):
        name_or_zero = unique_name_or_zero[i]
        if name_or_zero == 0:
            unique_name_or_zero.pop(i)
            break
        else:
            pass
    deleted_csv_list = unique_name_or_zero
    return deleted_csv_list

def main():
    # JSONファイルを読み込む
    with open('./script/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)

    feature_modes = ["mfcc", "delta-ceps", "mfcc_and_delta-ceps"]
    read_fpath = config["input_output_csv_place"]
    save_fpath = config["output_plot_data"]
    generate_save_directory(save_fpath, read_fpath, feature_modes)
    place_names = get_place_name(save_fpath, feature_modes)
    
    for feature_mode in feature_modes:
        for place_name in place_names:
            #copy fpath
            save_place_name = save_fpath + "/" + feature_mode + "/" + place_name

            #search csv data
            read_score_folders = operate_fpath.get_all_multi_folder(read_fpath)
            for score_folder in read_score_folders:
                read_score_fpath = read_fpath + "/" + score_folder
                feature_mode_folders = operate_fpath.get_all_multi_folder(read_score_fpath)
                for feature_mode_folder in feature_mode_folders:
                    if feature_mode_folder == feature_mode:
                        feature_mode_fpath = read_score_fpath + "/" + feature_mode_folder
                        csv_list = glob.glob(feature_mode_fpath + "/*.csv")
                        csv_fpath_list = search_place_name(csv_list, place_name)
                        for csv_fpath in csv_fpath_list:
                            shutil.copy(csv_fpath, save_place_name)
                    else:
                        pass
    return 0

if __name__ == "__main__":
    main()