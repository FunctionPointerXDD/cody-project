import pandas as pd
import matplotlib.pyplot as plt


def draw_map(input_file="dataFile/mas_map.csv", output_file="img/map.png"):
    df = pd.read_csv(input_file)

    # 좌표 범위 설정
    x_min, x_max = int(df["x"].min()), int(df["x"].max())
    y_min, y_max = int(df["y"].min()), int(df["y"].max())

    # 플롯 설정
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(x_min - 0.5, x_max + 0.5)
    ax.set_ylim(y_min - 0.5, y_max + 0.5)
    ax.invert_yaxis()
    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))
    ax.grid(True, which="both", linestyle="--", linewidth=0.5)
    ax.set_aspect("equal")

    # 구조물 스타일 정의
    category_styles = {
        1: dict(marker="o", s=150, color="saddlebrown", label="Apartment", zorder=2),
        2: dict(marker="o", s=150, color="saddlebrown", label="Building", zorder=2),
        3: dict(marker="^", s=150, color="green", label="MyHome", zorder=2),
        4: dict(marker="s", s=150, color="green", label="BandalgomCoffee", zorder=2),
    }

    # 1) 구조물 시각화
    for cat_id, style in category_styles.items():
        subset = df[df["category"] == cat_id]
        ax.scatter(subset["x"], subset["y"], **style)

    # 2) 건설 현장 시각화(가장 위에)
    if "ConstructionSite" in df.columns:
        const = df[df["ConstructionSite"] == 1]
        ax.scatter(
            const["x"],
            const["y"],
            marker="s",
            s=150,
            color="lightgray",
            label="Constructionsite",
            zorder=3,
        )

    # 범례
    ax.legend(loc="lower right")

    # 축 레이블 및 타이틀
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title("Local map")

    # 이미지 저장
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"{output_file} 저장 완료")


if __name__ == "__main__":
    draw_map()
