import pandas as pd
import methods

electrical_power_df = pd.read_csv('3_NN/elektrische_leistungsmessung_tesla.csv', sep=';')
electrical_power_df['Zeit'] = pd.to_datetime(electrical_power_df['Zeit']).dt.strftime('%H:%M:%S')

dj_tesla_df = pd.read_csv('3_NN/DJ-TESLA_DataCollector0120230301-000015.csv',low_memory=False)
dj_tesla_df['Zeit'] = pd.to_datetime(dj_tesla_df['Zeit']).dt.strftime('%H:%M:%S')

actions_df =  pd.read_csv('3_NN/Actions_SUT_Tesla.csv', sep=';', header = None)
actions_df.columns = ['Zeit', 'startstop']
actions_df['Zeit'] = pd.to_datetime(actions_df['Zeit']).dt.strftime('%H:%M:%S')

df_nn = pd.merge(dj_tesla_df, electrical_power_df, how='left', on='Zeit')
df_nn = pd.merge(df_nn, actions_df, how='left', on='Zeit')

df_nn = methods.determineRuntimePhases(df_nn)

df_nn = df_nn[df_nn['startstop'].notna()]

df_nn['CPU'] = pd.to_numeric(df_nn['CPU'])
df_nn['NetzwerkEmpfangen'] = pd.to_numeric(df_nn['NetzwerkEmpfangen'])
df_nn['FestplatteGeschrieben'] = pd.to_numeric(df_nn['FestplatteGeschrieben'])
df_nn['NetzwerkGesendet'] = pd.to_numeric(df_nn['NetzwerkGesendet'])
df_nn['FestplatteGelesen'] = pd.to_numeric(df_nn['FestplatteGelesen'])
df_nn = df_nn[['Zeit', 'RAM','Auslagerungsdatei','NetzwerkGesendet','NetzwerkEmpfangen','FestplatteGeschrieben','FestplatteGelesen','CPU','Wert 1-avg[W]','startstop']]
print(df_nn)
#descriptive nnriables
cpu_nn = df_nn['CPU']
ram_nn = df_nn['RAM']
el_power_nn = df_nn['Wert 1-avg[W]']
el_work_nn = methods.elWork120(el_power_nn)

df_desc = pd.DataFrame([[cpu_nn.min(), cpu_nn.max(), cpu_nn.mean(), cpu_nn.median(), cpu_nn.std()], 
                        [ram_nn.min(), ram_nn.max(), ram_nn.mean(), ram_nn.median(), ram_nn.std()], 
                        [el_power_nn.min(), el_power_nn.max(), el_power_nn.mean(), el_power_nn.median(), el_power_nn.std()]],
                       columns=['Minimum', 'Maximum', 'Mean', 'Median', 'Standard Deviation'], 
                       index=['CPU Utilization [%]','RAM [%]','Total Power [W]'])
print(df_desc)
df_desc.to_csv('3_NN/df_desc.csv')
df_nn.to_csv('3_NN/df_nn.csv')