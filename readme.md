# Hardware-based measurement

This is the data I collected and the analysis files used for a part of my bachelor's thesis using the method described by [Junger et al.](https://dl.gi.de/items/7f5ee625-729a-463c-9114-9cbeeb6e5736)

Measurement files in the folder are structured as follows:
Actions_SUT_Tesla.csv - logs start and stop of measurement cycles
DJ-TESLA_DataCollector[xxx].csv - Several data on collected parameters, e.g. RAM, CPU, network traffic
elektrische_leistungsmessung_Tesla.log - elctrical power used

## /1
Data for decision tree measurements 

## /2 
Data for logistic regression measurements 

## /3_NN
Data for multilayer perceptron measurements 

## /4_SVM
Data for support vector machine measurements 

## /Baseline_Tesla_WinAutomate_120s+60s_cooldown_new
Data for support vector machine measurements 

## /Baseline_Tesla_600+60
Data for support vector machine measurements 

## /analyse
[model/baseline].py - merges different files, structures and cleans data
mean_to_bl.py - compares mean values of the measurement per model to baseline values
methods.py - service class for the methods used across all analysis files
ttest.ipynb - significance tests and effect size tests (ttest and cohen's d)
shapiro-wilk.ipynb - tests for normality