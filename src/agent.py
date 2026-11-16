"""Agent Controller and Runner connecting to NVIDIA Build API (google/gemma-4-31b-it)."""
import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)


def load_env_file(env_path: Path = Path(".env")) -> dict[str, str]:
    """Load simple KEY=VALUE pairs from a .env file."""
    env_vars = {}
    if not env_path.exists():
        return env_vars
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            key, val = line.split("=", 1)
            env_vars[key.strip()] = val.strip().strip("'\"")
    return env_vars


class NvidiaGemmaController:
    """Controller implementation for NVIDIA NIM API with google/gemma-4-31b-it."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = "https://integrate.api.nvidia.com/v1",
        model: str = "nvidia/nemotron-3.5-lightning-30b-a3b",
        temperature: float = 0.1,
        max_tokens: int = 3000
    ):
        env = load_env_file()
        self.api_key = api_key or env.get("NVIDIA_API_KEY") or env.get("LLM_API_KEY") or os.environ.get("NVIDIA_API_KEY")
        if not self.api_key or self.api_key.startswith("nvapi-your_api_key"):
            raise ValueError(
                "NVIDIA_API_KEY is not set or still has placeholder. "
                "Please fill your API key in the .env file."
            )
        self.base_url = (env.get("LLM_BASE_URL") or base_url).rstrip("/")
        self.model = env.get("LLM_MODEL") or model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def _call_llm(self, messages: list[dict[str, str]], retries: int = 3) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": 0.7
        }

        last_err = None
        for attempt in range(1, retries + 1):
            try:
                resp = requests.post(url, headers=headers, json=payload, timeout=120)
                if resp.status_code == 200:
                    data = resp.json()
                    msg = data["choices"][0]["message"]
                    content = msg.get("content")
                    # If content is empty or None, fallback to reasoning_content
                    if not content and msg.get("reasoning_content"):
                        content = msg["reasoning_content"]
                    return content or ""
                elif resp.status_code in (429, 500, 502, 503, 504):
                    logger.warning(f"HTTP {resp.status_code} on attempt {attempt}/{retries}. Retrying...")
                    time.sleep(attempt * 2)
                else:
                    raise RuntimeError(f"NVIDIA API Error {resp.status_code}: {resp.text}")
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                last_err = e
                logger.warning(f"Connection error on attempt {attempt}/{retries}: {e}. Retrying...")
                time.sleep(attempt * 2)

        raise RuntimeError(f"NVIDIA API failed after {retries} attempts: {last_err}")

    def decide(self, question: str, history: list[dict[str, Any]]) -> dict[str, Any]:
        """Decide next action: search or final answer with citations."""
        system_prompt = (
            "Bạn là một trợ lý AI thông minh chuyên nghiên cứu tài liệu kỹ thuật về RAG (Retrieval-Augmented Generation) "
            "và LangChain (khóa AIO2025).\n"
            "Bạn có quyền truy xuất dữ liệu từ kho tài liệu để tìm kiếm bằng chứng và trả lời câu hỏi.\n\n"
            "QUY TẮC HOẠT ĐỘNG:\n"
            "1. Nếu chưa có ngữ cảnh tài liệu (context) hoặc ngữ cảnh hiện tại chưa đủ để trả lời câu hỏi, hãy yêu cầu tìm kiếm bằng cách trả về JSON:\n"
            '   {"action": "search", "query": "<câu truy vấn ngắn gọn, tập trung vào từ khóa cốt lõi>"}\n\n'
            "2. Khi đã có ngữ cảnh tài liệu (gồm các đoạn văn bản kèm định danh [chunk_id]):\n"
            "   - Kiểm tra kỹ xem trong ngữ cảnh có thông tin chính xác hỗ trợ câu trả lời hay không.\n"
            "   - NẾU CÓ ĐỦ BẰNG CHỨNG: Trả lời câu hỏi một cách chính xác, khách quan, súc tích bằng tiếng Việt. "
            "BẮT BUỘC chèn ký hiệu trích dẫn [chunk_id] ngay sau các luận điểm/thông tin được lấy từ chunk đó. "
            "Trả về JSON:\n"
            '     {"action": "answer", "answer": "<nội dung câu trả lời kèm [chunk_id]>", "citations": ["<chunk_id>", ...]}\n'
            "   - NẾU KHÔNG CÓ BẰNG CHỨNG (tài liệu không nhắc đến hoặc thiếu dữ kiện): Tuyệt đối KHÔNG tự bịa đặt, hãy từ chối trả lời:\n"
            '     {"action": "answer", "answer": "Không đủ bằng chứng trong tài liệu để trả lời câu hỏi này.", "citations": []}\n\n'
            "3. BẮT BUỘC chỉ trả về duy nhất một khối JSON hợp lệ, không thêm lời chào, không viết suy nghĩ dài dòng."
        )

        user_content = f"Câu hỏi của người dùng: {question}\n\n"

        if not history:
            user_content += "Hiện tại chưa có tài liệu nào trong ngữ cảnh. Hãy đưa ra truy vấn tìm kiếm phù hợp."
        else:
            latest = history[-1]
            user_content += f"Các truy vấn đã tìm kiếm trước đó: {latest.get('queries', [])}\n"
            user_content += f"Ngữ cảnh tài liệu hiện có:\n{latest.get('context', '(Trống)')}\n\n"
            user_content += (
                "Dựa trên ngữ cảnh trên, nếu đã đủ thông tin hãy trả lời và trích dẫn [chunk_id]. "
                "Nếu chưa đủ thông tin và còn hướng tìm kiếm khác, hãy đưa ra truy vấn mới. "
                "Nếu tài liệu hoàn toàn không có thông tin, hãy từ chối trả lời."
            )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        raw_output = self._call_llm(messages)
        return self._parse_response(raw_output)

    def _parse_response(self, text: str) -> dict[str, Any]:
        """Clean and parse JSON from model output, handling thinking traces and citations."""
        cleaned = text.strip()

        # 1. Try markdown code blocks (from latest to earliest)
        code_blocks = re.findall(r"```(?:json)?\s*(\{.*?\})\s*```", cleaned, re.DOTALL)
        for block in reversed(code_blocks):
            try:
                parsed = json.loads(block)
                if isinstance(parsed, dict) and "action" in parsed:
                    return self._normalize_action(parsed)
            except Exception:
                pass

        # 2. Search backwards for {"action": ...}
        idx = cleaned.rfind('{"action":')
        if idx != -1:
            snippet = cleaned[idx:]
            depth = 0
            for i, ch in enumerate(snippet):
                if ch == '{':
                    depth += 1
                elif ch == '}':
                    depth -= 1
                    if depth == 0:
                        try:
                            parsed = json.loads(snippet[:i+1])
                            if isinstance(parsed, dict) and "action" in parsed:
                                return self._normalize_action(parsed)
                        except Exception:
                            pass
                        break

            # If brace was cut off, attempt auto-closing
            try:
                parsed = json.loads(snippet.rstrip() + '"}')
                if isinstance(parsed, dict) and "action" in parsed:
                    return self._normalize_action(parsed)
            except Exception:
                pass

        # 3. Direct JSON attempt
        try:
            parsed = json.loads(cleaned)
            if isinstance(parsed, dict) and "action" in parsed:
                return self._normalize_action(parsed)
        except Exception:
            pass

        logger.warning(f"Failed to parse LLM JSON: {text[:200]}")
        return {
            "action": "answer",
            "answer": "Không đủ bằng chứng để trả lời.",
            "citations": []
        }

    def _normalize_action(self, action: dict[str, Any]) -> dict[str, Any]:
        """Ensure answer citations appear in answer text as [chunk-id] per starter contract."""
        if action.get("action") == "answer":
            answer = action.get("answer") or ""
            citations = action.get("citations") or []
            if isinstance(citations, list) and isinstance(answer, str):
                # Ensure all cited IDs appear in answer text
                missing = [c for c in citations if isinstance(c, str) and f"[{c}]" not in answer]
                if missing:
                    answer = answer.rstrip() + " " + " ".join(f"[{c}]" for c in missing)
                action["answer"] = answer
                action["citations"] = [str(c) for c in citations if isinstance(c, str)]
        return action
