1. (test_)linear_svm_fo_const.py
do SVM with fo const. output accuracy, precision, recall, f-1 value.

file structure
-input file

../pkl_file
„¥threshold_magnitude folder
„  „¤ place/
„ 	„¤ *.pkl
„ 
„¥threshold_magnitude folder
.
.
.
„¤threshold_magnitude folder

-output csv file
./output_Csv
„¥accuracy
„  „¥MFCC
„  „   „¥threshold_magnitude folder
„  „   „ „¤ *.csv
„  „   „¥threshold_magnitude folder
.  .   .
.  .   .
.  .   .
„  „   „¤threshold_magnitude folder
„  „¥delta-ceps
„  „¤mfcc_and_delta-ceps
„ 
„¥precision
„¥recall
„¤f1

2. copy_performance_value_against_mag.py
Collect performance evaluation values agains magnitude from "output_csv" folder.
output ./output_csv_against_mag


3. performance_value_against_mag.py -> OrganizeFile_forPlot.py -> plot_performance_value_against_mag.py
Write csv collected performance evaluation values agains magnitude and number of dataset being "output_csv_against_mag".