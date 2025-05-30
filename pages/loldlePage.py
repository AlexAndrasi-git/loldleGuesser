import time
from playwright.sync_api import Page, Locator


class LoldlePage:
    def __init__(self, page: Page):
        self.page = page
        self.consentButton = self.page.locator("button[aria-label='Consent']")

        self.changeLanguageSpan = self.page.locator("span[class*='fi flag flag-header img']")
        self.languagePickerInput = self.page.locator("input.vs__search")
        self.englishLanguageSpan = self.page.locator("span.language").filter(has_text="English")

        self.championAttributeContainerDiv = self.page.locator("div[class='answers-container classic-answers-container']")
        self.championNameInput = self.page.locator("input[type='text']")
        self.championGenderDiv = self.page.locator("div[class*='square 2 animate__animated animate__flipInY']")

        self.successfulChampionGuessResults = self.page.locator("div[class='background-end']")

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
        time.sleep(7)

    def test_verify_champion_data(self, number_of_guesses, correct_attributes):
        every_champion_attribute = self.page.locator("div[class='classic-answer']").nth(number_of_guesses -1)
        for attribute in range(1,7):
            champion_attribute_locator = every_champion_attribute.locator("[style='flex-basis: calc(12.5% - 4px);']").nth(attribute)
            champion_attribute_text = champion_attribute_locator.inner_text()
            print(f"With guess number: {number_of_guesses}, attribute {attribute} value is: {champion_attribute_text}")
            champion_attribute_class_for_validation = champion_attribute_locator.get_attribute("class")
            if "good" in champion_attribute_class_for_validation and champion_attribute_text not in correct_attributes:
                correct_attributes.append(champion_attribute_text)
                print(f"The word {champion_attribute_text} has been added to the correct word list: {correct_attributes}")


    def guess_until_guessing_is_successful(self):
        correct_attributes = []
        number_of_guesses = 1
        print(f"Guess number is: {number_of_guesses}")

        while self.successfulChampionGuessResults.is_hidden() and number_of_guesses < 3:
            self.test_guess_the_correct_lol_champion("Ashe")
            self.test_verify_champion_data(number_of_guesses, correct_attributes)
            number_of_guesses += 1
            # self.test_guess_the_correct_lol_champion("Leona")
            # self.test_verify_champion_data(number_of_guesses, correct_attributes)
            # number_of_guesses += 1
            # self.test_guess_the_correct_lol_champion("Yone")
            # self.test_verify_champion_data(number_of_guesses, correct_attributes)
            # number_of_guesses += 1
            # self.test_guess_the_correct_lol_champion("Kayn")
            # self.test_verify_champion_data(number_of_guesses, correct_attributes)
            # number_of_guesses += 1



