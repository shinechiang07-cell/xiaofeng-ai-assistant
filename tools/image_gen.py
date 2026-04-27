"""
小峰圖片生成工具（使用 OpenAI GPT-Image）
用法：python tools/image_gen.py "圖片描述" [--output 輸出路徑]
需要：OPENAI_API_KEY 環境變數
"""
import sys
import os
import argparse
import requests


def generate_image(prompt: str, output_path: str = "slides/generated.png") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[小峰] 找不到 OPENAI_API_KEY，請設定環境變數")
        print("  在終端機執行：set OPENAI_API_KEY=你的金鑰")
        sys.exit(1)

    try:
        from openai import OpenAI
    except ImportError:
        print("[小峰] openai 未安裝，執行：pip install openai")
        sys.exit(1)

    print(f"[小峰] 正在生成圖片：{prompt[:50]}...")

    client = OpenAI(api_key=api_key)
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img_data = requests.get(image_url, timeout=30).content
    with open(output_path, "wb") as f:
        f.write(img_data)

    print(f"[小峰] 圖片已儲存：{os.path.abspath(output_path)}")
    return os.path.abspath(output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="小峰圖片生成工具")
    parser.add_argument("prompt", help="圖片描述（英文效果更好）")
    parser.add_argument("--output", default="slides/generated.png", help="輸出路徑")
    args = parser.parse_args()
    generate_image(args.prompt, args.output)
