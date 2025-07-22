import pandas as pd


def Serching_Analysis() -> pd.DataFrame:
    struct, category, map_data = [pd.read_csv(
        f"dataFile/area_{f}.csv") for f in ['struct', 'category', 'map']]

    # 카테고리 매핑, 적용
    category_dict = {
        **category.set_index(category.columns[0])[category.columns[1]].to_dict(),
        0: "etc",
    }
    struct[struct.columns[2]] = struct[struct.columns[2]].map(category_dict)

    # 좌표 기준, 아우터 조인 실행 후, area 기준으로 정렬
    merged_map_data = (
        map_data.merge(struct, on=["x", "y"], how="outer")
        .sort_values(by="area")
        .reset_index(drop="True")
    )

    # Area1 데이터 필터링 결과 저장
    merged_map_data[merged_map_data["area"] == 1].reset_index(drop=True).to_csv(
        "dataFile/mas_map.csv", index=False, encoding="utf-8-sig"
    )

    return merged_map_data


def main():
    data = Serching_Analysis().value_counts().sort_index().to_frame("개수")
    print("구조물 종류별 개수:")
    print(data)


if __name__ == "__main__":
    main()
