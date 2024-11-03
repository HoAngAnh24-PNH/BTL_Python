import pandas as pd
from IPython.display import display
df = pd.read_csv('results.csv')
df.iloc[:, 5:] = df.iloc[:, 5:].replace(',', '', regex=True)
df.iloc[:, 4:] = df.iloc[:, 4:].apply(pd.to_numeric, errors='coerce')
pd.set_option('future.no_silent_downcasting', True)
df.fillna(0, inplace=True)
for x in df.columns[4:]:
    df[x] = df[x].astype(float)
for x in df.columns[4:]:
    df_copy =df.copy()
    tmp =df_copy[['Player',x]].sort_values(x)
    tmp.dropna(axis=0, inplace=True)
    print(f'Top 3 cầu thủ có chỉ số {x} cao nhất')
    display(tmp[-3:][::-1])
    print(f'Top 3 cầu thủ có chỉ số {x} thấp nhất')
    display(tmp[:3])

