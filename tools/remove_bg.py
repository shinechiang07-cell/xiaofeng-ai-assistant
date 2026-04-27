"""
批次去背工具：把指定資料夾內所有 PNG 去背
用法：python tools/remove_bg.py [pattern]
預設處理 slides/xiaofeng_car_*.png
"""
import sys
import os
from pathlib import Path
from rembg import remove, new_session


def main():
    base = Path(__file__).parent.parent / "slides"
    pattern = sys.argv[1] if len(sys.argv) > 1 else "xiaofeng_car_*.png"

    # 用 isnet-anime 模型對卡通/插畫效果最好
    session = new_session("isnet-anime")

    files = list(base.glob(pattern))
    if not files:
        print(f"[小峰] 找不到符合 {pattern} 的檔案")
        return

    for f in files:
        # 跳過已經去背的檔案
        if "_nobg" in f.name:
            continue
        out = f.parent / (f.stem + "_nobg.png")
        if out.exists():
            print(f"[小峰] 已存在跳過：{out.name}")
            continue
        with open(f, "rb") as inp:
            data = inp.read()
        result = remove(data, session=session)
        with open(out, "wb") as outp:
            outp.write(result)
        print(f"[小峰] 去背完成：{out.name}")


if __name__ == "__main__":
    main()
