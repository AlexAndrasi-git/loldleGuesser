import time

from playwright.sync_api import Page, Locator

class LoldlePage:
    def __init__(self, page: Page):
        self.page = page
        self.consentButton = self.page.locator("button[aria-label='Consent']")

        self.changeLanguageSpan = self.page.locator("span[class*='fi flag flag-header img']")
        self.languagePickerInput = self.page.locator("input.vs__search")
        self.englishLanguageSpan = self.page.locator("span.language").filter(has_text="English")

        self.championNameInput = self.page.locator("input[type='text']")
        self.championAttributeContainerDiv = self.page.locator("div.square-container")
        self.championGenderDiv = self.page.locator("div[class*='square 2 animate__animated animate__flipInY']")

    def test_open_loldle_and_change_language_if_needed(self):
        loldleUrl = "https://loldle.net/classic"

        self.page.goto(loldleUrl)
        if self.consentButton.is_visible():
            self.consentButton.click()

        selectedLanguage = self.changeLanguageSpan.get_attribute("title")
        print(f"\nThe language by default is: {selectedLanguage}")
        if selectedLanguage != "us":
            self.changeLanguageSpan.click()
            self.languagePickerInput.click()
            self.englishLanguageSpan.click()
            assert self.changeLanguageSpan.get_attribute("title") == "us"

    def test_guess_the_correct_lol_champion(self, championGuess):
        self.championNameInput.fill(championGuess)
        self.championNameInput.press("Enter")
        time.sleep(3)

