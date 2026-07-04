"""
Hugging Face Space (Gradio) — 구강보건 교육 도우미(출처 우선·안전 가드레일).
로컬: python app.py  /  HF Space: 이 파일 + src/ + data/ 업로드.
"""
import gradio as gr
from src.rag import answer, DISCLAIMER

INTRO = ("구강보건 교육 도우미입니다. 믿을 수 있는 정보를 **출처와 함께** 쉬운 말로 안내합니다.\n"
         "⚠️ 진단·처방이 아니며, 증상이 있으면 치과의사 대면 진료를 권합니다.")


def chat(message, history):
    reply, sources = answer(message, k=3)
    src = "\n".join(f"- {s['topic']} (출처: {s['source']}, 유사도 {s['score']})" for s in sources)
    return reply + "\n\n📚 참고한 근거:\n" + src


demo = gr.ChatInterface(
    fn=chat,
    title="구강보건 교육 도우미 (출처 우선 RAG)",
    description=INTRO,
    examples=["충치를 어떻게 예방하나요?", "잇몸에서 피가 나요", "돈이 없어 치과 못 가는데 방법 있나요?",
              "아이 충치 예방은?", "치과 얼마나 자주 가야 하나요?"],
)

if __name__ == "__main__":
    demo.launch()
