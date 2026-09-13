"""
🎛️ UI SO SÁNH: CHATBOT (CẤP 2) vs REACT AGENT + MCP (CẤP 3)
Chạy:  streamlit run ui_compare.py
"""

import json
import os
import sys
import time

import streamlit as st

# Đưa src/ vào path để import các module của lab
SRC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "src")
sys.path.insert(0, SRC_DIR)

from app import load_test_cases, run_react_agent
from mcp_server import MCPAcademicServer
from prompts import CHATBOT_BASELINE_PROMPT
from providers import get_llm_provider

st.set_page_config(page_title="Chatbot vs ReAct Agent (MCP)", page_icon="🤖", layout="wide")


@st.cache_resource
def get_resources():
    provider = get_llm_provider()
    mcp = MCPAcademicServer()
    return provider, mcp


provider, mcp = get_resources()


def extract_final_answer(trace_logs: list) -> str:
    """Lấy Final Answer cuối cùng từ trace log"""
    for ev in reversed(trace_logs):
        if ev.get("action_type") == "FINAL_ANSWER":
            return ev.get("output", "")
    return "(Agent chưa đưa ra câu trả lời cuối)"


def run_chatbot(query: str) -> dict:
    """Chạy Chatbot baseline (không Tool), trả về text + latency"""
    start = time.perf_counter()
    response = provider.generate(query, system_prompt=CHATBOT_BASELINE_PROMPT)
    latency = (time.perf_counter() - start) * 1000
    return {"response": response, "latency_ms": round(latency, 2)}


def run_agent(query: str) -> dict:
    """Chạy ReAct Agent qua MCP, trả về final answer + trace + latency"""
    start = time.perf_counter()
    trace = run_react_agent(query, provider, mcp)
    latency = (time.perf_counter() - start) * 1000
    tool_calls = sum(1 for ev in trace if ev.get("action_type") == "TOOL_EXECUTION")
    return {
        "response": extract_final_answer(trace),
        "trace": trace,
        "tool_calls": tool_calls,
        "latency_ms": round(latency, 2),
    }


# ---------------------------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------------------------
st.sidebar.title("⚙️ Cấu hình")
st.sidebar.write(f"**Provider:** `{provider.__class__.__name__}`")
st.sidebar.write(f"**Model:** `{getattr(provider, 'model_name', 'N/A')}`")

tests = load_test_cases()
tc_options = {"--- Nhập câu hỏi tự do ---": ""}
for t in tests:
    tc_options[f"{t['id']} · {t['complexity']} · {t['type']}"] = t["question"]

batch_mode = st.sidebar.checkbox("Chạy tất cả 5 Test Cases (tốn token)", value=False)

st.sidebar.divider()
st.sidebar.caption("Mẹo: chọn 1 Test Case từ dropdown rồi bấm So sánh.")

# ---------------------------------------------------------------------------
# MAIN — SO SÁNH ĐƠN LẺ
# ---------------------------------------------------------------------------
st.title("🤖 Chatbot vs ReAct Agent (MCP Enhanced)")
st.caption("So sánh trực tiếp Cấp 2 (LLM Chatbot — không có Tool) và Cấp 3 (ReAct Agent + MCP Server).")

selected_label = st.selectbox("Test Case mẫu:", list(tc_options.keys()))
query = st.text_area(
    "Câu hỏi:",
    value=tc_options[selected_label] or "Hãy tra cứu thông tin học vụ của sinh viên SV2026001.",
    height=80,
)

if st.button("🚀 So sánh", type="primary", use_container_width=True):
    query = query.strip()
    if not query:
        st.warning("Hãy nhập câu hỏi trước khi so sánh.")
        st.stop()

    chatbot_result = run_chatbot(query)
    agent_result = run_agent(query)

    st.divider()
    st.subheader(f"📌 Câu hỏi: {query}")

    c1, c2 = st.columns(2, gap="medium")

    with c1:
        st.markdown("### 💬 Chatbot (Cấp 2)")
        st.caption("Không có Tool — trả lời thuần văn bản, dễ ảo giác về dữ liệu thật.")
        st.info(chatbot_result["response"])
        st.metric("⏱️ Latency", f"{chatbot_result['latency_ms']:.0f} ms")

    with c2:
        st.markdown("### 🧠 ReAct Agent + MCP (Cấp 3)")
        st.caption("Suy luận Thought → Action → Observation, truy vấn dữ liệu thật qua MCP Server.")
        st.success(agent_result["response"])

        m1, m2 = st.columns(2)
        m1.metric("⏱️ Latency", f"{agent_result['latency_ms']:.0f} ms")
        m2.metric("🛠️ Tool calls", f"{agent_result['tool_calls']}")

        with st.expander("🧾 Xem Waterfall Trace (Thought → Action → Observation)", expanded=False):
            for ev in agent_result["trace"]:
                if ev.get("action_type") == "TOOL_EXECUTION":
                    st.markdown(
                        f"**Step {ev['step']} · 🛠️ {ev['tool_name']}** "
                        f"`{json.dumps(ev.get('arguments', {}), ensure_ascii=False)}`"
                    )
                    st.code(
                        json.dumps(ev.get("observation", {}), ensure_ascii=False, indent=2),
                        language="json",
                    )
                elif ev.get("action_type") == "FINAL_ANSWER":
                    st.markdown(f"**Step {ev['step']} · 🏁 Final Answer**")
                    st.write(ev.get("output", ""))

# ---------------------------------------------------------------------------
# BATCH MODE — SO SÁNH CẢ 5 TEST CASES
# ---------------------------------------------------------------------------
if batch_mode:
    st.divider()
    st.header("📊 Bảng so sánh toàn bộ Test Cases")

    rows = []
    progress = st.progress(0, text="Đang chạy 5 Test Cases...")
    for i, tc in enumerate(tests):
        q = tc["question"]
        if q.strip().startswith("TODO"):
            rows.append({"TC": tc["id"], "Loại": tc["type"], "Kỳ vọng": tc["expected_behavior"], "Chatbot": "", "Agent": "", "Tool calls": "—", "Chatbot latency": "—", "Agent latency": "—"})
            continue

        cb = run_chatbot(q)
        ag = run_agent(q)
        rows.append({
            "TC": tc["id"],
            "Loại": tc["type"],
            "Kỳ vọng": tc["expected_behavior"][:80] + "...",
            "Chatbot": cb["response"][:120] + ("..." if len(cb["response"]) > 120 else ""),
            "Agent": ag["response"][:120] + ("..." if len(ag["response"]) > 120 else ""),
            "Tool calls": ag["tool_calls"],
            "Chatbot latency": f"{cb['latency_ms']:.0f} ms",
            "Agent latency": f"{ag['latency_ms']:.0f} ms",
        })
        progress.progress((i + 1) / len(tests), text=f"Đã xong {i + 1}/{len(tests)}")

    st.dataframe(rows, use_container_width=True)
    st.caption("Nội dung câu trả lời được cắt ngắn ở 120 ký tự. Chi tiết xem ở phần so sánh đơn lẻ bên trên.")