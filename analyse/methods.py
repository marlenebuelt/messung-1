import pandas as pd

def determineRuntimePhases(df):
    start_index = None
    value = 'runtime'
    for index, row in df.iterrows():
        if row['startstop'] == 'startTestrun':
            start_index = index
        elif row['startstop'] == 'stopTestrun' and start_index is not None:
            df.loc[start_index:index, 'startstop'] = value
            start_index = None
    return df

def elWork120(elPower):
    elWork = elPower * (120/3600)
    return elWork

def elWork600(elPower):
    elWork = elPower * (600/3600)
    return elWork

def networkTraffic(sum):
    mbyte = sum/1000000
    return mbyte

#method: credit to https://stackoverflow.com/questions/30926840/how-to-check-change-between-two-values-in-percent#:~:text=If%20you%20want%20the%20percentage,%2Fprevious)*100%20%2D%20100%20.
def get_change(model_value, baseline_value):
    if model_value == baseline_value:
        return 0
    try:
        return (abs(model_value - baseline_value) / baseline_value) * 100.0
    except ZeroDivisionError:
        return float('inf')