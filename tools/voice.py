"""
小峰語音工具
用法：python tools/voice.py "要說的文字"
"""
import sys
import asyncio
import subprocess
import tempfile
import os


async def speak_async(text: str, voice: str = "zh-TW-YunJheNeural"):
    try:
        import edge_tts
    except ImportError:
        print("[小峰] edge-tts 未安裝，執行：pip install edge-tts")
        sys.exit(1)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        output_path = f.name

    communicate = edge_tts.Communicate(text, voice=voice)
    await communicate.save(output_path)

    # Windows 播放
    if sys.platform == "win32":
        os.startfile(output_path)
    elif sys.platform == "darwin":
        subprocess.run(["afplay", output_path])
    else:
        subprocess.run(["mpg123", output_path])

    print(f"[小峰說] {text}")


def speak(text: str, voice: str = "zh-TW-YunJheNeural"):
    asyncio.run(speak_async(text, voice))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python tools/voice.py \"要說的文字\"")
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    speak(text)
