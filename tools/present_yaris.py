"""
小峰播報：Toyota Yaris Cross 完整介紹
從 full_present.py 衍生，僅替換 SLIDES 與輸出檔名
"""
import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from full_present import generate_all_audio, build_html

# === Yaris Cross 簡報內容 ===
# 各頁對應的小峰角色圖（相對 slides/，去背版）
CAT_IMG = {
    "intro": "xiaofeng_car_intro_20260427_184045_nobg.png",
    "levels": "xiaofeng_car_levels_20260427_184124_nobg.png",
    "engine": "xiaofeng_car_engine_20260427_184214_nobg.png",
    "parking": "xiaofeng_car_parking_20260427_184307_nobg.png",
    "safety": "xiaofeng_car_safety_20260427_184348_nobg.png",
    "advice": "xiaofeng_car_advice_20260427_184414_nobg.png",
    "ending": "xiaofeng_car_ending_20260427_184449_nobg.png",
}

SLIDES = [
    {
        "type": "intro",
        "title": "Toyota Yaris Cross",
        "subtitle": "2026 購車比較完整解析",
        "cat_image": CAT_IMG["intro"],
        "narration": "乘峰老師你好，今天我們來看 2026 年 Toyota Yaris Cross。這是一台你研究過的小型跨界休旅，我把重點整理成五頁，幫你快速回顧。",
    },
    {
        "type": "topic",
        "label": "①",
        "section": "車型概覽",
        "title": "三個等級怎麼選",
        "subtitle": "Yaris Cross 在台灣常見三種配置",
        "cat_image": CAT_IMG["levels"],
        "bullets": [
            ("a", "入門型（Entry）：基本配備，預算優先選擇"),
            ("b", "中階型（Mid）：CP 值最高、最熱銷的版本"),
            ("c", "頂級型（Top）：完整 TSS 主動安全、皮椅內裝"),
        ],
        "example": "建議：如果預算允許，直上中階；要安全配備就選頂級",
        "narration": "Yaris Cross 在台灣常見三個等級。入門型滿足基本需求，中階型是 CP 值最高的選擇，也是最熱銷的版本。頂級型有完整的 TSS 主動安全系統和皮椅內裝。",
    },
    {
        "type": "topic",
        "label": "②",
        "section": "動力系統",
        "title": "1.5L 自然進氣動力",
        "subtitle": "和 Corolla Cross Hybrid 的關鍵差異",
        "cat_image": CAT_IMG["engine"],
        "bullets": [
            ("a", "Yaris Cross：1.5L NA 自然進氣引擎"),
            ("b", "Corolla Cross：1.8L 油電混合 Hybrid"),
            ("c", "差別：油耗、稅金、保養成本與起步加速感"),
        ],
        "example": "市區短距離通勤 → Yaris Cross 夠用；常跑長途 → Corolla Hybrid 較省",
        "narration": "Yaris Cross 用的是 1.5 升自然進氣引擎，相比 Corolla Cross 的 1.8 升油電混合，差別主要在油耗、稅金和保養成本。如果是市區短距離通勤，Yaris Cross 已經夠用。",
    },
    {
        "type": "topic",
        "label": "③",
        "section": "停車優勢",
        "title": "尺寸小，市區好停",
        "subtitle": "機械停車與路邊停車的關鍵指標",
        "cat_image": CAT_IMG["parking"],
        "bullets": [
            ("a", "車長約 4.18 米，比 Corolla Cross 短一截"),
            ("b", "車寬 1.77 米，台灣機械停車格通用"),
            ("c", "迴轉半徑小，狹窄巷弄轉向更靈活"),
        ],
        "example": "台北市區、機械車位、舊式公寓停車場 → Yaris Cross 更友善",
        "narration": "Yaris Cross 最大優勢是尺寸。車長 4.18 米，車寬 1.77 米，台灣多數機械停車格都能進。在台北市區或舊式公寓停車場，比 Corolla Cross 更靈活好停。",
    },
    {
        "type": "topic",
        "label": "④",
        "section": "安全配備",
        "title": "TSS 主動安全亮點",
        "subtitle": "Toyota Safety Sense 第三代",
        "cat_image": CAT_IMG["safety"],
        "bullets": [
            ("a", "PCS 預警式防護：自動緊急煞車含路口偵測"),
            ("b", "DRCC 動態雷達巡航：高速跟車不費力"),
            ("c", "LTA 車道循跡輔助：長途減輕疲勞"),
            ("d", "BSM 盲點偵測：變換車道更安心（部分等級）"),
        ],
        "example": "強烈建議至少選有完整 TSS 的等級",
        "narration": "在安全配備方面，Toyota TSS 第三代涵蓋自動煞車、雷達巡航、車道循跡、盲點偵測。我強烈建議老師至少選擇有完整 TSS 的等級，長途駕駛差別非常明顯。",
    },
    {
        "type": "topic",
        "label": "⑤",
        "section": "購買建議",
        "title": "誰適合買 Yaris Cross？",
        "subtitle": "三句話總結",
        "cat_image": CAT_IMG["advice"],
        "bullets": [
            ("a", "預算 80-100 萬，要新車且首選 SUV 造型"),
            ("b", "市區為主，停車空間有限的家庭"),
            ("c", "對油電不在意，重視保養便利與保值"),
        ],
        "example": "若年里程超過 2 萬公里、常跑高速 → 改看 Corolla Cross Hybrid",
        "narration": "總結一下，如果預算 80 到 100 萬，主要市區用、停車空間有限，又不特別在意油電混合，那 Yaris Cross 就是適合的選擇。但如果一年跑超過兩萬公里，可以考慮 Corolla Cross Hybrid。",
    },
    {
        "type": "ending",
        "title": "老師決定看哪台？",
        "subtitle": "需要試駕清單或殺價策略嗎？",
        "ending_image_override": CAT_IMG["ending"],
        "narration": "以上就是 Yaris Cross 的快速重點。乘峰老師，需要我幫你準備試駕清單，還是整理殺價的議價策略？我隨時待命。",
    },
]

