import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import requests
from src.agent import load_env_file

env = load_env_file()
key = env.get("NVIDIA_API_KEY")
headers = {"Authorization": f"Bearer {key}", "Accept": "application/json"}

resp = requests.get("https://integrate.api.nvidia.com/v1/models", headers=headers, timeout=15)
models = [m["id"] for m in resp.json().get("data", [])]
print(f"Total models available on NVIDIA NIM: {len(models)}")

candidates = [
    "meta/llama-3.3-70b-instruct",
    "meta/llama-3.1-8b-instruct",
    "mistralai/mistral-7b-instruct-v0.3",
    "google/gemma-2-9b-it",
    "google/gemma-2-27b-it",
    "google/gemma-4-31b-it"
]

print("\nChecking candidates:")
for c in candidates:
    status = "EXISTS" if c in models else "NOT FOUND"
    print(f" - {c}: {status}")

print("All available models:")
for m in sorted(models):
    print(" -", m)
