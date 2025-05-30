import pytest
from playwright.sync_api import sync_playwright
from pages.loldlePage import LoldlePage

@pytest.fixture()
def setup_browser():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        loldlePage = LoldlePage(page)

        yield loldlePage

        browser.close()


def test_guess_the_correct_lol_champion(setup_browser):
    setup_browser.test_open_loldle_and_change_language_if_needed()
    setup_browser.guess_until_guessing_is_successful()