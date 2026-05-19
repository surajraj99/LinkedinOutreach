import pytest
from linkedin.api.activity import parse_activity_response

def test_parse_activity_response():
    # Mock Voyager response
    mock_data = {
        "included": [
            {
                "$type": "com.linkedin.voyager.dash.identity.profile.ProfileUpdate",
                "createdTime": 1716000000000, # Some date in May 2024
                "value": {
                    "com.linkedin.voyager.dash.identity.profile.ProfileUpdateValue": {
                        "text": {"text": "Just finished a great project on AI!"}
                    }
                }
            },
            {
                "$type": "com.linkedin.voyager.dash.identity.profile.ProfileUpdate",
                "createdTime": 1715000000000,
                "value": {
                    "com.linkedin.voyager.dash.identity.profile.ProfileUpdateValue": {
                        "text": {"text": "Excited to join the new team at Valthos."}
                    }
                }
            },
            {
                "$type": "com.linkedin.voyager.dash.identity.profile.ProfileUpdate",
                "createdTime": 1714000000000,
                "value": {
                    "com.linkedin.voyager.dash.identity.profile.ProfileUpdateValue": {
                        "text": {"text": "Looking for new opportunities in CompBio."}
                    }
                }
            },
            {
                "$type": "com.linkedin.voyager.dash.identity.profile.ProfileUpdate",
                "createdTime": 1713000000000,
                "value": {
                    "com.linkedin.voyager.dash.identity.profile.ProfileUpdateValue": {
                        "text": {"text": "Older post that should be ignored."}
                    }
                }
            }
        ]
    }
    
    activity = parse_activity_response(mock_data)
    
    assert len(activity) == 3
    assert activity[0]["text"] == "Just finished a great project on AI!"
    assert activity[0]["timestamp"] == 1716000000000
    assert activity[1]["text"] == "Excited to join the new team at Valthos."
    assert activity[2]["text"] == "Looking for new opportunities in CompBio."
