import json

import pytest
from framework.api.place_bet_service import PlaceBetService


@pytest.mark.regression
@pytest.mark.smoke
def test_api_place_bet_unauthorized(valid_match_id):
    """
    Test to verify that not authorized user can not place a bet
    """
    expected_code = 401
    expected_error_msg = "missing_user_id"
    headers = ""
    body = {
        "matchId": valid_match_id,
        "selection": "HOME",
        "stake": 10.00
    }

    pb_service = PlaceBetService()
    response = pb_service.place_bet(json=json.dumps(body), headers=headers)
    pytest.assume( response.status_code == expected_code, (
        "Invalid status code for unauthorized request:\n"
        f"Found: {response.status_code}, "
        f"Expected: expected_code"
    ))

    error_msg_found = response.json().get("error")
    pytest.assume( expected_error_msg == error_msg_found, (
        "Error message is not as expected:\n"
        f"Found: {error_msg_found}, "
        f"Expected: {expected_error_msg}"
    ))
