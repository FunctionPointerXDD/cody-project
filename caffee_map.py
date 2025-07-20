import pandas as pd


def Serching_Analysis():
    structure = pd.read_csv("dataFile/area_struct.csv")
    category = pd.read_csv("dataFile/area_category.csv")
    map_data = pd.read_csv("dataFile/area_map.csv")

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
        .reset_index(drop="True")
    )

    # Area1 데이터 필터링 결과 저장
    merged_map_data[merged_map_data["area"] == 1].reset_index(drop=True).to_csv(
        "dataFile/mas_map.csv", index=False, encoding="utf-8-sig"
    )

    return merged_map_data


def print_report(data):
    summary = data["category"].value_counts().sort_index().to_frame("개수")
    print("구조물 종류별 개수:")
    print(summary)


def main():
    print_report(Serching_Analysis())


if __name__ == "__main__":
    main()
