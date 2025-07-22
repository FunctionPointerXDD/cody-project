#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt


def load_merged_data():
    """1단계에서 생성된 병합 데이터를 불러오기"""
    # 1단계 caffee_map.py 코드에서 merged_df를 csv로 저장하지 않았으므로
    # 여기서는 다시 병합 과정을 수행
    area_map = pd.read_csv('dataFile/area_map.csv')
    area_struct = pd.read_csv('dataFile/area_struct.csv')
    area_category = pd.read_csv('dataFile/area_category.csv')

    area_category.columns = area_category.columns.str.strip()

    area_struct = area_struct.merge(
        area_category,
        how='left',
        on='category'
    )
    area_struct.rename(columns={'struct': 'category_name'}, inplace=True)

    merged_df = area_map.merge(
        area_struct,
        how='left',
        on=['x', 'y']
    )
    return merged_df


def draw_map(merged_df):
    """지도 시각화 및 저장"""
    plt.figure(figsize=(10, 10))
    ax = plt.gca()

    max_x = merged_df['x'].max()
    max_y = merged_df['y'].max()

    # 그리드 라인
    for x in range(1, max_x + 2):
        ax.axvline(x - 0.5, color='lightgrey', linestyle='--', linewidth=0.5)
    for y in range(1, max_y + 2):
        ax.axhline(y - 0.5, color='lightgrey', linestyle='--', linewidth=0.5)

    # 각 구조물 시각화
    for _, row in merged_df.iterrows():
        x = row['x']
        y = max_y - row['y'] + 1  # 좌측 상단 (1,1) 기준

        
        if row['ConstructionSite'] == 1:
            # 건설 현장: 회색 사각형
            ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1,
                                       color='grey'))
        elif row['category_name'] == 'Apartment':
            # 아파트: 갈색 원형
            ax.plot(x, y, 'o', color='brown', markersize=12)
        elif row['category_name'] == 'Building':
            # 빌딩: 갈색 원형
            ax.plot(x, y, 'o', color='brown', markersize=12)
        elif row['category_name'] == 'BandalgomCoffee':
            # 반달곰 커피: 녹색 사각형
            ax.add_patch(plt.Rectangle((x - 0.3, y - 0.3), 0.6, 0.6,
                                       color='green'))
        elif row['category_name'] == 'MyHome':
            # 내 집: 녹색 삼각형
            ax.plot(x, y, '^', color='green', markersize=12)

        
        # 좌측 상단 라벨
        for x in range(1, max_x + 1):
            ax.text(1, max_y + 0.2, '(1,1)', color='black', fontsize=8)

        # 우측 하단 라벨
        for y in range(1, max_y +1):
            ax.text(max_x, 0.2, f'({max_x},{max_y})', color='black', fontsize=8)

    # 범례 추가
    from matplotlib.lines import Line2D
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Apartment/Building',
               markerfacecolor='brown', markersize=10),
        Line2D([0], [0], marker='s', color='w', label='Bandalgom Coffee',
               markerfacecolor='green', markersize=10),
        Line2D([0], [0], marker='^', color='w', label='MyHome',
               markerfacecolor='green', markersize=10),
        Line2D([0], [0], marker='s', color='grey', label='Construction Site',
               markerfacecolor='grey', markersize=10)
    ]
    ax.legend(handles=legend_elements, loc='upper right')

    # 축 설정
    ax.set_xlim(0.5, max_x + 0.5)
    ax.set_ylim(0.5, max_y + 0.5)
    ax.set_xticks(range(1, max_x + 1))
    ax.set_yticks(range(1, max_y + 1))
    ax.set_aspect('equal')
    ax.set_title('Area Map Visualization')

    # 이미지 저장
    plt.savefig('results/map.png')
    plt.close()


def main():
    merged_df = load_merged_data()
    draw_map(merged_df)


if __name__ == '__main__':
    main()
