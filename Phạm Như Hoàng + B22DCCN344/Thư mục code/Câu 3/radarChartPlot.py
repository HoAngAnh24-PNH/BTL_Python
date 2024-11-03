import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def radar_chart(player1_data, player2_data, attributes, name1 , name2):
    # Số lượng chỉ số
    num_vars = len(attributes)

    # Thiết lập góc cho các chỉ số
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Trả về đầu điểm đầu để tạo hình tròn
    player1_data = np.concatenate((player1_data, [player1_data[0]]))
    player2_data = np.concatenate((player2_data, [player2_data[0]]))
    angles += angles[:1]

    # Vẽ biểu đồ
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    
    ax.fill(angles, player1_data, color='red', alpha=0.25, label=name1)
    ax.fill(angles, player2_data, color='blue', alpha=0.25, label=name2)
    
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(attributes)

    plt.legend(loc='upper right')
    plt.title('Radar Chart Comparison')
    plt.show()

def main():

    df = pd.read_csv('results.csv')
    # Thiết lập phân tích tham số
    parser = argparse.ArgumentParser(description='Radar Chart Comparison between Players')
    parser.add_argument('--p1', type=str, required=True, help='Player 1 Name')
    parser.add_argument('--p2', type=str, required=True, help='Player 2 Name')
    parser.add_argument('--Attribute', type=str, required=True, help='Comma separated list of attributes')
    args = parser.parse_args()
    name1 = args.p1
    name2 = args.p2
    # Tách các thuộc tính
    attributes = args.Attribute.split(',')

    # Lấy dữ liệu cho các cầu thủ
    player1_data = df.loc[df['Player'] == args.p1, attributes].values.flatten()
    player2_data = df.loc[df['Player'] == args.p2, attributes].values.flatten()

    # Kiểm tra xem dữ liệu có hợp lệ không
    if player1_data.size == 0 or player2_data.size == 0:
        raise ValueError("Player not found or attributes invalid.")
    # Vẽ biểu đồ radar
    radar_chart(player1_data, player2_data, attributes, name1 , name2)

if __name__ == "__main__":
    main()