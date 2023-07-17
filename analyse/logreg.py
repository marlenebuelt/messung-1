import pandas as pd
import methods


electrical_power_df = pd.read_csv('2/elektrische_leistungsmessung_tesla.csv', sep=';')
electrical_power_df['Zeit'] = pd.to_datetime(electrical_power_df['Zeit']).dt.strftime('%H:%M:%S')

dj_tesla_df = pd.read_csv('2/DJ-TESLA_DataCollector0120230228-000014 copy.csv',low_memory=False)
dj_tesla_df['Zeit'] = pd.to_datetime(dj_tesla_df['Zeit']).dt.strftime('%H:%M:%S')

actions_df =  pd.read_csv('2/Actions_SUT_Tesla.csv', sep=';', header = None)
actions_df.columns = ['Zeit', 'startstop']
actions_df['Zeit'] = pd.to_datetime(actions_df['Zeit']).dt.strftime('%H:%M:%S')

df_bl_600 = pd.merge(dj_tesla_df, electrical_power_df, how='left', on='Zeit')
df_bl_600 = pd.merge(df_bl_600, actions_df, how='left', on='Zeit')

df_bl_600 = methods.determineRuntimePhases(df_bl_600)

df_bl_600 = df_bl_600[df_bl_600['startstop'].notna()]

actions_df =  pd.read_csv('2/Actions_SUT_Tesla.csv', sep=';', header = None)
actions_df.columns = ['Zeit', 'startstop']
actions_df['Zeit'] = pd.to_datetime(actions_df['Zeit']).dt.strftime('%H:%M:%S')

df_lr = pd.merge(dj_tesla_df, electrical_power_df, how='left', on='Zeit')
df_lr = pd.merge(df_lr, actions_df, how='left', on='Zeit')

df_lr = methods.determineRuntimePhases(df_lr)

df_lr = df_lr[df_lr['startstop'].notna()]

df_lr['CPU'] = pd.to_numeric(df_lr['CPU'])
df_lr['NetzwerkEmpfangen'] = pd.to_numeric(df_lr['NetzwerkEmpfangen'])
df_lr['FestplatteGeschrieben'] = pd.to_numeric(df_lr['FestplatteGeschrieben'])
df_lr['NetzwerkGesendet'] = pd.to_numeric(df_lr['NetzwerkGesendet'])
df_lr['FestplatteGelesen'] = pd.to_numeric(df_lr['FestplatteGelesen'])

df_lr = df_lr[['Zeit', 'RAM','Auslagerungsdatei','NetzwerkGesendet','NetzwerkEmpfangen','FestplatteGeschrieben','FestplatteGelesen','CPU','Wert 1-avg[W]','startstop']]
print(df_lr)
df_lr.to_csv('df_lr.csv')
#descriptive variables
cpu_lr = df_lr['CPU']
ram_lr = df_lr['RAM']
el_power_lr = df_lr['Wert 1-avg[W]']
el_work_lr = methods.elWork120(el_power_lr)

df_desc = pd.DataFrame([[cpu_lr.min(), cpu_lr.max(), cpu_lr.mean(), cpu_lr.median(), cpu_lr.std()], 
                        [ram_lr.min(), ram_lr.max(), ram_lr.mean(), ram_lr.median(), ram_lr.std()], 
                        [el_power_lr.min(), el_power_lr.max(), el_power_lr.mean(), el_power_lr.median(), el_power_lr.std()],],
                       columns=['Minimum', 'Maximum', 'Mean', 'Median', 'Standard Deviation'], 
                       index=['CPU Utilization [%]','RAM [%]','Total Power [W]'])
print(df_desc)
df_desc.to_csv('2/df_desc.csv')
df_lr.to_csv('2/df_lr.csv')