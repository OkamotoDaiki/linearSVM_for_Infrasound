import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import OperateFpath
import glob
import sys
import shutil
import os

Vaxis_min = 0
Vaxis_max = 1.05


def ExtractData(df):
    """
    Extract data from data frame of pandas for data against threshold magnitude.
    """
    threshold_mag = df["threshold_magnitude"].tolist()
    number_dataset = df["number_of_dataset"].tolist()
    score_mean = df["score_mean"].tolist()
    score_SE = df["score_std_error"].tolist()

    data = {
        "Haxis": {
            "threshold_magnitude" : threshold_mag
        },
        "Vaxis" : {
            #"number_dataset" : number_dataset,
            "score_mean" : score_mean
        }
    }
    return data


def ScoreName(csv_fpath):
    print(csv_fpath)
    csv_fname = csv_fpath.split("/")[-1]
    if csv_fname.split("_")[-2] == "and":
        score_name = csv_fname.split("_")[-4]
    else:
        score_name = csv_fname.split("_")[-2]
    return score_name


def OrganizePlotData(plot_data):
    ornot_count = 0
    input_plot_data = {}

    #Haxis data
    for score_name, data_in_score in plot_data.items():
        Vaxis_dct = {}
        for axis_name, data_dct in data_in_score.items():
            if axis_name == "Haxis" and ornot_count == 0:
                input_plot_data[axis_name] = data_dct
                break
            else:
                pass

    #Vaxis data
    score_datas = {}
    for score_name, data_in_score in plot_data.items():
        for axis_name, data_dct in data_in_score.items():
            if axis_name == "Vaxis":
                score_datas[score_name] = data_dct
            else:
                pass
    input_plot_data["Vaxis"] = score_datas
    return input_plot_data


def GenerateSavePNG(save_fpath, feature_mode_folders):
    try:
        shutil.rmtree(save_fpath)
        os.mkdir(save_fpath)
    except FileNotFoundError:
        os.mkdir(save_fpath)

    for feature_mode_folder in feature_mode_folders:
        feature_mode_fpath = save_fpath + "/" + feature_mode_folder
        os.mkdir(feature_mode_fpath)
    print("Generate Save Directory")
    return 0


def PlotGraph(fpath, input_plot_data):
    def DecideMarkerType(score_name):
        if score_name == "accuracy":
            marker = "o"
        elif score_name == "precision":
            marker = "s"
        elif score_name == "recall":
            marker = "^"
        elif score_name == "f1":
            marker = "x"
        else:
            print("Error : Not specifed marker type. Confirm data or Modify script.")
            sys.exit()
        return marker

    def DecideLineType(score_name):
        if score_name == "accuracy":
            linestyle = "-"
        elif score_name == "precision":
            linestyle = "-."
        elif score_name == "recall":
            linestyle = "--"
        elif score_name == "f1":
            linestyle = ":"
        else:
            print("Error : Not specifed linestle type. Confirm data or Modify script.")
            sys.exit()
        return linestyle

    plt.clf()

    #search Haxis
    for axis_name, data_and_name in input_plot_data.items():
        if axis_name == "Haxis":
            for data_name, data in data_and_name.items():
                Haxis_data = data
        else:
            pass
    
    #serach Vaxis
    for axis_name, score_and_data in input_plot_data.items():
        if axis_name == "Vaxis":
            for score_name, data_and_name in score_and_data.items():
                marker = DecideMarkerType(score_name)
                linestyle = DecideLineType(score_name)
                for data_name, data in data_and_name.items():
                    #print(data)
                    Vaxis_data = data
                    plt.ylim(Vaxis_min, Vaxis_max)
                    plt.plot(Haxis_data, Vaxis_data, label=score_name, marker=marker, linestyle=linestyle)
        else:
            pass
    plt.legend()
    #edit
    plt.xlabel("threshold magnitude", fontsize=12)
    plt.ylabel("performance evaluation value", fontsize=12)
    #edit end
    plt.tick_params(labelsize=12)
    plt.savefig(fpath)
    print("save : {}".format(fpath))
    return 0

def main():
    read_fpath = "./output_plot_data"
    save_fpath = "./png_files"

    feature_mode_folders = OperateFpath.GetAllMultiFolder(read_fpath)
    GenerateSavePNG(save_fpath, feature_mode_folders)

    for feature_mode_folder in feature_mode_folders:
        feature_mode_fpath = read_fpath + "/" + feature_mode_folder
        place_names = OperateFpath.GetAllMultiFolder(feature_mode_fpath)
        for place_name in place_names:
            place_name_fpath = feature_mode_fpath + "/" + place_name

            plot_data = {}
            csv_list = glob.glob(place_name_fpath + "/*.csv")
            for csv_fpath in csv_list:
                score_name = ScoreName(csv_fpath)
                df = pd.read_csv(csv_fpath)
                read_data = ExtractData(df)
                plot_data[score_name] = read_data
            input_plot_data = OrganizePlotData(plot_data)
            save_png_fpath = save_fpath + "/" + feature_mode_folder + "/" + place_name + "_" + feature_mode_folder + "_performance_value_agaist_mag.png"
            PlotGraph(save_png_fpath, input_plot_data)
    return 0


if __name__=="__main__":
    main()