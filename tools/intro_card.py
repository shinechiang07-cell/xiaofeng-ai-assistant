"""
小峰介紹卡生成工具
用法：python tools/intro_card.py [--image 圖片路徑] [--mission 今日任務]
"""
import argparse
import os
import webbrowser


def build_intro_card(
    name: str = "小峰",
    subtitle: str = "一隻住在 Claude Code 裡的灰虎斑貓",
    owner: str = "乘峰老師",
    image_path: str = None,
    persona: str = "圓圓胖胖的灰虎斑，額頭有神秘 M 字紋",
    personality: str = "好奇愛探索、撒嬌、偶爾賣萌翻肚",
    location: str = "Claude Code，隨乘峰老師穿梭各專案",
    mission: str = "陪老師備課、出題、播簡報、即時生圖",
    quote: str = "「老師說話，我來動手，順便把課變有趣。」",
) -> str:

    image_block = ""
    if image_path and os.path.exists(image_path):
        abs_path = os.path.abspath(image_path).replace("\\", "/")
        image_block = f'<img src="file:///{abs_path}" alt="{name}">'
    else:
        image_block = '<div class="cat-placeholder">🐱</div>'

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} 介紹卡</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;
    background: linear-gradient(135deg, #dbeeff 0%, #c8e8ff 50%, #d4eeff 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 20px;
  }}

  .slide {{
    width: 900px;
    min-height: 520px;
    background: white;
    border-radius: 24px;
    padding: 44px 52px 56px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 12px 48px rgba(80,150,255,0.18), 0 2px 8px rgba(0,0,0,0.06);
  }}

  /* 左上角裝飾色塊 */
  .slide::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 6px;
    height: 100%;
    background: linear-gradient(180deg, #5ba8ff, #89c8ff);
    border-radius: 24px 0 0 24px;
  }}

  /* 右下角裝飾圓 */
  .slide::after {{
    content: '';
    position: absolute;
    bottom: -60px; right: -60px;
    width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(91,168,255,0.12) 0%, transparent 70%);
    pointer-events: none;
  }}

  .header {{
    margin-bottom: 28px;
  }}

  .subtitle {{
    color: #5ba8ff;
    font-size: 14px;
    font-weight: 500;
    letter-spacing: 1.5px;
    margin-bottom: 6px;
  }}

  h1 {{
    color: #1a3a6e;
    font-size: 58px;
    font-weight: 900;
    letter-spacing: -1px;
    line-height: 1;
    position: relative;
    display: inline-block;
  }}

  /* 標題底線裝飾 */
  h1::after {{
    content: '';
    position: absolute;
    bottom: -4px; left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #5ba8ff, transparent);
    border-radius: 2px;
  }}

  .content {{
    display: flex;
    gap: 40px;
    align-items: flex-start;
    margin-top: 32px;
  }}

  .avatar-box {{
    flex-shrink: 0;
    width: 210px;
    height: 210px;
    background: linear-gradient(135deg, #eef6ff, #d8ecff);
    border-radius: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    border: 2px solid rgba(91,168,255,0.25);
    box-shadow: 0 4px 20px rgba(91,168,255,0.15);
  }}

  .avatar-box img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
  }}

  .cat-placeholder {{
    font-size: 96px;
  }}

  .info-list {{
    flex: 1;
  }}

  .info-row {{
    display: flex;
    align-items: flex-start;
    gap: 14px;
    padding: 11px 0;
    border-bottom: 1px solid #e8f4ff;
  }}

  .info-row:last-child {{
    border-bottom: none;
  }}

  .label {{
    background: linear-gradient(135deg, #5ba8ff, #4090ee);
    color: white;
    font-size: 12px;
    font-weight: 700;
    padding: 3px 10px;
    border-radius: 20px;
    min-width: 60px;
    text-align: center;
    letter-spacing: 0.5px;
    flex-shrink: 0;
    margin-top: 2px;
  }}

  .value {{
    color: #334466;
    font-size: 15.5px;
    line-height: 1.65;
    flex: 1;
    font-weight: 500;
  }}

  .quote {{
    position: absolute;
    bottom: 20px;
    left: 52px;
    right: 52px;
    color: #88aacc;
    font-size: 13px;
    font-style: italic;
    letter-spacing: 0.3px;
    padding-top: 12px;
    border-top: 1px solid #e0eefc;
  }}

  .badge {{
    position: absolute;
    top: 20px;
    right: 24px;
    background: linear-gradient(135deg, #5ba8ff22, #89c8ff22);
    border: 1px solid #5ba8ff44;
    color: #5ba8ff;
    font-size: 12px;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 20px;
    letter-spacing: 0.5px;
  }}
</style>
</head>
<body>
  <div class="slide">
    <div class="badge">🐱 AI 助教</div>

    <div class="header">
      <div class="subtitle">{subtitle}</div>
      <h1>我是{name}</h1>
    </div>

    <div class="content">
      <div class="avatar-box">
        {image_block}
      </div>

      <div class="info-list">
        <div class="info-row">
          <span class="label">主人</span>
          <span class="value">{owner}</span>
        </div>
        <div class="info-row">
          <span class="label">形象</span>
          <span class="value">{persona}</span>
        </div>
        <div class="info-row">
          <span class="label">個性</span>
          <span class="value">{personality}</span>
        </div>
        <div class="info-row">
          <span class="label">住所</span>
          <span class="value">{location}</span>
        </div>
        <div class="info-row">
          <span class="label">今日任務</span>
          <span class="value">{mission}</span>
        </div>
      </div>
    </div>

    <div class="quote">{quote}</div>
  </div>
</body>
</html>"""
    return html


def show_intro(image_path=None, output=None, **kwargs):
    html = build_intro_card(image_path=image_path, **kwargs)

    if output is None:
        slides_dir = os.path.join(os.path.dirname(__file__), "..", "slides")
        os.makedirs(slides_dir, exist_ok=True)
        output = os.path.join(slides_dir, "intro_card.html")

    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    abs_path = os.path.abspath(output).replace("\\", "/")
    webbrowser.open(f"file:///{abs_path}")
    print(f"[小峰] 介紹卡已開啟")
    return abs_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", default=None)
    parser.add_argument("--mission", default="陪老師備課、出題、播簡報、即時生圖")
    parser.add_argument("--owner", default="乘峰老師")
    args = parser.parse_args()

    image = args.image or os.path.join(
        os.path.dirname(__file__), "..", "slides", "xiaofeng_yuzu_20260427_125303.png"
    )

    show_intro(image_path=image, mission=args.mission, owner=args.owner)
