# linearSVM_for_Infrasound
Run linearSVM with infrasound data. Output accuracy, precision, recall, f-1 value.
 
# Features

1. linear_svm_fo_const.py

file structure
-input file

../pkl_file
├threshold_magnitude folder
│ └ place/
│	└ *.pkl
│
├threshold_magnitude folder
.
.
.
└threshold_magnitude folder

-output csv file
./result/output_csv
├accuracy
│ ├MFCC
│ │  ├threshold_magnitude folder
│ │  │└ *.csv
│ │  ├threshold_magnitude folder
.  .   .
.  .   .
.  .   .
│ │  └threshold_magnitude folder
│ ├delta-ceps
│ └mfcc_and_delta-ceps
│
├precision
├recall
└f1

2. copy_performance_value_against_mag.py
Collect performance evaluation values agains magnitude from "output_csv" folder.
output ./result/output_csv_against_mag


3. PerformanceValueAgainstMag.py -> organize_file_for_plot.py -> plot_performance_value_against_mag.py
Write csv collected performance evaluation values agains magnitude and number of dataset being "output_csv_against_mag".
output ./result/output_csv_place and ./result/output_plot_data and ./result/png_files
 
# Requirement
 
* Python 3.8.10
 
# Installation

Clone this repository and place the dataset in the ./input/pkl_file directory.
 
# Usage
 
Run this command.

```bash
bash run.sh
```
 
# Author
* Oka.D.
* okamotoschool2018@gmail.com
