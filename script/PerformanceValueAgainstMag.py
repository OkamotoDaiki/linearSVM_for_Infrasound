import pandas as pd
import os
import shutil
import glob
import sys
import OperateFpath

"""
write directory structure.
-output_PerformanceValue_VariableMag
├ accuracy
│　└ feature_mode
│　　　└ /*.csv written place_name and threshold 0
├ precision
├ recall
└ f1
"""

def ReadCSV(csv_fpath):
    """
    Read csv. Transform pd type to dictionary type. Output dictionary type.
    """
    data_dic = {}
    #from csv
    df = pd.read_csv(csv_fpath, index_col=0)
    header = df.columns.tolist()
    for row_name in header:
        data_dic[row_name] = df[row_name].tolist()
    return data_dic


def ReadPlaceName(data_dic):
    """
    Return place names for csv data.
    """
    read_data_type = "place_name"
    PlaceOrNotCount = 0
    for data_kind, data in data_dic.items():
        if data_kind == read_data_type:
            place_names = data
            PlaceOrNotCount += 1
            return place_names
    if PlaceOrNotCount == 0:
        print("Error : No place names rows. Check csv data.")
        sys.exit()
        return 0


def CompilePlaceData(target_place_name, data_dics):
    """
    Compile data and threshold magnitude against target place name. 
    """
    def GetTargetColumnNumber(target_place_name, data_dic):
        """
        find column number being target place name.
        """
        #init
        get_column_number = -1
        
        for row_name, data in data_dic.items():
            if row_name == "place_name":
                count_column = 0
                for place_name in data:
                    if place_name == target_place_name:
                        #decide getting column
                        get_column_number = count_column
                    else:
                        pass
                    count_column += 1
            else:
                pass
        return get_column_number
    
    
    #init
    all_data = []
    
    for threshold_mag, data_dic in data_dics.items():
        get_column_number = GetTargetColumnNumber(target_place_name, data_dic)
        if get_column_number != -1:
            column_data = []
            column_data.append(threshold_mag)
            for row_name, data in data_dic.items():
                if row_name == "number_of_dataset":
                    data_number_of_dataset = data[get_column_number]
                    column_data.append(data_number_of_dataset)
                elif row_name == "score_mean":
                    data_score_mean = data[get_column_number]
                    column_data.append(data_score_mean)
                elif row_name == "score_std_error":
                    data_score_std_error = data[get_column_number]
                    column_data.append(data_score_std_error)
                else:
                    pass
            all_data.append(column_data)
        else:
            pass
    return all_data


def SortCSVandMag(csv_list):
    """
    Sort csv list for threshold magnitude.
    """
    correspondence_dic = {}
    for csv_fpath in csv_list:
        threshold_mag_from_fname = csv_fpath.split("/")[-1].split(".")[0].split("_")[-3]
        numerator = int(threshold_mag_from_fname.split("mag")[0].split("div")[0])
        demominator = int(threshold_mag_from_fname.split("mag")[0].split("div")[1])
        threshold_mag = round(numerator / demominator, 2)
        correspondence_dic[csv_fpath] = threshold_mag

    sort_csv_fpath = {}
    #sort
    for k, v in sorted(correspondence_dic.items(), key=lambda x: x[1]):
        sort_csv_fpath[k] = v
    return sort_csv_fpath


def WriteCSV(data, fname, header):
    """
    Write CSV using header and data for pandas type.
    """
    df = pd.DataFrame(data, columns=header)
    df.to_csv(fname)
    print("Write '{}'.".format(fname))
    return 0


def main():
    header = ["threshold_magnitude", "number_of_dataset", "score_mean", "score_std_error"]
    #read csv and generate folder for saving new csv.
    save_place_csv_fpath = "./output_csv_place"

    try:
        shutil.rmtree(save_place_csv_fpath)
        os.mkdir(save_place_csv_fpath)
    except FileNotFoundError:
        os.mkdir(save_place_csv_fpath)

    read_score_csv_fpath = "./output_csv_against_mag"
    read_score_folders = OperateFpath.GetAllMultiFolder(read_score_csv_fpath)

    for read_score_folder in read_score_folders:
        print(read_score_folder)
        save_score_fpath = save_place_csv_fpath + "/" + read_score_folder
        os.mkdir(save_score_fpath)

        read_feature_mode_fpath = read_score_csv_fpath + "/" + read_score_folder
        read_feature_mode_folders = OperateFpath.GetAllMultiFolder(read_feature_mode_fpath)
        for read_feature_mode_folder in read_feature_mode_folders:
            print(read_feature_mode_folder)
            save_feature_mode_fpath = save_score_fpath + "/" + read_feature_mode_folder
            os.mkdir(save_feature_mode_fpath)

            read_csv_fpath = read_feature_mode_fpath + "/" + read_feature_mode_folder + "/*.csv"
            before_csv_list = glob.glob(read_csv_fpath)
            #edit
            csv_mag_dic = SortCSVandMag(before_csv_list)
            data_dics = {}
            for csv_fpath, threshold_mag in csv_mag_dic.items():
                data_dic = ReadCSV(csv_fpath)
                #search threshold 0 and generate place folder
                if threshold_mag == 0.0:
                    first_place_names = ReadPlaceName(data_dic)
                else:
                    pass            
                data_dics[threshold_mag] = data_dic
            #edit end

            for target_place_name in first_place_names:
                save_csv_fpath = save_feature_mode_fpath
                write_data = CompilePlaceData(target_place_name, data_dics)
                save_name_fpath = save_csv_fpath + "/" + target_place_name + "_" + read_score_folder + "_" + read_feature_mode_folder + ".csv"
                WriteCSV(write_data, save_name_fpath, header)
    return 0

if __name__=="__main__":
    main()