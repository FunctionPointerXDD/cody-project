import pandas as pd
from exceptions import ColumnError
from exceptions import RowError 


DATA_DIR = 'dataFile'

def validate_dataframe(df: pd.DataFrame, required_cols: list[str], name: str):
    missing_cols = [c for c in required_cols if c not in df.columns]
    if missing_cols:
        raise ColumnError(f"[{name}] 필수 컬럼 누락: {missing_cols}")

    if name == 'category':
        dup = df.duplicated(subset=['category'])
    else:
        dup = df.duplicated()
    if dup.any():
        raise RowError(f"[{name}] 중복된 행 존재: {df[dup].to_dict(orient='records')}")

    missing = df.isnull().any(axis=1)
    if missing.any():
        raise RowError(f"[{name}] 누락된 데이터 존재: {df[missing].to_dict(orient='records')}")


def serching_analysis() -> pd.DataFrame:
    structure = pd.read_csv(f'{DATA_DIR}/area_struct.csv')
    category = pd.read_csv(f'{DATA_DIR}/area_category.csv')
    map_data = pd.read_csv(f'{DATA_DIR}/area_map.csv')

    # 데이터 검증
    struct_cols = ['x', 'y', 'category', 'area']
    cate_cols = ['category', 'struct']
    map_cols = ['x', 'y', 'ConstructionSite']
    validate_dataframe(structure, struct_cols, "structure")
    validate_dataframe(category, cate_cols, "category")
    validate_dataframe(map_data, map_cols, "map_data")

    # 카테고리 매핑
    category_dict = {
        **category.set_index(category.columns[0])[category.columns[1]].to_dict(),
        0: " etc",
    }

    # 카테고리id -> 실제 이름
    structure[structure.columns[2]] = structure[structure.columns[2]].map(category_dict)

    # 좌표 기준, 아우터 조인 실행 후, area 기준으로 정렬
    merged_map_data = (
        map_data.merge(structure, on=["x", "y"], how="outer")
        .sort_values(by="area")
        .reset_index(drop=True)
    )

    # 병합 데이터 .csv파일로 저장
    merged_map_data.to_csv("dataFile/mas_map.csv", index=False, encoding="utf-8-sig")

    # Area1 데이터 필터링
    return merged_map_data[merged_map_data["area"] == 1].reset_index(drop=True)


def print_report(data) -> None:
    summary = data["category"].value_counts().sort_index().to_frame("개수")
    print("Area1 구조물 종류별 개수:")
    print(summary)


def main():
    try:
        print_report(serching_analysis())
    except FileNotFoundError as e:
        print(f'파일이 없습니다.{e.filename}')
    except PermissionError as e:
        print(f'파일 권한이 없습니다.{e.filename}')
    except (ColumnError, RowError) as e:
        print('Error:', e)

if __name__ == "__main__":
    main()


