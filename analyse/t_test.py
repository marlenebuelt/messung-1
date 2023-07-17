import pandas as pd
import decisionTree as dt
import logreg as lr
import nn
import svm
import baseline_df_120 as bl120
import baseline_df_600 as bl600
import scipy.stats as stats

#bl120 + 60
cpu_bl120 = bl120.df_bl_120['CPU']
ram_bl120 = bl120.df_bl_120['RAM']
el_power_bl120 = bl120.df_bl_120['Wert 1-avg[W]']

#bl600 + 60
cpu_bl600 = bl600.df_bl_600['CPU']
ram_bl600 = bl600.df_bl_600['RAM']
el_power_bl600 = bl600.df_bl_600['Wert 1-avg[W]']

#dt
cpu_dt = dt.df_dt['CPU']
ram_dt = dt.df_dt['RAM']
el_power_dt = dt.df_dt['Wert 1-avg[W]']

#lr
cpu_lr = lr.df_lr['CPU']
ram_lr = lr.df_lr['RAM']
el_power_lr = lr.df_lr['Wert 1-avg[W]']

#svm
cpu_svm = svm.df_svm['CPU']
ram_svm = svm.df_svm['RAM']
el_power_svm = svm.df_svm['Wert 1-avg[W]']

#nn
cpu_nn = nn.df_nn['CPU']
ram_nn = nn.df_nn['RAM']
el_power_nn = nn.df_nn['Wert 1-avg[W]']


df_significance = pd.DataFrame([[stats.ttest_rel(cpu_bl120, cpu_dt).pvalue, 
                        stats.ttest_rel(cpu_bl120, cpu_lr).pvalue,
                        stats.ttest_rel(cpu_bl600, cpu_svm).pvalue,
                        stats.ttest_rel(cpu_bl120, cpu_nn).pvalue], 
                        [stats.ttest_rel(ram_bl120, ram_dt).pvalue,
                        stats.ttest_rel(ram_bl120, ram_lr).pvalue,
                        stats.ttest_rel(ram_bl600, ram_svm).pvalue,
                        stats.ttest_rel(ram_bl120, ram_nn).pvalue], 
                        [stats.ttest_rel(el_power_bl120.fillna(0), el_power_dt.fillna(0)).pvalue,
                        stats.ttest_rel(el_power_bl120.fillna(0), el_power_lr.fillna(0)).pvalue,
                        stats.ttest_rel(el_power_bl600.fillna(0), el_power_svm.fillna(0)).pvalue,
                        stats.ttest_rel(el_power_bl120.fillna(0), el_power_nn.fillna(0)).pvalue]],
                    columns=['DT', 'LogReg','SVM', 'MLP'],      
                    index=['CPU Utilization [%]','RAM [%]','Electric Power [W]'])

pd.set_option('float_format', lambda x: '%.3f' % x)

print(df_significance)
df_significance.to_csv('df_significance.csv', float_format='%.2f')
