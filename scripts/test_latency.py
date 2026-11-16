import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import time
import requests
from src.agent import load_env_file

env = load_env_file()
key = env.get("NVIDIA_API_KEY")
headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}

models_to_test = [
    "minimaxai/minimax-m3.1-flash",
    "nvidia/nemotron-3.5-lightning-30b-a3b"
]

print("Testing latency of available chat models:")
for m in models_to_test:
    t0 = time.time()
    try:
        resp = requests.post(
            "https://integrate.api.nvidia.com/v1/chat/completions",
            headers=headers,
            json={
                "model": m,
                "messages": [{"role": "user", "content": "1+1=?"}],
                "max_tokens": 10
            },
            timeout=30
        )
        elapsed = time.time() - t0
        print(f"Status for {m}: {resp.status_code} in {elapsed:.2f}s")
        try:
            data = resp.json()
            print(f"Data for {m}: {data}")
        except Exception:
            print(f"Text for {m}: {resp.text[:200]}")
    except Exception as e:
        print(f" [!] {m}: {type(e).__name__} after {time.time()-t0:.2f}s")
