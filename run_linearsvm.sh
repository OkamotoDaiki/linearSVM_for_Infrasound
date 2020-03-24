#!/bin/sh

cd ./script
python linearSVM.py
python Copy_PerformanceValueAgainstMag.py
python PerformanceValueAgaistMag.py
python OrganizeFile_forPlot.py
python plot_performance_value_against_mag.py