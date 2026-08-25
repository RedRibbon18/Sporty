import pytest
from framework.config import (
    DEFAULT_BROWSER,
    DEFAULT_HEADLESS,
    get_environment_config,
)
from framework.drivers.webdriver_manager import WebDriverManager


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default=None,
        choices=["dev", "qa", "prod"],
        help="Environment for config values (dev, qa, prod)",
    )
    parser.addoption(
        "--base-url",
        action="store",
        default="https://qae-assignment-tau.vercel.app/",
        help="Base URL for E2E tests",
    )
    parser.addoption(
        "--browser",
        action="store",
        default=DEFAULT_BROWSER,
        choices=["chrome", "firefox"],
        help="Browser for E2E tests",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=DEFAULT_HEADLESS,
        help="Run browser in headless mode",
    )
    parser.addoption(
        "--user-id",
        action="store",
        required=True,
        help="User id to authorization",
    )


@pytest.fixture(scope="session")
def base_url(request):
    env_name = request.config.getoption("--env")
    config = get_environment_config(env_name)
    explicit_url = request.config.getoption("--base-url")
    return explicit_url or config.base_url


@pytest.fixture(scope="session")
def user_id(request):
    env_name = request.config.getoption("--env")
    config = get_environment_config(env_name)
    explicit_user_id = request.config.getoption("--user-id")
    return explicit_user_id or config.user_id


@pytest.fixture(scope="session")
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    manager = WebDriverManager(browser_name=browser_name, headless=headless)
    driver = manager.get_driver()

    yield driver

    driver.quit()
