"""
小峰完整簡報秀：多頁投影片 + 同步語音
語音播完自動換頁，全程自動播放
用法：python tools/full_present.py
"""
import asyncio
import os
import sys
import webbrowser
from pathlib import Path

# 簡報內容 ----------------------------------------------------------
SLIDES = [
    {
        "type": "intro",
        "title": "我是小峰",
        "subtitle": "一隻住在 Claude Code 裡的灰虎斑貓",
        "narration": "大家好，我是小峰，是乘峰老師的 AI 助教。我是一隻灰色虎斑貓，住在 Claude Code 裡面。今天讓我來介紹一下我自己。",
    },
    {
        "type": "topic",
        "label": "①",
        "section": "技能",
        "title": "我能做的事",
        "subtitle": "我不只是聊天 AI，我會動手做事。",
        "bullets": [
            ("a", "備課與出題：整理教材、生成試卷情境題"),
            ("b", "即時生圖：用 AI 畫出教學插圖、卡牌素材"),
            ("c", "語音 + 簡報：邊說話邊播動態 HTML 簡報"),
        ],
        "example": "「幫我準備明天五年級數學的隨堂測驗」",
        "narration": "我能做的事情有三類。第一，備課與出題；第二，即時生成教學圖片；第三，像現在這樣，邊說話邊播放簡報給大家看。",
    },
    {
        "type": "topic",
        "label": "②",
        "section": "個性",
        "title": "我的人格設定",
        "subtitle": "不只是工具，我有自己的個性。",
        "bullets": [
            ("a", "形象：圓圓胖胖的灰虎斑，額頭有 M 字紋"),
            ("b", "個性：好奇愛探索、撒嬌、賣萌翻肚"),
            ("c", "聲音：男生溫暖嗓音"),
        ],
        "example": "「老師說話，我來動手，順便把課變有趣。」",
        "narration": "我有自己的個性。我是一隻圓圓胖胖的灰虎斑貓，個性活潑、愛撒嬌。我說話是男生的聲音，希望讓老師上課變得更有趣。",
    },
    {
        "type": "topic",
        "label": "③",
        "section": "架構",
        "title": "我的技術組成",
        "subtitle": "用最強的 AI 工具組起來。",
        "bullets": [
            ("a", "大腦：Claude Code（Sonnet 4.6 模型）"),
            ("b", "語音：Edge-TTS 男聲合成"),
            ("c", "生圖：GPT-Image-2"),
            ("d", "簡報：HTML + CSS 動態生成"),
        ],
        "example": "Skill 模組化設計，可以隨時擴充新能力",
        "narration": "我的大腦是 Claude Code，使用 Sonnet 4.6 模型。語音用 Edge-TTS，圖片用 GPT Image 2。所有的能力都用 Skill 模組設計，可以隨時擴充。",
    },
    {
        "type": "ending",
        "title": "我們開始吧！",
        "subtitle": "今天有什麼需要幫忙的嗎？",
        "narration": "以上就是我的自我介紹。乘峰老師，今天有什麼需要我幫忙的嗎？我隨時待命。",
    },
]


async def generate_audio(text: str, output_path: str, voice: str = "zh-TW-YunJheNeural"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice=voice, rate="+0%")
    await communicate.save(output_path)


async def generate_all_audio(slides, audio_dir):
    os.makedirs(audio_dir, exist_ok=True)
    paths = []
    for i, slide in enumerate(slides):
        path = os.path.join(audio_dir, f"slide_{i}.mp3")
        await generate_audio(slide["narration"], path)
        paths.append(path)
        print(f"[小峰] 語音 {i+1}/{len(slides)} 已生成")
    return paths


