import pickle
import numpy as np
import time
import pandas as pd
import sys
import os
import glob
import shutil
import OperateFpath

class SVMclass():
    def __init__(self, training_list, label_list, split_number):
        self.training_list = training_list
        self.label_list = label_list
        self.split_number = split_number


    def linearSVM(self, score_func):
        """
        calculate linear SVM.
        """
        #テストデータの作成 
        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(
            self.training_list, self.label_list, random_state=0
        )

        from sklearn.svm import LinearSVC
        Linear_svm = LinearSVC().fit(X_train, y_train)
        score_testset = Linear_svm.score(X_test, y_test)
        print("Accuracy on test set: {}".format(score_testset))

        pred_linsvm = Linear_svm.predict(X_test)

        #confusion_matrix
        from sklearn.metrics import confusion_matrix
        confusion = confusion_matrix(y_test, pred_linsvm)
        print("Confusion matrinx: \n {}".format(confusion))

        #report
        from sklearn.metrics import classification_report
        print(classification_report(y_test,pred_linsvm))

        #cross-varidation
        from sklearn.model_selection import StratifiedKFold
        kf = StratifiedKFold(n_splits=self.split_number)
        from sklearn.model_selection import cross_val_score
        from sklearn.svm import LinearSVC
        Linear_svm = LinearSVC()
        scores = cross_val_score(Linear_svm, self.training_list, self.label_list,scoring=score_func, cv=kf)
        print(len(scores))
        scores_mean = np.mean(scores)
        scores_std = np.std(scores)
        print("Cross-validation scores- mean = {}, std = {}".format(scores_mean, scores_std))        

        typeofClassifier = "linearSVM"   

        return score_testset, typeofClassifier, scores_mean, scores_std


    def svm(self, training_list,label_list,C_value,g_value):
        #テストデータの作成 
        from sklearn.model_selection import train_test_split

        X_train, X_test, y_train, y_test = train_test_split(
            np.array(training_list), np.array(label_list), random_state=0
        )
        
        #ただのテスト
        print(X_train.shape)
        print(y_train.shape)

        #前処理なし,SVM
        from sklearn.svm import SVC
        svc = SVC(C=C_value,gamma=g_value)
        svc.fit(X_train, y_train)
        score_trainingset = svc.score(X_train, y_train)
        score_testset = svc.score(X_test, y_test)
        print("Accuracy on training set: {:.3f}".format(score_trainingset))
        print("Accuracy on test set: {:.3f}".format(score_testset))

        #MinMaxscaler
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        scaler.fit(X_train)
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        #svc = SVC(C=C_value,gamma=g_value)
        svc.fit(X_train_scaled, y_train)
        score_trainingset_MinMax = svc.score(X_train, y_train)
        score_testset_MinMax = svc.score(X_test, y_test)

        print("MinMax Scaled Accuracy on training set: {:.3f}".format(score_trainingset_MinMax))
        print("MinMax Scaled Accuracy on test set: {:.3f}".format(score_testset_MinMax))

        #StandardScaler
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        scaler.fit(X_train)
        X_train_scaled = scaler.transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        #scalecheck(X_train_scaled)
        #scalecheck(X_test_scaled)

        svc.fit(X_train_scaled, y_train)
        score_trainingset_standard = svc.score(X_train, y_train)
        score_testset_standard = svc.score(X_test, y_test)

        print("standard Scaled Accuracy on training set: {:.3f}".format(score_trainingset_standard))
        print("standard Scaled Accuracy on test set: {:.3f}".format(score_testset_standard))

        return [C_value, g_value, score_trainingset, score_testset, score_trainingset_MinMax, score_testset_MinMax, score_trainingset_standard, score_testset_standard]


class Preprocessing():
    def __init__(self,fname):
        self.fname = fname

    def GetData_fromPickle(self):
        """
        Get training data and label data from Pickle.
        """
        with open(self.fname, "rb") as f:
            data = pickle.load(f)
            count = 0
            for data_div in data:
                if count == 0:
                    label = data_div
                elif count == 1:
                    training_data = data_div
                count += 1
        return label, training_data
    
    def GenerateMultiClassNumber(self):
        """
        Generate list for number of class.
        """
        def SepSVM(training_list,label_list,number_list):
            """
            Spectify number. Append traning data and label data to list.
            """
            training_list, label_list = self.GetMLData_fromPickle()
            new_training_list = []
            new_label_list = []
            count = 0
            for number in number_list:
                for i in label_list:
                    if number == i:
                        new_training_list.append(training_list[count])
                        new_label_list.append(label_list[count])
                        count += 1
            return new_training_list, new_label_list


        number = max(label_list)
        number_list = []

        for i in range(number+1):
            #時間の計測
            number_list.append(i)
            if len(number_list) != 1:
                print("Run {} classification.".format(number_list))
                new_training_list, new_label_list = SepSVM(training_list,label_list,number_list)
        return new_training_list, new_label_list


