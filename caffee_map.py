#!/usr/bin/env python3

import pandas as pd

def load_csv_files():
    """CSV 파일 불러오기"""
    area_map = pd.read_csv('dataFile/area_map.csv')
    area_struct = pd.read_csv('dataFile/area_struct.csv')
    area_category = pd.read_csv('dataFile/area_category.csv')
    return area_map, area_struct, area_category

def merge_and_analyze(area_map, area_struct, area_category):
    """
    데이터 병합, 카테고리 이름 매핑, area 기준 정렬, area 1 필터링
    """
    # area_category 컬럼 공백 제거
    area_category.columns = area_category.columns.str.strip()

    # area_struct에 category 이름 매핑
    area_struct = area_struct.merge(
        area_category,
        how='left',
        on='category'
    )

    # 컬럼명 struct → category_name으로 변경
    area_struct.rename(columns={'struct': 'category_name'}, inplace=True)

    # area_map과 area_struct 병합
    merged_df = area_map.merge(
        area_struct,
        how='left',
        on=['x', 'y']
    )

    # area 기준으로 정렬
    merged_df.sort_values(by=['area', 'x', 'y'], inplace=True)

    # area 1 데이터만 필터링
    area_1_df = merged_df[merged_df['area'] == 1]

    return merged_df, area_1_df

def print_summary_by_category(area_1_df):
    """구조물 종류별 요약 통계 출력"""
    summary = area_1_df['category_name'].value_counts()
    print('=== 구조물 종류별 요약 통계 ===')
    print(summary)

def main():
    area_map, area_struct, area_category = load_csv_files()

    print('=== area_map.csv ===')
    print(area_map.head())

    print('=== area_struct.csv ===')
    print(area_struct.head())

    print('=== area_category.csv ===')
    print(area_category.head())

    merged_df, area_1_df = merge_and_analyze(
        area_map,
        area_struct,
        area_category
    )

    print('=== 병합된 데이터 (상위 5개) ===')
    print(merged_df.head())

    print('=== area 1 데이터 ===')
    print(area_1_df)

    print_summary_by_category(area_1_df)

if __name__ == '__main__':
    main()
