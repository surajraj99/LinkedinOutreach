# linkedin/ml/embeddings.py
"""Local sentence-transformer embeddings and similarity scoring."""
from __future__ import annotations

import logging
import numpy as np
from linkedin.conf import CAMPAIGN_CONFIG, FASTEMBED_CACHE_DIR

logger = logging.getLogger(__name__)

# User's professional fingerprint baseline
TARGET_VECTOR_TEXT = "Computational Biology Machine Learning Foundation Models Agentic Workflows Weill Cornell Medicine Georgia Tech Biomedical Engineering Data Scientist Valthos Abridge Phare Health"

_model = None

def _get_model():
    """Lazy-load fastembed model singleton."""
    global _model
    if _model is None:
        from fastembed import TextEmbedding

        # BAAI/bge-small-en-v1.5 is the 384-dim default
        model_name = CAMPAIGN_CONFIG.get("embedding_model", "BAAI/bge-small-en-v1.5")
        
        logger.debug("Loading embedding model: %s", model_name)
        FASTEMBED_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _model = TextEmbedding(model_name=model_name, cache_dir=str(FASTEMBED_CACHE_DIR))
    return _model

def embed_text(text: str) -> np.ndarray:
    """Embed a single text string → 384-dim numpy array."""
    model = _get_model()
    embeddings = list(model.embed([text]))
    return np.array(embeddings[0], dtype=np.float32)

def embed_texts(texts: list[str]) -> np.ndarray:
    """Embed multiple texts → (N, 384) numpy array."""
    model = _get_model()
    embeddings = list(model.embed(texts))
    return np.array(embeddings, dtype=np.float32)

def compute_similarity(embedding: np.ndarray) -> float:
    """Compute cosine similarity between embedding and TARGET_VECTOR."""
    target_emb = embed_text(TARGET_VECTOR_TEXT)
    
    # Cosine similarity: (a . b) / (||a|| * ||b||)
    dot_product = np.dot(embedding, target_emb)
    norm_a = np.linalg.norm(embedding)
    norm_b = np.linalg.norm(target_emb)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return float(dot_product / (norm_a * norm_b))
