"""
小峰即時簡報工具
用法：python tools/slide.py --title "標題" --content "內容" [--image "圖片路徑"] [--theme dark|light]
"""
import argparse
import os
import webbrowser
import json
from datetime import datetime


THEMES = {
    "dark": {
        "bg": "#0f0f1a",
        "card": "rgba(255,255,255,0.05)",
        "title_color": "#f8c94a",
        "text_color": "#e8e8f0",
        "accent": "#7b68ee",
        "border": "rgba(123,104,238,0.3)",
    },
    "light": {
        "bg": "#f5f5f5",
        "card": "rgba(0,0,0,0.05)",
        "title_color": "#e65c00",
        "text_color": "#222233",
        "accent": "#4a90d9",
        "border": "rgba(74,144,217,0.3)",
    },
}


def build_html(title: str, content: str, image_path: str = None, theme: str = "dark") -> str:
    t = THEMES.get(theme, THEMES["dark"])

    # 把換行轉成 <br>，支援 bullet list
    lines = content.split("\n")
    content_html = ""
    for line in lines:
        line = line.strip()
        if line.startswith("- ") or line.startswith("• "):
            content_html += f'<li>{line[2:]}</li>'
        elif line:
            content_html += f'<p>{line}</p>'

    if "<li>" in content_html:
        content_html = f"<ul>{content_html}</ul>"

    image_block = ""
    if image_path and os.path.exists(image_path):
        abs_path = os.path.abspath(image_path).replace("\\", "/")
        image_block = f'<img src="file:///{abs_path}" alt="插圖" style="max-width:480px; max-height:300px; border-radius:12px; margin:16px auto; display:block; box-shadow: 0 8px 32px rgba(0,0,0,0.4);">'

    timestamp = datetime.now().strftime("%H:%M")

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>小峰 — {title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Microsoft JhengHei', 'Noto Sans TC', sans-serif;
    background: {t['bg']};
    color: {t['text_color']};
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 40px 20px;
  }}
  .card {{
    background: {t['card']};
    border: 1px solid {t['border']};
    border-radius: 20px;
    padding: 48px 56px;
    max-width: 860px;
    width: 100%;
    backdrop-filter: blur(12px);
    box-shadow: 0 16px 64px rgba(0,0,0,0.3);
    animation: fadeIn 0.6s ease;
  }}
  @keyframes fadeIn {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}
  .badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: {t['accent']};
    color: white;
    font-size: 13px;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    margin-bottom: 20px;
    letter-spacing: 0.5px;
  }}
  h1 {{
    color: {t['title_color']};
    font-size: clamp(28px, 4vw, 42px);
    font-weight: 800;
    line-height: 1.2;
    margin-bottom: 28px;
    letter-spacing: -0.5px;
  }}
  .content {{
    font-size: clamp(16px, 2vw, 20px);
    line-height: 1.9;
    color: {t['text_color']};
  }}
  .content ul {{
    list-style: none;
    padding: 0;
  }}
  .content li {{
    padding: 8px 0 8px 28px;
    position: relative;
    border-bottom: 1px solid {t['border']};
  }}
  .content li:last-child {{ border-bottom: none; }}
  .content li::before {{
    content: '🦊';
    position: absolute;
    left: 0;
    font-size: 16px;
  }}
  .content p {{ margin-bottom: 12px; }}
  .footer {{
    margin-top: 32px;
    font-size: 13px;
    color: {t['accent']};
    opacity: 0.7;
    text-align: right;
  }}
</style>
</head>
<body>
  <div class="card">
    <div class="badge">🦊 小峰助教 · {timestamp}</div>
    <h1>{title}</h1>
    {image_block}
    <div class="content">{content_html}</div>
    <div class="footer">由 小峰 生成 · Claude Code</div>
  </div>
</body>
</html>"""
    return html


def present(title: str, content: str, image_path: str = None, theme: str = "dark", output: str = None):
    html = build_html(title, content, image_path, theme)

    if output is None:
        slides_dir = os.path.join(os.path.dirname(__file__), "..", "slides")
        os.makedirs(slides_dir, exist_ok=True)
        output = os.path.join(slides_dir, "current_slide.html")

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    abs_output = os.path.abspath(output)
    webbrowser.open(f"file:///{abs_output.replace(chr(92), '/')}")
    print(f"[小峰] 簡報已開啟：{abs_output}")
    return abs_output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="小峰即時簡報工具")
    parser.add_argument("--title", required=True, help="投影片標題")
    parser.add_argument("--content", required=True, help="投影片內容（用\\n換行，-開頭表示項目）")
    parser.add_argument("--image", default=None, help="圖片路徑（可選）")
    parser.add_argument("--theme", default="dark", choices=["dark", "light"], help="主題")
    parser.add_argument("--output", default=None, help="輸出 HTML 路徑")
    args = parser.parse_args()

    content = args.content.replace("\\n", "\n")
    present(args.title, content, args.image, args.theme, args.output)
