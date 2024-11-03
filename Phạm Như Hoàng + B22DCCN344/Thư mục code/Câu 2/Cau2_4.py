import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('results.csv')
df.iloc[:, 5:] = df.iloc[:, 5:].replace(',', '', regex=True)
df.iloc[:, 4:] = df.iloc[:, 4:].apply(pd.to_numeric, errors='coerce')
pd.set_option('future.no_silent_downcasting', True)
df.fillna(0, inplace=True)
for x in df.columns[4:]:
    df[x] = df[x].astype(float)
columns_to_sum = df.columns[4:].tolist()
team_stats = df.groupby('Team')[columns_to_sum].sum()
highest_team_stats = team_stats.idxmax()
for stat in team_stats.columns:
    print(f"'{stat}': {highest_team_stats[stat]}")