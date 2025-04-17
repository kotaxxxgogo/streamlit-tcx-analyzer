import streamlit as st
import openai
from utils import parse_tcx, summarize_run

st.set_page_config(page_title="ランニングレポート生成", layout="centered")
st.title("🏃‍♂️ Garmin TCX 分析アプリ")
st.write("TCXファイルをアップロードすると、ChatGPTがアドバイスを返します。")

openai.api_key = st.secrets["OPENAI_API_KEY"]

uploaded_file = st.file_uploader("📤 TCXファイルをアップロード", type="tcx")

if uploaded_file is not None:
    df = parse_tcx(uploaded_file)
    summary = summarize_run(df)

    st.subheader("📊 要約データ")
    for k, v in summary.items():
        st.write(f"**{k}**: {v}")

    st.subheader("🤖 ChatGPTアドバイス")
    prompt = f"""以下はランニングの要約です：\n{summary}
Danielsの理論に基づいて、改善点やアドバイスを200文字程度で日本語で教えてください。"""

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",  # または gpt-3.5-turbo
        messages=[{"role": "user", "content": prompt}]
    )
    comment = response.choices[0].message.content
    st.write(comment)
