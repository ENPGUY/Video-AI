EnerAion Video AI
Streamlit 기반 텍스트→영상 생성 앱의 기본 프로젝트입니다.
1. 설치
```bash
python -m venv .venv
```
Windows:
```powershell
.venv\Scripts\activate
pip install -r requirements.txt
```
2. 실행
```powershell
streamlit run app.py
```
3. Demo 모드
Demo는 UI/다운로드 동작 확인용이며 실제 AI 영상이 아닙니다.
PC에 FFmpeg가 설치되어 있어야 합니다.
4. 실제 영상 생성 API 연결
`.env.example`을 `.env`로 복사하고 다음 값을 설정합니다.
```text
REPLICATE_API_TOKEN=...
REPLICATE_MODEL=...
```
그 후 앱에서 `replicate`를 선택합니다.
주의: 영상 모델마다 API 입력 파라미터가 다릅니다.
`video_generator.py`의 `model_input`을 선택한 모델의 최신 API 스키마에 맞춰야 합니다.
구조
`app.py`: Streamlit UI
`video_generator.py`: 영상 생성 provider
`.env.example`: 비밀키 설정 예시
`outputs/`: 생성 영상 저장 폴더
