# linkedin/ml/embeddings.py
"""Local sentence-transformer embeddings and similarity scoring."""
from __future__ import annotations

import logging
import numpy as np
from linkedin.conf import CAMPAIGN_CONFIG, FASTEMBED_CACHE_DIR

logger = logging.getLogger(__name__)

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

def compute_similarity(embedding: np.ndarray, target_embedding: np.ndarray) -> float:
    """Compute cosine similarity between two embeddings."""
    # Cosine similarity: (a . b) / (||a|| * ||b||)
    dot_product = np.dot(embedding, target_embedding)
    norm_a = np.linalg.norm(embedding)
    norm_b = np.linalg.norm(target_embedding)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(dot_product / (norm_a * norm_b))


def compute_response_likelihood(similarity_score: float, last_active_date) -> float:
    """
    Calculate a response probability metric combining semantic similarity and activity.

    Rules:
    - If last_active_date is None or older than 90 days, cap likelihood at 0.1.
    - If user was active within 7 days, apply a scalar multiplier to base similarity.
    """
    from datetime import timedelta
    from django.utils import timezone

    if last_active_date is None:
        return min(similarity_score, 0.1)

    now = timezone.now()
    age = now - last_active_date

    if age > timedelta(days=90):
        return min(similarity_score, 0.1)

    likelihood = similarity_score

    if age <= timedelta(days=7):
        # User is highly active, boost the base similarity score
        likelihood *= 1.5

    return min(likelihood, 1.0)