def render_slide(slide, idx, total, image_path=None, scene_path=None):
    bg_style = ""
    if scene_path and os.path.exists(scene_path):
        rel_scene = os.path.basename(scene_path)
        bg_style = f'style="background-image: url({rel_scene});"'

    if slide["type"] == "intro":
        image_block = ""
        if image_path and os.path.exists(image_path):
            rel_img = os.path.basename(image_path)
            image_block = f'<div class="cat-image"><img src="{rel_img}" alt="小峰"></div>'

        return f"""
        <div class="slide intro-slide">
          <div class="hero">
            {image_block}
            <div class="hero-text">
              <div class="subtitle">{slide['subtitle']}</div>
              <h1>{slide['title']}</h1>
              <div class="tagline">「老師說話，我來動手，順便把課變有趣。」</div>
            </div>
          </div>
          <div class="page-num">{idx+1} / {total}</div>
        </div>
        """

    elif slide["type"] == "ending":
        ending_image = "xiaofeng_ending_20260427_132940.png"
        return f"""
        <div class="slide ending-slide" {bg_style}>
          <div class="ending-overlay"></div>
          <div class="ending-content">
            <div class="ending-image"><img src="{ending_image}" alt="小峰"></div>
            <h1>{slide['title']}</h1>
            <div class="subtitle">{slide['subtitle']}</div>
          </div>
          <div class="page-num">{idx+1} / {total}</div>
        </div>
        """

    elif slide["type"] == "topic":
        bullets_html = ""
        for letter, text in slide["bullets"]:
            bullets_html += f'''
            <div class="topic-bullet">
              <span class="bullet-tag">({letter})</span>
              <span class="bullet-text">{text}</span>
            </div>
            '''

        example_html = ""
        if slide.get("example"):
            example_html = f'''
            <div class="topic-example">
              <span class="example-tag">例</span>
              <span class="example-text">{slide['example']}</span>
            </div>
            '''

        return f"""
        <div class="slide topic-slide" {bg_style}>
          <div class="topic-overlay"></div>
          <div class="topic-content">
            <div class="topic-label">{slide['section']} {slide['label']}</div>
            <h1 class="topic-title">{slide['title']}</h1>
            <div class="topic-subtitle">{slide['subtitle']}</div>
            <div class="topic-bullets">
              {bullets_html}
              {example_html}
            </div>
          </div>
          <div class="page-num">{idx+1} / {total}</div>
        </div>
        """

    else:
        bullets = "".join(f'<li>{b}</li>' for b in slide.get("bullets", []))
        return f"""
        <div class="slide content-slide">
          <h2>{slide['title']}</h2>
          <ul class="bullets">{bullets}</ul>
          <div class="page-num">{idx+1} / {total}</div>
        </div>
        """


