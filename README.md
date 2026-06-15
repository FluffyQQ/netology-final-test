# F-Bank — итоговое задание по тестированию ПО

Студент: Эванс Максим, 2 курс  
Дисциплина: Тестирование прикладного ПО  
Дата: 2026-06-15

Тестируется учебное SPA-приложение «F-Bank» (Fake money, Real Bugs) — имитация банковских переводов с рублёвого счёта.

CI-сборка падает намеренно: в приложении найдено 4 дефекта, на каждый написан автотест.

---
## Шаги выполнения задания

### Шаг 1. Ручное тестирование
Подготовлено 7 ручных тест-кейсов в `docs/test_cases.md`, из них минимум 2 выявляют разные дефекты.

### Шаг 2. Автоматизированное тестирование
Настроен GitHub CI на запуск Selenium-тестов. Сборка красная по design из-за тестов на найденные дефекты (`pytest -m bug`).

### Шаг 3. Проверка работы
Репозиторий подготовлен для публикации и передачи ссылки на проверку преподавателю.

### Чек-лист
- найдено минимум 2 дефекта;
- на каждый дефект оформлен отдельный баг-репорт;
- на каждый дефект добавлен один автоматизированный тест;
- проект готов к передаче ссылкой на публичный GitHub-репозиторий.

---

## Что внутри

| Артефакт | Где |
|----------|-----|
| Приложение (dist) | `dist/` |
| Тест-кейсы (7 штук) | `docs/test_cases.md` |
| Баг-репорты (4 штуки) | `docs/bug_reports/` |
| Page Object | `tests/pages/bank_page.py` |
| Smoke-тесты (зелёные) | `tests/test_smoke.py` |
| Тесты на баги (красные) | `tests/test_bugs.py` |
| GitHub Actions | `.github/workflows/ci.yml` |

---

## Быстрый старт

### Запустить приложение

```bash
cd dist
python3 -m http.server 8000
```

Открыть: `http://localhost:8000/?balance=30000&reserved=20001`

### Запустить тесты

```bash
pip install -r requirements.txt

pytest -v                    # все тесты
pytest -m smoke              # только smoke (зелёные)
pytest -m bug                # только баги (красные)
```

---

## Найденные дефекты

| ID | Заголовок | Severity | Тест |
|----|-----------|----------|------|
| [bug_001](docs/bug_reports/bug_001_card_17digits.md) | Поле карты принимает 17 цифр вместо 16 | Major | `test_tc06_card_accepts_17_digits` |
| [bug_002](docs/bug_reports/bug_002_negative_amount.md) | Отрицательная сумма принимается, кнопка «Перевести» активна | **Critical** | `test_tc07_negative_amount_accepted` |
| [bug_003](docs/bug_reports/bug_003_boundary.md) | Off-by-one: `>` вместо `>=` блокирует граничный перевод | Major | `test_tc05_boundary_condition` |
| [bug_004](docs/bug_reports/bug_004_commission.md) | Комиссия округляется до 10 ₽ вместо 1 ₽ | Major | `test_tc04_commission_calculation` |

Подробные баг-репорты — в папке `docs/bug_reports/`.

---

## Тест-кейсы

Все 7 тест-кейсов — в файле `docs/test_cases.md`.

| ID | Тип | Статус |
|----|-----|--------|
| TC-01 | Smoke / Positive | ✅ PASS |
| TC-02 | Smoke / Positive | ✅ PASS |
| TC-03 | Smoke / Negative | ✅ PASS |
| TC-04 | Bug / Calculation | ❌ FAIL — bug_004 |
| TC-05 | Bug / Boundary | ❌ FAIL — bug_003 |
| TC-06 | Bug / Validation | ❌ FAIL — bug_001 |
| TC-07 | Bug / Validation | ❌ FAIL — bug_002 |

---

## Результат прогона

```
3 passed (smoke), 4 failed (bug) — CI красный by design
```

---

## Стек

- Python 3.11
- pytest 8.2
- Selenium 4.21
- Chrome headless
- GitHub Actions
