SESSION SUMMARY — 15.06.2026 (продолжение)
Закрыто:
utils layer: generate_booking_payload() с Faker — firstname, lastname, totalprice, additionalneeds рандомные; даты через date_between с инвариантом checkout > checkin через timedelta; Faker() инициализируется на уровне модуля (не внутри функции) — один объект на всю сессию вместо N; strftime("%Y-%m-%d") для конвертации date → строку.
test_delete_booking переписан без fixture booking — тест сам создаёт бронирование и удаляет, fixture больше не дублирует DELETE.
requirements.txt обновлён через pip freeze.

Ошибки и root cause:
Запятая после fake.date_between(...), — checkin стал кортежем вместо date. Root cause: невнимательность к синтаксису Python, где trailing comma создаёт tuple.
response = booking_id в fixture — попытка сохранить DELETE response до того, как DELETE был вызван. Root cause: непонимание порядка выполнения fixture (setup → yield → тест → teardown). DELETE response недоступен в yield, потому что происходит после теста.

Следующий шаг: новые тесты — GET, PUT/PATCH эндпоинты

---

SESSION SUMMARY — 15.06.2026
Закрыто:
fixtures layer: auth_token (scope=session — один токен на всю сессию), booking (yield + teardown: create_booking → yield id → delete_booking в cleanup)
первые тесты внутри framework: test_auth_token (Pydantic-валидация Auth модели), test_delete_booking (DELETE-эндпоинт)
models layer: закрыт (Auth, Booking, BookingDates nested model)

Ошибки и root cause:
test_delete_booking вызывает client.delete_booking вручную — но booking-fixture уже делает delete в teardown. В итоге DELETE летит дважды: тест удаляет бронирование, потом fixture пытается удалить уже несуществующий ресурс. Root cause: не увидел, что fixture — это не только setup, но и cleanup. Правило: если fixture делает teardown, тест не должен дублировать это действие.
В test_auth.py висят мёртвые импорты (import requests, from config import BASE_URL) — код не используется. Root cause: копипаст без чистки. В production это замусоривает namespace и вводит в заблуждение читателя.

Следующий шаг: utils layer

---

SESSION SUMMARY — 12.06.2026
Закрыто:

Промпт-пакет переработан до v3 (фазы вместо процентов, метрики по темам, правила про код/версии/термины)
Claude Code: установка, запуск в VS Code, CLAUDE.md в репозитории, разница сессий терминал/расширение, --continue
Git/GitHub: найден root cause «блокировок» — опечатка git.com в remote; SSH через порт 443 (~/.ssh/config); чтение git status глазами; git mv; правка remote через set-url
Терминал: nano/Pico (Ctrl+O → Enter → Ctrl+X), which, hash -r, mv, ls -a, чтение ошибок до конца
Окружения — главная тема дня: python -m venv (создать) vs source activate (включить) vs pip install -r (наполнить); флаги -m (module) и -r (requirements); pyenv shims и перехват команд; python -m pytest как надёжная форма; чтение шапки pytest (интерпретатор, плагины) как диагностика
.gitignore написан осознанно, без дублей; requirements.txt с фиксацией версий; закрыт старый хвост — тесты framework зелёные в чистом .venv (2 passed)