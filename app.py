import streamlit as st
from video_generator import generate_video, get_provider_name
from pathlib import Path

st.set_page_config(page_title="EnerAion Video AI", page_icon="🎬", layout="wide")

st.title("🎬 EnerAion Video Generation AI")
st.caption("텍스트 프롬프트로 AI 영상을 생성하는 Streamlit 앱")

with st.sidebar:
    st.header("생성 설정")
    provider = st.selectbox("영상 생성 엔진", ["demo", "replicate"])
    duration = st.slider("영상 길이(초)", 3, 10, 5)
    aspect_ratio = st.selectbox("화면 비율", ["16:9", "9:16", "1:1"])
    quality = st.selectbox("품질", ["Standard", "High"])
    st.caption(f"현재 엔진: {get_provider_name(provider)}")

prompt = st.text_area(
    "만들고 싶은 영상을 설명하세요",
    placeholder="예: 미래 LNG 플랜트에서 엔지니어와 로봇이 설비를 점검하는 영화 같은 장면",
    height=160,
)
negative_prompt = st.text_input(
    "제외할 요소(선택)",
    placeholder="blurry, distorted, low quality"
)

if st.button("🎥 영상 생성", type="primary", use_container_width=True):
    if not prompt.strip():
        st.warning("영상 설명을 입력해주세요.")
    else:
        try:
            with st.spinner("영상을 생성하고 있습니다..."):
                video_path = generate_video(
                    provider=provider,
                    prompt=prompt,
                    negative_prompt=negative_prompt,
                    duration=duration,
                    aspect_ratio=aspect_ratio,
                    quality=quality,
                )
            st.success("영상 생성 완료")
            st.video(str(video_path))
            data = Path(video_path).read_bytes()
            st.download_button(
                "⬇️ MP4 다운로드",
                data=data,
                file_name=Path(video_path).name,
                mime="video/mp4",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"생성 실패: {e}")
            st.info("Replicate를 사용할 경우 .env의 REPLICATE_API_TOKEN과 모델 설정을 확인하세요.")
