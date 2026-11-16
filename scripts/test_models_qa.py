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

models = [
    "openai/gpt-oss-20b",
    "stepfun-ai/step-5-preview",
    "z-ai/glm-5.3-flash",
    "nvidia/nemotron-3.5-lightning-30b-a3b"
]

prompt = """Bạn là trợ lý AI. Trả về JSON:
{"action": "answer", "answer": "Patrick Lewis và FAIR năm 2020 [chunk_1]", "citations": ["chunk_1"]}
Chỉ trả về JSON.
"""

for m in models:
    t0 = time.time()
    try:
        resp = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers=headers,
            json={
                "model": m,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1024,
                "temperature": 0.1
            },
            timeout=20
        )
        msg = resp.json()["choices"][0]["message"]
        content = msg.get("content") or msg.get("reasoning_content")
        print(f"[{m}] Status {resp.status_code} in {time.time()-t0:.2f}s:")
        print(f"  Content: {content[:150] if content else 'None'}\n")
    except Exception as e:
        print(f"[{m}] Error after {time.time()-t0:.2f}s: {e}\n")
