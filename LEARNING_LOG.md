# LEARNING LOG — qa-auto-framework

## Warm-up log
<!-- Формат строки: YYYY-MM-DD: W01, W07, W13 -->
<!-- Ментор дописывает строку в конце каждой сессии (в блоке SESSION SUMMARY) -->
<!-- Записи до 2026-06-15 включительно отсутствуют — банк вопросов введён позже, -->
<!-- в эти сессии warm-up по фиксированному банку не использовался -->

- 2026-06-15: W06, W07, W13
- 2026-06-23: W14, W20, W21
- 2026-06-24: W17, W20, W11

---

## История сессий

### 2026-07-01 — pre-commit code review, PEP8, AAA-паттерн
**Тема:** визуальный стиль кода, PEP8, AAA-паттерн в тестах

- Pre-commit review: 5/5 тестов зелёные, проект готов к коммиту
- PEP8: два разрыва перед top-level функцией, два разрыва между функциями в тест-файле
- Отступы в dict: содержимое словаря на один уровень глубже открывающей скобки (8 пробелов внутри функции)
- AAA-паттерн: пустая строка разделяет фазы (Arrange / Act / Assert), не отдельные строки внутри фазы; между assert-ами пустых строк нет
- Мёртвая переменная: `before` в `test_put_booking` заменена на `_`, т.к. не использовалась

**Ошибки:**
- Trailing whitespace после `:` в def — не виден глазом, но ловится линтером и git diff
- Отступ `"additionalneeds"` выровнен по закрывающей `}` вложенного dict вместо уровня родительского dict — перепутаны уровни вложенности
- Три пустые строки после импортов вместо двух — не замечено до ревью

**Следующий шаг:** параметризация — `@pytest.mark.parametrize` для PATCH/PUT

---

### 2026-07-01 — PATCH/PUT закрыты, 5 тестов зелёные
**Тема:** finalize test_patch_booking, test_put_booking, mutation check

- `models/__init__.py` — добавлен импорт `Booking`, `BookingDates`
- `patch_booking` и `put_booking` добавлены в `BookingClient`: Cookie-авторизация, `json=payload`, возвращают `Response`
- `test_patch_booking`: антизатирание — патчим `lastname`, проверяем изменение + все остальные поля не затёрты, даты через `date.fromisoformat()`
- `test_put_booking`: полная замена ресурса — `new_payload` через `generate_booking_payload()`, сравнение `after.model_dump(mode="json") == new_payload`
- Mutation check для обоих тестов пройден; все 5 тестов зелёные

**Следующий шаг:** параметризация — `@pytest.mark.parametrize` для PATCH/PUT с несколькими полями и значениями

---


### 2026-06-24 — PATCH закрыт, PUT в работе
**Тема:** финализация test_patch_booking, разбор test suite, следующий шаг — PUT

- PATCH-тест финализирован: `before = Booking(**before_dict)`, добавлен `assert after.lastname != res.lastname` — закрывает дыру «зелёный, но слепой»
- 4/4 тестов зелёные
- PUT отличается от PATCH: заменяет ресурс целиком → payload полный → один ассерт `assert after == expected` вместо пяти отдельных
- `put_booking` в клиенте отсутствует — следующий шаг: написать метод, затем тест

**Следующий шаг:** `put_booking` в клиенте → `test_put_booking`

---

### 2026-06-24 — PATCH: клиент, Response-объект, тест с антизатиранием
**Тема:** patch_booking в клиенте, requests.Response как объект-обёртка, паттерн read-after-write, PATCH-тест с антизатиранием

- `patch_booking(booking_id, payload, token) -> Response`: тело через `json=payload`, авторизация `Cookie: token=...` (как DELETE), `return response`
- `Content-Type` руками не ставим — `json=` сериализует dict и сам проставляет заголовок
- `requests.Response` — «конверт» с ответом: `.status_code`, `.json()`, `.text`, `.headers`; клиент возвращает конверт целиком, распаковывает вызывающий код
- Теория PATCH-теста: **антизатирание** (PATCH меняет только переданные поля, не трогает соседние), **read-after-write** (after берём независимым GET, не из тела ответа)
- `test_patch_booking`: arrange (before-модель `Booking(**data)`) → act → assert 200 → GET → assert изменилось + assert не затёрто