def build_html(slides, audio_paths, image_path=None, scene_path=None):
    slides_html = ""
    for i, slide in enumerate(slides):
        slides_html += render_slide(slide, i, len(slides), image_path, scene_path)

    audio_tags = ""
    for i, path in enumerate(audio_paths):
        # 相對路徑：audio/slide_N.mp3
        rel_audio = "audio/" + os.path.basename(path)
        audio_tags += f'<audio id="audio-{i}" src="{rel_audio}" preload="auto"></audio>\n'

    html = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>小峰自我介紹</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}

  body {{
    font-family: 'Noto Sans TC', 'Microsoft JhengHei', sans-serif;
    background: linear-gradient(135deg, #dbeeff 0%, #c8e8ff 50%, #d4eeff 100%);
    min-height: 100vh;
    overflow: hidden;
  }}

  .container {{
    width: 100vw;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }}

  .slide-wrapper {{
    width: 100%;
    max-width: 960px;
    height: 90vh;
    max-height: 600px;
    position: relative;
  }}

  .slide {{
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: white;
    border-radius: 24px;
    padding: 48px 56px;
    box-shadow: 0 16px 64px rgba(80,150,255,0.2);
    opacity: 0;
    transform: translateX(40px);
    transition: opacity 0.6s ease, transform 0.6s ease;
    pointer-events: none;
    overflow: hidden;
  }}

  .slide.active {{
    opacity: 1;
    transform: translateX(0);
    pointer-events: auto;
  }}

  .slide::before {{
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 6px; height: 100%;
    background: linear-gradient(180deg, #5ba8ff, #89c8ff);
    border-radius: 24px 0 0 24px;
  }}

  /* Intro slide */
  .intro-slide .hero {{
    display: flex;
    align-items: center;
    gap: 48px;
    height: 100%;
  }}

  .cat-image {{
    flex-shrink: 0;
    width: 280px;
    height: 280px;
    background: linear-gradient(135deg, #eef6ff, #d8ecff);
    border-radius: 24px;
    overflow: hidden;
    border: 3px solid rgba(91,168,255,0.3);
    box-shadow: 0 8px 32px rgba(91,168,255,0.2);
  }}

  .cat-image img {{
    width: 100%; height: 100%;
    object-fit: cover;
  }}

  .subtitle {{
    color: #5ba8ff;
    font-size: 16px;
    font-weight: 500;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
  }}

  h1 {{
    color: #1a3a6e;
    font-size: 64px;
    font-weight: 900;
    line-height: 1;
    margin-bottom: 24px;
  }}

  .tagline {{
    color: #5577aa;
    font-size: 18px;
    font-style: italic;
    line-height: 1.6;
  }}

  /* Topic slide (主題頁，仿三師爸版型但淡藍系) */
  .topic-slide {{
    background-size: cover;
    background-position: right center;
    background-repeat: no-repeat;
    padding: 0;
    color: white;
  }}

  .topic-overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg,
      rgba(255,255,255,0.92) 0%,
      rgba(240,250,255,0.85) 40%,
      rgba(220,240,255,0.3) 70%,
      rgba(200,232,255,0.05) 100%);
    border-radius: 24px;
  }}

  .topic-content {{
    position: relative;
    z-index: 2;
    padding: 56px 60px;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    max-width: 60%;
  }}

  .topic-label {{
    color: #4090ee;
    font-size: 18px;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 8px;
  }}

  .topic-title {{
    color: #1a3a6e;
    font-size: 60px;
    font-weight: 900;
    line-height: 1.05;
    margin-bottom: 16px;
    letter-spacing: -1px;
    text-shadow: 0 2px 12px rgba(255,255,255,0.5);
  }}

  .topic-subtitle {{
    color: #3a5577;
    font-size: 18px;
    line-height: 1.6;
    margin-bottom: 28px;
    font-weight: 500;
  }}

  .topic-bullets {{
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .topic-bullet, .topic-example {{
    display: flex;
    align-items: flex-start;
    gap: 12px;
    background: rgba(255,255,255,0.85);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(91,168,255,0.3);
    padding: 12px 18px;
    border-radius: 10px;
    font-size: 16px;
    line-height: 1.5;
    opacity: 0;
    transform: translateX(-20px);
    animation: bulletIn 0.5s ease forwards;
    box-shadow: 0 4px 16px rgba(91,168,255,0.1);
  }}

  .slide.active .topic-bullet:nth-child(1) {{ animation-delay: 0.4s; }}
  .slide.active .topic-bullet:nth-child(2) {{ animation-delay: 0.7s; }}
  .slide.active .topic-bullet:nth-child(3) {{ animation-delay: 1.0s; }}
  .slide.active .topic-bullet:nth-child(4) {{ animation-delay: 1.3s; }}
  .slide.active .topic-example {{ animation-delay: 1.6s; }}

  @keyframes bulletIn {{
    to {{ opacity: 1; transform: translateX(0); }}
  }}

  .bullet-tag {{
    color: #4090ee;
    font-weight: 900;
    font-size: 16px;
    flex-shrink: 0;
    min-width: 24px;
  }}

  .bullet-text {{
    color: #2a4466;
    font-weight: 500;
  }}

  .topic-example {{
    background: rgba(255,217,102,0.25);
    border-color: rgba(240,180,60,0.4);
    margin-top: 6px;
  }}

  .example-tag {{
    color: #d49020;
    font-weight: 900;
    flex-shrink: 0;
    min-width: 24px;
  }}

  .example-text {{
    color: #5a4010;
    font-style: italic;
  }}

  /* Ending slide background */
  .ending-slide {{
    background-size: cover;
    background-position: center;
  }}

  .ending-overlay {{
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg,
      rgba(20,40,80,0.85) 0%,
      rgba(40,80,140,0.7) 100%);
    border-radius: 24px;
  }}

  .ending-slide .ending-content {{
    position: relative;
    z-index: 2;
  }}

  .ending-slide h1 {{
    color: #ffd966;
    text-shadow: 0 4px 20px rgba(0,0,0,0.5);
  }}

  .ending-slide .subtitle {{
    color: rgba(255,255,255,0.9);
    text-shadow: 0 2px 8px rgba(0,0,0,0.4);
  }}

  /* Content slide */
  .content-slide h2 {{
    color: #1a3a6e;
    font-size: 44px;
    font-weight: 900;
    margin-bottom: 32px;
    padding-bottom: 16px;
    border-bottom: 3px solid #5ba8ff;
    display: inline-block;
  }}

  .bullets {{
    list-style: none;
    padding: 0;
  }}

  .bullets li {{
    color: #334466;
    font-size: 22px;
    line-height: 1.8;
    padding: 14px 20px;
    margin-bottom: 12px;
    background: linear-gradient(90deg, #f0f8ff, transparent);
    border-left: 4px solid #5ba8ff;
    border-radius: 8px;
    font-weight: 500;
    opacity: 0;
    transform: translateX(-20px);
    animation: slideIn 0.5s ease forwards;
  }}

  .slide.active .bullets li:nth-child(1) {{ animation-delay: 0.3s; }}
  .slide.active .bullets li:nth-child(2) {{ animation-delay: 0.7s; }}
  .slide.active .bullets li:nth-child(3) {{ animation-delay: 1.1s; }}
  .slide.active .bullets li:nth-child(4) {{ animation-delay: 1.5s; }}
  .slide.active .bullets li:nth-child(5) {{ animation-delay: 1.9s; }}

  @keyframes slideIn {{
    to {{ opacity: 1; transform: translateX(0); }}
  }}

  /* Ending slide */
  .ending-slide {{
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
  }}

  .ending-image {{
    width: 280px;
    height: 280px;
    margin: 0 auto 24px;
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 16px 48px rgba(91,168,255,0.35);
    border: 3px solid rgba(255,255,255,0.6);
    animation: floatUp 3s ease-in-out infinite;
  }}

  .ending-image img {{
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }}

  @keyframes floatUp {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-10px); }}
  }}

  .ending-slide h1 {{
    font-size: 72px;
    margin-bottom: 16px;
  }}

  .ending-slide .subtitle {{
    font-size: 24px;
    color: #5577aa;
  }}

  /* Page number */
  .page-num {{
    position: absolute;
    bottom: 20px;
    right: 32px;
    color: #88aacc;
    font-size: 14px;
    font-weight: 500;
  }}

  /* Controls */
  .controls {{
    position: fixed;
    bottom: 20px;
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    gap: 12px;
    background: rgba(255,255,255,0.9);
    padding: 8px 16px;
    border-radius: 30px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    backdrop-filter: blur(10px);
    z-index: 100;
  }}

  .controls button {{
    background: linear-gradient(135deg, #5ba8ff, #4090ee);
    color: white;
    border: none;
    padding: 8px 18px;
    border-radius: 20px;
    cursor: pointer;
    font-weight: 700;
    font-size: 14px;
    font-family: inherit;
  }}

  .controls button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(91,168,255,0.4);
  }}

  .controls button:disabled {{
    opacity: 0.4;
    cursor: not-allowed;
  }}

  .progress {{
    position: fixed;
    top: 0; left: 0;
    height: 4px;
    background: linear-gradient(90deg, #5ba8ff, #89c8ff);
    z-index: 200;
    transition: width 0.3s ease;
    width: 0%;
  }}

  .start-overlay {{
    position: fixed;
    inset: 0;
    background: rgba(219,238,255,0.95);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    cursor: pointer;
  }}

  .start-overlay .start-card {{
    background: white;
    padding: 48px 64px;
    border-radius: 24px;
    text-align: center;
    box-shadow: 0 16px 64px rgba(80,150,255,0.3);
  }}

  .start-overlay .start-card h2 {{
    color: #1a3a6e;
    font-size: 32px;
    margin-bottom: 16px;
  }}

  .start-overlay .start-card p {{
    color: #5577aa;
    font-size: 16px;
    margin-bottom: 24px;
  }}

  .start-overlay .start-btn {{
    background: linear-gradient(135deg, #5ba8ff, #4090ee);
    color: white;
    border: none;
    padding: 14px 36px;
    border-radius: 30px;
    font-size: 18px;
    font-weight: 700;
    cursor: pointer;
    font-family: inherit;
    box-shadow: 0 4px 20px rgba(91,168,255,0.4);
  }}
</style>
</head>
<body>
  <div class="progress" id="progress"></div>

  <div class="container">
    <div class="slide-wrapper">
      {slides_html}
    </div>
  </div>

  <div class="controls">
    <button id="prevBtn" onclick="prevSlide()">◀ 上一頁</button>
    <button id="playBtn" onclick="togglePlay()">⏸ 暫停</button>
    <button id="nextBtn" onclick="nextSlide()">下一頁 ▶</button>
  </div>

  {audio_tags}

  <script>
    const slides = document.querySelectorAll('.slide');
    const total = slides.length;
    let current = 0;
    let isPlaying = true;
    let currentAudio = null;

    function showSlide(idx) {{
      slides.forEach((s, i) => {{
        s.classList.toggle('active', i === idx);
      }});
      document.getElementById('progress').style.width = ((idx + 1) / total * 100) + '%';
    }}

    function playAudio(idx) {{
      if (currentAudio) {{
        currentAudio.pause();
        currentAudio.currentTime = 0;
      }}
      const audio = document.getElementById('audio-' + idx);
      if (!audio) return;
      currentAudio = audio;
      audio.currentTime = 0;
      audio.play().catch(e => console.log('播放失敗:', e));

      audio.onended = () => {{
        if (isPlaying && current < total - 1) {{
          setTimeout(() => nextSlide(), 800);
        }}
      }};
    }}

    function nextSlide() {{
      if (current < total - 1) {{
        current++;
        showSlide(current);
        if (isPlaying) playAudio(current);
      }}
    }}

    function prevSlide() {{
      if (current > 0) {{
        current--;
        showSlide(current);
        if (isPlaying) playAudio(current);
      }}
    }}

    function togglePlay() {{
      isPlaying = !isPlaying;
      const btn = document.getElementById('playBtn');
      if (isPlaying) {{
        btn.textContent = '⏸ 暫停';
        if (currentAudio) currentAudio.play();
      }} else {{
        btn.textContent = '▶ 播放';
        if (currentAudio) currentAudio.pause();
      }}
    }}

    // 鍵盤控制
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ') {{ e.preventDefault(); nextSlide(); }}
      if (e.key === 'ArrowLeft') prevSlide();
      if (e.key === 'p') togglePlay();
    }});

    // 初始顯示第一頁，立刻嘗試自動播放
    showSlide(0);
    let started = false;
    function tryAutoStart() {{
      if (started) return;
      started = true;
      playAudio(0);
    }}

    // 嘗試立刻播放（成功則完成；失敗則等使用者第一次互動）
    window.addEventListener('load', () => {{
      const audio = document.getElementById('audio-0');
      if (audio) {{
        const promise = audio.play();
        if (promise !== undefined) {{
          promise.then(() => {{ started = true; audio.onended = () => {{ if (isPlaying && current < total - 1) setTimeout(() => nextSlide(), 800); }}; }})
                 .catch(() => {{
                   // 自動播放被擋下，等任何點擊或按鍵
                   document.addEventListener('click', tryAutoStart, {{ once: true }});
                   document.addEventListener('keydown', tryAutoStart, {{ once: true }});
                 }});
        }}
      }}
    }});
  </script>
</body>
</html>"""
    return html


async def main():
    base = Path(__file__).parent.parent
    audio_dir = base / "slides" / "audio"
    image_path = base / "slides" / "xiaofeng_yuzu_20260427_125303.png"
    scene_path = base / "slides" / "xiaofeng_clean_bg_20260427_130637.png"

    print("[小峰] 正在生成語音檔...")
    audio_paths = await generate_all_audio(SLIDES, str(audio_dir))

    print("[小峰] 正在生成簡報...")
    html = build_html(
        SLIDES, audio_paths,
        str(image_path) if image_path.exists() else None,
        str(scene_path) if scene_path.exists() else None,
    )

    output = base / "slides" / "full_presentation.html"
    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    abs_path = str(output.absolute()).replace("\\", "/")
    webbrowser.open(f"file:///{abs_path}")
    print(f"[小峰] 簡報已開啟：{abs_path}")
    print("[小峰] 請點擊網頁上的「開始播放」按鈕")


if __name__ == "__main__":
    asyncio.run(main())
