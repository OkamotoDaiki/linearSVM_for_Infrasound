# linearSVM_for_Infrasound
Run linearSVM with infrasound data. Output accuracy, precision, recall, f-1 value.
 
# Features

1. infrasound_linear_svm_fo_const.py

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
The output folder is
    output_csv_against_mag...Accuracy rate for each station divided by magnification
    output_csv_place...Accuracy rate for each magnification divided by observatory
    output_plot_data...Accuracy rate plot data with magnification as horizontal axis
    plot_evaluation...Accuracy rate graph with magnification as horizontal axis


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
