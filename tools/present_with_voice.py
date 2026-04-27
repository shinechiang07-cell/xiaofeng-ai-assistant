"""
小峰上台工具：簡報 + 語音 一次完成
用法：python tools/present_with_voice.py --title "標題" --content "內容" [--voice] [--image 圖片路徑]
"""
import argparse
import asyncio
import os
import sys

# 加入上層目錄到路徑
sys.path.insert(0, os.path.dirname(__file__))
from slide import present
from voice import speak


def xiaofeng_present(title: str, content: str, image_path: str = None,
                     theme: str = "dark", with_voice: bool = True):
    # 1. 開啟簡報
    present(title, content, image_path, theme)

    # 2. 語音播報
    if with_voice:
        voice_text = f"{title}。{content.replace('-', '').replace('•', '').replace(chr(10), '，')}"
        speak(voice_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="小峰上台：簡報 + 語音")
    parser.add_argument("--title", required=True)
    parser.add_argument("--content", required=True)
    parser.add_argument("--image", default=None)
    parser.add_argument("--theme", default="dark", choices=["dark", "light"])
    parser.add_argument("--no-voice", action="store_true", help="只顯示簡報，不語音")
    args = parser.parse_args()

    content = args.content.replace("\\n", "\n")
    xiaofeng_present(args.title, content, args.image, args.theme, not args.no_voice)
