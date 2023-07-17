import pandas as pd
import methods

electrical_power_df = pd.read_csv('Baseline_Tesla_600+60/elektrische_leistungsmessung_tesla_CUTTED.csv', sep=';')
electrical_power_df['Zeit'] = pd.to_datetime(electrical_power_df['Zeit']).dt.strftime('%H:%M:%S')

dj_tesla_df = pd.read_csv('Baseline_Tesla_600+60/DJ-TESLA_DataCollector0120230314-000014_CUTTED.csv', low_memory=False)
dj_tesla_df['Zeit'] = pd.to_datetime(dj_tesla_df['Zeit']).dt.strftime('%H:%M:%S')

actions_df =  pd.read_csv('Baseline_Tesla_600+60/Actions_SUT_Tesla_cutted.csv', sep=';', header = None)
actions_df.columns = ['Zeit', 'startstop']
actions_df['Zeit'] = pd.to_datetime(actions_df['Zeit']).dt.strftime('%H:%M:%S')

df_bl_600 = pd.merge(dj_tesla_df, electrical_power_df, how='left', on='Zeit')
df_bl_600 = pd.merge(df_bl_600, actions_df, how='left', on='Zeit')

df_bl_600 = methods.determineRuntimePhases(df_bl_600)

df_bl_600 = df_bl_600[df_bl_600['startstop'].notna()]

df_bl_600['CPU'] = pd.to_numeric(df_bl_600['CPU'])
df_bl_600['NetzwerkEmpfangen'] = pd.to_numeric(df_bl_600['NetzwerkEmpfangen'])
df_bl_600['FestplatteGeschrieben'] = pd.to_numeric(df_bl_600['FestplatteGeschrieben'])
df_bl_600['NetzwerkGesendet'] = pd.to_numeric(df_bl_600['NetzwerkGesendet'])
df_bl_600['FestplatteGelesen'] = pd.to_numeric(df_bl_600['FestplatteGelesen'])
print(df_bl_600)
#descriptive variables
cpu_bl600 = df_bl_600['CPU']
ram_bl600 = df_bl_600['RAM']
el_power_bl600 = df_bl_600['Wert 1-avg[W]']
el_work_bl600 = methods.elWork120(el_power_bl600)

df_desc = pd.DataFrame([[cpu_bl600.min(), cpu_bl600.max(), cpu_bl600.mean(), cpu_bl600.median(), cpu_bl600.std()], 
                        [ram_bl600.min(), ram_bl600.max(), ram_bl600.mean(), ram_bl600.median(), ram_bl600.std()], 
                        [el_power_bl600.min(), el_power_bl600.max(), el_power_bl600.mean(), el_power_bl600.median(), el_power_bl600.std()]],
                       columns=['Minimum', 'Maximum', 'Mean', 'Median', 'Standard Deviation'], 
                       index=['CPU Utilization [%]','RAM [%]','Total Power [W]'])
print(df_desc)
df_desc.to_csv('Baseline_Tesla_600+60/df_desc.csv')
df_bl_600.to_csv('Baseline_Tesla_600+60/df_bl_600.csv')