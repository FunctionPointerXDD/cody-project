import pandas as pd

def searching_analysis():
    # 데이터 로드
    structure = pd.read_csv("dataFile/area_struct.csv")
    category = pd.read_csv("dataFile/area_category.csv")
    map_data = pd.read_csv("dataFile/area_map.csv")
    
    # 카테고리 매핑
    category_dict = {**category.set_index(category.columns[0])[category.columns[1]].to_dict(), 0: " etc"}
    
    # 카테고리 매핑 적용 및 병합, 정렬
    merged_data = (map_data
                   .merge(structure.assign(**{structure.columns[2]: structure[structure.columns[2]].map(category_dict)}), 
                          on=["x", "y"], how="outer")
                   .sort_values("area")
                   .reset_index(drop=True))
    
    # Area1 데이터 필터링 및 저장
    merged_data[merged_data["area"] == 1].reset_index(drop=True).to_csv(
        'dataFile/mas_map.csv', index=False, encoding='utf-8-sig')
    
    return merged_data

def print_report(data):
    summary = data["category"].value_counts().sort_index().to_frame("개수")
    print("구조물 종류별 개수:")
    print(summary)

if __name__ == "__main__":
    print_report(searching_analysis())
