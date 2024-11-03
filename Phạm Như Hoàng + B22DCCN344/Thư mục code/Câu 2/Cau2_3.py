import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv('results.csv')
df.iloc[:, 5:] = df.iloc[:, 5:].replace(',', '', regex=True)
df.iloc[:, 4:] = df.iloc[:, 4:].apply(pd.to_numeric, errors='coerce')
pd.set_option('future.no_silent_downcasting', True)
df.fillna(0, inplace=True)
for x in df.columns[4:]:
    df[x] = df[x].astype(float)
print("Phân bố của mỗi chỉ số của các cầu thủ trong toàn giải")
print("")
plt.ion()
for i, x in enumerate(df.columns[4:]):
    print(f"Phân bố của {x}")
    tmp = df[x].dropna()
    plt.hist(tmp)
    plt.xlabel(x)
    plt.ylabel("Frequency")
    plt.draw()
    plt.pause(0.5)  # Tạm dừng có thể tăng lên nếu muốn
    plt.clf()  # Xóa biểu đồ hiện tại trước khi vẽ biểu đồ mới
plt.ioff()
