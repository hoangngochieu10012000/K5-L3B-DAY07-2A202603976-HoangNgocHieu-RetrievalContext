"""Index 32 Bonus SGK Dia li 10 chunks into local Qdrant collection 'bonus_sgk10'."""
import json
import logging
import os
import sys
from pathlib import Path

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from src.embeddings import Day6Embedder
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CHUNKS_FILE = ROOT_DIR / "data" / "bonus" / "chunks.json"
QDRANT_PATH = ROOT_DIR / "data" / "qdrant_db"
COLLECTION_NAME = "bonus_sgk10"

with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
    chunks = json.load(f)

logger.info(f"Loaded {len(chunks)} bonus chunks")

embedder = Day6Embedder()
client = QdrantClient(path=str(QDRANT_PATH))

# Re-create collection
existing = [c.name for c in client.get_collections().collections]
if COLLECTION_NAME in existing:
    logger.info(f"Collection '{COLLECTION_NAME}' already exists, deleting and re-creating...")
    client.delete_collection(COLLECTION_NAME)

client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=768, distance=Distance.COSINE)
)
logger.info(f"Created collection '{COLLECTION_NAME}' (768d, Cosine)")

texts = [c["text"] for c in chunks]
embeddings = embedder.embed_documents(texts, batch_size=16)

points = []
for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
    points.append(
        PointStruct(
            id=idx + 1,
            vector=emb,
            payload={
                "chunk_id": chunk["id"],
                "source_id": chunk["source_id"],
                "source": chunk["source"],
                "page": chunk["page"],
                "text": chunk["text"],
                "metadata": chunk.get("metadata", {}),
                "type": chunk.get("metadata", {}).get("type", "text"),
                "chapter": chunk.get("metadata", {}).get("chapter", ""),
                "lesson": chunk.get("metadata", {}).get("lesson", "")
            }
        )
    )

client.upsert(collection_name=COLLECTION_NAME, points=points)
logger.info(f"Successfully indexed {len(points)} points into '{COLLECTION_NAME}'!")
client.close()
