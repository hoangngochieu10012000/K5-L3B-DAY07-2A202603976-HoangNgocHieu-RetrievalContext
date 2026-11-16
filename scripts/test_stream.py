import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import time
import requests
from src.agent import load_env_file

env = load_env_file()
key = env.get("NVIDIA_API_KEY")
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

payload = {
    "model": "google/gemma-4-31b-it",
    "messages": [{"role": "user", "content": "Khái niệm RAG là gì? Trả lời trong 2 câu."}],
    "temperature": 0.2,
    "max_tokens": 150,
    "stream": True
}

print("Testing streaming with google/gemma-4-31b-it...")
t0 = time.time()
resp = requests.post(
    "https://integrate.api.nvidia.com/v1/chat/completions",
    headers=headers,
    json=payload,
    stream=True,
    timeout=60
)
print(f"Connected in {time.time()-t0:.2f}s, status: {resp.status_code}")

full_content = []
for line in resp.iter_lines():
    if not line:
        continue
    line_str = line.decode("utf-8")
    if line_str.startswith("data: "):
        data_str = line_str[6:].strip()
        if data_str == "[DONE]":
            break
        try:
            chunk = json.loads(data_str)
            delta = chunk["choices"][0]["delta"].get("content", "")
            if delta:
                full_content.append(delta)
                print(delta, end="", flush=True)
        except Exception:
            pass

print(f"\n\nTotal time: {time.time()-t0:.2f}s")