import full_present
full_present.SLIDES = SLIDES


def apply_toyota_theme(html: str) -> str:
    """把淡藍主題換成 Toyota 紅藍深色主題"""
    # 先換網頁標題
    html = html.replace("<title>小峰自我介紹</title>", "<title>Yaris Cross 播報</title>")

    replacements = [
        # 整體背景（淡藍漸層 → 深炭黑）
        ("linear-gradient(135deg, #dbeeff 0%, #c8e8ff 50%, #d4eeff 100%)",
         "linear-gradient(135deg, #1a1d24 0%, #0d1117 50%, #1a1d24 100%)"),

        # 投影片白底 → 深石板
        ("background: white;\n    border-radius: 24px;\n    padding: 48px",
         "background: #1f2530;\n    border-radius: 24px;\n    padding: 48px"),

        # 左邊條（藍 → Toyota 紅）
        ("background: linear-gradient(180deg, #5ba8ff, #89c8ff);",
         "background: linear-gradient(180deg, #eb0a1e, #b00818);"),

        # Topic overlay（白霧 → 深霧）
        ("rgba(255,255,255,0.92) 0%,\n      rgba(240,250,255,0.85) 40%,\n      rgba(220,240,255,0.3) 70%,\n      rgba(200,232,255,0.05) 100%",
         "rgba(15,17,22,0.88) 0%,\n      rgba(20,28,40,0.78) 40%,\n      rgba(20,28,40,0.3) 70%,\n      rgba(20,28,40,0.0) 100%"),

        # Topic 標籤（藍 → Toyota 紅）
        ("color: #4090ee;\n    font-size: 18px;\n    font-weight: 700;\n    letter-spacing: 2px;\n    margin-bottom: 8px;\n  }",
         "color: #eb0a1e;\n    font-size: 18px;\n    font-weight: 700;\n    letter-spacing: 2px;\n    margin-bottom: 8px;\n  }"),

        # 主標題（深藍 → 暖白）
        ("color: #1a3a6e;\n    font-size: 60px;",
         "color: #f5f5f5;\n    font-size: 60px;"),
        ("text-shadow: 0 2px 12px rgba(255,255,255,0.5);",
         "text-shadow: 0 2px 16px rgba(235,10,30,0.3);"),

        # 副標題顏色
        ("color: #3a5577;\n    font-size: 18px;",
         "color: #b8c4d6;\n    font-size: 18px;"),

        # bullet 卡片（白 → 深石板半透明）
        ("background: rgba(255,255,255,0.85);\n    backdrop-filter: blur(10px);\n    border: 1px solid rgba(91,168,255,0.3);",
         "background: rgba(31,37,48,0.85);\n    backdrop-filter: blur(10px);\n    border: 1px solid rgba(235,10,30,0.25);"),

        ("box-shadow: 0 4px 16px rgba(91,168,255,0.1);",
         "box-shadow: 0 4px 16px rgba(0,0,0,0.4);"),

        # bullet 字標（藍 → 紅）
        ("color: #4090ee;\n    font-weight: 900;\n    font-size: 16px;",
         "color: #ff4d5c;\n    font-weight: 900;\n    font-size: 16px;"),

        # bullet 文字（深 → 淺）
        ("color: #2a4466;\n    font-weight: 500;",
         "color: #e8eef8;\n    font-weight: 500;"),

        # example 樣式（黃 → Toyota 藍）
        ("background: rgba(255,217,102,0.25);\n    border-color: rgba(240,180,60,0.4);",
         "background: rgba(0,48,135,0.35);\n    border-color: rgba(80,140,240,0.4);"),

        ("color: #d49020;\n    font-weight: 900;\n    flex-shrink: 0;\n    min-width: 24px;\n  }",
         "color: #6ba0ff;\n    font-weight: 900;\n    flex-shrink: 0;\n    min-width: 24px;\n  }"),

        ("color: #5a4010;\n    font-style: italic;",
         "color: #d8e4ff;\n    font-style: italic;"),

        # Intro 主標題（深藍 → 暖白）
        ("color: #1a3a6e;\n    font-size: 64px;",
         "color: #f5f5f5;\n    font-size: 64px;"),

        # Intro subtitle (淡藍 → Toyota 紅)
        ("color: #5ba8ff;\n    font-size: 16px;",
         "color: #eb0a1e;\n    font-size: 16px;"),

        # Tagline
        ("color: #5577aa;\n    font-size: 18px;",
         "color: #a8b8d0;\n    font-size: 18px;"),

        # 頭像框背景 (透明 — 因為圖已去背)
        ("background: linear-gradient(135deg, #eef6ff, #d8ecff);",
         "background: transparent;"),

        ("border: 3px solid rgba(91,168,255,0.3);",
         "border: none;"),

        ("box-shadow: 0 8px 32px rgba(91,168,255,0.2);",
         "box-shadow: 0 12px 40px rgba(235,10,30,0.25);"),

        # cat 圖在卡片內保持 contain（不裁切）
        (".cat-image img {\n    width: 100%; height: 100%;\n    object-fit: cover;\n  }",
         ".cat-image img {\n    width: 100%; height: 100%;\n    object-fit: contain;\n    filter: drop-shadow(0 8px 24px rgba(0,0,0,0.4));\n  }"),

        # 進度條
        ("background: linear-gradient(90deg, #5ba8ff, #89c8ff);",
         "background: linear-gradient(90deg, #eb0a1e, #ff6b78);"),

        # 控制按鈕
        ("background: linear-gradient(135deg, #5ba8ff, #4090ee);",
         "background: linear-gradient(135deg, #eb0a1e, #c00818);"),

        ("background: rgba(255,255,255,0.9);",
         "background: rgba(31,37,48,0.9);"),

        # 頁碼
        ("color: #88aacc;\n    font-size: 14px;",
         "color: #6b7a91;\n    font-size: 14px;"),

        # ending overlay
        ("rgba(20,40,80,0.85) 0%,\n      rgba(40,80,140,0.7) 100%",
         "rgba(0,0,0,0.85) 0%,\n      rgba(20,5,10,0.75) 100%"),

        ("color: #ffd966;\n    text-shadow: 0 4px 20px rgba(0,0,0,0.5);",
         "color: #eb0a1e;\n    text-shadow: 0 4px 20px rgba(235,10,30,0.5);"),

        # ending image 邊框
        ("border: 3px solid rgba(255,255,255,0.6);",
         "border: 3px solid rgba(235,10,30,0.5);"),

        ("box-shadow: 0 16px 48px rgba(91,168,255,0.35);",
         "box-shadow: 0 16px 48px rgba(235,10,30,0.4);"),

        # bullet 邊框（淡藍）
        ("border-bottom: 1px solid #e8f4ff;",
         "border-bottom: 1px solid #2a3040;"),
    ]

    for old, new in replacements:
        html = html.replace(old, new)
    return html


async def main():
    base = Path(__file__).parent.parent
    audio_dir = base / "slides" / "audio_yaris"
    image_path = base / "slides" / "xiaofeng_yuzu_20260427_125303.png"
    scene_path = base / "slides" / "yaris_bg_20260427_183851.png"

    print("[小峰] 正在生成 Yaris Cross 播報語音...")
    audio_paths = await generate_all_audio(SLIDES, str(audio_dir))

    # 把 audio 路徑轉成相對於 slides/ 的路徑
    rel_audio_paths = [os.path.join("audio_yaris", os.path.basename(p)) for p in audio_paths]

    print("[小峰] 正在生成簡報...")
    html = build_html(
        SLIDES,
        [str(base / "slides" / r) for r in rel_audio_paths],
        str(image_path) if image_path.exists() else None,
        str(scene_path) if scene_path.exists() else None,
    )

    # 套用 Toyota 深色主題
    html = apply_toyota_theme(html)

    output = base / "slides" / "yaris_presentation.html"
    with open(output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[小峰] 簡報已輸出：{output}")
    print(f"[小峰] 預覽網址：http://localhost:8766/yaris_presentation.html")


if __name__ == "__main__":
    asyncio.run(main())
