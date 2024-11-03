import pandas as pd
df = pd.read_csv('results.csv')
df.iloc[:, 5:] = df.iloc[:, 5:].replace(',', '', regex=True)
df.iloc[:, 4:] = df.iloc[:, 4:].apply(pd.to_numeric, errors='coerce')
pd.set_option('future.no_silent_downcasting', True)
index2 = ['Team']
df.fillna(0, inplace=True)
for x in df.columns[4:]:
    index2.append(x)
    df[x] = df[x].astype(float)

df= df[index2] # gán lại lấy những cột cần để xử lý thôi
df=df.set_index('Team') # đặt Team là chỉ số cho index

mean = df.groupby('Team').mean() # tính toán trung bình
median =df.groupby('Team').median() # trung vị
std = df.groupby('Team').std() # độ lệch chuẩn

mean_all= df.mean()
median_all= df.median()
std_all =df.std()

result2 = dict()
col_result2 = []
result2['all']=[]
for x in mean.index:
    result2[x]=[] 
for x in df.columns[5:]:
    col_result2.append(f'Median of {x}') # thêm tên vào danh sách cột
    col_result2.append(f'Mean of {x}')
    col_result2.append(f'Std of {x}')
    result2['all'].append(median_all[x]) # têm các giá trị chuẩn bị sẵn ở trên vào hàng
    result2['all'].append(mean_all[x])
    result2['all'].append(std_all[x])
    for y in mean.index:
        result2[y].append(median.loc[y][x]) # tương tự như trên vưới các đội
        result2[y].append(mean.loc[y][x])
        result2[y].append(std.loc[y][x])

result2=pd.DataFrame.from_dict(result2,orient='index',columns=col_result2)
result2.to_csv('results2.csv')