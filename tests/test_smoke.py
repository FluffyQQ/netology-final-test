"""
Smoke-тесты — базовые проверки что сервис вообще работает.
Все тесты должны быть зелёными.
"""

import pytest


@pytest.mark.smoke
def test_tc01_balance_from_url(page):
    """TC-01: баланс и резерв берутся из параметров URL."""
    page.open(balance=30000, reserved=20001)

    assert page.get_balance_text() == "30'000"
    assert page.get_reserved_text() == "20'001"


@pytest.mark.smoke
def test_tc02_transfer_form_opens(page):
    """TC-02: форма перевода появляется после клика на рублёвый счёт."""
    page.open(balance=30000, reserved=0)
    page.click_rub_account()

    # проверяем что поле ввода карты видно
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    inp = page.wait.until(
        EC.visibility_of_element_located(
            (By.XPATH, "//input[@placeholder='0000 0000 0000 0000']")
        )
    )
    assert inp.is_displayed()


@pytest.mark.smoke
def test_tc03_insufficient_funds_error(page):
    """TC-03: при превышении доступного остатка показывается ошибка."""
    page.open(balance=1000, reserved=0)
    page.click_rub_account()
    page.enter_card_number("1111222233334444")
    page.enter_amount(2000)

    assert page.is_error_visible(), "Сообщение об ошибке не появилось"
    assert not page.is_transfer_btn_visible(), "Кнопка перевода не должна быть видна"
