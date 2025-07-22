#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
from collections import deque


def load_merged_data():
    """1단계에서 생성된 병합 데이터를 불러오기"""
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

    merged_df['category_name'] = merged_df['category_name'].str.strip()

    return merged_df


def bfs_shortest_path(grid, start, goal, obstacles, max_x, max_y):
    """BFS를 활용한 최단 경로 탐색"""
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상하좌우

    while queue:
        (x, y), path = queue.popleft()

        if (x, y) == goal:
            return path

        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            if 1 <= nx <= max_x and 1 <= ny <= max_y:
                if (nx, ny) not in visited and (nx, ny) not in obstacles:
                    queue.append(((nx, ny), path + [(nx, ny)]))
                    visited.add((nx, ny))

    return None


def save_path_to_csv(path):
    """경로를 CSV로 저장"""
    df = pd.DataFrame(path, columns=['x', 'y'])
    df.to_csv('results/home_to_cafe.csv', index=False)


def draw_final_map(merged_df, path):
    """최종 경로가 포함된 지도 시각화"""
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
            ax.add_patch(plt.Rectangle((x - 0.5, y - 0.5), 1, 1, color='grey'))
        elif row['category_name'] == 'Apartment':
            ax.plot(x, y, 'o', color='brown', markersize=12)
        elif row['category_name'] == 'Building':
            ax.plot(x, y, 'o', color='brown', markersize=12)
        elif row['category_name'] == 'BandalgomCoffee':
            ax.add_patch(plt.Rectangle((x - 0.3, y - 0.3), 0.6, 0.6, color='green'))
        elif row['category_name'] == 'MyHome':
            ax.plot(x, y, '^', color='green', markersize=12)

    # 최단 경로 그리기
    if path:
        path_x = [p[0] for p in path]
        path_y = [max_y - p[1] + 1 for p in path]
        ax.plot(path_x, path_y, color='red', linewidth=2)

    # 축 설정
    ax.set_xlim(0.5, max_x + 0.5)
    ax.set_ylim(0.5, max_y + 0.5)
    ax.set_xticks(range(1, max_x + 1))
    ax.set_yticks(range(1, max_y + 1))
    ax.set_aspect('equal')
    ax.set_title('Final Map with Shortest Path')

    # 이미지 저장
    plt.savefig('results/map_final.png')
    plt.close()


def main():
    merged_df = load_merged_data()

    # 공백 제거
    merged_df['category_name'] = merged_df['category_name'].str.strip()

    print('=== merged_df category_name 고유값 ===')
    print(merged_df['category_name'].unique())

    # 시작점(MyHome)과 도착점(BandalgomCoffee) 찾기
    home_df = merged_df[merged_df['category_name'] == 'MyHome'][['x', 'y']]
    cafe_df = merged_df[merged_df['category_name'] == 'BandalgomCoffee'][['x', 'y']]

    if home_df.empty:
        print('MyHome 위치를 찾을 수 없습니다.')
        return

    if cafe_df.empty:
        print('BandalgomCoffee 위치를 찾을 수 없습니다.')
        return

    home = home_df.iloc[0]
    cafe = cafe_df.iloc[0]
    start = (home['x'], home['y'])
    goal = (cafe['x'], cafe['y'])

    max_x = merged_df['x'].max()
    max_y = merged_df['y'].max()

    # 장애물 위치(건설 현장) 좌표 집합
    obstacles = set(
        merged_df[merged_df['ConstructionSite'] == 1][['x', 'y']].apply(tuple, axis=1)
    )

    # BFS 최단 경로 탐색
    path = bfs_shortest_path(merged_df, start, goal, obstacles, max_x, max_y)

    if path:
        print('최단 경로를 찾았습니다.')
        save_path_to_csv(path)
        draw_final_map(merged_df, path)
    else:
        print('경로를 찾을 수 없습니다.')



if __name__ == '__main__':
    main()
