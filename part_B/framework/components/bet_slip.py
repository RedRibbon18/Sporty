from framework.components.base_component import BaseComponent
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class BetSlipComponent(BaseComponent):
    """Represents the bet slip component of the web application."""
    locators= {
        "container": (By.ID, "bet-slip"),
        # header elements
        "header": (By.ID, "bet-slip-header"),
        "title": (By.ID, "bet-slip-title"),
        "bet_count": (By.ID, "bet-slip-count"),
        "header_balance": (By.ID, "bet-slip-balance"),
        # only prensent when there are selections in the bet slip
        "remove_all": (By.ID, "bet-slip-remove-all"),
        # Contents elements
        # only present when there are no selections in the bet slip
        "empty": (By.CLASS_NAME, "betSlipBodyEmpty"),
        # only present when there are selections in the bet slip
        # selection elements
        "selection_teams": (By.CLASS_NAME, "betSelectionTeams"),
        "selection_market": (By.CLASS_NAME, "betSelectionMarket"),
        "selection_remove_button":(By.ID, "bet-slip-selection-remove"),
        "selection_odds":(By.CLASS_NAME, "betSelectionOdds"),
        # Stake
        "stake_input": (By.ID, "bet-slip-stake-input"),
        # footer elements
        "total_stake": (By.ID, "bet-slip-total-stake"),
        "potential_payout": (By.ID, "bet-slip-potential-payout"),
        "place_bet_button": (By.ID, "bet-slip-place-bet")
    }

    def __init__(self, driver: WebDriver, test_id: str):
        super().__init__(driver, test_id)

    def get_title(self):
        """Get the title text from the Bet Slip box."""
        return self.driver_explicit_wait.find_visible_element(self.locators["title"]).text

    def get_balance(self):
        """Get the balance text from the Bet Slip header"""
        return self.driver_explicit_wait.find_visible_element(self.locators["header_balance"]).text

    def get_selection_teams(self):
        """Get the selection teams element from the Bet Slip."""
        return self.driver_explicit_wait.find_visible_element(self.locators["selection_teams"]).text

    def get_selection_market(self):
        """Get the selection market element from the Bet Slip."""
        return self.driver_explicit_wait.find_visible_element(self.locators["selection_market"]).text

    def get_selection_odds(self):
        """Get the selection odds element from the Bet Slip."""
        return self.driver_explicit_wait.find_visible_element(self.locators["selection_odds"]).text

    def get_total_stake(self):
        """Get the total stake element from the Bet Slip."""
        return self.driver_explicit_wait.find_visible_element(self.locators["total_stake"]).text

    def get_potential_payout(self):
        """Get the potential payout element from the Bet Slip."""
        return self.driver_explicit_wait.find_visible_element(self.locators["potential_payout"]).text

    def enter_stake(self, stake_value: str):
        """Set the stake value in the Bet Slip."""
        self.driver_explicit_wait.send_keys(self.locators["stake_input"], stake_value)

    def click_place_bet(self):
        """Click the place bet button in the Bet Slip."""
        self.driver_explicit_wait.click(self.locators["place_bet_button"])
