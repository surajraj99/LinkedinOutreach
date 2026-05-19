import pytest
from unittest.mock import MagicMock, patch
from linkedin.ml.qualifier import qualify_with_llm

@patch("pydantic_ai.Agent")
@patch("linkedin.llm.run_agent_sync")
@patch("linkedin.llm.get_llm_model")
def test_dynamic_qualification(mock_get_model, mock_run_sync, mock_agent):
    profile_text = "Experienced Data Scientist with a focus on Machine Learning and NLP."
    
    # Case A: low similarity (auto-reject)
    label_low, reason_low = qualify_with_llm(
        profile_text, 
        similarity_score=0.3, 
        campaign_objective="Find anyone"
    )
    assert label_low == 0
    assert "Low semantic similarity" in reason_low

    # Case B: healthcare marketers (LLM rejection)
    mock_run_sync.return_value.output.is_match = False
    mock_run_sync.return_value.output.talking_points = "Not a fit for healthcare marketing."
    
    label_a, reason_a = qualify_with_llm(
        profile_text, 
        similarity_score=0.5, # Above 0.4 threshold
        campaign_objective="Find healthcare marketers",
        likelihood_score=0.1 # Inactive user but should still hit LLM
    )
    assert label_a == 0
    assert "Not a fit" in reason_a
    
    # Case B: machine learning practitioners
    mock_run_sync.return_value.output.is_match = True
    mock_run_sync.return_value.output.talking_points = "Great match for ML practitioners!"
    
    label_b, reason_b = qualify_with_llm(
        profile_text, 
        similarity_score=0.8, 
        campaign_objective="Find machine learning practitioners"
    )
    assert label_b == 1
    assert "Great match" in reason_b

@patch("pydantic_ai.Agent")
@patch("linkedin.llm.run_agent_sync")
@patch("linkedin.llm.get_llm_model")
def test_llm_prompt_verification(mock_get_model, mock_run_sync, mock_agent):
    profile_text = "Software Engineer at Google."
    recent_posts = "Post: Just published a blog post about LLM safety."
    campaign_objective = "Find AI safety researchers"
    
    # Mock LLM response that uses activity context
    mock_run_sync.return_value.output.is_match = True
    mock_run_sync.return_value.output.talking_points = "I read your recent post about LLM safety, very insightful!"
    
    label, reason = qualify_with_llm(
        profile_text,
        similarity_score=0.9,
        campaign_objective=campaign_objective,
        recent_posts=recent_posts
    )
    
    assert label == 1
    assert "LLM safety" in reason
