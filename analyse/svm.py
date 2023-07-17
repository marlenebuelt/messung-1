import pandas as pd
import methods

electrical_power_df = pd.read_csv('4_SVM/elektrische_leistungsmessung_tesla.csv', sep=';')
electrical_power_df['Zeit'] = pd.to_datetime(electrical_power_df['Zeit']).dt.strftime('%H:%M:%S')

dj_tesla_df = pd.read_csv('4_SVM/DJ-TESLA_DataCollector0120230301-000016.csv',low_memory=False)
dj_tesla_df['Zeit'] = pd.to_datetime(dj_tesla_df['Zeit']).dt.strftime('%H:%M:%S')

actions_df =  pd.read_csv('4_SVM/Actions_SUT_Tesla.csv', sep=';', header = None)
actions_df.columns = ['Zeit', 'startstop']
actions_df['Zeit'] = pd.to_datetime(actions_df['Zeit']).dt.strftime('%H:%M:%S')

df_svm = pd.merge(dj_tesla_df, electrical_power_df, how='left', on='Zeit')
df_svm = pd.merge(df_svm, actions_df, how='left', on='Zeit')

df_svm = methods.determineRuntimePhases(df_svm)

df_svm = df_svm[df_svm['startstop'].notna()]

df_svm['CPU'] = pd.to_numeric(df_svm['CPU'])
df_svm['NetzwerkEmpfangen'] = pd.to_numeric(df_svm['NetzwerkEmpfangen'])
df_svm['FestplatteGeschrieben'] = pd.to_numeric(df_svm['FestplatteGeschrieben'])
df_svm['NetzwerkGesendet'] = pd.to_numeric(df_svm['NetzwerkGesendet'])
df_svm['FestplatteGelesen'] = pd.to_numeric(df_svm['FestplatteGelesen'])

df_svm = df_svm[['Zeit', 'RAM','Auslagerungsdatei','NetzwerkGesendet','NetzwerkEmpfangen','FestplatteGeschrieben','FestplatteGelesen','CPU','Wert 1-avg[W]','startstop']]
print(df_svm)
#descriptive variables
cpu_svm = df_svm['CPU']
ram_svm = df_svm['RAM']
el_power_svm = df_svm['Wert 1-avg[W]']
el_work_svm = methods.elWork120(el_power_svm)

df_desc = pd.DataFrame([[cpu_svm.min(), cpu_svm.max(), cpu_svm.mean(), cpu_svm.median(), cpu_svm.std()], 
                        [ram_svm.min(), ram_svm.max(), ram_svm.mean(), ram_svm.median(), ram_svm.std()], 
                        [el_power_svm.min(), el_power_svm.max(), el_power_svm.mean(), el_power_svm.median(), el_power_svm.std()]],
                       columns=['Minimum', 'Maximum', 'Mean', 'Median', 'Standard Deviation'], 
                       index=['CPU Utilization [%]','RAM [%]','Total Power [W]'])
print(df_desc)
df_desc.to_csv('4_SVM/df_desc.csv')
df_svm.to_csv('4_SVM/df_svm.csv')
