import pandas as pd
import methods

electrical_power_df = pd.read_csv('Baseline_Tesla_WinAutomate_120s+60s_cooldown_new/elektrische_leistungsmessung_tesla.csv', sep=';')
electrical_power_df['Zeit'] = pd.to_datetime(electrical_power_df['Zeit']).dt.strftime('%H:%M:%S')

dj_tesla_df = pd.read_csv('Baseline_Tesla_WinAutomate_120s+60s_cooldown_new/DJ-TESLA_DataCollector0120230109-000011.csv',low_memory=False)
dj_tesla_df['Zeit'] = pd.to_datetime(dj_tesla_df['Zeit']).dt.strftime('%H:%M:%S')

actions_df =  pd.read_csv('Baseline_Tesla_WinAutomate_120s+60s_cooldown_new/Actions_SUT_Tesla.csv', sep=';', header = None)
actions_df.columns = ['Zeit', 'startstop']
actions_df['Zeit'] = pd.to_datetime(actions_df['Zeit']).dt.strftime('%H:%M:%S')

df_bl_120 = pd.merge(dj_tesla_df, electrical_power_df, how='left', on='Zeit')
df_bl_120 = pd.merge(df_bl_120, actions_df, how='left', on='Zeit')

df_bl_120 = methods.determineRuntimePhases(df_bl_120)
df_bl_120 = df_bl_120[df_bl_120['startstop'].notna()]

df_bl_120['CPU'] = pd.to_numeric(df_bl_120['CPU'])
df_bl_120['NetzwerkEmpfangen'] = pd.to_numeric(df_bl_120['NetzwerkEmpfangen'])
df_bl_120['FestplatteGeschrieben'] = pd.to_numeric(df_bl_120['FestplatteGeschrieben'])
df_bl_120['NetzwerkGesendet'] = pd.to_numeric(df_bl_120['NetzwerkGesendet'])
df_bl_120['FestplatteGelesen'] = pd.to_numeric(df_bl_120['FestplatteGelesen'])

#descriptive variables
cpu_bl120 = df_bl_120['CPU']
print(cpu_bl120)
ram_bl120 = df_bl_120['RAM']
el_power_bl120 = df_bl_120['Wert 1-avg[W]']
el_work_bl120 = methods.elWork120(el_power_bl120)

df_desc = pd.DataFrame([[cpu_bl120.min(), cpu_bl120.max(), cpu_bl120.mean(), cpu_bl120.median(), cpu_bl120.std()], 
                        [ram_bl120.min(), ram_bl120.max(), ram_bl120.mean(), ram_bl120.median(), ram_bl120.std()], 
                        [el_power_bl120.min(), el_power_bl120.max(), el_power_bl120.mean(), el_power_bl120.median(), el_power_bl120.std()]],
                       columns=['Minimum', 'Maximum', 'Mean', 'Median', 'Standard Deviation'], 
                       index=['CPU Utilization [%]','RAM [%]','Total Power [W]'])
print(df_desc)
df_desc.to_csv('Baseline_Tesla_WinAutomate_120s+60s_cooldown_new/df_desc.csv')
df_bl_120.to_csv('Baseline_Tesla_WinAutomate_120s+60s_cooldown_new/df_bl_120.csv')