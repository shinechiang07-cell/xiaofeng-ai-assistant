# 小峰助教 — 使用說明

## 快速啟動

在 Claude Code 中開啟此資料夾，小峰就上線了。

```bash
cd 小峰助教
claude  # 開啟 Claude Code
```

## 你可以對小峰說

| 指令 | 小峰會做 |
|------|----------|
| 「小峰出來」 | 自我介紹 + 播簡報 + 說話 |
| 「小峰介紹[主題]」 | 生成主題簡報並語音播報 |
| 「小峰出[科目]題目」 | 生成隨堂測驗 |
| 「小峰生一張[描述]的圖」 | 呼叫 Image 2 生成插圖 |
| 「小峰把剛才的內容播給全班看」 | 開啟簡報到大螢幕 |

## 工具直接使用

```bash
# 只播簡報（不語音）
python tools/slide.py --title "標題" --content "內容" --no-voice

# 只說話
python tools/voice.py "要說的話"

# 生成插圖（需要 OPENAI_API_KEY）
python tools/image_gen.py "a cute orange fox teaching math" --output slides/fox.png

# 簡報 + 語音 一次完成
python tools/present_with_voice.py --title "標題" --content "- 重點1\n- 重點2"
```

## 設定 OpenAI API Key（生圖用）

```bash
# Windows
set OPENAI_API_KEY=你的金鑰

# 或在系統環境變數中設定（永久）
```

## 目錄結構

```
小峰助教/
├── CLAUDE.md          ← 小峰的人格設定（Claude Code 讀取）
├── tools/
│   ├── voice.py       ← 語音播報
│   ├── slide.py       ← HTML 簡報生成
│   ├── image_gen.py   ← Image 2 生圖
│   └── present_with_voice.py  ← 簡報 + 語音合一
├── skills/
│   ├── present.md     ← 上台技能說明
│   └── quiz.md        ← 出題技能說明
└── slides/            ← 生成的簡報存這裡
```
