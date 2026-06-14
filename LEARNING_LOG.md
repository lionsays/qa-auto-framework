SESSION SUMMARY — 12.06.2026
Закрыто:

Промпт-пакет переработан до v3 (фазы вместо процентов, метрики по темам, правила про код/версии/термины)
Claude Code: установка, запуск в VS Code, CLAUDE.md в репозитории, разница сессий терминал/расширение, --continue
Git/GitHub: найден root cause «блокировок» — опечатка git.com в remote; SSH через порт 443 (~/.ssh/config); чтение git status глазами; git mv; правка remote через set-url
Терминал: nano/Pico (Ctrl+O → Enter → Ctrl+X), which, hash -r, mv, ls -a, чтение ошибок до конца
Окружения — главная тема дня: python -m venv (создать) vs source activate (включить) vs pip install -r (наполнить); флаги -m (module) и -r (requirements); pyenv shims и перехват команд; python -m pytest как надёжная форма; чтение шапки pytest (интерпретатор, плагины) как диагностика
.gitignore написан осознанно, без дублей; requirements.txt с фиксацией версий; закрыт старый хвост — тесты framework зелёные в чистом .venv (2 passed)