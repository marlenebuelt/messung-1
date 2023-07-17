import pandas as pd
import statistics
import decisionTree as dt
import logreg as lr
import nn
import svm
import baseline_df_120 as bl120
import methods
import baseline_df_600 as bl600

#bl120 + 60
cpu_bl120 = bl120.df_bl_120['CPU'].mean()
ram_bl120 = bl120.df_bl_120['RAM'].mean()
el_power_bl120 = bl120.df_bl_120['Wert 1-avg[W]'].mean()
el_work_bl120 = methods.elWork120(el_power_bl120)

#bl600 + 60
cpu_bl600 = bl600.df_bl_600['CPU'].mean()
ram_bl600 = bl600.df_bl_600['RAM'].mean()
el_power_bl600 = bl600.df_bl_600['Wert 1-avg[W]'].mean()
el_work_bl600 = methods.elWork600(el_power_bl600)

#dt
cpu_dt = dt.df_dt['CPU'].mean()
ram_dt = dt.df_dt['RAM'].mean()
el_power_dt = dt.df_dt['Wert 1-avg[W]'].mean()
el_work_dt = methods.elWork120(el_power_dt)
sum_nwt_dt= dt.df_dt['NetzwerkGesendet']+dt.df_dt['NetzwerkEmpfangen']

#lr
cpu_lr = lr.df_lr['CPU'].mean()
ram_lr = lr.df_lr['RAM'].mean()
el_power_lr = lr.df_lr['Wert 1-avg[W]'].mean()
el_work_lr = methods.elWork120(el_power_lr)

#svm
cpu_svm = svm.df_svm['CPU'].mean()
ram_svm = svm.df_svm['RAM'].mean()
el_power_svm = svm.df_svm['Wert 1-avg[W]'].mean()
el_work_svm = methods.elWork600(el_power_svm)

#nn
cpu_nn = nn.df_nn['CPU'].mean()
ram_nn = nn.df_nn['RAM'].mean()
el_power_nn = nn.df_nn['Wert 1-avg[W]'].mean()
el_work_nn = methods.elWork120(el_power_nn)

df_mean_abs = pd.DataFrame([[cpu_bl120, cpu_bl600, cpu_dt, cpu_lr, cpu_svm, cpu_nn], 
                        [ram_bl120, ram_bl600, ram_dt, ram_lr, ram_svm,ram_nn], 
                        [el_power_bl120, el_power_bl600,el_power_dt,el_power_lr,el_power_svm,el_power_nn],
                        [el_work_bl120, el_work_bl600, el_work_dt, el_work_lr, el_work_svm, el_work_nn]],
                    columns=['BL120', 'BL600', 'DT', 'Log. Reg.','SVM', 'MLP'], 
                    index=['CPU Utilization [%]','RAM Utilization[%]','Electric Power [W]', 'Electric Work'])
#pd.set_option('float_format', lambda x: '%.2f' % x)

df_mean_rel = pd.DataFrame([[methods.get_change(cpu_dt, cpu_bl120),
                        methods.get_change(cpu_lr, cpu_bl120),
                        methods.get_change(cpu_svm, cpu_bl600),
                        methods.get_change(cpu_nn, cpu_bl120)], 
                        [methods.get_change(ram_dt, ram_bl120),
                        methods.get_change(ram_lr, ram_bl120),
                        methods.get_change(ram_svm, ram_bl600),
                        methods.get_change(ram_nn, ram_bl120)], 
                        [methods.get_change(el_power_dt, el_power_bl120),
                        methods.get_change(el_power_lr, el_power_bl120),
                        methods.get_change(el_power_svm, el_power_bl600),
                        methods.get_change(el_power_nn, el_power_bl120)],
                        [methods.get_change(el_work_dt, el_work_bl120),
                        methods.get_change(el_work_lr, el_work_bl120),
                        methods.get_change(el_work_svm, el_work_bl600),
                        methods.get_change(el_work_nn, el_work_bl120)]],
                    columns=['Delta DT %','Delta LogReg %','Delta SVM %','Delta MLP % '], 
                    index=['CPU Utilization [%]','RAM Utilization[%]','Electric Power [W]', 'Electric Work'])
df_mean_abs.to_csv('df_mean_abs.csv', float_format='%.2f')
df_mean_rel.to_csv('df_mean_rel.csv', float_format='%.2f')