import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. 画像を読み込む（ススキではなく、成功した琵琶湖の画像にします）
img = cv2.imread("img/biwako.jpg")

if img is None:
    print("画像が読み込めません。ファイル名を確認してください。")
    exit()

# 2. 白黒画像にする
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 3. 輪郭を見つける（エッジ検出）
edges = cv2.Canny(gray, 30, 100)

# 4. 直線を見つける（ハフ変換）
# 琵琶湖で成功した設定値です
lines = cv2.HoughLinesP(
    edges,
    rho=1,
    theta=np.pi / 180,
    threshold=180,      # 直線とみなす厳しさ
    minLineLength=500,  # 200ピクセル以上の長さが必要
    maxLineGap=50       # 多少途切れていてもつなぐ
)

# 一番良い線を選ぶための準備
best_line = None
max_length = 0

if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]

        # 角度を計算
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

        # 水平に近い線だけを選ぶ（傾きが ±10度以内）
        if abs(angle) < 10:
            # 長さを計算
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            # 今までで一番長い線なら、それを採用する
            if length > max_length:
                max_length = length
                best_line = (x1, y1, x2, y2)

# 結果を表示する
result_img = img.copy()

if best_line is not None:
    # 緑色の線を引く
    x1, y1, x2, y2 = best_line
    cv2.line(result_img, (x1, y1), (x2, y2), (0, 255, 0), 5)

    # 角度を再計算して表示
    final_angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    print(f"地平線の傾き: {final_angle:.2f}°")
    
    # 簡易スコア（0に近いほど高得点）
    score = max(0, 100 - abs(final_angle) * 10)
    print(f"構図スコア: {int(score)}点")
else:
    print("地平線が見つかりませんでした")

# 画像を表示
plt.imshow(cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB))
plt.axis("off")
plt.show()