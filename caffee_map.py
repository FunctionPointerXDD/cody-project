import pandas as pd

DATA_DIR = 'dataFile/'
STRUCT_FILE = DATA_DIR + 'area_struct.csv'
CATEGORY_FILE = DATA_DIR + 'area_category.csv'
MAP_FILE = DATA_DIR + 'area_map.csv'

REQUIRED_COLUMNS = {
    STRUCT_FILE: ['x', 'y', 'category', 'area'],
    CATEGORY_FILE: ['category', 'struct'],
    MAP_FILE: ['x', 'y', 'ConstructionSite'],
}


def Serching_Analysis() -> pd.DataFrame:
    struct, category, map_data = [
        pd.read_csv(f'dataFile/area_{f}.csv') for f in ['struct', 'category', 'map']
    ]

    check_valid_data(struct, category, map_data)

    # 카테고리 매핑, 적용
    category_dict = {
        **category.set_index(category.columns[0])[category.columns[1]].to_dict(),
        0: 'etc',
    }
    struct[struct.columns[2]] = struct[struct.columns[2]].map(category_dict)

    # 좌표 기준, 아우터 조인 실행 후, area 기준으로 정렬
    merged_map_data = (
        map_data.merge(struct, on=['x', 'y'], how='outer')
        .sort_values(by='area')
        .reset_index(drop=True)
    )

    # 병합 데이터 .csv파일로 저장
    merged_map_data.to_csv('dataFile/mas_map.csv',
                           index=False, encoding='utf-8-sig')

    # Area1 데이터 필터링
    return merged_map_data[merged_map_data['area'] == 1].reset_index(drop=True)


def check_valid_file():
    all_data = dict()
    try:
        for file_path in [STRUCT_FILE, CATEGORY_FILE, MAP_FILE]:
            data = pd.read_csv(file_path)
            if data.empty:
                # 헤더만 있고 데이터가 없는 경우
                raise Exception(f'파일에 데이터가 없습니다: {file_path}')

            all_data[file_path] = data
            print(f">> 성공: '{file_path}' 로드 완료.")
    except FileNotFoundError:
        # 파일이 위치에 없음
        raise Exception(f'파일을 찾을 수 없습니다: {file_path}')
    except pd.errors.EmptyDataError:
        # 파일이 완전히 비어있음(컬럼도 없음)
        raise Exception(f'파일이 비어있습니다: {file_path}')

    for file_path, data in all_data.items():
        expected_cols = REQUIRED_COLUMNS[file_path]
        data.columns = data.columns.str.strip()
        current_cols = data.columns.tolist()
        # 누락된 컬럼 찾기
        missing = [col for col in expected_cols if col not in current_cols]
        if missing:
            raise Exception(f'{file_path} 필수 컬럼 누락: {missing}')

        # 정해져 있지 않은 컬럼 찾기
        extra = [col for col in current_cols if col not in expected_cols]
        if extra:
            raise Exception(f'{file_path} 예상치 못한 컬럼 발생: {extra}')


def check_valid_data(struct_data, category_data, map_data):
    for col in ['x', 'y', 'category', 'area']:
        # 좌표, 공사현장은 정수 값
        if not pd.api.types.is_integer_dtype(struct_data[col]):
            raise Exception(f"'{STRUCT_FILE}'의 '{col}' 컬럼은 정수여야 합니다.")
    # 공사현장 정수값, 0 OR 1
    if not pd.api.types.is_integer_dtype(map_data['ConstructionSite']):
        raise Exception(f"'{MAP_FILE}'의 'ConstructionSite' 컬럼은 정수여야 합니다.")
    if not map_data['ConstructionSite'].isin([0, 1]).all():
        raise Exception(
            f"'{MAP_FILE}'의 'ConstructionSite' 컬럼에 0 또는 1이 아닌 값이 있습니다."
        )

    # 카테고리(ID) 정수값, 0~4
    if not pd.api.types.is_integer_dtype(category_data['category']):
        raise Exception(f"'{CATEGORY_FILE}'의 'category' 컬럼은 정수여야 합니다.")
    invalid_categories = struct_data[~struct_data['category'].isin(range(5))]
    if not invalid_categories.empty:
        raise Exception(f'{STRUCT_FILE}에 잘못된 category id가 있습니다')
    # 중복값 찾기
    if struct_data.duplicated(subset=['x', 'y']).any():
        raise Exception(f"'{STRUCT_FILE}'에 중복된 (x, y) 좌표가 있습니다.")
    if map_data.duplicated(subset=['x', 'y']).any():
        raise Exception(f"'{MAP_FILE}'에 중복된 (x, y) 좌표가 있습니다.")
    if category_data.duplicated(subset=['category']).any():
        raise Exception(f"'{CATEGORY_FILE}'에 중복된 카테고리 ID가 있습니다.")


def main():
    try:
        check_valid_file()
        data = (
            Serching_Analysis()['category'].value_counts(
            ).sort_index().to_frame('개수')
        )
        print('구조물 종류별 개수:')
        print(data)

    except Exception as e:
        print(f'에러 발생: {e}')


if __name__ == '__main__':
    main()
