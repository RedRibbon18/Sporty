import pytest
from framework.api.api_client import ApiClient
from framework.api.reset_balance_service import ResetBalanceService
from framework.api.balance_service import BalanceService
from framework.api.match_service import MatchService
from framework.helpers import time_helper
from framework.config import ENDPOINTS


@pytest.fixture
def user_headers(user_id):
    return {"x-user-id": user_id}

@pytest.fixture
def valid_match_id(user_headers):
    def get_first_upcoming_match(match_list, current_date):
         # just to be sure let's find the next day matches
         next_day = time_helper.get_next_day(current_date)
         for match in match_list:
              match_date = match["kickoffDate"]
              # TODO: we are assuming that this date is in UTC tz, ask dev about it and fix
              match_datetime_o = time_helper.get_dt_object_from_str_with_utc_tz(match_date, "%Y-%m-%d")
              if match_datetime_o > next_day: return match["id"]
         # if no upcoming event return None
         return None
            
    current_date = time_helper.get_current_date_with_tz()
    match_service = MatchService()
    response = match_service.get_matches(headers=user_headers)
    assert response.status_code == 200, f"Failed to GET macthes, status code: {response.status_code}"
    return get_first_upcoming_match(response.json(), current_date)

     
@pytest.fixture
def reset_funds(user_headers):
    """
    Fixture to reset user balance, if the request fails, it will throw an
    exception.
    Also checking balance and currency changes were persisted comparing to
    a get balance, this won't block test execution but test will fail if  a
    discrepancy was found with proper fail message.
    """
    def get_balance_and_currency_from_response(response):
            body = response.json()
            return body["balance"], body["currency"]

    rb_service = ResetBalanceService()
    response = rb_service.reset_balance(headers=user_headers)
    # Let's verify that reset went successfully
    assert response.status_code == 200, f"Failed to reset balance, status code: {response.status_code}"
    res_balance, res_currency = get_balance_and_currency_from_response(response)

    # Let's check if balance was persisted
    balance_service = BalanceService()
    response = balance_service.get_balance(headers=user_headers)
    assert response.status_code == 200, f"Failed to GET balance, status code: {response.status_code}"
    updated_balance, updated_currency = get_balance_and_currency_from_response(response)

    pytest.assume( res_balance == updated_balance, (
        "Updated balance does not match expected: "
        f"Balance found: {updated_balance}\n"
        f"Balance expected: {res_balance}"
    ))

    pytest.assume( updated_currency == res_currency, (
        "Updated currency does not match expected: "
        f"Currency found: {updated_currency}\n"
        f"Currency expected: {res_currency}"
    ))