**Ошибки:**
- Трижды путал тип возврата метода клиента (`-> str`, `-> dict`) с типом распарсенного тела. Root cause: не разделял «что клиент возвращает» и «как тест читает тело»
- `Content-Type` в запросе описывает тело запроса (что шлёшь), не формат ответа — и при `json=` его вообще не нужно ставить руками
- `before` из фикстуры — это `dict` (Faker payload), не модель; `before.firstname` на dict = `AttributeError`. Решение: `before = Booking(**data)`
- Дыра «зелёный, но слепой»: если Faker сгенерил `lastname="Morgan"`, ассерт `== "Morgan"` ничего не доказывает. Нужен `after.lastname != before.lastname`

**Следующий шаг:** финализировать PATCH-тест (добавить before-модель и ассерт на реальное изменение), прогнать pytest, затем PUT-тест

---

### 2026-06-23 — GET round-trip, Pydantic date type
**Тема:** закрытие GET теста, Pydantic валидация дат, model_dump(mode='json')
- Убран ложный `.pop("additionalneeds")` — поле возвращалось корректно, workaround был основан на гипотезе, не на наблюдении
- `BookingDates.checkin/checkout`: тип изменён с `str` на `date` — Pydantic теперь бросает ValidationError на невалидную дату
- Сравнение починено через `model_dump(mode='json')` — сериализует `date` обратно в строку, оба словаря приводятся к одному типу

**Ошибки:**
- `.pop("additionalneeds")` убран на основании предположения «могло флакать» без воспроизведения реального падения — антипаттерн: never silence a field without proven cause
- `str` для date-полей в модели — произошло случайно, не осознанно; потеря валидации формата дат
- Поиск в документации Pydantic заменён на ответ Claude — навык читать доку не отработан

**Следующий шаг:** PUT/PATCH тесты

---

### 2026-06-12
**Тема:** окружения, Git/GitHub, терминал, промпт v3
- Промпт переработан до v3 (фазы вместо процентов, метрики по темам)
- Claude Code: установка, VS Code, CLAUDE.md, --continue
- Git: root cause «блокировок» — опечатка `git.com` в remote; SSH через порт 443
- Терминал: nano, which, hash -r, mv, ls -a
- Окружения: `python -m venv` vs `source activate` vs `pip install -r`; pyenv shims; `python -m pytest`
- `.gitignore` и `requirements.txt` с фиксацией версий; тесты framework зелёные (2 passed)

### 2026-06-15 — models/fixtures layer
**Тема:** Pydantic models, fixtures (auth_token, booking)
- models layer закрыт: Auth, Booking, BookingDates (nested model)
- fixtures layer: `auth_token` (scope=session), `booking` (yield + teardown)
- первые тесты: `test_auth_token`, `test_delete_booking`

**Ошибки:**
- DELETE летел дважды — тест вызывал `delete_booking` вручную, хотя fixture уже делает это в teardown. Root cause: не увидел, что fixture = setup + cleanup
- Мёртвые импорты в `test_auth.py` (`import requests`, `from config import BASE_URL`) — копипаст без чистки

### 2026-06-15 — utils layer (продолжение)
**Тема:** Faker, генерация тестовых данных
- `generate_booking_payload()` с Faker — рандомные firstname/lastname/totalprice/additionalneeds
- Даты через `date_between` с инвариантом `checkout > checkin` через `timedelta`
- `Faker()` инициализирован на уровне модуля, не внутри функции — один объект на сессию вместо N
- `strftime("%Y-%m-%d")` для конвертации `date` → строку
- `test_delete_booking` переписан без fixture `booking` — тест сам создаёт и удаляет бронирование
- `requirements.txt` обновлён через `pip freeze`

**Ошибки:**
- Trailing comma после `fake.date_between(...),` — `checkin` стал `tuple` вместо `date`
- `response = booking_id` в fixture до вызова DELETE — непонимание порядка `setup → yield → тест → teardown
