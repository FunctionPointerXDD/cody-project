"""
map_direct_save.py

- MyHome(시작점)에서 BandalgomCoffee(도착점)까지 BFS 알고리즘으로 최단 경로 탐색
- ConstructionSite==1 위치는 통과 불가
- 경로를 home_to_cafe.csv로 저장
- 지도 위에 빨간 선으로 경로를 시각화해 map_final.png 생성
"""

import pandas as pd
import matplotlib.pyplot as plt
from collections import deque
from typing import Dict, List, Tuple
from exceptions import PathNotFound


def load_data(path: str = "dataFile/mas_map.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    if "category" in df.columns:
        df["category"] = df["category"].str.strip()
    return df


def build_graph(df: pd.DataFrame) -> Dict[Tuple[int, int], List[Tuple[int, int]]]:
    """
    4-방향 이동 가능 좌표 그래프 생성
    ConstructionSite==1 위치 제외
    """
    traversable = set()
    for _, r in df.iterrows():
        if int(r.get("ConstructionSite", 0)) != 1:
            point = (int(r.x), int(r.y))
            traversable.add(point)

    adj: Dict[Tuple[int, int], List[Tuple[int, int]]] = {pt: [] for pt in traversable}
    for x, y in traversable:
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nb = (x + dx, y + dy)
            if nb in traversable:
                adj[(x, y)].append(nb)
    return adj


def bfs_shortest_path(
    adj: Dict[Tuple[int, int], List[Tuple[int, int]]],
    start: Tuple[int, int],
    targets: List[Tuple[int, int]],
) -> List[Tuple[int, int]]:
    """
    BFS를 이용해 start에서 end까지 최단 경로를 찾습니다.

    :param adj: 인접 리스트 그래프
    :param start: 시작 좌표
    :param end: 도착 좌표
    :return: 최단 경로 리스트 (없으면 빈 리스트)
    """
    target_sets = set(targets)
    prev: Dict[Tuple[int, int], Tuple[int, int]] = {}
    visited = set([start])
    queue = deque([start])

    while queue:
        u = queue.popleft()
        if u in target_sets:
            break
        for v in adj[u]:
            if v not in visited:
                visited.add(v)
                prev[v] = u
                queue.append(v)

    # 경로 역추적
    path: List[Tuple[int, int]] = []
    cur = u
    while cur != start:
        path.append(cur)
        cur = prev.get(cur)
        if cur is None:
            return []
    path.append(start)
    path.reverse()
    return path


def save_path(
    df: pd.DataFrame,
    path: List[Tuple[int, int]],
    output_csv: str = "dataFile/home_to_cafe.csv",
) -> None:
    """
    최단 경로를 CSV 파일로 저장

    :param df: 원본 DataFrame
    :param path: 좌표 리스트
    :param output_csv: 출력 파일명
    :return: 저장된 DataFrame
    """
    df_path = pd.DataFrame(path, columns=["x", "y"])
    info = df[["x", "y", "category"]]
    df_path = df_path.merge(info, on=["x", "y"], how="left")
    df_path.to_csv(output_csv, index=False, encoding="utf-8-sig")
    # print(f"{output_csv} 저장 완료 (이동 횟수: {len(path) - 1})")


def plot_path(
    df: pd.DataFrame, path: List[Tuple[int, int]], output_img: str = "img/map_final.png"
) -> None:
    """
    지도 위에 최단 경로 빨간 선 시각화

    :param df: 원본 DataFrame
    :param path: 좌표 리스트
    :param output_img: 출력 이미지 파일명
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    x_min, x_max = int(df.x.min()), int(df.x.max())
    y_min, y_max = int(df.y.min()), int(df.y.max())
    ax.set_xlim(x_min - 0.5, x_max + 0.5)
    ax.set_ylim(y_min - 0.5, y_max + 0.5)
    ax.invert_yaxis()
    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))
    ax.grid(True, linestyle="--", linewidth=0.5)
    ax.set_aspect("equal")

    styles = {
        "Apartment": {"marker": "o", "s": 100, "color": "brown", "label": "Apartment"},
        "Building": {"marker": "o", "s": 100, "color": "brown", "label": "Building"},
        "BandalgomCoffee": {
            "marker": "s",
            "s": 150,
            "color": "green",
            "label": "BandalgomCoffee",
        },
        "MyHome": {"marker": "^", "s": 150, "color": "green", "label": "MyHome"},
    }
    for cat, style in styles.items():
        pts = df[df["category"] == cat]
        if not pts.empty:
            ax.scatter(pts.x, pts.y, **style)
    if "ConstructionSite" in df.columns:
        cs = df[df["ConstructionSite"] == 1]
        if not cs.empty:
            ax.scatter(
                cs.x,
                cs.y,
                marker="s",
                s=200,
                color="lightgray",
                label="Constructionsite",
            )

    xs, ys = zip(*path)
    ax.plot(xs, ys, color="red", linewidth=2, label="shortest route")
    ax.legend(loc="lower right")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("MyHome → BandalgomCoffee shortest route")
    plt.tight_layout()
    plt.savefig(output_img, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"{output_img} 저장 완료")


def main():
    try:
        df = load_data()
        adj = build_graph(df)

        # 시작/도착점 설정
        start_row = df[df["category"] == "MyHome"]
        sx, sy = int(start_row.iloc[0].x), int(start_row.iloc[0].y)
        start = (sx, sy)

        coffee_df = df[df["category"] == "BandalgomCoffee"]
        targets = []
        for _, row in coffee_df.iterrows():
            x = int(row.x)
            y = int(row.y)
            targets.append((x, y))

        path = bfs_shortest_path(adj, start, targets)
        if not path:
            raise PathNotFound

        save_path(df, path)
        plot_path(df, path)

    except FileNotFoundError as e:
        print(f"파일이 없습니다.{e.filename}")
    except PermissionError as e:
        print(f"파일 권한이 없습니다.{e.filename}")
    except PathNotFound:
        print("경로를 찾을 수 없습니다.")


if __name__ == "__main__":
    main()
