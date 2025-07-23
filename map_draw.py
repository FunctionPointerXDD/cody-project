import pandas as pd
import matplotlib.pyplot as plt


def draw_map(input_file='dataFile/mas_map.csv', output_file='img/map.png'):
    # 데이터 로드
    df = pd.read_csv(input_file)
    df.columns = df.columns.str.strip()
    if 'category' in df.columns:
        df['category'] = df['category'].astype(str).str.strip()

    # 좌표 범위 설정
    x_min, x_max = int(df['x'].min()), int(df['x'].max())
    y_min, y_max = int(df['y'].min()), int(df['y'].max())

    # 플롯 설정
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(x_min - 0.5, x_max + 0.5)
    ax.set_ylim(y_min - 0.5, y_max + 0.5)
    ax.invert_yaxis()
    ax.set_xticks(range(x_min, x_max + 1))
    ax.set_yticks(range(y_min, y_max + 1))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_aspect('equal')

    # 구조물 스타일 정의
    category_styles = {
        'Apartment': {
            'marker': 'o',
            's': 100,
            'color': 'brown',
            'label': 'Apartment',
            'zorder': 3,
        },
        'Building': {
            'marker': 'o',
            's': 100,
            'color': 'brown',
            'label': 'Building',
            'zorder': 3,
        },
        'BandalgomCoffee': {
            'marker': 's',
            's': 150,
            'color': 'green',
            'label': 'BandalgomCoffee',
            'zorder': 4,
        },
        'MyHome': {
            'marker': '^',
            's': 150,
            'color': 'green',
            'label': 'MyHome',
            'zorder': 5,
        },
    }

    # 1) 구조물 시각화
    for cat_id, style in category_styles.items():
        subset = df[df['category'] == cat_id]
        if not subset.empty:
            ax.scatter(subset['x'], subset['y'], **style)

    # 2) 건설 현장 시각화(가장 위에)
    if 'ConstructionSite' in df.columns:
        const = df[df['ConstructionSite'] == 1]
        if not const.empty:
            ax.scatter(
                const['x'],
                const['y'],
                marker='s',
                s=150,
                color='lightgray',
                label='Constructionsite',
                zorder=6,
            )

    # 범례: 플롯 영역 밖 오른쪽에 배치
    ax.legend(loc='lower right')

    # 축 레이블 및 타이틀
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Local map')

    # 이미지 저장
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f'{output_file} 저장 완료')


def main():
    try:
        draw_map()
    except FileNotFoundError as e:
        print(f'파일이 없습니다.{e.filename}')
    except PermissionError as e:
        print(f'파일 권한이 없습니다.{e.filename}')


if __name__ == '__main__':
    main()
