import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

def get_provider_name(provider: str) -> str:
    return {"demo": "Demo MP4 생성", "replicate": "Replicate API"}.get(provider, provider)

def _output_path() -> Path:
    return OUTPUT_DIR / f"video_{int(time.time())}_{uuid.uuid4().hex[:6]}.mp4"

def _demo_video(duration: int, aspect_ratio: str) -> Path:
    """FFmpeg가 있으면 테스트용 MP4를 만든다. 실제 AI 생성은 아니다."""
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "Demo 모드에는 FFmpeg가 필요합니다. FFmpeg를 설치하거나 Replicate 모드를 사용하세요."
        )
    sizes = {"16:9": "1280x720", "9:16": "720x1280", "1:1": "720x720"}
    out = _output_path()
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=black:s={sizes[aspect_ratio]}:d={duration}",
        "-vf", "format=yuv420p",
        "-r", "24",
        str(out),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out

def _replicate_video(prompt, negative_prompt, duration, aspect_ratio, quality) -> Path:
    """
    Replicate 연결 예제.
    모델마다 input 파라미터가 다르므로 REPLICATE_MODEL과 아래 input을
    선택한 모델의 API 스키마에 맞게 조정해야 한다.
    """
    token = os.getenv("REPLICATE_API_TOKEN")
    model = os.getenv("REPLICATE_MODEL")
    if not token:
        raise RuntimeError("REPLICATE_API_TOKEN이 .env에 없습니다.")
    if not model:
        raise RuntimeError("REPLICATE_MODEL이 .env에 없습니다.")

    import replicate

    os.environ["REPLICATE_API_TOKEN"] = token

    model_input = {
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
    }
    # 아래 항목은 사용하는 모델이 지원할 때만 활성화하세요.
    # model_input["negative_prompt"] = negative_prompt
    # model_input["duration"] = duration

    output = replicate.run(model, input=model_input)

    # Replicate 모델별 반환 타입(URL/File/list)을 최대한 일반적으로 처리
    if isinstance(output, (list, tuple)):
        output = output[0]

    if hasattr(output, "read"):
        data = output.read()
        out = _output_path()
        out.write_bytes(data)
        return out

    url = getattr(output, "url", None)
    if callable(url):
        url = url()
    if not url:
        url = str(output)

    import requests
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    out = _output_path()
    out.write_bytes(r.content)
    return out

def generate_video(provider, prompt, negative_prompt="", duration=5,
                   aspect_ratio="16:9", quality="Standard") -> Path:
    if not prompt.strip():
        raise ValueError("prompt가 비어 있습니다.")
    if provider == "demo":
        return _demo_video(duration, aspect_ratio)
    if provider == "replicate":
        return _replicate_video(prompt, negative_prompt, duration, aspect_ratio, quality)
    raise ValueError(f"지원하지 않는 provider: {provider}")
