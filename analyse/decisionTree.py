import pandas as pd
import methods

electrical_power_df = pd.read_csv('1/elektrische_leistungsmessung_Tesla.csv', sep=';')
electrical_power_df['Zeit'] = pd.to_datetime(electrical_power_df['Zeit']).dt.strftime('%H:%M:%S')

dj_tesla_df = pd.read_csv('1/DJ-TESLA_DataCollector0120230228-000012.csv',low_memory=False)
dj_tesla_df['Zeit'] = pd.to_datetime(dj_tesla_df['Zeit']).dt.strftime('%H:%M:%S')

actions_df =  pd.read_csv('1/Actions_SUT_Tesla.csv', sep=';', header = None)
actions_df.columns = ['Zeit', 'startstop']
actions_df['Zeit'] = pd.to_datetime(actions_df['Zeit']).dt.strftime('%H:%M:%S')

df_dt = pd.merge(dj_tesla_df, electrical_power_df, how='left', on='Zeit')
df_dt = pd.merge(df_dt, actions_df, how='left', on='Zeit')

df_dt = methods.determineRuntimePhases(df_dt)

df_dt = df_dt[df_dt['startstop'].notna()]

df_dt['CPU'] = pd.to_numeric(df_dt['CPU'])
df_dt['NetzwerkEmpfangen'] = pd.to_numeric(df_dt['NetzwerkEmpfangen'])
df_dt['FestplatteGeschrieben'] = pd.to_numeric(df_dt['FestplatteGeschrieben'])
df_dt['NetzwerkGesendet'] = pd.to_numeric(df_dt['NetzwerkGesendet'])
df_dt['FestplatteGelesen'] = pd.to_numeric(df_dt['FestplatteGelesen'])

df_dt = df_dt[['Zeit', 'RAM','Auslagerungsdatei','NetzwerkGesendet','NetzwerkEmpfangen','FestplatteGeschrieben','FestplatteGelesen','CPU','Wert 1-avg[W]','startstop']]
print(df_dt)
#descriptive variables
cpu_dt = df_dt['CPU']
print(cpu_dt)
ram_dt = df_dt['RAM']
el_power_dt = df_dt['Wert 1-avg[W]']
el_work_dt = methods.elWork120(el_power_dt)

df_desc = pd.DataFrame([[cpu_dt.min(), cpu_dt.max(), cpu_dt.mean(), cpu_dt.median(), cpu_dt.std()], 
                        [ram_dt.min(), ram_dt.max(), ram_dt.mean(), ram_dt.median(), ram_dt.std()], 
                        [el_power_dt.min(), el_power_dt.max(), el_power_dt.mean(), el_power_dt.median(), el_power_dt.std()]],
                       columns=['Minimum', 'Maximum', 'Mean', 'Median', 'Standard Deviation'], 
                       index=['CPU Utilization [%]','RAM [%]','Total Power [W]'])
print(df_desc)
df_desc.to_csv('1/df_desc.csv')
df_dt.to_csv('1/df_dt.csv')