def WriteCSV(data, fname, header):
    import pandas as pd
    df = pd.DataFrame(data, columns=header)
    df.to_csv(fname)
    print("Write '{}'.".format(fname))
    return 0


def FindNaN_mfcc(data):
    count1 = 0
    for i in data:
        count1 += 1
        count2 = 0
        for j in i:
            if str(j) == 'NaN':
                print('Find NaN. number of ({},{})'.format(count1,count2))
                break
    return 0

def test_main():
    #時間を計測
    start = time.time()
    #fnames = "../mfcc_script/mfcc_number_random_*.pkl"
    split_number = 5
    output_csv_fpath = "./output_csv"
    feature_mode_fpath = "../pkl_file"
    feature_mode_list = OperateFpath.GetAllMultiFolder(feature_mode_fpath)

    score_funcs = [
        'accuracy',
        'precision',
        'recall',
        'f1'
    ]
    #Generate Direcotry
    try:
        shutil.rmtree(output_csv_fpath)
        os.mkdir(output_csv_fpath)
    except FileNotFoundError:
        os.mkdir(output_csv_fpath)

    for score_func in score_funcs:
        generate_scorefunc_fpath = output_csv_fpath + "/" + score_func
        os.mkdir(generate_scorefunc_fpath)
        for feature_mode in feature_mode_list:
            threshold_fpath = feature_mode_fpath + "/" + feature_mode
            threshold_variable_list = OperateFpath.GetAllMultiFolder(threshold_fpath)
            generate_feature_mode_fpath = generate_scorefunc_fpath + "/" + feature_mode
            os.mkdir(generate_feature_mode_fpath)
            for threshold_variable in threshold_variable_list:
                place_fpath = threshold_fpath + "/" + threshold_variable
                place_names = OperateFpath.GetAllMultiFolder(place_fpath)
                generate_threshold_fpath = generate_feature_mode_fpath + "/" + threshold_variable
                os.mkdir(generate_threshold_fpath)
                #Generate csv
                all_data = []
                for place_name in place_names:
                    pkl_fpath = place_fpath + "/" + place_name
                    print("place name : {}".format(place_name))
                    all_pkl_files = glob.glob(pkl_fpath+ "/*.pkl")

                    label_list = []
                    training_data_list = []
                    for fname in all_pkl_files:
                        #SVMの処理
                        Preprocessing_obj = Preprocessing(fname)
                        label, traning_data = Preprocessing_obj.GetData_fromPickle()
                        label_list.append(label)
                        training_data_list.append(traning_data)
                    newtime = time.time() #線形SVMの時間計測の開始
                    #線形SVM
                    try:
                        number_of_dataset = len(all_pkl_files)
                        SVM_obj = SVMclass(training_data_list, label_list, split_number)
                        score_linearsvm, typeofClassifier, score_crossvaridation_mean, score_crossvaridation_std = SVM_obj.linearSVM(score_func)
                        elapsed_time = time.time() - newtime #時間計測終了
                        print("linear SVMN elapsed_time:{}[sec],{}[min],{}[hour]".format(round(elapsed_time,2),round(elapsed_time/60,2), round(elapsed_time/(60*60),2)))
                        score_stderr = score_crossvaridation_std / np.sqrt(split_number)
                        #csvへの書き込み
                        data = [place_name, typeofClassifier, number_of_dataset, score_crossvaridation_mean, score_stderr, round(elapsed_time,2)]
                        all_data.append(data)
                    except ValueError:
                        print(len(label_list))
                        print(len(traning_data))
                        print("Error: modify script.")

                fname_csv = generate_threshold_fpath + "/" + score_func + "_" + feature_mode + "_" + threshold_variable + "_" + "fo_const.csv"
                header = ["place_name", "classifier", "number_of_dataset", "score_mean", "score_std_error","elapsed_time[s]"]
                WriteCSV(all_data, fname_csv, header)
    elapsed_time = time.time() - start
    print("all elapsed_time:{}[sec],{}[min],{}[hour]\n".format(round(elapsed_time,2),round(elapsed_time/60,2), round(elapsed_time/(60*60),2)))
    return 0

if __name__ == '__main__':
    test_main()