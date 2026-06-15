import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BankPage:
    # Все селекторы в одном месте — удобно если вдруг изменится вёрстка
    RUB_CARD = (By.XPATH, "//div[@role='button' and .//h2[text()='Рубли']]")
    CARD_INPUT = (By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
    AMOUNT_INPUT = (By.XPATH, "//input[@placeholder='1000']")
    COMMISSION = (By.ID, "comission")
    RUB_SUM = (By.ID, "rub-sum")
    RUB_RESERVED = (By.ID, "rub-reserved")
    TRANSFER_BTN = (By.XPATH, "//*[contains(text(), 'Перевести')]")
    ERROR_MSG = (By.XPATH, "//*[contains(text(), 'Недостаточно средств')]")

    def __init__(self, driver, base_url="http://localhost:8000"):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, 5)

    def open(self, balance=30000, reserved=0):
        self.driver.get(f"{self.base_url}/?balance={balance}&reserved={reserved}")
        self.wait.until(EC.visibility_of_element_located(self.RUB_SUM))
        return self

    def click_rub_account(self):
        self.wait.until(EC.element_to_be_clickable(self.RUB_CARD)).click()
        self.wait.until(EC.visibility_of_element_located(self.CARD_INPUT))
        return self

    def enter_card_number(self, number):
        inp = self.wait.until(EC.visibility_of_element_located(self.CARD_INPUT))
        inp.clear()
        inp.send_keys(number)
        return self

    def enter_amount(self, amount):
        inp = self.wait.until(EC.visibility_of_element_located(self.AMOUNT_INPUT))
        inp.clear()
        inp.send_keys(str(amount))
        time.sleep(0.4)
        return self

    def get_balance_text(self):
        return self.driver.find_element(*self.RUB_SUM).text

    def get_reserved_text(self):
        return self.driver.find_element(*self.RUB_RESERVED).text

    def get_commission(self):
        return self.driver.find_element(*self.COMMISSION).text.strip()

    def is_transfer_btn_visible(self):
        buttons = self.driver.find_elements(*self.TRANSFER_BTN)
        return any(b.is_displayed() for b in buttons)

    def is_error_visible(self):
        errors = self.driver.find_elements(*self.ERROR_MSG)
        return any(e.is_displayed() for e in errors)

    def is_amount_form_visible(self):
        fields = self.driver.find_elements(*self.AMOUNT_INPUT)
        return any(f.is_displayed() for f in fields)
