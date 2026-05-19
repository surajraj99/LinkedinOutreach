import pytest
from django.utils import timezone
from datetime import timedelta
from linkedin.ml.embeddings import compute_response_likelihood

def test_likelihood_scoring():
    similarity_score = 0.8
    
    # User A: No activity
    likelihood_a = compute_response_likelihood(similarity_score, None)
    assert likelihood_a == 0.1 # Capped at 0.1
    
    # User B: Active 2 days ago
    recent_date = timezone.now() - timedelta(days=2)
    likelihood_b = compute_response_likelihood(similarity_score, recent_date)
    assert likelihood_b == 1.0 # 0.8 * 1.5 = 1.2, capped at 1.0
    
    # User C: Active 30 days ago
    moderate_date = timezone.now() - timedelta(days=30)
    likelihood_c = compute_response_likelihood(similarity_score, moderate_date)
    assert likelihood_c == 0.8 # No boost, but not capped low
    
    # User D: Active 100 days ago
    old_date = timezone.now() - timedelta(days=100)
    likelihood_d = compute_response_likelihood(similarity_score, old_date)
    assert likelihood_d == 0.1 # Capped at 0.1
    
    # Check ranking order
    results = [
        {"name": "A", "score": likelihood_a},
        {"name": "B", "score": likelihood_b},
        {"name": "C", "score": likelihood_c},
        {"name": "D", "score": likelihood_d},
    ]
    results.sort(key=lambda x: x["score"], reverse=True)
    
    assert results[0]["name"] == "B" # Highest boost
    assert results[1]["name"] == "C" # Base score
    # A and D are both 0.1, order doesn't matter much but they should be last
    assert results[2]["score"] == 0.1
    assert results[3]["score"] == 0.1
