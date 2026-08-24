from datetime import datetime

import pytest
from framework.components.success_receipt_modal import SuccessReceiptModal
from framework.pages.main_page import MainPage

CURRENCY = "€"  # Assuming the currency is Euro, adjust as needed


@pytest.mark.smoke
@pytest.mark.regression
#@pytest.mark.skip(reason="Showing how to skip a test")
@pytest.mark.parametrize(
    "result, stake",
    [
        ("home", "10"),
        ("draw", "1"),
        ("away", "100"),
    ],
)
def test_user_can_place_a_home_bet(
    browser, base_url, user_id, reset_funds, result, stake
):
    """
    Automating critical happy path, for placing a single bet on an upcoming match
    Validating:
     - bet slip info shown in the proccess
     - placing bet
     - success receipt info
     - User balance updated
    """
    user_id = "candidate-J8g8HD3Lsw"

    main_page = MainPage(
        browser, base_url, test_id="test_user_can_place_a_home_bet", user_id=user_id
    )
    main_page.load()

    starting_balance = (
        main_page.toolbar.get_balance().split(" ")[1].replace(CURRENCY, "")
    )
    expected_final_balance = f"{(float(starting_balance) - float(stake)):.2f}"
    match_list = main_page.get_match_list()
    # Select the first upcoming match card and click the home odds button
    upcoming_match = match_list.select_first_card_by_time_badge("UPCOMING")
    result_odds = match_list.get_card_odds_for_result(upcoming_match, result)
    match_list.click_odds_button(upcoming_match, result)

    bet_slip = main_page.get_bet_slip()

    # Verify that the bet slip has been updated with the selected match
    card_teams = match_list.get_teams_names_for_card(upcoming_match)
    teams_expected = " vs ".join(card_teams)
    teams_found = bet_slip.get_selection_teams()
    pytest.assume(
        teams_expected == teams_found,
        (f"Card teams differs from bet slip info: {teams_expected} / {teams_found}"),
    )

    selection_market_expected = f"Match Winner: {result.capitalize()}"
    selection_market_found = bet_slip.get_selection_market()
    pytest.assume(
        selection_market_expected == selection_market_found,
        (
            "Card Selection Market differs from bet slip info: "
            f"{selection_market_expected} / {selection_market_found}"
        ),
    )

    odds_expected = f"Odds: {result_odds}"
    odds_found = bet_slip.get_selection_odds()
    pytest.assume(
        odds_expected == odds_found,
        (f"Card Odds differs from bet slip info: {odds_expected} / {odds_found}"),
    )

    # Place a bet with a stake of 10
    stake_amount = stake
    bet_slip.enter_stake(stake_amount)

    potential_payout = bet_slip.get_potential_payout()

    # verify potential payout is updated properly in bet slip
    expected_payout = float(stake_amount) * float(result_odds)
    expected_payout_str = f"{CURRENCY}{expected_payout:.2f}"
    pytest.assume(
        expected_payout_str == potential_payout,
        (
            "Potential payout differs from expected:"
            f"{potential_payout} / {expected_payout_str}"
        ),
    )

    # verify stake is updated properly in bet slip
    expected_stake_str = f"{CURRENCY}{float(stake_amount):.2f}"
    total_stake = bet_slip.get_total_stake()
    pytest.assume(
        expected_stake_str == total_stake,
        (
            "Stake shown in bet slips differs from input:"
            f"{total_stake} / {expected_stake_str}"
        ),
    )

    # Place the bet
    bet_slip.click_place_bet()
    expected_timestamp = datetime.now().astimezone().strftime("%Y-%m-%d, %I:%M %p")

    # Wait for receipt and validate info shown
    receipt = SuccessReceiptModal(browser, test_id="test_user_can_place_a_home_bet")
    receipt.wait_for_modal()
    receipt_bet_id = receipt.get_bet_id()
    recepit_match_info = receipt.get_match_info()
    receipt_stake = receipt.get_stake()
    receipt_odds = receipt.get_odds()
    receipt_payout = receipt.get_payout()
    receipt_timestamp = receipt.get_timestamp()

    pytest.assume(receipt_bet_id is not None, ("Bet id info not dound in receipt"))
    pytest.assume(
        recepit_match_info == teams_expected,
        (
            "Match info in receipt differs from expected: "
            f"{recepit_match_info} / {teams_expected}"
        ),
    )
    pytest.assume(
        receipt_stake == total_stake,
        (
            "Stake shown in receipt differs from input: "
            f"{total_stake} / {expected_stake_str}"
        ),
    )
    pytest.assume(
        receipt_odds == result_odds,
        (f"Odds shown in receipt differs from input: {receipt_odds} / {result_odds}"),
    )
    pytest.assume(
        receipt_payout == expected_payout_str,
        (
            "Potential payout shown in receipt differs from expected: "
            f"{receipt_payout} / {expected_payout_str}"
        ),
    )
    pytest.assume(
        receipt_timestamp == expected_timestamp,
        (
            "Timestamp shown in receipt differs from expected: "
            f"{receipt_timestamp} / {expected_timestamp}"
        ),
    )

    receipt.close_modal()  # closing modal
    final_balance = (
        main_page.toolbar.get_balance().split(" ")[1].replace(CURRENCY, "")
    )  # getting balance after bet

    pytest.assume(
        final_balance == expected_final_balance,
        (
            "Balance not being updated properly: "
            f"shown: {final_balance} / expected: {expected_final_balance}"
        ),
    )
