"""
Тесты на найденные баги — все должны падать пока баги не исправлены.
Каждый тест воспроизводит один конкретный дефект из docs/bug_reports/.
"""

import pytest


@pytest.mark.bug
def test_tc04_commission_calculation(page):
    """
    TC-04 [bug_004]: комиссия 10% должна округляться до рубля.
    Код использует Math.floor(O/100)*10 — округляет до 10 рублей.
    Сумма 150 → ожидаем 15 ₽, получаем 10 ₽.
    """
    page.open(balance=30000, reserved=0)
    page.click_rub_account()
    page.enter_card_number("1111222233334444")
    page.enter_amount(150)

    commission = page.get_commission()
    assert commission == "15", (
        f"Неверная комиссия: ожидали 15 ₽, получили {commission} ₽. "
        f"Баг в формуле: Math.floor(O/100)*10 вместо Math.floor(O/10)."
    )


@pytest.mark.bug
def test_tc05_boundary_condition(page):
    """
    TC-05 [bug_003]: когда сумма + комиссия равна доступному остатку — перевод должен работать.
    Код использует > 0 вместо >= 0, поэтому граничный случай отклоняется.
    balance=1100, reserved=0, amount=1000, commission=100 → 1000+100=1100=остаток.
    """
    page.open(balance=1100, reserved=0)
    page.click_rub_account()
    page.enter_card_number("1111222233334444")
    page.enter_amount(1000)

    assert page.is_transfer_btn_visible(), (
        "Кнопка «Перевести» не появилась, хотя сумма+комиссия = доступный остаток. "
        "Баг: условие A использует > 0 вместо >= 0."
    )


@pytest.mark.bug
def test_tc06_card_accepts_17_digits(page):
    """
    TC-06 [bug_001]: поле карты должно принимать ровно 16 цифр.
    При вводе 17 цифр форма суммы не должна открываться.
    Код обрезает до 17 (L.length > 17) вместо 16.
    """
    page.open(balance=30000, reserved=0)
    page.click_rub_account()
    page.enter_card_number("12345678901234567")  # 17 цифр

    assert not page.is_amount_form_visible(), (
        "Форма суммы открылась при вводе 17 цифр карты. "
        "Баг: код обрезает до 17 (L.length > 17) вместо 16, "
        "и показывает форму при y.length >= 16 вместо === 16."
    )


@pytest.mark.bug
def test_tc07_negative_amount_accepted(page):
    """
    TC-07 [bug_002]: отрицательная сумма перевода не должна проходить валидацию.
    Код сохраняет знак минус, комиссия становится отрицательной,
    и условие доступности всегда выполняется.
    """
    page.open(balance=30000, reserved=20001)
    page.click_rub_account()
    page.enter_card_number("1111222233334444")
    page.enter_amount(-100)

    assert not page.is_transfer_btn_visible(), (
        "Кнопка «Перевести» появилась при отрицательной сумме -100 ₽. "
        "Баг: код сохраняет минус → комиссия -10 ₽ → условие доступности всегда true."
    )
