"""
批次去背工具：強力版（rembg + 白邊清除）
用法：python tools/remove_bg.py [pattern]
預設處理 slides/xiaofeng_car_*.png（排除已去背檔）
"""
import sys
import os
from pathlib import Path
from rembg import remove, new_session
from PIL import Image
import numpy as np


def post_process(img: Image.Image, white_threshold: int = 235, alpha_threshold: int = 30) -> Image.Image:
    """把接近白色的殘留像素也設成透明，並清除 alpha 邊緣鋸齒"""
    arr = np.array(img.convert("RGBA"))
    r, g, b, a = arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3]

    # 1. 接近白色 + alpha 較低 → 直接設為透明
    near_white = (r >= white_threshold) & (g >= white_threshold) & (b >= white_threshold)
    low_alpha = a < 200
    arr[near_white & low_alpha, 3] = 0

    # 2. 半透明邊緣（alpha < 30）→ 完全透明（清掉光暈）
    arr[a < alpha_threshold, 3] = 0

    return Image.fromarray(arr, mode="RGBA")


def main():
    base = Path(__file__).parent.parent / "slides"
    pattern = sys.argv[1] if len(sys.argv) > 1 else "xiaofeng_car_*.png"
    model = sys.argv[2] if len(sys.argv) > 2 else "isnet-anime"

    print(f"[小峰] 使用模型：{model}")
    session = new_session(model)

    files = [f for f in base.glob(pattern) if "_nobg" not in f.name]
    if not files:
        print(f"[小峰] 找不到符合 {pattern} 的檔案（且未去背）")
        return

    for f in files:
        out = f.parent / (f.stem + "_nobg.png")
        with open(f, "rb") as inp:
            data = inp.read()
        result_bytes = remove(data, session=session)

        # 後處理：清白邊
        from io import BytesIO
        img = Image.open(BytesIO(result_bytes))
        img = post_process(img)
        img.save(out, "PNG")
        print(f"[小峰] 去背 + 清白邊完成：{out.name}")


if __name__ == "__main__":
    main()
