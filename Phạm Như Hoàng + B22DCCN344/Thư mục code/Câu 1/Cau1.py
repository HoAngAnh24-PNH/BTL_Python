from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import requests
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
urls = [
    "https://fbref.com/en/squads/b8fd03ef/2023-2024/Manchester-City-Stats",
    "https://fbref.com/en/squads/18bb7c10/2023-2024/Arsenal-Stats",
    "https://fbref.com/en/squads/822bd0ba/2023-2024/Liverpool-Stats",
    "https://fbref.com/en/squads/8602292d/2023-2024/Aston-Villa-Stats",
    "https://fbref.com/en/squads/361ca564/2023-2024/Tottenham-Hotspur-Stats",
    "https://fbref.com/en/squads/cff3d9bb/2023-2024/Chelsea-Stats",
    "https://fbref.com/en/squads/b2b47a98/2023-2024/Newcastle-United-Stats",
    "https://fbref.com/en/squads/19538871/2023-2024/Manchester-United-Stats",
    "https://fbref.com/en/squads/7c21e445/2023-2024/West-Ham-United-Stats",
    "https://fbref.com/en/squads/47c64c55/2023-2024/Crystal-Palace-Stats",
    "https://fbref.com/en/squads/d07537b9/2023-2024/Brighton-and-Hove-Albion-Stats",
    "https://fbref.com/en/squads/4ba7cbea/2023-2024/Bournemouth-Stats",
    "https://fbref.com/en/squads/fd962109/2023-2024/Fulham-Stats",
    "https://fbref.com/en/squads/8cec06e1/2023-2024/Wolverhampton-Wanderers-Stats",
    "https://fbref.com/en/squads/d3fd31cc/2023-2024/Everton-Stats",
    "https://fbref.com/en/squads/cd051869/2023-2024/Brentford-Stats",
    "https://fbref.com/en/squads/e4a775cb/2023-2024/Nottingham-Forest-Stats",
    "https://fbref.com/en/squads/e297cd13/2023-2024/Luton-Town-Stats",
    "https://fbref.com/en/squads/943e8050/2023-2024/Burnley-Stats",
    "https://fbref.com/en/squads/1df6b87e/2023-2024/Sheffield-United-Stats"
]
data_all_out = {}
row_all_out = []
headers_out = []
def collect_data(url): #hàm để lấy dữ liệu của 1 đội
    global row_all_out , headers_out , data_all_out
    standings_url = url
    driver = webdriver.Chrome() # khoi tao 1 tronh duyet chrome
    driver.get(standings_url) # trong trình duyệt trên mở đường dẫn đã cho

    #Set thoi gian cho
    driver.implicitly_wait(10)

    for i in range(len(standings_url)): # xác định vị trí lấy tên đội
        if(standings_url[i] == '/'):
            start = i
    name_team = standings_url[start + 1 : len(standings_url) - 6] # lấy tên của đội
    headers = [] # dùng để lưu header của tất cả bảng
    data_all = {} # dùng để lưu dữ liệu của từng cầu thủ trong đội
    stats_standard = 'stats_standard_9' # đây là ID của từng bảng
    stats_keeper = 'stats_keeper_9'
    stats_shooting = 'stats_shooting_9'
    stats_passing = 'stats_passing_9'
    stats_passing_types = 'stats_passing_types_9'
    stats_gca = 'stats_gca_9'
    stats_defense = 'stats_defense_9'
    stats_possession = 'stats_possession_9'
    stats_playing_time = 'stats_playing_time_9'
    stats_misc = 'stats_misc_9'
    # xử lý bảng đầu tiên lấy dữ liệu của cá cầu thủ thi đấu trên 90 phút, để về sau các cầu thủ không có
    # trong danh sách cầu thủ trên thì không lấy dữ liệu

    # standard_stats

    soup = driver.find_element(By.ID , stats_standard) # xác định bảng thông qua ID

    html_content = soup.get_attribute('outerHTML')
    table = BeautifulSoup(html_content , 'html.parser') #dua ve html

    header_tmp = [th.get_text(strip=True) for th in table.find_all('th')] #lọc header
    for i , item in enumerate(header_tmp):
        if header_tmp[i] == 'Player':
            st = i
            break
    for i in range(len(header_tmp)): # sửa lại tên header theo ý muốn "chỉ số - nhóm - bảng"
        if i >= 12 and i <= 15:
            header_tmp[i] += '-Playing_Time-standard_stats'
        elif i >= 16 and i <= 23:
            header_tmp[i] += '-Performace-standard_stats'
        elif i >= 24 and i <= 27:
            header_tmp[i] += '-Expected-standard_stats' 
        elif i >= 28 and i <= 30:
            header_tmp[i] += '-Progression-standard_stats'
        elif i >= 31 and i <= 40:
            header_tmp[i] += '-Per_90_Minutes-standard_stats' 
    headers = headers + header_tmp[st:st + 33] # lọc lấy header chính để tạo dataframe sau này
    headers.insert(2, 'Team')
    data_rows = table.find_all('tr' , {'data-row' : True , 'class' : False}) # lọc ra các row
    rows = []
    for row in data_rows:
        if row.find('td', {'data-stat': 'minutes'}): # check cầu thủ có thi đấu trên 90 phút không
            minutes = row.find('td', {'data-stat': 'minutes'}).get_text(strip=True).replace(',', '') # lấy số phút thi đấu
            if minutes.isdigit() and int(minutes) > 90:
                cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])] # đưa dữ liệu cầu thủ về list
                cells.insert(2, name_team) # chèn thêm tên đội vào do ban dầu chưa có
                rows.append(cells) # lưu dữ liệu của từng cầu thủ vào 1 danh sách
                # ['name' , 'nation' , 'team' , 'pos', ....]
    data_all = {i[0] : i[:len(i) - 1] for i in rows} # lấy tên cầu thủ làm key và value là dữ liệu của cầu thủ đó

    # Goalkeeping(a):

    soup = driver.find_element(By.ID , stats_keeper) # bước đầu lặp lại y hệt bảng trên
    html_content = soup.get_attribute('outerHTML')
    table = BeautifulSoup(html_content , 'html.parser')
    header_tmp = [th.get_text(strip=True) for th in table.find_all('th')]
    for i in range(len(header_tmp)):
        if i >= 13 and i <= 22:
            header_tmp[i] += '-Performance-Goalkeeping'
        elif i >= 23 and i <= 28:
            header_tmp[i] += '-Penalty_kicks-Goalkeeping'
    headers = headers + header_tmp[13:28] # nối header bảng mới với header bảng cũ
    data_rows = table.find_all('tr' , {'data-row' : True , 'class' : False})
    rows = []
    for row in data_rows:
        if row.find('td', {'data-stat': 'gk_minutes'}):
            minutes = row.find('td', {'data-stat': 'gk_minutes'}).get_text(strip=True).replace(',', '')
            if minutes.isdigit() and int(minutes) > 90:
                cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
                rows.append(cells)
    row_out = [] # danh sách  dữ liệu cầu thủ về sau tạo thành dataframe
    #[['name' , 'nation' , 'team' , 'pos', ....], ['name' , 'nation' , 'team' , 'pos', ....], .....]
    for key , value in data_all.items(): # kiem tra các cầu thủ có trong dict có xuất hiện trong bảng không
        check = 1
        for i in rows:
            if(i[0] == key): # nếu cầu thủ có trong dict trùng tên vs cầu thủ trong bảng
                data_all[i[0]] += i[8:23] # ta nối dữ liệu
                check = 0
        if check == 1: # nếu cầu thủ trong dict không xuất hiện trong bảng
            data_all[key] += ['N/a']*15
        row_out.append(data_all[key]) # cập nhập lại data cầu thủ
    #shooting 
    # ta lặp lại y hệt bảng trên cho tới khi hết bảng
    soup = driver.find_element(By.ID , stats_shooting)
    html_content = soup.get_attribute('outerHTML')
    table = BeautifulSoup(html_content , 'html.parser')
    header_tmp = [th.get_text(strip=True) for th in table.find_all('th')]
    for i in range(len(header_tmp)):
        if i >= 9 and i <= 20:
            header_tmp[i] += '-Standard-Shooting'
        elif i >= 21 and i <= 25:
            header_tmp[i] += '-Expected-Shooting'
    headers = headers + header_tmp[9:25]
    data_rows = table.find_all('tr' , {'data-row' : True , 'class' : False})
    rows = []
    for row in data_rows:
        cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        rows.append(cells)
    row_out = []
    for key , value in data_all.items():
        check = 0
        for i in rows:
            if(key in i):
                data_all[i[0]] += i[5:21]
                check = 1
        if check == 0:
            data_all[key] += ['N/a']*16
        row_out.append(data_all[key])
    #Passing
    soup = driver.find_element(By.ID , stats_passing)
    html_content = soup.get_attribute('outerHTML')
    table = BeautifulSoup(html_content , 'html.parser')
    header_tmp = [th.get_text(strip=True) for th in table.find_all('th')]
    for i in range(len(header_tmp)):
        if i >= 14 and i <= 18:
            header_tmp[i] += '-Total-Passing'
        elif i >= 19 and i <= 21:
            header_tmp[i] += '-Short-Passing'
        elif i >= 22 and i <= 24:
            header_tmp[i] += '-Medium-Passing'
        elif i >= 25 and i <= 28:
            header_tmp[i] += '-Long-Passing'
        elif i >= 29 and i <= 37:
            header_tmp[i] += '-Expected-Passing'
    headers = headers + header_tmp[14:37]
    data_rows = table.find_all('tr' , {'data-row' : True , 'class' : False})
    rows = []
    for row in data_rows:
        cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        rows.append(cells)
    row_out = []
    for key , value in data_all.items():
        check = 1
        for i in rows:
            if(key in i):
                data_all[i[0]] += i[5:28]
                check = 0
        if check == 1:
            data_all[key] += ['N/a']*13
        row_out.append(data_all[key])
    #Pass_types
    soup = driver.find_element(By.ID , stats_passing_types)
    html_content = soup.get_attribute('outerHTML')
    table = BeautifulSoup(html_content , 'html.parser')
    header_tmp = [th.get_text(strip=True) for th in table.find_all('th')]
    for i in range(len(header_tmp)):
        if i >= 11 and i <= 18:
            header_tmp[i] += '-Pass_types-Pass_types'
        elif i >= 19 and i <= 21:
            header_tmp[i] += '-Corner_Kicks-Pass_types'
        elif i >= 22 and i <= 24:
            header_tmp[i] += '-Outcomes-Pass_types'
    headers = headers + header_tmp[11:25]
    data_rows = table.find_all('tr' , {'data-row' : True , 'class' : False})
    rows = []
    for row in data_rows:
        cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        rows.append(cells)
    row_out = []
    for key , value in data_all.items():
        check = 0
        for i in rows:
            if(key in i):
                data_all[i[0]] += i[6:20]
                check = 1
        if check == 0:
            data_all[key] += ['N/a']*14
        row_out.append(data_all[key])
    #Goal and shoot Creation
    soup = driver.find_element(By.ID , stats_gca)
    html_content = soup.get_attribute('outerHTML')
    table = BeautifulSoup(html_content , 'html.parser')
    header_tmp = [th.get_text(strip=True) for th in table.find_all('th')]
    for i in range(len(header_tmp)):
        if i >= 11 and i <= 12:
            header_tmp[i] += '-SCA-Goal_and_shoot_Creation'
        elif i >= 13 and i <= 18:
            header_tmp[i] += '-SCA_types-Goal_and_shoot_Creation'
        elif i >= 19 and i <= 20:
            header_tmp[i] += '-GCA-Goal_and_shoot_Creation'
        elif i >= 21 and i <= 26:
            header_tmp[i] += '-GCS_types-Goal_and_shoot_Creation'
    headers = headers + header_tmp[11:27]
    data_rows = table.find_all('tr' , {'data-row' : True , 'class' : False})
    rows = []
    for row in data_rows:
        cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        rows.append(cells)
    row_out = []
    for key , value in data_all.items():
        check = 0
        for i in rows:
            if(key in i):
                data_all[i[0]] += i[5:21]
                check = 1
        if check == 0:
            data_all[key] += ['N/a']*16
        row_out.append(data_all[key])
    # Defensive Actions
    soup = driver.find_element(By.ID , stats_defense)
    html_content = soup.get_attribute('outerHTML')
    table = BeautifulSoup(html_content , 'html.parser')
    header_tmp = [th.get_text(strip=True) for th in table.find_all('th')]
    for i in range(len(header_tmp)):
        if i >= 11 and i <= 15:
            header_tmp[i] += '-Tackles-Defensive_Actions'
        elif i >= 16 and i <= 20:
            header_tmp[i] += '-Challenges-Defensive_Actions'
        elif i >= 21 and i <= 26:
            header_tmp[i] += '-Blocks-Defensive_Actions'
    headers = headers + header_tmp[11:27]
    data_rows = table.find_all('tr' , {'data-row' : True , 'class' : False})
    rows = []
    for row in data_rows:
        cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        rows.append(cells)
    row_out = []
    for key , value in data_all.items():
        check = 0
        for i in rows:
            if(key in i):
                data_all[i[0]] += i[5:21]
                check = 1
        if check == 0:
            data_all[key] += ['N/a']*16
        row_out.append(data_all[key])
    #Possession
    soup = driver.find_element(By.ID , stats_possession)
    html_content = soup.get_attribute('outerHTML')
    table = BeautifulSoup(html_content , 'html.parser')
    header_tmp = [th.get_text(strip=True) for th in table.find_all('th')]
    for i in range(len(header_tmp)):
        if i >= 11 and i <= 17:
            header_tmp[i] += '-Touches-Possession'
        elif i >= 18 and i <= 22:
            header_tmp[i] += '-Take_Ons-Possession'
        elif i >= 23 and i <= 30:
            header_tmp[i] += '-Carries-Possession'
        elif i >= 31 and i <= 32:
            header_tmp[i] += '-Receiving-Possession'
    headers = headers + header_tmp[11:33]
    data_rows = table.find_all('tr' , {'data-row' : True , 'class' : False})
    rows = []
    for row in data_rows:
        cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        rows.append(cells)
    row_out = []
    for key , value in data_all.items():
        check = 0
        for i in rows:
            if(key in i):
                data_all[i[0]] += i[5:27]
                check = 1
        if check == 0:
            data_all[key] += ['N/a']*22
        row_out.append(data_all[key])
    # playing time
    soup = driver.find_element(By.ID , stats_playing_time)
    html_content = soup.get_attribute('outerHTML')
    table = BeautifulSoup(html_content , 'html.parser')
    header_tmp = [th.get_text(strip=True) for th in table.find_all('th')]
    for i in range(len(header_tmp)):
        if i >= 16 and i <= 18:
            header_tmp[i] += '-Starts-Playing_time'
        elif i >= 19 and i <= 21:
            header_tmp[i] += '-Sub-Playing_time'
        elif i >= 22 and i <= 27:
            header_tmp[i] += '-Team_Success-Playing_time'
        elif i >= 28 and i <= 32:
            header_tmp[i] += '-Team_Success(xG)-Playing_time'
    headers = headers + header_tmp[16:33]
    data_rows = table.find_all('tr' , {'data-row' : True , 'class' : False})
    rows = []
    for row in data_rows:
        cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        rows.append(cells)
    row_out = []
    for key , value in data_all.items():
        check = 0
        for i in rows:
            if(key in i):
                data_all[i[0]] += i[9:26]
                check = 1
        if check == 0:
            data_all[key] += ['N/a']*17
        row_out.append(data_all[key])
    # Miscellaneous Stats
    soup = driver.find_element(By.ID , stats_misc)
    html_content = soup.get_attribute('outerHTML')
    table = BeautifulSoup(html_content , 'html.parser')
    header_tmp = [th.get_text(strip=True) for th in table.find_all('th')]
    for i in range(len(header_tmp)):
        if i >= 9 and i <= 21:
            header_tmp[i] += '-Performance-Miscellaneous_Stats'
        elif i >= 22 and i <= 24:
            header_tmp[i] += '-Aerial_Duels-Miscellaneous_Stats'
    headers = headers + header_tmp[9:25]
    data_rows = table.find_all('tr' , {'data-row' : True , 'class' : False})
    rows = []
    for row in data_rows:
        cells = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        rows.append(cells)
    row_out = []
    for key , value in data_all.items():
        check = 0
        for i in rows:
            if(key in i):
                data_all[i[0]] += i[5:21]
                check = 1
        if check == 0:
            data_all[key] += ['N/a']*16
        row_out.append(data_all[key])
    row_out = row_out[:len(row_out) - 2] # bỏ 2 dòng cuối là dữ liệu thừa
    headers_out = headers # lấy header cho dataframe sau cùng
    row_all_out = row_all_out + row_out # cập nhập thêm dữ liệu cầu thủ của các đội
    data_all_out = {**data_all_out, **data_all} # cập nhật thêm cầu thủ của các đội
    driver.quit() # đóng trình duyệt chrome
for url in urls: # lặp duyệt hết tất cả các câu lạc bộ
    collect_data(url)

row_all_out = sorted(row_all_out, key=lambda x: (x[0], -int(x[4]))) # sắp xếp theo tên
df = pd.DataFrame(row_all_out , columns=headers_out) # tạo dataframe
# Thay thế bất kỳ giá trị rỗng hoặc NaN nào bằng 'N/a'
df = df.replace({None: 'N/a', '': 'N/a'}).fillna('N/a')
# Ghi dữ liệu ra file CSV
df.to_csv('results.csv', index=False, encoding='utf-8-sig')

print("Dữ liệu đã được ghi ra file 'results.csv'.")
