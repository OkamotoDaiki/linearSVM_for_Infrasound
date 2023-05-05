#!/bin/sh

python3 ./script/infrasound_linear_svm_fo_const.py
python3 ./script/copy_performance_value_against_mag.py
python3 ./script/performance_value_against_mag.py
python3 ./script/organize_file_for_plot.py
python3 ./script/plot_performance_value_against_mag.py