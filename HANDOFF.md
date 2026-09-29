# AI Orchestrator — передача проекта

Единый файл для продолжения работы над проектом: цель, принятые решения,
полный код всех файлов, команды запуска и список незакрытых задач.

**Версия:** 1.0.0 · **Python:** 3.11+ · **Объём:** ~12 100 строк в 62 модулях
**Состояние:** все девять этапов MVP реализованы. Ядро покрыто смоук-тестами
(37 проверок), интерфейс — сквозным сценарием на реальных виджетах
(34 проверки, 	ests/ui_smoke.py). Сценарий проверен на Windows 11,
PySide6 6.11, в том числе на HiDPI.

---

## Цель проекта

Десктопное приложение, в котором несколько ИИ-агентов совместно работают над
задачей пользователя под контролем ИИ-супервайзера. Всё хранится локально,
пользователь подключает собственные API-ключи.

Ключевые свойства, заданные постановкой задачи:

1. **Локальность.** Данные, ключи и переписка не покидают устройство.
   SQLite для базы, файловая система для рабочих файлов и выгрузок.
   Локальная авторизация с несколькими профилями на одном устройстве.
2. **Свои ключи, любые провайдеры.** Пресеты для OpenAI, Anthropic, Gemini,
   Groq, OpenRouter, Ollama, Hugging Face и произвольного
   OpenAI-совместимого endpoint. Количество агентов не ограничено.
3. **Изоляция агентов.** Агенты не видят промптов и переписки друг друга.
   Единственный канал обмена — анонимная сводка супервайзера, которая
   рассылается без указания авторов, чтобы не возникало «слепого доверия
   авторитету».
4. **Супервайзер.** Проверяет отчёты по чек-листу, возвращает работу на
   доработку, находит противоречия между результатами, эскалирует
   нерешаемое пользователю.
5. **Human-in-the-loop.** В критических точках система останавливается и
   ждёт решения человека.
6. **Наблюдаемость и контроль расхода.** Дашборд реального времени,
   лимиты по токенам и деньгам на трёх уровнях с алертами.
7. **Гибкий результат.** Формат выгрузки зависит от типа задачи:
   Markdown, DOCX, PDF или ZIP с файлами кода.

---

## Содержание кода

**Точка входа и конфигурация**

- `main.py`
- `app/config.py`
- `app/i18n.py`

**Хранилище**

- `storage/schema.sql`
- `storage/db.py`
- `storage/models.py`
- `storage/repositories.py`

**Безопасность**

- `core/security/crypto.py`

**Провайдеры моделей**

- `providers/base.py`
- `providers/presets.py`
- `providers/openai_compat.py`
- `providers/anthropic_provider.py`
- `providers/gemini_provider.py`
- `providers/factory.py`
- `providers/pricing.json`

**Инструменты агентов**

- `core/tools/base.py`
- `core/tools/sandbox.py`
- `core/tools/code_exec.py`
- `core/tools/files.py`
- `core/tools/web_search.py`

**Ядро: агенты, оркестратор, супервайзер**

- `core/events.py`
- `core/agents/roles.py`
- `core/agents/runner.py`
- `core/orchestrator.py`
- `core/planner.py`
- `core/supervisor/checklist.py`
- `core/supervisor/supervisor.py`
- `core/hitl.py`
- `core/budget.py`

**Экспорт результата**

- `core/export/bundle.py`
- `core/export/exporters.py`

**Интерфейс**

- `ui/theme.py`
- `ui/widgets/common.py`
- `ui/widgets/charts.py`
- `ui/widgets/approval_panel.py`
- `ui/login_window.py`
- `ui/main_window.py`
- `ui/pages/workspaces_page.py`
- `ui/pages/keys_page.py`
- `ui/pages/agents_page.py`
- `ui/pages/task_page.py`
- `ui/pages/run_page.py`
- `ui/pages/supervisor_page.py`
- `ui/pages/dashboard_page.py`
- `ui/pages/budget_page.py`
- `ui/pages/export_page.py`
- `ui/pages/settings_page.py`

**Служебное**

- `utils/asyncutils.py`
- `utils/logging_setup.py`
- `tests/smoke.py`
- `tests/ui_smoke.py`

**Сборка и запуск**

- `requirements.txt`
- `run.sh`
- `run.bat`
- `.gitignore`

Файлы `__init__.py` содержат только строку документации и здесь не приводятся:

- `.venv\Lib\site-packages\PIL\__init__.py`
- `.venv\Lib\site-packages\PySide6\QtAsyncio\__init__.py`
- `.venv\Lib\site-packages\PySide6\__init__.py`
- `.venv\Lib\site-packages\PySide6\scripts\__init__.py`
- `.venv\Lib\site-packages\PySide6\scripts\deploy_lib\__init__.py`
- `.venv\Lib\site-packages\PySide6\scripts\project_lib\__init__.py`
- `.venv\Lib\site-packages\PySide6\support\__init__.py`
- `.venv\Lib\site-packages\_distutils_hack\__init__.py`
- `.venv\Lib\site-packages\anyio\__init__.py`
- `.venv\Lib\site-packages\anyio\_backends\__init__.py`
- `.venv\Lib\site-packages\anyio\_core\__init__.py`
- `.venv\Lib\site-packages\anyio\abc\__init__.py`
- `.venv\Lib\site-packages\anyio\streams\__init__.py`
- `.venv\Lib\site-packages\babel\__init__.py`
- `.venv\Lib\site-packages\babel\localtime\__init__.py`
- `.venv\Lib\site-packages\babel\messages\__init__.py`
- `.venv\Lib\site-packages\backports\__init__.py`
- `.venv\Lib\site-packages\backports\tarfile\__init__.py`
- `.venv\Lib\site-packages\backports\tarfile\compat\__init__.py`
- `.venv\Lib\site-packages\bs4\__init__.py`
- `.venv\Lib\site-packages\bs4\builder\__init__.py`
- `.venv\Lib\site-packages\certifi\__init__.py`
- `.venv\Lib\site-packages\certifi\tests\__init__.py`
- `.venv\Lib\site-packages\cffi\__init__.py`
- `.venv\Lib\site-packages\charset_normalizer\__init__.py`
- `.venv\Lib\site-packages\charset_normalizer\cli\__init__.py`
- `.venv\Lib\site-packages\click\__init__.py`
- `.venv\Lib\site-packages\courlan\__init__.py`
- `.venv\Lib\site-packages\cryptography\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\asn1\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\backends\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\backends\openssl\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\bindings\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\bindings\openssl\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\decrepit\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\decrepit\ciphers\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\primitives\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\primitives\asymmetric\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\primitives\ciphers\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\primitives\kdf\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\primitives\serialization\__init__.py`
- `.venv\Lib\site-packages\cryptography\hazmat\primitives\twofactor\__init__.py`
- `.venv\Lib\site-packages\cryptography\x509\__init__.py`
- `.venv\Lib\site-packages\dateparser\__init__.py`
- `.venv\Lib\site-packages\dateparser\calendars\__init__.py`
- `.venv\Lib\site-packages\dateparser\custom_language_detection\__init__.py`
- `.venv\Lib\site-packages\dateparser\data\__init__.py`
- `.venv\Lib\site-packages\dateparser\data\date_translation_data\__init__.py`
- `.venv\Lib\site-packages\dateparser\languages\__init__.py`
- `.venv\Lib\site-packages\dateparser\search\__init__.py`
- `.venv\Lib\site-packages\dateparser\utils\__init__.py`
- `.venv\Lib\site-packages\dateparser_cli\__init__.py`
- `.venv\Lib\site-packages\dateparser_data\__init__.py`
- `.venv\Lib\site-packages\dateparser_scripts\__init__.py`
- `.venv\Lib\site-packages\dateutil\__init__.py`
- `.venv\Lib\site-packages\dateutil\parser\__init__.py`
- `.venv\Lib\site-packages\dateutil\tz\__init__.py`
- `.venv\Lib\site-packages\dateutil\zoneinfo\__init__.py`
- `.venv\Lib\site-packages\ddgs\__init__.py`
- `.venv\Lib\site-packages\ddgs\api_server\__init__.py`
- `.venv\Lib\site-packages\ddgs\engines\__init__.py`
- `.venv\Lib\site-packages\docx\__init__.py`
- `.venv\Lib\site-packages\docx\dml\__init__.py`
- `.venv\Lib\site-packages\docx\drawing\__init__.py`
- `.venv\Lib\site-packages\docx\enum\__init__.py`
- `.venv\Lib\site-packages\docx\image\__init__.py`
- `.venv\Lib\site-packages\docx\opc\__init__.py`
- `.venv\Lib\site-packages\docx\opc\parts\__init__.py`
- `.venv\Lib\site-packages\docx\oxml\__init__.py`
- `.venv\Lib\site-packages\docx\oxml\text\__init__.py`
- `.venv\Lib\site-packages\docx\parts\__init__.py`
- `.venv\Lib\site-packages\docx\styles\__init__.py`
- `.venv\Lib\site-packages\docx\text\__init__.py`
- `.venv\Lib\site-packages\h11\__init__.py`
- `.venv\Lib\site-packages\htmldate\__init__.py`
- `.venv\Lib\site-packages\httpcore\__init__.py`
- `.venv\Lib\site-packages\httpcore\_async\__init__.py`
- `.venv\Lib\site-packages\httpcore\_backends\__init__.py`
- `.venv\Lib\site-packages\httpcore\_sync\__init__.py`
- `.venv\Lib\site-packages\httpx\__init__.py`
- `.venv\Lib\site-packages\httpx\_transports\__init__.py`
- `.venv\Lib\site-packages\idna\__init__.py`
- `.venv\Lib\site-packages\importlib_metadata\__init__.py`
- `.venv\Lib\site-packages\importlib_metadata\compat\__init__.py`
- `.venv\Lib\site-packages\jaraco\classes\__init__.py`
- `.venv\Lib\site-packages\jaraco\context\__init__.py`
- `.venv\Lib\site-packages\jaraco\functools\__init__.py`
- `.venv\Lib\site-packages\justext\__init__.py`
- `.venv\Lib\site-packages\keyring\__init__.py`
- `.venv\Lib\site-packages\keyring\backends\__init__.py`
- `.venv\Lib\site-packages\keyring\backends\macOS\__init__.py`
- `.venv\Lib\site-packages\keyring\compat\__init__.py`
- `.venv\Lib\site-packages\keyring\testing\__init__.py`
- `.venv\Lib\site-packages\keyring\util\__init__.py`
- `.venv\Lib\site-packages\lxml\__init__.py`
- `.venv\Lib\site-packages\lxml\html\__init__.py`
- `.venv\Lib\site-packages\lxml\includes\__init__.py`
- `.venv\Lib\site-packages\lxml\includes\extlibs\__init__.py`
- `.venv\Lib\site-packages\lxml\includes\libexslt\__init__.py`
- `.venv\Lib\site-packages\lxml\includes\libxml\__init__.py`
- `.venv\Lib\site-packages\lxml\includes\libxslt\__init__.py`
- `.venv\Lib\site-packages\lxml\isoschematron\__init__.py`
- `.venv\Lib\site-packages\lxml_html_clean\__init__.py`
- `.venv\Lib\site-packages\more_itertools\__init__.py`
- `.venv\Lib\site-packages\pip\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\build_env\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\cli\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\commands\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\distributions\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\index\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\locations\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\metadata\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\metadata\importlib\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\models\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\network\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\operations\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\operations\build\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\operations\install\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\req\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\resolution\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\resolution\legacy\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\resolution\resolvelib\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\utils\__init__.py`
- `.venv\Lib\site-packages\pip\_internal\vcs\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\cachecontrol\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\cachecontrol\caches\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\certifi\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\distlib\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\distro\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\idna\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\msgpack\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\packaging\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\packaging\licenses\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\pkg_resources\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\platformdirs\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\pygments\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\pygments\filters\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\pygments\formatters\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\pygments\lexers\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\pygments\styles\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\pyproject_hooks\_in_process\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\requests\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\resolvelib\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\resolvelib\resolvers\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\rich\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\tomli\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\tomli_w\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\truststore\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\urllib3\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\urllib3\contrib\emscripten\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\urllib3\http2\__init__.py`
- `.venv\Lib\site-packages\pip\_vendor\urllib3\util\__init__.py`
- `.venv\Lib\site-packages\pkg_resources\__init__.py`
- `.venv\Lib\site-packages\pkg_resources\_vendor\__init__.py`
- `.venv\Lib\site-packages\pkg_resources\_vendor\importlib_resources\__init__.py`
- `.venv\Lib\site-packages\pkg_resources\_vendor\jaraco\__init__.py`
- `.venv\Lib\site-packages\pkg_resources\_vendor\jaraco\text\__init__.py`
- `.venv\Lib\site-packages\pkg_resources\_vendor\more_itertools\__init__.py`
- `.venv\Lib\site-packages\pkg_resources\_vendor\packaging\__init__.py`
- `.venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\__init__.py`
- `.venv\Lib\site-packages\pkg_resources\_vendor\pyparsing\diagram\__init__.py`
- `.venv\Lib\site-packages\pkg_resources\extern\__init__.py`
- `.venv\Lib\site-packages\primp\__init__.py`
- `.venv\Lib\site-packages\pycparser\__init__.py`
- `.venv\Lib\site-packages\pytz\__init__.py`
- `.venv\Lib\site-packages\qasync\__init__.py`
- `.venv\Lib\site-packages\regex\__init__.py`
- `.venv\Lib\site-packages\reportlab\__init__.py`
- `.venv\Lib\site-packages\reportlab\graphics\__init__.py`
- `.venv\Lib\site-packages\reportlab\graphics\barcode\__init__.py`
- `.venv\Lib\site-packages\reportlab\graphics\charts\__init__.py`
- `.venv\Lib\site-packages\reportlab\graphics\samples\__init__.py`
- `.venv\Lib\site-packages\reportlab\graphics\widgets\__init__.py`
- `.venv\Lib\site-packages\reportlab\lib\__init__.py`
- `.venv\Lib\site-packages\reportlab\pdfbase\__init__.py`
- `.venv\Lib\site-packages\reportlab\pdfgen\__init__.py`
- `.venv\Lib\site-packages\reportlab\platypus\__init__.py`
- `.venv\Lib\site-packages\setuptools\__init__.py`
- `.venv\Lib\site-packages\setuptools\_distutils\__init__.py`
- `.venv\Lib\site-packages\setuptools\_distutils\command\__init__.py`
- `.venv\Lib\site-packages\setuptools\_vendor\__init__.py`
- `.venv\Lib\site-packages\setuptools\_vendor\importlib_metadata\__init__.py`
- `.venv\Lib\site-packages\setuptools\_vendor\importlib_resources\__init__.py`
- `.venv\Lib\site-packages\setuptools\_vendor\jaraco\__init__.py`
- `.venv\Lib\site-packages\setuptools\_vendor\jaraco\text\__init__.py`
- `.venv\Lib\site-packages\setuptools\_vendor\more_itertools\__init__.py`
- `.venv\Lib\site-packages\setuptools\_vendor\packaging\__init__.py`
- `.venv\Lib\site-packages\setuptools\_vendor\pyparsing\__init__.py`
- `.venv\Lib\site-packages\setuptools\_vendor\pyparsing\diagram\__init__.py`
- `.venv\Lib\site-packages\setuptools\_vendor\tomli\__init__.py`
- `.venv\Lib\site-packages\setuptools\command\__init__.py`
- `.venv\Lib\site-packages\setuptools\config\__init__.py`
- `.venv\Lib\site-packages\setuptools\config\_validate_pyproject\__init__.py`
- `.venv\Lib\site-packages\setuptools\extern\__init__.py`
- `.venv\Lib\site-packages\shiboken6\__init__.py`
- `.venv\Lib\site-packages\soupsieve\__init__.py`
- `.venv\Lib\site-packages\tld\__init__.py`
- `.venv\Lib\site-packages\tld\tests\__init__.py`
- `.venv\Lib\site-packages\trafilatura\__init__.py`
- `.venv\Lib\site-packages\tzdata\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Africa\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\America\Argentina\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\America\Indiana\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\America\Kentucky\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\America\North_Dakota\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\America\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Antarctica\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Arctic\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Asia\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Atlantic\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Australia\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Brazil\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Canada\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Chile\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Etc\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Europe\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Indian\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Mexico\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\Pacific\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\US\__init__.py`
- `.venv\Lib\site-packages\tzdata\zoneinfo\__init__.py`
- `.venv\Lib\site-packages\tzlocal\__init__.py`
- `.venv\Lib\site-packages\urllib3\__init__.py`
- `.venv\Lib\site-packages\urllib3\contrib\__init__.py`
- `.venv\Lib\site-packages\urllib3\contrib\emscripten\__init__.py`
- `.venv\Lib\site-packages\urllib3\http2\__init__.py`
- `.venv\Lib\site-packages\urllib3\util\__init__.py`
- `.venv\Lib\site-packages\win32ctypes\__init__.py`
- `.venv\Lib\site-packages\win32ctypes\core\__init__.py`
- `.venv\Lib\site-packages\win32ctypes\core\cffi\__init__.py`
- `.venv\Lib\site-packages\win32ctypes\core\ctypes\__init__.py`
- `.venv\Lib\site-packages\win32ctypes\pywin32\__init__.py`
- `.venv\Lib\site-packages\win32ctypes\tests\__init__.py`
- `.venv\Lib\site-packages\zipp\__init__.py`
- `.venv\Lib\site-packages\zipp\compat\__init__.py`
- `app\__init__.py`
- `core\__init__.py`
- `core\agents\__init__.py`
- `core\export\__init__.py`
- `core\security\__init__.py`
- `core\supervisor\__init__.py`
- `core\tools\__init__.py`
- `providers\__init__.py`
- `storage\__init__.py`
- `tests\__init__.py`
- `ui\__init__.py`
- `ui\pages\__init__.py`
- `ui\widgets\__init__.py`
- `utils\__init__.py`

---


## Принятые решения

Эти развилки были согласованы до написания кода. Менять их можно, но каждая
тянет за собой остальное.

### Стек и платформа

**GUI — PySide6 (Qt).** Нативное окно на Windows, macOS и Linux без
веб-прослойки. Зрелые виджеты под плотные таблицы и дашборды, штатная
интеграция с asyncio через `qasync`, нормальная упаковка через PyInstaller.
Лицензия LGPL допускает закрытую дистрибуцию при динамической линковке.

**Параллелизм — один asyncio-луп.** Qt и asyncio объединены `qasync`, агенты
живут в нём как обычные таски. Пятнадцать агентов не превращаются в
пятнадцать потоков. Блокирующие операции (SQLite, библиотека поиска) уходят
в `asyncio.to_thread`, исполнение кода — в отдельный процесс или контейнер.

**Графики — собственная отрисовка на QPainter.** Не QtCharts и не pyqtgraph:
ноль дополнительных зависимостей, цвета сразу из активной темы приложения,
независимость от конкретной сборки PySide6.

### Безопасность

**Шифрование ключей.** `Argon2id(пароль профиля, соль)` даёт 32-байтовый
мастер-ключ, который живёт только в оперативной памяти. API-ключи шифруются
`AES-256-GCM`. База остаётся обычным SQLite, но секреты в ней нечитаемы.
Смена пароля перешифровывает все ключи. Пароль профиля и мастер-пароль —
одно и то же: одно поле при входе, и восстановления нет.

**Песочница — интерфейс с двумя реализациями.** `DockerSandbox`
(`--network none`, `--read-only`, лимиты памяти, CPU и PID, `--cap-drop ALL`)
используется, если Docker доступен. Иначе `SubprocessSandbox`: одноразовый
каталог, своя группа процессов, `RLIMIT_CPU/AS/FSIZE/NPROC`, вычищенное
окружение без ключей хоста, сеть отрезана. Второй режим — барьер по
умолчанию, а не полная изоляция, и приложение говорит об этом прямо
в настройках.

**Права на файлы.** Агент работает в каталоге своего воркспейса.
Дополнительные каталоги добавляет пользователь вручную. Проверка пути
централизована в `ToolContext.resolve` и отсекает `../`, абсолютные пути
и симлинки наружу.

### Логика работы

**Цикл агента — ReAct.** Модель думает, вызывает инструменты, получает
результат, продолжает. Остановка по одному из условий: выдан блок `RESULT:`,
кончились разрешённые шаги, исчерпан лимит токенов, пользователь нажал
«Стоп». Из ответа разбираются блок `RESULT:` и строка `CONFIDENCE: 0..1`.

**Лимит токенов на задачу** задаёт пользователь; пустое поле означает
отсутствие лимита.

**Супервайзер** работает либо на одном из подключённых API-ключей, либо на
локальной модели через Ollama (по умолчанию Qwen) — второй вариант
бесплатен и работает офлайн. Он может вернуть работу на доработку до
`max_rework_rounds` раз. Сводку для команды пересказывает своими словами,
имена агентов вычищаются пост-обработкой, а не только просьбой в промпте.

**Нечитаемый ответ супервайзера** трактуется как «нужна доработка», а не
«принято»: молча пропустить непроверенный отчёт хуже, чем перепроверить.
Но если супервайзер недоступен целиком, прогон не падает — отчёт
принимается, а пропуск проверки пишется в ленту.

**Решение человека важнее настройки.** `max_rework_rounds` ограничивает
автоматические доработки супервайзера. Когда доработку назначает человек,
выдаётся дополнительный круг сверх лимита — до трёх таких кругов, иначе
цикл «вернул — переделал — вернул» не заканчивался бы.

**Бюджеты проверяются до вызова модели**, а не после: узнавать о превышении
постфактум бессмысленно, деньги уже потрачены. Расход берётся из журнала
`usage_log`, а не из накопительных счётчиков, поэтому перезапуск приложения
не обнуляет израсходованный бюджет.

**Стоимость считается на клиенте** по таблице `providers/pricing.json`
(USD за миллион токенов, поиск по точному совпадению и по префиксу):
провайдеры почти никогда не возвращают цену, только токены. Для локальных
моделей стоимость равна нулю.

### Интерфейс

**Панель решений, а не модальное окно.** Вопросов human-in-the-loop может
быть несколько одновременно, если параллельно работают разные агенты.
Модалка заслоняла бы прогресс и ленту — ровно то, по чему принимается
решение.

**Локализация RU/EN** с переключателем, строки вынесены в словари
(232 ключа в каждом языке).

---


## Установка и запуск

### Быстрый способ

Windows — двойной щелчок по `run.bat`. Linux и macOS:

````bash
./run.sh
````

Скрипт проверит версию Python, создаст виртуальное окружение, поставит
зависимости и запустит приложение. Первый запуск — 2–5 минут.

### Вручную

````bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python main.py
````

Нужен **Python 3.11+**. Минимальный набор пакетов, если экспорт в DOCX и PDF
не нужен: `pip install PySide6 qasync httpx cryptography`.

### Системные зависимости на Linux

````bash
sudo apt install python3-venv python3-pip \
     libgl1 libegl1 libxkbcommon-x11-0 libdbus-1-3 \
     libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 \
     libxcb-randr0 libxcb-render-util0 libxcb-shape0 \
     fonts-dejavu
````

Пакет `fonts-dejavu` нужен для экспорта в PDF с кириллицей.

### Проверка ядра

````bash
python tests/smoke.py
````

Тесты не ходят в интернет и не тратят токены: модели подменяются фейковыми
провайдерами. Ожидаемый результат — `ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ: 37 из 37`.
Работают во временном каталоге, профиль пользователя не трогают.

### Проверка интерфейса

``bash
python tests/ui_smoke.py
``

Сквозной сценарий на настоящих виджетах: регистрация → воркспейс → ключ →
агенты → задача с автоматическим разбиением → прогон с паузой
human-in-the-loop → супервайзер, дашборд, бюджеты → экспорт во все четыре
формата → светлая тема → смена языка → выход и повторный вход. Модальные
окна подменяются заполнителями, модели — фейковым провайдером. Провалом
считается и любое исключение в слоте Qt или обработчике шины, даже если
приложение его проглотило. Ожидаемый результат —
ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ: 34 из 34.

По умолчанию окна не показываются (платформа offscreen), а скриншоты
каждого экрана складываются во временный каталог — путь печатается в конце.
--show запускает с настоящими окнами, --out DIR задаёт каталог скриншотов,
QT_SCALE_FACTOR=2 проверяет HiDPI.

Одно правило для тех, кто будет дописывать сценарий: не вызывайте
QApplication.processEvents() внутри корутины. Под qasync это повторный вход
в луп, и чужие таски падают с «Cannot enter into task». Давать интерфейсу
отрисоваться нужно через wait asyncio.sleep(...).

### Пересборка этого документа

Документ собирается скриптом из реальных файлов, поэтому не может разойтись
с кодом. После изменений выполните:

````bash
python make_handoff.py
````

### Каталог данных

| ОС | Путь |
|---|---|
| Windows | `%APPDATA%\ai-orchestrator` |
| macOS | `~/Library/Application Support/ai-orchestrator` |
| Linux | `~/.local/share/ai-orchestrator` |

Переопределяется переменной окружения `AIORC_HOME` — этим пользуются тесты.
Внутри: `app.db`, `logs/`, `workspaces/`, `exports/`, `settings.json`.

### Сборка в исполняемый файл

````bash
pip install pyinstaller
pyinstaller --name AIOrchestrator --windowed --onedir main.py \
  --add-data "storage/schema.sql:storage" \
  --add-data "providers/pricing.json:providers"
````

На Windows разделитель в `--add-data` — точка с запятой. Вариант `--onedir`
стартует заметно быстрее `--onefile`.

---


## Архитектура

### Слои

````
UI (PySide6)  →  Repos (единственная точка доступа к БД)  →  SQLite
     ↑                        ↑
     │                        │
EventBus  ←──  Orchestrator ──┴──  Providers (HTTP к моделям)
                   │
                   ├── AgentRunner    ReAct-цикл одного агента
                   ├── Supervisor     проверка, сводки, конфликты
                   ├── ApprovalGate   паузы human-in-the-loop
                   ├── BudgetGuard    лимиты трёх уровней
                   └── ToolRegistry   поиск, файлы, песочница
````

Ядро ничего не знает о Qt: оно публикует события в `EventBus`, а страницы
интерфейса на них подписываются. Всё работает в одном лупе, поэтому
обработчики могут напрямую трогать виджеты.

### Схема базы

14 таблиц, заведены сразу под все этапы, чтобы миграции не ломали уже
созданные профили:

`users`, `workspaces`, `api_keys` (секреты зашифрованы), `agents`, `tasks`,
`subtasks`, `messages` (приватная история агента), `reports`, `summaries`,
`incidents`, `approvals` (точки human-in-the-loop), `budgets`, `usage_log`.

**Изоляция агентов держится на выборке.** История каждого агента лежит
в `messages` и всегда выбирается с фильтром по `agent_id`. Кросс-агентных
выборок в коде нет — это инвариант, который нельзя нарушать при доработках.

### Поток выполнения одной подзадачи

1. `Orchestrator._schedule` строит волну подзадач, у которых выполнены
   зависимости, и запускает их параллельно (по умолчанию до 6 одновременно).
   На каждого агента стоит персональный лок: он не берёт две подзадачи
   сразу, иначе его личная история перестала бы быть связной.
2. `AgentRunner.run` собирает контекст: системный промпт роли, общая задача
   проекта, своя подзадача, приватная история, последняя анонимная сводка.
   Дальше ReAct-цикл с инструментами.
3. Результат сохраняется в `subtasks.result` и `reports`.
4. `Supervisor.review` выносит вердикт по чек-листу. `ok` закрывает
   подзадачу, `rework` возвращает её тому же исполнителю с замечаниями,
   `conflict` заводит инцидент.
5. При включённом human-in-the-loop срабатывают три триггера паузы:
   конфликт или непринятый результат, самооценка агента ниже порога,
   завершение волны подзадач.
6. `BudgetGuard` проверяется перед каждым обращением к модели.

---


---

# Полный код


## Точка входа и конфигурация

### `main.py`

*114 строк*

````python
"""Точка входа AI Orchestrator.

Запуск::

    python main.py

Цикл событий Qt и asyncio объединяются через qasync — это даёт один общий
луп, в котором живут и интерфейс, и параллельно работающие агенты.
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

# Чтобы приложение запускалось из любого каталога.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.config import APP_NAME, PATHS, AppSettings  # noqa: E402
from app.i18n import set_language  # noqa: E402
from utils.logging_setup import setup_logging  # noqa: E402

log = logging.getLogger("aiorc.main")


def _check_dependencies() -> None:
    """Понятное сообщение вместо стектрейса, если зависимости не установлены."""
    missing: list[str] = []
    for module, package in (("PySide6", "PySide6"), ("qasync", "qasync"),
                            ("httpx", "httpx"), ("cryptography", "cryptography")):
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    if missing:
        print(f"Не установлены зависимости: {', '.join(missing)}\n"
              f"Выполните:  pip install -r requirements.txt", file=sys.stderr)
        sys.exit(1)


def start_ui(db, settings: AppSettings) -> dict[str, object]:
    """Связывает окна: вход → главное окно → выход или смена языка.

    Возвращает словарь с текущими окнами (ключи ``login`` и ``main``) —
    по нему смоук-тест интерфейса ходит по тому же пути, что и приложение.
    """
    from ui.login_window import LoginWindow
    from ui.main_window import MainWindow

    windows: dict[str, object] = {}

    def show_login() -> None:
        login = LoginWindow(db, settings)
        login.logged_in.connect(lambda session: on_login(login, session))
        windows["login"] = login
        login.show()

    def open_main(session, page: int = 0) -> None:
        window = MainWindow(db, session, settings)
        window.logged_out.connect(show_login)
        window.rebuild_requested.connect(lambda index: rebuild_main(window, index))
        windows["main"] = window
        window.select_page(page)
        window.show()

    def rebuild_main(old: MainWindow, page: int) -> None:
        """Пересобирает главное окно после смены языка, сохраняя сессию."""
        geometry = old.saveGeometry()
        open_main(old.session, page)
        windows["main"].restoreGeometry(geometry)
        old.close()
        old.deleteLater()

    def on_login(login: LoginWindow, session) -> None:
        login.close()
        open_main(session)

    show_login()
    return windows


def main() -> int:
    _check_dependencies()

    import qasync
    from PySide6.QtWidgets import QApplication

    from storage.db import Database
    from ui.theme import stylesheet

    setup_logging()
    PATHS.ensure()
    log.info("Старт %s, каталог данных: %s", APP_NAME, PATHS.home)

    settings = AppSettings.load()
    set_language(settings.language)

    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setStyleSheet(stylesheet(settings.theme))

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    windows = start_ui(Database(), settings)  # noqa: F841 — держит окна живыми

    with loop:
        return loop.run_forever() or 0


if __name__ == "__main__":
    sys.exit(main())
````

### `app/config.py`

*128 строк*

````python
"""Глобальная конфигурация приложения: пути, константы, настройки по умолчанию.

Все пользовательские данные хранятся ЛОКАЛЬНО в домашнем каталоге пользователя.
Каталог можно переопределить переменной окружения ``AIORC_HOME``.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

APP_NAME = "AI Orchestrator"
APP_SLUG = "ai-orchestrator"
APP_VERSION = "1.0.0"          # версия растёт вместе с этапами MVP
SCHEMA_VERSION = 1             # версия схемы SQLite (для миграций)


def _default_home() -> Path:
    """Возвращает корневой каталог данных приложения для текущей ОС."""
    env = os.environ.get("AIORC_HOME")
    if env:
        return Path(env).expanduser()
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    return base / APP_SLUG


@dataclass(frozen=True)
class Paths:
    """Набор путей, используемых приложением."""

    home: Path = field(default_factory=_default_home)

    @property
    def db_file(self) -> Path:
        return self.home / "app.db"

    @property
    def logs_dir(self) -> Path:
        return self.home / "logs"

    @property
    def workspaces_dir(self) -> Path:
        """Корень песочниц/рабочих файлов воркспейсов."""
        return self.home / "workspaces"

    @property
    def exports_dir(self) -> Path:
        return self.home / "exports"

    @property
    def config_file(self) -> Path:
        return self.home / "settings.json"

    def workspace_dir(self, workspace_id: int) -> Path:
        """Каталог конкретного воркспейса (рабочая зона агентов)."""
        return self.workspaces_dir / f"ws_{workspace_id}"

    def ensure(self) -> None:
        """Создаёт все необходимые каталоги."""
        for p in (self.home, self.logs_dir, self.workspaces_dir, self.exports_dir):
            p.mkdir(parents=True, exist_ok=True)


PATHS = Paths()


@dataclass
class AppSettings:
    """Настройки уровня приложения (не привязаны к пользователю)."""

    language: str = "ru"           # "ru" | "en"
    theme: str = "dark"            # "dark" | "light"
    last_username: str = ""
    remember_master_password: bool = False

    @classmethod
    def load(cls) -> "AppSettings":
        PATHS.ensure()
        if PATHS.config_file.exists():
            try:
                data = json.loads(PATHS.config_file.read_text("utf-8"))
                known = {f for f in cls.__dataclass_fields__}
                return cls(**{k: v for k, v in data.items() if k in known})
            except Exception:  # noqa: BLE001 — повреждённый конфиг не должен ронять старт
                pass
        return cls()

    def save(self) -> None:
        PATHS.ensure()
        PATHS.config_file.write_text(
            json.dumps(self.__dict__, ensure_ascii=False, indent=2), "utf-8"
        )


# ---------------------------------------------------------------------------
# Значения по умолчанию для воркспейса (этапы 5-9 читают их отсюда)
# ---------------------------------------------------------------------------

DEFAULT_WORKSPACE_SETTINGS: dict = {
    "human_in_the_loop": True,          # паузы в критических точках
    "hitl_confidence_threshold": 0.5,   # ниже этой самооценки агента — спросить человека
    "hitl_pause_on_milestone": False,   # пауза после каждой волны подзадач
    "summary_interval_minutes": 15,     # периодическая сводка супервайзера
    "summary_on_event": True,           # сводка при завершении подзадачи
    "supervisor_agent_id": None,        # какой агент играет роль супервайзера
    "supervisor_mode": "api",           # "api" | "local" (Ollama и т.п.)
    "supervisor_local_model": "qwen2.5:7b-instruct",
    "supervisor_local_base_url": "http://localhost:11434/v1",
    "max_rework_rounds": 2,             # сколько раз супервайзер может вернуть работу
    "anonymize_summaries": True,        # пересказ без указания авторов
    "task_token_limit": None,           # None = без лимита (вопрос 7)
    "agent_max_steps": 10,              # шагов ReAct-цикла на подзадачу
    "tools_enabled": ["web_search", "files", "code_exec"],
    "extra_allowed_paths": [],          # доп. каталоги для файлового инструмента
    "sandbox_backend": "auto",          # "auto" | "subprocess" | "docker"
    "sandbox_timeout_sec": 30,
    "sandbox_memory_mb": 512,
    "search_backend": "duckduckgo",     # "duckduckgo" | "tavily" | "brave"
    "fetch_pages": True,                # скачивать и парсить страницы из выдачи
}
````

### `app/i18n.py`

*547 строк*

````python
"""Локализация интерфейса (RU/EN) с переключателем в настройках.

Использование::

    from app.i18n import tr
    label.setText(tr("login.title"))

Строки хранятся плоскими словарями «ключ -> перевод». Отсутствующий ключ
возвращается как есть — это заметно в UI и помогает не потерять переводы.
"""

from __future__ import annotations

from typing import Callable

_LISTENERS: list[Callable[[], None]] = []
_CURRENT = "ru"

RU: dict[str, str] = {
    # --- общее ---
    "app.title": "AI Orchestrator — оркестрация ИИ-агентов",
    "common.ok": "OK",
    "common.cancel": "Отмена",
    "common.save": "Сохранить",
    "common.delete": "Удалить",
    "common.edit": "Изменить",
    "common.add": "Добавить",
    "common.close": "Закрыть",
    "common.name": "Название",
    "common.description": "Описание",
    "common.created": "Создан",
    "common.status": "Статус",
    "common.error": "Ошибка",
    "common.success": "Готово",
    "common.test": "Проверить",
    "common.yes": "Да",
    "common.no": "Нет",
    "common.confirm": "Подтверждение",
    "common.none": "не задан",
    "common.refresh": "Обновить",
    "common.open": "Открыть",
    # --- авторизация ---
    "login.title": "Вход в профиль",
    "login.subtitle": "Все данные хранятся локально на этом устройстве",
    "login.username": "Имя профиля",
    "login.password": "Пароль",
    "login.password2": "Повторите пароль",
    "login.signin": "Войти",
    "login.create": "Создать профиль",
    "login.create_title": "Новый локальный профиль",
    "login.remember": "Запомнить пароль в хранилище ОС",
    "login.no_profiles": "Профилей пока нет — создайте первый",
    "login.bad_credentials": "Неверное имя профиля или пароль",
    "login.password_mismatch": "Пароли не совпадают",
    "login.password_short": "Пароль должен быть не короче 8 символов",
    "login.user_exists": "Профиль с таким именем уже существует",
    "login.warning": (
        "Пароль профиля используется как мастер-ключ для шифрования API-ключей. "
        "Восстановить его невозможно — при утере ключи придётся добавить заново."
    ),
    # --- бюджеты (этап 9) ---
    "nav.budget": "Бюджеты",
    "bud.title": "Бюджеты и лимиты",
    "bud.subtitle": "Лимит можно поставить на проект, задачу и каждого агента. Пустое поле — без ограничения",
    "bud.spent": "израсходовано: {tokens} токенов · ${cost}",
    "bud.token_limit": "Лимит токенов",
    "bud.cost_limit": "Лимит стоимости, $",
    "bud.alert_at": "Алерт при",
    "bud.no_limit": "без лимита",
    "bud.used_pct": "Выбрано {pct}% бюджета",
    "bud.exceeded": "Лимит исчерпан — новые вызовы модели заблокированы",
    "bud.nothing": "Пока нечего ограничивать: создайте агентов и поставьте задачу.",
    # --- экспорт (этап 8) ---
    "nav.export": "Экспорт",
    "exp.title": "Экспорт результата",
    "exp.subtitle": "Формат подбирается по типу задачи, но выбор всегда за вами",
    "exp.format": "Формат",
    "exp.use_auto": "Определить автоматически",
    "exp.auto_hint": "Рекомендация: {reason}",
    "exp.stats": "Готовых результатов: {results} из {total}  ·  файлов в проекте: {files}  ·  отчётов: {reports}",
    "exp.content": "Что включить",
    "exp.opt_results": "Результаты подзадач (основное содержание)",
    "exp.opt_reports": "Полные отчёты исполнителей",
    "exp.opt_summaries": "Сводки супервайзера",
    "exp.opt_incidents": "Инциденты и как они разрешились",
    "exp.opt_decisions": "Решения, принятые вами вручную",
    "exp.opt_stats": "Статистика прогона (токены, стоимость)",
    "exp.opt_files": "Файлы из рабочего каталога",
    "exp.opt_anon": "Скрыть имена агентов",
    "exp.opt_anon_hint": "Вместо имён будет «Исполнитель A», «Исполнитель B» и так далее",
    "exp.files_zip_only": "Вложить файлы можно только в ZIP-архив",
    "exp.output": "Куда сохранить",
    "exp.browse": "Обзор…",
    "exp.export": "Экспортировать",
    "exp.open_folder": "Открыть папку",
    "exp.done": "Сохранено: {path} ({size})",
    "exp.no_path": "Укажите путь для сохранения файла.",
    "exp.nothing": "Экспортировать пока нечего: нет ни готовых результатов, ни файлов.",
    "exp.open_failed": "Не удалось открыть проводник. Файл лежит здесь: {path}",
    # --- дашборд (этап 6) ---
    "dash.title": "Дашборд",
    "dash.subtitle": "Состояние агентов, прогресс, расход и лента событий в реальном времени",
    "dash.m_agents": "Агентов",
    "dash.m_subtasks": "Подзадач готово",
    "dash.m_tokens": "Токенов израсходовано",
    "dash.m_tokens_limit": "Токенов: {pct}% от лимита {limit}",
    "dash.m_cost": "Примерная стоимость",
    "dash.m_reworks": "Доработок",
    "dash.m_open_incidents": "Требуют решения",
    "dash.cost_chart": "Стоимость нарастающим итогом",
    "dash.tokens_chart": "Токены нарастающим итогом",
    "dash.by_agent": "Расход по агентам",
    "dash.no_usage": "расхода пока не было",
    "dash.agents": "Агенты",
    "dash.feed": "Лента отчётов и сводок",
    "dash.incidents": "Инциденты",
    "dash.no_feed": "Отчётов пока нет — запустите агентов на вкладке «Выполнение».",
    "dash.summary_line": "Сводка супервайзера",
    "dash.supervisor_line": "Проверки и сводки",
    "dash.unknown_agent": "Агент удалён",
    "dash.confidence": "уверенность",
    "dash.v_ok": "принято",
    "dash.v_rework": "на доработку",
    "dash.v_conflict": "конфликт",
    "dash.i_open": "открыт",
    "dash.i_escalated": "требует решения",
    "dash.i_auto": "разрешён автоматически",
    "dash.i_resolved": "закрыт",
    # --- супервайзер (этап 5) ---
    "nav.supervisor": "Супервайзер",
    "sup.title": "Супервайзер",
    "sup.subtitle": "Проверяет отчёты по чек-листу и рассылает анонимные сводки",
    "sup.summaries": "Сводки",
    "sup.incidents": "Инциденты",
    "sup.make_summary": "Составить сводку",
    "sup.no_summaries": "Сводок пока нет. Они появятся во время прогона или по кнопке выше.",
    "sup.no_incidents": "Инцидентов нет — супервайзер не нашёл проблем.",
    "sup.resolve": "Закрыть инцидент",
    "sup.resolution": "Решение",
    "sup.delivered": "получателей: {n}",
    "sup.by_timer": "по таймеру",
    "sup.by_event": "по событию",
    "sup.by_hand": "вручную",
    "sup.by_final": "итоговая",
    "sup.model_api": "Супервайзер: {name} — {model}",
    "sup.model_local": "Супервайзер: локальная модель {model} ({url})",
    "sup.not_configured": "Супервайзер не настроен. Выберите его на вкладке «Настройки».",
    "sup.nothing_to_summarize": "Пока нечего обобщать — нет готовых результатов.",
    # --- навигация ---
    "nav.workspaces": "Воркспейсы",
    "nav.keys": "API-ключи",
    "nav.agents": "Агенты",
    "nav.task": "Задача",
    "nav.dashboard": "Дашборд",
    "nav.settings": "Настройки",
    "nav.logout": "Выйти",
    # --- воркспейсы ---
    "ws.title": "Воркспейсы (параллельные проекты)",
    "ws.new": "Новый воркспейс",
    "ws.name": "Название проекта",
    "ws.empty": "Ещё нет ни одного воркспейса. Создайте первый, чтобы начать.",
    "ws.current": "Активный воркспейс",
    "ws.select": "Выбрать",
    "ws.delete_confirm": "Удалить воркспейс вместе со всеми агентами и задачами?",
    "ws.agents_count": "агентов",
    "ws.archived": "В архиве",
    # --- ключи ---
    "keys.title": "API-ключи провайдеров",
    "keys.subtitle": "Ключи шифруются AES-256-GCM мастер-ключом вашего профиля",
    "keys.new": "Добавить ключ",
    "keys.label": "Метка",
    "keys.provider": "Провайдер",
    "keys.key": "API-ключ",
    "keys.base_url": "Base URL",
    "keys.no_key_needed": "Этот провайдер работает без ключа (локальные модели)",
    "keys.empty": "Ключей пока нет. Добавьте хотя бы один, чтобы создавать агентов.",
    "keys.test_ok": "Соединение установлено. Доступно моделей: {n}",
    "keys.test_fail": "Не удалось подключиться: {err}",
    "keys.delete_confirm": "Удалить ключ? Агенты, привязанные к нему, перестанут работать.",
    "keys.reveal": "Показать",
    # --- агенты ---
    "agents.title": "Агенты воркспейса",
    "agents.new": "Создать агента",
    "agents.name": "Имя агента",
    "agents.role": "Роль",
    "agents.template": "Шаблон роли",
    "agents.prompt": "Системный промпт",
    "agents.provider_key": "Ключ / провайдер",
    "agents.model": "Модель",
    "agents.temperature": "Температура",
    "agents.max_tokens": "Макс. токенов ответа",
    "agents.enabled": "Активен",
    "agents.empty": "В этом воркспейсе ещё нет агентов.",
    "agents.no_keys": "Сначала добавьте API-ключ на вкладке «API-ключи».",
    "agents.load_models": "Загрузить список моделей",
    "agents.delete_confirm": "Удалить агента и всю его историю?",
    "agents.isolated_note": "Агенты полностью изолированы: они не видят промпты и переписку друг друга.",
    # --- задача ---
    "task.title": "Постановка задачи",
    "task.name": "Название задачи",
    "task.body": "Формулировка задачи",
    "task.placeholder": "Опишите, что нужно сделать. Чем подробнее — тем точнее разбиение на подзадачи.",
    "task.save": "Сохранить задачу",
    "task.subtasks": "Подзадачи",
    "task.add_subtask": "Добавить подзадачу",
    "task.autosplit": "Разбить автоматически (ИИ)",
    "task.assignee": "Исполнитель",
    "task.unassigned": "Не назначен",
    "task.token_limit": "Лимит токенов на задачу",
    "task.token_limit_hint": "Пусто = без лимита",
    "task.result_format": "Формат результата",
    "task.no_task": "Задача ещё не поставлена.",
    "task.subtask_title": "Что нужно сделать",
    "task.move_up": "Выше",
    "task.move_down": "Ниже",
    "task.run": "Запустить агентов",
    # --- выполнение (этап 4) ---
    "nav.run": "Выполнение",
    "run.title": "Выполнение задачи",
    "run.subtitle": "Агенты работают параллельно; изоляция контекста сохраняется",
    "run.start": "Запустить агентов",
    "run.pause": "Пауза",
    "run.resume": "Продолжить",
    "run.stop": "Остановить",
    "run.stop_confirm": "Остановить выполнение? Текущие шаги агентов будут прерваны.",
    "run.feed": "Лента событий",
    "run.clear_feed": "Очистить",
    "run.idle": "Прогон не запущен",
    "run.summary": "Выполнено {done} из {total}, с ошибкой: {errors}",
    "run.no_subtasks": "Нет подзадач. Добавьте их на вкладке «Задача».",
    "run.unassigned": "У этих подзадач не назначен исполнитель:",
    # --- статусы ---
    "status.idle": "Ожидает",
    "status.running": "Работает",
    "status.paused": "На паузе",
    "status.error": "Ошибка",
    "status.done": "Завершено",
    "status.review": "На проверке",
    "status.rework": "На доработке",
    # --- настройки ---
    "settings.title": "Настройки",
    "settings.language": "Язык интерфейса",
    "settings.theme": "Тема",
    "settings.hitl": "Human-in-the-loop (паузы в критических точках)",
    "settings.hitl_threshold": "Порог уверенности для паузы",
    "settings.hitl_threshold_hint": "Если исполнитель оценил свою уверенность ниже этого значения, система остановится и спросит вас. 0 — не спрашивать никогда.",
    "settings.hitl_milestone": "Пауза после каждого этапа работ",
    "settings.hitl_milestone_hint": "Спрашивать подтверждение перед запуском следующей волны подзадач",
    "sup.approvals": "Решения",
    "sup.no_approvals": "Решений пока не было.",
    "sup.d_approve": "принято",
    "sup.d_rework": "на доработку",
    "sup.d_skip": "пропущено",
    "sup.d_abort": "прогон остановлен",
    "sup.d_cancelled": "снято без решения",
    "sup.d_pending": "ожидает решения",
    "settings.supervisor": "Супервайзер",
    "settings.supervisor_mode": "Режим супервайзера",
    "settings.supervisor_api": "Свой API-ключ (один из агентов/провайдеров)",
    "settings.supervisor_local": "Локальная модель (Ollama, напр. Qwen)",
    "settings.summary_interval": "Интервал сводок, мин",
    "settings.summary_on_event": "Сводка при завершении подзадачи",
    "settings.sandbox": "Песочница для кода",
    "settings.allowed_paths": "Доп. каталоги, доступные агентам",
    "settings.add_path": "Добавить каталог",
    "settings.change_password": "Сменить пароль профиля",
    "settings.restart_note": "Язык переключается сразу. Во время прогона — после выхода и повторного входа.",
    "settings.lang_after_run": "Идёт прогон — язык сменится после выхода и повторного входа, чтобы не прерывать агентов.",
    "settings.budget": "Бюджеты и лимиты",
}

EN: dict[str, str] = {
    "app.title": "AI Orchestrator — multi-agent orchestration",
    "common.ok": "OK",
    "common.cancel": "Cancel",
    "common.save": "Save",
    "common.delete": "Delete",
    "common.edit": "Edit",
    "common.add": "Add",
    "common.close": "Close",
    "common.name": "Name",
    "common.description": "Description",
    "common.created": "Created",
    "common.status": "Status",
    "common.error": "Error",
    "common.success": "Done",
    "common.test": "Test",
    "common.yes": "Yes",
    "common.no": "No",
    "common.confirm": "Confirm",
    "common.none": "not set",
    "common.refresh": "Refresh",
    "common.open": "Open",
    "login.title": "Sign in",
    "login.subtitle": "All data is stored locally on this device",
    "login.username": "Profile name",
    "login.password": "Password",
    "login.password2": "Repeat password",
    "login.signin": "Sign in",
    "login.create": "Create profile",
    "login.create_title": "New local profile",
    "login.remember": "Remember password in OS keyring",
    "login.no_profiles": "No profiles yet — create the first one",
    "login.bad_credentials": "Wrong profile name or password",
    "login.password_mismatch": "Passwords do not match",
    "login.password_short": "Password must be at least 8 characters",
    "login.user_exists": "A profile with this name already exists",
    "login.warning": (
        "The profile password is also the master key that encrypts your API keys. "
        "It cannot be recovered — if lost, keys must be re-entered."
    ),
    "nav.budget": "Budgets",
    "bud.title": "Budgets and limits",
    "bud.subtitle": "Limits apply to the project, the task and each agent. An empty field means no limit",
    "bud.spent": "spent: {tokens} tokens · ${cost}",
    "bud.token_limit": "Token limit",
    "bud.cost_limit": "Cost limit, $",
    "bud.alert_at": "Alert at",
    "bud.no_limit": "no limit",
    "bud.used_pct": "{pct}% of budget used",
    "bud.exceeded": "Limit reached — further model calls are blocked",
    "bud.nothing": "Nothing to limit yet: create agents and define a task.",
    "nav.export": "Export",
    "exp.title": "Export result",
    "exp.subtitle": "The format is suggested from the task type, but the choice is yours",
    "exp.format": "Format",
    "exp.use_auto": "Detect automatically",
    "exp.auto_hint": "Suggestion: {reason}",
    "exp.stats": "Ready results: {results} of {total}  ·  project files: {files}  ·  reports: {reports}",
    "exp.content": "What to include",
    "exp.opt_results": "Subtask results (main content)",
    "exp.opt_reports": "Full agent reports",
    "exp.opt_summaries": "Supervisor summaries",
    "exp.opt_incidents": "Incidents and how they were resolved",
    "exp.opt_decisions": "Decisions you made manually",
    "exp.opt_stats": "Run statistics (tokens, cost)",
    "exp.opt_files": "Files from the working folder",
    "exp.opt_anon": "Hide agent names",
    "exp.opt_anon_hint": "Names are replaced with “Agent A”, “Agent B” and so on",
    "exp.files_zip_only": "Files can only be bundled into a ZIP archive",
    "exp.output": "Save to",
    "exp.browse": "Browse…",
    "exp.export": "Export",
    "exp.open_folder": "Open folder",
    "exp.done": "Saved: {path} ({size})",
    "exp.no_path": "Choose where to save the file.",
    "exp.nothing": "Nothing to export yet: no finished results and no files.",
    "exp.open_failed": "Could not open the file manager. The file is here: {path}",
    "dash.title": "Dashboard",
    "dash.subtitle": "Agent status, progress, spending and activity feed in real time",
    "dash.m_agents": "Agents",
    "dash.m_subtasks": "Subtasks done",
    "dash.m_tokens": "Tokens spent",
    "dash.m_tokens_limit": "Tokens: {pct}% of limit {limit}",
    "dash.m_cost": "Estimated cost",
    "dash.m_reworks": "Reworks",
    "dash.m_open_incidents": "Need a decision",
    "dash.cost_chart": "Cumulative cost",
    "dash.tokens_chart": "Cumulative tokens",
    "dash.by_agent": "Spending by agent",
    "dash.no_usage": "no spending yet",
    "dash.agents": "Agents",
    "dash.feed": "Reports and summaries",
    "dash.incidents": "Incidents",
    "dash.no_feed": "No reports yet — start the agents on the Run tab.",
    "dash.summary_line": "Supervisor summary",
    "dash.supervisor_line": "Supervisor checks",
    "dash.unknown_agent": "Deleted agent",
    "dash.confidence": "confidence",
    "dash.v_ok": "accepted",
    "dash.v_rework": "rework",
    "dash.v_conflict": "conflict",
    "dash.i_open": "open",
    "dash.i_escalated": "needs a decision",
    "dash.i_auto": "auto-resolved",
    "dash.i_resolved": "closed",
    "nav.supervisor": "Supervisor",
    "sup.title": "Supervisor",
    "sup.subtitle": "Reviews reports against a checklist and broadcasts anonymous summaries",
    "sup.summaries": "Summaries",
    "sup.incidents": "Incidents",
    "sup.make_summary": "Create summary",
    "sup.no_summaries": "No summaries yet. They appear during a run or via the button above.",
    "sup.no_incidents": "No incidents — the supervisor found no problems.",
    "sup.resolve": "Close incident",
    "sup.resolution": "Resolution",
    "sup.delivered": "recipients: {n}",
    "sup.by_timer": "on timer",
    "sup.by_event": "on event",
    "sup.by_hand": "manual",
    "sup.by_final": "final",
    "sup.model_api": "Supervisor: {name} — {model}",
    "sup.model_local": "Supervisor: local model {model} ({url})",
    "sup.not_configured": "Supervisor is not configured. Pick one on the Settings tab.",
    "sup.nothing_to_summarize": "Nothing to summarize yet — no finished results.",
    "nav.workspaces": "Workspaces",
    "nav.keys": "API keys",
    "nav.agents": "Agents",
    "nav.task": "Task",
    "nav.dashboard": "Dashboard",
    "nav.settings": "Settings",
    "nav.logout": "Log out",
    "ws.title": "Workspaces (parallel projects)",
    "ws.new": "New workspace",
    "ws.name": "Project name",
    "ws.empty": "No workspaces yet. Create one to get started.",
    "ws.current": "Active workspace",
    "ws.select": "Select",
    "ws.delete_confirm": "Delete workspace with all its agents and tasks?",
    "ws.agents_count": "agents",
    "ws.archived": "Archived",
    "keys.title": "Provider API keys",
    "keys.subtitle": "Keys are encrypted with AES-256-GCM using your profile master key",
    "keys.new": "Add key",
    "keys.label": "Label",
    "keys.provider": "Provider",
    "keys.key": "API key",
    "keys.base_url": "Base URL",
    "keys.no_key_needed": "This provider needs no key (local models)",
    "keys.empty": "No keys yet. Add one to be able to create agents.",
    "keys.test_ok": "Connection OK. Models available: {n}",
    "keys.test_fail": "Connection failed: {err}",
    "keys.delete_confirm": "Delete the key? Agents bound to it will stop working.",
    "keys.reveal": "Reveal",
    "agents.title": "Workspace agents",
    "agents.new": "Create agent",
    "agents.name": "Agent name",
    "agents.role": "Role",
    "agents.template": "Role template",
    "agents.prompt": "System prompt",
    "agents.provider_key": "Key / provider",
    "agents.model": "Model",
    "agents.temperature": "Temperature",
    "agents.max_tokens": "Max response tokens",
    "agents.enabled": "Enabled",
    "agents.empty": "This workspace has no agents yet.",
    "agents.no_keys": "Add an API key on the “API keys” tab first.",
    "agents.load_models": "Load model list",
    "agents.delete_confirm": "Delete the agent and all its history?",
    "agents.isolated_note": "Agents are fully isolated: they never see each other's prompts or chats.",
    "task.title": "Task definition",
    "task.name": "Task title",
    "task.body": "Task statement",
    "task.placeholder": "Describe what needs to be done. More detail = better subtask split.",
    "task.save": "Save task",
    "task.subtasks": "Subtasks",
    "task.add_subtask": "Add subtask",
    "task.autosplit": "Auto-split (AI)",
    "task.assignee": "Assignee",
    "task.unassigned": "Unassigned",
    "task.token_limit": "Task token limit",
    "task.token_limit_hint": "Empty = no limit",
    "task.result_format": "Result format",
    "task.no_task": "No task defined yet.",
    "task.subtask_title": "What to do",
    "task.move_up": "Up",
    "task.move_down": "Down",
    "task.run": "Run agents",
    "nav.run": "Run",
    "run.title": "Task execution",
    "run.subtitle": "Agents work in parallel; context isolation is preserved",
    "run.start": "Run agents",
    "run.pause": "Pause",
    "run.resume": "Resume",
    "run.stop": "Stop",
    "run.stop_confirm": "Stop execution? Agents' current steps will be interrupted.",
    "run.feed": "Event feed",
    "run.clear_feed": "Clear",
    "run.idle": "Not running",
    "run.summary": "{done} of {total} finished, failed: {errors}",
    "run.no_subtasks": "No subtasks. Add them on the “Task” tab.",
    "run.unassigned": "These subtasks have no assignee:",
    "status.idle": "Idle",
    "status.running": "Running",
    "status.paused": "Paused",
    "status.error": "Error",
    "status.done": "Done",
    "status.review": "In review",
    "status.rework": "Rework",
    "settings.title": "Settings",
    "settings.language": "Interface language",
    "settings.theme": "Theme",
    "settings.hitl": "Human-in-the-loop (pause at critical points)",
    "settings.hitl_threshold": "Confidence threshold for pausing",
    "settings.hitl_threshold_hint": "If an agent rates its own confidence below this, the system stops and asks you. 0 — never ask.",
    "settings.hitl_milestone": "Pause after each stage",
    "settings.hitl_milestone_hint": "Ask for confirmation before starting the next wave of subtasks",
    "sup.approvals": "Decisions",
    "sup.no_approvals": "No decisions yet.",
    "sup.d_approve": "approved",
    "sup.d_rework": "sent back",
    "sup.d_skip": "skipped",
    "sup.d_abort": "run aborted",
    "sup.d_cancelled": "dropped without a decision",
    "sup.d_pending": "awaiting decision",
    "settings.supervisor": "Supervisor",
    "settings.supervisor_mode": "Supervisor mode",
    "settings.supervisor_api": "Own API key (one of the providers)",
    "settings.supervisor_local": "Local model (Ollama, e.g. Qwen)",
    "settings.summary_interval": "Summary interval, min",
    "settings.summary_on_event": "Summary when a subtask finishes",
    "settings.sandbox": "Code sandbox",
    "settings.allowed_paths": "Extra folders accessible to agents",
    "settings.add_path": "Add folder",
    "settings.change_password": "Change profile password",
    "settings.restart_note": "Language switches immediately. During a run it applies after you log out and back in.",
    "settings.lang_after_run": "A run is in progress — the language will change after you log out and back in, so agents are not interrupted.",
    "settings.budget": "Budgets and limits",
}

_CATALOG: dict[str, dict[str, str]] = {"ru": RU, "en": EN}


def set_language(code: str) -> None:
    """Переключает язык и уведомляет подписчиков (окна перерисовывают тексты)."""
    global _CURRENT
    if code in _CATALOG:
        _CURRENT = code
        for cb in list(_LISTENERS):
            try:
                cb()
            except Exception:  # noqa: BLE001
                pass


def current_language() -> str:
    return _CURRENT


def available_languages() -> list[tuple[str, str]]:
    return [("ru", "Русский"), ("en", "English")]


def on_language_changed(callback: Callable[[], None]) -> None:
    """Подписка на смену языка."""
    _LISTENERS.append(callback)


def tr(key: str, **kwargs) -> str:
    """Возвращает локализованную строку; поддерживает ``{placeholders}``."""
    text = _CATALOG.get(_CURRENT, RU).get(key) or RU.get(key, key)
    if kwargs:
        try:
            return text.format(**kwargs)
        except (KeyError, IndexError):
            return text
    return text
````


## Хранилище

### `storage/schema.sql`

*214 строк*

````sql
-- Схема локальной БД AI Orchestrator (SQLite).
-- Таблицы заведены сразу под все 9 этапов MVP, чтобы не ломать миграциями
-- уже созданные профили пользователей.

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------------
-- Этап 1: локальные профили и воркспейсы
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS users (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    username      TEXT    NOT NULL UNIQUE,
    password_hash BLOB    NOT NULL,   -- Argon2id(password, verify_salt)
    verify_salt   BLOB    NOT NULL,   -- соль для проверки пароля
    kdf_salt      BLOB    NOT NULL,   -- соль для вывода мастер-ключа шифрования
    created_at    TEXT    NOT NULL,
    settings_json TEXT    NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS workspaces (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name          TEXT    NOT NULL,
    description   TEXT    NOT NULL DEFAULT '',
    settings_json TEXT    NOT NULL DEFAULT '{}',
    archived      INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT    NOT NULL,
    updated_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ws_user ON workspaces(user_id);

-- ---------------------------------------------------------------------------
-- Этап 2: API-ключи (зашифрованы) и агенты
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS api_keys (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id       INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    label         TEXT    NOT NULL,
    provider      TEXT    NOT NULL,   -- ключ пресета: openai/anthropic/gemini/...
    base_url      TEXT    NOT NULL DEFAULT '',
    secret_blob   BLOB,               -- nonce||ciphertext||tag; NULL для Ollama
    meta_json     TEXT    NOT NULL DEFAULT '{}',
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_keys_user ON api_keys(user_id);

CREATE TABLE IF NOT EXISTS agents (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id  INTEGER NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    name          TEXT    NOT NULL,
    role          TEXT    NOT NULL DEFAULT '',
    system_prompt TEXT    NOT NULL DEFAULT '',
    api_key_id    INTEGER REFERENCES api_keys(id) ON DELETE SET NULL,
    provider      TEXT    NOT NULL DEFAULT '',
    model         TEXT    NOT NULL DEFAULT '',
    params_json   TEXT    NOT NULL DEFAULT '{}',  -- temperature, max_tokens, tools
    enabled       INTEGER NOT NULL DEFAULT 1,
    status        TEXT    NOT NULL DEFAULT 'idle',
    is_supervisor INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_agents_ws ON agents(workspace_id);

-- ---------------------------------------------------------------------------
-- Этап 3: задачи и подзадачи
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS tasks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id  INTEGER NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    title         TEXT    NOT NULL DEFAULT '',
    description   TEXT    NOT NULL DEFAULT '',
    status        TEXT    NOT NULL DEFAULT 'draft',
    result_format TEXT    NOT NULL DEFAULT 'auto',  -- auto|markdown|docx|pdf|zip
    token_limit   INTEGER,                          -- NULL = без лимита
    created_at    TEXT    NOT NULL,
    updated_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tasks_ws ON tasks(workspace_id);

CREATE TABLE IF NOT EXISTS subtasks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id       INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
    agent_id      INTEGER REFERENCES agents(id) ON DELETE SET NULL,
    title         TEXT    NOT NULL,
    description   TEXT    NOT NULL DEFAULT '',
    status        TEXT    NOT NULL DEFAULT 'idle',
    order_index   INTEGER NOT NULL DEFAULT 0,
    depends_on    TEXT    NOT NULL DEFAULT '',   -- CSV id подзадач-предшественников
    result        TEXT    NOT NULL DEFAULT '',
    rework_count  INTEGER NOT NULL DEFAULT 0,
    tokens_in     INTEGER NOT NULL DEFAULT 0,
    tokens_out    INTEGER NOT NULL DEFAULT 0,
    cost_usd      REAL    NOT NULL DEFAULT 0,
    created_at    TEXT    NOT NULL,
    updated_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_subtasks_task ON subtasks(task_id);

-- ---------------------------------------------------------------------------
-- Этап 4-5: приватная история агента, отчёты, сводки супервайзера
-- ---------------------------------------------------------------------------

-- Полностью изолированный контекст агента: каждая строка видна только
-- своему agent_id, кросс-агентных выборок в коде нет.
CREATE TABLE IF NOT EXISTS messages (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id      INTEGER NOT NULL REFERENCES agents(id) ON DELETE CASCADE,
    subtask_id    INTEGER REFERENCES subtasks(id) ON DELETE CASCADE,
    role          TEXT    NOT NULL,      -- system|user|assistant|tool
    content       TEXT    NOT NULL DEFAULT '',
    tool_name     TEXT    NOT NULL DEFAULT '',
    tool_call_id  TEXT    NOT NULL DEFAULT '',
    tokens        INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_messages_agent ON messages(agent_id, subtask_id);

CREATE TABLE IF NOT EXISTS reports (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id   INTEGER NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    task_id        INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    subtask_id     INTEGER REFERENCES subtasks(id) ON DELETE CASCADE,
    agent_id       INTEGER REFERENCES agents(id) ON DELETE SET NULL,
    content        TEXT    NOT NULL,
    confidence     REAL,                       -- самооценка уверенности 0..1
    tokens_in      INTEGER NOT NULL DEFAULT 0,
    tokens_out     INTEGER NOT NULL DEFAULT 0,
    cost_usd       REAL    NOT NULL DEFAULT 0,
    reviewed       INTEGER NOT NULL DEFAULT 0,
    review_verdict TEXT    NOT NULL DEFAULT '', -- ok|rework|conflict
    review_notes   TEXT    NOT NULL DEFAULT '',
    created_at     TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_reports_ws ON reports(workspace_id, created_at);

CREATE TABLE IF NOT EXISTS summaries (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id  INTEGER NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    task_id       INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    content       TEXT    NOT NULL,          -- анонимизированный пересказ
    trigger       TEXT    NOT NULL DEFAULT 'timer',  -- timer|event|manual
    delivered_to  TEXT    NOT NULL DEFAULT '',       -- CSV agent_id
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_summaries_ws ON summaries(workspace_id, created_at);

CREATE TABLE IF NOT EXISTS incidents (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id  INTEGER NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    task_id       INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    subtask_id    INTEGER REFERENCES subtasks(id) ON DELETE SET NULL,
    report_id     INTEGER REFERENCES reports(id) ON DELETE SET NULL,
    kind          TEXT    NOT NULL,   -- conflict|factual_error|contradiction|off_scope
    severity      TEXT    NOT NULL DEFAULT 'medium',
    description   TEXT    NOT NULL,
    status        TEXT    NOT NULL DEFAULT 'open',  -- open|auto_resolved|escalated|resolved
    resolution    TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    resolved_at   TEXT
);
CREATE INDEX IF NOT EXISTS idx_incidents_ws ON incidents(workspace_id, created_at);

-- ---------------------------------------------------------------------------
-- Этап 7: точки human-in-the-loop
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS approvals (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id  INTEGER NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
    task_id       INTEGER REFERENCES tasks(id) ON DELETE CASCADE,
    reason        TEXT    NOT NULL,     -- conflict|low_confidence|milestone
    payload_json  TEXT    NOT NULL DEFAULT '{}',
    decision      TEXT    NOT NULL DEFAULT '',  -- '' пока ждём пользователя
    comment       TEXT    NOT NULL DEFAULT '',
    created_at    TEXT    NOT NULL,
    decided_at    TEXT
);

-- ---------------------------------------------------------------------------
-- Этап 9: бюджеты и лимиты
-- ---------------------------------------------------------------------------

CREATE TABLE IF NOT EXISTS budgets (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    scope            TEXT    NOT NULL,   -- 'workspace' | 'agent' | 'task'
    scope_id         INTEGER NOT NULL,
    token_limit      INTEGER,
    cost_limit_usd   REAL,
    tokens_used      INTEGER NOT NULL DEFAULT 0,
    cost_used_usd    REAL    NOT NULL DEFAULT 0,
    alert_threshold  REAL    NOT NULL DEFAULT 0.8,
    alerted          INTEGER NOT NULL DEFAULT 0,
    updated_at       TEXT    NOT NULL,
    UNIQUE(scope, scope_id)
);

-- Журнал вызовов моделей: основа для графиков расхода на дашборде.
CREATE TABLE IF NOT EXISTS usage_log (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    workspace_id  INTEGER REFERENCES workspaces(id) ON DELETE CASCADE,
    task_id       INTEGER,
    subtask_id    INTEGER,
    agent_id      INTEGER,
    provider      TEXT    NOT NULL DEFAULT '',
    model         TEXT    NOT NULL DEFAULT '',
    tokens_in     INTEGER NOT NULL DEFAULT 0,
    tokens_out    INTEGER NOT NULL DEFAULT 0,
    cost_usd      REAL    NOT NULL DEFAULT 0,
    created_at    TEXT    NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_usage_ws ON usage_log(workspace_id, created_at);
````

### `storage/db.py`

*99 строк*

````python
"""Подключение к локальной SQLite-БД и применение схемы.

Соединение одно на процесс (``check_same_thread=False``), запись защищена
мьютексом — этого достаточно, потому что вся работа с БД идёт из одного
asyncio-лупа, а фоновые потоки обращаются к ней редко.
"""

from __future__ import annotations

import sqlite3
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Sequence

from app.config import PATHS, SCHEMA_VERSION

_SCHEMA_FILE = Path(__file__).with_name("schema.sql")


def utcnow() -> str:
    """Единый формат времени для всех таблиц (ISO-8601, UTC)."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def local_time(iso: str, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Переводит сохранённую UTC-метку в местное время для показа человеку."""
    try:
        moment = datetime.fromisoformat(iso)
    except (TypeError, ValueError):
        return iso or ""
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=timezone.utc)
    return moment.astimezone().strftime(fmt)


class Database:
    """Тонкая обёртка над sqlite3 с удобными хелперами."""

    _instance: "Database | None" = None

    def __init__(self, path: Path | None = None) -> None:
        PATHS.ensure()
        self.path = path or PATHS.db_file
        self._lock = threading.RLock()
        self.conn = sqlite3.connect(self.path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.execute("PRAGMA journal_mode = WAL")
        self.conn.execute("PRAGMA synchronous = NORMAL")
        self._migrate()

    # -- singleton -----------------------------------------------------------
    @classmethod
    def instance(cls) -> "Database":
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    # -- миграции ------------------------------------------------------------
    def _migrate(self) -> None:
        """Применяет schema.sql и записывает версию схемы."""
        with self._lock:
            self.conn.executescript(_SCHEMA_FILE.read_text("utf-8"))
            cur = self.conn.execute("PRAGMA user_version")
            current = cur.fetchone()[0]
            if current != SCHEMA_VERSION:
                # Здесь появятся инкрементальные ALTER TABLE, когда схема
                # поедет дальше; сейчас достаточно зафиксировать версию.
                self.conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            self.conn.commit()

    # -- базовые операции ----------------------------------------------------
    def execute(self, sql: str, params: Sequence[Any] = ()) -> sqlite3.Cursor:
        with self._lock:
            cur = self.conn.execute(sql, params)
            self.conn.commit()
            return cur

    def executemany(self, sql: str, seq: Iterable[Sequence[Any]]) -> None:
        with self._lock:
            self.conn.executemany(sql, seq)
            self.conn.commit()

    def query(self, sql: str, params: Sequence[Any] = ()) -> list[sqlite3.Row]:
        with self._lock:
            return self.conn.execute(sql, params).fetchall()

    def query_one(self, sql: str, params: Sequence[Any] = ()) -> sqlite3.Row | None:
        rows = self.query(sql, params)
        return rows[0] if rows else None

    def insert(self, sql: str, params: Sequence[Any] = ()) -> int:
        """INSERT с возвратом нового id."""
        return int(self.execute(sql, params).lastrowid or 0)

    def close(self) -> None:
        with self._lock:
            self.conn.close()
````

### `storage/models.py`

*261 строк*

````python
"""Датаклассы предметной области — типизированное представление строк БД."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from typing import Any


def _json(raw: str | None) -> dict:
    try:
        return json.loads(raw) if raw else {}
    except (TypeError, ValueError):
        return {}


# ---------------------------------------------------------------------------


@dataclass
class User:
    id: int
    username: str
    created_at: str
    settings: dict = field(default_factory=dict)

    @staticmethod
    def from_row(r: sqlite3.Row) -> "User":
        return User(r["id"], r["username"], r["created_at"], _json(r["settings_json"]))


@dataclass
class Workspace:
    id: int
    user_id: int
    name: str
    description: str
    settings: dict
    archived: bool
    created_at: str
    updated_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Workspace":
        return Workspace(
            r["id"], r["user_id"], r["name"], r["description"],
            _json(r["settings_json"]), bool(r["archived"]),
            r["created_at"], r["updated_at"],
        )


@dataclass
class ApiKey:
    """Метаданные ключа. Сам секрет в объект не попадает — только по запросу."""

    id: int
    user_id: int
    label: str
    provider: str
    base_url: str
    has_secret: bool
    meta: dict
    created_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "ApiKey":
        return ApiKey(
            r["id"], r["user_id"], r["label"], r["provider"], r["base_url"],
            r["secret_blob"] is not None, _json(r["meta_json"]), r["created_at"],
        )


@dataclass
class Agent:
    id: int
    workspace_id: int
    name: str
    role: str
    system_prompt: str
    api_key_id: int | None
    provider: str
    model: str
    params: dict
    enabled: bool
    status: str
    is_supervisor: bool
    created_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Agent":
        return Agent(
            r["id"], r["workspace_id"], r["name"], r["role"], r["system_prompt"],
            r["api_key_id"], r["provider"], r["model"], _json(r["params_json"]),
            bool(r["enabled"]), r["status"], bool(r["is_supervisor"]), r["created_at"],
        )

    @property
    def temperature(self) -> float:
        return float(self.params.get("temperature", 0.7))

    @property
    def max_tokens(self) -> int:
        return int(self.params.get("max_tokens", 2048))

    @property
    def tools(self) -> list[str]:
        return list(self.params.get("tools", []))


@dataclass
class Task:
    id: int
    workspace_id: int
    title: str
    description: str
    status: str
    result_format: str
    token_limit: int | None
    created_at: str
    updated_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Task":
        return Task(
            r["id"], r["workspace_id"], r["title"], r["description"], r["status"],
            r["result_format"], r["token_limit"], r["created_at"], r["updated_at"],
        )


@dataclass
class Subtask:
    id: int
    task_id: int
    agent_id: int | None
    title: str
    description: str
    status: str
    order_index: int
    depends_on: str
    result: str
    rework_count: int
    tokens_in: int
    tokens_out: int
    cost_usd: float
    created_at: str
    updated_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Subtask":
        return Subtask(
            r["id"], r["task_id"], r["agent_id"], r["title"], r["description"],
            r["status"], r["order_index"], r["depends_on"], r["result"],
            r["rework_count"], r["tokens_in"], r["tokens_out"], r["cost_usd"],
            r["created_at"], r["updated_at"],
        )


@dataclass
class Report:
    id: int
    workspace_id: int
    task_id: int | None
    subtask_id: int | None
    agent_id: int | None
    content: str
    confidence: float | None
    tokens_in: int
    tokens_out: int
    cost_usd: float
    reviewed: bool
    review_verdict: str
    review_notes: str
    created_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Report":
        return Report(
            r["id"], r["workspace_id"], r["task_id"], r["subtask_id"], r["agent_id"],
            r["content"], r["confidence"], r["tokens_in"], r["tokens_out"],
            r["cost_usd"], bool(r["reviewed"]), r["review_verdict"],
            r["review_notes"], r["created_at"],
        )


@dataclass
class Summary:
    id: int
    workspace_id: int
    task_id: int | None
    content: str
    trigger: str
    delivered_to: str
    created_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Summary":
        return Summary(
            r["id"], r["workspace_id"], r["task_id"], r["content"],
            r["trigger"], r["delivered_to"], r["created_at"],
        )


@dataclass
class Incident:
    id: int
    workspace_id: int
    task_id: int | None
    subtask_id: int | None
    report_id: int | None
    kind: str
    severity: str
    description: str
    status: str
    resolution: str
    created_at: str
    resolved_at: str | None

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Incident":
        return Incident(
            r["id"], r["workspace_id"], r["task_id"], r["subtask_id"], r["report_id"],
            r["kind"], r["severity"], r["description"], r["status"], r["resolution"],
            r["created_at"], r["resolved_at"],
        )


@dataclass
class Budget:
    id: int
    scope: str
    scope_id: int
    token_limit: int | None
    cost_limit_usd: float | None
    tokens_used: int
    cost_used_usd: float
    alert_threshold: float
    alerted: bool
    updated_at: str

    @staticmethod
    def from_row(r: sqlite3.Row) -> "Budget":
        return Budget(
            r["id"], r["scope"], r["scope_id"], r["token_limit"], r["cost_limit_usd"],
            r["tokens_used"], r["cost_used_usd"], r["alert_threshold"],
            bool(r["alerted"]), r["updated_at"],
        )

    def ratio(self) -> float:
        """Доля израсходованного бюджета (максимум из токенов и денег)."""
        parts: list[float] = []
        if self.token_limit:
            parts.append(self.tokens_used / self.token_limit)
        if self.cost_limit_usd:
            parts.append(self.cost_used_usd / self.cost_limit_usd)
        return max(parts) if parts else 0.0


def dumps(obj: Any) -> str:
    """Безопасная сериализация словарей настроек в TEXT-колонки."""
    return json.dumps(obj, ensure_ascii=False)
````

### `storage/repositories.py`

*650 строк*

````python
"""Репозитории — единственная точка доступа к БД.

UI и ядро никогда не пишут SQL напрямую: это упрощает будущую замену
хранилища и гарантирует, что секреты шифруются в одном месте.
"""

from __future__ import annotations

from typing import Any

from core.security.crypto import (
    SecretBox,
    Session,
    derive_master_key,
    hash_password,
    new_salt,
    verify_password,
)
from storage.db import Database, utcnow
from storage.models import (
    Agent,
    ApiKey,
    Budget,
    Incident,
    Report,
    Subtask,
    Summary,
    Task,
    User,
    Workspace,
    dumps,
)


class UserRepo:
    """Локальные профили: регистрация, вход, смена пароля."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def list_usernames(self) -> list[str]:
        return [r["username"] for r in self.db.query("SELECT username FROM users ORDER BY username")]

    def exists(self, username: str) -> bool:
        return self.db.query_one("SELECT 1 FROM users WHERE username = ?", (username,)) is not None

    def create(self, username: str, password: str) -> Session:
        """Создаёт профиль и сразу возвращает открытую сессию."""
        verify_salt, kdf_salt = new_salt(), new_salt()
        uid = self.db.insert(
            "INSERT INTO users(username, password_hash, verify_salt, kdf_salt, created_at) "
            "VALUES (?,?,?,?,?)",
            (username, hash_password(password, verify_salt), verify_salt, kdf_salt, utcnow()),
        )
        return Session(uid, username, SecretBox(derive_master_key(password, kdf_salt)))

    def authenticate(self, username: str, password: str) -> Session | None:
        """Проверяет пароль и выводит мастер-ключ шифрования."""
        row = self.db.query_one("SELECT * FROM users WHERE username = ?", (username,))
        if not row or not verify_password(password, row["verify_salt"], row["password_hash"]):
            return None
        key = derive_master_key(password, row["kdf_salt"])
        return Session(row["id"], row["username"], SecretBox(key))

    def get(self, user_id: int) -> User | None:
        row = self.db.query_one("SELECT * FROM users WHERE id = ?", (user_id,))
        return User.from_row(row) if row else None

    def change_password(self, session: Session, old_password: str, new_password: str) -> bool:
        """Меняет пароль и ПЕРЕШИФРОВЫВАЕТ все API-ключи новым мастер-ключом."""
        row = self.db.query_one("SELECT * FROM users WHERE id = ?", (session.user_id,))
        if not row or not verify_password(old_password, row["verify_salt"], row["password_hash"]):
            return False

        old_box = session.box
        new_verify_salt, new_kdf_salt = new_salt(), new_salt()
        new_box = SecretBox(derive_master_key(new_password, new_kdf_salt))

        # Сначала расшифровываем всё старым ключом, затем пишем одной транзакцией.
        rows = self.db.query(
            "SELECT id, secret_blob FROM api_keys WHERE user_id = ? AND secret_blob IS NOT NULL",
            (session.user_id,),
        )
        reencrypted = [
            (new_box.encrypt(old_box.decrypt(r["secret_blob"])), r["id"]) for r in rows
        ]
        for blob, key_id in reencrypted:
            self.db.execute("UPDATE api_keys SET secret_blob = ? WHERE id = ?", (blob, key_id))
        self.db.execute(
            "UPDATE users SET password_hash = ?, verify_salt = ?, kdf_salt = ? WHERE id = ?",
            (hash_password(new_password, new_verify_salt), new_verify_salt,
             new_kdf_salt, session.user_id),
        )
        session.box = new_box
        return True

    def save_settings(self, user_id: int, settings: dict) -> None:
        self.db.execute(
            "UPDATE users SET settings_json = ? WHERE id = ?", (dumps(settings), user_id)
        )


class WorkspaceRepo:
    """Воркспейсы = параллельные проекты со своим набором агентов."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def list(self, user_id: int, include_archived: bool = False) -> list[Workspace]:
        sql = "SELECT * FROM workspaces WHERE user_id = ?"
        if not include_archived:
            sql += " AND archived = 0"
        sql += " ORDER BY updated_at DESC"
        return [Workspace.from_row(r) for r in self.db.query(sql, (user_id,))]

    def get(self, ws_id: int) -> Workspace | None:
        row = self.db.query_one("SELECT * FROM workspaces WHERE id = ?", (ws_id,))
        return Workspace.from_row(row) if row else None

    def create(self, user_id: int, name: str, description: str, settings: dict) -> Workspace:
        now = utcnow()
        ws_id = self.db.insert(
            "INSERT INTO workspaces(user_id, name, description, settings_json, created_at, updated_at) "
            "VALUES (?,?,?,?,?,?)",
            (user_id, name, description, dumps(settings), now, now),
        )
        return self.get(ws_id)  # type: ignore[return-value]

    def update(self, ws_id: int, **fields: Any) -> None:
        allowed = {"name", "description", "archived"}
        sets, params = [], []
        for k, v in fields.items():
            if k in allowed:
                sets.append(f"{k} = ?")
                params.append(v)
            elif k == "settings":
                sets.append("settings_json = ?")
                params.append(dumps(v))
        if not sets:
            return
        sets.append("updated_at = ?")
        params.extend([utcnow(), ws_id])
        self.db.execute(f"UPDATE workspaces SET {', '.join(sets)} WHERE id = ?", params)

    def delete(self, ws_id: int) -> None:
        self.db.execute("DELETE FROM workspaces WHERE id = ?", (ws_id,))

    def agent_count(self, ws_id: int) -> int:
        row = self.db.query_one("SELECT COUNT(*) c FROM agents WHERE workspace_id = ?", (ws_id,))
        return int(row["c"]) if row else 0


class ApiKeyRepo:
    """Хранилище API-ключей. Секрет шифруется мастер-ключом сессии."""

    def __init__(self, db: Database, session: Session) -> None:
        self.db = db
        self.session = session

    def list(self) -> list[ApiKey]:
        rows = self.db.query(
            "SELECT * FROM api_keys WHERE user_id = ? ORDER BY provider, label",
            (self.session.user_id,),
        )
        return [ApiKey.from_row(r) for r in rows]

    def get(self, key_id: int) -> ApiKey | None:
        row = self.db.query_one(
            "SELECT * FROM api_keys WHERE id = ? AND user_id = ?",
            (key_id, self.session.user_id),
        )
        return ApiKey.from_row(row) if row else None

    def reveal(self, key_id: int) -> str:
        """Расшифровывает секрет. Вызывается только в момент запроса к провайдеру."""
        row = self.db.query_one(
            "SELECT secret_blob FROM api_keys WHERE id = ? AND user_id = ?",
            (key_id, self.session.user_id),
        )
        if not row or row["secret_blob"] is None:
            return ""
        return self.session.box.decrypt(row["secret_blob"])

    def create(self, label: str, provider: str, secret: str,
               base_url: str = "", meta: dict | None = None) -> ApiKey:
        blob = self.session.box.encrypt(secret) if secret else None
        key_id = self.db.insert(
            "INSERT INTO api_keys(user_id, label, provider, base_url, secret_blob, "
            "meta_json, created_at) VALUES (?,?,?,?,?,?,?)",
            (self.session.user_id, label, provider, base_url, blob,
             dumps(meta or {}), utcnow()),
        )
        return self.get(key_id)  # type: ignore[return-value]

    def update(self, key_id: int, label: str, base_url: str,
               secret: str | None = None, meta: dict | None = None) -> None:
        sets = ["label = ?", "base_url = ?"]
        params: list[Any] = [label, base_url]
        if secret is not None:
            sets.append("secret_blob = ?")
            params.append(self.session.box.encrypt(secret) if secret else None)
        if meta is not None:
            sets.append("meta_json = ?")
            params.append(dumps(meta))
        params.extend([key_id, self.session.user_id])
        self.db.execute(
            f"UPDATE api_keys SET {', '.join(sets)} WHERE id = ? AND user_id = ?", params
        )

    def delete(self, key_id: int) -> None:
        self.db.execute(
            "DELETE FROM api_keys WHERE id = ? AND user_id = ?", (key_id, self.session.user_id)
        )


class AgentRepo:
    def __init__(self, db: Database) -> None:
        self.db = db

    def list(self, ws_id: int) -> list[Agent]:
        rows = self.db.query(
            "SELECT * FROM agents WHERE workspace_id = ? ORDER BY is_supervisor DESC, id",
            (ws_id,),
        )
        return [Agent.from_row(r) for r in rows]

    def get(self, agent_id: int) -> Agent | None:
        row = self.db.query_one("SELECT * FROM agents WHERE id = ?", (agent_id,))
        return Agent.from_row(row) if row else None

    def create(self, ws_id: int, name: str, role: str, system_prompt: str,
               api_key_id: int | None, provider: str, model: str,
               params: dict, is_supervisor: bool = False) -> Agent:
        agent_id = self.db.insert(
            "INSERT INTO agents(workspace_id, name, role, system_prompt, api_key_id, provider, "
            "model, params_json, is_supervisor, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (ws_id, name, role, system_prompt, api_key_id, provider, model,
             dumps(params), int(is_supervisor), utcnow()),
        )
        return self.get(agent_id)  # type: ignore[return-value]

    def update(self, agent_id: int, **fields: Any) -> None:
        allowed = {"name", "role", "system_prompt", "api_key_id", "provider",
                   "model", "enabled", "status", "is_supervisor"}
        sets, params = [], []
        for k, v in fields.items():
            if k in allowed:
                sets.append(f"{k} = ?")
                params.append(int(v) if isinstance(v, bool) else v)
            elif k == "params":
                sets.append("params_json = ?")
                params.append(dumps(v))
        if not sets:
            return
        params.append(agent_id)
        self.db.execute(f"UPDATE agents SET {', '.join(sets)} WHERE id = ?", params)

    def set_status(self, agent_id: int, status: str) -> None:
        self.db.execute("UPDATE agents SET status = ? WHERE id = ?", (status, agent_id))

    def delete(self, agent_id: int) -> None:
        self.db.execute("DELETE FROM agents WHERE id = ?", (agent_id,))


class TaskRepo:
    """Задачи и подзадачи воркспейса."""

    def __init__(self, db: Database) -> None:
        self.db = db

    # -- задачи --------------------------------------------------------------
    def current(self, ws_id: int) -> Task | None:
        """Последняя (активная) задача воркспейса."""
        row = self.db.query_one(
            "SELECT * FROM tasks WHERE workspace_id = ? ORDER BY id DESC LIMIT 1", (ws_id,)
        )
        return Task.from_row(row) if row else None

    def get(self, task_id: int) -> Task | None:
        row = self.db.query_one("SELECT * FROM tasks WHERE id = ?", (task_id,))
        return Task.from_row(row) if row else None

    def create(self, ws_id: int, title: str, description: str,
               result_format: str = "auto", token_limit: int | None = None) -> Task:
        now = utcnow()
        task_id = self.db.insert(
            "INSERT INTO tasks(workspace_id, title, description, result_format, token_limit, "
            "created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
            (ws_id, title, description, result_format, token_limit, now, now),
        )
        return self.get(task_id)  # type: ignore[return-value]

    def update(self, task_id: int, **fields: Any) -> None:
        allowed = {"title", "description", "status", "result_format", "token_limit"}
        sets = [f"{k} = ?" for k in fields if k in allowed]
        params = [v for k, v in fields.items() if k in allowed]
        if not sets:
            return
        sets.append("updated_at = ?")
        params.extend([utcnow(), task_id])
        self.db.execute(f"UPDATE tasks SET {', '.join(sets)} WHERE id = ?", params)

    # -- подзадачи -----------------------------------------------------------
    def subtasks(self, task_id: int) -> list[Subtask]:
        rows = self.db.query(
            "SELECT * FROM subtasks WHERE task_id = ? ORDER BY order_index, id", (task_id,)
        )
        return [Subtask.from_row(r) for r in rows]

    def get_subtask(self, subtask_id: int) -> Subtask | None:
        row = self.db.query_one("SELECT * FROM subtasks WHERE id = ?", (subtask_id,))
        return Subtask.from_row(row) if row else None

    def add_subtask(self, task_id: int, title: str, description: str = "",
                    agent_id: int | None = None) -> Subtask:
        row = self.db.query_one(
            "SELECT COALESCE(MAX(order_index), -1) + 1 AS n FROM subtasks WHERE task_id = ?",
            (task_id,),
        )
        now = utcnow()
        sid = self.db.insert(
            "INSERT INTO subtasks(task_id, agent_id, title, description, order_index, "
            "created_at, updated_at) VALUES (?,?,?,?,?,?,?)",
            (task_id, agent_id, title, description, int(row["n"]) if row else 0, now, now),
        )
        return self.get_subtask(sid)  # type: ignore[return-value]

    def update_subtask(self, subtask_id: int, **fields: Any) -> None:
        allowed = {"agent_id", "title", "description", "status", "order_index",
                   "depends_on", "result", "rework_count", "tokens_in",
                   "tokens_out", "cost_usd"}
        sets = [f"{k} = ?" for k in fields if k in allowed]
        params = [v for k, v in fields.items() if k in allowed]
        if not sets:
            return
        sets.append("updated_at = ?")
        params.extend([utcnow(), subtask_id])
        self.db.execute(f"UPDATE subtasks SET {', '.join(sets)} WHERE id = ?", params)

    def delete_subtask(self, subtask_id: int) -> None:
        self.db.execute("DELETE FROM subtasks WHERE id = ?", (subtask_id,))

    def reorder(self, ordered_ids: list[int]) -> None:
        """Переписывает order_index по переданному порядку id."""
        self.db.executemany(
            "UPDATE subtasks SET order_index = ? WHERE id = ?",
            [(i, sid) for i, sid in enumerate(ordered_ids)],
        )


class ReportRepo:
    """Отчёты агентов и сводки супервайзера (этапы 4-5)."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def add_report(self, ws_id: int, task_id: int | None, subtask_id: int | None,
                   agent_id: int | None, content: str, confidence: float | None = None,
                   tokens_in: int = 0, tokens_out: int = 0, cost_usd: float = 0.0) -> int:
        return self.db.insert(
            "INSERT INTO reports(workspace_id, task_id, subtask_id, agent_id, content, "
            "confidence, tokens_in, tokens_out, cost_usd, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (ws_id, task_id, subtask_id, agent_id, content, confidence,
             tokens_in, tokens_out, cost_usd, utcnow()),
        )

    def list_reports(self, ws_id: int, limit: int = 100) -> list[Report]:
        rows = self.db.query(
            "SELECT * FROM reports WHERE workspace_id = ? ORDER BY id DESC LIMIT ?",
            (ws_id, limit),
        )
        return [Report.from_row(r) for r in rows]

    def unreviewed(self, ws_id: int) -> list[Report]:
        rows = self.db.query(
            "SELECT * FROM reports WHERE workspace_id = ? AND reviewed = 0 ORDER BY id",
            (ws_id,),
        )
        return [Report.from_row(r) for r in rows]

    def mark_reviewed(self, report_id: int, verdict: str, notes: str = "") -> None:
        self.db.execute(
            "UPDATE reports SET reviewed = 1, review_verdict = ?, review_notes = ? WHERE id = ?",
            (verdict, notes, report_id),
        )

    def add_summary(self, ws_id: int, task_id: int | None, content: str,
                    trigger: str, delivered_to: list[int]) -> int:
        return self.db.insert(
            "INSERT INTO summaries(workspace_id, task_id, content, trigger, delivered_to, "
            "created_at) VALUES (?,?,?,?,?,?)",
            (ws_id, task_id, content, trigger,
             ",".join(str(i) for i in delivered_to), utcnow()),
        )

    def list_summaries(self, ws_id: int, limit: int = 50) -> list[Summary]:
        rows = self.db.query(
            "SELECT * FROM summaries WHERE workspace_id = ? ORDER BY id DESC LIMIT ?",
            (ws_id, limit),
        )
        return [Summary.from_row(r) for r in rows]


class IncidentRepo:
    """История инцидентов: что супервайзер счёл ошибкой и чем это кончилось."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, ws_id: int, kind: str, description: str, severity: str = "medium",
            task_id: int | None = None, subtask_id: int | None = None,
            report_id: int | None = None) -> int:
        return self.db.insert(
            "INSERT INTO incidents(workspace_id, task_id, subtask_id, report_id, kind, "
            "severity, description, created_at) VALUES (?,?,?,?,?,?,?,?)",
            (ws_id, task_id, subtask_id, report_id, kind, severity, description, utcnow()),
        )

    def list(self, ws_id: int, limit: int = 100) -> list[Incident]:
        rows = self.db.query(
            "SELECT * FROM incidents WHERE workspace_id = ? ORDER BY id DESC LIMIT ?",
            (ws_id, limit),
        )
        return [Incident.from_row(r) for r in rows]

    def resolve_for_subtask(self, subtask_id: int, resolution: str) -> int:
        """Закрывает открытые инциденты подзадачи — например, после доработки.

        Возвращает количество закрытых записей.
        """
        cur = self.db.execute(
            "UPDATE incidents SET status = 'resolved', resolution = ?, resolved_at = ? "
            "WHERE subtask_id = ? AND status IN ('open', 'escalated')",
            (resolution, utcnow(), subtask_id),
        )
        return cur.rowcount or 0

    def resolve(self, incident_id: int, status: str, resolution: str) -> None:
        self.db.execute(
            "UPDATE incidents SET status = ?, resolution = ?, resolved_at = ? WHERE id = ?",
            (status, resolution, utcnow(), incident_id),
        )


class ApprovalRepo:
    """Точки human-in-the-loop: заданные вопросы и принятые решения."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def create(self, ws_id: int, task_id: int | None, reason: str,
               payload: dict) -> int:
        return self.db.insert(
            "INSERT INTO approvals(workspace_id, task_id, reason, payload_json, created_at) "
            "VALUES (?,?,?,?,?)",
            (ws_id, task_id, reason, dumps(payload), utcnow()),
        )

    def decide(self, approval_id: int, decision: str, comment: str = "") -> None:
        self.db.execute(
            "UPDATE approvals SET decision = ?, comment = ?, decided_at = ? WHERE id = ?",
            (decision, comment, utcnow(), approval_id),
        )

    def history(self, ws_id: int, limit: int = 100) -> list[dict]:
        """История решений, новые сверху — для вкладки супервайзера."""
        rows = self.db.query(
            "SELECT * FROM approvals WHERE workspace_id = ? ORDER BY id DESC LIMIT ?",
            (ws_id, limit),
        )
        return [dict(r) for r in rows]

    def pending_count(self, ws_id: int) -> int:
        row = self.db.query_one(
            "SELECT COUNT(*) n FROM approvals WHERE workspace_id = ? AND decision = ''",
            (ws_id,),
        )
        return int(row["n"]) if row else 0


class BudgetRepo:
    """Лимиты по токенам и деньгам + журнал расхода."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def get(self, scope: str, scope_id: int) -> Budget | None:
        row = self.db.query_one(
            "SELECT * FROM budgets WHERE scope = ? AND scope_id = ?", (scope, scope_id)
        )
        return Budget.from_row(row) if row else None

    def upsert(self, scope: str, scope_id: int, token_limit: int | None,
               cost_limit_usd: float | None, alert_threshold: float = 0.8) -> None:
        self.db.execute(
            "INSERT INTO budgets(scope, scope_id, token_limit, cost_limit_usd, "
            "alert_threshold, updated_at) VALUES (?,?,?,?,?,?) "
            "ON CONFLICT(scope, scope_id) DO UPDATE SET token_limit = excluded.token_limit, "
            "cost_limit_usd = excluded.cost_limit_usd, "
            "alert_threshold = excluded.alert_threshold, updated_at = excluded.updated_at",
            (scope, scope_id, token_limit, cost_limit_usd, alert_threshold, utcnow()),
        )

    def add_usage(self, scope: str, scope_id: int, tokens: int, cost: float) -> None:
        self.db.execute(
            "UPDATE budgets SET tokens_used = tokens_used + ?, cost_used_usd = cost_used_usd + ?, "
            "updated_at = ? WHERE scope = ? AND scope_id = ?",
            (tokens, cost, utcnow(), scope, scope_id),
        )

    def log_call(self, ws_id: int | None, task_id: int | None, subtask_id: int | None,
                 agent_id: int | None, provider: str, model: str,
                 tokens_in: int, tokens_out: int, cost: float) -> None:
        self.db.execute(
            "INSERT INTO usage_log(workspace_id, task_id, subtask_id, agent_id, provider, "
            "model, tokens_in, tokens_out, cost_usd, created_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
            (ws_id, task_id, subtask_id, agent_id, provider, model,
             tokens_in, tokens_out, cost, utcnow()),
        )

    def workspace_totals(self, ws_id: int) -> tuple[int, float]:
        row = self.db.query_one(
            "SELECT COALESCE(SUM(tokens_in + tokens_out), 0) t, COALESCE(SUM(cost_usd), 0) c "
            "FROM usage_log WHERE workspace_id = ?",
            (ws_id,),
        )
        return (int(row["t"]), float(row["c"])) if row else (0, 0.0)

    def usage_series(self, ws_id: int, limit: int = 300) -> list[tuple[str, int, float]]:
        """Хронология вызовов: (время, токены, стоимость).

        Возвращает последние ``limit`` записей в прямом порядке — из них
        дашборд строит кумулятивные кривые расхода.
        """
        rows = self.db.query(
            "SELECT created_at, tokens_in + tokens_out AS tokens, cost_usd FROM ("
            "  SELECT created_at, tokens_in, tokens_out, cost_usd FROM usage_log "
            "  WHERE workspace_id = ? ORDER BY id DESC LIMIT ?"
            ") ORDER BY created_at",
            (ws_id, limit),
        )
        return [(r["created_at"], int(r["tokens"]), float(r["cost_usd"])) for r in rows]

    def usage_by_agent(self, ws_id: int) -> list[tuple[int | None, int, float]]:
        """Расход в разрезе агентов: (agent_id, токены, стоимость)."""
        rows = self.db.query(
            "SELECT agent_id, COALESCE(SUM(tokens_in + tokens_out), 0) t, "
            "COALESCE(SUM(cost_usd), 0) c FROM usage_log WHERE workspace_id = ? "
            "GROUP BY agent_id ORDER BY t DESC",
            (ws_id,),
        )
        return [(r["agent_id"], int(r["t"]), float(r["c"])) for r in rows]

    def task_totals(self, task_id: int) -> tuple[int, float]:
        """Расход по конкретной задаче."""
        row = self.db.query_one(
            "SELECT COALESCE(SUM(tokens_in + tokens_out), 0) t, COALESCE(SUM(cost_usd), 0) c "
            "FROM usage_log WHERE task_id = ?",
            (task_id,),
        )
        return (int(row["t"]), float(row["c"])) if row else (0, 0.0)

    def agent_totals(self, ws_id: int) -> dict[int, tuple[int, float]]:
        """Расход по каждому агенту воркспейса."""
        rows = self.db.query(
            "SELECT agent_id, COALESCE(SUM(tokens_in + tokens_out), 0) t, "
            "COALESCE(SUM(cost_usd), 0) c FROM usage_log "
            "WHERE workspace_id = ? AND agent_id IS NOT NULL GROUP BY agent_id",
            (ws_id,),
        )
        return {int(r["agent_id"]): (int(r["t"]), float(r["c"])) for r in rows}

    def list_limits(self, scope: str, scope_ids: list[int]) -> dict[int, Budget]:
        """Лимиты нескольких объектов одного типа одним запросом."""
        if not scope_ids:
            return {}
        marks = ",".join("?" * len(scope_ids))
        rows = self.db.query(
            f"SELECT * FROM budgets WHERE scope = ? AND scope_id IN ({marks})",
            [scope, *scope_ids],
        )
        return {int(r["scope_id"]): Budget.from_row(r) for r in rows}

    def delete_limit(self, scope: str, scope_id: int) -> None:
        self.db.execute("DELETE FROM budgets WHERE scope = ? AND scope_id = ?",
                        (scope, scope_id))

    def sync_used(self, scope: str, scope_id: int, tokens: int, cost: float) -> None:
        """Записывает фактический расход в строку лимита (для отображения)."""
        self.db.execute(
            "UPDATE budgets SET tokens_used = ?, cost_used_usd = ?, updated_at = ? "
            "WHERE scope = ? AND scope_id = ?",
            (tokens, cost, utcnow(), scope, scope_id),
        )

    def incident_counts(self, ws_id: int) -> dict[str, int]:
        """Инциденты по статусам — для плашки «требуют решения»."""
        rows = self.db.query(
            "SELECT status, COUNT(*) n FROM incidents WHERE workspace_id = ? GROUP BY status",
            (ws_id,),
        )
        return {r["status"]: int(r["n"]) for r in rows}


class MessageRepo:
    """Приватная история агента. Выборки ВСЕГДА фильтруются по agent_id,
    поэтому один агент физически не может прочитать контекст другого."""

    def __init__(self, db: Database) -> None:
        self.db = db

    def add(self, agent_id: int, role: str, content: str, subtask_id: int | None = None,
            tool_name: str = "", tool_call_id: str = "", tokens: int = 0) -> int:
        return self.db.insert(
            "INSERT INTO messages(agent_id, subtask_id, role, content, tool_name, "
            "tool_call_id, tokens, created_at) VALUES (?,?,?,?,?,?,?,?)",
            (agent_id, subtask_id, role, content, tool_name, tool_call_id, tokens, utcnow()),
        )

    def history(self, agent_id: int, subtask_id: int | None = None,
                limit: int = 200) -> list[dict]:
        sql = "SELECT * FROM messages WHERE agent_id = ?"
        params: list[Any] = [agent_id]
        if subtask_id is not None:
            sql += " AND subtask_id = ?"
            params.append(subtask_id)
        sql += " ORDER BY id LIMIT ?"
        params.append(limit)
        return [dict(r) for r in self.db.query(sql, params)]

    def clear(self, agent_id: int) -> None:
        self.db.execute("DELETE FROM messages WHERE agent_id = ?", (agent_id,))


class Repos:
    """Агрегатор репозиториев — удобно передавать одним объектом в UI."""

    def __init__(self, db: Database, session: Session) -> None:
        self.db = db
        self.session = session
        self.users = UserRepo(db)
        self.workspaces = WorkspaceRepo(db)
        self.keys = ApiKeyRepo(db, session)
        self.agents = AgentRepo(db)
        self.tasks = TaskRepo(db)
        self.reports = ReportRepo(db)
        self.incidents = IncidentRepo(db)
        self.budgets = BudgetRepo(db)
        self.approvals = ApprovalRepo(db)
        self.messages = MessageRepo(db)
````


## Безопасность

### `core/security/crypto.py`

*164 строк*

````python
"""Криптография профиля: вывод мастер-ключа и шифрование секретов.

Схема (ответ на вопросы 4 и 5):

* Пароль профиля — единственный секрет, который вводит пользователь.
* ``Argon2id(password, salt)`` → 32-байтовый мастер-ключ. Ключ живёт только
  в оперативной памяти и никогда не пишется на диск.
* Проверка пароля при входе — по хэшу ``Argon2id(password, verify_salt)``,
  сравнение выполняется в постоянном времени.
* API-ключи шифруются ``AES-256-GCM`` мастер-ключом. На диск ложится
  ``nonce(12) || ciphertext || tag`` — сама БД остаётся обычным SQLite,
  открытым для чтения инструментами, но секреты в ней нечитаемы.

Зависимость только одна — ``cryptography``. Argon2id берётся из неё
(версия ≥ 42 с поддержкой KDF), при её отсутствии — из ``argon2-cffi``.
"""

from __future__ import annotations

import hmac
import os
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Параметры Argon2id: ~64 МБ памяти, 3 прохода — разумный компромисс
# между стойкостью и временем отклика десктопного логина (~0.2-0.5 с).
ARGON2_TIME_COST = 3
ARGON2_MEMORY_KIB = 64 * 1024
ARGON2_LANES = 4
KEY_LENGTH = 32
SALT_LENGTH = 16
NONCE_LENGTH = 12


def _derive_raw(password: bytes, salt: bytes, length: int = KEY_LENGTH) -> bytes:
    """Argon2id через ``cryptography`` с откатом на ``argon2-cffi``."""
    try:
        from cryptography.hazmat.primitives.kdf.argon2 import Argon2id

        kdf = Argon2id(
            salt=salt,
            length=length,
            iterations=ARGON2_TIME_COST,
            lanes=ARGON2_LANES,
            memory_cost=ARGON2_MEMORY_KIB,
        )
        return kdf.derive(password)
    except ImportError:  # pragma: no cover — путь для старых cryptography
        from argon2.low_level import Type, hash_secret_raw

        return hash_secret_raw(
            secret=password,
            salt=salt,
            time_cost=ARGON2_TIME_COST,
            memory_cost=ARGON2_MEMORY_KIB,
            parallelism=ARGON2_LANES,
            hash_len=length,
            type=Type.ID,
        )


def new_salt() -> bytes:
    """Случайная соль для KDF."""
    return os.urandom(SALT_LENGTH)


def derive_master_key(password: str, salt: bytes) -> bytes:
    """Выводит 32-байтовый мастер-ключ шифрования из пароля профиля."""
    return _derive_raw(password.encode("utf-8"), salt)


def hash_password(password: str, salt: bytes) -> bytes:
    """Хэш для проверки пароля. Соль намеренно ОТЛИЧАЕТСЯ от соли мастер-ключа."""
    return _derive_raw(password.encode("utf-8"), salt)


def verify_password(password: str, salt: bytes, expected_hash: bytes) -> bool:
    """Сравнение хэшей в постоянном времени."""
    return hmac.compare_digest(hash_password(password, salt), expected_hash)


class SecretBox:
    """Шифрование/расшифровка коротких секретов (API-ключей) на мастер-ключе."""

    def __init__(self, master_key: bytes) -> None:
        if len(master_key) != KEY_LENGTH:
            raise ValueError("Мастер-ключ должен быть длиной 32 байта")
        self._aead = AESGCM(master_key)

    def encrypt(self, plaintext: str, associated: str = "") -> bytes:
        """Возвращает ``nonce || ciphertext||tag``."""
        nonce = os.urandom(NONCE_LENGTH)
        blob = self._aead.encrypt(
            nonce, plaintext.encode("utf-8"), associated.encode("utf-8") or None
        )
        return nonce + blob

    def decrypt(self, payload: bytes, associated: str = "") -> str:
        """Обратная операция; бросает исключение при неверном ключе/порче данных."""
        nonce, blob = payload[:NONCE_LENGTH], payload[NONCE_LENGTH:]
        raw = self._aead.decrypt(nonce, blob, associated.encode("utf-8") or None)
        return raw.decode("utf-8")


@dataclass
class Session:
    """Активная сессия пользователя: кто вошёл и на каком мастер-ключе работаем.

    Объект передаётся в репозитории, чтобы они могли прозрачно
    шифровать/расшифровывать поля с секретами.
    """

    user_id: int
    username: str
    box: SecretBox

    def wipe(self) -> None:
        """Обнуляет ссылку на ключ при выходе из профиля."""
        self.box = None  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# Необязательная интеграция с хранилищем секретов ОС («запомнить пароль»)
# ---------------------------------------------------------------------------

_KEYRING_SERVICE = "ai-orchestrator"


def keyring_available() -> bool:
    try:
        import keyring  # noqa: F401

        return True
    except Exception:  # noqa: BLE001
        return False


def keyring_store_password(username: str, password: str) -> bool:
    try:
        import keyring

        keyring.set_password(_KEYRING_SERVICE, username, password)
        return True
    except Exception:  # noqa: BLE001
        return False


def keyring_get_password(username: str) -> str | None:
    try:
        import keyring

        return keyring.get_password(_KEYRING_SERVICE, username)
    except Exception:  # noqa: BLE001
        return None


def keyring_delete_password(username: str) -> None:
    try:
        import keyring

        keyring.delete_password(_KEYRING_SERVICE, username)
    except Exception:  # noqa: BLE001
        pass
````


## Провайдеры моделей

### `providers/base.py`

*136 строк*

````python
"""Единый интерфейс LLM-провайдера.

Все провайдеры (OpenAI, Anthropic, Gemini, Groq, OpenRouter, Ollama, HF)
приводятся к одному набору типов, чтобы ядро агентов ничего не знало
о различиях в их HTTP-API — включая формат tool-calling.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncIterator


@dataclass
class ToolCall:
    """Запрос модели на вызов инструмента."""

    id: str
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def parse_args(raw: Any) -> dict[str, Any]:
        if isinstance(raw, dict):
            return raw
        try:
            return json.loads(raw or "{}")
        except (TypeError, ValueError):
            return {"_raw": str(raw)}


@dataclass
class ChatMessage:
    """Сообщение диалога в нейтральном формате."""

    role: str                         # system | user | assistant | tool
    content: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_call_id: str = ""            # для role="tool"
    name: str = ""


@dataclass
class ToolSpec:
    """Описание инструмента в формате JSON Schema."""

    name: str
    description: str
    parameters: dict[str, Any]


@dataclass
class Usage:
    """Расход токенов за один вызов."""

    input_tokens: int = 0
    output_tokens: int = 0

    @property
    def total(self) -> int:
        return self.input_tokens + self.output_tokens


@dataclass
class CompletionResult:
    """Результат одного обращения к модели."""

    text: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: Usage = field(default_factory=Usage)
    finish_reason: str = ""
    model: str = ""
    raw: dict[str, Any] = field(default_factory=dict)


class ProviderError(RuntimeError):
    """Ошибка обращения к провайдеру с человекочитаемым сообщением."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


class LLMProvider(ABC):
    """Базовый класс провайдера.

    Реализации обязаны быть потокобезопасными в пределах одного asyncio-лупа
    и не хранить состояние диалога — вся история приходит в ``messages``.
    """

    #: строковый идентификатор пресета (см. providers/presets.py)
    key: str = ""

    def __init__(self, api_key: str = "", base_url: str = "", timeout: float = 120.0) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    @abstractmethod
    async def complete(
        self,
        model: str,
        messages: list[ChatMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        tools: list[ToolSpec] | None = None,
    ) -> CompletionResult:
        """Однократный вызов модели."""

    @abstractmethod
    async def list_models(self) -> list[str]:
        """Список доступных моделей (используется в UI и для проверки ключа)."""

    async def stream(
        self,
        model: str,
        messages: list[ChatMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> AsyncIterator[str]:
        """Потоковая генерация. По умолчанию — эмуляция через ``complete``."""
        result = await self.complete(
            model, messages, temperature=temperature, max_tokens=max_tokens
        )
        yield result.text

    async def test(self) -> list[str]:
        """Проверка соединения: возвращает список моделей либо бросает ProviderError."""
        return await self.list_models()

    async def aclose(self) -> None:
        """Освобождение ресурсов (HTTP-клиента)."""
````

### `providers/presets.py`

*122 строк*

````python
"""Пресеты подключения к провайдерам «из коробки».

Пользователю достаточно выбрать провайдера и вставить свой ключ — base URL,
формат API и список популярных моделей подставляются автоматически.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProviderPreset:
    key: str
    title: str
    base_url: str
    api_style: str              # "openai" | "anthropic" | "gemini"
    requires_key: bool = True
    free_tier: bool = False     # бесплатный/условно-бесплатный доступ
    local: bool = False         # работает без интернета
    docs_url: str = ""
    suggested_models: list[str] = field(default_factory=list)
    notes: str = ""


PRESETS: dict[str, ProviderPreset] = {
    "openai": ProviderPreset(
        key="openai",
        title="OpenAI",
        base_url="https://api.openai.com/v1",
        api_style="openai",
        docs_url="https://platform.openai.com/api-keys",
        suggested_models=["gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini", "o4-mini"],
    ),
    "anthropic": ProviderPreset(
        key="anthropic",
        title="Anthropic (Claude)",
        base_url="https://api.anthropic.com/v1",
        api_style="anthropic",
        docs_url="https://console.anthropic.com/settings/keys",
        suggested_models=[
            "claude-sonnet-4-5", "claude-opus-4-1", "claude-3-7-sonnet-latest",
            "claude-3-5-haiku-latest",
        ],
    ),
    "gemini": ProviderPreset(
        key="gemini",
        title="Google Gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        api_style="gemini",
        free_tier=True,
        docs_url="https://aistudio.google.com/app/apikey",
        suggested_models=["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash"],
        notes="Есть бесплатная квота в AI Studio.",
    ),
    "groq": ProviderPreset(
        key="groq",
        title="Groq",
        base_url="https://api.groq.com/openai/v1",
        api_style="openai",
        free_tier=True,
        docs_url="https://console.groq.com/keys",
        suggested_models=[
            "llama-3.3-70b-versatile", "llama-3.1-8b-instant",
            "qwen/qwen3-32b", "deepseek-r1-distill-llama-70b",
        ],
        notes="Очень быстрый инференс, щедрый бесплатный лимит.",
    ),
    "openrouter": ProviderPreset(
        key="openrouter",
        title="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        api_style="openai",
        free_tier=True,
        docs_url="https://openrouter.ai/keys",
        suggested_models=[
            "deepseek/deepseek-chat", "qwen/qwen-2.5-72b-instruct",
            "meta-llama/llama-3.3-70b-instruct", "google/gemma-3-27b-it:free",
        ],
        notes="Единый ключ к десяткам моделей, часть из них бесплатна (суффикс :free).",
    ),
    "ollama": ProviderPreset(
        key="ollama",
        title="Ollama (локально)",
        base_url="http://localhost:11434/v1",
        api_style="openai",
        requires_key=False,
        free_tier=True,
        local=True,
        docs_url="https://ollama.com/download",
        suggested_models=["qwen2.5:7b-instruct", "qwen2.5:14b-instruct",
                          "llama3.1:8b", "mistral-nemo", "gemma3:12b"],
        notes="Работает офлайн. Ключ не нужен — достаточно запущенного сервера Ollama.",
    ),
    "huggingface": ProviderPreset(
        key="huggingface",
        title="Hugging Face Inference",
        base_url="https://router.huggingface.co/v1",
        api_style="openai",
        free_tier=True,
        docs_url="https://huggingface.co/settings/tokens",
        suggested_models=["Qwen/Qwen2.5-72B-Instruct", "meta-llama/Llama-3.3-70B-Instruct"],
        notes="Router HF совместим с OpenAI API. Бесплатная квота ограничена.",
    ),
    "custom": ProviderPreset(
        key="custom",
        title="Свой OpenAI-совместимый endpoint",
        base_url="",
        api_style="openai",
        requires_key=False,
        notes="LM Studio, vLLM, llama.cpp server, корпоративный шлюз и т.п.",
    ),
}


def preset(key: str) -> ProviderPreset:
    """Возвращает пресет; неизвестный ключ трактуется как «custom»."""
    return PRESETS.get(key, PRESETS["custom"])


def preset_list() -> list[ProviderPreset]:
    return list(PRESETS.values())
````

### `providers/openai_compat.py`

*189 строк*

````python
"""Провайдер для всех OpenAI-совместимых API.

Покрывает OpenAI, Groq, OpenRouter, Ollama, Hugging Face Router и любой
локальный сервер (LM Studio, vLLM, llama.cpp) — различается только base_url.
"""

from __future__ import annotations

import json
from typing import Any, AsyncIterator

import httpx

from providers.base import (
    ChatMessage,
    CompletionResult,
    LLMProvider,
    ProviderError,
    ToolCall,
    ToolSpec,
    Usage,
)


class OpenAICompatProvider(LLMProvider):
    """Реализация протокола ``/chat/completions``."""

    key = "openai"

    def __init__(self, api_key: str = "", base_url: str = "",
                 timeout: float = 120.0, extra_headers: dict | None = None) -> None:
        super().__init__(api_key, base_url or "https://api.openai.com/v1", timeout)
        self._extra_headers = extra_headers or {}
        self._client: httpx.AsyncClient | None = None

    # -- служебное -----------------------------------------------------------
    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", **self._extra_headers}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @staticmethod
    def _to_wire(messages: list[ChatMessage]) -> list[dict[str, Any]]:
        """Конвертирует нейтральные сообщения в формат OpenAI."""
        out: list[dict[str, Any]] = []
        for m in messages:
            if m.role == "tool":
                out.append({"role": "tool", "tool_call_id": m.tool_call_id,
                            "content": m.content})
                continue
            item: dict[str, Any] = {"role": m.role, "content": m.content}
            if m.tool_calls:
                item["tool_calls"] = [
                    {"id": tc.id, "type": "function",
                     "function": {"name": tc.name,
                                  "arguments": json.dumps(tc.arguments, ensure_ascii=False)}}
                    for tc in m.tool_calls
                ]
                # OpenAI требует content=None, когда есть tool_calls
                item["content"] = m.content or None
            out.append(item)
        return out

    @staticmethod
    def _tools_payload(tools: list[ToolSpec] | None) -> list[dict] | None:
        if not tools:
            return None
        return [
            {"type": "function",
             "function": {"name": t.name, "description": t.description,
                          "parameters": t.parameters}}
            for t in tools
        ]

    # -- API -----------------------------------------------------------------
    async def complete(self, model: str, messages: list[ChatMessage], *,
                       temperature: float = 0.7, max_tokens: int = 2048,
                       tools: list[ToolSpec] | None = None) -> CompletionResult:
        payload: dict[str, Any] = {
            "model": model,
            "messages": self._to_wire(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        tool_payload = self._tools_payload(tools)
        if tool_payload:
            payload["tools"] = tool_payload
            payload["tool_choice"] = "auto"

        try:
            resp = await self._http().post(
                f"{self.base_url}/chat/completions", headers=self._headers(), json=payload
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc

        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)

        data = resp.json()
        choice = (data.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        calls = [
            ToolCall(id=c.get("id", ""),
                     name=(c.get("function") or {}).get("name", ""),
                     arguments=ToolCall.parse_args((c.get("function") or {}).get("arguments")))
            for c in (msg.get("tool_calls") or [])
        ]
        u = data.get("usage") or {}
        return CompletionResult(
            text=msg.get("content") or "",
            tool_calls=calls,
            usage=Usage(int(u.get("prompt_tokens", 0)), int(u.get("completion_tokens", 0))),
            finish_reason=choice.get("finish_reason", ""),
            model=data.get("model", model),
            raw=data,
        )

    async def stream(self, model: str, messages: list[ChatMessage], *,
                     temperature: float = 0.7,
                     max_tokens: int = 2048) -> AsyncIterator[str]:
        payload = {
            "model": model,
            "messages": self._to_wire(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": True,
        }
        try:
            async with self._http().stream(
                "POST", f"{self.base_url}/chat/completions",
                headers=self._headers(), json=payload
            ) as resp:
                if resp.status_code >= 400:
                    await resp.aread()
                    raise ProviderError(_error_text(resp), resp.status_code)
                async for line in resp.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    chunk = line[5:].strip()
                    if chunk in ("", "[DONE]"):
                        continue
                    try:
                        delta = json.loads(chunk)["choices"][0].get("delta", {})
                    except (ValueError, KeyError, IndexError):
                        continue
                    if delta.get("content"):
                        yield delta["content"]
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc

    async def list_models(self) -> list[str]:
        try:
            resp = await self._http().get(f"{self.base_url}/models", headers=self._headers())
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)
        data = resp.json()
        items = data.get("data", data if isinstance(data, list) else [])
        names = [it.get("id") or it.get("name", "") for it in items if isinstance(it, dict)]
        return sorted(n for n in names if n)


def _error_text(resp: httpx.Response) -> str:
    """Достаёт понятное сообщение об ошибке из ответа провайдера."""
    try:
        data = resp.json()
        err = data.get("error")
        if isinstance(err, dict):
            return f"{resp.status_code}: {err.get('message', resp.text[:200])}"
        if isinstance(err, str):
            return f"{resp.status_code}: {err}"
        if "message" in data:
            return f"{resp.status_code}: {data['message']}"
    except Exception:  # noqa: BLE001
        pass
    return f"{resp.status_code}: {resp.text[:200]}"
````

### `providers/anthropic_provider.py`

*173 строк*

````python
"""Провайдер Anthropic Messages API.

Отличия от OpenAI, которые здесь скрываются:
* системный промпт передаётся отдельным полем ``system``;
* результат инструмента — блок ``tool_result`` внутри сообщения роли ``user``;
* заголовки ``x-api-key`` и ``anthropic-version``.
"""

from __future__ import annotations

from typing import Any, AsyncIterator

import httpx

from providers.base import (
    ChatMessage,
    CompletionResult,
    LLMProvider,
    ProviderError,
    ToolCall,
    ToolSpec,
    Usage,
)

ANTHROPIC_VERSION = "2023-06-01"


class AnthropicProvider(LLMProvider):
    key = "anthropic"

    def __init__(self, api_key: str = "", base_url: str = "",
                 timeout: float = 120.0) -> None:
        super().__init__(api_key, base_url or "https://api.anthropic.com/v1", timeout)
        self._client: httpx.AsyncClient | None = None

    def _headers(self) -> dict[str, str]:
        return {
            "content-type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": ANTHROPIC_VERSION,
        }

    def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @staticmethod
    def _split(messages: list[ChatMessage]) -> tuple[str, list[dict[str, Any]]]:
        """Отделяет system-промпт и собирает тело диалога."""
        system_parts: list[str] = []
        wire: list[dict[str, Any]] = []
        for m in messages:
            if m.role == "system":
                system_parts.append(m.content)
            elif m.role == "tool":
                wire.append({
                    "role": "user",
                    "content": [{"type": "tool_result",
                                 "tool_use_id": m.tool_call_id,
                                 "content": m.content}],
                })
            elif m.role == "assistant" and m.tool_calls:
                blocks: list[dict[str, Any]] = []
                if m.content:
                    blocks.append({"type": "text", "text": m.content})
                blocks += [{"type": "tool_use", "id": tc.id, "name": tc.name,
                            "input": tc.arguments} for tc in m.tool_calls]
                wire.append({"role": "assistant", "content": blocks})
            else:
                wire.append({"role": m.role, "content": m.content})
        return "\n\n".join(p for p in system_parts if p), wire

    async def complete(self, model: str, messages: list[ChatMessage], *,
                       temperature: float = 0.7, max_tokens: int = 2048,
                       tools: list[ToolSpec] | None = None) -> CompletionResult:
        system, wire = self._split(messages)
        payload: dict[str, Any] = {
            "model": model,
            "messages": wire,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system:
            payload["system"] = system
        if tools:
            payload["tools"] = [
                {"name": t.name, "description": t.description, "input_schema": t.parameters}
                for t in tools
            ]

        try:
            resp = await self._http().post(
                f"{self.base_url}/messages", headers=self._headers(), json=payload
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)

        data = resp.json()
        text_parts: list[str] = []
        calls: list[ToolCall] = []
        for block in data.get("content", []):
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                calls.append(ToolCall(id=block.get("id", ""), name=block.get("name", ""),
                                      arguments=block.get("input") or {}))
        u = data.get("usage") or {}
        return CompletionResult(
            text="".join(text_parts),
            tool_calls=calls,
            usage=Usage(int(u.get("input_tokens", 0)), int(u.get("output_tokens", 0))),
            finish_reason=data.get("stop_reason", ""),
            model=data.get("model", model),
            raw=data,
        )

    async def stream(self, model: str, messages: list[ChatMessage], *,
                     temperature: float = 0.7,
                     max_tokens: int = 2048) -> AsyncIterator[str]:
        import json as _json

        system, wire = self._split(messages)
        payload: dict[str, Any] = {
            "model": model, "messages": wire, "max_tokens": max_tokens,
            "temperature": temperature, "stream": True,
        }
        if system:
            payload["system"] = system
        try:
            async with self._http().stream(
                "POST", f"{self.base_url}/messages", headers=self._headers(), json=payload
            ) as resp:
                if resp.status_code >= 400:
                    await resp.aread()
                    raise ProviderError(_error_text(resp), resp.status_code)
                async for line in resp.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    try:
                        event = _json.loads(line[5:].strip())
                    except ValueError:
                        continue
                    if event.get("type") == "content_block_delta":
                        piece = (event.get("delta") or {}).get("text")
                        if piece:
                            yield piece
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc

    async def list_models(self) -> list[str]:
        try:
            resp = await self._http().get(f"{self.base_url}/models", headers=self._headers())
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)
        return sorted(it.get("id", "") for it in resp.json().get("data", []) if it.get("id"))


def _error_text(resp: httpx.Response) -> str:
    try:
        err = resp.json().get("error") or {}
        return f"{resp.status_code}: {err.get('message', resp.text[:200])}"
    except Exception:  # noqa: BLE001
        return f"{resp.status_code}: {resp.text[:200]}"
````

### `providers/gemini_provider.py`

*143 строк*

````python
"""Провайдер Google Gemini (generativeLanguage API).

Особенности, скрытые внутри класса:
* роли называются ``user``/``model``, системный промпт — ``systemInstruction``;
* ключ передаётся заголовком ``x-goog-api-key``;
* инструменты описываются как ``functionDeclarations``.
"""

from __future__ import annotations

import uuid
from typing import Any

import httpx

from providers.base import (
    ChatMessage,
    CompletionResult,
    LLMProvider,
    ProviderError,
    ToolCall,
    ToolSpec,
    Usage,
)


class GeminiProvider(LLMProvider):
    key = "gemini"

    def __init__(self, api_key: str = "", base_url: str = "",
                 timeout: float = 120.0) -> None:
        super().__init__(
            api_key, base_url or "https://generativelanguage.googleapis.com/v1beta", timeout
        )
        self._client: httpx.AsyncClient | None = None

    def _headers(self) -> dict[str, str]:
        return {"Content-Type": "application/json", "x-goog-api-key": self.api_key}

    def _http(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(timeout=self.timeout)
        return self._client

    async def aclose(self) -> None:
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    @staticmethod
    def _split(messages: list[ChatMessage]) -> tuple[str, list[dict[str, Any]]]:
        system_parts: list[str] = []
        contents: list[dict[str, Any]] = []
        for m in messages:
            if m.role == "system":
                system_parts.append(m.content)
            elif m.role == "tool":
                contents.append({
                    "role": "user",
                    "parts": [{"functionResponse": {"name": m.name or "tool",
                                                    "response": {"result": m.content}}}],
                })
            elif m.role == "assistant":
                parts: list[dict[str, Any]] = []
                if m.content:
                    parts.append({"text": m.content})
                parts += [{"functionCall": {"name": tc.name, "args": tc.arguments}}
                          for tc in m.tool_calls]
                contents.append({"role": "model", "parts": parts or [{"text": ""}]})
            else:
                contents.append({"role": "user", "parts": [{"text": m.content}]})
        return "\n\n".join(p for p in system_parts if p), contents

    async def complete(self, model: str, messages: list[ChatMessage], *,
                       temperature: float = 0.7, max_tokens: int = 2048,
                       tools: list[ToolSpec] | None = None) -> CompletionResult:
        system, contents = self._split(messages)
        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": {"temperature": temperature,
                                 "maxOutputTokens": max_tokens},
        }
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        if tools:
            payload["tools"] = [{
                "functionDeclarations": [
                    {"name": t.name, "description": t.description, "parameters": t.parameters}
                    for t in tools
                ]
            }]

        url = f"{self.base_url}/models/{model}:generateContent"
        try:
            resp = await self._http().post(url, headers=self._headers(), json=payload)
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)

        data = resp.json()
        candidate = (data.get("candidates") or [{}])[0]
        text_parts, calls = [], []
        for part in (candidate.get("content") or {}).get("parts", []):
            if "text" in part:
                text_parts.append(part["text"])
            elif "functionCall" in part:
                fc = part["functionCall"]
                calls.append(ToolCall(id=uuid.uuid4().hex[:12], name=fc.get("name", ""),
                                      arguments=fc.get("args") or {}))
        u = data.get("usageMetadata") or {}
        return CompletionResult(
            text="".join(text_parts),
            tool_calls=calls,
            usage=Usage(int(u.get("promptTokenCount", 0)),
                        int(u.get("candidatesTokenCount", 0))),
            finish_reason=candidate.get("finishReason", ""),
            model=model,
            raw=data,
        )

    async def list_models(self) -> list[str]:
        try:
            resp = await self._http().get(f"{self.base_url}/models", headers=self._headers())
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)
        names = []
        for m in resp.json().get("models", []):
            name = (m.get("name") or "").removeprefix("models/")
            if name and "generateContent" in (m.get("supportedGenerationMethods") or
                                              ["generateContent"]):
                names.append(name)
        return sorted(names)


def _error_text(resp: httpx.Response) -> str:
    try:
        err = resp.json().get("error") or {}
        return f"{resp.status_code}: {err.get('message', resp.text[:200])}"
    except Exception:  # noqa: BLE001
        return f"{resp.status_code}: {resp.text[:200]}"
````

### `providers/factory.py`

*87 строк*

````python
"""Фабрика провайдеров и расчёт стоимости вызовов.

Провайдеры почти никогда не возвращают цену — только токены. Поэтому
стоимость считается на клиенте по таблице ``pricing.json``
(USD за 1 млн токенов). Для локальных моделей стоимость равна нулю.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from providers.base import LLMProvider
from providers.presets import preset

_PRICING_FILE = Path(__file__).with_name("pricing.json")


def build_provider(provider_key: str, api_key: str = "",
                   base_url: str = "", timeout: float = 120.0) -> LLMProvider:
    """Создаёт экземпляр провайдера по ключу пресета.

    Импорт реализаций ленивый: расчёт стоимости и работа с пресетами не должны
    тянуть за собой httpx, если сетевой вызов в этом сценарии не нужен.
    """
    from providers.anthropic_provider import AnthropicProvider
    from providers.gemini_provider import GeminiProvider
    from providers.openai_compat import OpenAICompatProvider

    p = preset(provider_key)
    url = base_url or p.base_url
    if p.api_style == "anthropic":
        return AnthropicProvider(api_key, url, timeout)
    if p.api_style == "gemini":
        return GeminiProvider(api_key, url, timeout)
    extra: dict[str, str] = {}
    if provider_key == "openrouter":
        # OpenRouter просит идентифицировать приложение.
        extra = {"HTTP-Referer": "https://localhost/ai-orchestrator",
                 "X-Title": "AI Orchestrator"}
    prov = OpenAICompatProvider(api_key, url, timeout, extra_headers=extra)
    prov.key = provider_key
    return prov


@lru_cache(maxsize=1)
def _pricing() -> dict:
    try:
        return json.loads(_PRICING_FILE.read_text("utf-8"))
    except Exception:  # noqa: BLE001
        return {}


def reload_pricing() -> None:
    """Сбрасывает кэш — используется после ручного редактирования таблицы цен."""
    _pricing.cache_clear()


def model_price(provider_key: str, model: str) -> tuple[float, float]:
    """Возвращает (цена_входа, цена_выхода) в USD за 1 млн токенов.

    Поиск идёт от точного совпадения к префиксному: ``gpt-4o-2024-11-20``
    подхватит цену ``gpt-4o``.
    """
    data = _pricing()
    if preset(provider_key).local:
        return (0.0, 0.0)
    table: dict = data.get(provider_key, {})
    if model in table:
        row = table[model]
        return float(row[0]), float(row[1])
    best: tuple[str, list] | None = None
    for name, row in table.items():
        if model.startswith(name) and (best is None or len(name) > len(best[0])):
            best = (name, row)
    if best:
        return float(best[1][0]), float(best[1][1])
    default = data.get("_default", [0.0, 0.0])
    return float(default[0]), float(default[1])


def estimate_cost(provider_key: str, model: str,
                  tokens_in: int, tokens_out: int) -> float:
    """Приблизительная стоимость вызова в USD."""
    p_in, p_out = model_price(provider_key, model)
    return (tokens_in * p_in + tokens_out * p_out) / 1_000_000.0
````

### `providers/pricing.json`

*47 строк*

````json
{
  "_comment": "USD за 1 000 000 токенов: [вход, выход]. Цены ориентировочные, обновляйте вручную по прайс-листам провайдеров. Ключ ищется по точному совпадению, затем по самому длинному префиксу.",
  "_default": [0.0, 0.0],

  "openai": {
    "gpt-4o": [2.50, 10.00],
    "gpt-4o-mini": [0.15, 0.60],
    "gpt-4.1": [2.00, 8.00],
    "gpt-4.1-mini": [0.40, 1.60],
    "gpt-4.1-nano": [0.10, 0.40],
    "o3": [2.00, 8.00],
    "o4-mini": [1.10, 4.40]
  },

  "anthropic": {
    "claude-opus-4": [15.00, 75.00],
    "claude-sonnet-4": [3.00, 15.00],
    "claude-3-7-sonnet": [3.00, 15.00],
    "claude-3-5-sonnet": [3.00, 15.00],
    "claude-3-5-haiku": [0.80, 4.00],
    "claude-3-haiku": [0.25, 1.25]
  },

  "gemini": {
    "gemini-2.5-pro": [1.25, 10.00],
    "gemini-2.5-flash": [0.30, 2.50],
    "gemini-2.5-flash-lite": [0.10, 0.40],
    "gemini-2.0-flash": [0.10, 0.40]
  },

  "groq": {
    "llama-3.3-70b-versatile": [0.59, 0.79],
    "llama-3.1-8b-instant": [0.05, 0.08],
    "qwen/qwen3-32b": [0.29, 0.59],
    "deepseek-r1-distill-llama-70b": [0.75, 0.99]
  },

  "openrouter": {
    "deepseek/deepseek-chat": [0.27, 1.10],
    "qwen/qwen-2.5-72b-instruct": [0.12, 0.39],
    "meta-llama/llama-3.3-70b-instruct": [0.12, 0.30]
  },

  "huggingface": {},
  "ollama": {},
  "custom": {}
}
````


## Инструменты агентов

### `core/tools/base.py`

*143 строк*

````python
"""Базовая инфраструктура инструментов агентов (tool-calling).

Модель прав простая и явная: у каждого запуска агента есть ``ToolContext``
с корнем рабочего каталога и списком дополнительно разрешённых путей.
Инструмент обязан валидировать любой путь через ``ToolContext.resolve``,
иначе обращение за пределы песочницы просто не состоится.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from providers.base import ToolSpec


class ToolError(RuntimeError):
    """Ошибка инструмента, которую не стыдно показать модели дословно."""


@dataclass
class ToolContext:
    """Границы, в которых агенту позволено действовать."""

    workspace_dir: Path
    agent_id: int | None = None
    subtask_id: int | None = None
    #: дополнительные каталоги, явно разрешённые пользователем в настройках
    extra_allowed_paths: list[Path] = field(default_factory=list)
    #: параметры песочницы
    sandbox_backend: str = "auto"
    sandbox_timeout_sec: int = 30
    sandbox_memory_mb: int = 512
    allow_network_in_sandbox: bool = False
    #: настройки веб-поиска
    search_backend: str = "duckduckgo"
    search_api_key: str = ""
    fetch_pages: bool = True

    def roots(self) -> list[Path]:
        return [self.workspace_dir.resolve(), *[p.resolve() for p in self.extra_allowed_paths]]

    def resolve(self, raw_path: str, must_exist: bool = False) -> Path:
        """Приводит путь к абсолютному и проверяет, что он внутри разрешённых корней.

        Защищает от ``../``, абсолютных путей и симлинков наружу.
        """
        candidate = Path(raw_path)
        if not candidate.is_absolute():
            candidate = self.workspace_dir / candidate
        try:
            resolved = candidate.resolve()
        except OSError as exc:
            raise ToolError(f"Некорректный путь: {raw_path} ({exc})") from exc

        for root in self.roots():
            if resolved == root or root in resolved.parents:
                if must_exist and not resolved.exists():
                    raise ToolError(f"Файл не найден: {raw_path}")
                return resolved
        raise ToolError(
            f"Доступ запрещён: путь «{raw_path}» вне разрешённых каталогов. "
            "Разрешены только рабочий каталог воркспейса и каталоги, "
            "добавленные пользователем в настройках."
        )


class Tool(ABC):
    """Инструмент, доступный агенту через tool-calling."""

    name: str = ""
    description: str = ""
    parameters: dict[str, Any] = {}

    def spec(self) -> ToolSpec:
        return ToolSpec(self.name, self.description, self.parameters)

    @abstractmethod
    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        """Выполняет инструмент и возвращает текстовый результат для модели."""


class ToolRegistry:
    """Реестр инструментов; агент получает только разрешённое ему подмножество."""

    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def specs(self, allowed: list[str]) -> list[ToolSpec]:
        return [t.spec() for n, t in self._tools.items() if n in allowed]

    def names(self) -> list[str]:
        return list(self._tools)

    async def invoke(self, name: str, ctx: ToolContext, **kwargs: Any) -> str:
        """Вызывает инструмент, превращая любые ошибки в текст для модели."""
        tool = self.get(name)
        if tool is None:
            return f"ОШИБКА: инструмент «{name}» недоступен."
        try:
            return await tool.run(ctx, **kwargs)
        except ToolError as exc:
            return f"ОШИБКА ИНСТРУМЕНТА: {exc}"
        except Exception as exc:  # noqa: BLE001 — модель должна узнать о сбое
            return f"ОШИБКА ИНСТРУМЕНТА ({type(exc).__name__}): {exc}"


#: групповые имена из шаблонов ролей и настроек воркспейса → реальные инструменты
TOOL_GROUPS: dict[str, list[str]] = {
    "files": ["read_file", "write_file", "list_dir"],
    "web_search": ["web_search", "fetch_url"],
}


def expand_tool_names(names) -> list[str]:
    """Разворачивает групповые имена, сохраняя порядок и убирая повторы."""
    out: list[str] = []
    for name in names or []:
        for real in TOOL_GROUPS.get(name, [name]):
            if real not in out:
                out.append(real)
    return out


def default_registry() -> ToolRegistry:
    """Собирает стандартный набор инструментов."""
    from core.tools.code_exec import CodeExecTool
    from core.tools.files import FileReadTool, FileWriteTool, ListDirTool
    from core.tools.web_search import WebFetchTool, WebSearchTool

    reg = ToolRegistry()
    for tool in (WebSearchTool(), WebFetchTool(), FileReadTool(),
                 FileWriteTool(), ListDirTool(), CodeExecTool()):
        reg.register(tool)
    return reg
````

### `core/tools/sandbox.py`

*258 строк*

````python
"""Песочница для исполнения кода агентами.

Ответ на вопрос 3: интерфейс ``Sandbox`` с двумя реализациями.

``SubprocessSandbox`` (по умолчанию, работает везде)
    * отдельный процесс в одноразовом временном каталоге;
    * ``setsid`` + убийство всей группы процессов по таймауту;
    * POSIX: ``RLIMIT_CPU``, ``RLIMIT_AS``, ``RLIMIT_FSIZE``, ``RLIMIT_NPROC``;
    * вычищенное окружение (нет API-ключей и прочих переменных хоста);
    * сеть по умолчанию отключается подстановкой недоступного прокси —
      это не жёсткая изоляция, а барьер «по умолчанию».

``DockerSandbox`` (если найден работающий Docker)
    * ``--network none``, ``--read-only``, ``--pids-limit``, ``--memory``,
      ``--cpus``, непривилегированный пользователь, ``--rm``;
    * настоящая изоляция ФС и сети.

Выбор ``auto`` берёт Docker, когда он доступен, иначе subprocess.
Абсолютной защиты subprocess-режим не даёт, и в UI об этом сказано прямо.
"""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import sys
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

# Языки, которые разрешено исполнять. Shell намеренно не включён в Docker-режиме
# по умолчанию — он нужен реже, а рисков даёт больше.
LANG_COMMANDS: dict[str, list[str]] = {
    "python": [sys.executable or "python3", "-I", "{file}"],
    "bash": ["bash", "{file}"],
    "node": ["node", "{file}"],
}
LANG_EXT = {"python": ".py", "bash": ".sh", "node": ".js"}


@dataclass
class SandboxResult:
    exit_code: int
    stdout: str
    stderr: str
    timed_out: bool = False
    backend: str = ""

    def as_text(self, limit: int = 8000) -> str:
        """Компактное представление для отправки модели."""
        parts = [f"[{self.backend}] exit_code={self.exit_code}"]
        if self.timed_out:
            parts.append("ПРЕВЫШЕН ТАЙМАУТ ВЫПОЛНЕНИЯ")
        if self.stdout.strip():
            parts.append("STDOUT:\n" + self.stdout[:limit])
        if self.stderr.strip():
            parts.append("STDERR:\n" + self.stderr[:limit])
        if len(self.stdout) > limit or len(self.stderr) > limit:
            parts.append("(вывод обрезан)")
        return "\n\n".join(parts)


class Sandbox(ABC):
    """Интерфейс песочницы."""

    name = "sandbox"

    @abstractmethod
    async def run(self, code: str, language: str, workdir: Path,
                  timeout: int, memory_mb: int, network: bool) -> SandboxResult:
        ...


# ---------------------------------------------------------------------------


def _preexec(memory_mb: int, cpu_seconds: int):  # pragma: no cover — POSIX-only
    """Ограничения ресурсов для дочернего процесса (POSIX)."""
    import resource

    def apply() -> None:
        os.setsid()  # своя группа процессов: убьём её целиком по таймауту
        mem = memory_mb * 1024 * 1024
        resource.setrlimit(resource.RLIMIT_AS, (mem, mem))
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_seconds, cpu_seconds + 1))
        resource.setrlimit(resource.RLIMIT_FSIZE, (64 * 1024 * 1024, 64 * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        try:
            resource.setrlimit(resource.RLIMIT_NPROC, (64, 64))
        except (ValueError, OSError):
            pass

    return apply


class SubprocessSandbox(Sandbox):
    """Исполнение в отдельном процессе с ограничением ресурсов."""

    name = "subprocess"

    async def run(self, code: str, language: str, workdir: Path,
                  timeout: int, memory_mb: int, network: bool) -> SandboxResult:
        if language not in LANG_COMMANDS:
            return SandboxResult(1, "", f"Язык «{language}» не поддерживается",
                                 backend=self.name)

        workdir.mkdir(parents=True, exist_ok=True)
        tmpdir = Path(tempfile.mkdtemp(prefix="aiorc_run_", dir=str(workdir)))
        script = tmpdir / f"script{LANG_EXT[language]}"
        script.write_text(code, "utf-8")

        cmd = [part.format(file=str(script)) for part in LANG_COMMANDS[language]]
        if shutil.which(cmd[0]) is None and not Path(cmd[0]).exists():
            shutil.rmtree(tmpdir, ignore_errors=True)
            return SandboxResult(127, "", f"Интерпретатор «{cmd[0]}» не найден в системе",
                                 backend=self.name)

        # Чистое окружение: никаких ключей и токенов хоста.
        env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": str(tmpdir),
            "TMPDIR": str(tmpdir),
            "LANG": "C.UTF-8",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONDONTWRITEBYTECODE": "1",
        }
        if not network:
            # Грубый, но действенный барьер для большинства http-библиотек.
            env.update({"http_proxy": "http://127.0.0.1:9", "https_proxy": "http://127.0.0.1:9",
                        "HTTP_PROXY": "http://127.0.0.1:9", "HTTPS_PROXY": "http://127.0.0.1:9",
                        "no_proxy": ""})

        kwargs: dict = {}
        if os.name == "posix":
            kwargs["preexec_fn"] = _preexec(memory_mb, timeout)
        else:  # Windows: своя группа процессов, чтобы корректно убивать дерево
            kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd, cwd=str(tmpdir), env=env,
                stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.DEVNULL, **kwargs,
            )
        except OSError as exc:
            shutil.rmtree(tmpdir, ignore_errors=True)
            return SandboxResult(126, "", f"Не удалось запустить процесс: {exc}",
                                 backend=self.name)

        timed_out = False
        try:
            out, err = await asyncio.wait_for(proc.communicate(), timeout=timeout)
        except asyncio.TimeoutError:
            timed_out = True
            _kill_tree(proc)
            out, err = b"", "Процесс остановлен по таймауту".encode("utf-8")
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)

        return SandboxResult(
            exit_code=proc.returncode if proc.returncode is not None else -1,
            stdout=out.decode("utf-8", "replace"),
            stderr=err.decode("utf-8", "replace"),
            timed_out=timed_out,
            backend=self.name,
        )


def _kill_tree(proc) -> None:
    """Убивает процесс вместе с его группой."""
    try:
        if os.name == "posix":
            os.killpg(os.getpgid(proc.pid), 9)
        else:
            proc.kill()
    except Exception:  # noqa: BLE001
        try:
            proc.kill()
        except Exception:  # noqa: BLE001
            pass


class DockerSandbox(Sandbox):
    """Исполнение в одноразовом контейнере с отключённой сетью."""

    name = "docker"
    IMAGES = {"python": "python:3.12-slim", "bash": "debian:stable-slim",
              "node": "node:22-slim"}

    async def run(self, code: str, language: str, workdir: Path,
                  timeout: int, memory_mb: int, network: bool) -> SandboxResult:
        if language not in self.IMAGES:
            return SandboxResult(1, "", f"Язык «{language}» не поддерживается",
                                 backend=self.name)
        workdir.mkdir(parents=True, exist_ok=True)
        tmpdir = Path(tempfile.mkdtemp(prefix="aiorc_dock_", dir=str(workdir)))
        script = tmpdir / f"script{LANG_EXT[language]}"
        script.write_text(code, "utf-8")

        inner = {"python": ["python", "/work/" + script.name],
                 "bash": ["bash", "/work/" + script.name],
                 "node": ["node", "/work/" + script.name]}[language]

        cmd = [
            "docker", "run", "--rm",
            "--network", "bridge" if network else "none",
            "--memory", f"{memory_mb}m", "--memory-swap", f"{memory_mb}m",
            "--cpus", "1", "--pids-limit", "128",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", "1000:1000",
            "-v", f"{tmpdir}:/work",
            "-w", "/work",
            self.IMAGES[language], *inner,
        ]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.DEVNULL,
            )
            timed_out = False
            try:
                out, err = await asyncio.wait_for(proc.communicate(), timeout=timeout + 15)
            except asyncio.TimeoutError:
                timed_out = True
                proc.kill()
                out, err = b"", "Контейнер остановлен по таймауту".encode("utf-8")
            return SandboxResult(
                proc.returncode if proc.returncode is not None else -1,
                out.decode("utf-8", "replace"), err.decode("utf-8", "replace"),
                timed_out, self.name,
            )
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


def docker_available() -> bool:
    """Проверяет, что Docker установлен и демон отвечает."""
    if shutil.which("docker") is None:
        return False
    try:
        res = subprocess.run(["docker", "info", "--format", "{{json .ServerVersion}}"],
                             capture_output=True, timeout=5)
        return res.returncode == 0 and bool(json.loads(res.stdout or b'""'))
    except Exception:  # noqa: BLE001
        return False


def get_sandbox(backend: str = "auto") -> Sandbox:
    """Фабрика песочницы по настройке воркспейса."""
    if backend == "docker":
        return DockerSandbox()
    if backend == "subprocess":
        return SubprocessSandbox()
    return DockerSandbox() if docker_available() else SubprocessSandbox()
````

### `core/tools/code_exec.py`

*49 строк*

````python
"""Инструмент исполнения кода в песочнице."""

from __future__ import annotations

from typing import Any

from core.tools.base import Tool, ToolContext, ToolError
from core.tools.sandbox import LANG_COMMANDS, get_sandbox


class CodeExecTool(Tool):
    name = "code_exec"
    description = (
        "Выполнить фрагмент кода в изолированной песочнице и получить stdout/stderr. "
        "Сеть внутри песочницы отключена, файловая система одноразовая. "
        "Используй для проверки гипотез, расчётов и прогона тестов."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "code": {"type": "string", "description": "Исходный код целиком"},
            "language": {
                "type": "string",
                "enum": list(LANG_COMMANDS),
                "description": "Язык исполнения",
                "default": "python",
            },
        },
        "required": ["code"],
    }

    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        code = (kwargs.get("code") or "").strip()
        language = (kwargs.get("language") or "python").lower()
        if not code:
            raise ToolError("Пустой код — нечего исполнять")
        if language not in LANG_COMMANDS:
            raise ToolError(f"Язык «{language}» не поддерживается")

        sandbox = get_sandbox(ctx.sandbox_backend)
        result = await sandbox.run(
            code=code,
            language=language,
            workdir=ctx.workspace_dir / ".sandbox",
            timeout=ctx.sandbox_timeout_sec,
            memory_mb=ctx.sandbox_memory_mb,
            network=ctx.allow_network_in_sandbox,
        )
        return result.as_text()
````

### `core/tools/files.py`

*109 строк*

````python
"""Файловые инструменты агента.

Права ограничены каталогом воркспейса плюс каталогами, которые пользователь
явно добавил в настройках (ответ на вопрос 10). Проверка пути централизована
в ``ToolContext.resolve``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from core.tools.base import Tool, ToolContext, ToolError

MAX_READ_BYTES = 200_000
MAX_WRITE_BYTES = 2_000_000


class FileReadTool(Tool):
    name = "read_file"
    description = (
        "Прочитать текстовый файл из рабочего каталога проекта "
        "или из каталога, разрешённого пользователем."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Путь относительно рабочего каталога"},
            "max_bytes": {"type": "integer",
                          "description": f"Сколько байт прочитать (по умолчанию {MAX_READ_BYTES})"},
        },
        "required": ["path"],
    }

    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        path = ctx.resolve(str(kwargs.get("path", "")), must_exist=True)
        if path.is_dir():
            raise ToolError(f"«{path.name}» — каталог, используй list_dir")
        limit = min(int(kwargs.get("max_bytes") or MAX_READ_BYTES), MAX_READ_BYTES)
        data = path.read_bytes()[:limit]
        text = data.decode("utf-8", "replace")
        suffix = "\n\n(файл обрезан)" if path.stat().st_size > limit else ""
        return f"Файл: {path}\n\n{text}{suffix}"


class FileWriteTool(Tool):
    name = "write_file"
    description = (
        "Создать или перезаписать текстовый файл в рабочем каталоге проекта. "
        "Промежуточные каталоги создаются автоматически."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Путь относительно рабочего каталога"},
            "content": {"type": "string", "description": "Содержимое файла"},
            "append": {"type": "boolean", "description": "Дописать в конец вместо перезаписи",
                       "default": False},
        },
        "required": ["path", "content"],
    }

    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        content = str(kwargs.get("content", ""))
        if len(content.encode("utf-8")) > MAX_WRITE_BYTES:
            raise ToolError("Слишком большой файл (лимит 2 МБ)")
        path = ctx.resolve(str(kwargs.get("path", "")))
        path.parent.mkdir(parents=True, exist_ok=True)
        if kwargs.get("append"):
            with path.open("a", encoding="utf-8") as fh:
                fh.write(content)
            action = "дописан"
        else:
            path.write_text(content, "utf-8")
            action = "записан"
        return f"Файл {action}: {path} ({len(content)} символов)"


class ListDirTool(Tool):
    name = "list_dir"
    description = "Показать содержимое каталога внутри разрешённой зоны."
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "Каталог (по умолчанию корень проекта)",
                     "default": "."},
        },
    }

    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        path = ctx.resolve(str(kwargs.get("path") or "."), must_exist=True)
        if not path.is_dir():
            raise ToolError(f"«{path.name}» — не каталог")
        lines: list[str] = []
        for item in sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
            if item.name.startswith("."):
                continue
            lines.append(f"{'DIR ' if item.is_dir() else 'FILE'}  {item.name}"
                         + ("" if item.is_dir() else f"  ({_human(item)})"))
        return f"Каталог: {path}\n" + ("\n".join(lines) if lines else "(пусто)")


def _human(path: Path) -> str:
    size = path.stat().st_size
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024
    return f"{size:.1f} ТБ"
````

### `core/tools/web_search.py`

*175 строк*

````python
"""Веб-поиск и чтение страниц.

Ответ на вопрос 9: по умолчанию используется DuckDuckGo (библиотека ``ddgs``) —
она не требует ключа, поэтому поиск работает «из коробки». Если пользователь
добавит ключ Tavily или Brave, можно переключить бэкенд в настройках воркспейса.

Сетевые вызовы вынесены в поток (``asyncio.to_thread``), потому что ``ddgs``
синхронная, и блокировать общий asyncio-луп нельзя.
"""

from __future__ import annotations

import asyncio
from typing import Any

from core.tools.base import Tool, ToolContext, ToolError

MAX_RESULTS = 8
MAX_PAGE_CHARS = 20_000


class WebSearchTool(Tool):
    name = "web_search"
    description = (
        "Найти информацию в интернете. Возвращает список результатов: "
        "заголовок, ссылка, краткое описание. Для подробностей открой ссылку "
        "инструментом fetch_url."
    )
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "Поисковый запрос"},
            "max_results": {"type": "integer", "description": "Сколько результатов вернуть",
                            "default": 5},
        },
        "required": ["query"],
    }

    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        query = (kwargs.get("query") or "").strip()
        if not query:
            raise ToolError("Пустой поисковый запрос")
        n = max(1, min(int(kwargs.get("max_results") or 5), MAX_RESULTS))

        backend = ctx.search_backend
        if backend == "tavily" and ctx.search_api_key:
            items = await _tavily(query, n, ctx.search_api_key)
        elif backend == "brave" and ctx.search_api_key:
            items = await _brave(query, n, ctx.search_api_key)
        else:
            items = await asyncio.to_thread(_duckduckgo, query, n)

        if not items:
            return f"По запросу «{query}» ничего не найдено."
        lines = [f"Результаты поиска: {query}", ""]
        for i, it in enumerate(items, 1):
            lines.append(f"{i}. {it['title']}\n   {it['url']}\n   {it['snippet']}")
        return "\n".join(lines)


class WebFetchTool(Tool):
    name = "fetch_url"
    description = "Открыть веб-страницу и вернуть её основной текст без разметки."
    parameters: dict[str, Any] = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "description": "Полный URL, включая https://"},
        },
        "required": ["url"],
    }

    async def run(self, ctx: ToolContext, **kwargs: Any) -> str:
        url = (kwargs.get("url") or "").strip()
        if not url.startswith(("http://", "https://")):
            raise ToolError("URL должен начинаться с http:// или https://")
        if not ctx.fetch_pages:
            raise ToolError("Загрузка страниц отключена в настройках воркспейса")

        import httpx

        try:
            async with httpx.AsyncClient(
                timeout=30, follow_redirects=True,
                headers={"User-Agent": "Mozilla/5.0 (compatible; AI-Orchestrator/1.0)"},
            ) as client:
                resp = await client.get(url)
        except Exception as exc:  # noqa: BLE001
            raise ToolError(f"Не удалось загрузить страницу: {exc}") from exc
        if resp.status_code >= 400:
            raise ToolError(f"HTTP {resp.status_code} при загрузке {url}")

        text = await asyncio.to_thread(_extract_text, resp.text)
        clipped = text[:MAX_PAGE_CHARS]
        tail = "\n\n(текст обрезан)" if len(text) > MAX_PAGE_CHARS else ""
        return f"Источник: {url}\n\n{clipped}{tail}"


# ---------------------------------------------------------------------------
# Бэкенды поиска
# ---------------------------------------------------------------------------


def _duckduckgo(query: str, n: int) -> list[dict]:
    """Поиск без ключа. Библиотека называется ``ddgs`` (ранее duckduckgo-search)."""
    try:
        from ddgs import DDGS
    except ImportError:
        try:
            from duckduckgo_search import DDGS  # type: ignore[no-redef]
        except ImportError as exc:
            raise ToolError(
                "Веб-поиск недоступен: установите пакет «ddgs» "
                "(pip install ddgs) или переключите бэкенд в настройках."
            ) from exc
    with DDGS() as ddgs:
        rows = list(ddgs.text(query, max_results=n))
    return [{"title": r.get("title", ""), "url": r.get("href") or r.get("link", ""),
             "snippet": (r.get("body") or "")[:400]} for r in rows]


async def _tavily(query: str, n: int, api_key: str) -> list[dict]:
    import httpx

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.tavily.com/search",
            json={"api_key": api_key, "query": query, "max_results": n},
        )
    if resp.status_code >= 400:
        raise ToolError(f"Tavily: HTTP {resp.status_code}")
    return [{"title": r.get("title", ""), "url": r.get("url", ""),
             "snippet": (r.get("content") or "")[:400]}
            for r in resp.json().get("results", [])]


async def _brave(query: str, n: int, api_key: str) -> list[dict]:
    import httpx

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            "https://api.search.brave.com/res/v1/web/search",
            params={"q": query, "count": n},
            headers={"X-Subscription-Token": api_key, "Accept": "application/json"},
        )
    if resp.status_code >= 400:
        raise ToolError(f"Brave: HTTP {resp.status_code}")
    web = resp.json().get("web", {})
    return [{"title": r.get("title", ""), "url": r.get("url", ""),
             "snippet": (r.get("description") or "")[:400]}
            for r in web.get("results", [])]


def _extract_text(html: str) -> str:
    """Извлекает основной текст: trafilatura → bs4 → грубый фолбэк."""
    try:
        import trafilatura

        extracted = trafilatura.extract(html, include_comments=False, include_tables=True)
        if extracted:
            return extracted
    except ImportError:
        pass
    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            tag.decompose()
        return "\n".join(line.strip() for line in soup.get_text("\n").splitlines()
                         if line.strip())
    except ImportError:
        pass
    import re

    return re.sub(r"<[^>]+>", " ", html)
````


## Ядро: агенты, оркестратор, супервайзер

### `core/events.py`

*103 строк*

````python
"""Шина событий между ядром и интерфейсом.

Ядро не знает о Qt: оно публикует события, а UI на них подписывается.
Всё происходит в одном asyncio-лупе (он же луп Qt), поэтому обработчики
могут напрямую трогать виджеты — отдельная синхронизация не нужна.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable

from storage.db import local_time

log = logging.getLogger("aiorc.events")


class EventType(str, Enum):
    """Типы событий выполнения."""

    RUN_STARTED = "run_started"
    RUN_FINISHED = "run_finished"
    RUN_PAUSED = "run_paused"
    RUN_RESUMED = "run_resumed"
    RUN_STOPPED = "run_stopped"

    AGENT_STATUS = "agent_status"        # агент сменил статус
    AGENT_THINKING = "agent_thinking"    # шаг рассуждения
    AGENT_TOOL_CALL = "agent_tool_call"  # агент вызвал инструмент
    AGENT_TOOL_RESULT = "agent_tool_result"

    SUBTASK_STARTED = "subtask_started"
    SUBTASK_PROGRESS = "subtask_progress"
    SUBTASK_FINISHED = "subtask_finished"
    SUBTASK_FAILED = "subtask_failed"

    REPORT_CREATED = "report_created"
    REPORT_REVIEWED = "report_reviewed"  # супервайзер вынес вердикт
    SUMMARY_CREATED = "summary_created"
    INCIDENT_CREATED = "incident_created"
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_RESOLVED = "approval_resolved"  # пользователь принял решение

    BUDGET_ALERT = "budget_alert"          # расход подошёл к порогу
    BUDGET_EXCEEDED = "budget_exceeded"    # лимит исчерпан, вызовы заблокированы
    USAGE = "usage"                      # расход токенов/денег
    LOG = "log"                          # произвольное сообщение в ленту
    ERROR = "error"


@dataclass
class Event:
    """Одно событие в ленте выполнения."""

    type: EventType
    workspace_id: int | None = None
    task_id: int | None = None
    subtask_id: int | None = None
    agent_id: int | None = None
    agent_name: str = ""
    message: str = ""
    payload: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat(timespec="seconds")
    )

    @property
    def time_short(self) -> str:
        return local_time(self.created_at, "%H:%M:%S")


Handler = Callable[[Event], None]


class EventBus:
    """Публикация событий подписчикам. Сбой обработчика не ломает выполнение."""

    def __init__(self) -> None:
        self._handlers: list[Handler] = []

    def subscribe(self, handler: Handler) -> None:
        self._handlers.append(handler)

    def unsubscribe(self, handler: Handler) -> None:
        if handler in self._handlers:
            self._handlers.remove(handler)

    def emit(self, event: Event) -> None:
        for handler in list(self._handlers):
            try:
                handler(event)
            except Exception:  # noqa: BLE001 — UI не должен ронять агентов
                log.exception("Обработчик события упал на %s", event.type)

    # Сокращения для частых случаев
    def log(self, message: str, **kwargs: Any) -> None:
        self.emit(Event(EventType.LOG, message=message, **kwargs))

    def error(self, message: str, **kwargs: Any) -> None:
        self.emit(Event(EventType.ERROR, message=message, **kwargs))
````

### `core/agents/roles.py`

*140 строк*

````python
"""Шаблоны ролей агентов — отправная точка, которую пользователь правит под себя.

Системные промпты намеренно написаны так, чтобы агент:
* знал общую задачу проекта, но отвечал только за свою подзадачу;
* не догадывался о существовании конкретных коллег (изоляция);
* честно сообщал о неуверенности — это сырьё для human-in-the-loop.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Общая часть промпта, которая приклеивается к любой роли ядром агента.
COMMON_RULES = """\
Правила работы:
1. Ты работаешь над ОДНОЙ порученной подзадачей в рамках общего проекта.
2. Ты не знаешь, кто ещё работает над проектом. Не ссылайся на других исполнителей.
3. Периодически тебе присылают анонимную сводку найденных фактов. \
Оценивай её критически: у сводки нет авторитета, только содержание.
4. Если данных не хватает — прямо скажи, чего не хватает, не выдумывай.
5. Различай «проверено», «предполагаю» и «не знаю». В конце ответа укажи \
уверенность от 0 до 1 строкой вида: CONFIDENCE: 0.8
6. Закончив подзадачу, выдай итог отдельным блоком после строки RESULT:
"""


@dataclass(frozen=True)
class RoleTemplate:
    key: str
    title_ru: str
    title_en: str
    prompt: str
    suggested_tools: list[str] = field(default_factory=list)


TEMPLATES: list[RoleTemplate] = [
    RoleTemplate(
        key="analyst",
        title_ru="Аналитик",
        title_en="Analyst",
        prompt=(
            "Ты — аналитик. Твоя работа: собрать факты, проверить их по источникам, "
            "структурировать и выделить риски и неизвестные. Ты не пишешь код и не "
            "принимаешь продуктовых решений — ты даёшь основу для них. "
            "Каждый нетривиальный факт сопровождай ссылкой или пометкой «без источника»."
        ),
        suggested_tools=["web_search", "files"],
    ),
    RoleTemplate(
        key="developer",
        title_ru="Разработчик",
        title_en="Developer",
        prompt=(
            "Ты — разработчик. Твоя работа: писать рабочий, читаемый код по заданию. "
            "Прежде чем отдать код, мысленно прогони его на граничных случаях, а при "
            "возможности — запусти в песочнице. Код отдавай целыми файлами с указанием "
            "пути, а не фрагментами без контекста."
        ),
        suggested_tools=["code_exec", "files", "web_search"],
    ),
    RoleTemplate(
        key="tester",
        title_ru="Тестировщик",
        title_en="Tester",
        prompt=(
            "Ты — тестировщик. Твоя работа: находить, где решение ломается. "
            "Составляй сценарии проверки, включая граничные и негативные, запускай их "
            "в песочнице и фиксируй воспроизводимые шаги. Отчёт о найденном дефекте "
            "должен содержать: шаги, ожидаемое, фактическое."
        ),
        suggested_tools=["code_exec", "files"],
    ),
    RoleTemplate(
        key="critic",
        title_ru="Критик",
        title_en="Critic",
        prompt=(
            "Ты — критик. Твоя работа: искать слабые места в предложенном решении: "
            "логические дыры, непроверенные допущения, преувеличения, пропущенные "
            "альтернативы. Критикуй содержание, а не исполнителя. На каждое замечание "
            "предлагай конкретное улучшение, иначе замечание бесполезно."
        ),
        suggested_tools=["web_search"],
    ),
    RoleTemplate(
        key="documenter",
        title_ru="Документатор",
        title_en="Documenter",
        prompt=(
            "Ты — технический писатель. Твоя работа: превращать сырые материалы в "
            "понятный документ: структура, однозначные формулировки, примеры. "
            "Не добавляй фактов, которых нет в исходных материалах; если чего-то "
            "не хватает — оставь пометку TODO с точным вопросом."
        ),
        suggested_tools=["files"],
    ),
    RoleTemplate(
        key="researcher",
        title_ru="Исследователь",
        title_en="Researcher",
        prompt=(
            "Ты — исследователь. Твоя работа: находить первоисточники, сравнивать "
            "противоречащие данные и явно помечать расхождения. Предпочитай "
            "официальную документацию и первичные публикации пересказам."
        ),
        suggested_tools=["web_search", "files"],
    ),
    RoleTemplate(
        key="supervisor",
        title_ru="Супервайзер",
        title_en="Supervisor",
        prompt=(
            "Ты — супервайзер команды исполнителей. Ты проверяешь их отчёты по чек-листу: "
            "(1) соответствие исходному заданию; (2) внутренняя логическая "
            "непротиворечивость; (3) фактические ошибки и выдумки; (4) противоречия "
            "между отчётами разных исполнителей. Ты не переписываешь работу за них — "
            "ты выносишь вердикт и формулируешь, что именно нужно исправить. "
            "Сводку для команды пиши своими словами, без указания авторов."
        ),
        suggested_tools=[],
    ),
    RoleTemplate(
        key="custom",
        title_ru="Произвольная роль",
        title_en="Custom role",
        prompt="",
        suggested_tools=[],
    ),
]


def by_key(key: str) -> RoleTemplate:
    for t in TEMPLATES:
        if t.key == key:
            return t
    return TEMPLATES[-1]


def title(template: RoleTemplate, lang: str) -> str:
    return template.title_en if lang == "en" else template.title_ru
````

### `core/agents/runner.py`

*392 строк*

````python
"""Этап 4 — исполнитель одного агента над одной подзадачей.

Цикл ReAct: модель думает → при необходимости вызывает инструменты →
получает их результат → продолжает. Останов по одному из условий:
собственный сигнал завершения, исчерпание шагов, лимит токенов, отмена.

Контекст агента строится заново для каждой подзадачи, но его личная
история (таблица ``messages``) сохраняется и подмешивается при доработке.
Чужие истории недоступны: выборка всегда идёт по ``agent_id``.
"""

from __future__ import annotations

import asyncio
import logging
import re
from dataclasses import dataclass, field

from app.config import PATHS
from core.events import Event, EventBus, EventType
from core.tools.base import ToolContext, ToolRegistry, expand_tool_names
from providers.base import ChatMessage, CompletionResult, LLMProvider, ProviderError, ToolCall
from providers.factory import estimate_cost
from storage.models import Agent, Subtask, Task
from storage.repositories import Repos

log = logging.getLogger("aiorc.runner")

#: сколько последних сообщений истории подмешивать без сжатия
HISTORY_WINDOW = 24
#: после какого количества символов истории включается сжатие
HISTORY_COMPACT_CHARS = 24_000


class RunCancelled(Exception):
    """Выполнение остановлено пользователем."""


class BudgetExceeded(Exception):
    """Достигнут лимит токенов задачи."""


@dataclass
class RunResult:
    """Итог работы агента над подзадачей."""

    ok: bool
    result_text: str = ""
    confidence: float | None = None
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0
    steps: int = 0
    error: str = ""
    tool_calls: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Разбор ответа агента
# ---------------------------------------------------------------------------

_CONFIDENCE_RE = re.compile(r"CONFIDENCE\s*[:=]\s*([01](?:[.,]\d+)?)", re.IGNORECASE)
_RESULT_RE = re.compile(r"RESULT\s*:\s*\n?(.+)\Z", re.IGNORECASE | re.DOTALL)
_DONE_RE = re.compile(r"\b(TASK_COMPLETE|ЗАДАЧА_ВЫПОЛНЕНА)\b", re.IGNORECASE)


def parse_confidence(text: str) -> float | None:
    """Достаёт самооценку уверенности из ответа (строка ``CONFIDENCE: 0.8``)."""
    match = _CONFIDENCE_RE.search(text or "")
    if not match:
        return None
    try:
        value = float(match.group(1).replace(",", "."))
        return min(max(value, 0.0), 1.0)
    except ValueError:
        return None


def parse_result(text: str) -> str:
    """Возвращает содержимое блока ``RESULT:`` либо весь текст."""
    match = _RESULT_RE.search(text or "")
    body = match.group(1) if match else (text or "")
    return _CONFIDENCE_RE.sub("", body).strip()


def looks_done(text: str) -> bool:
    """Агент явно обозначил завершение подзадачи."""
    return bool(_DONE_RE.search(text or "") or _RESULT_RE.search(text or ""))


# ---------------------------------------------------------------------------


class AgentRunner:
    """Выполняет одну подзадачу силами одного агента."""

    def __init__(self, repos: Repos, bus: EventBus, registry: ToolRegistry,
                 workspace_id: int, workspace_settings: dict,
                 task: Task, subtask: Subtask, agent: Agent,
                 provider: LLMProvider,
                 budget_guard: "BudgetGuard | None" = None,
                 rework_notes: str = "") -> None:
        self.repos = repos
        self.bus = bus
        self.registry = registry
        self.workspace_id = workspace_id
        self.settings = workspace_settings
        self.task = task
        self.subtask = subtask
        self.agent = agent
        self.provider = provider
        self.budget = budget_guard
        self.rework_notes = rework_notes

        self.max_steps = int(workspace_settings.get("agent_max_steps", 10))
        # Шаблоны и старые настройки хранят групповые имена («files»),
        # поэтому обе стороны разворачиваются до реальных инструментов.
        enabled = expand_tool_names(workspace_settings.get("tools_enabled")) \
            or registry.names()
        self.tools_allowed = [
            name for name in expand_tool_names(agent.tools)
            if name in registry.names() and name in enabled
        ]

    # -- контекст ------------------------------------------------------------
    def _tool_context(self) -> ToolContext:
        """Границы прав агента на этот запуск."""
        from pathlib import Path

        extra = [Path(p) for p in (self.settings.get("extra_allowed_paths") or [])]
        return ToolContext(
            workspace_dir=PATHS.workspace_dir(self.workspace_id),
            agent_id=self.agent.id,
            subtask_id=self.subtask.id,
            extra_allowed_paths=extra,
            sandbox_backend=self.settings.get("sandbox_backend", "auto"),
            sandbox_timeout_sec=int(self.settings.get("sandbox_timeout_sec", 30)),
            sandbox_memory_mb=int(self.settings.get("sandbox_memory_mb", 512)),
            allow_network_in_sandbox=False,
            search_backend=self.settings.get("search_backend", "duckduckgo"),
            search_api_key=self.settings.get("search_api_key", ""),
            fetch_pages=bool(self.settings.get("fetch_pages", True)),
        )

    def _briefing(self) -> str:
        """Задание агенту: общая задача, своя подзадача, вход от предшественников."""
        parts = [
            "ОБЩАЯ ЗАДАЧА ПРОЕКТА",
            f"{self.task.title}\n{self.task.description}",
            "",
            "ТВОЯ ПОДЗАДАЧА",
            f"{self.subtask.title}",
        ]
        if self.subtask.description:
            parts.append(self.subtask.description)

        # Результаты подзадач, от которых зависит текущая: это не «чужая
        # переписка», а переданный по конвейеру артефакт работы.
        inputs = self._dependency_inputs()
        if inputs:
            parts += ["", "ИСХОДНЫЕ МАТЕРИАЛЫ (результаты предыдущих этапов)", inputs]

        summary = self._latest_summary()
        if summary:
            parts += [
                "",
                "АНОНИМНАЯ СВОДКА ПО ПРОЕКТУ",
                "(источник не указан намеренно — оценивай содержание, а не авторитет)",
                summary,
            ]

        if self.rework_notes:
            parts += ["", "ЗАМЕЧАНИЯ К ПРЕДЫДУЩЕЙ ВЕРСИИ (исправь их)", self.rework_notes]

        if self.tools_allowed:
            parts += ["", "Доступные инструменты: " + ", ".join(self.tools_allowed)]

        parts += [
            "",
            "Когда подзадача выполнена, выдай итог после строки RESULT: "
            "и укажи строку CONFIDENCE: <0..1>.",
        ]
        return "\n".join(parts)

    def _dependency_inputs(self) -> str:
        """Собирает результаты подзадач-предшественников."""
        raw = (self.subtask.depends_on or "").strip()
        if not raw:
            return ""
        chunks: list[str] = []
        for token in raw.split(","):
            token = token.strip()
            if not token.isdigit():
                continue
            dep = self.repos.tasks.get_subtask(int(token))
            if dep and dep.result:
                chunks.append(f"— {dep.title}:\n{dep.result[:4000]}")
        return "\n\n".join(chunks)

    def _latest_summary(self) -> str:
        summaries = self.repos.reports.list_summaries(self.workspace_id, limit=1)
        return summaries[0].content if summaries else ""

    def _history(self) -> list[ChatMessage]:
        """Личная история агента по этой подзадаче, при необходимости сжатая."""
        rows = self.repos.messages.history(self.agent.id, self.subtask.id, limit=200)
        if not rows:
            return []
        total = sum(len(r["content"] or "") for r in rows)
        if total > HISTORY_COMPACT_CHARS or len(rows) > HISTORY_WINDOW:
            head, tail = rows[:2], rows[-HISTORY_WINDOW:]
            dropped = len(rows) - len(head) - len(tail)
            rows = head + ([{
                "role": "user",
                "content": f"[…пропущено {dropped} промежуточных шагов работы…]",
                "tool_call_id": "", "tool_name": "",
            }] if dropped > 0 else []) + tail
        return [
            ChatMessage(role=r["role"], content=r["content"] or "",
                        tool_call_id=r.get("tool_call_id", "") or "",
                        name=r.get("tool_name", "") or "")
            for r in rows
            # tool-сообщения без парного вызова ломают формат части провайдеров
            if r["role"] in ("user", "assistant")
        ]

    # -- учёт расхода --------------------------------------------------------
    def _account(self, result: CompletionResult) -> float:
        """Пишет расход в журнал и в бюджет задачи."""
        cost = estimate_cost(self.agent.provider, self.agent.model,
                             result.usage.input_tokens, result.usage.output_tokens)
        self.repos.budgets.log_call(
            self.workspace_id, self.task.id, self.subtask.id, self.agent.id,
            self.agent.provider, self.agent.model,
            result.usage.input_tokens, result.usage.output_tokens, cost,
        )
        if self.budget:
            self.budget.add(result.usage.total, cost, self.agent.id)
        self.bus.emit(Event(
            EventType.USAGE, workspace_id=self.workspace_id, task_id=self.task.id,
            subtask_id=self.subtask.id, agent_id=self.agent.id,
            agent_name=self.agent.name,
            message=f"+{result.usage.total} токенов (~${cost:.4f})",
            payload={"tokens": result.usage.total, "cost": cost},
        ))
        return cost

    def _emit(self, kind: EventType, message: str, **payload) -> None:
        self.bus.emit(Event(
            kind, workspace_id=self.workspace_id, task_id=self.task.id,
            subtask_id=self.subtask.id, agent_id=self.agent.id,
            agent_name=self.agent.name, message=message, payload=payload,
        ))

    # -- основной цикл -------------------------------------------------------
    async def run(self) -> RunResult:
        """Прогоняет ReAct-цикл до готового результата или до стоп-условия."""
        tool_ctx = self._tool_context()
        specs = self.registry.specs(self.tools_allowed)

        system_prompt = self.agent.system_prompt.strip() or "Ты — полезный ассистент."
        messages: list[ChatMessage] = [ChatMessage("system", system_prompt)]
        messages += self._history()
        briefing = self._briefing()
        messages.append(ChatMessage("user", briefing))
        self.repos.messages.add(self.agent.id, "user", briefing, self.subtask.id)

        totals = RunResult(ok=False)
        last_text = ""

        for step in range(1, self.max_steps + 1):
            # Проверка ДО вызова модели: узнавать о лимите постфактум
            # бессмысленно — деньги уже потрачены.
            blocked = (self.budget.blocking_scope(self.agent.id)
                       if self.budget else None)
            if blocked is not None:
                totals.error = f"Лимит исчерпан — {blocked.reason()}"
                self._emit(EventType.SUBTASK_FAILED, totals.error)
                return totals

            totals.steps = step
            self._emit(EventType.AGENT_THINKING, f"шаг {step}/{self.max_steps}", step=step)

            try:
                result = await self.provider.complete(
                    self.agent.model, messages,
                    temperature=self.agent.temperature,
                    max_tokens=self.agent.max_tokens,
                    tools=specs or None,
                )
            except asyncio.CancelledError:
                raise
            except ProviderError as exc:
                totals.error = f"Провайдер: {exc}"
                self._emit(EventType.SUBTASK_FAILED, totals.error)
                return totals
            except Exception as exc:  # noqa: BLE001
                log.exception("Сбой вызова модели")
                totals.error = f"{type(exc).__name__}: {exc}"
                self._emit(EventType.SUBTASK_FAILED, totals.error)
                return totals

            totals.tokens_in += result.usage.input_tokens
            totals.tokens_out += result.usage.output_tokens
            totals.cost_usd += self._account(result)
            last_text = result.text or last_text

            # Ответ модели сохраняем в её личную историю.
            if result.text:
                self.repos.messages.add(self.agent.id, "assistant", result.text,
                                        self.subtask.id, tokens=result.usage.output_tokens)

            if not result.tool_calls:
                if looks_done(result.text) or step == self.max_steps:
                    totals.ok = True
                    totals.result_text = parse_result(result.text)
                    totals.confidence = parse_confidence(result.text)
                    self._emit(EventType.SUBTASK_PROGRESS, "получен результат")
                    return totals
                # Модель ответила текстом, но не обозначила финал — просим завершить.
                messages.append(ChatMessage("assistant", result.text))
                nudge = ("Если подзадача выполнена — выдай итог после строки RESULT: "
                         "и строку CONFIDENCE. Если нет — продолжай работу.")
                messages.append(ChatMessage("user", nudge))
                continue

            # --- есть вызовы инструментов ---
            messages.append(ChatMessage("assistant", result.text,
                                        tool_calls=result.tool_calls))
            for call in result.tool_calls:
                output = await self._invoke_tool(call, tool_ctx, totals)
                messages.append(ChatMessage("tool", output, tool_call_id=call.id,
                                            name=call.name))
                self.repos.messages.add(self.agent.id, "tool", output[:20000],
                                        self.subtask.id, tool_name=call.name,
                                        tool_call_id=call.id)

        # Шаги кончились — отдаём то, что есть.
        totals.ok = bool(last_text)
        totals.result_text = parse_result(last_text)
        totals.confidence = parse_confidence(last_text)
        if not totals.ok:
            totals.error = "Агент не выдал результат за отведённое число шагов"
        return totals

    async def _invoke_tool(self, call: ToolCall, ctx: ToolContext,
                           totals: RunResult) -> str:
        """Вызывает инструмент с проверкой прав и сообщает об этом в ленту."""
        if call.name not in self.tools_allowed:
            return (f"ОШИБКА: инструмент «{call.name}» не разрешён этому агенту. "
                    f"Доступны: {', '.join(self.tools_allowed) or 'нет'}")
        totals.tool_calls.append(call.name)
        preview = ", ".join(f"{k}={str(v)[:60]}" for k, v in call.arguments.items())
        self._emit(EventType.AGENT_TOOL_CALL, f"{call.name}({preview})", tool=call.name)

        output = await self.registry.invoke(call.name, ctx, **call.arguments)
        self._emit(EventType.AGENT_TOOL_RESULT,
                   f"{call.name} → {output[:120].replace(chr(10), ' ')}", tool=call.name)
        return output


class TokenBudget:
    """Простой счётчик на один лимит.

    Оставлен как запасной вариант и для тестов: интерфейс совпадает с
    ``BudgetGuard`` (``add`` / ``exhausted`` / ``blocking_scope``), поэтому
    их можно подставлять друг вместо друга.
    """

    def __init__(self, limit: int | None) -> None:
        self.limit = limit
        self.tokens = 0
        self.cost = 0.0

    def add(self, tokens: int, cost: float, agent_id: int | None = None) -> None:
        self.tokens += tokens
        self.cost += cost

    def exhausted(self, agent_id: int | None = None) -> bool:
        return self.limit is not None and self.tokens >= self.limit

    def blocking_scope(self, agent_id: int | None = None):
        """Возвращает объект с объяснением, чтобы сообщение было единообразным."""
        if not self.exhausted():
            return None
        from core.budget import Limit, ScopeState

        return ScopeState("task", 0, "задача", Limit(self.limit),
                          self.tokens, self.cost)

    def ratio(self) -> float:
        return (self.tokens / self.limit) if self.limit else 0.0
````

### `core/orchestrator.py`

*707 строк*

````python
"""Этап 4 — оркестратор выполнения задачи.

Отвечает за расписание: какие подзадачи можно запускать сейчас, какие ждут
предшественников, сколько агентов работают параллельно. Каждый агент
выполняет свои подзадачи последовательно (семафор на агента), разные агенты —
параллельно, все в одном asyncio-лупе.

Оркестратор ведёт весь жизненный цикл: статусы, отчёты, расход, паузы и
корректную остановку по требованию пользователя.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field

from app.config import DEFAULT_WORKSPACE_SETTINGS, PATHS
from core.agents.runner import AgentRunner, RunResult
from core.budget import BudgetGuard
from core.events import Event, EventBus, EventType
from core.hitl import ApprovalGate, Decision, Reason
from core.supervisor.supervisor import Supervisor
from core.tools.base import ToolRegistry, default_registry
from providers.base import LLMProvider
from providers.factory import build_provider
from storage.models import Agent, Report, Subtask, Task
from storage.repositories import Repos

log = logging.getLogger("aiorc.orchestrator")

#: сколько дополнительных кругов доработки может выдать человек
#: сверх автоматического лимита супервайзера
USER_REWORK_LIMIT = 3

#: сколько агентов могут работать одновременно
DEFAULT_CONCURRENCY = 6


@dataclass
class RunState:
    """Наблюдаемое состояние текущего прогона."""

    running: bool = False
    paused: bool = False
    task_id: int | None = None
    started_at: str = ""
    finished: int = 0
    total: int = 0
    failed: int = 0
    tokens: int = 0
    cost: float = 0.0
    reworks: int = 0
    escalated: int = 0
    errors: list[str] = field(default_factory=list)


class Orchestrator:
    """Запускает подзадачи задачи и собирает отчёты агентов."""

    def __init__(self, repos: Repos, bus: EventBus,
                 registry: ToolRegistry | None = None) -> None:
        self.repos = repos
        self.bus = bus
        self.registry = registry or default_registry()
        self.state = RunState()

        self._pause = asyncio.Event()
        self._pause.set()                       # «не на паузе»
        self._stop = asyncio.Event()
        self._tasks: set[asyncio.Task] = set()
        self._agent_locks: dict[int, asyncio.Lock] = {}
        self._providers: dict[int, LLMProvider] = {}
        self._budget: BudgetGuard | None = None
        self._supervisor: Supervisor | None = None
        self._summary_on_event: bool = True
        self._gate: ApprovalGate | None = None
        self._confidence_threshold: float = 0.0

    # -- управление ----------------------------------------------------------
    def pause(self) -> None:
        if self.state.running and not self.state.paused:
            self.state.paused = True
            self._pause.clear()
            self.bus.emit(Event(EventType.RUN_PAUSED, task_id=self.state.task_id,
                                message="Выполнение поставлено на паузу"))

    def resume(self) -> None:
        if self.state.running and self.state.paused:
            self.state.paused = False
            self._pause.set()
            self.bus.emit(Event(EventType.RUN_RESUMED, task_id=self.state.task_id,
                                message="Выполнение возобновлено"))

    def stop(self) -> None:
        if not self.state.running:
            return
        self._stop.set()
        self._pause.set()                       # разбудить ожидающих
        for task in list(self._tasks):
            task.cancel()
        self.bus.emit(Event(EventType.RUN_STOPPED, task_id=self.state.task_id,
                            message="Остановка по команде пользователя"))

    # -- основной запуск -----------------------------------------------------
    async def run_task(self, workspace_id: int, task_id: int,
                       concurrency: int = DEFAULT_CONCURRENCY) -> RunState:
        """Прогоняет все подзадачи задачи с учётом зависимостей."""
        if self.state.running:
            raise RuntimeError("Выполнение уже запущено")

        workspace = self.repos.workspaces.get(workspace_id)
        task = self.repos.tasks.get(task_id)
        if workspace is None or task is None:
            raise RuntimeError("Воркспейс или задача не найдены")

        settings = {**DEFAULT_WORKSPACE_SETTINGS, **workspace.settings}
        PATHS.workspace_dir(workspace_id).mkdir(parents=True, exist_ok=True)

        subtasks = [s for s in self.repos.tasks.subtasks(task_id)
                    if s.status not in ("done",)]
        unassigned = [s for s in subtasks if not s.agent_id]
        if unassigned:
            raise RuntimeError(
                "Не у всех подзадач назначен исполнитель: "
                + ", ".join(s.title for s in unassigned[:5])
            )
        if not subtasks:
            raise RuntimeError("Нет подзадач для выполнения")

        self._reset_state(task_id, len(subtasks))
        self._budget = BudgetGuard(self.repos, self.bus, workspace_id,
                                   task.id, task.token_limit)
        self.repos.tasks.update(task_id, status="running")
        self.bus.emit(Event(EventType.RUN_STARTED, workspace_id=workspace_id,
                            task_id=task_id,
                            message=f"Запуск: {len(subtasks)} подзадач"))

        self._start_supervisor(workspace_id, settings, task)
        self._start_gate(workspace_id, settings)

        semaphore = asyncio.Semaphore(max(1, concurrency))
        try:
            await self._schedule(workspace_id, settings, task, subtasks, semaphore)
            if self._supervisor is not None and not self._stop.is_set():
                # Финальный разбор: ищем расхождения между результатами
                # и подводим общий итог для команды.
                await self._supervisor.find_conflicts(task)
                await self._supervisor.make_summary(task, trigger="final")
        except asyncio.CancelledError:
            log.info("Прогон отменён")
        finally:
            await self._cleanup()
            self.state.running = False
            self.repos.tasks.update(
                task_id,
                status="stopped" if self._stop.is_set()
                else ("failed" if self.state.failed else "done"),
            )
            self.bus.emit(Event(
                EventType.RUN_FINISHED, workspace_id=workspace_id, task_id=task_id,
                message=(f"Готово: {self.state.finished} выполнено, "
                         f"{self.state.failed} с ошибкой, "
                         f"{self.state.reworks} доработок, "
                         f"{self.state.escalated} на решение пользователя, "
                         f"{self.state.tokens} токенов, ~${self.state.cost:.4f}"),
                payload={"finished": self.state.finished, "failed": self.state.failed,
                         "reworks": self.state.reworks,
                         "escalated": self.state.escalated},
            ))
        return self.state

    def _reset_state(self, task_id: int, total: int) -> None:
        from storage.db import utcnow

        self._stop.clear()
        self._pause.set()
        self._tasks.clear()
        self._agent_locks.clear()
        self.state = RunState(running=True, task_id=task_id, total=total,
                              started_at=utcnow())

    # -- расписание ----------------------------------------------------------
    async def _schedule(self, workspace_id: int, settings: dict, task: Task,
                        subtasks: list[Subtask], semaphore: asyncio.Semaphore) -> None:
        """Волнами запускает подзадачи, у которых выполнены зависимости."""
        pending = {s.id: s for s in subtasks}
        done_ids: set[int] = {
            s.id for s in self.repos.tasks.subtasks(task.id) if s.status == "done"
        }

        while pending and not self._stop.is_set():
            ready = [s for s in pending.values() if self._deps_met(s, done_ids)]
            if not ready:
                # Циклическая или неразрешимая зависимость — не зависаем молча.
                names = ", ".join(s.title for s in pending.values())
                self.bus.error(f"Невозможно разрешить зависимости подзадач: {names}",
                               workspace_id=workspace_id, task_id=task.id)
                for s in pending.values():
                    self.repos.tasks.update_subtask(s.id, status="error")
                    self.state.failed += 1
                break

            wave = [
                asyncio.ensure_future(
                    self._run_subtask(workspace_id, settings, task, s, semaphore)
                )
                for s in ready
            ]
            self._tasks.update(wave)
            results = await asyncio.gather(*wave, return_exceptions=True)
            for subtask, outcome in zip(ready, results):
                pending.pop(subtask.id, None)
                # CancelledError наследуется от BaseException, а не от Exception,
                # поэтому проверяем именно BaseException — иначе отменённая
                # подзадача была бы ошибочно засчитана как выполненная.
                if isinstance(outcome, asyncio.CancelledError):
                    continue
                if isinstance(outcome, BaseException):
                    self.state.failed += 1
                    self.state.errors.append(f"{subtask.title}: {outcome}")
                elif outcome:
                    done_ids.add(subtask.id)

            # Завершён этап работ: если пользователь просил останавливаться
            # на контрольных точках, спрашиваем перед следующей волной.
            # На последней волне вопрос не задаём — спрашивать «продолжать?»,
            # когда продолжать уже нечего, бессмысленно.
            if (pending and self._gate is not None and not self._stop.is_set()
                    and settings.get("hitl_pause_on_milestone")):
                answer = await self._gate.ask(
                    Reason.MILESTONE,
                    f"Завершён этап: готово {len(done_ids)} из {len(subtasks)} подзадач. "
                    f"Продолжать?",
                    details=self._wave_summary(task, done_ids),
                    task_id=task.id,
                )
                if answer.decision is Decision.ABORT:
                    self.bus.log("Прогон остановлен на контрольной точке",
                                 workspace_id=workspace_id, task_id=task.id)
                    self._stop.set()
                    break

    def _wave_summary(self, task: Task, done_ids: set[int]) -> str:
        """Короткая сводка по завершённой волне — чтобы решать осознанно."""
        lines: list[str] = []
        for subtask in self.repos.tasks.subtasks(task.id):
            if subtask.id not in done_ids:
                continue
            body = (subtask.result or "").strip().replace("\n", " ")
            lines.append(f"· {subtask.title}: {body[:180]}" if body else f"· {subtask.title}")
        tokens, cost = self.repos.budgets.workspace_totals(task.workspace_id)
        lines.append("")
        lines.append(f"Израсходовано: {tokens} токенов, ~${cost:.4f}")
        return "\n".join(lines)

    @staticmethod
    def _deps_met(subtask: Subtask, done_ids: set[int]) -> bool:
        raw = (subtask.depends_on or "").strip()
        if not raw:
            return True
        return all(int(tok) in done_ids
                   for tok in (t.strip() for t in raw.split(",")) if tok.isdigit())

    # -- выполнение одной подзадачи -----------------------------------------
    async def _run_subtask(self, workspace_id: int, settings: dict, task: Task,
                           subtask: Subtask, semaphore: asyncio.Semaphore) -> bool:
        agent = self.repos.agents.get(subtask.agent_id or 0)
        if agent is None or not agent.enabled:
            self._fail(subtask, agent, "Исполнитель недоступен или отключён")
            return False

        lock = self._agent_locks.setdefault(agent.id, asyncio.Lock())
        async with semaphore, lock:
            await self._pause.wait()
            if self._stop.is_set():
                return False

            provider = self._provider_for(agent)
            if provider is None:
                self._fail(subtask, agent, "У агента не настроен API-ключ или модель")
                return False

            self._set_status(agent, subtask, "running")
            self.bus.emit(Event(
                EventType.SUBTASK_STARTED, workspace_id=workspace_id, task_id=task.id,
                subtask_id=subtask.id, agent_id=agent.id, agent_name=agent.name,
                message=subtask.title,
            ))

            max_rework = int(settings.get("max_rework_rounds", 2))
            notes = self._rework_notes(subtask)

            # Цикл «выполнил → проверили → доработал». Лок агента держится
            # всё это время: доработку делает тот же исполнитель, и его
            # личная история остаётся связной.
            #
            # max_rework ограничивает АВТОМАТИЧЕСКИЕ доработки супервайзера.
            # Когда доработку назначает человек, он даёт дополнительный круг
            # сверх лимита: его решение важнее настройки. Жёсткий потолок
            # USER_REWORK_LIMIT защищает от бесконечного цикла, если человек
            # раз за разом возвращает работу.
            attempt = 0
            allowed = max_rework
            user_grants = 0          # сколько кругов уже выдал человек
            while attempt <= allowed:
                runner = AgentRunner(
                    self.repos, self.bus, self.registry, workspace_id, settings,
                    task, subtask, agent, provider, self._budget,
                    rework_notes=notes,
                )
                try:
                    result = await runner.run()
                except asyncio.CancelledError:
                    self._set_status(agent, subtask, "paused")
                    raise
                except Exception as exc:  # noqa: BLE001
                    log.exception("Агент %s упал на подзадаче %s", agent.name, subtask.id)
                    self._fail(subtask, agent, f"{type(exc).__name__}: {exc}")
                    return False

                accepted, notes, granted = await self._review_result(
                    workspace_id, task, subtask, agent, result, attempt, max_rework
                )
                if accepted is not None:
                    return accepted

                # accepted is None → назначена доработка, идём на новый круг
                # Потолок считается по числу выданных человеком кругов,
                # а не относительно текущей попытки: иначе граница уезжала бы
                # вперёд на каждом круге и цикл никогда бы не закончился.
                if granted and user_grants < USER_REWORK_LIMIT:
                    user_grants += 1
                    allowed = attempt + 1
                attempt += 1
                subtask = self.repos.tasks.get_subtask(subtask.id) or subtask
                await self._pause.wait()
                if self._stop.is_set():
                    return False

            self.bus.log(f"исчерпан лимит доработок по «{subtask.title}»",
                         workspace_id=workspace_id, subtask_id=subtask.id,
                         agent_name=agent.name)
            return False

    async def _review_result(self, workspace_id: int, task: Task, subtask: Subtask,
                             agent: Agent, result: RunResult,
                             attempt: int, max_rework: int
                             ) -> tuple[bool | None, str, bool]:
        """Сохраняет результат и проводит его через супервайзера.

        Возвращает ``(итог, замечания, доработку назначил человек)``:
        итог ``True``/``False`` — подзадача закрыта успешно или с ошибкой,
        ``None`` — назначена доработка. Третий флаг говорит вызывающему коду,
        что круг доработки нужно выдать сверх автоматического лимита.
        """
        finished = self._finish_subtask(workspace_id, task, subtask, agent, result)
        if not finished:
            return False, "", False

        supervisor = self._supervisor
        if supervisor is None:
            # Без супервайзера отчёт принимается как есть.
            self.repos.tasks.update_subtask(subtask.id, status="done")
            self.state.finished += 1
            return True, "", False

        report = self._last_report(subtask.id)
        if report is None:
            self.repos.tasks.update_subtask(subtask.id, status="done")
            self.state.finished += 1
            return True, "", False

        try:
            verdict = await supervisor.review(task, subtask, report)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
            log.exception("Супервайзер упал на проверке %s", subtask.id)
            self.bus.error(f"Проверка не выполнена: {exc}",
                           workspace_id=workspace_id, subtask_id=subtask.id)
            self.repos.tasks.update_subtask(subtask.id, status="done")
            self.state.finished += 1
            return True, "", False

        if verdict.accepted:
            self.repos.tasks.update_subtask(subtask.id, status="done")
            self.state.finished += 1
            # Замечания, из-за которых подзадача уходила на доработку,
            # закрываем: они больше не актуальны, а открытый инцидент
            # без причины только зашумляет историю.
            if subtask.rework_count or attempt > 0:
                closed = self.repos.incidents.resolve_for_subtask(
                    subtask.id, "Исправлено при доработке, результат принят"
                )
                if closed:
                    self.bus.log(f"закрыто замечаний после доработки: {closed}",
                                 workspace_id=workspace_id, subtask_id=subtask.id,
                                 agent_name="Супервайзер")
            # Супервайзер доволен, но сам исполнитель — нет. Это как раз тот
            # случай, когда дешевле спросить человека, чем нести сомнительный
            # результат дальше по цепочке подзадач.
            if (self._gate is not None and report.confidence is not None
                    and report.confidence < self._confidence_threshold):
                self._set_status(agent, subtask, "paused")
                answer = await self._gate.ask(
                    Reason.LOW_CONFIDENCE,
                    f"«{subtask.title}»: исполнитель оценил свою уверенность "
                    f"в {report.confidence:.2f}",
                    details=self._decision_details(subtask, report, verdict),
                    task_id=task.id, subtask_id=subtask.id, agent_name=agent.name,
                )
                if answer.decision is not Decision.APPROVE:
                    # Решение отменяет уже засчитанную приёмку.
                    self.state.finished -= 1
                    return await self._apply_decision(
                        workspace_id, task, subtask, agent, answer, None
                    )
                # Пользователь подтвердил результат — возвращаем статусы,
                # которые были сняты на время ожидания ответа.
                self.repos.tasks.update_subtask(subtask.id, status="done")
                self.repos.agents.set_status(agent.id, "idle")

            await self._maybe_summarize(task)
            return True, "", False

        can_rework = attempt < max_rework and verdict.verdict == "rework"
        if can_rework:
            self.state.reworks += 1
            self.repos.tasks.update_subtask(
                subtask.id, status="rework", rework_count=subtask.rework_count + 1
            )
            self.bus.emit(Event(
                EventType.SUBTASK_PROGRESS, workspace_id=workspace_id, task_id=task.id,
                subtask_id=subtask.id, agent_id=agent.id, agent_name=agent.name,
                message=f"доработка {attempt + 1}/{max_rework}: "
                        f"{verdict.notes[:120] or 'см. замечания супервайзера'}",
            ))
            return None, verdict.notes, False

        # Доработки исчерпаны либо это конфликт — фиксируем инцидент
        # и, если human-in-the-loop включён, останавливаемся и спрашиваем.
        self.repos.tasks.update_subtask(subtask.id, status="review")
        self.state.escalated += 1
        incident_id = self.repos.incidents.add(
            workspace_id,
            kind="conflict" if verdict.verdict == "conflict" else "contradiction",
            description=(verdict.notes
                         or "Супервайзер не принял результат после доработок"),
            severity=verdict.max_severity,
            task_id=task.id, subtask_id=subtask.id, report_id=report.id,
        )
        self.repos.incidents.resolve(incident_id, "escalated",
                                     "Требуется решение пользователя")

        if self._gate is None:
            # Режим без пауз: помечаем и идём дальше, решение остаётся человеку
            # постфактум на вкладке «Супервайзер».
            self.bus.emit(Event(
                EventType.APPROVAL_REQUESTED, workspace_id=workspace_id, task_id=task.id,
                subtask_id=subtask.id, agent_id=agent.id, agent_name=agent.name,
                message=f"нужно решение по «{subtask.title}»: {verdict.notes[:150]}",
                payload={"incident_id": incident_id, "verdict": verdict.verdict},
            ))
            self.state.finished += 1
            await self._maybe_summarize(task)
            return True, "", False

        reason = (Reason.CONFLICT if verdict.verdict == "conflict"
                  else Reason.NOT_ACCEPTED)
        self._set_status(agent, subtask, "paused")
        answer = await self._gate.ask(
            reason,
            f"«{subtask.title}»: {verdict.notes[:200] or 'результат не принят'}",
            details=self._decision_details(subtask, report, verdict),
            task_id=task.id, subtask_id=subtask.id, agent_name=agent.name,
        )
        return await self._apply_decision(workspace_id, task, subtask, agent,
                                          answer, incident_id)

    def _decision_details(self, subtask: Subtask, report: Report, verdict) -> str:
        """Готовит выжимку, по которой человек может принять решение не вслепую."""
        parts = [f"Подзадача: {subtask.description[:400]}" if subtask.description else ""]
        if verdict.issues:
            parts.append("Замечания супервайзера:\n" + "\n".join(
                f"· [{i.severity}] {i.description}" for i in verdict.issues
            ))
        parts.append("Результат исполнителя:\n" + (report.content or "")[:1200])
        return "\n\n".join(p for p in parts if p)

    async def _apply_decision(self, workspace_id: int, task: Task, subtask: Subtask,
                              agent: Agent, answer, incident_id: int | None
                              ) -> tuple[bool | None, str, bool]:
        """Применяет решение пользователя к подзадаче.

        Третий элемент кортежа — признак того, что круг доработки назначил
        человек, а значит его надо выдать сверх автоматического лимита.
        """
        if answer.decision is Decision.ABORT:
            self.bus.log("Прогон остановлен решением пользователя",
                         workspace_id=workspace_id, task_id=task.id)
            self._stop.set()
            self.repos.tasks.update_subtask(subtask.id, status="paused")
            self.repos.agents.set_status(agent.id, "paused")
            return False, "", False

        if answer.decision is Decision.REWORK:
            # Комментарий человека важнее замечаний супервайзера: он идёт
            # исполнителю первым и получает дополнительный круг доработки.
            self.state.reworks += 1
            self.repos.tasks.update_subtask(
                subtask.id, status="rework", rework_count=subtask.rework_count + 1
            )
            if incident_id:
                self.repos.incidents.resolve(
                    incident_id, "resolved",
                    f"Пользователь отправил на доработку: {answer.comment[:200]}"
                )
            self.state.escalated = max(0, self.state.escalated - 1)
            return None, answer.comment or "Пользователь вернул работу на доработку.", True

        if answer.decision is Decision.SKIP:
            self.repos.tasks.update_subtask(subtask.id, status="error")
            self.repos.agents.set_status(agent.id, "idle")
            self.state.failed += 1
            self.state.escalated = max(0, self.state.escalated - 1)
            if incident_id:
                self.repos.incidents.resolve(
                    incident_id, "resolved",
                    f"Подзадача пропущена пользователем: {answer.comment[:200]}"
                )
            self.bus.log(f"подзадача «{subtask.title}» пропущена",
                         workspace_id=workspace_id, subtask_id=subtask.id,
                         agent_name=agent.name)
            await self._maybe_summarize(task)
            return False, "", False

        # APPROVE: принимаем результат как есть
        self.repos.tasks.update_subtask(subtask.id, status="done")
        self.repos.agents.set_status(agent.id, "idle")
        self.state.finished += 1
        self.state.escalated = max(0, self.state.escalated - 1)
        if incident_id:
            self.repos.incidents.resolve(
                incident_id, "resolved",
                f"Принято пользователем: {answer.comment[:200] or 'без комментария'}"
            )
        await self._maybe_summarize(task)
        return True, "", False

    def _last_report(self, subtask_id: int) -> Report | None:
        row = self.repos.db.query_one(
            "SELECT * FROM reports WHERE subtask_id = ? ORDER BY id DESC LIMIT 1",
            (subtask_id,),
        )
        return Report.from_row(row) if row else None

    async def _maybe_summarize(self, task: Task) -> None:
        """Сводка по событию «агент завершил подзадачу», если она включена."""
        if self._supervisor is None or not self._summary_on_event:
            return
        try:
            await self._supervisor.make_summary(task, trigger="event")
        except asyncio.CancelledError:
            raise
        except Exception:  # noqa: BLE001
            log.exception("Сбой сводки по событию")

    def _finish_subtask(self, workspace_id: int, task: Task, subtask: Subtask,
                        agent: Agent, result: RunResult) -> bool:
        """Сохраняет результат, создаёт отчёт для супервайзера, обновляет счётчики."""
        self.state.tokens += result.tokens_in + result.tokens_out
        self.state.cost += result.cost_usd

        self.repos.tasks.update_subtask(
            subtask.id,
            status="review" if result.ok else "error",
            result=result.result_text,
            tokens_in=subtask.tokens_in + result.tokens_in,
            tokens_out=subtask.tokens_out + result.tokens_out,
            cost_usd=subtask.cost_usd + result.cost_usd,
        )

        if not result.ok:
            self.state.failed += 1
            self.repos.agents.set_status(agent.id, "error")
            self.bus.emit(Event(
                EventType.SUBTASK_FAILED, workspace_id=workspace_id, task_id=task.id,
                subtask_id=subtask.id, agent_id=agent.id, agent_name=agent.name,
                message=result.error or "Подзадача не выполнена",
            ))
            return False

        # Отчёт — это то, что увидит супервайзер на этапе 5.
        report_id = self.repos.reports.add_report(
            workspace_id, task.id, subtask.id, agent.id,
            content=result.result_text, confidence=result.confidence,
            tokens_in=result.tokens_in, tokens_out=result.tokens_out,
            cost_usd=result.cost_usd,
        )
        self.repos.agents.set_status(agent.id, "idle")

        confidence = f", уверенность {result.confidence:.2f}" if result.confidence else ""
        self.bus.emit(Event(
            EventType.REPORT_CREATED, workspace_id=workspace_id, task_id=task.id,
            subtask_id=subtask.id, agent_id=agent.id, agent_name=agent.name,
            message=f"Отчёт по «{subtask.title}» ({result.steps} шагов{confidence})",
            payload={"report_id": report_id, "confidence": result.confidence},
        ))
        self.bus.emit(Event(
            EventType.SUBTASK_FINISHED, workspace_id=workspace_id, task_id=task.id,
            subtask_id=subtask.id, agent_id=agent.id, agent_name=agent.name,
            message=subtask.title,
        ))
        return True

    def _rework_notes(self, subtask: Subtask) -> str:
        """Замечания супервайзера к прошлой версии подзадачи (используется на этапе 5)."""
        if subtask.rework_count <= 0:
            return ""
        row = self.repos.db.query_one(
            "SELECT review_notes FROM reports WHERE subtask_id = ? AND review_notes <> '' "
            "ORDER BY id DESC LIMIT 1",
            (subtask.id,),
        )
        return row["review_notes"] if row else ""

    # -- служебное -----------------------------------------------------------
    def _provider_for(self, agent: Agent) -> LLMProvider | None:
        """Кэширует по одному HTTP-клиенту на агента за прогон."""
        if agent.id in self._providers:
            return self._providers[agent.id]
        if not agent.model or not agent.api_key_id:
            return None
        key = self.repos.keys.get(agent.api_key_id)
        if key is None:
            return None
        secret = self.repos.keys.reveal(agent.api_key_id)
        provider = build_provider(agent.provider, secret, key.base_url)
        self._providers[agent.id] = provider
        return provider

    def _set_status(self, agent: Agent, subtask: Subtask, status: str) -> None:
        self.repos.agents.set_status(agent.id, status)
        self.repos.tasks.update_subtask(subtask.id, status=status)
        self.bus.emit(Event(EventType.AGENT_STATUS, agent_id=agent.id,
                            agent_name=agent.name, subtask_id=subtask.id,
                            message=status, payload={"status": status}))

    def _fail(self, subtask: Subtask, agent: Agent | None, message: str) -> None:
        self.state.failed += 1
        self.repos.tasks.update_subtask(subtask.id, status="error")
        if agent:
            self.repos.agents.set_status(agent.id, "error")
        self.bus.emit(Event(
            EventType.SUBTASK_FAILED, subtask_id=subtask.id,
            agent_id=agent.id if agent else None,
            agent_name=agent.name if agent else "", message=message,
        ))

    def _start_gate(self, workspace_id: int, settings: dict) -> None:
        """Включает human-in-the-loop, если он разрешён в настройках проекта."""
        if not settings.get("human_in_the_loop", True):
            self._gate = None
            self._confidence_threshold = 0.0
            self.bus.log("Human-in-the-loop выключен — система не будет останавливаться",
                         workspace_id=workspace_id)
            return
        self._gate = ApprovalGate(self.repos, self.bus, workspace_id)
        try:
            self._confidence_threshold = float(
                settings.get("hitl_confidence_threshold", 0.5) or 0.0
            )
        except (TypeError, ValueError):
            self._confidence_threshold = 0.5

    @property
    def gate(self) -> ApprovalGate | None:
        """Ворота согласования — интерфейс отдаёт через них решения пользователя."""
        return self._gate

    def _start_supervisor(self, workspace_id: int, settings: dict, task: Task) -> None:
        """Поднимает супервайзера, если он настроен, и включает сводки по таймеру."""
        self._summary_on_event = bool(settings.get("summary_on_event", True))
        supervisor = Supervisor(self.repos, self.bus, workspace_id, settings)
        if not supervisor.available():
            self._supervisor = None
            self.bus.log("Супервайзер не настроен — отчёты принимаются без проверки",
                         workspace_id=workspace_id, task_id=task.id)
            return
        self._supervisor = supervisor
        supervisor.start_timer(task)

    async def _cleanup(self) -> None:
        if self._gate is not None:
            self._gate.cancel_all()
            self._gate = None
        if self._supervisor is not None:
            await self._supervisor.aclose()
            self._supervisor = None
        for provider in self._providers.values():
            try:
                await provider.aclose()
            except Exception:  # noqa: BLE001
                pass
        self._providers.clear()
        self._tasks.clear()
````

### `core/planner.py`

*140 строк*

````python
"""Автоматическое разбиение задачи на подзадачи через ИИ (этап 3).

Планировщик — обычный вызов модели с требованием вернуть строгий JSON.
Модель берётся у агента-супервайзера, а если он не назначен — у первого
доступного агента воркспейса.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass

from providers.base import ChatMessage
from providers.factory import build_provider, estimate_cost
from storage.models import Agent
from storage.repositories import Repos

log = logging.getLogger("aiorc.planner")

PLANNER_SYSTEM = """\
Ты — планировщик работ. Тебе дают формулировку задачи и список доступных \
исполнителей с их ролями. Разбей задачу на 3-8 последовательных подзадач.

Требования к разбиению:
- каждая подзадача самодостаточна и проверяема, её результат можно предъявить;
- подзадачи не дублируют друг друга;
- исполнитель подбирается по роли; если подходящего нет, ставь assignee_role = null;
- формулировки конкретные, без общих слов вроде «проработать вопрос».

Ответь СТРОГО одним JSON-объектом без markdown-разметки и пояснений:
{"subtasks": [{"title": "...", "description": "...", "assignee_role": "analyst"}]}
"""


@dataclass
class PlannedSubtask:
    title: str
    description: str
    assignee_role: str | None = None


def _extract_json(text: str) -> dict:
    """Достаёт JSON, даже если модель обернула его в ```json ... ```."""
    cleaned = text.strip()
    fence = re.search(r"```(?:json)?\s*(.+?)```", cleaned, re.DOTALL)
    if fence:
        cleaned = fence.group(1).strip()
    try:
        return json.loads(cleaned)
    except ValueError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start >= 0 and end > start:
            return json.loads(cleaned[start:end + 1])
        raise


def choose_planner_agent(repos: Repos, workspace_id: int) -> Agent | None:
    """Супервайзер, иначе первый включённый агент с моделью."""
    agents = repos.agents.list(workspace_id)
    for a in agents:
        if a.is_supervisor and a.model and a.api_key_id:
            return a
    for a in agents:
        if a.enabled and a.model and a.api_key_id:
            return a
    return None


async def plan_subtasks(repos: Repos, workspace_id: int,
                        task_title: str, task_text: str) -> list[PlannedSubtask]:
    """Просит модель разбить задачу; возвращает список подзадач."""
    agent = choose_planner_agent(repos, workspace_id)
    if agent is None:
        raise RuntimeError(
            "Нет ни одного агента с моделью и ключом — некому планировать. "
            "Создайте агента на вкладке «Агенты»."
        )

    roster = [
        {"name": a.name, "role": a.role}
        for a in repos.agents.list(workspace_id)
        if a.enabled and not a.is_supervisor
    ]
    user_prompt = (
        f"ЗАДАЧА: {task_title}\n\n{task_text}\n\n"
        f"ДОСТУПНЫЕ ИСПОЛНИТЕЛИ: {json.dumps(roster, ensure_ascii=False)}"
    )

    secret = repos.keys.reveal(agent.api_key_id) if agent.api_key_id else ""
    key = repos.keys.get(agent.api_key_id) if agent.api_key_id else None
    provider = build_provider(agent.provider, secret, key.base_url if key else "")
    try:
        result = await provider.complete(
            agent.model,
            [ChatMessage("system", PLANNER_SYSTEM), ChatMessage("user", user_prompt)],
            temperature=0.3,
            max_tokens=2048,
        )
    finally:
        await provider.aclose()

    # Учёт расхода — планирование тоже стоит денег.
    cost = estimate_cost(agent.provider, agent.model,
                         result.usage.input_tokens, result.usage.output_tokens)
    repos.budgets.log_call(workspace_id, None, None, agent.id, agent.provider,
                           agent.model, result.usage.input_tokens,
                           result.usage.output_tokens, cost)

    try:
        data = _extract_json(result.text)
    except ValueError as exc:
        log.warning("Планировщик вернул не-JSON: %s", result.text[:400])
        raise RuntimeError("Модель вернула ответ не в формате JSON. "
                           "Попробуйте ещё раз или выберите другую модель.") from exc

    out: list[PlannedSubtask] = []
    for item in data.get("subtasks", []):
        title = str(item.get("title", "")).strip()
        if not title:
            continue
        out.append(PlannedSubtask(
            title=title,
            description=str(item.get("description", "")).strip(),
            assignee_role=(item.get("assignee_role") or None),
        ))
    if not out:
        raise RuntimeError("Модель не вернула ни одной подзадачи.")
    return out


def match_agent_by_role(repos: Repos, workspace_id: int, role: str | None) -> int | None:
    """Подбирает агента под предложенную планировщиком роль."""
    if not role:
        return None
    for a in repos.agents.list(workspace_id):
        if a.enabled and not a.is_supervisor and a.role == role:
            return a.id
    return None
````

### `core/supervisor/checklist.py`

*305 строк*

````python
"""Этап 5 — промпты супервайзера и разбор его ответов.

Ключевая идея анонимизации: супервайзер видит отчёты как «Исполнитель A/B/C»,
а не по именам агентов, и сводку для команды пересказывает своими словами.
Так исчезает эффект «слепого доверия авторитету»: у сводки нет ни автора,
ни узнаваемого стиля, только содержание.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

# ---------------------------------------------------------------------------
# Чек-лист проверки отчёта
# ---------------------------------------------------------------------------

REVIEW_SYSTEM = """\
Ты — супервайзер команды исполнителей. Ты не переписываешь работу за них:
ты выносишь вердикт и формулируешь, что именно нужно исправить.

Проверь отчёт строго по чек-листу:
1. СООТВЕТСТВИЕ ЗАДАНИЮ — отчёт отвечает именно на поставленную подзадачу,
   ничего из требуемого не пропущено, лишнего не добавлено.
2. ЛОГИЧЕСКАЯ НЕПРОТИВОРЕЧИВОСТЬ — выводы следуют из приведённых данных,
   внутри отчёта нет взаимоисключающих утверждений.
3. ФАКТИЧЕСКИЕ ОШИБКИ — проверяемые утверждения верны, нет выдуманных
   источников, цифр, API, цитат и ссылок.
4. СОГЛАСОВАННОСТЬ С ПРОЕКТОМ — отчёт не противоречит ранее принятым
   результатам других подзадач.

Будь требователен, но конкретен: замечание без указания, что именно исправить,
бесполезно. Не придирайся к стилю и оформлению, если суть верна.

Вердикты:
- "ok"       — работа принимается;
- "rework"   — есть исправимые недостатки, нужна доработка;
- "conflict" — отчёт противоречит другим результатам проекта, нужен разбор.

Ответь СТРОГО одним JSON-объектом без markdown и пояснений:
{
  "verdict": "ok" | "rework" | "conflict",
  "notes": "что именно исправить, по пунктам; пусто если verdict=ok",
  "issues": [
    {"kind": "off_scope" | "contradiction" | "factual_error" | "conflict",
     "severity": "low" | "medium" | "high",
     "description": "суть проблемы одной-двумя фразами"}
  ],
  "confidence": 0.0
}
"""

REVIEW_USER = """\
ОБЩАЯ ЗАДАЧА ПРОЕКТА
{task}

ПРОВЕРЯЕМАЯ ПОДЗАДАЧА
{subtask}

ОТЧЁТ ({label})
самооценка уверенности исполнителя: {confidence}
---
{report}
---
{context}"""

# ---------------------------------------------------------------------------
# Сводка для команды
# ---------------------------------------------------------------------------

SUMMARY_SYSTEM = """\
Ты — супервайзер проекта. Составь краткую сводку хода работ для всех
исполнителей.

Жёсткие требования:
- пиши СВОИМИ СЛОВАМИ, не копируй формулировки из отчётов;
- НЕ указывай, кто что сделал: ни имён, ни ролей, ни «первый исполнитель»;
- отделяй проверенные факты от предположений;
- отдельно перечисли расхождения между результатами, если они есть;
- отдельно перечисли открытые вопросы, которые мешают двигаться дальше;
- не более 250 слов, без вступлений и заключений.

Формат ответа — обычный текст с тремя разделами:
ФАКТЫ:
РАСХОЖДЕНИЯ:
ОТКРЫТЫЕ ВОПРОСЫ:
Раздел без содержания пиши как «нет».
"""

SUMMARY_USER = """\
ОБЩАЯ ЗАДАЧА ПРОЕКТА
{task}

МАТЕРИАЛЫ (источники обезличены намеренно)
{reports}"""

# ---------------------------------------------------------------------------
# Поиск конфликтов между отчётами
# ---------------------------------------------------------------------------

CONFLICT_SYSTEM = """\
Ты — супервайзер. Сравни результаты разных подзадач одного проекта и найди
ПРЯМЫЕ противоречия: взаимоисключающие утверждения, несовпадающие числа,
разные ответы на один и тот же вопрос.

Не считай противоречием: разный уровень детализации, разный ракурс на одну
тему, дополняющие друг друга сведения.

Для каждого противоречия оцени, можно ли решить его автоматически — то есть
существует ли объективный признак, по которому одна из версий очевидно верна
(свежая дата, первичный источник, арифметическая проверка).

Ответь СТРОГО одним JSON-объектом:
{
  "conflicts": [
    {"description": "в чём противоречие",
     "severity": "low" | "medium" | "high",
     "labels": ["Исполнитель A", "Исполнитель B"],
     "auto_resolvable": true | false,
     "resolution": "какая версия верна и почему; пусто если решить нельзя"}
  ]
}
Если противоречий нет — верни {"conflicts": []}.
"""


# ---------------------------------------------------------------------------
# Структуры ответов
# ---------------------------------------------------------------------------


@dataclass
class Issue:
    """Одно замечание супервайзера."""

    kind: str = "contradiction"
    severity: str = "medium"
    description: str = ""


@dataclass
class Verdict:
    """Результат проверки одного отчёта."""

    verdict: str = "ok"                      # ok | rework | conflict
    notes: str = ""
    issues: list[Issue] = field(default_factory=list)
    confidence: float | None = None
    raw: str = ""

    @property
    def accepted(self) -> bool:
        return self.verdict == "ok"

    @property
    def max_severity(self) -> str:
        order = {"low": 0, "medium": 1, "high": 2}
        if not self.issues:
            return "low"
        return max((i.severity for i in self.issues), key=lambda s: order.get(s, 1))


@dataclass
class Conflict:
    """Расхождение между результатами разных подзадач."""

    description: str = ""
    severity: str = "medium"
    labels: list[str] = field(default_factory=list)
    auto_resolvable: bool = False
    resolution: str = ""


# ---------------------------------------------------------------------------
# Разбор
# ---------------------------------------------------------------------------

_VALID_VERDICTS = {"ok", "rework", "conflict"}
_VALID_KINDS = {"off_scope", "contradiction", "factual_error", "conflict"}
_VALID_SEVERITY = {"low", "medium", "high"}


def extract_json(text: str) -> dict[str, Any]:
    """Достаёт JSON из ответа модели, даже если он обёрнут в ```json."""
    cleaned = (text or "").strip()
    fence = re.search(r"```(?:json)?\s*(.+?)```", cleaned, re.DOTALL)
    if fence:
        cleaned = fence.group(1).strip()
    try:
        data = json.loads(cleaned)
    except ValueError:
        start, end = cleaned.find("{"), cleaned.rfind("}")
        if start < 0 or end <= start:
            raise
        data = json.loads(cleaned[start:end + 1])
    return data if isinstance(data, dict) else {}


def parse_verdict(text: str) -> Verdict:
    """Разбирает вердикт. Нечитаемый ответ трактуется как «нужна доработка»,
    потому что молча принять непроверенный отчёт хуже, чем перепроверить."""
    try:
        data = extract_json(text)
    except ValueError:
        return Verdict(
            verdict="rework",
            notes="Супервайзер не смог вынести структурированный вердикт. "
                  "Переформулируй отчёт короче и по пунктам.",
            raw=text,
        )

    verdict = str(data.get("verdict", "ok")).lower().strip()
    if verdict not in _VALID_VERDICTS:
        verdict = "rework"

    issues: list[Issue] = []
    for item in data.get("issues") or []:
        if not isinstance(item, dict):
            continue
        kind = str(item.get("kind", "contradiction")).lower()
        severity = str(item.get("severity", "medium")).lower()
        issues.append(Issue(
            kind=kind if kind in _VALID_KINDS else "contradiction",
            severity=severity if severity in _VALID_SEVERITY else "medium",
            description=str(item.get("description", "")).strip(),
        ))

    confidence = data.get("confidence")
    try:
        confidence = min(max(float(confidence), 0.0), 1.0) if confidence is not None else None
    except (TypeError, ValueError):
        confidence = None

    return Verdict(
        verdict=verdict,
        notes=str(data.get("notes", "")).strip(),
        issues=issues,
        confidence=confidence,
        raw=text,
    )


def parse_conflicts(text: str) -> list[Conflict]:
    """Разбирает список конфликтов; при нечитаемом ответе возвращает пустой список."""
    try:
        data = extract_json(text)
    except ValueError:
        return []
    out: list[Conflict] = []
    for item in data.get("conflicts") or []:
        if not isinstance(item, dict):
            continue
        description = str(item.get("description", "")).strip()
        if not description:
            continue
        severity = str(item.get("severity", "medium")).lower()
        out.append(Conflict(
            description=description,
            severity=severity if severity in _VALID_SEVERITY else "medium",
            labels=[str(x) for x in (item.get("labels") or [])],
            auto_resolvable=bool(item.get("auto_resolvable")),
            resolution=str(item.get("resolution", "")).strip(),
        ))
    return out


# ---------------------------------------------------------------------------
# Анонимизация
# ---------------------------------------------------------------------------

_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class Anonymizer:
    """Устойчиво подменяет id агентов на метки «Исполнитель A», «Исполнитель B»…

    Метки стабильны в пределах одного объекта, поэтому супервайзер может
    ссылаться на них внутри одного разбора, но за пределы сводки имена
    не утекают.
    """

    def __init__(self) -> None:
        self._labels: dict[int, str] = {}

    def label(self, agent_id: int | None) -> str:
        if agent_id is None:
            return "Исполнитель ?"
        if agent_id not in self._labels:
            index = len(self._labels)
            suffix = (_ALPHABET[index] if index < len(_ALPHABET)
                      else f"{index + 1}")
            self._labels[agent_id] = f"Исполнитель {suffix}"
        return self._labels[agent_id]

    def scrub(self, text: str, names: dict[int, str]) -> str:
        """Вычищает имена агентов из готового текста — страховка на случай,
        если модель всё-таки назвала кого-то по имени."""
        result = text or ""
        for agent_id, name in names.items():
            if name and len(name) > 2:
                result = re.sub(re.escape(name), self.label(agent_id), result,
                                flags=re.IGNORECASE)
        return result
````

### `core/supervisor/supervisor.py`

*338 строк*

````python
"""Этап 5 — служба супервайзера.

Обязанности:
* проверять отчёты агентов по чек-листу и выносить вердикт;
* возвращать работу на доработку (не более ``max_rework_rounds`` раз);
* составлять анонимные сводки и рассылать их всем агентам;
* находить противоречия между результатами и заводить инциденты;
* эскалировать пользователю то, что не разрешается автоматически.

Модель супервайзера выбирается в настройках воркспейса: либо один из
подключённых агентов со своим API-ключом, либо локальная модель через
OpenAI-совместимый endpoint (Ollama, по умолчанию Qwen) — она работает
офлайн и ничего не стоит.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass

from core.events import Event, EventBus, EventType
from core.supervisor.checklist import (
    CONFLICT_SYSTEM,
    REVIEW_SYSTEM,
    REVIEW_USER,
    SUMMARY_SYSTEM,
    SUMMARY_USER,
    Anonymizer,
    Conflict,
    Verdict,
    parse_conflicts,
    parse_verdict,
)
from providers.base import ChatMessage, LLMProvider, ProviderError
from providers.factory import build_provider, estimate_cost
from storage.models import Report, Subtask, Task
from storage.repositories import Repos

log = logging.getLogger("aiorc.supervisor")

#: сколько последних результатов подмешивать в контекст проверки
CONTEXT_REPORTS = 6
#: предел длины одного отчёта в промпте супервайзера
REPORT_CLIP = 6000


@dataclass
class SupervisorModel:
    """Чем именно работает супервайзер в этом прогоне."""

    provider: LLMProvider
    model: str
    provider_key: str
    source: str          # "api" | "local"
    label: str


class Supervisor:
    """Проверяющий над командой агентов."""

    def __init__(self, repos: Repos, bus: EventBus, workspace_id: int,
                 settings: dict) -> None:
        self.repos = repos
        self.bus = bus
        self.workspace_id = workspace_id
        self.settings = settings
        self.anon = Anonymizer()
        self._model: SupervisorModel | None = None
        self._summary_task: asyncio.Task | None = None
        self._stop = asyncio.Event()

    # -- модель --------------------------------------------------------------
    def available(self) -> bool:
        """Можно ли вообще запустить супервайзера с текущими настройками."""
        try:
            return self._resolve_model() is not None
        except Exception:  # noqa: BLE001
            return False

    def _resolve_model(self) -> SupervisorModel | None:
        """Создаёт провайдера супервайзера один раз на прогон."""
        if self._model is not None:
            return self._model

        mode = self.settings.get("supervisor_mode", "api")

        if mode == "local":
            base_url = (self.settings.get("supervisor_local_base_url")
                        or "http://localhost:11434/v1")
            model_name = self.settings.get("supervisor_local_model") or "qwen2.5:7b-instruct"
            provider = build_provider("ollama", "", base_url, timeout=180)
            self._model = SupervisorModel(provider, model_name, "ollama", "local",
                                          f"локальная модель {model_name}")
            return self._model

        agent_id = self.settings.get("supervisor_agent_id")
        agent = self.repos.agents.get(int(agent_id)) if agent_id else None
        if agent is None:
            # Запасной вариант: агент, помеченный звёздочкой в списке.
            agent = next((a for a in self.repos.agents.list(self.workspace_id)
                          if a.is_supervisor), None)
        if agent is None or not agent.model or not agent.api_key_id:
            return None

        key = self.repos.keys.get(agent.api_key_id)
        if key is None:
            return None
        secret = self.repos.keys.reveal(agent.api_key_id)
        provider = build_provider(agent.provider, secret, key.base_url, timeout=180)
        self._model = SupervisorModel(provider, agent.model, agent.provider, "api",
                                      f"{agent.name} ({agent.model})")
        return self._model

    async def aclose(self) -> None:
        self._stop.set()
        if self._summary_task:
            self._summary_task.cancel()
            self._summary_task = None
        if self._model is not None:
            try:
                await self._model.provider.aclose()
            except Exception:  # noqa: BLE001
                pass
            self._model = None

    # -- вызов модели --------------------------------------------------------
    async def _ask(self, system: str, user: str, task_id: int | None,
                   max_tokens: int = 1600) -> str:
        """Один вызов модели супервайзера с учётом расхода."""
        model = self._resolve_model()
        if model is None:
            raise RuntimeError(
                "Супервайзер не настроен: выберите агента или локальную модель "
                "на вкладке «Настройки»."
            )
        result = await model.provider.complete(
            model.model,
            [ChatMessage("system", system), ChatMessage("user", user)],
            temperature=0.2,          # проверка требует предсказуемости
            max_tokens=max_tokens,
        )
        cost = estimate_cost(model.provider_key, model.model,
                             result.usage.input_tokens, result.usage.output_tokens)
        self.repos.budgets.log_call(
            self.workspace_id, task_id, None, None,
            model.provider_key, model.model,
            result.usage.input_tokens, result.usage.output_tokens, cost,
        )
        return result.text

    def _emit(self, kind: EventType, message: str, **payload) -> None:
        self.bus.emit(Event(kind, workspace_id=self.workspace_id,
                            agent_name="Супервайзер", message=message,
                            payload=payload))

    # -- проверка отчёта -----------------------------------------------------
    async def review(self, task: Task, subtask: Subtask, report: Report) -> Verdict:
        """Проверяет отчёт по чек-листу и возвращает вердикт."""
        label = self.anon.label(report.agent_id)
        context = self._accepted_context(task.id, exclude_subtask=subtask.id)

        user = REVIEW_USER.format(
            task=f"{task.title}\n{task.description}"[:4000],
            subtask=f"{subtask.title}\n{subtask.description}"[:2000],
            label=label,
            confidence=(f"{report.confidence:.2f}" if report.confidence is not None
                        else "не указана"),
            report=report.content[:REPORT_CLIP],
            context=(f"\nРАНЕЕ ПРИНЯТЫЕ РЕЗУЛЬТАТЫ ПРОЕКТА\n{context}" if context else ""),
        )

        self._emit(EventType.AGENT_THINKING, f"проверяю «{subtask.title}»")
        try:
            raw = await self._ask(REVIEW_SYSTEM, user, task.id)
        except ProviderError as exc:
            log.warning("Супервайзер недоступен: %s", exc)
            # Недоступность проверяющего не должна ронять весь прогон:
            # отчёт принимается, но факт пропуска проверки фиксируется.
            self._emit(EventType.ERROR, f"проверка пропущена: {exc}")
            return Verdict(verdict="ok", notes=f"Проверка не выполнена: {exc}")

        verdict = parse_verdict(raw)
        self.repos.reports.mark_reviewed(report.id, verdict.verdict, verdict.notes)

        for issue in verdict.issues:
            incident_id = self.repos.incidents.add(
                self.workspace_id, kind=issue.kind, description=issue.description,
                severity=issue.severity, task_id=task.id, subtask_id=subtask.id,
                report_id=report.id,
            )
            self._emit(EventType.INCIDENT_CREATED,
                       f"{issue.kind}: {issue.description[:120]}",
                       incident_id=incident_id, severity=issue.severity)

        message = {
            "ok": f"принято: «{subtask.title}»",
            "rework": f"на доработку: «{subtask.title}»",
            "conflict": f"конфликт данных: «{subtask.title}»",
        }.get(verdict.verdict, verdict.verdict)
        self._emit(EventType.REPORT_REVIEWED, message,
                   verdict=verdict.verdict, subtask_id=subtask.id)
        return verdict

    def _accepted_context(self, task_id: int, exclude_subtask: int | None = None) -> str:
        """Обезличенная выжимка уже принятых результатов проекта."""
        chunks: list[str] = []
        for st in self.repos.tasks.subtasks(task_id):
            if st.id == exclude_subtask or not st.result:
                continue
            if st.status not in ("done", "review"):
                continue
            chunks.append(f"[{self.anon.label(st.agent_id)}] {st.title}:\n"
                          f"{st.result[:1200]}")
        return "\n\n".join(chunks[-CONTEXT_REPORTS:])

    # -- сводки --------------------------------------------------------------
    async def make_summary(self, task: Task, trigger: str = "manual") -> str:
        """Составляет анонимную сводку и «рассылает» её всем агентам.

        Рассылка означает запись в таблицу ``summaries``: каждый агент
        подхватывает последнюю сводку при следующем запуске, не зная,
        кто из коллег что написал.
        """
        materials = self._summary_materials(task.id)
        if not materials:
            return ""

        self._emit(EventType.AGENT_THINKING, "составляю сводку")
        try:
            raw = await self._ask(
                SUMMARY_SYSTEM,
                SUMMARY_USER.format(task=f"{task.title}\n{task.description}"[:3000],
                                    reports=materials),
                task.id,
                max_tokens=1200,
            )
        except (ProviderError, RuntimeError) as exc:
            self._emit(EventType.ERROR, f"сводка не составлена: {exc}")
            return ""

        # Страховка: вычищаем имена агентов, если модель их всё-таки назвала.
        names = {a.id: a.name for a in self.repos.agents.list(self.workspace_id)}
        content = self.anon.scrub(raw.strip(), names)
        if not content:
            return ""

        recipients = [a.id for a in self.repos.agents.list(self.workspace_id)
                      if a.enabled and not a.is_supervisor]
        summary_id = self.repos.reports.add_summary(
            self.workspace_id, task.id, content, trigger, recipients
        )
        self._emit(EventType.SUMMARY_CREATED,
                   f"сводка разослана ({len(recipients)} получателей, {trigger})",
                   summary_id=summary_id, trigger=trigger)
        return content

    def _summary_materials(self, task_id: int) -> str:
        """Обезличенные материалы для сводки."""
        chunks: list[str] = []
        for st in self.repos.tasks.subtasks(task_id):
            if not st.result:
                continue
            chunks.append(f"[{self.anon.label(st.agent_id)}] {st.title}:\n"
                          f"{st.result[:2500]}")
        return "\n\n".join(chunks[-CONTEXT_REPORTS:])

    def start_timer(self, task: Task) -> None:
        """Запускает периодическую рассылку сводок по таймеру."""
        minutes = int(self.settings.get("summary_interval_minutes", 15) or 0)
        if minutes <= 0 or self._summary_task is not None:
            return

        async def loop() -> None:
            try:
                while not self._stop.is_set():
                    await asyncio.sleep(minutes * 60)
                    if self._stop.is_set():
                        return
                    await self.make_summary(task, trigger="timer")
            except asyncio.CancelledError:
                raise
            except Exception:  # noqa: BLE001
                log.exception("Сбой периодической сводки")

        self._summary_task = asyncio.ensure_future(loop())
        self._emit(EventType.LOG, f"сводки по таймеру: раз в {minutes} мин")

    # -- конфликты -----------------------------------------------------------
    async def find_conflicts(self, task: Task) -> list[Conflict]:
        """Ищет прямые противоречия между результатами подзадач.

        Противоречие требует как минимум двух результатов, поэтому при одном
        готовом результате вызов модели пропускается — это экономит токены,
        а не срезает проверку.
        """
        with_results = [s for s in self.repos.tasks.subtasks(task.id) if s.result.strip()]
        if len(with_results) < 2:
            return []
        materials = self._summary_materials(task.id)
        if not materials:
            return []

        try:
            raw = await self._ask(
                CONFLICT_SYSTEM,
                SUMMARY_USER.format(task=f"{task.title}\n{task.description}"[:3000],
                                    reports=materials),
                task.id,
                max_tokens=1200,
            )
        except (ProviderError, RuntimeError) as exc:
            self._emit(EventType.ERROR, f"поиск конфликтов пропущен: {exc}")
            return []

        conflicts = parse_conflicts(raw)
        for conflict in conflicts:
            resolved = conflict.auto_resolvable and bool(conflict.resolution)
            incident_id = self.repos.incidents.add(
                self.workspace_id, kind="conflict", description=conflict.description,
                severity=conflict.severity, task_id=task.id,
            )
            if resolved:
                self.repos.incidents.resolve(incident_id, "auto_resolved",
                                             conflict.resolution)
                self._emit(EventType.INCIDENT_CREATED,
                           f"конфликт разрешён автоматически: {conflict.description[:100]}",
                           incident_id=incident_id, resolved=True)
            else:
                self.repos.incidents.resolve(incident_id, "escalated",
                                             "Требуется решение пользователя")
                self._emit(EventType.INCIDENT_CREATED,
                           f"конфликт эскалирован: {conflict.description[:100]}",
                           incident_id=incident_id, resolved=False,
                           severity=conflict.severity)
        if conflicts:
            self._emit(EventType.LOG, f"найдено расхождений: {len(conflicts)}")
        return conflicts
````

### `core/hitl.py`

*212 строк*

````python
"""Этап 7 — human-in-the-loop: реальная пауза в критических точках.

Ядро не спрашивает пользователя напрямую — оно публикует запрос в шину и
останавливается на ``asyncio.Future``. Интерфейс показывает вопрос, человек
нажимает кнопку, и ядро продолжает с его решением. Запрос и ответ пишутся
в таблицу ``approvals``, поэтому история решений сохраняется.

Важно: остановка прогона должна разблокировать все ожидания, иначе кнопка
«Стоп» не сработает, пока висит вопрос. За это отвечает ``cancel_all``.
"""

from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field
from enum import Enum

from core.events import Event, EventBus, EventType
from storage.db import utcnow
from storage.repositories import Repos

log = logging.getLogger("aiorc.hitl")


class Decision(str, Enum):
    """Что решил пользователь."""

    APPROVE = "approve"    # принять как есть и идти дальше
    REWORK = "rework"      # вернуть исполнителю с комментарием
    SKIP = "skip"          # пометить подзадачу как неудачную и продолжить
    ABORT = "abort"        # остановить весь прогон


class Reason(str, Enum):
    """Почему система остановилась."""

    CONFLICT = "conflict"              # супервайзер нашёл противоречие
    NOT_ACCEPTED = "not_accepted"      # доработки исчерпаны, результат не принят
    LOW_CONFIDENCE = "low_confidence"  # агент сам не уверен в результате
    MILESTONE = "milestone"            # завершён этап работ


REASON_TITLES = {
    Reason.CONFLICT: "Конфликт данных",
    Reason.NOT_ACCEPTED: "Результат не принят супервайзером",
    Reason.LOW_CONFIDENCE: "Низкая уверенность исполнителя",
    Reason.MILESTONE: "Завершён этап работ",
}

#: какие кнопки показывать для каждой причины
REASON_OPTIONS: dict[Reason, list[Decision]] = {
    Reason.CONFLICT: [Decision.APPROVE, Decision.REWORK, Decision.SKIP, Decision.ABORT],
    Reason.NOT_ACCEPTED: [Decision.APPROVE, Decision.REWORK, Decision.SKIP, Decision.ABORT],
    Reason.LOW_CONFIDENCE: [Decision.APPROVE, Decision.REWORK, Decision.ABORT],
    Reason.MILESTONE: [Decision.APPROVE, Decision.ABORT],
}

DECISION_TITLES = {
    Decision.APPROVE: "Принять",
    Decision.REWORK: "На доработку",
    Decision.SKIP: "Пропустить",
    Decision.ABORT: "Остановить прогон",
}


@dataclass
class ApprovalRequest:
    """Открытый вопрос к пользователю."""

    id: int
    workspace_id: int
    task_id: int | None
    subtask_id: int | None
    reason: Reason
    question: str
    details: str = ""
    agent_name: str = ""
    options: list[Decision] = field(default_factory=list)
    created_at: str = ""


@dataclass
class Answer:
    """Ответ пользователя."""

    decision: Decision
    comment: str = ""

    @property
    def is_abort(self) -> bool:
        return self.decision is Decision.ABORT


class ApprovalGate:
    """Останавливает работу и ждёт решения человека."""

    def __init__(self, repos: Repos, bus: EventBus, workspace_id: int) -> None:
        self.repos = repos
        self.bus = bus
        self.workspace_id = workspace_id
        self._waiters: dict[int, asyncio.Future] = {}
        self._open: dict[int, ApprovalRequest] = {}
        self._aborted = False

    # -- запрос --------------------------------------------------------------
    async def ask(self, reason: Reason, question: str, *, details: str = "",
                  task_id: int | None = None, subtask_id: int | None = None,
                  agent_name: str = "", options: list[Decision] | None = None,
                  default: Decision = Decision.APPROVE) -> Answer:
        """Публикует вопрос и ждёт ответа.

        Если прогон уже остановлен, вопрос не задаётся — возвращается
        ``ABORT``, чтобы вызывающий код свернул работу.
        """
        if self._aborted:
            return Answer(Decision.ABORT)

        choices = options or REASON_OPTIONS.get(reason, [Decision.APPROVE, Decision.ABORT])
        payload = {
            "subtask_id": subtask_id,
            "question": question,
            "details": details,
            "agent_name": agent_name,
            "options": [c.value for c in choices],
        }
        approval_id = self.repos.approvals.create(
            self.workspace_id, task_id, reason.value, payload
        )
        request = ApprovalRequest(
            id=approval_id, workspace_id=self.workspace_id, task_id=task_id,
            subtask_id=subtask_id, reason=reason, question=question, details=details,
            agent_name=agent_name, options=choices, created_at=utcnow(),
        )
        self._open[approval_id] = request

        loop = asyncio.get_running_loop()
        future: asyncio.Future = loop.create_future()
        self._waiters[approval_id] = future

        self.bus.emit(Event(
            EventType.APPROVAL_REQUESTED, workspace_id=self.workspace_id,
            task_id=task_id, subtask_id=subtask_id, agent_name=agent_name or "Система",
            message=f"нужно решение: {question}",
            payload={"approval_id": approval_id, "reason": reason.value,
                     "details": details,
                     "options": [c.value for c in choices]},
        ))

        try:
            answer: Answer = await future
        except asyncio.CancelledError:
            self.repos.approvals.decide(approval_id, "cancelled",
                                        "Прогон остановлен до получения решения")
            self._open.pop(approval_id, None)
            raise
        finally:
            self._waiters.pop(approval_id, None)

        self._open.pop(approval_id, None)
        self.repos.approvals.decide(approval_id, answer.decision.value, answer.comment)
        self.bus.emit(Event(
            EventType.APPROVAL_RESOLVED, workspace_id=self.workspace_id,
            task_id=task_id, subtask_id=subtask_id, agent_name="Пользователь",
            message=f"решение: {DECISION_TITLES.get(answer.decision, answer.decision.value)}"
                    + (f" — {answer.comment[:120]}" if answer.comment else ""),
            payload={"approval_id": approval_id, "decision": answer.decision.value},
        ))
        if answer.is_abort:
            self._aborted = True
        return answer

    # -- ответ ---------------------------------------------------------------
    def resolve(self, approval_id: int, decision: Decision | str,
                comment: str = "") -> bool:
        """Отдаёт решение ожидающему коду. Вызывается из интерфейса."""
        future = self._waiters.get(approval_id)
        if future is None or future.done():
            return False
        if isinstance(decision, str):
            try:
                decision = Decision(decision)
            except ValueError:
                decision = Decision.APPROVE
        future.set_result(Answer(decision, comment.strip()))
        return True

    def cancel_all(self) -> None:
        """Снимает все ожидания — нужно при остановке прогона."""
        self._aborted = True
        for approval_id, future in list(self._waiters.items()):
            if not future.done():
                future.set_result(Answer(Decision.ABORT, "Прогон остановлен"))
            self._waiters.pop(approval_id, None)
        self._open.clear()

    def pending(self) -> list[ApprovalRequest]:
        """Список открытых вопросов — интерфейс рисует их карточками."""
        return sorted(self._open.values(), key=lambda r: r.id)

    def has_pending(self) -> bool:
        return bool(self._open)


def parse_payload(raw: str) -> dict:
    """Безопасный разбор ``payload_json`` из таблицы approvals."""
    try:
        data = json.loads(raw or "{}")
        return data if isinstance(data, dict) else {}
    except ValueError:
        return {}
````

### `core/budget.py`

*251 строк*

````python
"""Этап 9 — бюджеты, лимиты и алерты.

Лимит можно поставить на трёх уровнях: весь воркспейс, текущая задача и
отдельный агент. Каждый уровень ограничивается и по токенам, и по деньгам.

Две важные детали реализации:

* Проверка идёт **перед** вызовом модели, а не после. Иначе лимит узнавался бы
  постфактум — деньги уже потрачены, а сказать об этом нечем.
* Фактический расход берётся из ``usage_log``, а не из накопительных счётчиков
  в таблице ``budgets``. Журнал вызовов — единственный источник правды, и при
  перезапуске приложения лимит не «обнуляется» сам собой.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from core.events import Event, EventBus, EventType
from storage.repositories import Repos

log = logging.getLogger("aiorc.budget")

SCOPE_TITLES = {
    "workspace": "воркспейс",
    "task": "задача",
    "agent": "агент",
}


def money(value: float) -> str:
    """Сумма с точностью, достаточной чтобы не превратиться в «$0.00».

    Лимиты на дешёвых моделях легко оказываются меньше цента, и округление
    до двух знаков сделало бы сообщение бессмысленным.
    """
    if value >= 1:
        return f"${value:,.2f}".replace(",", " ")
    if value >= 0.01:
        return f"${value:.3f}"
    return f"${value:.5f}"


@dataclass
class Limit:
    """Ограничение одного уровня. ``None`` означает «без лимита»."""

    token_limit: int | None = None
    cost_limit: float | None = None
    alert_threshold: float = 0.8

    @property
    def is_set(self) -> bool:
        return bool(self.token_limit) or bool(self.cost_limit)


@dataclass
class ScopeState:
    """Текущее состояние одного уровня бюджета."""

    scope: str
    scope_id: int
    name: str
    limit: Limit = field(default_factory=Limit)
    tokens: int = 0
    cost: float = 0.0
    alerted: bool = False

    def ratio(self) -> float:
        """Доля израсходованного — максимум из токенов и денег."""
        parts: list[float] = []
        if self.limit.token_limit:
            parts.append(self.tokens / self.limit.token_limit)
        if self.limit.cost_limit:
            parts.append(self.cost / self.limit.cost_limit)
        return max(parts) if parts else 0.0

    def exceeded(self) -> bool:
        if self.limit.token_limit and self.tokens >= self.limit.token_limit:
            return True
        return bool(self.limit.cost_limit and self.cost >= self.limit.cost_limit)

    def reason(self) -> str:
        """Человеческое объяснение, какой именно лимит упёрся."""
        if self.limit.token_limit and self.tokens >= self.limit.token_limit:
            return (f"{SCOPE_TITLES.get(self.scope, self.scope)} «{self.name}»: "
                    f"израсходовано {self.tokens} токенов из {self.limit.token_limit}")
        if self.limit.cost_limit and self.cost >= self.limit.cost_limit:
            return (f"{SCOPE_TITLES.get(self.scope, self.scope)} «{self.name}»: "
                    f"израсходовано {money(self.cost)} из {money(self.limit.cost_limit)}")
        return ""


class BudgetGuard:
    """Следит за лимитами всех уровней во время прогона.

    Совместим по интерфейсу со старым ``TokenBudget``: ``add`` и ``exhausted``
    вызываются из ``AgentRunner`` так же, как раньше.
    """

    def __init__(self, repos: Repos, bus: EventBus, workspace_id: int,
                 task_id: int | None = None,
                 task_token_limit: int | None = None) -> None:
        self.repos = repos
        self.bus = bus
        self.workspace_id = workspace_id
        self.task_id = task_id
        self._scopes: dict[tuple[str, int], ScopeState] = {}
        self._load(task_token_limit)

    # -- загрузка ------------------------------------------------------------
    def _load(self, task_token_limit: int | None) -> None:
        workspace = self.repos.workspaces.get(self.workspace_id)
        tokens, cost = self.repos.budgets.workspace_totals(self.workspace_id)
        self._scopes[("workspace", self.workspace_id)] = ScopeState(
            "workspace", self.workspace_id,
            workspace.name if workspace else "проект",
            self._limit_of("workspace", self.workspace_id), tokens, cost,
        )

        if self.task_id:
            task = self.repos.tasks.get(self.task_id)
            used_tokens, used_cost = self.repos.budgets.task_totals(self.task_id)
            limit = self._limit_of("task", self.task_id)
            # Лимит, заданный прямо в форме задачи, не должен теряться:
            # если отдельной записи в budgets нет, берём его оттуда.
            if limit.token_limit is None and task_token_limit:
                limit.token_limit = task_token_limit
            self._scopes[("task", self.task_id)] = ScopeState(
                "task", self.task_id, task.title if task else "задача",
                limit, used_tokens, used_cost,
            )

        agents = self.repos.agents.list(self.workspace_id)
        limits = self.repos.budgets.list_limits("agent", [a.id for a in agents])
        totals = self.repos.budgets.agent_totals(self.workspace_id)
        for agent in agents:
            row = limits.get(agent.id)
            used = totals.get(agent.id, (0, 0.0))
            self._scopes[("agent", agent.id)] = ScopeState(
                "agent", agent.id, agent.name,
                Limit(row.token_limit, row.cost_limit_usd, row.alert_threshold)
                if row else Limit(),
                used[0], used[1],
            )

    def _limit_of(self, scope: str, scope_id: int) -> Limit:
        row = self.repos.budgets.get(scope, scope_id)
        if row is None:
            return Limit()
        return Limit(row.token_limit, row.cost_limit_usd, row.alert_threshold)

    # -- проверка ------------------------------------------------------------
    def blocking_scope(self, agent_id: int | None = None) -> ScopeState | None:
        """Возвращает уровень, лимит которого исчерпан, или ``None``.

        Проверка идёт от общего к частному: сначала воркспейс, потом задача,
        потом конкретный агент — так сообщение получается по самой
        «дорогой» причине.
        """
        for key in (("workspace", self.workspace_id),
                    ("task", self.task_id) if self.task_id else None,
                    ("agent", agent_id) if agent_id else None):
            if key is None:
                continue
            state = self._scopes.get(key)  # type: ignore[arg-type]
            if state is not None and state.exceeded():
                return state
        return None

    def exhausted(self, agent_id: int | None = None) -> bool:
        """Совместимость со старым интерфейсом ``TokenBudget``."""
        return self.blocking_scope(agent_id) is not None

    # -- учёт ----------------------------------------------------------------
    def add(self, tokens: int, cost: float, agent_id: int | None = None) -> None:
        """Записывает расход и при необходимости поднимает алерты."""
        keys = [("workspace", self.workspace_id)]
        if self.task_id:
            keys.append(("task", self.task_id))
        if agent_id:
            keys.append(("agent", agent_id))

        for key in keys:
            state = self._scopes.get(key)
            if state is None:
                continue
            state.tokens += tokens
            state.cost += cost
            if state.limit.is_set:
                self.repos.budgets.sync_used(state.scope, state.scope_id,
                                             state.tokens, state.cost)
                self._maybe_alert(state)

    def _maybe_alert(self, state: ScopeState) -> None:
        """Алерт срабатывает один раз на уровень — иначе он превратится в шум."""
        if state.exceeded():
            if not state.alerted:
                state.alerted = True
            self.bus.emit(Event(
                EventType.BUDGET_EXCEEDED, workspace_id=self.workspace_id,
                task_id=self.task_id,
                message=f"лимит исчерпан — {state.reason()}",
                payload={"scope": state.scope, "scope_id": state.scope_id,
                         "ratio": state.ratio()},
            ))
            return

        if not state.alerted and state.ratio() >= state.limit.alert_threshold:
            state.alerted = True
            percent = state.ratio() * 100
            self.bus.emit(Event(
                EventType.BUDGET_ALERT, workspace_id=self.workspace_id,
                task_id=self.task_id,
                message=(f"бюджет на {percent:.0f}% — "
                         f"{SCOPE_TITLES.get(state.scope, state.scope)} "
                         f"«{state.name}»"),
                payload={"scope": state.scope, "scope_id": state.scope_id,
                         "ratio": state.ratio()},
            ))

    # -- отчётность ----------------------------------------------------------
    def snapshot(self) -> list[ScopeState]:
        """Состояние всех уровней — для дашборда и страницы бюджетов."""
        order = {"workspace": 0, "task": 1, "agent": 2}
        return sorted(self._scopes.values(),
                      key=lambda s: (order.get(s.scope, 3), s.name))

    @property
    def tokens(self) -> int:
        state = self._scopes.get(("task", self.task_id)) if self.task_id else None
        if state is None:
            state = self._scopes[("workspace", self.workspace_id)]
        return state.tokens

    @property
    def cost(self) -> float:
        state = self._scopes.get(("task", self.task_id)) if self.task_id else None
        if state is None:
            state = self._scopes[("workspace", self.workspace_id)]
        return state.cost


def load_states(repos: Repos, workspace_id: int) -> list[ScopeState]:
    """Состояние бюджетов вне прогона — для страницы настройки лимитов."""
    task = repos.tasks.current(workspace_id)
    guard = BudgetGuard(repos, EventBus(), workspace_id,
                        task.id if task else None,
                        task.token_limit if task else None)
    return guard.snapshot()
````


## Экспорт результата

### `core/export/bundle.py`

*373 строк*

````python
"""Этап 8 — сборка результата проекта.

Формат результата зависит от задачи, поэтому экспорт устроен в два слоя:

1. Из базы и рабочего каталога собирается ``ResultBundle`` — всё, что
   наработал проект.
2. Из него строится **единая модель документа** (список блоков), и уже её
   рендерят четыре формата. Благодаря этому Markdown, DOCX и PDF получаются
   одинаковыми по содержанию: правится один сборщик, а не три экспортёра.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from app.config import PATHS
from core.hitl import parse_payload
from storage.models import Incident, Report, Subtask, Summary, Task, Workspace
from storage.repositories import Repos

log = logging.getLogger("aiorc.export")

#: расширения, по которым распознаём «проект с кодом»
CODE_SUFFIXES = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".kt", ".go", ".rs", ".rb",
    ".php", ".cs", ".cpp", ".c", ".h", ".hpp", ".swift", ".scala", ".sh",
    ".sql", ".html", ".css", ".scss", ".vue", ".yml", ".yaml", ".toml",
}
#: служебные каталоги, которые не попадают в экспорт
SKIP_DIRS = {".sandbox", "__pycache__", ".git", "node_modules", ".venv"}

FORMAT_TITLES = {
    "markdown": "Markdown (.md)",
    "docx": "Документ Word (.docx)",
    "pdf": "Документ PDF (.pdf)",
    "zip": "ZIP-архив с файлами",
}


# ---------------------------------------------------------------------------
# Модель документа
# ---------------------------------------------------------------------------


@dataclass
class Block:
    """Единица содержания. ``kind`` определяет, как её рисовать."""

    kind: str                     # heading | text | code | bullets | divider | meta
    text: str = ""
    level: int = 1                # для heading
    items: list[str] = field(default_factory=list)   # для bullets
    language: str = ""            # для code


def heading(text: str, level: int = 1) -> Block:
    return Block("heading", text=text, level=level)


def text(body: str) -> Block:
    return Block("text", text=body)


def bullets(items: list[str]) -> Block:
    return Block("bullets", items=[i for i in items if i])


def code(body: str, language: str = "") -> Block:
    return Block("code", text=body, language=language)


def divider() -> Block:
    return Block("divider")


# ---------------------------------------------------------------------------
# Сбор данных
# ---------------------------------------------------------------------------


@dataclass
class ExportOptions:
    """Что включать в выгрузку. Значения по умолчанию — «полезное без шума»."""

    include_results: bool = True       # результаты подзадач (суть работы)
    include_reports: bool = False      # полные отчёты агентов
    include_summaries: bool = False    # сводки супервайзера
    include_incidents: bool = True     # что пошло не так и чем кончилось
    include_decisions: bool = False    # решения human-in-the-loop
    include_files: bool = True         # файлы из рабочего каталога (для ZIP)
    include_stats: bool = True         # расход токенов и стоимость
    anonymize: bool = False            # скрыть имена агентов в документе


@dataclass
class ResultBundle:
    """Всё, что наработал проект."""

    workspace: Workspace
    task: Task | None
    subtasks: list[Subtask] = field(default_factory=list)
    reports: list[Report] = field(default_factory=list)
    summaries: list[Summary] = field(default_factory=list)
    incidents: list[Incident] = field(default_factory=list)
    decisions: list[dict] = field(default_factory=list)
    agent_names: dict[int, str] = field(default_factory=dict)
    files: list[Path] = field(default_factory=list)
    tokens: int = 0
    cost: float = 0.0

    @property
    def workspace_dir(self) -> Path:
        return PATHS.workspace_dir(self.workspace.id)

    def agent_name(self, agent_id: int | None, anonymize: bool = False) -> str:
        if agent_id is None:
            return "Супервайзер"
        if anonymize:
            ordered = sorted(self.agent_names)
            index = ordered.index(agent_id) if agent_id in ordered else 0
            return f"Исполнитель {chr(ord('A') + index)}"
        return self.agent_names.get(agent_id, "Агент удалён")

    def has_code(self) -> bool:
        return any(f.suffix.lower() in CODE_SUFFIXES for f in self.files)


def collect(repos: Repos, workspace_id: int) -> ResultBundle:
    """Собирает результат проекта из БД и рабочего каталога."""
    workspace = repos.workspaces.get(workspace_id)
    if workspace is None:
        raise ValueError("Воркспейс не найден")

    task = repos.tasks.current(workspace_id)
    subtasks = repos.tasks.subtasks(task.id) if task else []
    tokens, cost = repos.budgets.workspace_totals(workspace_id)

    bundle = ResultBundle(
        workspace=workspace,
        task=task,
        subtasks=subtasks,
        reports=repos.reports.list_reports(workspace_id, limit=500),
        summaries=repos.reports.list_summaries(workspace_id, limit=100),
        incidents=repos.incidents.list(workspace_id, limit=500),
        decisions=repos.approvals.history(workspace_id, limit=200),
        agent_names={a.id: a.name for a in repos.agents.list(workspace_id)},
        files=scan_files(PATHS.workspace_dir(workspace_id)),
        tokens=tokens,
        cost=cost,
    )
    return bundle


def scan_files(root: Path, limit: int = 2000) -> list[Path]:
    """Файлы рабочего каталога без служебных каталогов и скрытых файлов."""
    if not root.exists():
        return []
    found: list[Path] = []
    for path in sorted(root.rglob("*")):
        if len(found) >= limit:
            break
        if path.is_dir():
            continue
        if any(part in SKIP_DIRS or part.startswith(".") for part in path.relative_to(root).parts):
            continue
        found.append(path)
    return found


# ---------------------------------------------------------------------------
# Автоопределение формата
# ---------------------------------------------------------------------------

#: слова, по которым задача похожа на «сделать документ»
DOC_HINTS = ("документ", "отчёт", "отчет", "статья", "текст", "инструкция",
             "руководство", "план", "анализ", "обзор", "презентация",
             "report", "document", "article", "guide", "analysis")
#: слова, по которым задача похожа на «написать код»
CODE_HINTS = ("код", "программ", "скрипт", "приложение", "сервис", "api",
              "библиотек", "рефактор", "баг", "тест", "code", "script",
              "app", "service", "library", "refactor")


def detect_format(bundle: ResultBundle) -> tuple[str, str]:
    """Возвращает ``(формат, объяснение)``.

    Объяснение показывается пользователю, чтобы автоопределение не выглядело
    магией и его можно было осознанно переопределить.
    """
    if bundle.task and bundle.task.result_format not in ("", "auto"):
        chosen = bundle.task.result_format
        return chosen, "Формат задан вручную при постановке задачи."

    if bundle.has_code():
        count = sum(1 for f in bundle.files if f.suffix.lower() in CODE_SUFFIXES)
        return "zip", (f"В рабочем каталоге найдено файлов с кодом: {count}. "
                       f"Архив сохранит структуру каталогов.")

    if len(bundle.files) > 3:
        return "zip", (f"В рабочем каталоге {len(bundle.files)} файлов — "
                       f"архив удобнее одного документа.")

    haystack = " ".join(filter(None, [
        bundle.task.title if bundle.task else "",
        bundle.task.description if bundle.task else "",
    ])).lower()

    if any(word in haystack for word in CODE_HINTS):
        return "zip", "Формулировка задачи говорит о коде — собираем архив."
    if any(word in haystack for word in DOC_HINTS):
        return "docx", "Формулировка задачи говорит о документе."

    total = sum(len(s.result) for s in bundle.subtasks)
    if total > 20_000:
        return "docx", "Результат объёмный — документ Word удобнее читать."
    return "markdown", "Результат текстовый и компактный — подойдёт Markdown."


# ---------------------------------------------------------------------------
# Построение документа
# ---------------------------------------------------------------------------


def build_document(bundle: ResultBundle, options: ExportOptions) -> list[Block]:
    """Собирает единую модель документа, общую для всех форматов."""
    blocks: list[Block] = []
    task = bundle.task

    blocks.append(heading(task.title if task and task.title else bundle.workspace.name, 1))
    blocks.append(Block("meta", text=(
        f"Проект: {bundle.workspace.name}   ·   "
        f"Сформировано: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    )))

    if task and task.description:
        blocks.append(heading("Задача", 2))
        blocks.append(text(task.description))

    if options.include_results and bundle.subtasks:
        blocks.append(heading("Результат", 2))
        done = [s for s in bundle.subtasks if s.result.strip()]
        if not done:
            blocks.append(text("Готовых результатов пока нет: ни одна подзадача "
                               "не завершилась успешно."))
        for index, subtask in enumerate(done, 1):
            blocks.append(heading(f"{index}. {subtask.title}", 3))
            author = bundle.agent_name(subtask.agent_id, options.anonymize)
            status = _status_title(subtask.status)
            blocks.append(Block("meta", text=f"{author}   ·   {status}"))
            if subtask.description:
                blocks.append(Block("meta", text=subtask.description))
            blocks.extend(_body_blocks(subtask.result))

    if options.include_summaries and bundle.summaries:
        blocks.append(divider())
        blocks.append(heading("Сводки супервайзера", 2))
        for summary in reversed(bundle.summaries):
            blocks.append(Block("meta", text=_when(summary.created_at)))
            blocks.extend(_body_blocks(summary.content))

    if options.include_reports and bundle.reports:
        blocks.append(divider())
        blocks.append(heading("Отчёты исполнителей", 2))
        for report in reversed(bundle.reports):
            author = bundle.agent_name(report.agent_id, options.anonymize)
            confidence = (f"   ·   уверенность {report.confidence:.2f}"
                          if report.confidence is not None else "")
            blocks.append(heading(f"{author}{confidence}", 3))
            blocks.append(Block("meta", text=_when(report.created_at)))
            blocks.extend(_body_blocks(report.content))

    if options.include_incidents and bundle.incidents:
        blocks.append(divider())
        blocks.append(heading("Инциденты", 2))
        blocks.append(text(
            "Что супервайзер счёл проблемой и чем это закончилось."
        ))
        blocks.append(bullets([
            f"[{i.severity}] {i.kind}: {i.description}"
            + (f" → {i.resolution}" if i.resolution else "")
            for i in reversed(bundle.incidents)
        ]))

    if options.include_decisions and bundle.decisions:
        blocks.append(divider())
        blocks.append(heading("Решения пользователя", 2))
        rows: list[str] = []
        for row in reversed(bundle.decisions):
            payload = parse_payload(row.get("payload_json", "{}"))
            decision = row.get("decision") or "ожидает решения"
            comment = f" — {row['comment']}" if row.get("comment") else ""
            rows.append(f"{payload.get('question', '')} → {decision}{comment}")
        blocks.append(bullets(rows))

    if options.include_stats:
        blocks.append(divider())
        blocks.append(heading("Статистика прогона", 2))
        done = sum(1 for s in bundle.subtasks if s.status == "done")
        reworks = sum(s.rework_count for s in bundle.subtasks)
        blocks.append(bullets([
            f"Подзадач выполнено: {done} из {len(bundle.subtasks)}",
            f"Доработок: {reworks}",
            f"Израсходовано токенов: {bundle.tokens:,}".replace(",", " "),
            f"Примерная стоимость: ${bundle.cost:.4f}",
            f"Агентов в проекте: {len(bundle.agent_names)}",
        ]))

    if bundle.files and options.include_files:
        blocks.append(heading("Файлы проекта", 2))
        blocks.append(bullets([
            f"{f.relative_to(bundle.workspace_dir)}  ({_human_size(f)})"
            for f in bundle.files[:200]
        ]))

    return blocks


def _body_blocks(raw: str) -> list[Block]:
    """Разбивает текст результата на абзацы и блоки кода.

    Полноценный парсер Markdown здесь не нужен: единственное, что важно
    не испортить, — ограждённые блоки кода.
    """
    blocks: list[Block] = []
    buffer: list[str] = []
    in_code = False
    language = ""

    for line in (raw or "").splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                blocks.append(code("\n".join(buffer), language))
                buffer, in_code, language = [], False, ""
            else:
                if buffer:
                    blocks.append(text("\n".join(buffer).strip()))
                    buffer = []
                in_code = True
                language = stripped[3:].strip()
            continue
        buffer.append(line)

    if buffer:
        tail = "\n".join(buffer).strip()
        if tail:
            blocks.append(code(tail, language) if in_code else text(tail))
    return blocks


def _status_title(status: str) -> str:
    return {"done": "принято", "review": "на проверке", "rework": "на доработке",
            "error": "с ошибкой", "paused": "на паузе",
            "running": "выполняется"}.get(status, status)


def _when(raw: str) -> str:
    return (raw or "")[:19].replace("T", " ")


def _human_size(path: Path) -> str:
    try:
        size = float(path.stat().st_size)
    except OSError:
        return "?"
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024
    return f"{size:.1f} ТБ"
````

### `core/export/exporters.py`

*386 строк*

````python
"""Рендеринг результата в конкретные форматы (этап 8).

Все экспортёры получают одну и ту же модель блоков из ``bundle.py``,
поэтому содержание Markdown, DOCX и PDF совпадает по построению.

Отдельная история — кириллица в PDF: встроенные шрифты reportlab её не
знают, поэтому приходится искать в системе TrueType-шрифт. Если не нашли,
экспорт не молчит и не выдаёт кракозябры, а честно говорит об этом.
"""

from __future__ import annotations

import json
import logging
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path

from core.export.bundle import Block, ExportOptions, ResultBundle, build_document

log = logging.getLogger("aiorc.export")


class ExportError(RuntimeError):
    """Ошибка экспорта с текстом, который можно показать пользователю."""


@dataclass
class ExportResult:
    path: Path
    format: str
    size: int
    note: str = ""


# ---------------------------------------------------------------------------
# Markdown
# ---------------------------------------------------------------------------


def render_markdown(blocks: list[Block]) -> str:
    """Собирает Markdown-текст из блоков."""
    out: list[str] = []
    for block in blocks:
        if block.kind == "heading":
            out.append(f"{'#' * min(block.level, 6)} {block.text}")
        elif block.kind == "meta":
            out.append(f"*{block.text}*")
        elif block.kind == "text":
            out.append(block.text)
        elif block.kind == "code":
            out.append(f"```{block.language}\n{block.text}\n```")
        elif block.kind == "bullets":
            out.extend(f"- {item}" for item in block.items)
        elif block.kind == "divider":
            out.append("---")
        out.append("")
    return "\n".join(out).strip() + "\n"


def export_markdown(bundle: ResultBundle, options: ExportOptions,
                    path: Path) -> ExportResult:
    blocks = build_document(bundle, options)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_markdown(blocks), "utf-8")
    return ExportResult(path, "markdown", path.stat().st_size)


# ---------------------------------------------------------------------------
# DOCX
# ---------------------------------------------------------------------------


def export_docx(bundle: ResultBundle, options: ExportOptions,
                path: Path) -> ExportResult:
    try:
        from docx import Document
        from docx.enum.style import WD_STYLE_TYPE
        from docx.shared import Pt, RGBColor
    except ImportError as exc:
        raise ExportError(
            "Для экспорта в DOCX нужен пакет python-docx:\n"
            "pip install python-docx"
        ) from exc

    blocks = build_document(bundle, options)
    document = Document()

    # Моноширинный стиль для кода — в стандартном шаблоне его нет.
    styles = document.styles
    try:
        code_style = styles.add_style("AiorcCode", WD_STYLE_TYPE.PARAGRAPH)
        code_style.font.name = "Consolas"
        code_style.font.size = Pt(9)
    except Exception:  # noqa: BLE001 — стиль уже есть
        code_style = styles["AiorcCode"]

    for block in blocks:
        if block.kind == "heading":
            document.add_heading(block.text, level=min(block.level, 4))
        elif block.kind == "meta":
            paragraph = document.add_paragraph(block.text)
            run = paragraph.runs[0] if paragraph.runs else paragraph.add_run("")
            run.italic = True
            run.font.size = Pt(9)
            run.font.color.rgb = RGBColor(0x66, 0x6D, 0x7A)
        elif block.kind == "text":
            for chunk in block.text.split("\n\n"):
                if chunk.strip():
                    document.add_paragraph(chunk.strip())
        elif block.kind == "code":
            paragraph = document.add_paragraph(block.text, style=code_style)
            paragraph.paragraph_format.left_indent = Pt(12)
        elif block.kind == "bullets":
            for item in block.items:
                document.add_paragraph(item, style="List Bullet")
        elif block.kind == "divider":
            document.add_paragraph("―" * 40)

    path.parent.mkdir(parents=True, exist_ok=True)
    document.save(str(path))
    return ExportResult(path, "docx", path.stat().st_size)


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

#: где искать TrueType-шрифт с кириллицей
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/TTF/DejaVuSans.ttf",
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/segoeui.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
]
MONO_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "C:/Windows/Fonts/consola.ttf",
    "/System/Library/Fonts/Menlo.ttc",
]


def find_font(candidates: list[str]) -> Path | None:
    """Ищет шрифт в системе, а если не нашёл — в пакете matplotlib.

    matplotlib кладёт рядом с собой DejaVu, и это частый способ получить
    кириллический шрифт на машине, где системных TTF нет.
    """
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return path
    try:
        import matplotlib

        fonts_dir = Path(matplotlib.__file__).parent / "mpl-data" / "fonts" / "ttf"
        mono = "Mono" in " ".join(candidates)
        pattern = "DejaVuSansMono.ttf" if mono else "DejaVuSans.ttf"
        found = fonts_dir / pattern
        if found.exists():
            return found
    except Exception:  # noqa: BLE001
        pass
    return None


def export_pdf(bundle: ResultBundle, options: ExportOptions,
               path: Path) -> ExportResult:
    try:
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.ttfonts import TTFont
        from reportlab.platypus import (
            HRFlowable,
            ListFlowable,
            ListItem,
            Paragraph,
            SimpleDocTemplate,
            Spacer,
        )
    except ImportError as exc:
        raise ExportError(
            "Для экспорта в PDF нужен пакет reportlab:\n"
            "pip install reportlab"
        ) from exc

    regular = find_font(FONT_CANDIDATES)
    if regular is None:
        raise ExportError(
            "Не найден шрифт с поддержкой кириллицы, а встроенные шрифты PDF "
            "её не знают — текст получился бы нечитаемым.\n\n"
            "Установите шрифты DejaVu (Linux: пакет fonts-dejavu) либо "
            "выберите экспорт в DOCX или Markdown."
        )
    mono = find_font(MONO_CANDIDATES) or regular

    pdfmetrics.registerFont(TTFont("AiorcSans", str(regular)))
    pdfmetrics.registerFont(TTFont("AiorcMono", str(mono)))

    sheet = getSampleStyleSheet()
    body = ParagraphStyle("AiorcBody", parent=sheet["BodyText"],
                          fontName="AiorcSans", fontSize=10, leading=14,
                          alignment=TA_LEFT, spaceAfter=6)
    meta = ParagraphStyle("AiorcMeta", parent=body, fontSize=8,
                          textColor="#6a7080", spaceAfter=4)
    code_style = ParagraphStyle("AiorcCode", parent=body, fontName="AiorcMono",
                                fontSize=8, leading=11, leftIndent=8,
                                backColor="#f2f3f6", borderPadding=4)
    headings = {
        level: ParagraphStyle(
            f"AiorcH{level}", parent=body, fontName="AiorcSans",
            fontSize={1: 18, 2: 14, 3: 12, 4: 11}.get(level, 11),
            leading={1: 22, 2: 18, 3: 15, 4: 14}.get(level, 14),
            spaceBefore={1: 0, 2: 12, 3: 10, 4: 8}.get(level, 8), spaceAfter=6,
        )
        for level in (1, 2, 3, 4)
    }

    story: list = []
    for block in build_document(bundle, options):
        if block.kind == "heading":
            story.append(Paragraph(_escape(block.text),
                                   headings.get(min(block.level, 4), body)))
        elif block.kind == "meta":
            story.append(Paragraph(_escape(block.text), meta))
        elif block.kind == "text":
            for chunk in block.text.split("\n\n"):
                if chunk.strip():
                    story.append(Paragraph(_escape(chunk.strip()).replace("\n", "<br/>"),
                                           body))
        elif block.kind == "code":
            story.append(Paragraph(
                _escape(block.text).replace("\n", "<br/>").replace(" ", "&nbsp;"),
                code_style,
            ))
            story.append(Spacer(1, 6))
        elif block.kind == "bullets" and block.items:
            story.append(ListFlowable(
                [ListItem(Paragraph(_escape(item), body)) for item in block.items],
                bulletType="bullet", start="•", leftIndent=14,
            ))
        elif block.kind == "divider":
            story.append(Spacer(1, 6))
            story.append(HRFlowable(width="100%", color="#d7dae2"))
            story.append(Spacer(1, 6))

    path.parent.mkdir(parents=True, exist_ok=True)
    document = SimpleDocTemplate(
        str(path), pagesize=A4,
        leftMargin=20 * mm, rightMargin=18 * mm,
        topMargin=18 * mm, bottomMargin=18 * mm,
        title=(bundle.task.title if bundle.task else bundle.workspace.name),
    )
    document.build(story)
    note = "" if mono != regular else "Моноширинный шрифт не найден, код набран основным."
    return ExportResult(path, "pdf", path.stat().st_size, note)


def _escape(raw: str) -> str:
    """Экранирует спецсимволы разметки reportlab."""
    return (raw or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---------------------------------------------------------------------------
# ZIP
# ---------------------------------------------------------------------------


def export_zip(bundle: ResultBundle, options: ExportOptions,
               path: Path) -> ExportResult:
    """Архив с файлами проекта, отчётом в Markdown и машиночитаемым манифестом."""
    blocks = build_document(bundle, options)
    path.parent.mkdir(parents=True, exist_ok=True)

    manifest = {
        "workspace": bundle.workspace.name,
        "task": bundle.task.title if bundle.task else "",
        "generated_at": _now(),
        "subtasks": [
            {"title": s.title, "status": s.status,
             "agent": bundle.agent_name(s.agent_id, options.anonymize),
             "rework_count": s.rework_count}
            for s in bundle.subtasks
        ],
        "incidents": [
            {"kind": i.kind, "severity": i.severity, "status": i.status,
             "description": i.description, "resolution": i.resolution}
            for i in bundle.incidents
        ],
        "usage": {"tokens": bundle.tokens, "cost_usd": round(bundle.cost, 6)},
        "files": [],
    }

    root = bundle.workspace_dir
    written = 0
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("RESULT.md", render_markdown(blocks))

        if options.include_files:
            for file_path in bundle.files:
                try:
                    relative = file_path.relative_to(root)
                except ValueError:
                    continue
                arcname = str(Path("files") / relative)
                try:
                    archive.write(file_path, arcname)
                except OSError as exc:
                    log.warning("Не удалось добавить %s: %s", file_path, exc)
                    continue
                manifest["files"].append(str(relative))
                written += 1

        archive.writestr("manifest.json",
                         json.dumps(manifest, ensure_ascii=False, indent=2))

    note = (f"В архив добавлено файлов: {written}" if written
            else "Файлов в рабочем каталоге не было — в архиве только отчёт.")
    return ExportResult(path, "zip", path.stat().st_size, note)


def _now() -> str:
    from datetime import datetime

    return datetime.now().isoformat(timespec="seconds")


# ---------------------------------------------------------------------------
# Единая точка входа
# ---------------------------------------------------------------------------

EXPORTERS = {
    "markdown": export_markdown,
    "docx": export_docx,
    "pdf": export_pdf,
    "zip": export_zip,
}
EXTENSIONS = {"markdown": ".md", "docx": ".docx", "pdf": ".pdf", "zip": ".zip"}


def export(bundle: ResultBundle, options: ExportOptions, fmt: str,
           path: Path) -> ExportResult:
    """Экспортирует результат в указанном формате."""
    exporter = EXPORTERS.get(fmt)
    if exporter is None:
        raise ExportError(f"Неизвестный формат экспорта: {fmt}")
    return exporter(bundle, options, path)


def suggest_filename(bundle: ResultBundle, fmt: str) -> str:
    """Предлагает имя файла: название задачи + дата."""
    from datetime import datetime

    base = (bundle.task.title if bundle.task and bundle.task.title
            else bundle.workspace.name) or "result"
    safe = "".join(ch if ch.isalnum() or ch in " -_" else "_" for ch in base).strip()
    safe = "_".join(safe.split())[:60] or "result"
    return f"{safe}_{datetime.now().strftime('%Y%m%d_%H%M')}{EXTENSIONS.get(fmt, '.txt')}"


def open_folder(path: Path) -> bool:
    """Открывает каталог с файлом в проводнике ОС."""
    import subprocess
    import sys

    folder = str(path.parent if path.is_file() else path)
    try:
        if sys.platform == "win32":
            subprocess.Popen(["explorer", folder])
        elif sys.platform == "darwin":
            subprocess.Popen(["open", folder])
        else:
            if shutil.which("xdg-open") is None:
                return False
            subprocess.Popen(["xdg-open", folder])
        return True
    except Exception:  # noqa: BLE001
        return False
````


## Интерфейс

### `ui/theme.py`

*264 строк*

````python
"""Оформление приложения: палитра и QSS.

Тема тёмная по умолчанию, светлая — переключается в настройках. Цвета
статусов вынесены отдельно: ими красятся бейджи агентов на дашборде.
"""

from __future__ import annotations

from app.config import PATHS

DARK = {
    "bg": "#12141a",
    "surface": "#191c24",
    "surface2": "#20242e",
    "border": "#2c313d",
    "text": "#e6e9f0",
    "text_dim": "#99a1b3",
    "accent": "#6c8cff",
    "accent_hover": "#8099ff",
    "danger": "#ef5f6b",
    "ok": "#3ecf8e",
    "warn": "#f0b429",
}

LIGHT = {
    "bg": "#f4f5f8",
    "surface": "#ffffff",
    "surface2": "#eef0f5",
    "border": "#d7dae2",
    "text": "#1a1d24",
    "text_dim": "#6a7080",
    "accent": "#3a5bd9",
    "accent_hover": "#2c49ba",
    "danger": "#d63a48",
    "ok": "#1f9d63",
    "warn": "#c98a06",
}

STATUS_COLORS = {
    "idle": "#99a1b3",
    "running": "#6c8cff",
    "paused": "#f0b429",
    "error": "#ef5f6b",
    "done": "#3ecf8e",
    "review": "#b07cff",
    "rework": "#f0b429",
}


#: текущая активная тема; графики берут цвета отсюда, чтобы не тянуть
#: настройки через полдюжины конструкторов
_ACTIVE_THEME = "dark"


def palette(theme: str) -> dict[str, str]:
    return LIGHT if theme == "light" else DARK


def set_active_theme(theme: str) -> None:
    """Запоминает тему, применённую к приложению."""
    global _ACTIVE_THEME
    _ACTIVE_THEME = theme if theme in ("dark", "light") else "dark"


def active_theme() -> str:
    return _ACTIVE_THEME


def current_palette() -> dict[str, str]:
    """Палитра активной темы — для виджетов, рисующих себя вручную."""
    return palette(_ACTIVE_THEME)


_ARROW_POINTS = {"down": ((1, 3), (5, 7), (9, 3)), "up": ((1, 7), (5, 3), (9, 7))}


def _arrow_icon(direction: str, colour: str) -> str:
    """Рисует стрелку в PNG-файл кэша и возвращает путь для QSS.

    Стрелки у QComboBox и QSpinBox пропадают, как только их кнопки
    стилизованы через QSS, а треугольник из рамок Qt не рисует — нужна
    картинка. SVG не годится: плагина qsvg в сборке PySide6 может не быть.
    Рядом кладётся вариант @2x — Qt сам берёт его на HiDPI-экранах.
    Вызывать можно только после создания QApplication.
    """
    from PySide6.QtCore import QPointF, Qt
    from PySide6.QtGui import QColor, QImage, QPainter, QPen

    folder = PATHS.home / "cache" / "theme"
    base = f"arrow_{direction}_{colour.lstrip('#')}"
    path = folder / f"{base}.png"
    if not path.exists():
        folder.mkdir(parents=True, exist_ok=True)
        for scale, target in ((1, path), (2, folder / f"{base}@2x.png")):
            image = QImage(10 * scale, 10 * scale, QImage.Format.Format_ARGB32)
            image.fill(Qt.GlobalColor.transparent)
            painter = QPainter(image)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            pen = QPen(QColor(colour), 1.6 * scale)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
            painter.setPen(pen)
            painter.drawPolyline([QPointF(x * scale, y * scale)
                                  for x, y in _ARROW_POINTS[direction]])
            painter.end()
            image.save(str(target))
    return path.as_posix()


def stylesheet(theme: str = "dark") -> str:
    """Собирает QSS под выбранную палитру."""
    set_active_theme(theme)
    c = palette(theme)
    down, up = _arrow_icon("down", c["text_dim"]), _arrow_icon("up", c["text_dim"])
    down_off, up_off = _arrow_icon("down", c["border"]), _arrow_icon("up", c["border"])
    return f"""
    QWidget {{
        background: {c['bg']};
        color: {c['text']};
        font-family: "Inter", "Segoe UI", "SF Pro Text", "Noto Sans", sans-serif;
        font-size: 14px;
    }}
    /* Правило выше красит фон всем виджетам. Внутри карточек это давало
       тёмные «заплатки» под надписями и под контейнерами-раскладками, поэтому
       у них фон прозрачный. «.QWidget» — только сам QWidget, без подклассов:
       окна и страницы свой фон сохраняют. */
    QLabel, QCheckBox, QRadioButton {{ background: transparent; }}
    .QWidget {{ background: transparent; }}
    QLabel#H1 {{ font-size: 24px; font-weight: 600; }}
    QLabel#H2 {{ font-size: 18px; font-weight: 600; }}
    QLabel#Dim {{ color: {c['text_dim']}; }}
    QLabel#Error {{ color: {c['danger']}; }}
    QLabel#Ok {{ color: {c['ok']}; }}

    QFrame#Card, QWidget#Card {{
        background: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 12px;
    }}
    QFrame#Sidebar {{
        background: {c['surface']};
        border-right: 1px solid {c['border']};
    }}

    QLineEdit, QTextEdit, QPlainTextEdit, QComboBox, QSpinBox, QDoubleSpinBox {{
        background: {c['surface2']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 7px 10px;
        selection-background-color: {c['accent']};
    }}
    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus, QComboBox:focus {{
        border: 1px solid {c['accent']};
    }}
    QComboBox::drop-down {{ border: none; width: 22px; }}
    QComboBox::down-arrow {{ image: url("{down}"); width: 10px; height: 10px; }}
    QComboBox::down-arrow:on {{ image: url("{up}"); }}
    QAbstractSpinBox {{ padding-right: 24px; }}
    QAbstractSpinBox::up-button, QAbstractSpinBox::down-button {{
        subcontrol-origin: border; width: 22px;
        border: none; background: transparent;
    }}
    QAbstractSpinBox::up-button {{ subcontrol-position: top right; }}
    QAbstractSpinBox::down-button {{ subcontrol-position: bottom right; }}
    QAbstractSpinBox::up-arrow {{ image: url("{up}"); width: 8px; height: 8px; }}
    QAbstractSpinBox::down-arrow {{ image: url("{down}"); width: 8px; height: 8px; }}
    QAbstractSpinBox::up-arrow:disabled, QAbstractSpinBox::up-arrow:off {{ image: url("{up_off}"); }}
    QAbstractSpinBox::down-arrow:disabled, QAbstractSpinBox::down-arrow:off {{ image: url("{down_off}"); }}
    QComboBox QAbstractItemView {{
        background: {c['surface2']};
        border: 1px solid {c['border']};
        selection-background-color: {c['accent']};
        outline: none;
    }}

    QPushButton {{
        background: {c['surface2']};
        border: 1px solid {c['border']};
        border-radius: 8px;
        padding: 8px 16px;
    }}
    QPushButton:hover {{ border-color: {c['accent']}; }}
    QPushButton:disabled {{ color: {c['text_dim']}; border-color: {c['border']}; }}
    QPushButton#Primary {{
        background: {c['accent']};
        border: 1px solid {c['accent']};
        color: #ffffff;
        font-weight: 600;
    }}
    QPushButton#Primary:hover {{ background: {c['accent_hover']}; }}
    QPushButton#Primary:disabled {{
        background: {c['surface2']}; border-color: {c['border']};
        color: {c['text_dim']}; font-weight: 600;
    }}
    QPushButton#Icon {{ padding: 6px 0; }}
    QPushButton#Danger {{ color: {c['danger']}; }}
    QPushButton#Danger:hover {{ border-color: {c['danger']}; }}
    QPushButton#Nav {{
        background: transparent;
        border: none;
        border-radius: 8px;
        padding: 10px 14px;
        text-align: left;
    }}
    QPushButton#Nav:hover {{ background: {c['surface2']}; }}
    QPushButton#Nav:checked {{ background: {c['accent']}; color: #ffffff; font-weight: 600; }}

    QListWidget, QTableWidget, QTreeWidget {{
        background: {c['surface']};
        border: 1px solid {c['border']};
        border-radius: 10px;
        outline: none;
    }}
    QListWidget::item {{ padding: 8px; border-radius: 6px; }}
    QListWidget::item:selected {{ background: {c['accent']}; color: #ffffff; }}
    QHeaderView::section {{
        background: {c['surface2']};
        border: none;
        border-bottom: 1px solid {c['border']};
        padding: 8px;
        font-weight: 600;
    }}
    QTableWidget {{ gridline-color: {c['border']}; }}

    QScrollBar:vertical {{ background: transparent; width: 10px; margin: 2px; }}
    QScrollBar::handle:vertical {{
        background: {c['border']}; border-radius: 5px; min-height: 30px;
    }}
    QScrollBar::handle:vertical:hover {{ background: {c['text_dim']}; }}
    QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; width: 0; }}
    QScrollBar:horizontal {{ background: transparent; height: 10px; margin: 2px; }}
    QScrollBar::handle:horizontal {{
        background: {c['border']}; border-radius: 5px; min-width: 30px;
    }}

    QProgressBar {{
        background: {c['surface2']};
        border: none; border-radius: 6px; height: 10px; text-align: center;
    }}
    QProgressBar::chunk {{ background: {c['accent']}; border-radius: 6px; }}

    QCheckBox::indicator, QRadioButton::indicator {{
        width: 16px; height: 16px; border-radius: 4px;
        border: 1px solid {c['border']}; background: {c['surface2']};
    }}
    QCheckBox::indicator:checked {{ background: {c['accent']}; border-color: {c['accent']}; }}

    QTabWidget::pane {{ border: 1px solid {c['border']}; border-radius: 10px; top: -1px; }}
    QTabBar::tab {{
        background: transparent; padding: 8px 16px; border: none;
        color: {c['text_dim']};
    }}
    QTabBar::tab:selected {{ color: {c['text']}; border-bottom: 2px solid {c['accent']}; }}

    QToolTip {{
        background: {c['surface2']}; color: {c['text']};
        border: 1px solid {c['border']}; padding: 6px; border-radius: 6px;
    }}
    QMenu {{
        background: {c['surface2']}; border: 1px solid {c['border']}; border-radius: 8px;
    }}
    QMenu::item:selected {{ background: {c['accent']}; }}
    QSplitter::handle {{ background: {c['border']}; }}
    """
````

### `ui/widgets/common.py`

*144 строк*

````python
"""Мелкие переиспользуемые виджеты."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from ui.theme import STATUS_COLORS


class Card(QFrame):
    """Карточка-контейнер со скруглением и рамкой."""

    def __init__(self, parent: QWidget | None = None, spacing: int = 12) -> None:
        super().__init__(parent)
        self.setObjectName("Card")
        self.body = QVBoxLayout(self)
        self.body.setContentsMargins(16, 16, 16, 16)
        self.body.setSpacing(spacing)


class StatusBadge(QLabel):
    """Цветной бейдж статуса агента/подзадачи."""

    def __init__(self, status: str = "idle", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Иначе в строке с крупным заголовком бейдж растягивается по высоте.
        self.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.set_status(status)

    def set_status(self, status: str) -> None:
        color = STATUS_COLORS.get(status, STATUS_COLORS["idle"])
        self.setText(tr(f"status.{status}") if f"status.{status}" else status)
        self.setStyleSheet(
            f"color: {color}; border: 1px solid {color}; border-radius: 9px;"
            f"padding: 2px 10px; font-size: 12px; font-weight: 600; background: transparent;"
        )


class Header(QWidget):
    """Заголовок страницы: title + subtitle + слот для кнопок справа."""

    def __init__(self, title: str, subtitle: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        row = QHBoxLayout(self)
        row.setContentsMargins(0, 0, 0, 0)

        texts = QVBoxLayout()
        texts.setSpacing(2)
        self.title_label = QLabel(title)
        self.title_label.setObjectName("H1")
        texts.addWidget(self.title_label)
        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setObjectName("Dim")
        self.subtitle_label.setWordWrap(True)
        self.subtitle_label.setVisible(bool(subtitle))
        texts.addWidget(self.subtitle_label)
        row.addLayout(texts, 1)

        self.actions = QHBoxLayout()
        self.actions.setSpacing(8)
        row.addLayout(self.actions)

    def add_action(self, button: QPushButton) -> None:
        self.actions.addWidget(button)

    def set_texts(self, title: str, subtitle: str = "") -> None:
        self.title_label.setText(title)
        self.subtitle_label.setText(subtitle)
        self.subtitle_label.setVisible(bool(subtitle))


class PageSwitcher(QWidget):
    """Замена QStackedWidget для форм с переносом строк.

    QStackedWidget не передаёт height-for-width своих страниц, из-за чего
    длинные надписи с переносом обрезаются. Здесь страницы просто лежат
    в одном layout, а видна только текущая.
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._pages: list[QWidget] = []
        self._current = -1

    def addWidget(self, page: QWidget) -> int:  # noqa: N802 — как у QStackedWidget
        self._pages.append(page)
        self._layout.addWidget(page)
        if self._current < 0:
            self._current = 0
        page.setVisible(len(self._pages) - 1 == self._current)
        return len(self._pages) - 1

    def setCurrentIndex(self, index: int) -> None:  # noqa: N802
        self._current = index
        for i, page in enumerate(self._pages):
            page.setVisible(i == index)

    def currentIndex(self) -> int:  # noqa: N802
        return self._current


class EmptyState(QLabel):
    """Заглушка для пустых списков."""

    def __init__(self, text: str, parent: QWidget | None = None) -> None:
        super().__init__(text, parent)
        self.setObjectName("Dim")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setWordWrap(True)
        self.setMinimumHeight(120)


def confirm(parent: QWidget, text: str) -> bool:
    """Диалог подтверждения с локализованными кнопками."""
    box = QMessageBox(parent)
    box.setWindowTitle(tr("common.confirm"))
    box.setText(text)
    box.setIcon(QMessageBox.Icon.Question)
    yes = box.addButton(tr("common.yes"), QMessageBox.ButtonRole.YesRole)
    box.addButton(tr("common.no"), QMessageBox.ButtonRole.NoRole)
    box.exec()
    return box.clickedButton() is yes


def warn(parent: QWidget, text: str, title: str = "") -> None:
    QMessageBox.warning(parent, title or tr("common.error"), text)


def info(parent: QWidget, text: str, title: str = "") -> None:
    QMessageBox.information(parent, title or tr("common.success"), text)
````

### `ui/widgets/charts.py`

*305 строк*

````python
"""Лёгкие графики на QPainter.

Намеренно без QtCharts и pyqtgraph: дашборду нужны две простые диаграммы,
а собственная отрисовка не тянет зависимостей, мгновенно подхватывает тему
приложения и не ломается при разных сборках PySide6.

Все виджеты безопасны к пустым данным: при отсутствии точек рисуется
аккуратная надпись, а не пустой прямоугольник.
"""

from __future__ import annotations

from dataclasses import dataclass

from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QSizePolicy, QWidget

from ui.theme import current_palette

PADDING_LEFT = 58
PADDING_RIGHT = 14
PADDING_TOP = 26
PADDING_BOTTOM = 30
GRID_LINES = 4


def _color(key: str, alpha: int = 255) -> QColor:
    colour = QColor(current_palette().get(key, "#888888"))
    colour.setAlpha(alpha)
    return colour


def _nice_max(value: float) -> float:
    """Округляет верх шкалы вверх до «красивого» числа (1, 2, 5 × 10^n)."""
    if value <= 0:
        return 1.0
    import math

    exponent = math.floor(math.log10(value))
    base = 10 ** exponent
    for step in (1, 2, 2.5, 5, 10):
        if value <= step * base:
            return step * base
    return 10 * base


def _fmt(value: float, unit: str) -> str:
    """Короткая подпись оси: 12.3k, $0.0412, 1.2M."""
    if unit == "usd":
        if value >= 1:
            return f"${value:,.2f}".replace(",", " ")
        return f"${value:.4f}"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"{value / 1_000:.1f}k"
    return f"{value:.0f}"


class ChartBase(QWidget):
    """Общая рамка: заголовок, сетка, подписи оси Y."""

    def __init__(self, title: str = "", unit: str = "", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.title = title
        self.unit = unit
        self.empty_text = "нет данных"
        self.setMinimumHeight(190)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

    def set_title(self, title: str) -> None:
        self.title = title
        self.update()

    def _plot_rect(self) -> QRectF:
        return QRectF(
            PADDING_LEFT, PADDING_TOP,
            max(10.0, self.width() - PADDING_LEFT - PADDING_RIGHT),
            max(10.0, self.height() - PADDING_TOP - PADDING_BOTTOM),
        )

    def _draw_frame(self, painter: QPainter, top_value: float) -> QRectF:
        """Рисует заголовок, горизонтальную сетку и подписи, возвращает поле графика."""
        rect = self._plot_rect()

        if self.title:
            font = QFont(painter.font())
            font.setPointSizeF(max(8.0, font.pointSizeF()))
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QPen(_color("text")))
            painter.drawText(QRectF(PADDING_LEFT, 2, rect.width(), 20),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             self.title)
            font.setBold(False)
            painter.setFont(font)

        grid_pen = QPen(_color("border"))
        grid_pen.setWidthF(1.0)
        painter.setPen(grid_pen)
        for i in range(GRID_LINES + 1):
            y = rect.bottom() - rect.height() * i / GRID_LINES
            painter.drawLine(QPointF(rect.left(), y), QPointF(rect.right(), y))
            painter.setPen(QPen(_color("text_dim")))
            painter.drawText(
                QRectF(0, y - 9, PADDING_LEFT - 8, 18),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                _fmt(top_value * i / GRID_LINES, self.unit),
            )
            painter.setPen(grid_pen)
        return rect

    def _draw_empty(self, painter: QPainter) -> None:
        painter.setPen(QPen(_color("text_dim")))
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.empty_text)


@dataclass
class SeriesPoint:
    """Точка временного ряда: подпись по оси X и значение."""

    label: str
    value: float


class LineChart(ChartBase):
    """Кумулятивная кривая с заливкой под ней."""

    def __init__(self, title: str = "", unit: str = "",
                 parent: QWidget | None = None) -> None:
        super().__init__(title, unit, parent)
        self._points: list[SeriesPoint] = []

    def set_points(self, points: list[SeriesPoint]) -> None:
        self._points = points
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802 — сигнатура Qt
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        if len(self._points) < 2:
            if self.title:
                self._draw_frame(painter, 1.0)
            self._draw_empty(painter)
            return

        top = _nice_max(max(p.value for p in self._points))
        rect = self._draw_frame(painter, top)

        step = rect.width() / (len(self._points) - 1)
        coords = [
            QPointF(rect.left() + i * step,
                    rect.bottom() - (p.value / top) * rect.height())
            for i, p in enumerate(self._points)
        ]

        # Заливка под кривой
        area = QPainterPath()
        area.moveTo(QPointF(coords[0].x(), rect.bottom()))
        for point in coords:
            area.lineTo(point)
        area.lineTo(QPointF(coords[-1].x(), rect.bottom()))
        area.closeSubpath()
        painter.fillPath(area, _color("accent", 46))

        line_pen = QPen(_color("accent"))
        line_pen.setWidthF(2.0)
        painter.setPen(line_pen)
        path = QPainterPath(coords[0])
        for point in coords[1:]:
            path.lineTo(point)
        painter.drawPath(path)

        # Точка последнего значения и её подпись
        painter.setBrush(_color("accent"))
        painter.drawEllipse(coords[-1], 3.5, 3.5)
        painter.setPen(QPen(_color("text")))
        painter.drawText(
            QRectF(coords[-1].x() - 90, coords[-1].y() - 24, 86, 18),
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
            _fmt(self._points[-1].value, self.unit),
        )

        # Подписи по краям оси X
        painter.setPen(QPen(_color("text_dim")))
        painter.drawText(QRectF(rect.left(), rect.bottom() + 6, 120, 18),
                         Qt.AlignmentFlag.AlignLeft, self._points[0].label)
        painter.drawText(QRectF(rect.right() - 120, rect.bottom() + 6, 120, 18),
                         Qt.AlignmentFlag.AlignRight, self._points[-1].label)


@dataclass
class Bar:
    """Столбец: подпись, значение и необязательный цвет."""

    label: str
    value: float
    color: str = ""


class BarChart(ChartBase):
    """Горизонтальные столбцы — удобны, когда подписи длинные (имена агентов)."""

    ROW_HEIGHT = 30

    def __init__(self, title: str = "", unit: str = "",
                 parent: QWidget | None = None) -> None:
        super().__init__(title, unit, parent)
        self._bars: list[Bar] = []

    def set_bars(self, bars: list[Bar]) -> None:
        self._bars = bars
        self.setMinimumHeight(max(140, PADDING_TOP + 14 + self.ROW_HEIGHT * max(1, len(bars))))
        self.update()

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.title:
            font = QFont(painter.font())
            font.setBold(True)
            painter.setFont(font)
            painter.setPen(QPen(_color("text")))
            painter.drawText(QRectF(10, 2, self.width() - 20, 20),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                             self.title)
            font.setBold(False)
            painter.setFont(font)

        if not self._bars:
            self._draw_empty(painter)
            return

        top = max((b.value for b in self._bars), default=0.0) or 1.0
        label_width = 150.0
        metrics = painter.fontMetrics()
        bar_left = 12 + label_width
        bar_width = max(30.0, self.width() - bar_left - 90)

        for i, bar in enumerate(self._bars):
            y = PADDING_TOP + 6 + i * self.ROW_HEIGHT
            painter.setPen(QPen(_color("text_dim")))
            painter.drawText(
                QRectF(12, y, label_width - 10, self.ROW_HEIGHT - 8),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                metrics.elidedText(bar.label, Qt.TextElideMode.ElideRight,
                                   int(label_width - 10)),
            )

            track = QRectF(bar_left, y + 6, bar_width, self.ROW_HEIGHT - 18)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(_color("surface2"))
            painter.drawRoundedRect(track, 5, 5)

            filled = QRectF(track)
            filled.setWidth(max(3.0, bar_width * (bar.value / top)))
            painter.setBrush(QColor(bar.color) if bar.color else _color("accent"))
            painter.drawRoundedRect(filled, 5, 5)

            painter.setPen(QPen(_color("text")))
            painter.drawText(
                QRectF(bar_left + bar_width + 8, y, 80, self.ROW_HEIGHT - 8),
                Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
                _fmt(bar.value, self.unit),
            )


class SegmentBar(QWidget):
    """Одна полоска, разбитая на цветные сегменты — статусы подзадач."""

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._segments: list[tuple[str, int, str]] = []   # (подпись, количество, цвет)
        self.setFixedHeight(14)

    def set_segments(self, segments: list[tuple[str, int, str]]) -> None:
        self._segments = [s for s in segments if s[1] > 0]
        self.update()
        self.setToolTip(", ".join(f"{label}: {count}" for label, count, _ in self._segments))

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        total = sum(count for _, count, _ in self._segments)
        track = QRectF(0, 0, self.width(), self.height())
        painter.setBrush(_color("surface2"))
        painter.drawRoundedRect(track, 7, 7)
        if not total:
            return

        painter.setClipping(True)
        path = QPainterPath()
        path.addRoundedRect(track, 7, 7)
        painter.setClipPath(path)

        x = 0.0
        for _, count, colour in self._segments:
            width = self.width() * count / total
            painter.setBrush(QColor(colour))
            painter.drawRect(QRectF(x, 0, width + 0.5, self.height()))
            x += width
````

### `ui/widgets/approval_panel.py`

*155 строк*

````python
"""Панель решений human-in-the-loop (этап 7).

Когда ядро останавливается и ждёт человека, здесь появляется карточка с
вопросом, выжимкой по делу и кнопками. Панель намеренно встроена в страницу
«Выполнение», а не сделана модальным окном: вопросов может быть несколько
одновременно, и модалка заслоняла бы прогресс, по которому как раз и
принимается решение.
"""

from __future__ import annotations

from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.hitl import DECISION_TITLES, REASON_TITLES, ApprovalRequest, Decision
from ui.theme import current_palette

#: у деструктивных решений своя окраска, чтобы их не нажимали на автомате
DECISION_STYLES = {
    Decision.APPROVE: "Primary",
    Decision.REWORK: "",
    Decision.SKIP: "",
    Decision.ABORT: "Danger",
}

DECISION_HINTS = {
    Decision.APPROVE: "Принять результат как есть и продолжить",
    Decision.REWORK: "Вернуть исполнителю; комментарий уйдёт ему первым",
    Decision.SKIP: "Пометить подзадачу неудачной и идти дальше",
    Decision.ABORT: "Остановить весь прогон",
}


class ApprovalCard(QFrame):
    """Один вопрос к пользователю."""

    def __init__(self, request: ApprovalRequest,
                 on_decide: Callable[[int, Decision, str], None],
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.request = request
        self.on_decide = on_decide

        colours = current_palette()
        self.setObjectName("Card")
        self.setStyleSheet(
            f"QFrame#Card {{ border: 1px solid {colours['warn']}; "
            f"border-radius: 12px; background: {colours['surface']}; }}"
        )

        lay = QVBoxLayout(self)
        lay.setContentsMargins(16, 14, 16, 14)
        lay.setSpacing(8)

        head = QHBoxLayout()
        badge = QLabel(REASON_TITLES.get(request.reason, request.reason.value))
        badge.setStyleSheet(
            f"color: {colours['warn']}; border: 1px solid {colours['warn']};"
            f"border-radius: 9px; padding: 2px 10px; font-size: 12px; font-weight: 600;"
        )
        head.addWidget(badge)
        if request.agent_name:
            who = QLabel(request.agent_name)
            who.setObjectName("Dim")
            head.addWidget(who)
        head.addStretch(1)
        lay.addLayout(head)

        question = QLabel(request.question)
        question.setObjectName("H2")
        question.setWordWrap(True)
        lay.addWidget(question)

        if request.details:
            self.details = QLabel(_clip(request.details, 700))
            self.details.setObjectName("Dim")
            self.details.setWordWrap(True)
            self.details.setTextInteractionFlags(
                Qt.TextInteractionFlag.TextSelectableByMouse
            )
            lay.addWidget(self.details)

            if len(request.details) > 700:
                self._expanded = False
                self.btn_more = QPushButton("Показать полностью")
                self.btn_more.clicked.connect(self._toggle_details)
                lay.addWidget(self.btn_more, 0, Qt.AlignmentFlag.AlignLeft)

        self.comment = QLineEdit()
        self.comment.setPlaceholderText(
            "Комментарий (уйдёт исполнителю при отправке на доработку)"
        )
        lay.addWidget(self.comment)

        buttons = QHBoxLayout()
        buttons.setSpacing(8)
        for decision in request.options:
            button = QPushButton(DECISION_TITLES.get(decision, decision.value))
            style = DECISION_STYLES.get(decision, "")
            if style:
                button.setObjectName(style)
            button.setToolTip(DECISION_HINTS.get(decision, ""))
            button.clicked.connect(
                lambda _=False, d=decision: self._decide(d)
            )
            buttons.addWidget(button)
        buttons.addStretch(1)
        lay.addLayout(buttons)

    def _toggle_details(self) -> None:
        self._expanded = not self._expanded
        self.details.setText(self.request.details if self._expanded
                             else _clip(self.request.details, 700))
        self.btn_more.setText("Свернуть" if self._expanded else "Показать полностью")

    def _decide(self, decision: Decision) -> None:
        self.setEnabled(False)
        self.on_decide(self.request.id, decision, self.comment.text())


class ApprovalPanel(QWidget):
    """Стопка открытых вопросов; скрывается, когда их нет."""

    def __init__(self, on_decide: Callable[[int, Decision, str], None],
                 parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.on_decide = on_decide
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(10)
        self.setVisible(False)

    def set_requests(self, requests: list[ApprovalRequest]) -> None:
        while self._layout.count():
            item = self._layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        for request in requests:
            self._layout.addWidget(ApprovalCard(request, self.on_decide, self))
        self.setVisible(bool(requests))


def _clip(text: str, limit: int) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[:limit] + " …"
````

### `ui/login_window.py`

*288 строк*

````python
"""Этап 1 — окно локальной авторизации.

Поддерживает несколько профилей на одном устройстве. Пароль профиля
одновременно является мастер-паролем для расшифровки API-ключей, поэтому
при создании профиля показывается предупреждение о невозможности восстановления.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_NAME, APP_VERSION, AppSettings
from app.i18n import available_languages, current_language, set_language, tr
from core.security.crypto import (
    Session,
    keyring_available,
    keyring_delete_password,
    keyring_get_password,
    keyring_store_password,
)
from storage.db import Database
from storage.repositories import UserRepo
from ui.widgets.common import Card, PageSwitcher

MIN_PASSWORD_LEN = 8


class LoginWindow(QWidget):
    """Окно входа. При успехе эмитит ``logged_in`` с открытой сессией."""

    logged_in = Signal(object)  # Session

    def __init__(self, db: Database, settings: AppSettings) -> None:
        super().__init__()
        self.db = db
        self.settings = settings
        self.users = UserRepo(db)

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(460, 560)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(40, 32, 40, 32)
        outer.addStretch(1)

        self.card = Card(self, spacing=14)
        # Фиксированная ширина, а не максимальная: при выравнивании по центру
        # layout отдаёт карточке ширину sizeHint, и перенос строк в
        # предупреждении считался бы не от той ширины — текст обрезался.
        self.card.setFixedWidth(420)
        outer.addWidget(self.card, 0, Qt.AlignmentFlag.AlignHCenter)
        outer.addStretch(1)

        self.footer = QLabel(f"{APP_NAME} {APP_VERSION} · локальное хранение данных")
        self.footer.setObjectName("Dim")
        self.footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        outer.addWidget(self.footer)

        self.stack = PageSwitcher()
        self.card.body.addWidget(self.stack)
        self.stack.addWidget(self._build_signin())
        self.stack.addWidget(self._build_signup())

        self._refresh_profiles()

    # -- построение экранов --------------------------------------------------
    def _build_signin(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        lang_row = QHBoxLayout()
        lang_row.addStretch(1)
        self.lang_box = QComboBox()
        for code, label in available_languages():
            self.lang_box.addItem(label, code)
        self.lang_box.setCurrentIndex(
            max(0, [c for c, _ in available_languages()].index(current_language()))
        )
        self.lang_box.currentIndexChanged.connect(self._on_language)
        self.lang_box.setMaximumWidth(140)
        lang_row.addWidget(self.lang_box)
        lay.addLayout(lang_row)

        self.title = QLabel(tr("login.title"))
        self.title.setObjectName("H1")
        lay.addWidget(self.title)
        self.subtitle = QLabel(tr("login.subtitle"))
        self.subtitle.setObjectName("Dim")
        self.subtitle.setWordWrap(True)
        lay.addWidget(self.subtitle)

        self.lbl_user = QLabel(tr("login.username"))
        lay.addWidget(self.lbl_user)
        self.profile_box = QComboBox()
        self.profile_box.setEditable(False)
        self.profile_box.currentTextChanged.connect(self._on_profile_changed)
        lay.addWidget(self.profile_box)

        self.lbl_pass = QLabel(tr("login.password"))
        lay.addWidget(self.lbl_pass)
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.returnPressed.connect(self._do_signin)
        lay.addWidget(self.password)

        self.remember = QCheckBox(tr("login.remember"))
        self.remember.setEnabled(keyring_available())
        self.remember.setChecked(self.settings.remember_master_password)
        if not keyring_available():
            self.remember.setToolTip("Установите пакет keyring, чтобы включить эту опцию")
        lay.addWidget(self.remember)

        self.error = QLabel("")
        self.error.setObjectName("Error")
        self.error.setWordWrap(True)
        self.error.setVisible(False)
        lay.addWidget(self.error)

        self.btn_signin = QPushButton(tr("login.signin"))
        self.btn_signin.setObjectName("Primary")
        self.btn_signin.clicked.connect(self._do_signin)
        lay.addWidget(self.btn_signin)

        self.btn_to_signup = QPushButton(tr("login.create"))
        self.btn_to_signup.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        lay.addWidget(self.btn_to_signup)
        return page

    def _build_signup(self) -> QWidget:
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(12)

        self.su_title = QLabel(tr("login.create_title"))
        self.su_title.setObjectName("H1")
        lay.addWidget(self.su_title)

        self.su_warning = QLabel(tr("login.warning"))
        self.su_warning.setObjectName("Dim")
        self.su_warning.setWordWrap(True)
        lay.addWidget(self.su_warning)

        self.su_lbl_user = QLabel(tr("login.username"))
        lay.addWidget(self.su_lbl_user)
        self.su_username = QLineEdit()
        lay.addWidget(self.su_username)

        self.su_lbl_pass = QLabel(tr("login.password"))
        lay.addWidget(self.su_lbl_pass)
        self.su_password = QLineEdit()
        self.su_password.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.su_password)

        self.su_lbl_pass2 = QLabel(tr("login.password2"))
        lay.addWidget(self.su_lbl_pass2)
        self.su_password2 = QLineEdit()
        self.su_password2.setEchoMode(QLineEdit.EchoMode.Password)
        self.su_password2.returnPressed.connect(self._do_signup)
        lay.addWidget(self.su_password2)

        self.su_error = QLabel("")
        self.su_error.setObjectName("Error")
        self.su_error.setWordWrap(True)
        self.su_error.setVisible(False)
        lay.addWidget(self.su_error)

        self.su_btn_create = QPushButton(tr("login.create"))
        self.su_btn_create.setObjectName("Primary")
        self.su_btn_create.clicked.connect(self._do_signup)
        lay.addWidget(self.su_btn_create)

        self.su_btn_back = QPushButton(tr("common.cancel"))
        self.su_btn_back.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        lay.addWidget(self.su_btn_back)
        return page

    # -- логика --------------------------------------------------------------
    def _refresh_profiles(self) -> None:
        names = self.users.list_usernames()
        self.profile_box.clear()
        self.profile_box.addItems(names)
        if not names:
            self._show_error(tr("login.no_profiles"))
            self.stack.setCurrentIndex(1)
            return
        if self.settings.last_username in names:
            self.profile_box.setCurrentText(self.settings.last_username)
        self._on_profile_changed(self.profile_box.currentText())

    def _on_profile_changed(self, username: str) -> None:
        """Подставляет сохранённый пароль, если пользователь просил его запомнить."""
        self.password.clear()
        if username and self.settings.remember_master_password and keyring_available():
            saved = keyring_get_password(username)
            if saved:
                self.password.setText(saved)

    def _on_language(self) -> None:
        code = self.lang_box.currentData()
        set_language(code)
        self.settings.language = code
        self.settings.save()
        self._retranslate()

    def _retranslate(self) -> None:
        self.title.setText(tr("login.title"))
        self.subtitle.setText(tr("login.subtitle"))
        self.lbl_user.setText(tr("login.username"))
        self.lbl_pass.setText(tr("login.password"))
        self.remember.setText(tr("login.remember"))
        self.btn_signin.setText(tr("login.signin"))
        self.btn_to_signup.setText(tr("login.create"))
        self.su_title.setText(tr("login.create_title"))
        self.su_warning.setText(tr("login.warning"))
        self.su_lbl_user.setText(tr("login.username"))
        self.su_lbl_pass.setText(tr("login.password"))
        self.su_lbl_pass2.setText(tr("login.password2"))
        self.su_btn_create.setText(tr("login.create"))
        self.su_btn_back.setText(tr("common.cancel"))

    def _show_error(self, text: str) -> None:
        self.error.setText(text)
        self.error.setVisible(bool(text))

    def _show_signup_error(self, text: str) -> None:
        self.su_error.setText(text)
        self.su_error.setVisible(bool(text))

    def _do_signin(self) -> None:
        username = self.profile_box.currentText().strip()
        password = self.password.text()
        if not username or not password:
            self._show_error(tr("login.bad_credentials"))
            return
        self.btn_signin.setEnabled(False)
        try:
            session: Session | None = self.users.authenticate(username, password)
        finally:
            self.btn_signin.setEnabled(True)
        if session is None:
            self._show_error(tr("login.bad_credentials"))
            return

        self.settings.last_username = username
        self.settings.remember_master_password = self.remember.isChecked()
        self.settings.save()
        if self.remember.isChecked():
            keyring_store_password(username, password)
        else:
            keyring_delete_password(username)

        self._show_error("")
        self.logged_in.emit(session)

    def _do_signup(self) -> None:
        username = self.su_username.text().strip()
        p1, p2 = self.su_password.text(), self.su_password2.text()
        if not username:
            self._show_signup_error(tr("login.username"))
            return
        if self.users.exists(username):
            self._show_signup_error(tr("login.user_exists"))
            return
        if len(p1) < MIN_PASSWORD_LEN:
            self._show_signup_error(tr("login.password_short"))
            return
        if p1 != p2:
            self._show_signup_error(tr("login.password_mismatch"))
            return

        session = self.users.create(username, p1)
        self.settings.last_username = username
        self.settings.save()
        self._show_signup_error("")
        self.logged_in.emit(session)
````

### `ui/main_window.py`

*250 строк*

````python
"""Главное окно: боковая навигация + стек страниц.

Активный воркспейс — общее состояние окна: при его смене страницы агентов,
задачи, дашборда и настроек перезагружают свои данные.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from app.config import APP_NAME, APP_VERSION, AppSettings
from app.i18n import tr
from core.events import EventBus
from core.orchestrator import Orchestrator
from core.security.crypto import Session
from storage.db import Database
from storage.repositories import Repos
from ui.pages.agents_page import AgentsPage
from ui.pages.dashboard_page import DashboardPage
from ui.pages.budget_page import BudgetPage
from ui.pages.export_page import ExportPage
from ui.pages.keys_page import KeysPage
from ui.pages.run_page import RunPage
from ui.pages.settings_page import SettingsPage
from ui.pages.supervisor_page import SupervisorPage
from ui.pages.task_page import TaskPage
from ui.pages.workspaces_page import WorkspacesPage
from ui.theme import stylesheet


class MainWindow(QMainWindow):
    """Основное окно приложения после успешного входа."""

    logged_out = Signal()
    #: язык сменился — окно нужно собрать заново (аргумент: индекс страницы)
    rebuild_requested = Signal(int)

    def __init__(self, db: Database, session: Session, app_settings: AppSettings) -> None:
        super().__init__()
        self.db = db
        self.session = session
        self.app_settings = app_settings
        self.repos = Repos(db, session)
        self.workspace_id: int | None = None

        # Шина событий и оркестратор живут на уровне окна: один прогон на окно.
        self.bus = EventBus()
        self.orchestrator = Orchestrator(self.repos, self.bus)

        self.setWindowTitle(f"{APP_NAME} — {session.username}")
        self.resize(1280, 820)

        central = QWidget()
        self.setCentralWidget(central)
        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        root.addWidget(self._build_sidebar())

        self.stack = QStackedWidget()
        root.addWidget(self.stack, 1)

        # --- страницы ---
        self.page_workspaces = WorkspacesPage(self.repos)
        self.page_keys = KeysPage(self.repos)
        self.page_agents = AgentsPage(self.repos)
        self.page_task = TaskPage(self.repos)
        self.page_run = RunPage(self.repos, self.bus, self.orchestrator)
        self.page_supervisor = SupervisorPage(self.repos, self.bus, self.orchestrator)
        self.page_dashboard = DashboardPage(self.repos, self.bus)
        self.page_budget = BudgetPage(self.repos, self.bus)
        self.page_export = ExportPage(self.repos)
        self.page_settings = SettingsPage(
            self.repos, app_settings,
            on_theme_change=self._apply_theme,
            on_language_change=lambda _: self._on_language_changed(),
        )
        for page in (self.page_workspaces, self.page_keys, self.page_agents,
                     self.page_task, self.page_run, self.page_supervisor,
                     self.page_dashboard, self.page_budget, self.page_export,
                     self.page_settings):
            self.stack.addWidget(page)

        # --- связи ---
        self.page_workspaces.workspace_selected.connect(self.set_workspace)
        self.page_workspaces.workspaces_changed.connect(self._update_workspace_label)
        self.page_keys.keys_changed.connect(self.page_agents.refresh)
        self.page_agents.agents_changed.connect(self.page_task.refresh)
        self.page_agents.agents_changed.connect(self.page_dashboard.refresh)
        self.page_task.task_changed.connect(self.page_dashboard.refresh)
        self.page_task.task_changed.connect(self.page_run.refresh)
        self.page_task.run_requested.connect(self._goto_run)
        self.page_agents.agents_changed.connect(self.page_run.refresh)

        self._select_page(0)
        self.page_workspaces.refresh()
        self.page_keys.refresh()
        self._restore_last_workspace()

    # -- построение ----------------------------------------------------------
    def _build_sidebar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("Sidebar")
        bar.setFixedWidth(230)
        lay = QVBoxLayout(bar)
        lay.setContentsMargins(14, 18, 14, 18)
        lay.setSpacing(6)

        logo = QLabel(APP_NAME)
        logo.setObjectName("H2")
        lay.addWidget(logo)
        version = QLabel(f"v{APP_VERSION} · {self.session.username}")
        version.setObjectName("Dim")
        lay.addWidget(version)
        lay.addSpacing(12)

        self.ws_label = QLabel(tr("ws.current") + ": —")
        self.ws_label.setObjectName("Dim")
        self.ws_label.setWordWrap(True)
        lay.addWidget(self.ws_label)
        lay.addSpacing(8)

        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        entries = [
            ("nav.workspaces", 0),
            ("nav.keys", 1),
            ("nav.agents", 2),
            ("nav.task", 3),
            ("nav.run", 4),
            ("nav.supervisor", 5),
            ("nav.dashboard", 6),
            ("nav.budget", 7),
            ("nav.export", 8),
            ("nav.settings", 9),
        ]
        for key, index in entries:
            button = QPushButton(tr(key))
            button.setObjectName("Nav")
            button.setCheckable(True)
            button.clicked.connect(lambda _=False, i=index: self._select_page(i))
            self.nav_group.addButton(button, index)
            lay.addWidget(button)

        lay.addStretch(1)
        logout = QPushButton(tr("nav.logout"))
        logout.clicked.connect(self._logout)
        lay.addWidget(logout)
        return bar

    # -- состояние -----------------------------------------------------------
    def _select_page(self, index: int) -> None:
        self.stack.setCurrentIndex(index)
        button = self.nav_group.button(index)
        if button:
            button.setChecked(True)
        widget = self.stack.currentWidget()
        if hasattr(widget, "refresh"):
            widget.refresh()

    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.page_workspaces.set_active(ws_id)
        self.page_agents.set_workspace(ws_id)
        self.page_task.set_workspace(ws_id)
        self.page_run.set_workspace(ws_id)
        self.page_supervisor.set_workspace(ws_id)
        self.page_budget.set_workspace(ws_id)
        self.page_export.set_workspace(ws_id)
        self.page_dashboard.set_workspace(ws_id)
        self.page_settings.set_workspace(ws_id)
        self._update_workspace_label()
        self._remember_workspace(ws_id)

    def _goto_run(self) -> None:
        """Переход на страницу выполнения по кнопке со страницы задачи."""
        self._select_page(4)

    def _update_workspace_label(self) -> None:
        ws = self.repos.workspaces.get(self.workspace_id) if self.workspace_id else None
        self.ws_label.setText(f"{tr('ws.current')}: {ws.name if ws else '—'}")

    def _remember_workspace(self, ws_id: int | None) -> None:
        user = self.repos.users.get(self.session.user_id)
        if user is None:
            return
        settings = dict(user.settings)
        settings["last_workspace_id"] = ws_id
        self.repos.users.save_settings(self.session.user_id, settings)

    def _restore_last_workspace(self) -> None:
        user = self.repos.users.get(self.session.user_id)
        last = (user.settings.get("last_workspace_id") if user else None)
        workspaces = self.repos.workspaces.list(self.session.user_id)
        ids = [w.id for w in workspaces]
        if last in ids:
            self.set_workspace(last)
        elif ids:
            self.set_workspace(ids[0])
        else:
            self.set_workspace(None)

    # -- прочее --------------------------------------------------------------
    def _apply_theme(self, theme: str) -> None:
        app = self.window().style().parent() if False else None  # noqa: SIM108
        from PySide6.QtWidgets import QApplication

        QApplication.instance().setStyleSheet(stylesheet(theme))

    def _on_language_changed(self) -> None:
        """Строки страниц берутся при построении, поэтому окно собирается заново.

        Во время прогона пересборка убила бы агентов — тогда язык применится
        при следующем входе.
        """
        if self.orchestrator.state.running:
            from ui.widgets.common import info

            info(self, tr("settings.lang_after_run"))
            return
        self.rebuild_requested.emit(self.stack.currentIndex())

    def select_page(self, index: int) -> None:
        """Открывает страницу по индексу — нужно после пересборки окна."""
        self._select_page(index)

    def closeEvent(self, event) -> None:  # noqa: N802 — сигнатура Qt
        """Корректно гасим фоновые задачи агентов при закрытии окна."""
        if self.orchestrator.state.running:
            self.orchestrator.stop()
        super().closeEvent(event)

    def _logout(self) -> None:
        if self.orchestrator.state.running:
            self.orchestrator.stop()
        self.session.wipe()
        self.logged_out.emit()
        self.close()
````

### `ui/pages/workspaces_page.py`

*204 строк*

````python
"""Этап 1 — страница воркспейсов (параллельных проектов).

Каждый воркспейс полностью изолирован: свой набор агентов, своя задача,
свой рабочий каталог на диске и свои настройки супервайзера.
"""

from __future__ import annotations

import shutil

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.config import DEFAULT_WORKSPACE_SETTINGS, PATHS
from app.i18n import tr
from storage.db import local_time
from storage.models import Workspace
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, confirm


class WorkspaceDialog(QDialog):
    """Диалог создания/переименования воркспейса."""

    def __init__(self, parent: QWidget, workspace: Workspace | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("ws.new"))
        self.setMinimumWidth(440)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        lay.addWidget(QLabel(tr("ws.name")))
        self.name = QLineEdit(workspace.name if workspace else "")
        lay.addWidget(self.name)

        lay.addWidget(QLabel(tr("common.description")))
        self.description = QPlainTextEdit(workspace.description if workspace else "")
        self.description.setFixedHeight(90)
        lay.addWidget(self.description)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def values(self) -> tuple[str, str]:
        return self.name.text().strip(), self.description.toPlainText().strip()


class WorkspaceCard(Card):
    """Карточка одного воркспейса в списке."""

    def __init__(self, parent: QWidget, ws: Workspace, agents: int,
                 is_active: bool, on_select, on_edit, on_delete) -> None:
        super().__init__(parent, spacing=8)
        row = QHBoxLayout()
        texts = QVBoxLayout()
        texts.setSpacing(2)

        title = QLabel(ws.name + ("  ·  " + tr("ws.current") if is_active else ""))
        title.setObjectName("H2")
        texts.addWidget(title)

        meta = QLabel(f"{agents} {tr('ws.agents_count')}  ·  {local_time(ws.updated_at, '%Y-%m-%d %H:%M')}")
        meta.setObjectName("Dim")
        texts.addWidget(meta)

        if ws.description:
            desc = QLabel(ws.description)
            desc.setObjectName("Dim")
            desc.setWordWrap(True)
            texts.addWidget(desc)

        row.addLayout(texts, 1)

        btn_select = QPushButton(tr("ws.select"))
        btn_select.setObjectName("Primary")
        btn_select.setEnabled(not is_active)
        btn_select.clicked.connect(lambda: on_select(ws))
        row.addWidget(btn_select, 0, Qt.AlignmentFlag.AlignTop)

        btn_edit = QPushButton(tr("common.edit"))
        btn_edit.clicked.connect(lambda: on_edit(ws))
        row.addWidget(btn_edit, 0, Qt.AlignmentFlag.AlignTop)

        btn_delete = QPushButton(tr("common.delete"))
        btn_delete.setObjectName("Danger")
        btn_delete.clicked.connect(lambda: on_delete(ws))
        row.addWidget(btn_delete, 0, Qt.AlignmentFlag.AlignTop)

        self.body.addLayout(row)


class WorkspacesPage(QWidget):
    """Список воркспейсов с выбором активного."""

    workspace_selected = Signal(int)
    workspaces_changed = Signal()

    def __init__(self, repos: Repos) -> None:
        super().__init__()
        self.repos = repos
        self.active_id: int | None = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(16)

        self.header = Header(tr("ws.title"))
        btn_new = QPushButton(tr("ws.new"))
        btn_new.setObjectName("Primary")
        btn_new.clicked.connect(self._create)
        self.header.add_action(btn_new)
        lay.addWidget(self.header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        lay.addWidget(self.scroll, 1)

        self.container = QWidget()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        self.scroll.setWidget(self.container)

    # -- отрисовка -----------------------------------------------------------
    def refresh(self) -> None:
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        items = self.repos.workspaces.list(self.repos.session.user_id)
        if not items:
            self.list_layout.addWidget(EmptyState(tr("ws.empty")))
            return
        for ws in items:
            self.list_layout.addWidget(
                WorkspaceCard(
                    self, ws, self.repos.workspaces.agent_count(ws.id),
                    ws.id == self.active_id, self._select, self._edit, self._delete,
                )
            )
        self.list_layout.addStretch(1)

    def set_active(self, ws_id: int | None) -> None:
        self.active_id = ws_id
        self.refresh()

    # -- действия ------------------------------------------------------------
    def _create(self) -> None:
        dlg = WorkspaceDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        name, description = dlg.values()
        if not name:
            return
        ws = self.repos.workspaces.create(
            self.repos.session.user_id, name, description,
            dict(DEFAULT_WORKSPACE_SETTINGS),
        )
        PATHS.workspace_dir(ws.id).mkdir(parents=True, exist_ok=True)
        self.workspaces_changed.emit()
        self._select(ws)

    def _edit(self, ws: Workspace) -> None:
        dlg = WorkspaceDialog(self, ws)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        name, description = dlg.values()
        if name:
            self.repos.workspaces.update(ws.id, name=name, description=description)
            self.workspaces_changed.emit()
            self.refresh()

    def _delete(self, ws: Workspace) -> None:
        if not confirm(self, tr("ws.delete_confirm")):
            return
        self.repos.workspaces.delete(ws.id)
        shutil.rmtree(PATHS.workspace_dir(ws.id), ignore_errors=True)
        if self.active_id == ws.id:
            self.active_id = None
        self.workspaces_changed.emit()
        self.refresh()

    def _select(self, ws: Workspace) -> None:
        self.active_id = ws.id
        PATHS.workspace_dir(ws.id).mkdir(parents=True, exist_ok=True)
        self.workspace_selected.emit(ws.id)
        self.refresh()
````

### `ui/pages/keys_page.py`

*254 строк*

````python
"""Этап 2 — страница API-ключей.

Ключи хранятся зашифрованными (AES-256-GCM на мастер-ключе профиля).
Кнопка «Проверить» делает реальный запрос списка моделей — это заодно
подтверждает, что ключ и base URL рабочие.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from providers.base import ProviderError
from providers.factory import build_provider
from providers.presets import preset, preset_list
from storage.models import ApiKey
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, confirm, info, warn
from utils.asyncutils import run_async


class KeyDialog(QDialog):
    """Создание/редактирование ключа с автоподстановкой base URL из пресета."""

    def __init__(self, parent: QWidget, repos: Repos, key: ApiKey | None = None) -> None:
        super().__init__(parent)
        self.repos = repos
        self.key = key
        self.setWindowTitle(tr("keys.new"))
        self.setMinimumWidth(520)

        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        lay.addWidget(QLabel(tr("keys.provider")))
        self.provider = QComboBox()
        for p in preset_list():
            suffix = []
            if p.free_tier:
                suffix.append("free")
            if p.local:
                suffix.append("local")
            label = p.title + (f"  ({', '.join(suffix)})" if suffix else "")
            self.provider.addItem(label, p.key)
        self.provider.currentIndexChanged.connect(self._on_provider)
        self.provider.setEnabled(key is None)   # провайдер не меняем после создания
        lay.addWidget(self.provider)

        self.notes = QLabel("")
        self.notes.setObjectName("Dim")
        self.notes.setWordWrap(True)
        lay.addWidget(self.notes)

        lay.addWidget(QLabel(tr("keys.label")))
        self.label = QLineEdit(key.label if key else "")
        lay.addWidget(self.label)

        lay.addWidget(QLabel(tr("keys.base_url")))
        self.base_url = QLineEdit(key.base_url if key else "")
        lay.addWidget(self.base_url)

        self.key_label = QLabel(tr("keys.key"))
        lay.addWidget(self.key_label)
        self.secret = QLineEdit()
        self.secret.setEchoMode(QLineEdit.EchoMode.Password)
        self.secret.setPlaceholderText("sk-..." if key is None else "оставьте пустым, чтобы не менять")
        lay.addWidget(self.secret)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

        if key is not None:
            idx = self.provider.findData(key.provider)
            if idx >= 0:
                self.provider.setCurrentIndex(idx)
        self._on_provider()

    def _on_provider(self) -> None:
        p = preset(self.provider.currentData())
        if self.key is None:
            self.base_url.setText(p.base_url)
            if not self.label.text():
                self.label.setText(p.title)
        self.secret.setEnabled(p.requires_key or p.key == "custom")
        hint = p.notes
        if not p.requires_key:
            hint = (hint + " " if hint else "") + tr("keys.no_key_needed")
        if p.docs_url:
            hint = (hint + "  " if hint else "") + p.docs_url
        self.notes.setText(hint)

    def values(self) -> tuple[str, str, str, str]:
        return (
            self.provider.currentData(),
            self.label.text().strip() or preset(self.provider.currentData()).title,
            self.base_url.text().strip(),
            self.secret.text().strip(),
        )


class KeysPage(QWidget):
    """Список ключей пользователя (общий для всех воркспейсов)."""

    keys_changed = Signal()

    def __init__(self, repos: Repos) -> None:
        super().__init__()
        self.repos = repos

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(16)

        self.header = Header(tr("keys.title"), tr("keys.subtitle"))
        btn_new = QPushButton(tr("keys.new"))
        btn_new.setObjectName("Primary")
        btn_new.clicked.connect(self._create)
        self.header.add_action(btn_new)
        lay.addWidget(self.header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        lay.addWidget(self.scroll, 1)

        self.container = QWidget()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        self.scroll.setWidget(self.container)

    def refresh(self) -> None:
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        keys = self.repos.keys.list()
        if not keys:
            self.list_layout.addWidget(EmptyState(tr("keys.empty")))
            return
        for key in keys:
            self.list_layout.addWidget(self._build_card(key))
        self.list_layout.addStretch(1)

    def _build_card(self, key: ApiKey) -> Card:
        p = preset(key.provider)
        card = Card(self, spacing=8)
        row = QHBoxLayout()

        texts = QVBoxLayout()
        texts.setSpacing(2)
        title = QLabel(f"{key.label}")
        title.setObjectName("H2")
        texts.addWidget(title)
        meta = QLabel(f"{p.title}  ·  {key.base_url or p.base_url or '—'}  ·  "
                      + ("ключ сохранён" if key.has_secret else "без ключа"))
        meta.setObjectName("Dim")
        texts.addWidget(meta)
        status = QLabel("")
        status.setObjectName("Dim")
        status.setWordWrap(True)
        texts.addWidget(status)
        row.addLayout(texts, 1)

        btn_test = QPushButton(tr("common.test"))
        btn_test.clicked.connect(lambda: self._test(key, btn_test, status))
        row.addWidget(btn_test, 0, Qt.AlignmentFlag.AlignTop)

        btn_edit = QPushButton(tr("common.edit"))
        btn_edit.clicked.connect(lambda: self._edit(key))
        row.addWidget(btn_edit, 0, Qt.AlignmentFlag.AlignTop)

        btn_del = QPushButton(tr("common.delete"))
        btn_del.setObjectName("Danger")
        btn_del.clicked.connect(lambda: self._delete(key))
        row.addWidget(btn_del, 0, Qt.AlignmentFlag.AlignTop)

        card.body.addLayout(row)
        return card

    # -- действия ------------------------------------------------------------
    def _create(self) -> None:
        dlg = KeyDialog(self, self.repos)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        provider, label, base_url, secret = dlg.values()
        p = preset(provider)
        if p.requires_key and not secret:
            warn(self, tr("keys.key"))
            return
        self.repos.keys.create(label, provider, secret, base_url)
        self.keys_changed.emit()
        self.refresh()

    def _edit(self, key: ApiKey) -> None:
        dlg = KeyDialog(self, self.repos, key)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        _, label, base_url, secret = dlg.values()
        self.repos.keys.update(key.id, label, base_url, secret if secret else None)
        self.keys_changed.emit()
        self.refresh()

    def _delete(self, key: ApiKey) -> None:
        if not confirm(self, tr("keys.delete_confirm")):
            return
        self.repos.keys.delete(key.id)
        self.keys_changed.emit()
        self.refresh()

    def _test(self, key: ApiKey, button: QPushButton, status: QLabel) -> None:
        """Асинхронная проверка соединения без блокировки интерфейса."""
        button.setEnabled(False)
        status.setText("…")

        async def job() -> list[str]:
            secret = self.repos.keys.reveal(key.id)
            provider = build_provider(key.provider, secret, key.base_url, timeout=20)
            try:
                return await provider.test()
            finally:
                await provider.aclose()

        def done(models: list[str]) -> None:
            button.setEnabled(True)
            status.setText(tr("keys.test_ok", n=len(models)))
            meta = dict(key.meta)
            meta["models"] = models[:300]   # кэш для выпадающего списка в агентах
            self.repos.keys.update(key.id, key.label, key.base_url, None, meta)
            self.keys_changed.emit()

        def failed(exc: Exception) -> None:
            button.setEnabled(True)
            message = str(exc) if isinstance(exc, ProviderError) else f"{type(exc).__name__}: {exc}"
            status.setText(tr("keys.test_fail", err=message))

        run_async(job(), done, failed)
````

### `ui/pages/agents_page.py`

*384 строк*

````python
"""Этап 2 — страница агентов воркспейса.

Количество агентов не ограничено: список прокручивается, а карточки
компактны, поэтому 2 агента и 15+ агентов выглядят одинаково опрятно.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.i18n import current_language, tr
from core.agents.roles import COMMON_RULES, TEMPLATES, by_key, title as role_title
from core.tools.base import default_registry, expand_tool_names
from providers.base import ProviderError
from providers.factory import build_provider
from providers.presets import preset
from storage.models import Agent
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, StatusBadge, confirm, warn
from utils.asyncutils import run_async


class AgentDialog(QDialog):
    """Форма создания/редактирования агента."""

    def __init__(self, parent: QWidget, repos: Repos, agent: Agent | None = None) -> None:
        super().__init__(parent)
        self.repos = repos
        self.agent = agent
        self.setWindowTitle(tr("agents.new"))
        self.setMinimumSize(620, 700)

        root = QVBoxLayout(self)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        lay = QVBoxLayout(page)
        lay.setSpacing(10)

        lay.addWidget(QLabel(tr("agents.name")))
        self.name = QLineEdit(agent.name if agent else "")
        lay.addWidget(self.name)
        #: имя, подставленное из шаблона; пока пользователь его не менял,
        #: смена шаблона меняет и имя
        self._auto_name = ""
        self._auto_prompt = ""

        lay.addWidget(QLabel(tr("agents.template")))
        self.template = QComboBox()
        lang = current_language()
        for t in TEMPLATES:
            self.template.addItem(role_title(t, lang), t.key)
        self.template.currentIndexChanged.connect(self._apply_template)
        lay.addWidget(self.template)

        lay.addWidget(QLabel(tr("agents.provider_key")))
        self.key_box = QComboBox()
        self.keys = self.repos.keys.list()
        for k in self.keys:
            self.key_box.addItem(f"{k.label} — {preset(k.provider).title}", k.id)
        self.key_box.currentIndexChanged.connect(self._on_key_changed)
        lay.addWidget(self.key_box)

        model_row = QHBoxLayout()
        model_col = QVBoxLayout()
        model_col.addWidget(QLabel(tr("agents.model")))
        self.model = QComboBox()
        self.model.setEditable(True)   # можно вписать модель вручную
        model_col.addWidget(self.model)
        model_row.addLayout(model_col, 1)
        self.btn_models = QPushButton(tr("agents.load_models"))
        self.btn_models.clicked.connect(self._load_models)
        model_row.addWidget(self.btn_models, 0, Qt.AlignmentFlag.AlignBottom)
        lay.addLayout(model_row)

        params_row = QHBoxLayout()
        temp_col = QVBoxLayout()
        temp_col.addWidget(QLabel(tr("agents.temperature")))
        self.temperature = QDoubleSpinBox()
        self.temperature.setRange(0.0, 2.0)
        self.temperature.setSingleStep(0.1)
        self.temperature.setValue(agent.temperature if agent else 0.7)
        temp_col.addWidget(self.temperature)
        params_row.addLayout(temp_col)

        tok_col = QVBoxLayout()
        tok_col.addWidget(QLabel(tr("agents.max_tokens")))
        self.max_tokens = QSpinBox()
        self.max_tokens.setRange(256, 32768)
        self.max_tokens.setSingleStep(256)
        self.max_tokens.setValue(agent.max_tokens if agent else 2048)
        tok_col.addWidget(self.max_tokens)
        params_row.addLayout(tok_col)
        lay.addLayout(params_row)

        lay.addWidget(QLabel("Инструменты"))
        tools_row = QHBoxLayout()
        self.tool_boxes: dict[str, QCheckBox] = {}
        enabled_tools = set(expand_tool_names(agent.tools)) if agent else set()
        for tool_name in default_registry().names():
            box = QCheckBox(tool_name)
            box.setChecked(tool_name in enabled_tools)
            self.tool_boxes[tool_name] = box
            tools_row.addWidget(box)
        tools_row.addStretch(1)
        lay.addLayout(tools_row)

        lay.addWidget(QLabel(tr("agents.prompt")))
        self.prompt = QPlainTextEdit(agent.system_prompt if agent else "")
        self.prompt.setMinimumHeight(180)
        lay.addWidget(self.prompt)

        note = QLabel(tr("agents.isolated_note"))
        note.setObjectName("Dim")
        note.setWordWrap(True)
        lay.addWidget(note)

        self.is_supervisor = QCheckBox(tr("settings.supervisor"))
        self.is_supervisor.setChecked(agent.is_supervisor if agent else False)
        lay.addWidget(self.is_supervisor)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        root.addWidget(buttons)

        if agent is not None:
            idx = self.template.findData(agent.role or "custom")
            self.template.blockSignals(True)
            self.template.setCurrentIndex(max(0, idx))
            self.template.blockSignals(False)
            idx = self.key_box.findData(agent.api_key_id)
            if idx >= 0:
                self.key_box.setCurrentIndex(idx)
            self._on_key_changed()
            self.model.setCurrentText(agent.model)
        else:
            self._apply_template()
            self._on_key_changed()

    # -- реакции -------------------------------------------------------------
    def _apply_template(self) -> None:
        template = by_key(self.template.currentData())
        # Промпт, который пользователь успел поправить руками, не затираем.
        prompt = self.prompt.toPlainText().strip()
        if template.prompt and (not prompt or prompt == self._auto_prompt):
            self._auto_prompt = template.prompt + "\n\n" + COMMON_RULES.strip()
            self.prompt.setPlainText(self._auto_prompt)
        current = self.name.text().strip()
        if not current or current == self._auto_name:
            self._auto_name = role_title(template, current_language())
            self.name.setText(self._auto_name)
        suggested = expand_tool_names(template.suggested_tools)
        for name, box in self.tool_boxes.items():
            box.setChecked(name in suggested)

    def _on_key_changed(self) -> None:
        """Подставляет в список моделей кэш последней проверки или пресет."""
        key_id = self.key_box.currentData()
        key = next((k for k in self.keys if k.id == key_id), None)
        if key is None:
            return
        current = self.model.currentText()
        cached = key.meta.get("models") or []
        models = cached or preset(key.provider).suggested_models
        self.model.clear()
        self.model.addItems(models)
        if current:
            self.model.setCurrentText(current)
        elif models:
            self.model.setCurrentIndex(0)

    def _load_models(self) -> None:
        key_id = self.key_box.currentData()
        key = next((k for k in self.keys if k.id == key_id), None)
        if key is None:
            return
        self.btn_models.setEnabled(False)

        async def job() -> list[str]:
            secret = self.repos.keys.reveal(key.id)
            provider = build_provider(key.provider, secret, key.base_url, timeout=20)
            try:
                return await provider.list_models()
            finally:
                await provider.aclose()

        def done(models: list[str]) -> None:
            self.btn_models.setEnabled(True)
            current = self.model.currentText()
            self.model.clear()
            self.model.addItems(models)
            if current:
                self.model.setCurrentText(current)
            meta = dict(key.meta)
            meta["models"] = models[:300]
            self.repos.keys.update(key.id, key.label, key.base_url, None, meta)

        def failed(exc: Exception) -> None:
            self.btn_models.setEnabled(True)
            message = str(exc) if isinstance(exc, ProviderError) else f"{type(exc).__name__}: {exc}"
            warn(self, tr("keys.test_fail", err=message))

        run_async(job(), done, failed)

    def values(self) -> dict:
        key_id = self.key_box.currentData()
        key = next((k for k in self.keys if k.id == key_id), None)
        return {
            "name": self.name.text().strip(),
            "role": self.template.currentData(),
            "system_prompt": self.prompt.toPlainText().strip(),
            "api_key_id": key_id,
            "provider": key.provider if key else "",
            "model": self.model.currentText().strip(),
            "params": {
                "temperature": self.temperature.value(),
                "max_tokens": self.max_tokens.value(),
                "tools": [n for n, b in self.tool_boxes.items() if b.isChecked()],
            },
            "is_supervisor": self.is_supervisor.isChecked(),
        }


class AgentsPage(QWidget):
    """Список агентов текущего воркспейса."""

    agents_changed = Signal()

    def __init__(self, repos: Repos) -> None:
        super().__init__()
        self.repos = repos
        self.workspace_id: int | None = None

        lay = QVBoxLayout(self)
        lay.setContentsMargins(24, 24, 24, 24)
        lay.setSpacing(16)

        self.header = Header(tr("agents.title"), tr("agents.isolated_note"))
        self.btn_new = QPushButton(tr("agents.new"))
        self.btn_new.setObjectName("Primary")
        self.btn_new.clicked.connect(self._create)
        self.header.add_action(self.btn_new)
        lay.addWidget(self.header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        lay.addWidget(self.scroll, 1)

        self.container = QWidget()
        self.list_layout = QVBoxLayout(self.container)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(10)
        self.scroll.setWidget(self.container)

    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        while self.list_layout.count():
            item = self.list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.workspace_id is None:
            self.btn_new.setEnabled(False)
            self.list_layout.addWidget(EmptyState(tr("ws.empty")))
            return
        self.btn_new.setEnabled(True)

        if not self.repos.keys.list():
            self.list_layout.addWidget(EmptyState(tr("agents.no_keys")))
            return

        agents = self.repos.agents.list(self.workspace_id)
        if not agents:
            self.list_layout.addWidget(EmptyState(tr("agents.empty")))
            return
        for agent in agents:
            self.list_layout.addWidget(self._build_card(agent))
        self.list_layout.addStretch(1)

    def _build_card(self, agent: Agent) -> Card:
        card = Card(self, spacing=6)
        row = QHBoxLayout()

        texts = QVBoxLayout()
        texts.setSpacing(2)
        head = QHBoxLayout()
        name = QLabel(agent.name + ("  ⭐" if agent.is_supervisor else ""))
        name.setObjectName("H2")
        head.addWidget(name)
        head.addWidget(StatusBadge(agent.status))
        head.addStretch(1)
        texts.addLayout(head)

        p = preset(agent.provider)
        meta = QLabel(f"{role_title(by_key(agent.role), current_language())}  ·  "
                      f"{p.title}  ·  {agent.model or '—'}"
                      f"  ·  T={agent.temperature}  ·  max={agent.max_tokens}")
        meta.setObjectName("Dim")
        texts.addWidget(meta)

        if agent.tools:
            tools = QLabel("Инструменты: " + ", ".join(agent.tools))
            tools.setObjectName("Dim")
            texts.addWidget(tools)

        prompt_preview = agent.system_prompt.replace("\n", " ")[:160]
        if prompt_preview:
            preview = QLabel(prompt_preview + ("…" if len(agent.system_prompt) > 160 else ""))
            preview.setObjectName("Dim")
            preview.setWordWrap(True)
            texts.addWidget(preview)

        row.addLayout(texts, 1)

        btn_edit = QPushButton(tr("common.edit"))
        btn_edit.clicked.connect(lambda: self._edit(agent))
        row.addWidget(btn_edit, 0, Qt.AlignmentFlag.AlignTop)

        btn_del = QPushButton(tr("common.delete"))
        btn_del.setObjectName("Danger")
        btn_del.clicked.connect(lambda: self._delete(agent))
        row.addWidget(btn_del, 0, Qt.AlignmentFlag.AlignTop)

        card.body.addLayout(row)
        return card

    # -- действия ------------------------------------------------------------
    def _create(self) -> None:
        if self.workspace_id is None:
            return
        if not self.repos.keys.list():
            warn(self, tr("agents.no_keys"))
            return
        dlg = AgentDialog(self, self.repos)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        data = dlg.values()
        if not data["name"] or not data["model"]:
            warn(self, tr("agents.model"))
            return
        self.repos.agents.create(self.workspace_id, **data)
        self.agents_changed.emit()
        self.refresh()

    def _edit(self, agent: Agent) -> None:
        dlg = AgentDialog(self, self.repos, agent)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        self.repos.agents.update(agent.id, **dlg.values())
        self.agents_changed.emit()
        self.refresh()

    def _delete(self, agent: Agent) -> None:
        if not confirm(self, tr("agents.delete_confirm")):
            return
        self.repos.agents.delete(agent.id)
        self.agents_changed.emit()
        self.refresh()
````

### `ui/pages/task_page.py`

*394 строк*

````python
"""Этап 3 — постановка задачи и разбиение на подзадачи.

Здесь пользователь формулирует общую задачу воркспейса, задаёт лимит токенов
(пусто = без лимита, ответ на вопрос 7), выбирает формат результата и
раскладывает работу на подзадачи — руками или автоматически через ИИ.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from core.planner import match_agent_by_role, plan_subtasks
from storage.models import Subtask, Task
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, StatusBadge, confirm, warn
from utils.asyncutils import run_async

RESULT_FORMATS = [
    ("auto", "Определить автоматически"),
    ("markdown", "Markdown-документ"),
    ("docx", "Документ DOCX"),
    ("pdf", "Документ PDF"),
    ("zip", "ZIP-архив с файлами/кодом"),
]


class SubtaskDialog(QDialog):
    """Ручное создание/редактирование подзадачи и назначение исполнителя."""

    def __init__(self, parent: QWidget, repos: Repos, workspace_id: int,
                 subtask: Subtask | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("task.add_subtask"))
        self.setMinimumWidth(560)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        lay.addWidget(QLabel(tr("task.subtask_title")))
        self.title = QLineEdit(subtask.title if subtask else "")
        lay.addWidget(self.title)

        lay.addWidget(QLabel(tr("common.description")))
        self.description = QPlainTextEdit(subtask.description if subtask else "")
        self.description.setMinimumHeight(140)
        lay.addWidget(self.description)

        lay.addWidget(QLabel(tr("task.assignee")))
        self.assignee = QComboBox()
        self.assignee.addItem(tr("task.unassigned"), None)
        for agent in repos.agents.list(workspace_id):
            if not agent.is_supervisor:
                self.assignee.addItem(f"{agent.name} — {agent.model}", agent.id)
        if subtask and subtask.agent_id:
            idx = self.assignee.findData(subtask.agent_id)
            if idx >= 0:
                self.assignee.setCurrentIndex(idx)
        lay.addWidget(self.assignee)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def values(self) -> tuple[str, str, int | None]:
        return (self.title.text().strip(),
                self.description.toPlainText().strip(),
                self.assignee.currentData())


class TaskPage(QWidget):
    """Страница задачи текущего воркспейса."""

    task_changed = Signal()
    run_requested = Signal()   # пользователь нажал «Запустить агентов»

    def __init__(self, repos: Repos) -> None:
        super().__init__()
        self.repos = repos
        self.workspace_id: int | None = None
        self.task: Task | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)

        self.header = Header(tr("task.title"))
        root.addWidget(self.header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        # --- карточка постановки задачи ---
        self.task_card = Card(self)
        lay.addWidget(self.task_card)

        self.task_card.body.addWidget(QLabel(tr("task.name")))
        self.title_edit = QLineEdit()
        self.task_card.body.addWidget(self.title_edit)

        self.task_card.body.addWidget(QLabel(tr("task.body")))
        self.body_edit = QPlainTextEdit()
        self.body_edit.setPlaceholderText(tr("task.placeholder"))
        self.body_edit.setMinimumHeight(220)
        self.task_card.body.addWidget(self.body_edit)

        options = QHBoxLayout()
        fmt_col = QVBoxLayout()
        fmt_col.addWidget(QLabel(tr("task.result_format")))
        self.format_box = QComboBox()
        for key, label in RESULT_FORMATS:
            self.format_box.addItem(label, key)
        fmt_col.addWidget(self.format_box)
        options.addLayout(fmt_col, 1)

        limit_col = QVBoxLayout()
        limit_col.addWidget(QLabel(tr("task.token_limit")))
        self.token_limit = QLineEdit()
        self.token_limit.setPlaceholderText(tr("task.token_limit_hint"))
        limit_col.addWidget(self.token_limit)
        options.addLayout(limit_col, 1)
        self.task_card.body.addLayout(options)

        buttons = QHBoxLayout()
        self.btn_save = QPushButton(tr("task.save"))
        self.btn_save.setObjectName("Primary")
        self.btn_save.clicked.connect(self._save_task)
        buttons.addWidget(self.btn_save)

        self.btn_run = QPushButton(tr("task.run"))
        self.btn_run.clicked.connect(self._request_run)
        buttons.addWidget(self.btn_run)
        buttons.addStretch(1)
        self.task_card.body.addLayout(buttons)

        # --- карточка подзадач ---
        self.subtasks_header = Header(tr("task.subtasks"))
        self.btn_add = QPushButton(tr("task.add_subtask"))
        self.btn_add.clicked.connect(self._add_subtask)
        self.subtasks_header.add_action(self.btn_add)
        self.btn_auto = QPushButton(tr("task.autosplit"))
        self.btn_auto.setObjectName("Primary")
        self.btn_auto.clicked.connect(self._autosplit)
        self.subtasks_header.add_action(self.btn_auto)
        lay.addWidget(self.subtasks_header)

        self.subtasks_box = QWidget()
        self.subtasks_layout = QVBoxLayout(self.subtasks_box)
        self.subtasks_layout.setContentsMargins(0, 0, 0, 0)
        self.subtasks_layout.setSpacing(8)
        lay.addWidget(self.subtasks_box)
        lay.addStretch(1)

    # -- загрузка ------------------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        enabled = self.workspace_id is not None
        for widget in (self.title_edit, self.body_edit, self.format_box,
                       self.token_limit, self.btn_save, self.btn_add,
                       self.btn_auto, self.btn_run):
            widget.setEnabled(enabled)
        if not enabled:
            self._clear_subtasks()
            self.subtasks_layout.addWidget(EmptyState(tr("ws.empty")))
            return

        self.task = self.repos.tasks.current(self.workspace_id)
        if self.task:
            self.title_edit.setText(self.task.title)
            self.body_edit.setPlainText(self.task.description)
            idx = self.format_box.findData(self.task.result_format)
            self.format_box.setCurrentIndex(max(0, idx))
            self.token_limit.setText(str(self.task.token_limit) if self.task.token_limit else "")
        else:
            self.title_edit.clear()
            self.body_edit.clear()
            self.format_box.setCurrentIndex(0)
            self.token_limit.clear()
        self._render_subtasks()

    def _clear_subtasks(self) -> None:
        while self.subtasks_layout.count():
            item = self.subtasks_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _render_subtasks(self) -> None:
        self._clear_subtasks()
        if self.task is None:
            self.subtasks_layout.addWidget(EmptyState(tr("task.no_task")))
            return
        items = self.repos.tasks.subtasks(self.task.id)
        if not items:
            self.subtasks_layout.addWidget(EmptyState(tr("task.subtasks")))
            return
        agents = {a.id: a for a in self.repos.agents.list(self.workspace_id)}
        for position, st in enumerate(items):
            self.subtasks_layout.addWidget(
                self._build_subtask_card(st, position, len(items), agents)
            )

    def _build_subtask_card(self, st: Subtask, position: int, total: int,
                            agents: dict) -> Card:
        card = Card(self, spacing=6)
        row = QHBoxLayout()

        texts = QVBoxLayout()
        texts.setSpacing(2)
        head = QHBoxLayout()
        title = QLabel(f"{position + 1}. {st.title}")
        title.setObjectName("H2")
        title.setWordWrap(True)
        head.addWidget(title, 1)
        head.addWidget(StatusBadge(st.status))
        texts.addLayout(head)

        agent = agents.get(st.agent_id)
        meta = QLabel(f"{tr('task.assignee')}: "
                      f"{agent.name if agent else tr('task.unassigned')}")
        meta.setObjectName("Dim")
        texts.addWidget(meta)

        if st.description:
            desc = QLabel(st.description[:300] + ("…" if len(st.description) > 300 else ""))
            desc.setObjectName("Dim")
            desc.setWordWrap(True)
            texts.addWidget(desc)
        row.addLayout(texts, 1)

        controls = QVBoxLayout()
        controls.setSpacing(4)
        move_row = QHBoxLayout()
        btn_up = QPushButton("▲")
        btn_up.setObjectName("Icon")
        btn_up.setFixedWidth(36)
        btn_up.setEnabled(position > 0)
        btn_up.clicked.connect(lambda: self._move(st.id, -1))
        move_row.addWidget(btn_up)
        btn_down = QPushButton("▼")
        btn_down.setObjectName("Icon")
        btn_down.setFixedWidth(36)
        btn_down.setEnabled(position < total - 1)
        btn_down.clicked.connect(lambda: self._move(st.id, +1))
        move_row.addWidget(btn_down)
        controls.addLayout(move_row)

        btn_edit = QPushButton(tr("common.edit"))
        btn_edit.clicked.connect(lambda: self._edit_subtask(st))
        controls.addWidget(btn_edit)

        btn_del = QPushButton(tr("common.delete"))
        btn_del.setObjectName("Danger")
        btn_del.clicked.connect(lambda: self._delete_subtask(st))
        controls.addWidget(btn_del)

        row.addLayout(controls, 0)
        card.body.addLayout(row)
        return card

    # -- действия ------------------------------------------------------------
    def _parse_limit(self) -> int | None:
        raw = self.token_limit.text().strip()
        if not raw:
            return None       # пусто = лимита нет
        try:
            value = int(raw.replace(" ", ""))
            return value if value > 0 else None
        except ValueError:
            return None

    def _save_task(self) -> bool:
        if self.workspace_id is None:
            return False
        title = self.title_edit.text().strip() or "Без названия"
        body = self.body_edit.toPlainText().strip()
        if not body:
            warn(self, tr("task.placeholder"))
            return False
        fmt = self.format_box.currentData()
        limit = self._parse_limit()
        if self.task is None:
            self.task = self.repos.tasks.create(self.workspace_id, title, body, fmt, limit)
        else:
            self.repos.tasks.update(self.task.id, title=title, description=body,
                                    result_format=fmt, token_limit=limit)
            self.task = self.repos.tasks.get(self.task.id)
        self.task_changed.emit()
        self._render_subtasks()
        return True

    def _add_subtask(self) -> None:
        if self.task is None and not self._save_task():
            return
        dlg = SubtaskDialog(self, self.repos, self.workspace_id)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        title, description, agent_id = dlg.values()
        if not title:
            return
        self.repos.tasks.add_subtask(self.task.id, title, description, agent_id)
        self.task_changed.emit()
        self._render_subtasks()

    def _edit_subtask(self, st: Subtask) -> None:
        dlg = SubtaskDialog(self, self.repos, self.workspace_id, st)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        title, description, agent_id = dlg.values()
        if not title:
            return
        self.repos.tasks.update_subtask(st.id, title=title, description=description,
                                        agent_id=agent_id)
        self.task_changed.emit()
        self._render_subtasks()

    def _delete_subtask(self, st: Subtask) -> None:
        if not confirm(self, tr("common.delete") + "?"):
            return
        self.repos.tasks.delete_subtask(st.id)
        self.task_changed.emit()
        self._render_subtasks()

    def _move(self, subtask_id: int, delta: int) -> None:
        if self.task is None:
            return
        ids = [s.id for s in self.repos.tasks.subtasks(self.task.id)]
        i = ids.index(subtask_id)
        j = i + delta
        if 0 <= j < len(ids):
            ids[i], ids[j] = ids[j], ids[i]
            self.repos.tasks.reorder(ids)
            self._render_subtasks()

    def _autosplit(self) -> None:
        """Просит ИИ разбить задачу и сразу назначает исполнителей по ролям."""
        if not self._save_task() or self.task is None:
            return
        self.btn_auto.setEnabled(False)
        self.btn_auto.setText("…")

        task_id = self.task.id
        ws_id = self.workspace_id
        title, body = self.task.title, self.task.description

        async def job():
            return await plan_subtasks(self.repos, ws_id, title, body)

        def done(planned) -> None:
            self._reset_auto_button()
            for item in planned:
                agent_id = match_agent_by_role(self.repos, ws_id, item.assignee_role)
                self.repos.tasks.add_subtask(task_id, item.title, item.description, agent_id)
            self.task_changed.emit()
            self._render_subtasks()

        def failed(exc: Exception) -> None:
            self._reset_auto_button()
            warn(self, str(exc))

        run_async(job(), done, failed)

    def _request_run(self) -> None:
        """Сохраняет задачу и передаёт управление странице выполнения."""
        if self._save_task():
            self.run_requested.emit()

    def _reset_auto_button(self) -> None:
        self.btn_auto.setEnabled(True)
        self.btn_auto.setText(tr("task.autosplit"))
````

### `ui/pages/run_page.py`

*354 строк*

````python
"""Этап 4 — страница выполнения: запуск агентов и наблюдение в реальном времени.

Слева — прогресс по подзадачам и статусы агентов, справа — лента событий:
шаги рассуждений, вызовы инструментов, отчёты, расход токенов.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from core.events import Event, EventBus, EventType
from core.hitl import Decision
from core.orchestrator import Orchestrator
from storage.repositories import Repos
from ui.theme import STATUS_COLORS, current_palette
from ui.widgets.approval_panel import ApprovalPanel
from ui.widgets.common import Card, EmptyState, Header, StatusBadge, confirm, warn
from utils.asyncutils import run_async

#: цвет строки в ленте для каждого типа события
FEED_COLORS = {
    EventType.RUN_STARTED: "#6c8cff",
    EventType.RUN_FINISHED: "#3ecf8e",
    EventType.RUN_PAUSED: "#f0b429",
    EventType.RUN_RESUMED: "#6c8cff",
    EventType.RUN_STOPPED: "#f0b429",
    EventType.AGENT_THINKING: "#99a1b3",
    EventType.AGENT_TOOL_CALL: "#b07cff",
    EventType.AGENT_TOOL_RESULT: "#7c8aa5",
    EventType.SUBTASK_STARTED: "#6c8cff",
    EventType.SUBTASK_FINISHED: "#3ecf8e",
    EventType.SUBTASK_FAILED: "#ef5f6b",
    EventType.REPORT_CREATED: "#3ecf8e",
    EventType.SUMMARY_CREATED: "#b07cff",
    EventType.INCIDENT_CREATED: "#ef5f6b",
    EventType.USAGE: "#5f6a7d",
    EventType.ERROR: "#ef5f6b",
}

#: события, которые не засоряют ленту при большом числе агентов
QUIET_EVENTS = {EventType.AGENT_STATUS}


class RunPage(QWidget):
    """Управление прогоном и живая телеметрия."""

    def __init__(self, repos: Repos, bus: EventBus, orchestrator: Orchestrator) -> None:
        super().__init__()
        self.repos = repos
        self.bus = bus
        self.orchestrator = orchestrator
        self.workspace_id: int | None = None
        self._feed_lines = 0

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        self.header = Header(tr("run.title"), tr("run.subtitle"))
        self.btn_start = QPushButton(tr("run.start"))
        self.btn_start.setObjectName("Primary")
        self.btn_start.clicked.connect(self._start)
        self.header.add_action(self.btn_start)

        self.btn_pause = QPushButton(tr("run.pause"))
        self.btn_pause.clicked.connect(self._toggle_pause)
        self.btn_pause.setEnabled(False)
        self.header.add_action(self.btn_pause)

        self.btn_stop = QPushButton(tr("run.stop"))
        self.btn_stop.setObjectName("Danger")
        self.btn_stop.clicked.connect(self._stop)
        self.btn_stop.setEnabled(False)
        self.header.add_action(self.btn_stop)
        root.addWidget(self.header)

        # --- полоса прогресса и счётчики ---
        top = Card(self, spacing=8)
        self.progress = QProgressBar()
        self.progress.setTextVisible(False)
        top.body.addWidget(self.progress)
        self.summary_label = QLabel(tr("run.idle"))
        self.summary_label.setObjectName("Dim")
        top.body.addWidget(self.summary_label)
        root.addWidget(top)

        # --- запросы решений (human-in-the-loop) ---
        self.approvals = ApprovalPanel(self._decide)
        root.addWidget(self.approvals)

        # --- две колонки ---
        splitter = QSplitter(Qt.Orientation.Horizontal)
        root.addWidget(splitter, 1)

        left = QWidget()
        left_lay = QVBoxLayout(left)
        left_lay.setContentsMargins(0, 0, 0, 0)
        left_lay.setSpacing(10)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        left_lay.addWidget(self.scroll, 1)
        self.panel = QWidget()
        self.panel_layout = QVBoxLayout(self.panel)
        self.panel_layout.setContentsMargins(0, 0, 0, 0)
        self.panel_layout.setSpacing(8)
        self.scroll.setWidget(self.panel)
        splitter.addWidget(left)

        right = QWidget()
        right_lay = QVBoxLayout(right)
        right_lay.setContentsMargins(0, 0, 0, 0)
        right_lay.setSpacing(8)
        feed_head = QHBoxLayout()
        feed_title = QLabel(tr("run.feed"))
        feed_title.setObjectName("H2")
        feed_head.addWidget(feed_title, 1)
        btn_clear = QPushButton(tr("run.clear_feed"))
        btn_clear.clicked.connect(lambda: (self.feed.clear(),
                                           setattr(self, "_feed_lines", 0)))
        feed_head.addWidget(btn_clear)
        right_lay.addLayout(feed_head)

        self.feed = QTextEdit()
        self.feed.setReadOnly(True)
        self.feed.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        right_lay.addWidget(self.feed, 1)
        splitter.addWidget(right)
        splitter.setSizes([520, 620])

        self.bus.subscribe(self._on_event)

    # -- данные --------------------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        self._clear_panel()
        running = self.orchestrator.state.running
        has_ws = self.workspace_id is not None
        self.btn_start.setEnabled(has_ws and not running)
        self.btn_pause.setEnabled(running)
        self.btn_stop.setEnabled(running)

        if not has_ws:
            self.panel_layout.addWidget(EmptyState(tr("ws.empty")))
            return

        task = self.repos.tasks.current(self.workspace_id)
        if task is None:
            self.panel_layout.addWidget(EmptyState(tr("task.no_task")))
            self.btn_start.setEnabled(False)
            return

        subtasks = self.repos.tasks.subtasks(task.id)
        agents = {a.id: a for a in self.repos.agents.list(self.workspace_id)}
        done = sum(1 for s in subtasks if s.status == "done")
        review = sum(1 for s in subtasks if s.status == "review")
        errors = sum(1 for s in subtasks if s.status == "error")
        total = len(subtasks) or 1
        self.progress.setMaximum(total)
        self.progress.setValue(done + review)

        tokens, cost = self.repos.budgets.workspace_totals(self.workspace_id)
        limit = f" / {task.token_limit}" if task.token_limit else " (без лимита)"
        self.summary_label.setText(
            tr("run.summary", done=done + review, total=len(subtasks), errors=errors)
            + f"  ·  {tokens}{limit} токенов  ·  ~${cost:.4f}"
        )

        # --- подзадачи ---
        head = QLabel(tr("task.subtasks"))
        head.setObjectName("H2")
        self.panel_layout.addWidget(head)
        if not subtasks:
            self.panel_layout.addWidget(EmptyState(tr("run.no_subtasks")))
        for i, st in enumerate(subtasks, 1):
            self.panel_layout.addWidget(self._subtask_row(i, st, agents))

        # --- агенты ---
        head2 = QLabel(tr("agents.title"))
        head2.setObjectName("H2")
        self.panel_layout.addWidget(head2)
        for agent in agents.values():
            row = QWidget()
            h = QHBoxLayout(row)
            h.setContentsMargins(4, 2, 4, 2)
            name = QLabel(agent.name + ("  ⭐" if agent.is_supervisor else ""))
            h.addWidget(name, 1)
            model = QLabel(agent.model)
            model.setObjectName("Dim")
            h.addWidget(model)
            h.addWidget(StatusBadge(agent.status))
            self.panel_layout.addWidget(row)
        self.panel_layout.addStretch(1)

    def _subtask_row(self, index: int, st, agents: dict) -> Card:
        card = Card(self, spacing=4)
        row = QHBoxLayout()
        texts = QVBoxLayout()
        texts.setSpacing(2)

        title = QLabel(f"{index}. {st.title}")
        title.setWordWrap(True)
        texts.addWidget(title)

        agent = agents.get(st.agent_id)
        meta = QLabel(f"{agent.name if agent else tr('task.unassigned')}"
                      f"  ·  {st.tokens_in + st.tokens_out} токенов"
                      f"  ·  ~${st.cost_usd:.4f}")
        meta.setObjectName("Dim")
        texts.addWidget(meta)

        if st.result:
            preview = QLabel(st.result[:200].replace("\n", " ")
                             + ("…" if len(st.result) > 200 else ""))
            preview.setObjectName("Dim")
            preview.setWordWrap(True)
            texts.addWidget(preview)

        row.addLayout(texts, 1)
        row.addWidget(StatusBadge(st.status), 0, Qt.AlignmentFlag.AlignTop)
        card.body.addLayout(row)
        return card

    def _clear_panel(self) -> None:
        while self.panel_layout.count():
            item = self.panel_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    # -- события -------------------------------------------------------------
    def _sync_approvals(self) -> None:
        """Перерисовывает панель из состояния ворот согласования."""
        gate = self.orchestrator.gate
        self.approvals.set_requests(gate.pending() if gate else [])

    def _decide(self, approval_id: int, decision: Decision, comment: str) -> None:
        """Передаёт решение пользователя в ядро."""
        gate = self.orchestrator.gate
        if gate is None or not gate.resolve(approval_id, decision, comment):
            # Вопрос уже снят (например, прогон остановлен) — просто обновляем вид.
            self._sync_approvals()
            return
        self._sync_approvals()

    def _on_event(self, event: Event) -> None:
        """Обработчик шины: пишет строку в ленту и обновляет панель."""
        if event.type in QUIET_EVENTS:
            return
        self._append_feed(event)

        if event.type in (EventType.APPROVAL_REQUESTED, EventType.APPROVAL_RESOLVED):
            self._sync_approvals()

        if event.type in (EventType.SUBTASK_STARTED, EventType.SUBTASK_FINISHED,
                          EventType.SUBTASK_FAILED, EventType.REPORT_CREATED,
                          EventType.RUN_STARTED, EventType.RUN_FINISHED,
                          EventType.RUN_STOPPED):
            self.refresh()

        if event.type in (EventType.RUN_FINISHED, EventType.RUN_STOPPED):
            # Прогон закончился — висящих вопросов быть не должно.
            self._sync_approvals()

        if event.type == EventType.RUN_FINISHED:
            self.btn_start.setEnabled(True)
            self.btn_pause.setEnabled(False)
            self.btn_stop.setEnabled(False)
            self.btn_pause.setText(tr("run.pause"))

    def _append_feed(self, event: Event) -> None:
        """Добавляет цветную строку; лента подрезается, чтобы не расти вечно."""
        if self._feed_lines > 1500:
            self.feed.clear()
            self._feed_lines = 0

        cursor = self.feed.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        dim = QTextCharFormat()
        dim.setForeground(QColor(STATUS_COLORS["idle"]))
        cursor.insertText(f"{event.time_short}  ", dim)

        if event.agent_name:
            name_fmt = QTextCharFormat()
            name_fmt.setForeground(QColor(current_palette()["text"]))
            cursor.insertText(f"[{event.agent_name}] ", name_fmt)

        body = QTextCharFormat()
        body.setForeground(QColor(FEED_COLORS.get(event.type, "#c8cedb")))
        cursor.insertText(f"{event.message}\n", body)

        self._feed_lines += 1
        self.feed.setTextCursor(cursor)
        self.feed.ensureCursorVisible()

    # -- действия ------------------------------------------------------------
    def _start(self) -> None:
        if self.workspace_id is None:
            return
        task = self.repos.tasks.current(self.workspace_id)
        if task is None:
            warn(self, tr("task.no_task"))
            return
        subtasks = self.repos.tasks.subtasks(task.id)
        if not subtasks:
            warn(self, tr("run.no_subtasks"))
            return
        missing = [s.title for s in subtasks if not s.agent_id and s.status != "done"]
        if missing:
            warn(self, tr("run.unassigned") + "\n· " + "\n· ".join(missing[:8]))
            return

        self.btn_start.setEnabled(False)
        self.btn_pause.setEnabled(True)
        self.btn_stop.setEnabled(True)

        ws_id, task_id = self.workspace_id, task.id

        def failed(exc: Exception) -> None:
            self.btn_start.setEnabled(True)
            self.btn_pause.setEnabled(False)
            self.btn_stop.setEnabled(False)
            warn(self, str(exc))

        run_async(self.orchestrator.run_task(ws_id, task_id), None, failed)

    def _toggle_pause(self) -> None:
        if self.orchestrator.state.paused:
            self.orchestrator.resume()
            self.btn_pause.setText(tr("run.pause"))
        else:
            self.orchestrator.pause()
            self.btn_pause.setText(tr("run.resume"))

    def _stop(self) -> None:
        if confirm(self, tr("run.stop_confirm")):
            self.orchestrator.stop()
````

### `ui/pages/supervisor_page.py`

*373 строк*

````python
"""Этап 5 — страница супервайзера.

Три раздела: кто сейчас работает супервайзером, лента анонимных сводок и
история инцидентов с возможностью закрыть эскалированный вручную.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from app.config import DEFAULT_WORKSPACE_SETTINGS
from app.i18n import tr
from core.events import Event, EventBus, EventType
from core.orchestrator import Orchestrator
from storage.db import local_time
from storage.models import Incident
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, warn
from utils.asyncutils import run_async

SEVERITY_COLORS = {"low": "#99a1b3", "medium": "#f0b429", "high": "#ef5f6b"}
SEVERITY_TITLES = {"low": "низкая", "medium": "средняя", "high": "высокая"}
STATUS_TITLES = {
    "open": "открыт",
    "auto_resolved": "разрешён автоматически",
    "escalated": "требует решения",
    "resolved": "закрыт",
}
REASON_LABELS = {
    "conflict": "Конфликт данных",
    "not_accepted": "Результат не принят",
    "low_confidence": "Низкая уверенность",
    "milestone": "Завершён этап",
}
KIND_TITLES = {
    "conflict": "конфликт данных",
    "factual_error": "фактическая ошибка",
    "contradiction": "противоречие",
    "off_scope": "выход за рамки задания",
}


class ResolveDialog(QDialog):
    """Ручное закрытие инцидента с объяснением решения."""

    def __init__(self, parent: QWidget, incident: Incident) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("sup.resolve"))
        self.setMinimumWidth(520)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        problem = QLabel(incident.description)
        problem.setWordWrap(True)
        lay.addWidget(problem)

        lay.addWidget(QLabel(tr("sup.resolution")))
        self.text = QPlainTextEdit(incident.resolution)
        self.text.setMinimumHeight(120)
        lay.addWidget(self.text)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def value(self) -> str:
        return self.text.toPlainText().strip()


class SupervisorPage(QWidget):
    """Сводки и инциденты текущего воркспейса."""

    def __init__(self, repos: Repos, bus: EventBus, orchestrator: Orchestrator) -> None:
        super().__init__()
        self.repos = repos
        self.bus = bus
        self.orchestrator = orchestrator
        self.workspace_id: int | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        self.header = Header(tr("sup.title"), tr("sup.subtitle"))
        self.btn_summary = QPushButton(tr("sup.make_summary"))
        self.btn_summary.setObjectName("Primary")
        self.btn_summary.clicked.connect(self._make_summary)
        self.header.add_action(self.btn_summary)
        root.addWidget(self.header)

        self.model_label = QLabel("")
        self.model_label.setObjectName("Dim")
        self.model_label.setWordWrap(True)
        root.addWidget(self.model_label)

        self.tabs = QTabWidget()
        root.addWidget(self.tabs, 1)

        self.summaries_box, summaries_page = _scrollable()
        self.tabs.addTab(summaries_page, tr("sup.summaries"))

        self.incidents_box, incidents_page = _scrollable()
        self.tabs.addTab(incidents_page, tr("sup.incidents"))

        self.approvals_box, approvals_page = _scrollable()
        self.tabs.addTab(approvals_page, tr("sup.approvals"))

        self.bus.subscribe(self._on_event)

    # -- данные --------------------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        _clear(self.summaries_box)
        _clear(self.incidents_box)
        _clear(self.approvals_box)

        has_ws = self.workspace_id is not None
        self.btn_summary.setEnabled(has_ws and not self.orchestrator.state.running)
        if not has_ws:
            self.model_label.setText("")
            self.summaries_box.addWidget(EmptyState(tr("ws.empty")))
            self.incidents_box.addWidget(EmptyState(tr("ws.empty")))
            self.approvals_box.addWidget(EmptyState(tr("ws.empty")))
            return

        self.model_label.setText(self._describe_model())
        self._render_summaries()
        self._render_incidents()
        self._render_approvals()

    def _describe_model(self) -> str:
        ws = self.repos.workspaces.get(self.workspace_id)
        if ws is None:
            return ""
        s = {**DEFAULT_WORKSPACE_SETTINGS, **ws.settings}
        if s.get("supervisor_mode") == "local":
            return tr("sup.model_local",
                      model=s.get("supervisor_local_model", "—"),
                      url=s.get("supervisor_local_base_url", "—"))
        agent = self.repos.agents.get(int(s["supervisor_agent_id"])) \
            if s.get("supervisor_agent_id") else None
        if agent is None:
            agent = next((a for a in self.repos.agents.list(self.workspace_id)
                          if a.is_supervisor), None)
        if agent is None:
            return tr("sup.not_configured")
        return tr("sup.model_api", name=agent.name, model=agent.model)

    def _render_summaries(self) -> None:
        summaries = self.repos.reports.list_summaries(self.workspace_id, limit=30)
        if not summaries:
            self.summaries_box.addWidget(EmptyState(tr("sup.no_summaries")))
            return
        triggers = {"timer": tr("sup.by_timer"), "event": tr("sup.by_event"),
                    "manual": tr("sup.by_hand"), "final": tr("sup.by_final")}
        for item in summaries:
            card = Card(self, spacing=6)
            head = QHBoxLayout()
            when = QLabel(local_time(item.created_at))
            when.setObjectName("Dim")
            head.addWidget(when)
            trigger = QLabel(triggers.get(item.trigger, item.trigger))
            trigger.setObjectName("Dim")
            head.addWidget(trigger)
            head.addStretch(1)
            count = len([x for x in item.delivered_to.split(",") if x])
            recipients = QLabel(tr("sup.delivered", n=count))
            recipients.setObjectName("Dim")
            head.addWidget(recipients)
            card.body.addLayout(head)

            body = QLabel(item.content)
            body.setWordWrap(True)
            body.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
            card.body.addWidget(body)
            self.summaries_box.addWidget(card)
        self.summaries_box.addStretch(1)

    def _render_incidents(self) -> None:
        incidents = self.repos.incidents.list(self.workspace_id, limit=200)
        if not incidents:
            self.incidents_box.addWidget(EmptyState(tr("sup.no_incidents")))
            return
        for incident in incidents:
            self.incidents_box.addWidget(self._incident_card(incident))
        self.incidents_box.addStretch(1)

    def _incident_card(self, incident: Incident) -> Card:
        card = Card(self, spacing=6)
        row = QHBoxLayout()
        texts = QVBoxLayout()
        texts.setSpacing(3)

        head = QHBoxLayout()
        kind = QLabel(KIND_TITLES.get(incident.kind, incident.kind))
        kind.setObjectName("H2")
        head.addWidget(kind)

        color = SEVERITY_COLORS.get(incident.severity, SEVERITY_COLORS["medium"])
        severity = QLabel(SEVERITY_TITLES.get(incident.severity, incident.severity))
        severity.setStyleSheet(
            f"color: {color}; border: 1px solid {color}; border-radius: 9px;"
            f"padding: 1px 9px; font-size: 12px; font-weight: 600;"
        )
        head.addWidget(severity)
        head.addStretch(1)
        when = QLabel(local_time(incident.created_at))
        when.setObjectName("Dim")
        head.addWidget(when)
        texts.addLayout(head)

        description = QLabel(incident.description)
        description.setWordWrap(True)
        texts.addWidget(description)

        status = QLabel(f"{tr('common.status')}: "
                        f"{STATUS_TITLES.get(incident.status, incident.status)}")
        status.setObjectName("Dim")
        texts.addWidget(status)

        if incident.resolution:
            resolution = QLabel(f"{tr('sup.resolution')}: {incident.resolution}")
            resolution.setObjectName("Dim")
            resolution.setWordWrap(True)
            texts.addWidget(resolution)

        row.addLayout(texts, 1)
        if incident.status in ("open", "escalated"):
            button = QPushButton(tr("sup.resolve"))
            button.clicked.connect(lambda: self._resolve(incident))
            row.addWidget(button, 0, Qt.AlignmentFlag.AlignTop)
        card.body.addLayout(row)
        return card

    def _render_approvals(self) -> None:
        """История точек human-in-the-loop: что спросили и что ответили."""
        from core.hitl import parse_payload

        rows = self.repos.approvals.history(self.workspace_id, limit=60)
        if not rows:
            self.approvals_box.addWidget(EmptyState(tr("sup.no_approvals")))
            return

        titles = {"approve": tr("sup.d_approve"), "rework": tr("sup.d_rework"),
                  "skip": tr("sup.d_skip"), "abort": tr("sup.d_abort"),
                  "cancelled": tr("sup.d_cancelled"), "": tr("sup.d_pending")}
        colours = {"approve": "#3ecf8e", "rework": "#f0b429", "skip": "#99a1b3",
                   "abort": "#ef5f6b", "cancelled": "#99a1b3", "": "#6c8cff"}

        for row in rows:
            payload = parse_payload(row.get("payload_json", "{}"))
            card = Card(self, spacing=5)

            head = QHBoxLayout()
            reason = QLabel(REASON_LABELS.get(row["reason"], row["reason"]))
            reason.setObjectName("H2")
            head.addWidget(reason, 1)
            decision = row.get("decision", "")
            verdict = QLabel(titles.get(decision, decision))
            colour = colours.get(decision, "#99a1b3")
            verdict.setStyleSheet(
                f"color: {colour}; border: 1px solid {colour}; border-radius: 9px;"
                f"padding: 1px 9px; font-size: 12px; font-weight: 600;"
            )
            head.addWidget(verdict)
            card.body.addLayout(head)

            question = QLabel(payload.get("question", ""))
            question.setWordWrap(True)
            card.body.addWidget(question)

            meta_parts = [local_time(row["created_at"])]
            if payload.get("agent_name"):
                meta_parts.append(payload["agent_name"])
            if row.get("comment"):
                meta_parts.append(f"комментарий: {row['comment']}")
            meta = QLabel("  ·  ".join(meta_parts))
            meta.setObjectName("Dim")
            meta.setWordWrap(True)
            card.body.addWidget(meta)
            self.approvals_box.addWidget(card)
        self.approvals_box.addStretch(1)

    # -- действия ------------------------------------------------------------
    def _resolve(self, incident: Incident) -> None:
        dialog = ResolveDialog(self, incident)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        self.repos.incidents.resolve(incident.id, "resolved",
                                     dialog.value() or "Закрыто пользователем")
        self.refresh()

    def _make_summary(self) -> None:
        """Ручная сводка вне прогона — удобно, чтобы освежить контекст агентов."""
        if self.workspace_id is None:
            return
        task = self.repos.tasks.current(self.workspace_id)
        if task is None:
            warn(self, tr("task.no_task"))
            return

        ws = self.repos.workspaces.get(self.workspace_id)
        settings = {**DEFAULT_WORKSPACE_SETTINGS, **(ws.settings if ws else {})}
        from core.supervisor.supervisor import Supervisor

        supervisor = Supervisor(self.repos, self.bus, self.workspace_id, settings)
        if not supervisor.available():
            warn(self, tr("sup.not_configured"))
            return

        self.btn_summary.setEnabled(False)

        async def job() -> str:
            try:
                return await supervisor.make_summary(task, trigger="manual")
            finally:
                await supervisor.aclose()

        def done(content: str) -> None:
            self.btn_summary.setEnabled(True)
            if not content:
                warn(self, tr("sup.nothing_to_summarize"))
            self.refresh()

        def failed(exc: Exception) -> None:
            self.btn_summary.setEnabled(True)
            warn(self, str(exc))

        run_async(job(), done, failed)

    def _on_event(self, event: Event) -> None:
        if event.type in (EventType.SUMMARY_CREATED, EventType.INCIDENT_CREATED,
                          EventType.REPORT_REVIEWED, EventType.RUN_FINISHED,
                          EventType.APPROVAL_REQUESTED, EventType.APPROVAL_RESOLVED):
            self.refresh()


def _scrollable() -> tuple[QVBoxLayout, QWidget]:
    """Создаёт прокручиваемую страницу и возвращает её внутренний layout."""
    scroll = QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setFrameShape(QScrollArea.Shape.NoFrame)
    container = QWidget()
    layout = QVBoxLayout(container)
    layout.setContentsMargins(4, 8, 4, 8)
    layout.setSpacing(10)
    scroll.setWidget(container)
    return layout, scroll


def _clear(layout: QVBoxLayout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
````

### `ui/pages/dashboard_page.py`

*461 строк*

````python
"""Этап 6 — дашборд реального времени.

Собирает в одном месте всё, что происходит в воркспейсе: статус каждого
агента, прогресс по задаче и подзадачам, кривые расхода токенов и денег,
объединённую ленту отчётов и сводок, историю инцидентов.

Обновление идёт по событиям шины, но с троттлингом: во время прогона
события летят пачками, и перерисовывать всё на каждое — лишняя работа.
Таймер собирает их в один апдейт не чаще раза в секунду.
"""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from core.events import Event, EventBus, EventType
from storage.db import local_time
from storage.repositories import Repos
from ui.pages.supervisor_page import KIND_TITLES
from ui.theme import STATUS_COLORS
from ui.widgets.charts import Bar, BarChart, LineChart, SegmentBar, SeriesPoint
from ui.widgets.common import Card, EmptyState, Header, StatusBadge

#: не чаще одного перерисовывания в секунду
REFRESH_THROTTLE_MS = 1000
#: сколько записей показывать в ленте
FEED_LIMIT = 40
#: точек на кривой расхода
SERIES_LIMIT = 300

AGENT_COLORS = ["#6c8cff", "#3ecf8e", "#f0b429", "#b07cff", "#ef5f6b",
                "#4fc3f7", "#ff9e64", "#7ee787"]


class Metric(QWidget):
    """Одна крупная цифра с подписью."""

    def __init__(self, caption: str, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(1)
        self.value = QLabel("—")
        self.value.setObjectName("H1")
        lay.addWidget(self.value)
        self.caption = QLabel(caption)
        self.caption.setObjectName("Dim")
        lay.addWidget(self.caption)

    def set(self, value: str, colour: str = "") -> None:
        self.value.setText(value)
        self.value.setStyleSheet(f"color: {colour};" if colour else "")

    def set_caption(self, caption: str) -> None:
        self.caption.setText(caption)


class DashboardPage(QWidget):
    """Сводная картина по активному воркспейсу."""

    def __init__(self, repos: Repos, bus: EventBus) -> None:
        super().__init__()
        self.repos = repos
        self.bus = bus
        self.workspace_id: int | None = None

        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(REFRESH_THROTTLE_MS)
        self._timer.timeout.connect(self.refresh)

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        self.header = Header(tr("dash.title"), tr("dash.subtitle"))
        refresh_button = QPushButton(tr("common.refresh"))
        refresh_button.clicked.connect(self.refresh)
        self.header.add_action(refresh_button)
        root.addWidget(self.header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        body = QVBoxLayout(page)
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(14)

        body.addWidget(self._build_metrics())
        body.addWidget(self._build_progress())

        charts_row = QHBoxLayout()
        charts_row.setSpacing(14)
        charts_row.addWidget(self._build_cost_chart(), 1)
        charts_row.addWidget(self._build_agents_chart(), 1)
        body.addLayout(charts_row)

        body.addWidget(self._build_agents_card())

        feeds_row = QHBoxLayout()
        feeds_row.setSpacing(14)
        feeds_row.addWidget(self._build_feed_card(), 3)
        feeds_row.addWidget(self._build_incidents_card(), 2)
        body.addLayout(feeds_row)
        body.addStretch(1)

        self.bus.subscribe(self._on_event)

    # -- построение ----------------------------------------------------------
    def _build_metrics(self) -> Card:
        card = Card(self)
        grid = QGridLayout()
        grid.setSpacing(18)
        self.m_agents = Metric(tr("dash.m_agents"))
        self.m_subtasks = Metric(tr("dash.m_subtasks"))
        self.m_tokens = Metric(tr("dash.m_tokens"))
        self.m_cost = Metric(tr("dash.m_cost"))
        self.m_reworks = Metric(tr("dash.m_reworks"))
        self.m_open = Metric(tr("dash.m_open_incidents"))
        for i, metric in enumerate((self.m_agents, self.m_subtasks, self.m_tokens,
                                    self.m_cost, self.m_reworks, self.m_open)):
            grid.addWidget(metric, 0, i)
        card.body.addLayout(grid)
        return card

    def _build_progress(self) -> Card:
        card = Card(self, spacing=8)
        row = QHBoxLayout()
        self.task_title = QLabel(tr("task.no_task"))
        self.task_title.setObjectName("H2")
        self.task_title.setWordWrap(True)
        row.addWidget(self.task_title, 1)
        self.progress_label = QLabel("")
        self.progress_label.setObjectName("Dim")
        row.addWidget(self.progress_label)
        card.body.addLayout(row)

        self.progress_bar = SegmentBar()
        card.body.addWidget(self.progress_bar)

        self.legend = QLabel("")
        self.legend.setObjectName("Dim")
        self.legend.setWordWrap(True)
        card.body.addWidget(self.legend)
        return card

    def _build_cost_chart(self) -> Card:
        card = Card(self, spacing=6)
        self.cost_chart = LineChart(tr("dash.cost_chart"), unit="usd")
        self.cost_chart.empty_text = tr("dash.no_usage")
        card.body.addWidget(self.cost_chart)
        self.tokens_chart = LineChart(tr("dash.tokens_chart"), unit="tokens")
        self.tokens_chart.empty_text = tr("dash.no_usage")
        card.body.addWidget(self.tokens_chart)
        return card

    def _build_agents_chart(self) -> Card:
        card = Card(self, spacing=6)
        self.agent_chart = BarChart(tr("dash.by_agent"), unit="tokens")
        self.agent_chart.empty_text = tr("dash.no_usage")
        card.body.addWidget(self.agent_chart)
        return card

    def _build_agents_card(self) -> Card:
        card = Card(self, spacing=8)
        title = QLabel(tr("dash.agents"))
        title.setObjectName("H2")
        card.body.addWidget(title)
        self.agents_box = QVBoxLayout()
        self.agents_box.setSpacing(4)
        card.body.addLayout(self.agents_box)
        return card

    def _build_feed_card(self) -> Card:
        card = Card(self, spacing=8)
        title = QLabel(tr("dash.feed"))
        title.setObjectName("H2")
        card.body.addWidget(title)
        self.feed_box = QVBoxLayout()
        self.feed_box.setSpacing(6)
        card.body.addLayout(self.feed_box)
        return card

    def _build_incidents_card(self) -> Card:
        card = Card(self, spacing=8)
        title = QLabel(tr("dash.incidents"))
        title.setObjectName("H2")
        card.body.addWidget(title)
        self.incidents_box = QVBoxLayout()
        self.incidents_box.setSpacing(6)
        card.body.addLayout(self.incidents_box)
        return card

    # -- данные --------------------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        _clear(self.agents_box)
        _clear(self.feed_box)
        _clear(self.incidents_box)

        if self.workspace_id is None:
            self.task_title.setText(tr("ws.empty"))
            self.progress_label.setText("")
            self.legend.setText("")
            self.progress_bar.set_segments([])
            for metric in (self.m_agents, self.m_subtasks, self.m_tokens,
                           self.m_cost, self.m_reworks, self.m_open):
                metric.set("—")
            self.cost_chart.set_points([])
            self.tokens_chart.set_points([])
            self.agent_chart.set_bars([])
            self.agents_box.addWidget(EmptyState(tr("ws.empty")))
            return

        agents = self.repos.agents.list(self.workspace_id)
        task = self.repos.tasks.current(self.workspace_id)
        subtasks = self.repos.tasks.subtasks(task.id) if task else []

        self._fill_metrics(agents, task, subtasks)
        self._fill_progress(task, subtasks)
        self._fill_charts(agents)
        self._fill_agents(agents, subtasks)
        self._fill_feed()
        self._fill_incidents()

    def _fill_metrics(self, agents, task, subtasks) -> None:
        tokens, cost = self.repos.budgets.workspace_totals(self.workspace_id)
        counts = self.repos.budgets.incident_counts(self.workspace_id)
        open_count = counts.get("open", 0) + counts.get("escalated", 0)
        done = sum(1 for s in subtasks if s.status == "done")
        reworks = sum(s.rework_count for s in subtasks)

        self.m_agents.set(str(len(agents)))
        self.m_subtasks.set(f"{done} / {len(subtasks)}" if subtasks else "—")
        self.m_tokens.set(f"{tokens:,}".replace(",", " "))
        self.m_cost.set(f"${cost:.4f}" if cost < 1 else f"${cost:,.2f}".replace(",", " "))
        self.m_reworks.set(str(reworks), STATUS_COLORS["rework"] if reworks else "")
        self.m_open.set(str(open_count), STATUS_COLORS["error"] if open_count else "")

        if task and task.token_limit:
            share = tokens / task.token_limit
            self.m_tokens.set_caption(
                tr("dash.m_tokens_limit", pct=f"{share * 100:.0f}",
                   limit=f"{task.token_limit:,}".replace(",", " "))
            )
        else:
            self.m_tokens.set_caption(tr("dash.m_tokens"))

    def _fill_progress(self, task, subtasks) -> None:
        if task is None:
            self.task_title.setText(tr("task.no_task"))
            self.progress_label.setText("")
            self.legend.setText("")
            self.progress_bar.set_segments([])
            return

        self.task_title.setText(task.title or tr("task.title"))
        order = ["done", "review", "rework", "running", "error", "paused", "idle"]
        buckets = {key: 0 for key in order}
        for subtask in subtasks:
            buckets[subtask.status] = buckets.get(subtask.status, 0) + 1

        self.progress_bar.set_segments(
            [(tr(f"status.{key}"), buckets.get(key, 0), STATUS_COLORS.get(key, "#888"))
             for key in order]
        )
        done = buckets.get("done", 0)
        total = len(subtasks)
        percent = (done / total * 100) if total else 0
        self.progress_label.setText(f"{done} / {total}  ·  {percent:.0f}%")
        self.legend.setText("   ".join(
            f"{tr(f'status.{key}')}: {buckets[key]}" for key in order if buckets.get(key)
        ) or tr("task.subtasks"))

    def _fill_charts(self, agents) -> None:
        series = self.repos.budgets.usage_series(self.workspace_id, SERIES_LIMIT)
        cost_points: list[SeriesPoint] = []
        token_points: list[SeriesPoint] = []
        cost_acc = 0.0
        token_acc = 0
        for created_at, tokens, cost in series:
            cost_acc += cost
            token_acc += tokens
            label = local_time(created_at, "%H:%M")
            cost_points.append(SeriesPoint(label, cost_acc))
            token_points.append(SeriesPoint(label, float(token_acc)))
        self.cost_chart.set_points(cost_points)
        self.tokens_chart.set_points(token_points)

        names = {a.id: a.name for a in agents}
        bars: list[Bar] = []
        for i, (agent_id, tokens, _cost) in enumerate(
            self.repos.budgets.usage_by_agent(self.workspace_id)
        ):
            if not tokens:
                continue
            label = names.get(agent_id) if agent_id else tr("dash.supervisor_line")
            bars.append(Bar(label or tr("dash.supervisor_line"), float(tokens),
                            AGENT_COLORS[i % len(AGENT_COLORS)]))
        self.agent_chart.set_bars(bars[:10])

    def _fill_agents(self, agents, subtasks) -> None:
        if not agents:
            self.agents_box.addWidget(EmptyState(tr("agents.empty")))
            return
        usage = {agent_id: (tokens, cost) for agent_id, tokens, cost
                 in self.repos.budgets.usage_by_agent(self.workspace_id)}
        assigned: dict[int, str] = {}
        for subtask in subtasks:
            if subtask.agent_id and subtask.status in ("running", "rework"):
                assigned[subtask.agent_id] = subtask.title

        for agent in agents:
            row = QWidget()
            line = QHBoxLayout(row)
            line.setContentsMargins(0, 0, 0, 0)
            line.setSpacing(10)

            name = QLabel(agent.name + ("  ⭐" if agent.is_supervisor else ""))
            line.addWidget(name)

            current = assigned.get(agent.id)
            if current:
                doing = QLabel("→ " + _elide(current, 38))
                doing.setObjectName("Dim")
                line.addWidget(doing)
            line.addStretch(1)

            tokens, cost = usage.get(agent.id, (0, 0.0))
            spent = QLabel(f"{tokens:,}".replace(",", " ") + f" · ${cost:.4f}")
            spent.setObjectName("Dim")
            line.addWidget(spent)
            line.addWidget(StatusBadge(agent.status))
            self.agents_box.addWidget(row)

    def _fill_feed(self) -> None:
        """Объединённая лента отчётов и сводок, новое сверху."""
        entries: list[tuple[str, str, str, str]] = []   # (время, метка, текст, цвет)
        names = {a.id: a.name for a in self.repos.agents.list(self.workspace_id)}

        for report in self.repos.reports.list_reports(self.workspace_id, limit=FEED_LIMIT):
            verdict = {"ok": tr("dash.v_ok"), "rework": tr("dash.v_rework"),
                       "conflict": tr("dash.v_conflict")}.get(report.review_verdict, "")
            colour = {"ok": STATUS_COLORS["done"], "rework": STATUS_COLORS["rework"],
                      "conflict": STATUS_COLORS["error"]}.get(
                          report.review_verdict, STATUS_COLORS["idle"])
            confidence = (f"  ·  {tr('dash.confidence')} {report.confidence:.2f}"
                          if report.confidence is not None else "")
            entries.append((
                report.created_at,
                names.get(report.agent_id, tr("dash.unknown_agent")),
                f"{_elide(report.content.strip().replace(chr(10), ' '), 150)}"
                f"{confidence}{('  ·  ' + verdict) if verdict else ''}",
                colour,
            ))

        for summary in self.repos.reports.list_summaries(self.workspace_id,
                                                         limit=FEED_LIMIT):
            entries.append((
                summary.created_at,
                tr("dash.summary_line"),
                _elide(summary.content.strip().replace("\n", " "), 150),
                "#b07cff",
            ))

        entries.sort(key=lambda e: e[0], reverse=True)
        if not entries:
            self.feed_box.addWidget(EmptyState(tr("dash.no_feed")))
            return

        for created_at, who, text, colour in entries[:FEED_LIMIT]:
            item = QWidget()
            lay = QVBoxLayout(item)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(1)

            head = QHBoxLayout()
            author = QLabel(who)
            author.setStyleSheet(f"color: {colour}; font-weight: 600;")
            head.addWidget(author)
            head.addStretch(1)
            when = QLabel(local_time(created_at, "%H:%M:%S"))
            when.setObjectName("Dim")
            head.addWidget(when)
            lay.addLayout(head)

            body = QLabel(text)
            body.setObjectName("Dim")
            body.setWordWrap(True)
            lay.addWidget(body)
            self.feed_box.addWidget(item)

    def _fill_incidents(self) -> None:
        incidents = self.repos.incidents.list(self.workspace_id, limit=FEED_LIMIT)
        if not incidents:
            self.incidents_box.addWidget(EmptyState(tr("sup.no_incidents")))
            return
        severity_colours = {"low": STATUS_COLORS["idle"], "medium": STATUS_COLORS["rework"],
                            "high": STATUS_COLORS["error"]}
        statuses = {"open": tr("dash.i_open"), "escalated": tr("dash.i_escalated"),
                    "auto_resolved": tr("dash.i_auto"), "resolved": tr("dash.i_resolved")}
        for incident in incidents:
            item = QWidget()
            lay = QVBoxLayout(item)
            lay.setContentsMargins(0, 0, 0, 0)
            lay.setSpacing(1)

            head = QHBoxLayout()
            kind = QLabel(KIND_TITLES.get(incident.kind, incident.kind))
            kind.setStyleSheet(
                f"color: {severity_colours.get(incident.severity, '#888')}; font-weight: 600;"
            )
            head.addWidget(kind)
            head.addStretch(1)
            status = QLabel(statuses.get(incident.status, incident.status))
            status.setObjectName("Dim")
            head.addWidget(status)
            lay.addLayout(head)

            description = QLabel(_elide(incident.description, 140))
            description.setObjectName("Dim")
            description.setWordWrap(True)
            lay.addWidget(description)
            self.incidents_box.addWidget(item)

    # -- реакция на события --------------------------------------------------
    def _on_event(self, event: Event) -> None:
        """Ставит обновление в очередь, а не перерисовывает всё немедленно."""
        if event.type in (EventType.AGENT_THINKING, EventType.AGENT_TOOL_CALL,
                          EventType.AGENT_TOOL_RESULT):
            return
        if not self._timer.isActive():
            self._timer.start()


def _elide(text: str, limit: int) -> str:
    text = (text or "").strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _clear(layout) -> None:
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()
````

### `ui/pages/budget_page.py`

*225 строк*

````python
"""Этап 9 — страница бюджетов и лимитов.

Лимит ставится на трёх уровнях: весь проект, текущая задача, отдельный агент.
Каждый — и по токенам, и по деньгам. Пустое поле означает «без ограничения»:
так же, как лимит токенов при постановке задачи.
"""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QProgressBar,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.i18n import tr
from core.budget import SCOPE_TITLES, ScopeState, load_states
from core.events import Event, EventBus, EventType
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, info

#: цвет полосы в зависимости от того, насколько выбран бюджет
BAR_COLORS = [(1.0, "#ef5f6b"), (0.8, "#f0b429"), (0.0, "#6c8cff")]


def _bar_color(ratio: float) -> str:
    for threshold, colour in BAR_COLORS:
        if ratio >= threshold:
            return colour
    return BAR_COLORS[-1][1]


class LimitRow(Card):
    """Одна строка: уровень, расход и поля лимитов."""

    def __init__(self, parent: QWidget, state: ScopeState, on_change) -> None:
        super().__init__(parent, spacing=8)
        self.state = state
        self.on_change = on_change

        head = QHBoxLayout()
        name = QLabel(state.name)
        name.setObjectName("H2")
        head.addWidget(name)
        scope = QLabel(SCOPE_TITLES.get(state.scope, state.scope))
        scope.setObjectName("Dim")
        head.addWidget(scope)
        head.addStretch(1)

        spent = QLabel(tr("bud.spent",
                          tokens=f"{state.tokens:,}".replace(",", " "),
                          cost=f"{state.cost:.4f}"))
        spent.setObjectName("Dim")
        head.addWidget(spent)
        self.body.addLayout(head)

        if state.limit.is_set:
            ratio = min(state.ratio(), 1.0)
            bar = QProgressBar()
            bar.setTextVisible(False)
            bar.setValue(int(ratio * 100))
            colour = _bar_color(state.ratio())
            bar.setStyleSheet(
                f"QProgressBar::chunk {{ background: {colour}; border-radius: 6px; }}"
            )
            self.body.addWidget(bar)

            note = QLabel(tr("bud.used_pct", pct=f"{state.ratio() * 100:.0f}"))
            note.setStyleSheet(f"color: {colour};")
            if state.exceeded():
                note.setText(tr("bud.exceeded"))
            self.body.addWidget(note)

        fields = QHBoxLayout()
        tokens_col = QVBoxLayout()
        tokens_col.addWidget(QLabel(tr("bud.token_limit")))
        self.tokens_edit = QLineEdit(
            str(state.limit.token_limit) if state.limit.token_limit else ""
        )
        self.tokens_edit.setPlaceholderText(tr("bud.no_limit"))
        self.tokens_edit.editingFinished.connect(self._changed)
        tokens_col.addWidget(self.tokens_edit)
        fields.addLayout(tokens_col, 1)

        cost_col = QVBoxLayout()
        cost_col.addWidget(QLabel(tr("bud.cost_limit")))
        self.cost_edit = QLineEdit(
            f"{state.limit.cost_limit:g}" if state.limit.cost_limit else ""
        )
        self.cost_edit.setPlaceholderText(tr("bud.no_limit"))
        self.cost_edit.editingFinished.connect(self._changed)
        cost_col.addWidget(self.cost_edit)
        fields.addLayout(cost_col, 1)

        alert_col = QVBoxLayout()
        alert_col.addWidget(QLabel(tr("bud.alert_at")))
        self.alert_spin = QDoubleSpinBox()
        self.alert_spin.setRange(0.1, 1.0)
        self.alert_spin.setSingleStep(0.05)
        self.alert_spin.setDecimals(2)
        self.alert_spin.setValue(state.limit.alert_threshold or 0.8)
        self.alert_spin.valueChanged.connect(self._changed)
        alert_col.addWidget(self.alert_spin)
        fields.addLayout(alert_col)
        self.body.addLayout(fields)

    def _changed(self) -> None:
        self.on_change(self.state, self.values())

    def values(self) -> tuple[int | None, float | None, float]:
        return (_parse_int(self.tokens_edit.text()),
                _parse_float(self.cost_edit.text()),
                round(self.alert_spin.value(), 2))


class BudgetPage(QWidget):
    """Настройка лимитов и наблюдение за расходом."""

    def __init__(self, repos: Repos, bus: EventBus) -> None:
        super().__init__()
        self.repos = repos
        self.bus = bus
        self.workspace_id: int | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        self.header = Header(tr("bud.title"), tr("bud.subtitle"))
        refresh = QPushButton(tr("common.refresh"))
        refresh.clicked.connect(self.refresh)
        self.header.add_action(refresh)
        root.addWidget(self.header)

        self.alerts = QLabel("")
        self.alerts.setWordWrap(True)
        self.alerts.setVisible(False)
        root.addWidget(self.alerts)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        self.rows = QVBoxLayout(page)
        self.rows.setContentsMargins(0, 0, 0, 0)
        self.rows.setSpacing(10)

        self.bus.subscribe(self._on_event)

    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        while self.rows.count():
            item = self.rows.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if self.workspace_id is None:
            self.rows.addWidget(EmptyState(tr("ws.empty")))
            return

        states = load_states(self.repos, self.workspace_id)
        if not states:
            self.rows.addWidget(EmptyState(tr("bud.nothing")))
            return
        for state in states:
            self.rows.addWidget(LimitRow(self, state, self._save))
        self.rows.addStretch(1)

    def _save(self, state: ScopeState, values) -> None:
        """Сохраняет лимит. Пустые поля означают «ограничения нет»."""
        token_limit, cost_limit, threshold = values
        if token_limit is None and cost_limit is None:
            self.repos.budgets.delete_limit(state.scope, state.scope_id)
        else:
            self.repos.budgets.upsert(state.scope, state.scope_id,
                                      token_limit, cost_limit, threshold)
            self.repos.budgets.sync_used(state.scope, state.scope_id,
                                         state.tokens, state.cost)
        self.refresh()

    def _on_event(self, event: Event) -> None:
        if event.type not in (EventType.BUDGET_ALERT, EventType.BUDGET_EXCEEDED):
            return
        colour = "#ef5f6b" if event.type is EventType.BUDGET_EXCEEDED else "#f0b429"
        self.alerts.setText(event.message)
        self.alerts.setStyleSheet(
            f"color: {colour}; border: 1px solid {colour}; border-radius: 8px;"
            f"padding: 8px 12px;"
        )
        self.alerts.setVisible(True)
        self.refresh()


def _parse_int(raw: str) -> int | None:
    raw = (raw or "").replace(" ", "").strip()
    if not raw:
        return None
    try:
        value = int(raw)
    except ValueError:
        return None
    return value if value > 0 else None


def _parse_float(raw: str) -> float | None:
    raw = (raw or "").replace(",", ".").replace("$", "").strip()
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    return value if value > 0 else None
````

### `ui/pages/export_page.py`

*301 строк*

````python
"""Этап 8 — страница экспорта результата.

Формат подбирается автоматически по типу задачи и по тому, что реально
наработано, но выбор всегда остаётся за пользователем: рядом с подсказкой
написано, **почему** предложен именно этот формат.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.config import PATHS
from app.i18n import tr
from core.export.bundle import FORMAT_TITLES, ExportOptions, collect, detect_format
from core.export.exporters import (
    ExportError,
    ExportResult,
    export,
    open_folder,
    suggest_filename,
)
from storage.repositories import Repos
from ui.widgets.common import Card, EmptyState, Header, warn


class ExportPage(QWidget):
    """Сборка и выгрузка финального результата."""

    def __init__(self, repos: Repos) -> None:
        super().__init__()
        self.repos = repos
        self.workspace_id: int | None = None
        self._bundle = None
        self._last: ExportResult | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(14)

        self.header = Header(tr("exp.title"), tr("exp.subtitle"))
        self.btn_refresh = QPushButton(tr("common.refresh"))
        self.btn_refresh.clicked.connect(self.refresh)
        self.header.add_action(self.btn_refresh)
        root.addWidget(self.header)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        body = QVBoxLayout(page)
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(14)

        body.addWidget(self._build_format_card())
        body.addWidget(self._build_content_card())
        body.addWidget(self._build_output_card())
        body.addStretch(1)

    # -- карточки ------------------------------------------------------------
    def _build_format_card(self) -> Card:
        card = Card(self, spacing=10)
        title = QLabel(tr("exp.format"))
        title.setObjectName("H2")
        card.body.addWidget(title)

        row = QHBoxLayout()
        self.format_box = QComboBox()
        for key, label in FORMAT_TITLES.items():
            self.format_box.addItem(label, key)
        self.format_box.currentIndexChanged.connect(self._on_format_changed)
        row.addWidget(self.format_box, 1)

        self.btn_auto = QPushButton(tr("exp.use_auto"))
        self.btn_auto.clicked.connect(self._apply_auto)
        row.addWidget(self.btn_auto)
        card.body.addLayout(row)

        self.hint = QLabel("")
        self.hint.setObjectName("Dim")
        self.hint.setWordWrap(True)
        card.body.addWidget(self.hint)

        self.stats = QLabel("")
        self.stats.setObjectName("Dim")
        self.stats.setWordWrap(True)
        card.body.addWidget(self.stats)
        return card

    def _build_content_card(self) -> Card:
        card = Card(self, spacing=8)
        title = QLabel(tr("exp.content"))
        title.setObjectName("H2")
        card.body.addWidget(title)

        self.opt_results = QCheckBox(tr("exp.opt_results"))
        self.opt_results.setChecked(True)
        self.opt_reports = QCheckBox(tr("exp.opt_reports"))
        self.opt_summaries = QCheckBox(tr("exp.opt_summaries"))
        self.opt_incidents = QCheckBox(tr("exp.opt_incidents"))
        self.opt_incidents.setChecked(True)
        self.opt_decisions = QCheckBox(tr("exp.opt_decisions"))
        self.opt_stats = QCheckBox(tr("exp.opt_stats"))
        self.opt_stats.setChecked(True)
        self.opt_files = QCheckBox(tr("exp.opt_files"))
        self.opt_files.setChecked(True)
        self.opt_anon = QCheckBox(tr("exp.opt_anon"))
        self.opt_anon.setToolTip(tr("exp.opt_anon_hint"))

        for box in (self.opt_results, self.opt_reports, self.opt_summaries,
                    self.opt_incidents, self.opt_decisions, self.opt_stats,
                    self.opt_files, self.opt_anon):
            card.body.addWidget(box)
        return card

    def _build_output_card(self) -> Card:
        card = Card(self, spacing=10)
        title = QLabel(tr("exp.output"))
        title.setObjectName("H2")
        card.body.addWidget(title)

        row = QHBoxLayout()
        self.path_edit = QLineEdit()
        row.addWidget(self.path_edit, 1)
        browse = QPushButton(tr("exp.browse"))
        browse.clicked.connect(self._browse)
        row.addWidget(browse)
        card.body.addLayout(row)

        buttons = QHBoxLayout()
        self.btn_export = QPushButton(tr("exp.export"))
        self.btn_export.setObjectName("Primary")
        self.btn_export.clicked.connect(self._export)
        buttons.addWidget(self.btn_export)

        self.btn_open = QPushButton(tr("exp.open_folder"))
        self.btn_open.setEnabled(False)
        self.btn_open.clicked.connect(self._open_folder)
        buttons.addWidget(self.btn_open)
        buttons.addStretch(1)
        card.body.addLayout(buttons)

        self.result_label = QLabel("")
        self.result_label.setWordWrap(True)
        self.result_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        card.body.addWidget(self.result_label)

        self.empty = EmptyState(tr("exp.nothing"))
        self.empty.setVisible(False)
        card.body.addWidget(self.empty)
        return card

    # -- данные --------------------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.refresh()

    def refresh(self) -> None:
        enabled = self.workspace_id is not None
        for widget in (self.format_box, self.btn_auto, self.btn_export,
                       self.path_edit):
            widget.setEnabled(enabled)
        if not enabled:
            self.hint.setText(tr("ws.empty"))
            self.stats.setText("")
            return

        try:
            self._bundle = collect(self.repos, self.workspace_id)
        except ValueError as exc:
            self.hint.setText(str(exc))
            return

        done = sum(1 for s in self._bundle.subtasks if s.result.strip())
        self.stats.setText(tr(
            "exp.stats",
            results=done,
            total=len(self._bundle.subtasks),
            files=len(self._bundle.files),
            reports=len(self._bundle.reports),
        ))

        nothing = done == 0 and not self._bundle.files
        self.empty.setVisible(nothing)
        self.btn_export.setEnabled(not nothing)

        self._apply_auto()

    def _apply_auto(self) -> None:
        """Подставляет автоопределённый формат и объясняет выбор."""
        if self._bundle is None:
            return
        fmt, reason = detect_format(self._bundle)
        index = self.format_box.findData(fmt)
        if index >= 0:
            self.format_box.setCurrentIndex(index)
        self.hint.setText(tr("exp.auto_hint", reason=reason))
        self._suggest_path()

    def _on_format_changed(self) -> None:
        self._suggest_path()
        fmt = self.format_box.currentData()
        # Файлы проекта имеют смысл только в архиве: в документ их не вложить.
        self.opt_files.setEnabled(fmt == "zip")
        if fmt != "zip":
            self.opt_files.setToolTip(tr("exp.files_zip_only"))
        else:
            self.opt_files.setToolTip("")

    def _suggest_path(self) -> None:
        if self._bundle is None:
            return
        fmt = self.format_box.currentData()
        PATHS.ensure()
        self.path_edit.setText(
            str(PATHS.exports_dir / suggest_filename(self._bundle, fmt))
        )

    def _options(self) -> ExportOptions:
        return ExportOptions(
            include_results=self.opt_results.isChecked(),
            include_reports=self.opt_reports.isChecked(),
            include_summaries=self.opt_summaries.isChecked(),
            include_incidents=self.opt_incidents.isChecked(),
            include_decisions=self.opt_decisions.isChecked(),
            include_files=self.opt_files.isChecked(),
            include_stats=self.opt_stats.isChecked(),
            anonymize=self.opt_anon.isChecked(),
        )

    # -- действия ------------------------------------------------------------
    def _browse(self) -> None:
        current = Path(self.path_edit.text() or str(PATHS.exports_dir))
        chosen, _ = QFileDialog.getSaveFileName(
            self, tr("exp.output"), str(current)
        )
        if chosen:
            self.path_edit.setText(chosen)

    def _export(self) -> None:
        if self._bundle is None:
            return
        raw = self.path_edit.text().strip()
        if not raw:
            warn(self, tr("exp.no_path"))
            return

        fmt = self.format_box.currentData()
        path = Path(raw).expanduser()
        self.btn_export.setEnabled(False)
        try:
            result = export(self._bundle, self._options(), fmt, path)
        except ExportError as exc:
            warn(self, str(exc))
            return
        except Exception as exc:  # noqa: BLE001
            warn(self, f"{type(exc).__name__}: {exc}")
            return
        finally:
            self.btn_export.setEnabled(True)

        self._last = result
        self.btn_open.setEnabled(True)
        note = f"\n{result.note}" if result.note else ""
        self.result_label.setText(
            tr("exp.done", path=str(result.path), size=_human(result.size)) + note
        )
        self.result_label.setObjectName("Ok")
        self.result_label.setStyleSheet("color: #3ecf8e;")

    def _open_folder(self) -> None:
        if self._last is None:
            return
        if not open_folder(self._last.path):
            warn(self, tr("exp.open_failed", path=str(self._last.path.parent)))


def _human(size: int) -> str:
    value = float(size)
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if value < 1024:
            return f"{value:.0f} {unit}"
        value /= 1024
    return f"{value:.1f} ТБ"
````

### `ui/pages/settings_page.py`

*450 строк*

````python
"""Страница настроек: приложение + настройки активного воркспейса.

Здесь же выбирается режим супервайзера (ответ на вопрос 8): либо один из
подключённых API-ключей/агентов, либо локальная модель через Ollama —
например Qwen, которая работает офлайн и ничего не стоит.
"""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.config import DEFAULT_WORKSPACE_SETTINGS, AppSettings
from app.i18n import available_languages, current_language, set_language, tr
from core.tools.sandbox import docker_available
from storage.repositories import Repos
from ui.widgets.common import Card, Header, info, warn

MIN_PASSWORD_LEN = 8


class PasswordDialog(QDialog):
    """Смена пароля профиля с перешифровкой всех API-ключей."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("settings.change_password"))
        self.setMinimumWidth(420)
        lay = QVBoxLayout(self)
        lay.setSpacing(10)

        lay.addWidget(QLabel("Текущий пароль"))
        self.old = QLineEdit()
        self.old.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.old)

        lay.addWidget(QLabel(tr("login.password")))
        self.new1 = QLineEdit()
        self.new1.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.new1)

        lay.addWidget(QLabel(tr("login.password2")))
        self.new2 = QLineEdit()
        self.new2.setEchoMode(QLineEdit.EchoMode.Password)
        lay.addWidget(self.new2)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        lay.addWidget(buttons)

    def values(self) -> tuple[str, str, str]:
        return self.old.text(), self.new1.text(), self.new2.text()


class SettingsPage(QWidget):
    """Настройки приложения и текущего воркспейса."""

    theme_changed = object  # заменяется сигналом в main_window через callback

    def __init__(self, repos: Repos, app_settings: AppSettings,
                 on_theme_change=None, on_language_change=None) -> None:
        super().__init__()
        self.repos = repos
        self.app_settings = app_settings
        self.on_theme_change = on_theme_change
        self.on_language_change = on_language_change
        self.workspace_id: int | None = None

        root = QVBoxLayout(self)
        root.setContentsMargins(24, 24, 24, 24)
        root.setSpacing(16)
        root.addWidget(Header(tr("settings.title")))

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)
        root.addWidget(scroll, 1)
        page = QWidget()
        scroll.setWidget(page)
        lay = QVBoxLayout(page)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(14)

        lay.addWidget(self._build_app_card())
        self.ws_card = self._build_workspace_card()
        lay.addWidget(self.ws_card)
        lay.addWidget(self._build_security_card())
        lay.addStretch(1)

    # -- карточки ------------------------------------------------------------
    def _build_app_card(self) -> Card:
        card = Card(self)
        title = QLabel("Приложение")
        title.setObjectName("H2")
        card.body.addWidget(title)

        row = QHBoxLayout()
        lang_col = QVBoxLayout()
        lang_col.addWidget(QLabel(tr("settings.language")))
        self.lang_box = QComboBox()
        for code, label in available_languages():
            self.lang_box.addItem(label, code)
        idx = self.lang_box.findData(current_language())
        self.lang_box.setCurrentIndex(max(0, idx))
        self.lang_box.currentIndexChanged.connect(self._change_language)
        lang_col.addWidget(self.lang_box)
        row.addLayout(lang_col)

        theme_col = QVBoxLayout()
        theme_col.addWidget(QLabel(tr("settings.theme")))
        self.theme_box = QComboBox()
        self.theme_box.addItem("Тёмная", "dark")
        self.theme_box.addItem("Светлая", "light")
        self.theme_box.setCurrentIndex(0 if self.app_settings.theme == "dark" else 1)
        self.theme_box.currentIndexChanged.connect(self._change_theme)
        theme_col.addWidget(self.theme_box)
        row.addLayout(theme_col)
        row.addStretch(1)
        card.body.addLayout(row)

        note = QLabel(tr("settings.restart_note"))
        note.setObjectName("Dim")
        card.body.addWidget(note)
        return card

    def _build_workspace_card(self) -> Card:
        card = Card(self)
        title = QLabel("Воркспейс")
        title.setObjectName("H2")
        card.body.addWidget(title)

        self.hitl = QCheckBox(tr("settings.hitl"))
        self.hitl.stateChanged.connect(self._on_hitl_toggled)
        card.body.addWidget(self.hitl)

        hitl_row = QHBoxLayout()
        conf_col = QVBoxLayout()
        conf_col.addWidget(QLabel(tr("settings.hitl_threshold")))
        self.hitl_threshold = QDoubleSpinBox()
        self.hitl_threshold.setRange(0.0, 1.0)
        self.hitl_threshold.setSingleStep(0.05)
        self.hitl_threshold.setDecimals(2)
        self.hitl_threshold.setToolTip(tr("settings.hitl_threshold_hint"))
        self.hitl_threshold.valueChanged.connect(self._save_workspace)
        conf_col.addWidget(self.hitl_threshold)
        hitl_row.addLayout(conf_col)
        hitl_row.addStretch(1)
        card.body.addLayout(hitl_row)

        self.hitl_milestone = QCheckBox(tr("settings.hitl_milestone"))
        self.hitl_milestone.setToolTip(tr("settings.hitl_milestone_hint"))
        self.hitl_milestone.stateChanged.connect(self._save_workspace)
        card.body.addWidget(self.hitl_milestone)

        card.body.addWidget(QLabel(tr("settings.supervisor_mode")))
        self.sup_mode = QComboBox()
        self.sup_mode.addItem(tr("settings.supervisor_api"), "api")
        self.sup_mode.addItem(tr("settings.supervisor_local"), "local")
        self.sup_mode.currentIndexChanged.connect(self._on_sup_mode)
        card.body.addWidget(self.sup_mode)

        self.sup_agent = QComboBox()
        card.body.addWidget(self.sup_agent)
        self.sup_agent.currentIndexChanged.connect(self._save_workspace)

        local_row = QHBoxLayout()
        local_col = QVBoxLayout()
        local_col.addWidget(QLabel("Локальная модель (Ollama)"))
        self.sup_local_model = QLineEdit()
        self.sup_local_model.editingFinished.connect(self._save_workspace)
        local_col.addWidget(self.sup_local_model)
        local_row.addLayout(local_col, 1)

        url_col = QVBoxLayout()
        url_col.addWidget(QLabel("Base URL"))
        self.sup_local_url = QLineEdit()
        self.sup_local_url.editingFinished.connect(self._save_workspace)
        url_col.addWidget(self.sup_local_url)
        local_row.addLayout(url_col, 1)
        card.body.addLayout(local_row)

        interval_row = QHBoxLayout()
        int_col = QVBoxLayout()
        int_col.addWidget(QLabel(tr("settings.summary_interval")))
        self.summary_interval = QSpinBox()
        self.summary_interval.setRange(1, 600)
        self.summary_interval.valueChanged.connect(self._save_workspace)
        int_col.addWidget(self.summary_interval)
        interval_row.addLayout(int_col)

        steps_col = QVBoxLayout()
        steps_col.addWidget(QLabel("Шагов ReAct на подзадачу"))
        self.max_steps = QSpinBox()
        self.max_steps.setRange(1, 50)
        self.max_steps.valueChanged.connect(self._save_workspace)
        steps_col.addWidget(self.max_steps)
        interval_row.addLayout(steps_col)
        interval_row.addStretch(1)
        card.body.addLayout(interval_row)

        self.summary_on_event = QCheckBox(tr("settings.summary_on_event"))
        self.summary_on_event.stateChanged.connect(self._save_workspace)
        card.body.addWidget(self.summary_on_event)

        # --- песочница ---
        sandbox_title = QLabel(tr("settings.sandbox"))
        sandbox_title.setObjectName("H2")
        card.body.addWidget(sandbox_title)

        sandbox_row = QHBoxLayout()
        back_col = QVBoxLayout()
        back_col.addWidget(QLabel("Бэкенд"))
        self.sandbox_backend = QComboBox()
        self.sandbox_backend.addItem("Авто", "auto")
        self.sandbox_backend.addItem("Отдельный процесс", "subprocess")
        self.sandbox_backend.addItem("Docker", "docker")
        self.sandbox_backend.currentIndexChanged.connect(self._save_workspace)
        back_col.addWidget(self.sandbox_backend)
        sandbox_row.addLayout(back_col, 1)

        to_col = QVBoxLayout()
        to_col.addWidget(QLabel("Таймаут, с"))
        self.sandbox_timeout = QSpinBox()
        self.sandbox_timeout.setRange(5, 600)
        self.sandbox_timeout.valueChanged.connect(self._save_workspace)
        to_col.addWidget(self.sandbox_timeout)
        sandbox_row.addLayout(to_col)

        mem_col = QVBoxLayout()
        mem_col.addWidget(QLabel("Память, МБ"))
        self.sandbox_memory = QSpinBox()
        self.sandbox_memory.setRange(64, 8192)
        self.sandbox_memory.setSingleStep(64)
        self.sandbox_memory.valueChanged.connect(self._save_workspace)
        mem_col.addWidget(self.sandbox_memory)
        sandbox_row.addLayout(mem_col)
        card.body.addLayout(sandbox_row)

        self.docker_note = QLabel("")
        self.docker_note.setObjectName("Dim")
        self.docker_note.setWordWrap(True)
        card.body.addWidget(self.docker_note)

        # --- разрешённые каталоги ---
        paths_title = QLabel(tr("settings.allowed_paths"))
        paths_title.setObjectName("H2")
        card.body.addWidget(paths_title)

        self.paths_list = QListWidget()
        self.paths_list.setMaximumHeight(120)
        card.body.addWidget(self.paths_list)

        paths_buttons = QHBoxLayout()
        btn_add_path = QPushButton(tr("settings.add_path"))
        btn_add_path.clicked.connect(self._add_path)
        paths_buttons.addWidget(btn_add_path)
        btn_del_path = QPushButton(tr("common.delete"))
        btn_del_path.setObjectName("Danger")
        btn_del_path.clicked.connect(self._remove_path)
        paths_buttons.addWidget(btn_del_path)
        paths_buttons.addStretch(1)
        card.body.addLayout(paths_buttons)

        warning = QLabel(
            "Агенты получают доступ на чтение и запись в эти каталоги. "
            "Не добавляйте сюда системные папки и каталоги с личными данными."
        )
        warning.setObjectName("Dim")
        warning.setWordWrap(True)
        card.body.addWidget(warning)
        return card

    def _build_security_card(self) -> Card:
        card = Card(self)
        title = QLabel("Безопасность")
        title.setObjectName("H2")
        card.body.addWidget(title)

        text = QLabel(
            "API-ключи зашифрованы AES-256-GCM. Ключ шифрования выводится из пароля "
            "профиля функцией Argon2id и существует только в оперативной памяти."
        )
        text.setObjectName("Dim")
        text.setWordWrap(True)
        card.body.addWidget(text)

        btn = QPushButton(tr("settings.change_password"))
        btn.clicked.connect(self._change_password)
        card.body.addWidget(btn)
        return card

    # -- загрузка/сохранение -------------------------------------------------
    def set_workspace(self, ws_id: int | None) -> None:
        self.workspace_id = ws_id
        self.ws_card.setEnabled(ws_id is not None)
        if ws_id is None:
            return
        ws = self.repos.workspaces.get(ws_id)
        if ws is None:
            return
        s = {**DEFAULT_WORKSPACE_SETTINGS, **ws.settings}

        self._loading = True
        self.hitl.setChecked(bool(s["human_in_the_loop"]))
        self.hitl_threshold.setValue(float(s.get("hitl_confidence_threshold", 0.5)))
        self.hitl_milestone.setChecked(bool(s.get("hitl_pause_on_milestone", False)))
        self._sync_hitl_enabled()
        self.sup_mode.setCurrentIndex(0 if s["supervisor_mode"] == "api" else 1)

        self.sup_agent.clear()
        self.sup_agent.addItem(tr("common.none"), None)
        for agent in self.repos.agents.list(ws_id):
            self.sup_agent.addItem(f"{agent.name} — {agent.model}", agent.id)
        idx = self.sup_agent.findData(s.get("supervisor_agent_id"))
        self.sup_agent.setCurrentIndex(max(0, idx))

        self.sup_local_model.setText(str(s["supervisor_local_model"]))
        self.sup_local_url.setText(str(s["supervisor_local_base_url"]))
        self.summary_interval.setValue(int(s["summary_interval_minutes"]))
        self.summary_on_event.setChecked(bool(s["summary_on_event"]))
        self.max_steps.setValue(int(s["agent_max_steps"]))

        i = self.sandbox_backend.findData(s["sandbox_backend"])
        self.sandbox_backend.setCurrentIndex(max(0, i))
        self.sandbox_timeout.setValue(int(s["sandbox_timeout_sec"]))
        self.sandbox_memory.setValue(int(s["sandbox_memory_mb"]))

        self.paths_list.clear()
        self.paths_list.addItems([str(p) for p in s.get("extra_allowed_paths", [])])

        self.docker_note.setText(
            "Docker найден — доступна полная изоляция сети и файловой системы."
            if docker_available() else
            "Docker не найден. Будет использован режим отдельного процесса: "
            "ограничены CPU, память, размер файлов и переменные окружения, "
            "но это не полная изоляция."
        )
        self._on_sup_mode()
        self._loading = False

    def refresh(self) -> None:
        """Перечитывает настройки: список агентов мог измениться после входа на страницу."""
        self.set_workspace(self.workspace_id)

    def _save_workspace(self) -> None:
        if self.workspace_id is None or getattr(self, "_loading", False):
            return
        ws = self.repos.workspaces.get(self.workspace_id)
        if ws is None:
            return
        s = {**DEFAULT_WORKSPACE_SETTINGS, **ws.settings}
        s.update({
            "human_in_the_loop": self.hitl.isChecked(),
            "hitl_confidence_threshold": round(self.hitl_threshold.value(), 2),
            "hitl_pause_on_milestone": self.hitl_milestone.isChecked(),
            "supervisor_mode": self.sup_mode.currentData(),
            "supervisor_agent_id": self.sup_agent.currentData(),
            "supervisor_local_model": self.sup_local_model.text().strip(),
            "supervisor_local_base_url": self.sup_local_url.text().strip(),
            "summary_interval_minutes": self.summary_interval.value(),
            "summary_on_event": self.summary_on_event.isChecked(),
            "agent_max_steps": self.max_steps.value(),
            "sandbox_backend": self.sandbox_backend.currentData(),
            "sandbox_timeout_sec": self.sandbox_timeout.value(),
            "sandbox_memory_mb": self.sandbox_memory.value(),
            "extra_allowed_paths": [self.paths_list.item(i).text()
                                    for i in range(self.paths_list.count())],
        })
        self.repos.workspaces.update(self.workspace_id, settings=s)

    def _on_hitl_toggled(self) -> None:
        self._sync_hitl_enabled()
        self._save_workspace()

    def _sync_hitl_enabled(self) -> None:
        """Настройки пауз бессмысленны при выключенном human-in-the-loop."""
        enabled = self.hitl.isChecked()
        self.hitl_threshold.setEnabled(enabled)
        self.hitl_milestone.setEnabled(enabled)

    def _on_sup_mode(self) -> None:
        local = self.sup_mode.currentData() == "local"
        self.sup_agent.setVisible(not local)
        self.sup_local_model.setEnabled(local)
        self.sup_local_url.setEnabled(local)
        self._save_workspace()

    # -- действия ------------------------------------------------------------
    def _change_language(self) -> None:
        code = self.lang_box.currentData()
        set_language(code)
        self.app_settings.language = code
        self.app_settings.save()
        if self.on_language_change:
            self.on_language_change(code)

    def _change_theme(self) -> None:
        theme = self.theme_box.currentData()
        self.app_settings.theme = theme
        self.app_settings.save()
        if self.on_theme_change:
            self.on_theme_change(theme)

    def _add_path(self) -> None:
        folder = QFileDialog.getExistingDirectory(self, tr("settings.add_path"),
                                                  str(Path.home()))
        if folder:
            self.paths_list.addItem(folder)
            self._save_workspace()

    def _remove_path(self) -> None:
        for item in self.paths_list.selectedItems():
            self.paths_list.takeItem(self.paths_list.row(item))
        self._save_workspace()

    def _change_password(self) -> None:
        dlg = PasswordDialog(self)
        if dlg.exec() != QDialog.DialogCode.Accepted:
            return
        old, new1, new2 = dlg.values()
        if len(new1) < MIN_PASSWORD_LEN:
            warn(self, tr("login.password_short"))
            return
        if new1 != new2:
            warn(self, tr("login.password_mismatch"))
            return
        if self.repos.users.change_password(self.repos.session, old, new1):
            info(self, "Пароль изменён, API-ключи перешифрованы.")
        else:
            warn(self, tr("login.bad_credentials"))
````


## Служебное

### `utils/asyncutils.py`

*68 строк*

````python
"""Мост между Qt и asyncio.

Ответ на вопрос 2: в приложении ОДИН asyncio-луп, который qasync делает
общим с циклом событий Qt. Агенты — это корутины/таски в этом лупе, поэтому
15+ параллельных агентов не превращаются в 15 потоков. Блокирующие вызовы
(sqlite, ddgs, чтение файлов) уводятся в пул потоков через ``asyncio.to_thread``,
исполнение кода — в отдельный процесс.
"""

from __future__ import annotations

import asyncio
import logging
import traceback
from typing import Any, Awaitable, Callable

log = logging.getLogger("aiorc.async")


def run_async(
    coro: Awaitable[Any],
    on_done: Callable[[Any], None] | None = None,
    on_error: Callable[[Exception], None] | None = None,
) -> asyncio.Task:
    """Запускает корутину в текущем лупе и безопасно возвращает результат в UI.

    Колбэки вызываются уже в лупе Qt, поэтому им разрешено трогать виджеты.
    """
    task = asyncio.ensure_future(coro)

    def _callback(t: asyncio.Task) -> None:
        if t.cancelled():
            return
        exc = t.exception()
        if exc is not None:
            log.error("Async task failed: %s\n%s", exc,
                      "".join(traceback.format_exception(exc)))
            if on_error:
                on_error(exc)  # type: ignore[arg-type]
            return
        if on_done:
            on_done(t.result())

    task.add_done_callback(_callback)
    return task


class TaskGroup:
    """Простой учёт фоновых задач воркспейса, чтобы уметь их остановить."""

    def __init__(self) -> None:
        self._tasks: set[asyncio.Task] = set()

    def spawn(self, coro: Awaitable[Any], name: str = "") -> asyncio.Task:
        task = asyncio.ensure_future(coro)
        if name:
            task.set_name(name)
        self._tasks.add(task)
        task.add_done_callback(self._tasks.discard)
        return task

    def cancel_all(self) -> None:
        for task in list(self._tasks):
            task.cancel()
        self._tasks.clear()

    def active(self) -> int:
        return sum(1 for t in self._tasks if not t.done())
````

### `utils/logging_setup.py`

*33 строк*

````python
"""Настройка логирования: файл с ротацией + консоль."""

from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler

from app.config import PATHS

_FORMAT = "%(asctime)s  %(levelname)-7s  %(name)-22s  %(message)s"


def setup_logging(level: int = logging.INFO) -> None:
    PATHS.ensure()
    root = logging.getLogger()
    if root.handlers:  # уже настроено
        return
    root.setLevel(level)

    file_handler = RotatingFileHandler(
        PATHS.logs_dir / "app.log", maxBytes=2_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(logging.Formatter(_FORMAT))
    root.addHandler(file_handler)

    console = logging.StreamHandler(sys.stderr)
    console.setFormatter(logging.Formatter(_FORMAT))
    root.addHandler(console)

    # Библиотеки не должны заливать лог.
    for noisy in ("httpx", "httpcore", "urllib3", "asyncio"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
````

### `tests/smoke.py`

*489 строк*

````python
"""Смоук-тесты ядра: все девять этапов MVP без сети и без GUI.

Запуск::

    python tests/smoke.py

Модели подменяются фейковыми провайдерами, поэтому тесты не ходят в интернет,
не тратят токены и выполняются за секунды. Проверяется именно логика ядра:
шифрование, изоляция агентов, конвейер выполнения, супервайзер, паузы,
экспорт и бюджеты. Интерфейс сюда не входит — его надо смотреть глазами.
"""

from __future__ import annotations

import asyncio
import itertools
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Изолированный каталог данных, чтобы не трогать реальный профиль.
_TEMP_HOME = Path(tempfile.mkdtemp(prefix="aiorc_smoke_"))
os.environ["AIORC_HOME"] = str(_TEMP_HOME)

from app.config import DEFAULT_WORKSPACE_SETTINGS, PATHS  # noqa: E402
from core.budget import load_states  # noqa: E402
from core.events import EventBus, EventType  # noqa: E402
from core.export.bundle import ExportOptions, collect, detect_format  # noqa: E402
from core.export.exporters import export, suggest_filename  # noqa: E402
from core.hitl import Decision  # noqa: E402
import core.orchestrator as orchestrator_module  # noqa: E402
from core.orchestrator import Orchestrator  # noqa: E402
from core.supervisor.supervisor import Supervisor, SupervisorModel  # noqa: E402
from providers.base import CompletionResult, LLMProvider, ToolCall, Usage  # noqa: E402
from storage.db import Database  # noqa: E402
from storage.repositories import Repos, UserRepo  # noqa: E402

_counter = itertools.count()
_passed: list[str] = []
_failed: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    """Печатает результат одной проверки и копит статистику."""
    mark = "OK  " if condition else "FAIL"
    print(f"  [{mark}] {name}" + (f" — {detail}" if detail else ""))
    (_passed if condition else _failed).append(name)


# ---------------------------------------------------------------------------
# Подменные провайдеры
# ---------------------------------------------------------------------------


class Worker(LLMProvider):
    """Исполнитель: при наличии инструментов сначала вызывает один из них."""

    def __init__(self, name: str = "agent", confidence: str = "0.9",
                 use_tool: bool = False, tokens: tuple[int, int] = (200, 80)) -> None:
        super().__init__()
        self.name = name
        self.confidence = confidence
        self.use_tool = use_tool
        self.tokens = tokens
        self.calls = 0

    async def list_models(self) -> list[str]:
        return ["fake-model"]

    async def aclose(self) -> None:
        return None

    async def complete(self, model, messages, *, temperature=0.7,
                       max_tokens=2048, tools=None):
        self.calls += 1
        if self.use_tool and self.calls == 1 and tools:
            return CompletionResult(
                text="Посчитаю в песочнице.",
                tool_calls=[ToolCall("call-1", "code_exec",
                                     {"code": "print(6 * 7)", "language": "python"})],
                usage=Usage(*self.tokens),
            )
        return CompletionResult(
            text=(f"Готово.\nCONFIDENCE: {self.confidence}\n"
                  f"RESULT:\nРезультат от {self.name}, попытка {self.calls}."),
            usage=Usage(*self.tokens),
        )


class SupervisorProvider(LLMProvider):
    """Проверяющий: вердикты задаются списком, остальное — заглушки."""

    def __init__(self, verdicts: list[str] | None = None,
                 conflicts: str = '{"conflicts": []}') -> None:
        super().__init__()
        self.verdicts = verdicts or []
        self.conflicts = conflicts
        self.reviews = 0

    async def list_models(self) -> list[str]:
        return ["fake-model"]

    async def aclose(self) -> None:
        return None

    async def complete(self, model, messages, **kwargs):
        system, user = messages[0].content, messages[1].content
        if "ПРОВЕРЯЕМАЯ ПОДЗАДАЧА" in user:
            self.reviews += 1
            if self.reviews <= len(self.verdicts):
                return CompletionResult(text=self.verdicts[self.reviews - 1],
                                        usage=Usage(150, 40))
            return CompletionResult(text='{"verdict":"ok","notes":"","issues":[]}',
                                    usage=Usage(150, 20))
        if "Сравни результаты" in system:
            return CompletionResult(text=self.conflicts, usage=Usage(120, 40))
        return CompletionResult(
            text=("ФАКТЫ:\nработа идёт\nРАСХОЖДЕНИЯ:\nнет\nОТКРЫТЫЕ ВОПРОСЫ:\nнет"),
            usage=Usage(120, 50),
        )


def patch_supervisor(provider: SupervisorProvider) -> None:
    """Подменяет модель супервайзера, не трогая остальную его логику."""

    class Patched(Supervisor):
        def _resolve_model(self):
            if self._model is None:
                self._model = SupervisorModel(provider, "fake-model", "openai",
                                              "api", "тестовый супервайзер")
            return self._model

    orchestrator_module.Supervisor = Patched


# ---------------------------------------------------------------------------
# Каркас сценария
# ---------------------------------------------------------------------------


def build_project(subtask_count: int = 2, agent_count: int = 2,
                  settings: dict | None = None, token_limit: int | None = None):
    """Создаёт профиль, воркспейс, агентов и задачу."""
    db = Database()
    session = UserRepo(db).create(f"smoke{next(_counter)}", "password123")
    repos = Repos(db, session)

    config = dict(DEFAULT_WORKSPACE_SETTINGS)
    config.update(summary_interval_minutes=0, human_in_the_loop=False,
                  max_rework_rounds=1)
    config.update(settings or {})

    workspace = repos.workspaces.create(session.user_id, "Смоук-проект", "", config)
    key = repos.keys.create("Тестовый ключ", "openai", "sk-secret-value", "")

    agents = [
        repos.agents.create(workspace.id, f"Агент {i + 1}", "analyst",
                            "Ты исполнитель.", key.id, "openai", "gpt-4o-mini",
                            {"temperature": 0.3, "max_tokens": 512,
                             "tools": ["code_exec"]})
        for i in range(agent_count)
    ]
    supervisor = repos.agents.create(workspace.id, "Супервайзер", "supervisor",
                                     "Ты проверяющий.", key.id, "openai",
                                     "gpt-4o-mini", {}, is_supervisor=True)
    repos.workspaces.update(workspace.id,
                            settings={**config, "supervisor_agent_id": supervisor.id})

    task = repos.tasks.create(workspace.id, "Смоук-задача",
                              "Проверить работу конвейера", "auto", token_limit)
    for i in range(subtask_count):
        repos.tasks.add_subtask(task.id, f"Подзадача {i + 1}", "",
                                agents[i % len(agents)].id)
    return repos, workspace, task, agents, key


async def drive(orch: Orchestrator, workspace_id: int, task_id: int,
                answers: list[tuple[Decision, str]] | None = None,
                fallback: Decision = Decision.APPROVE, timeout: float = 30.0):
    """Запускает прогон, отвечая на вопросы human-in-the-loop по сценарию."""
    plan = list(answers or [])

    async def responder() -> None:
        while True:
            gate = orch.gate
            if gate and gate.pending():
                request = gate.pending()[0]
                decision, comment = plan.pop(0) if plan else (fallback, "авто")
                gate.resolve(request.id, decision, comment)
            await asyncio.sleep(0.02)

    helper = asyncio.ensure_future(responder())
    try:
        return await asyncio.wait_for(orch.run_task(workspace_id, task_id), timeout)
    finally:
        helper.cancel()


# ---------------------------------------------------------------------------
# Сценарии
# ---------------------------------------------------------------------------


def test_storage_and_crypto() -> None:
    print("\n[1-3] Хранилище, шифрование ключей, задачи")
    repos, workspace, task, agents, key = build_project()

    check("профиль создан и пароль проверяется",
          repos.users.authenticate(repos.session.username, "password123") is not None)
    check("неверный пароль отвергается",
          repos.users.authenticate(repos.session.username, "wrong") is None)

    row = repos.db.query_one("SELECT secret_blob FROM api_keys WHERE id = ?", (key.id,))
    check("секрет не лежит в БД открытым текстом",
          b"sk-secret-value" not in row["secret_blob"])
    check("секрет расшифровывается", repos.keys.reveal(key.id) == "sk-secret-value")

    repos.users.change_password(repos.session, "password123", "newpassword456")
    check("после смены пароля ключ читается",
          repos.keys.reveal(key.id) == "sk-secret-value",
          "перешифровка выполнена")

    check("подзадачи привязаны к агентам",
          all(s.agent_id for s in repos.tasks.subtasks(task.id)))


async def test_pipeline() -> None:
    print("\n[4] Конвейер: ReAct, инструменты, зависимости, изоляция")
    repos, workspace, task, agents, _ = build_project(subtask_count=2)
    subtasks = repos.tasks.subtasks(task.id)
    repos.tasks.update_subtask(subtasks[1].id, depends_on=str(subtasks[0].id))

    bus = EventBus()
    seen: list[tuple] = []
    bus.subscribe(lambda e: seen.append((e.type, e.subtask_id)))

    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, bus)
    workers = {a.id: Worker(a.name, use_tool=(i == 0))
               for i, a in enumerate(agents)}
    orch._provider_for = lambda agent: workers.get(agent.id, Worker(agent.name))

    state = await drive(orch, workspace.id, task.id)

    check("обе подзадачи выполнены", state.finished == 2 and state.failed == 0,
          f"finished={state.finished}, failed={state.failed}")
    check("результаты сохранены",
          all(s.result.strip() for s in repos.tasks.subtasks(task.id)))
    check("инструмент code_exec отработал", workers[agents[0].id].calls >= 2,
          f"вызовов модели: {workers[agents[0].id].calls}")

    started = [s for t, s in seen if t is EventType.SUBTASK_STARTED]
    finished = [s for t, s in seen if t is EventType.SUBTASK_FINISHED]
    check("зависимость соблюдена",
          finished and started.index(subtasks[1].id) > 0
          and subtasks[0].id in finished[:started.index(subtasks[1].id) + 1])

    history_one = repos.messages.history(agents[0].id)
    history_two = repos.messages.history(agents[1].id)
    check("истории агентов изолированы",
          bool(history_one) and bool(history_two)
          and all(m["agent_id"] == agents[1].id for m in history_two),
          f"{len(history_one)} и {len(history_two)} сообщений")
    check("отчёты созданы", len(repos.reports.list_reports(workspace.id)) == 2)


async def test_supervisor() -> None:
    print("\n[5] Супервайзер: доработка, анонимизация, конфликты")
    repos, workspace, task, agents, _ = build_project(subtask_count=2)
    repos.agents.update(agents[0].id, name="Аналитик Пётр")
    repos.agents.update(agents[1].id, name="Критик Анна")

    provider = SupervisorProvider(
        verdicts=['{"verdict":"rework","notes":"Нет источников.",'
                  '"issues":[{"kind":"factual_error","severity":"high",'
                  '"description":"Цифры без источника"}]}'],
        conflicts='{"conflicts":[{"description":"Оценки расходятся",'
                  '"severity":"high","labels":[],"auto_resolvable":false,'
                  '"resolution":""},'
                  '{"description":"Мелкое расхождение в дате",'
                  '"severity":"low","labels":[],"auto_resolvable":true,'
                  '"resolution":"Верна более свежая дата"}]}',
    )
    patch_supervisor(provider)
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: Worker(agent.name)

    state = await drive(orch, workspace.id, task.id)

    check("доработка назначена и выполнена", state.reworks == 1,
          f"reworks={state.reworks}")
    check("после доработки результат принят",
          all(s.status == "done" for s in repos.tasks.subtasks(task.id)))

    summaries = repos.reports.list_summaries(workspace.id)
    leaked = [s for s in summaries if "Пётр" in s.content or "Анна" in s.content]
    check("имена агентов не утекают в сводки", not leaked and bool(summaries),
          f"сводок: {len(summaries)}")

    incidents = repos.incidents.list(workspace.id)
    auto = [i for i in incidents if i.status == "auto_resolved"]
    escalated = [i for i in incidents if i.status == "escalated"]
    closed = [i for i in incidents if i.status == "resolved"]
    check("конфликт разрешён автоматически", len(auto) == 1)
    check("неразрешимый конфликт эскалирован", len(escalated) == 1)
    check("замечание закрыто после доработки", len(closed) >= 1)


async def test_hitl() -> None:
    print("\n[7] Human-in-the-loop: пауза, доработка, остановка")
    repos, workspace, task, agents, _ = build_project(
        subtask_count=1,
        settings={"human_in_the_loop": True, "hitl_confidence_threshold": 0.9,
                  "max_rework_rounds": 0},
    )
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, EventBus())
    worker = Worker("Агент", confidence="0.4")
    orch._provider_for = lambda agent: worker

    state = await drive(orch, workspace.id, task.id,
                        answers=[(Decision.REWORK, "Добавь источники"),
                                 (Decision.APPROVE, "теперь годится")])
    subtask = repos.tasks.subtasks(task.id)[0]
    check("пауза по низкой уверенности сработала", worker.calls == 2,
          f"вызовов модели: {worker.calls}")
    check("решение пользователя дало круг доработки", subtask.rework_count == 1)
    check("после подтверждения подзадача закрыта", subtask.status == "done")
    check("история решений записана",
          len(repos.approvals.history(workspace.id)) == 2)

    # Защита от бесконечного цикла: человек возвращает работу снова и снова.
    repos2, ws2, task2, agents2, _ = build_project(
        subtask_count=1,
        settings={"human_in_the_loop": True, "hitl_confidence_threshold": 0.9,
                  "max_rework_rounds": 0},
    )
    patch_supervisor(SupervisorProvider())
    orch2 = Orchestrator(repos2, EventBus())
    stubborn = Worker("Агент", confidence="0.4")
    orch2._provider_for = lambda agent: stubborn
    await drive(orch2, ws2.id, task2.id, fallback=Decision.REWORK)
    check("потолок доработок человека держится", stubborn.calls == 4,
          f"вызовов модели: {stubborn.calls} (1 + 3 круга)")

    # Остановка прогона решением пользователя.
    repos3, ws3, task3, agents3, _ = build_project(
        subtask_count=3,
        settings={"human_in_the_loop": True, "hitl_confidence_threshold": 0.9,
                  "max_rework_rounds": 0},
    )
    patch_supervisor(SupervisorProvider())
    orch3 = Orchestrator(repos3, EventBus())
    orch3._provider_for = lambda agent: Worker(agent.name, confidence="0.4")
    state3 = await drive(orch3, ws3.id, task3.id, fallback=Decision.ABORT)
    statuses = [s.status for s in repos3.tasks.subtasks(task3.id)]
    check("остановка прогона работает",
          state3.finished == 0 and statuses.count("idle") >= 1,
          f"статусы: {statuses}")


async def test_budget() -> None:
    print("\n[9] Бюджеты: блокировка и алерты")
    repos, workspace, task, agents, _ = build_project(subtask_count=3, agent_count=1)
    subtasks = repos.tasks.subtasks(task.id)
    for previous, current in zip(subtasks, subtasks[1:]):
        repos.tasks.update_subtask(current.id, depends_on=str(previous.id))

    repos.budgets.upsert("agent", agents[0].id, 400, None, 0.5)

    events: list[str] = []
    bus = EventBus()
    bus.subscribe(lambda e: events.append(e.type.value)
                  if e.type in (EventType.BUDGET_ALERT, EventType.BUDGET_EXCEEDED)
                  else None)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, bus)
    worker = Worker("Агент", tokens=(300, 100))
    orch._provider_for = lambda agent: worker

    state = await drive(orch, workspace.id, task.id)
    statuses = [s.status for s in repos.tasks.subtasks(task.id)]

    check("лимит остановил работу", worker.calls == 1,
          f"вызовов модели: {worker.calls}")
    check("заблокированные подзадачи помечены ошибкой",
          statuses.count("error") == 2, f"статусы: {statuses}")
    check("событие о превышении опубликовано", "budget_exceeded" in events)

    states = load_states(repos, workspace.id)
    scopes = {s.scope for s in states}
    check("бюджет считается на трёх уровнях",
          {"workspace", "task", "agent"} <= scopes, f"уровни: {sorted(scopes)}")


async def test_export() -> None:
    print("\n[8] Экспорт результата")
    repos, workspace, task, agents, _ = build_project(subtask_count=2)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: Worker(agent.name)
    await drive(orch, workspace.id, task.id)

    bundle = collect(repos, workspace.id)
    fmt, reason = detect_format(bundle)
    check("формат определяется автоматически", bool(fmt) and bool(reason),
          f"{fmt}: {reason}")

    out = _TEMP_HOME / "exports"
    out.mkdir(parents=True, exist_ok=True)
    options = ExportOptions(include_reports=True, include_summaries=True)

    result = export(bundle, options, "markdown", out / suggest_filename(bundle, "markdown"))
    body = result.path.read_text("utf-8")
    check("markdown собран", result.size > 0 and "# " in body, f"{result.size} байт")
    check("результаты подзадач попали в документ", "Результат" in body)

    for optional, module in (("docx", "docx"), ("pdf", "reportlab")):
        try:
            __import__(module)
        except ImportError:
            print(f"  [SKIP] {optional} — пакет {module} не установлен")
            continue
        result = export(bundle, options, optional,
                        out / suggest_filename(bundle, optional))
        check(f"{optional} собран", result.size > 0, f"{result.size} байт")

    # ZIP: в рабочем каталоге появляются файлы проекта
    workspace_dir = PATHS.workspace_dir(workspace.id)
    (workspace_dir / "src").mkdir(parents=True, exist_ok=True)
    (workspace_dir / "src" / "main.py").write_text("print('привет')\n", "utf-8")
    (workspace_dir / ".sandbox").mkdir(exist_ok=True)
    (workspace_dir / ".sandbox" / "junk.py").write_text("мусор", "utf-8")

    bundle = collect(repos, workspace.id)
    fmt, _ = detect_format(bundle)
    check("появление кода переключает формат на архив", fmt == "zip", fmt)

    result = export(bundle, options, "zip", out / suggest_filename(bundle, "zip"))
    import zipfile

    with zipfile.ZipFile(result.path) as archive:
        names = archive.namelist()
    check("архив содержит отчёт и манифест",
          "RESULT.md" in names and "manifest.json" in names)
    check("файлы проекта вложены", "files/src/main.py" in names)
    check("служебные каталоги исключены",
          not any(".sandbox" in name for name in names))


# ---------------------------------------------------------------------------


async def main() -> int:
    print("=" * 66)
    print("Смоук-тесты AI Orchestrator (без сети, без GUI)")
    print(f"Временный каталог данных: {_TEMP_HOME}")
    print("=" * 66)

    test_storage_and_crypto()
    await test_pipeline()
    await test_supervisor()
    await test_export()
    await test_hitl()
    await test_budget()

    print("\n" + "=" * 66)
    total = len(_passed) + len(_failed)
    if _failed:
        print(f"ПРОВАЛЕНО {len(_failed)} из {total}:")
        for name in _failed:
            print(f"  · {name}")
        return 1
    print(f"ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ: {total} из {total}")
    return 0


if __name__ == "__main__":
    code = 0
    try:
        code = asyncio.run(main())
    finally:
        shutil.rmtree(_TEMP_HOME, ignore_errors=True)
    sys.exit(code)
````

### `tests/ui_smoke.py`

*511 строк*

````python
"""Смоук-прогон интерфейса: полный пользовательский сценарий без сети.

Запуск::

    python tests/ui_smoke.py              # без окон (offscreen), скриншоты в temp
    python tests/ui_smoke.py --show       # с настоящими окнами
    python tests/ui_smoke.py --out DIR    # куда сложить скриншоты

Сценарий: создание профиля → воркспейс → ключ → агенты → задача и
автоматическое разбиение → прогон с паузой human-in-the-loop → супервайзер,
дашборд, бюджеты → экспорт во все форматы → смена темы и языка.

Модальные диалоги подменяются заполнителями, модели — фейковым провайдером.
Любое исключение в слоте Qt, в обработчике шины или в фоновой задаче
считается провалом.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
import tempfile
import traceback
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

parser = argparse.ArgumentParser()
parser.add_argument("--show", action="store_true", help="показывать настоящие окна")
parser.add_argument("--out", default="", help="каталог для скриншотов")
ARGS = parser.parse_args()

if not ARGS.show:
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    # offscreen-платформа сама системные шрифты не находит — без этого
    # на скриншотах вместо текста квадраты
    if sys.platform == "win32":
        os.environ.setdefault("QT_QPA_FONTDIR", os.path.join(os.environ.get("WINDIR", "C:\\Windows"), "Fonts"))
    elif sys.platform == "darwin":
        os.environ.setdefault("QT_QPA_FONTDIR", "/System/Library/Fonts")
    else:
        os.environ.setdefault("QT_QPA_FONTDIR", "/usr/share/fonts")
_TEMP_HOME = Path(tempfile.mkdtemp(prefix="aiorc_ui_"))
os.environ["AIORC_HOME"] = str(_TEMP_HOME)
SHOTS = Path(ARGS.out) if ARGS.out else _TEMP_HOME / "shots"
SHOTS.mkdir(parents=True, exist_ok=True)

import qasync  # noqa: E402
import shiboken6  # noqa: E402
from PySide6.QtWidgets import QApplication, QDialog, QMessageBox, QPushButton  # noqa: E402

from app.config import PATHS, AppSettings  # noqa: E402
from app.i18n import set_language  # noqa: E402
from core.hitl import DECISION_TITLES, Decision  # noqa: E402
from providers.base import CompletionResult, LLMProvider, ToolCall, Usage  # noqa: E402
from storage.db import Database  # noqa: E402
from ui.theme import stylesheet  # noqa: E402

# ---------------------------------------------------------------------------
# Сбор ошибок
# ---------------------------------------------------------------------------

ERRORS: list[str] = []
_passed: list[str] = []
_failed: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    mark = "OK  " if condition else "FAIL"
    print(f"  [{mark}] {name}" + (f" — {detail}" if detail else ""))
    (_passed if condition else _failed).append(name)


def _excepthook(kind, value, tb) -> None:
    ERRORS.append("".join(traceback.format_exception(kind, value, tb)))


class _ErrorLog(logging.Handler):
    """Ошибки, которые ядро глотает и пишет в лог (шина, run_async)."""

    def emit(self, record: logging.LogRecord) -> None:
        if record.levelno >= logging.ERROR:
            text = record.getMessage()
            if record.exc_info:
                text += "\n" + "".join(traceback.format_exception(*record.exc_info))
            ERRORS.append(text)


sys.excepthook = _excepthook
logging.getLogger().addHandler(_ErrorLog())
logging.getLogger().setLevel(logging.INFO)

# ---------------------------------------------------------------------------
# Фейковая модель: одна на всех, роль определяется по промпту
# ---------------------------------------------------------------------------


class FakeModel(LLMProvider):
    calls: dict[str, int] = {}

    async def list_models(self) -> list[str]:
        return ["fake-mini", "fake-large"]

    async def aclose(self) -> None:
        return None

    async def complete(self, model, messages, *, temperature=0.7,
                       max_tokens=2048, tools=None):
        await asyncio.sleep(0.05)
        system, user = messages[0].content, messages[-1].content
        joined = "\n".join(m.content for m in messages)
        if "планировщик работ" in system:
            return CompletionResult(
                text='{"subtasks": ['
                     '{"title": "Собрать требования", "description": "Опросить источники", '
                     '"assignee_role": "analyst"},'
                     '{"title": "Написать скрипт", "description": "Сохранить main.py", '
                     '"assignee_role": "developer"}]}',
                usage=Usage(300, 120))
        if "ПРОВЕРЯЕМАЯ ПОДЗАДАЧА" in joined:
            return CompletionResult(text='{"verdict":"ok","notes":"","issues":[]}',
                                    usage=Usage(150, 20))
        if "Сравни результаты" in system:
            return CompletionResult(
                text='{"conflicts":[{"description":"Сроки в отчётах расходятся",'
                     '"severity":"medium","labels":[],"auto_resolvable":true,'
                     '"resolution":"Берём более поздний срок"}]}',
                usage=Usage(120, 40))
        if "Составь краткую сводку" in system:
            return CompletionResult(
                text="ФАКТЫ:\nтребования собраны\nРАСХОЖДЕНИЯ:\nнет\nОТКРЫТЫЕ ВОПРОСЫ:\nнет",
                usage=Usage(120, 50))

        # Исполнитель: разработчик сначала пишет файл, аналитик один раз
        # отвечает неуверенно — это должно остановить прогон.
        wants_file = "Сохранить main.py" in joined
        if wants_file and tools and not self.calls.get("file"):
            self.calls["file"] = 1
            return CompletionResult(
                text="Сохраняю файл.",
                tool_calls=[ToolCall("c1", "write_file",
                                     {"path": "main.py", "content": "print('hello')\n"})],
                usage=Usage(250, 60))
        low = "Собрать требования" in joined and not self.calls.get("low")
        if low:
            self.calls["low"] = 1
        confidence = "0.3" if low else "0.9"
        return CompletionResult(
            text=f"Готово.\nCONFIDENCE: {confidence}\nRESULT:\nИтог работы по «{user[:60]}».",
            usage=Usage(400, 150))


def fake_build_provider(*_args, **_kwargs) -> LLMProvider:
    return FakeModel()


import core.orchestrator  # noqa: E402
import core.planner  # noqa: E402
import core.supervisor.supervisor  # noqa: E402
import ui.pages.agents_page  # noqa: E402
import ui.pages.keys_page  # noqa: E402

for module in (core.orchestrator, core.planner, core.supervisor.supervisor,
               ui.pages.agents_page, ui.pages.keys_page):
    module.build_provider = fake_build_provider

# ---------------------------------------------------------------------------
# Подмена модальных окон
# ---------------------------------------------------------------------------

FILLERS: dict[str, object] = {}
MESSAGES: list[str] = []


def _fake_exec(self) -> int:
    filler = FILLERS.pop(type(self).__name__, None)
    if filler is None:
        ERRORS.append(f"неожиданный диалог {type(self).__name__}")
        return QDialog.DialogCode.Rejected
    self.show()
    filler(self)
    self.layout().activate()
    self.grab().save(str(SHOTS / f"dialog_{type(self).__name__}.png"))
    self.hide()
    return QDialog.DialogCode.Accepted


QDialog.exec = _fake_exec
QMessageBox.warning = staticmethod(lambda _p, _t, text, *a, **k: MESSAGES.append(text))
QMessageBox.information = staticmethod(lambda _p, _t, text, *a, **k: MESSAGES.append(text))

import ui.widgets.common as common  # noqa: E402

_yes = lambda *_a, **_k: True  # noqa: E731
common.confirm = _yes
for name in ("workspaces_page", "keys_page", "agents_page", "task_page", "run_page"):
    setattr(sys.modules.get(f"ui.pages.{name}") or __import__(f"ui.pages.{name}",
            fromlist=["x"]), "confirm", _yes)


# ---------------------------------------------------------------------------
# Сценарий
# ---------------------------------------------------------------------------


def shot(widget, name: str) -> None:
    # processEvents() здесь нельзя: внутри корутины он повторно входит в луп
    # qasync и ломает чужие таски. Отрисовку дают паузы settle().
    widget.grab().save(str(SHOTS / f"{name}.png"))


async def settle(seconds: float = 0.2) -> None:
    await asyncio.sleep(seconds)


async def wait_for(predicate, timeout: float = 20.0) -> bool:
    loop = asyncio.get_event_loop()
    end = loop.time() + timeout
    while loop.time() < end:
        if predicate():
            return True
        await settle(0.05)
    return False


async def scenario(app: QApplication) -> None:
    from main import start_ui

    settings = AppSettings.load()
    db = Database()

    # Та же связка окон, что в приложении: вход → главное окно → выход → вход.
    windows = start_ui(db, settings)

    print("\n[1] Вход")
    login = windows["login"]
    login.resize(520, 640)
    await settle()
    shot(login, "01_signup")
    check("без профилей открыт экран регистрации", login.stack.currentIndex() == 1)

    login.su_username.setText("tester")
    login.su_password.setText("short")
    login.su_password2.setText("short")
    login._do_signup()
    check("короткий пароль отвергнут", "main" not in windows and login.su_error.isVisible())
    login.su_password.setText("password123")
    login.su_password2.setText("password123")
    login._do_signup()
    check("профиль создан", "main" in windows)

    print("\n[2] Главное окно")
    window = windows["main"]
    await settle(0.5)
    check("приложение не закрылось при переходе из окна входа",
          asyncio.get_event_loop().is_running() and window.isVisible())
    for i in range(window.stack.count()):
        window._select_page(i)
        await settle(0.05)
        shot(window, f"02_empty_{i:02d}")
    check("все страницы открываются без воркспейса", not ERRORS)

    print("\n[3] Воркспейс, ключ, агенты")
    window._select_page(0)

    def fill_ws(dlg):
        dlg.name.setText("Демо-проект")
        dlg.description.setPlainText("Проверка интерфейса")
    FILLERS["WorkspaceDialog"] = fill_ws
    window.page_workspaces._create()
    await settle()
    check("воркспейс создан и выбран", window.workspace_id is not None)
    shot(window, "03_workspaces")

    window._select_page(1)

    def fill_key(dlg):
        dlg.provider.setCurrentIndex(dlg.provider.findData("openai"))
        dlg.secret.setText("sk-test-123")
    FILLERS["KeyDialog"] = fill_key
    window.page_keys._create()
    await settle()
    keys = window.repos.keys.list()
    check("ключ сохранён", len(keys) == 1)
    for button in window.page_keys.findChildren(QPushButton):
        if button.text() == common.tr("common.test"):
            button.click()
    await settle(0.5)
    shot(window, "04_keys")
    check("проверка ключа закэшировала модели",
          window.repos.keys.get(keys[0].id).meta.get("models") == ["fake-mini", "fake-large"])

    window._select_page(2)
    for role, is_sup in (("analyst", False), ("developer", False), ("supervisor", True)):
        def fill_agent(dlg, role=role, is_sup=is_sup):
            idx = dlg.template.findData(role)
            if idx < 0:
                idx = 0
            dlg.template.setCurrentIndex(idx)
            dlg._load_models()
            dlg.model.setCurrentText("fake-mini")
            dlg.is_supervisor.setChecked(is_sup)
        FILLERS["AgentDialog"] = fill_agent
        window.page_agents._create()
        await settle(0.2)
    agents = window.repos.agents.list(window.workspace_id)
    check("три агента созданы", len(agents) == 3, ", ".join(a.name for a in agents))
    shot(window, "05_agents")

    print("\n[4] Задача")
    window._select_page(3)
    page = window.page_task
    page.title_edit.setText("Демо-задача")
    page.body_edit.setPlainText("Подготовить демо: требования и небольшой скрипт")
    page.token_limit.setText("100 000")
    page._autosplit()
    ok = await wait_for(lambda: page.btn_auto.isEnabled())
    subtasks = window.repos.tasks.subtasks(page.task.id)
    check("автоматическое разбиение", ok and len(subtasks) == 2,
          f"подзадач: {len(subtasks)}")
    check("исполнители назначены по ролям", all(s.agent_id for s in subtasks))

    def fill_sub(dlg):
        dlg.title.setText("Проверить итог")
        dlg.description.setPlainText("Свести результаты")
        dlg.assignee.setCurrentIndex(1)
    FILLERS["SubtaskDialog"] = fill_sub
    page._add_subtask()
    await settle()
    page._move(window.repos.tasks.subtasks(page.task.id)[-1].id, -1)
    await settle()
    shot(window, "06_task")
    check("подзадача добавлена вручную",
          len(window.repos.tasks.subtasks(page.task.id)) == 3)

    print("\n[5] Настройки воркспейса")
    window._select_page(9)
    sp = window.page_settings
    sp.hitl.setChecked(True)
    sp.hitl_threshold.setValue(0.5)
    idx = sp.sup_agent.findData(next(a.id for a in agents if a.is_supervisor))
    sp.sup_agent.setCurrentIndex(idx)
    await settle()
    ws = window.repos.workspaces.get(window.workspace_id)
    check("human-in-the-loop включён", ws.settings.get("human_in_the_loop") is True)
    supervisor_id = next(a.id for a in agents if a.is_supervisor)
    check("список агентов в настройках актуален", idx >= 0, f"индекс: {idx}")
    check("супервайзер выбран", ws.settings.get("supervisor_agent_id") == supervisor_id)
    shot(window, "07_settings")

    print("\n[6] Прогон")
    window.page_task._request_run()
    await settle()
    check("кнопка «Запустить» переводит на страницу выполнения",
          window.stack.currentWidget() is window.page_run)
    window.page_run.btn_start.click()
    run = window.page_run
    paused = await wait_for(lambda: run.approvals.isVisible(), 20)
    await settle(0.3)
    shot(window, "08_run_paused")
    confidences = [r.confidence for r in window.repos.reports.list_reports(window.workspace_id)]
    check("появилась панель решения", paused, f"уверенность в отчётах: {confidences}")

    window._select_page(6)
    await settle(1.3)
    shot(window, "09_dashboard_live")
    window._select_page(4)

    approve = DECISION_TITLES[Decision.APPROVE]
    for _ in range(10):
        buttons = [b for b in run.approvals.findChildren(QPushButton)
                   if b.text() == approve and b.isEnabled() and b.isVisible()]
        if not buttons:
            if not window.orchestrator.state.running:
                break
            await settle(0.2)
            continue
        buttons[0].click()
        await settle(0.3)
    finished = await wait_for(lambda: not window.orchestrator.state.running, 30)
    await settle(0.5)
    shot(window, "10_run_done")
    statuses = [s.status for s in window.repos.tasks.subtasks(page.task.id)]
    check("прогон завершён", finished, f"статусы: {statuses}")
    check("все подзадачи выполнены", all(s == "done" for s in statuses))
    check("разработчик записал файл инструментом write_file",
          (PATHS.workspace_dir(window.workspace_id) / "main.py").exists())
    check("кнопки вернулись в исходное состояние",
          run.btn_start.isEnabled() and not run.btn_stop.isEnabled())

    print("\n[7] Супервайзер, дашборд, бюджеты")
    window._select_page(5)
    for i in range(window.page_supervisor.tabs.count()):
        window.page_supervisor.tabs.setCurrentIndex(i)
        await settle(0.05)
        shot(window, f"11_supervisor_{i}")
    check("история решений не пуста",
          bool(window.repos.approvals.history(window.workspace_id)))

    window._select_page(6)
    await settle(1.2)
    dash = window.page_dashboard
    shot(window, "12_dashboard")
    check("график расходов получил точки", len(dash.cost_chart._points) >= 2,
          f"точек: {len(dash.cost_chart._points)}")
    check("распределение по агентам заполнено", len(dash.agent_chart._bars) >= 1)

    window._select_page(7)
    await settle()
    rows = [w for w in window.page_budget.findChildren(
        sys.modules["ui.pages.budget_page"].LimitRow)]
    check("бюджеты отображаются по уровням", len(rows) >= 3, f"строк: {len(rows)}")
    if rows:
        rows[0].tokens_edit.setText("5000")
        rows[0].tokens_edit.editingFinished.emit()
        await settle()
    shot(window, "13_budget")

    print("\n[8] Экспорт")
    window._select_page(8)
    await settle()
    ep = window.page_export
    auto_fmt = ep.format_box.currentData()
    check("формат определён автоматически", auto_fmt == "zip", f"формат: {auto_fmt}")
    shot(window, "14_export")
    for fmt in ("markdown", "docx", "pdf", "zip"):
        ep.format_box.setCurrentIndex(ep.format_box.findData(fmt))
        ep.opt_reports.setChecked(True)
        ep.opt_summaries.setChecked(True)
        ep.opt_decisions.setChecked(True)
        before = len(MESSAGES)
        ep._export()
        path = Path(ep.path_edit.text())
        check(f"экспорт {fmt}", path.exists() and path.stat().st_size > 0
              and len(MESSAGES) == before,
              MESSAGES[-1] if len(MESSAGES) > before else path.name)

    print("\n[9] Тема и язык")
    window._select_page(9)
    sp.theme_box.setCurrentIndex(1)
    await settle()
    for i in (6, 4, 9):
        window._select_page(i)
        await settle(0.1)
        shot(window, f"15_light_{i:02d}")
    sp.theme_box.setCurrentIndex(0)
    sp.lang_box.setCurrentIndex(sp.lang_box.findData("en"))
    await settle(0.5)
    rebuilt = windows["main"]
    nav = rebuilt.nav_group.button(0).text() if rebuilt is not window else ""
    check("смена языка пересобрала окно", rebuilt is not window and rebuilt.isVisible()
          and not shiboken6.isValid(window) and nav == "Workspaces",
          f"кнопка навигации: {nav!r}")
    check("после пересборки открыта та же страница",
          rebuilt.stack.currentWidget() is rebuilt.page_settings)
    shot(rebuilt, "16_main_en")

    rebuilt._logout()
    await settle(0.5)
    login2 = windows["login"]
    check("после выхода снова открыто окно входа",
          login2 is not login and login2.isVisible()
          and login2.stack.currentIndex() == 0)
    shot(login2, "17_login_en")
    login2.password.setText("password123")
    login2._do_signin()
    await settle(0.5)
    check("повторный вход по паролю",
          windows["main"] is not rebuilt and windows["main"].isVisible())
    shot(windows["main"], "18_main_after_login")
    set_language("ru")


def main() -> int:
    settings = AppSettings.load()
    set_language(settings.language)
    PATHS.ensure()
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet(settings.theme))
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    with loop:
        try:
            loop.run_until_complete(asyncio.wait_for(scenario(app), 120))
        except Exception:  # noqa: BLE001
            ERRORS.append(traceback.format_exc())

    print(f"\nСкриншоты: {SHOTS}")
    if ERRORS:
        print(f"\nОШИБКИ ({len(ERRORS)}):")
        for text in dict.fromkeys(ERRORS):
            print("-" * 66)
            print(text.rstrip())
    print("\n" + "=" * 66)
    total = len(_passed) + len(_failed)
    if _failed or ERRORS:
        print(f"ПРОВАЛЕНО: {len(_failed)} из {total}, ошибок в слотах: {len(ERRORS)}")
        for name in _failed:
            print(f"  - {name}")
        return 1
    print(f"ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ: {total} из {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
````


## Сборка и запуск

### `requirements.txt`

*25 строк*

````text
# ============================================================================
#  AI Orchestrator — зависимости
#  Установка:  pip install -r requirements.txt
# ============================================================================

# --- ОБЯЗАТЕЛЬНЫЕ: без них приложение не запустится ------------------------
PySide6>=6.6,<7          # десктопный интерфейс (Qt)
qasync>=0.27             # общий цикл событий Qt + asyncio
httpx>=0.27              # асинхронные запросы к провайдерам моделей
cryptography>=42.0       # Argon2id + AES-256-GCM для шифрования API-ключей

# --- РЕКОМЕНДУЕМЫЕ: без них теряются отдельные функции ---------------------
ddgs>=9.0                # веб-поиск без API-ключа (инструмент web_search)
trafilatura>=1.12        # извлечение текста страниц (инструмент fetch_url)
beautifulsoup4>=4.12     # запасной парсер HTML, если trafilatura не справилась
keyring>=25.0            # опция «запомнить пароль в хранилище ОС»

# --- ЭКСПОРТ: нужны только для соответствующих форматов --------------------
python-docx>=1.1         # экспорт в DOCX
reportlab>=4.2           # экспорт в PDF
# Markdown и ZIP работают без дополнительных пакетов.

# --- ЗАПАСНОЙ ВАРИАНТ -----------------------------------------------------
# Если установлена cryptography старее 42.0, раскомментируйте строку ниже:
# argon2-cffi>=23.1
````

### `run.sh`

*30 строк*

````bash
#!/usr/bin/env bash
# Запуск AI Orchestrator на Linux и macOS.
# При первом запуске создаёт виртуальное окружение и ставит зависимости.
set -euo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"

if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "Не найден интерпретатор Python. Установите Python 3.11 или новее." >&2
    exit 1
fi

VERSION=$("$PYTHON" -c 'import sys; print("%d.%d" % sys.version_info[:2])')
REQUIRED=$("$PYTHON" -c 'import sys; print(1 if sys.version_info >= (3, 11) else 0)')
if [ "$REQUIRED" != "1" ]; then
    echo "Нужен Python 3.11 или новее, найден $VERSION." >&2
    echo "Укажите другой интерпретатор: PYTHON=python3.12 ./run.sh" >&2
    exit 1
fi

if [ ! -d ".venv" ]; then
    echo "Создаю виртуальное окружение (.venv)…"
    "$PYTHON" -m venv .venv
    ./.venv/bin/python -m pip install --upgrade pip --quiet
    echo "Устанавливаю зависимости, это займёт пару минут…"
    ./.venv/bin/pip install -r requirements.txt
fi

exec ./.venv/bin/python main.py "$@"
````

### `run.bat`

*59 строк*

````batch
@echo off
REM ===========================================================
REM  AI Orchestrator - launcher for Windows
REM  Creates a virtual environment on first run, then starts.
REM  Messages are in Latin script on purpose: the Windows
REM  console uses a legacy code page and would garble UTF-8.
REM ===========================================================
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo  ERROR: Python not found.
    echo  Install Python 3.11+ from https://www.python.org/downloads/
    echo  and tick "Add Python to PATH" during setup.
    echo.
    pause
    exit /b 1
)

python -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"
if errorlevel 1 (
    echo.
    echo  ERROR: Python 3.11 or newer is required.
    python --version
    echo.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo.
    echo  Creating virtual environment (.venv)...
    python -m venv .venv
    if errorlevel 1 (
        echo  ERROR: failed to create the virtual environment.
        pause
        exit /b 1
    )
    ".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
    echo  Installing dependencies, this takes a few minutes...
    ".venv\Scripts\pip.exe" install -r requirements.txt
    if errorlevel 1 (
        echo  ERROR: failed to install dependencies.
        pause
        exit /b 1
    )
    echo  Done.
    echo.
)

".venv\Scripts\python.exe" main.py %*
if errorlevel 1 (
    echo.
    echo  The application exited with an error.
    echo  See the log: %%APPDATA%%\ai-orchestrator\logs\app.log
    pause
)
````

### `.gitignore`

*10 строк*

````text
__pycache__/
*.py[cod]
.venv/
venv/
*.db
*.db-wal
*.db-shm
logs/
exports/
.DS_Store
````



---

# Что осталось сделать

## Сделано при первом запуске интерфейса

Интерфейс впервые запущен и пройден сценарием 	ests/ui_smoke.py. Найдено
и исправлено:

- **Дашборд не обновлялся в реальном времени.** Обработчик шины ссылался на
  несуществующий EventType.TOOL_CALL и падал на каждом событии. Шина
  глотала исключение, так что снаружи ничего не было видно.
- **Файловые инструменты не доходили до агентов.** Шаблоны ролей и
  	ools_enabled в настройках по умолчанию используют групповое имя
  iles, а в реестре есть только 
ead_file, write_file и list_dir
  (так же web_search без etch_url). Группы теперь разворачивает
  expand_tool_names в core/tools/base.py, в том числе для уже
  сохранённых агентов и воркспейсов.
- **Диалог агента.** При смене шаблона имя не менялось (все агенты
  становились «Аналитиками»), а промпт, поправленный руками, затирался.
  Теперь меняется только то, что было подставлено автоматически.
- **Настройки воркспейса** не перечитывали список агентов, поэтому выбор
  супервайзера был пустым, если агентов создали после открытия страницы.
- **Смена языка** теперь пересобирает главное окно сразу, на той же странице.
  Во время прогона — после выхода и повторного входа, чтобы не прерывать
  агентов. Связка окон вынесена в main.start_ui.
- **Время** везде показывалось в UTC. Хранится по-прежнему UTC, а для показа
  есть storage.db.local_time.
- **Оформление.** Правило QWidget { background } давало тёмные подложки под
  каждой надписью в карточках. Стрелки у выпадающих списков и счётчиков
  пропадали, а трюк с треугольником из рамок Qt не рисует: теперь это PNG,
  которые рисуются при старте в cache/theme (вариант @2x для HiDPI;
  плагина SVG в сборке PySide6 может не быть). Неактивная основная кнопка
  выглядела активной. Кнопки ▲▼ были обрезаны. Бейджи статуса растягивались.
  Имена в ленте были не видны в светлой теме. Предупреждение на экране
  регистрации обрезалось, потому что QStackedWidget не передаёт
  height-for-width: вместо него PageSwitcher.
- **Мелочи.** Константа WD_STYLE_TYPE.PARAGRAPH вместо числа в экспорте
  DOCX. Подписи столбцов обрезаются по пикселям. Расход проверок
  супервайзера подписан отдельно от агента-супервайзера. Важность и тип
  инцидентов переведены на русский.

Графики на QPainter (charts.py) работали с первого раза.
## Функциональные доработки

**Фильтр графиков по прогонам.** Дашборд показывает всю историю воркспейса
без разделения по запускам. В `usage_log` нет идентификатора прогона —
его нужно добавить и прокинуть через `BudgetRepo.log_call`.

**Слот параллельности при паузе.** Пока система ждёт решения человека,
занятый агент удерживает свой слот: другие подзадачи волны продолжают
работать, но новая на его место не встанет. Лечится освобождением семафора
на время ожидания в `ApprovalGate.ask`.

**Суммаризация длинной истории агента.** Сейчас история обрезается по
лимиту сообщений. Для длинных задач нужна сворачивающая суммаризация при
приближении к контекстному окну модели.

**Стриминг ответов в интерфейс.** Провайдеры умеют `stream()`, но
`AgentRunner` использует только `complete()`. Для активного агента поток
токенов в ленту сделал бы ожидание менее глухим.

**Шаблоны воркспейсов.** Готовые наборы «аналитик + разработчик +
тестировщик» с настроенными промптами, чтобы не собирать команду заново
под каждый проект.

**Повторный запуск подзадач.** Сейчас перезапуск прогона берёт все
незавершённые подзадачи. Нужна возможность перезапустить одну конкретную.

## Технический долг

**Таблица цен устаревает.** `providers/pricing.json` заполнен вручную
и требует сверки с прайс-листами. Стоит добавить дату последнего обновления
и предупреждение в интерфейсе, если она старше нескольких месяцев.

**Нет автотестов интерфейса.** `tests/smoke.py` покрывает только ядро.
Для виджетов имело бы смысл добавить `pytest-qt`.

**`TokenBudget` в `core/agents/runner.py`** остался как совместимая обёртка
после появления `BudgetGuard`. Используется только в тестах — можно убрать,
когда в нём отпадёт нужда.

**Обработка ошибок провайдеров** сводится к тексту исключения. Полезно
различать исчерпание квоты, неверный ключ и временную недоступность:
на первое стоит останавливать агента, на третье — повторять с задержкой.

**Ретраи при сетевых сбоях** не реализованы вовсе. Одна оборвавшаяся
HTTP-сессия роняет подзадачу.

## Известные ограничения по замыслу

Это не баги, а осознанные решения — менять их стоит только вместе с
пониманием последствий:

- Пароль профиля невосстановим: механизма «забыли пароль» нет, иначе
  шифрование ключей теряло бы смысл.
- Режим `subprocess` в песочнице ограничивает ресурсы и окружение, но не
  изолирует файловую систему. Для строгой изоляции нужен Docker.
- Супервайзер — самая дорогая часть системы по токенам: на тестовом прогоне
  из трёх подзадач он израсходовал около двух третей бюджета. Это следствие
  того, что он читает каждый отчёт.
