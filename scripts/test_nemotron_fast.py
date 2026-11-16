import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import requests
import json
from src.agent import load_env_file

env = load_env_file()
key = env.get("NVIDIA_API_KEY")
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

model = "nvidia/nemotron-3.5-lightning-30b-a3b"
print(f"Testing {model} on full QA prompt...")

prompt = """Bạn là trợ lý AI nghiên cứu tài liệu. Hãy trả về JSON:
{"action": "answer", "answer": "<nội dung câu trả lời kèm [chunk_id]>", "citations": ["<chunk_id>"]}

Câu hỏi: Khái niệm RAG lần đầu tiên được đề xuất chính thức trong bài báo nào và bởi ai?
Ngữ cảnh:
[aio2025-tutorial-rag_p4_b00 | page 4]
Khái niệm RAG lần đầu tiên được đề xuất chính thức trong bài báo khoa học “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks” bởi Patrick Lewis và các cộng sự tại Facebook AI Research (FAIR) vào năm 2020.
"""

t0 = time.time()
resp = requests.post(
    "https://integrate.api.nvidia.com/v1/chat/completions",
    headers=headers,
    json={
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "max_tokens": 512
    },
    timeout=60
)
t_elapsed = time.time() - t0
print(f"Status: {resp.status_code} in {t_elapsed:.2f}s")
if resp.status_code == 200:
    msg = resp.json()["choices"][0]["message"]
    print("Content:", msg.get("content"))
    if not msg.get("content") and msg.get("reasoning_content"):
        print("Reasoning:", msg.get("reasoning_content")[:300])
else:
    print("Error:", resp.text)
