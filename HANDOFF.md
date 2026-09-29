# Agent Forge - передача проекта

Единый файл для продолжения работы над проектом: цель, принятые решения,
полный код всех файлов, команды запуска и список незакрытых задач.

**Версия:** 1.1.1 · **Python:** 3.11+ · **Интерфейс:** PySide6 6.11, Qt Quick
**Состояние:** все девять этапов MVP реализованы. Версия 1.1: новый интерфейс
на Qt Quick, стриминг рассуждений агентов, исправления ядра по итогам ревью.
Ядро покрыто смоук-тестами (37 проверок) и регрессионными pytest-тестами,
интерфейс - туром по всем экранам с живым прогоном фейковых агентов
(`tests/ui_tour.py`). Проверено на Windows 11. Прежнее имя проекта -
AI Orchestrator.

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
   Единственный канал обмена - анонимная сводка супервайзера, которая
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

**Интерфейс: мост Python и QML**

- `ui/app.py`
- `ui/bridge/core.py`
- `ui/bridge/listmodel.py`
- `ui/bridge/i18n_bridge.py`
- `ui/bridge/backend.py`
- `ui/bridge/pages.py`
- `ui/bridge/c_workspaces.py`
- `ui/bridge/c_keys.py`
- `ui/bridge/c_agents.py`
- `ui/bridge/c_task.py`
- `ui/bridge/c_run.py`
- `ui/bridge/c_supervisor.py`
- `ui/bridge/c_dashboard.py`
- `ui/bridge/c_budget.py`
- `ui/bridge/c_export.py`
- `ui/bridge/c_prefs.py`
- `app/i18n_ui.py`

**Интерфейс: QML**

- `ui/qml/Main.qml`
- `ui/qml/Login.qml`
- `ui/qml/Shell.qml`
- `ui/qml/pages/Workspaces.qml`
- `ui/qml/pages/Keys.qml`
- `ui/qml/pages/Agents.qml`
- `ui/qml/pages/Task.qml`
- `ui/qml/pages/Run.qml`
- `ui/qml/pages/Supervisor.qml`
- `ui/qml/pages/Dashboard.qml`
- `ui/qml/pages/Budget.qml`
- `ui/qml/pages/Export.qml`
- `ui/qml/pages/Settings.qml`

**Интерфейс: дизайн-система Ao**

- `ui/qml/Ao/qmldir`
- `ui/qml/Ao/Theme.qml`
- `ui/qml/Ao/Icons.qml`
- `ui/qml/Ao/AText.qml`
- `ui/qml/Ao/Icon.qml`
- `ui/qml/Ao/Button.qml`
- `ui/qml/Ao/IconButton.qml`
- `ui/qml/Ao/Card.qml`
- `ui/qml/Ao/Page.qml`
- `ui/qml/Ao/PageHeader.qml`
- `ui/qml/Ao/SectionTitle.qml`
- `ui/qml/Ao/Field.qml`
- `ui/qml/Ao/TextBox.qml`
- `ui/qml/Ao/Select.qml`
- `ui/qml/Ao/Toggle.qml`
- `ui/qml/Ao/Chip.qml`
- `ui/qml/Ao/Segmented.qml`
- `ui/qml/Ao/RangeSlider.qml`
- `ui/qml/Ao/Badge.qml`
- `ui/qml/Ao/StatusDot.qml`
- `ui/qml/Ao/Spinner.qml`
- `ui/qml/Ao/Skeleton.qml`
- `ui/qml/Ao/Tip.qml`
- `ui/qml/Ao/ScrollBar.qml`
- `ui/qml/Ao/EmptyState.qml`
- `ui/qml/Ao/Sheet.qml`
- `ui/qml/Ao/Confirm.qml`
- `ui/qml/Ao/Toasts.qml`
- `ui/qml/Ao/ProgressRing.qml`
- `ui/qml/Ao/SegmentBar.qml`
- `ui/qml/Ao/LineChart.qml`
- `ui/qml/Ao/BarList.qml`
- `ui/qml/Ao/Ticker.qml`
- `ui/qml/Ao/Aurora.qml`
- `ui/qml/Ao/OrbitLogo.qml`

**Служебное и тесты**

- `utils/asyncutils.py`
- `utils/logging_setup.py`
- `tests/conftest.py`
- `tests/fakes.py`
- `tests/smoke.py`
- `tests/test_core_fixes.py`
- `tests/test_audit_fixes.py`
- `tests/test_models.py`
- `tests/qml_controls_check.py`
- `tests/test_ui.py`
- `tests/ui_tour.py`
- `pytest.ini`

**Сборка и запуск**

- `requirements.txt`
- `requirements-dev.txt`
- `run.sh`
- `run.bat`
- `.gitignore`

Файлы `__init__.py` содержат только строку документации и здесь не приводятся:

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
- `ui\bridge\__init__.py`
- `utils\__init__.py`

---


## Принятые решения

Эти развилки были согласованы до написания кода. Менять их можно, но каждая
тянет за собой остальное.

### Стек и платформа

**GUI - PySide6 + Qt Quick (QML).** Нативное окно на Windows, macOS и Linux
без веб-прослойки и без Node.js. Интерфейс в `ui/qml`, дизайн-система в модуле
`Ao` (тема, иконки Lucide, компоненты). Данные отдаёт мост `ui/bridge`:
`Backend` и по контроллеру на экран. Штатная интеграция с asyncio через
`qasync`, упаковка через PyInstaller. Лицензия LGPL допускает закрытую
дистрибуцию при динамической линковке.

**Два правила моста, нарушение которых ломает интерфейс молча.** Сигнал
`changed = Signal()` объявляется в каждом конечном классе моста: PySide6
связывает `notify` свойства только с сигналом того же класса, иначе биндинги
QML перестают обновляться. Роль модели списка не может называться `model`:
в делегате она перекрывает сам объект `model`. Оба правила проверяются
тестами (`tests/test_ui.py`, `DictListModel`).

**Параллелизм - один asyncio-луп.** Qt и asyncio объединены `qasync`, агенты
живут в нём как обычные таски. Пятнадцать агентов не превращаются в
пятнадцать потоков. Блокирующие операции (SQLite, библиотека поиска) уходят
в `asyncio.to_thread`, исполнение кода - в отдельный процесс или контейнер.

**Графики - средствами Qt Quick** (Canvas, Shapes), без QtCharts: ноль
дополнительных зависимостей, цвета из темы, анимации отрисовки.

### Безопасность

**Шифрование ключей.** `Argon2id(пароль профиля, соль)` даёт 32-байтовый
мастер-ключ, который живёт только в оперативной памяти. API-ключи шифруются
`AES-256-GCM`. База остаётся обычным SQLite, но секреты в ней нечитаемы.
Смена пароля перешифровывает все ключи. Пароль профиля и мастер-пароль -
одно и то же: одно поле при входе, и восстановления нет.

**Песочница - интерфейс с двумя реализациями.** `DockerSandbox`
(`--network none`, `--read-only`, лимиты памяти, CPU и PID, `--cap-drop ALL`)
используется, если Docker доступен. Иначе `SubprocessSandbox`: одноразовый
каталог, своя группа процессов, `RLIMIT_CPU/AS/FSIZE/NPROC`, вычищенное
окружение без ключей хоста, сеть отрезана. Второй режим - барьер по
умолчанию, а не полная изоляция, и приложение говорит об этом прямо
в настройках.

**Права на файлы.** Агент работает в каталоге своего воркспейса.
Дополнительные каталоги добавляет пользователь вручную. Проверка пути
централизована в `ToolContext.resolve` и отсекает `../`, абсолютные пути
и симлинки наружу.

### Логика работы

**Цикл агента - ReAct.** Модель думает, вызывает инструменты, получает
результат, продолжает. Остановка по одному из условий: выдан блок `RESULT:`,
кончились разрешённые шаги, исчерпан лимит токенов, пользователь нажал
«Стоп». Из ответа разбираются блок `RESULT:` и строка `CONFIDENCE: 0..1`.

**Лимит токенов на задачу** задаёт пользователь; пустое поле означает
отсутствие лимита.

**Супервайзер** работает либо на одном из подключённых API-ключей, либо на
локальной модели через Ollama (по умолчанию Qwen) - второй вариант
бесплатен и работает офлайн. Он может вернуть работу на доработку до
`max_rework_rounds` раз. Сводку для команды пересказывает своими словами,
имена агентов вычищаются пост-обработкой, а не только просьбой в промпте.

**Нечитаемый ответ супервайзера** трактуется как «нужна доработка», а не
«принято»: молча пропустить непроверенный отчёт хуже, чем перепроверить.
Если супервайзер недоступен или упёрся в лимит, результат считается
непроверенным и не уходит в зависимые подзадачи без решения человека.

**Решение человека важнее настройки.** `max_rework_rounds` ограничивает
автоматические доработки супервайзера. Когда доработку назначает человек,
выдаётся дополнительный круг сверх лимита - до трёх таких кругов, иначе
цикл «вернул - переделал - вернул» не заканчивался бы.

**Бюджеты проверяются до вызова модели**, а не после: узнавать о превышении
постфактум бессмысленно, деньги уже потрачены. Через бюджет проходят и
проверки супервайзера, и планирование. При включённом human-in-the-loop
исчерпанный лимит не обрывает работу, а превращается в вопрос «поднять на
50%?», общий для всех агентов, упёршихся в этот уровень. Расход берётся из журнала
`usage_log`, а не из накопительных счётчиков, поэтому перезапуск приложения
не обнуляет израсходованный бюджет.

**Стоимость считается на клиенте** по таблице `providers/pricing.json`
(USD за миллион токенов, поиск по точному совпадению и по префиксу):
провайдеры почти никогда не возвращают цену, только токены. Для локальных
моделей стоимость равна нулю.

### Интерфейс

**Панель решений, а не модальное окно.** Вопросов human-in-the-loop может
быть несколько одновременно, если параллельно работают разные агенты.
Модалка заслоняла бы прогресс и ленту - ровно то, по чему принимается
решение.

**Локализация RU/EN** переключается на лету без пересборки окна: QML
читает словарь строк как свойство моста. Строки версии 1.1 лежат в
`app/i18n_ui.py`, тест проверяет, что каждый ключ из QML есть в обоих языках.

**Анимации с выключателем.** Все длительности идут через `Theme.dur()`, а
уровень «полные / сдержанные / выключены» задаётся в настройках.

---


## Установка и запуск

### Быстрый способ

Windows - двойной щелчок по `run.bat`. Linux и macOS:

````bash
./run.sh
````

Скрипт проверит версию Python, создаст виртуальное окружение, поставит
зависимости и запустит приложение. Первый запуск - 2-5 минут.

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
провайдерами. Ожидаемый результат - `ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ: 37 из 37`.
Работают во временном каталоге, профиль пользователя не трогают.

### Проверка интерфейса

````bash
python -m pytest                  # всё, включая тур по интерфейсу
python tests/ui_tour.py shots     # тур со скриншотами всех экранов
````

Тур создаёт профиль, два воркспейса, агентов, задачу с зависимостями,
проходит все десять экранов и запускает прогон фейковыми агентами со
стримингом, отвечая на вопрос human-in-the-loop. Провал - любое
предупреждение QML или незавершённая подзадача.

Правило для тех, кто будет дописывать сценарий: весь тур идёт внутри одного
`loop.run_until_complete(...)`. Если прерывать цикл между шагами, Qt
продолжает обрабатывать события (например, при снимке окна), и корутины
агентов просыпаются вне цикла с «no running event loop».

### Пересборка этого документа

Документ собирается скриптом из реальных файлов, поэтому не может разойтись
с кодом. После изменений выполните:

````bash
python make_handoff.py
````

### Каталог данных

| ОС | Путь |
|---|---|
| Windows | `%APPDATA%\agent-forge` |
| macOS | `~/Library/Application Support/agent-forge` |
| Linux | `~/.local/share/agent-forge` |

Переопределяется переменной окружения `AGENTFORGE_HOME` - этим пользуются тесты.
Внутри: `app.db`, `logs/`, `workspaces/`, `exports/`, `settings.json`.

### Сборка в исполняемый файл

````bash
pip install pyinstaller
pyinstaller --name AgentForge --windowed --onedir main.py \
  --add-data "storage/schema.sql:storage" \
  --add-data "providers/pricing.json:providers" \
  --add-data "ui/qml:ui/qml" \
  --add-data "ui/assets:ui/assets"
````

На Windows разделитель в `--add-data` - точка с запятой. Вариант `--onedir`
стартует заметно быстрее `--onefile`.

---


## Архитектура

### Слои

````
UI (Qt Quick) ↔ ui/bridge  →  Repos (единственная точка доступа к БД)  →  SQLite
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

Ядро ничего не знает о Qt: оно публикует события в `EventBus`, а контроллеры
моста на них подписываются и обновляют модели для QML. Всё работает в одном
лупе. Фрагменты стриминга (`AGENT_DELTA`) копятся и сбрасываются в интерфейс
таймером раз в 60 мс, дашборд перерисовывается не чаще раза в секунду.

### Схема базы

14 таблиц, заведены сразу под все этапы, чтобы миграции не ломали уже
созданные профили:

`users`, `workspaces`, `api_keys` (секреты зашифрованы), `agents`, `tasks`,
`subtasks`, `messages` (приватная история агента), `reports`, `summaries`,
`incidents`, `approvals` (точки human-in-the-loop), `budgets`, `usage_log`.

**Изоляция агентов держится на выборке.** История каждого агента лежит
в `messages` и всегда выбирается с фильтром по `agent_id`. Кросс-агентных
выборок в коде нет - это инвариант, который нельзя нарушать при доработках.

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
5. При включённом human-in-the-loop срабатывают триггеры паузы: конфликт
   или непринятый результат, непроверенный результат, самооценка агента ниже
   порога, исчерпанный бюджет, завершение волны подзадач. На время вопроса
   слот параллельности отдаётся другим подзадачам.
6. `BudgetGuard.ensure_allowed` проверяется перед каждым обращением к модели,
   включая проверки супервайзера.

---


---

# Полный код


## Точка входа и конфигурация

### `main.py`

*85 строк*

````python
"""Точка входа Agent Forge.

Запуск::

    python main.py

Цикл событий Qt и asyncio объединяются через qasync - это даёт один общий
луп, в котором живут и интерфейс, и параллельно работающие агенты.
"""

from __future__ import annotations

import asyncio
import logging
import os
import sys
from pathlib import Path

# Чтобы приложение запускалось из любого каталога.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from app.config import APP_NAME, PATHS, AppSettings  # noqa: E402
from app.i18n import set_language  # noqa: E402

# Шрифты и геометрия Qt Quick лучше выглядят без принудительного округления
# масштаба на дисплеях 125-175 %.
os.environ.setdefault("QT_ENABLE_HIGHDPI_SCALING", "1")
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


def main() -> int:
    _check_dependencies()

    import qasync
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QApplication

    from storage.db import Database
    from ui.app import UiApp

    setup_logging()
    PATHS.ensure()
    log.info("Старт %s, каталог данных: %s", APP_NAME, PATHS.home)

    settings = AppSettings.load()
    set_language(settings.language)

    # QApplication, а не QGuiApplication: системные диалоги выбора файлов
    # и папок (экспорт, разрешённые каталоги) живут в QtWidgets.
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setOrganizationName("AgentForge")

    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)

    ui = UiApp(settings, Database())

    with loop:
        code = loop.run_forever() or 0
        ui.dispose()
    return code


if __name__ == "__main__":
    sys.exit(main())
````

### `app/config.py`

*139 строк*

````python
"""Глобальная конфигурация приложения: пути, константы, настройки по умолчанию.

Все пользовательские данные хранятся ЛОКАЛЬНО в домашнем каталоге пользователя.
Каталог можно переопределить переменной окружения ``AGENTFORGE_HOME``
(старое имя ``AIORC_HOME`` тоже понимается).
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

APP_NAME = "Agent Forge"
APP_SLUG = "agent-forge"
#: каталог данных до переименования проекта (AI Orchestrator → Agent Forge)
LEGACY_SLUG = "ai-orchestrator"
APP_VERSION = "1.1.1"          # 1.1.1: исправления после полного прохода по коду
SCHEMA_VERSION = 2             # версия схемы SQLite (для миграций)


def _default_home() -> Path:
    """Возвращает корневой каталог данных приложения для текущей ОС."""
    env = os.environ.get("AGENTFORGE_HOME") or os.environ.get("AIORC_HOME")
    if env:
        return Path(env).expanduser()
    if sys.platform == "win32":
        base = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        base = Path.home() / "Library" / "Application Support"
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
    # Профили, созданные до переименования, продолжают работать: если нового
    # каталога ещё нет, а старый есть, используем старый.
    legacy = base / LEGACY_SLUG
    if not (base / APP_SLUG).exists() and legacy.exists():
        return legacy
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
    #: насколько активны анимации интерфейса: "full" | "reduced" | "off"
    motion: str = "full"
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
            except Exception:  # noqa: BLE001 - повреждённый конфиг не должен ронять старт
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
    "hitl_confidence_threshold": 0.5,   # ниже этой самооценки агента - спросить человека
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
    "max_parallel_agents": 6,           # сколько агентов работают одновременно
    "tools_enabled": ["web_search", "files", "code_exec"],
    "extra_allowed_paths": [],          # доп. каталоги для файлового инструмента
    "sandbox_backend": "auto",          # "auto" | "subprocess" | "docker"
    "sandbox_timeout_sec": 30,
    "sandbox_memory_mb": 512,
    "search_backend": "duckduckgo",     # "duckduckgo" | "tavily" | "brave"
    "search_api_key": "",               # ключ Tavily/Brave, хранится зашифрованным
    "fetch_pages": True,                # скачивать и парсить страницы из выдачи
}
````

### `app/i18n.py`

*558 строк*

````python
"""Локализация интерфейса (RU/EN) с переключателем в настройках.

Использование::

    from app.i18n import tr
    label.setText(tr("login.title"))

Строки хранятся плоскими словарями «ключ -> перевод». Отсутствующий ключ
возвращается как есть - это заметно в UI и помогает не потерять переводы.
"""

from __future__ import annotations

from typing import Callable

_LISTENERS: list[Callable[[], None]] = []
_CURRENT = "ru"

RU: dict[str, str] = {
    # --- общее ---
    "app.title": "Agent Forge - оркестрация ИИ-агентов",
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
    "login.no_profiles": "Профилей пока нет - создайте первый",
    "login.bad_credentials": "Неверное имя профиля или пароль",
    "login.password_mismatch": "Пароли не совпадают",
    "login.password_short": "Пароль должен быть не короче 8 символов",
    "login.user_exists": "Профиль с таким именем уже существует",
    "login.warning": (
        "Пароль профиля используется как мастер-ключ для шифрования API-ключей. "
        "Восстановить его невозможно - при утере ключи придётся добавить заново."
    ),
    # --- бюджеты (этап 9) ---
    "nav.budget": "Бюджеты",
    "bud.title": "Бюджеты и лимиты",
    "bud.subtitle": "Лимит можно поставить на проект, задачу и каждого агента. Пустое поле - без ограничения",
    "bud.spent": "израсходовано: {tokens} токенов · ${cost}",
    "bud.token_limit": "Лимит токенов",
    "bud.cost_limit": "Лимит стоимости, $",
    "bud.alert_at": "Алерт при",
    "bud.no_limit": "без лимита",
    "bud.used_pct": "Выбрано {pct}% бюджета",
    "bud.exceeded": "Лимит исчерпан - новые вызовы модели заблокированы",
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
    "dash.no_feed": "Отчётов пока нет - запустите агентов на вкладке «Выполнение».",
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
    "sup.no_incidents": "Инцидентов нет - супервайзер не нашёл проблем.",
    "sup.resolve": "Закрыть инцидент",
    "sup.resolution": "Решение",
    "sup.delivered": "получателей: {n}",
    "sup.by_timer": "по таймеру",
    "sup.by_event": "по событию",
    "sup.by_hand": "вручную",
    "sup.by_final": "итоговая",
    "sup.model_api": "Супервайзер: {name} - {model}",
    "sup.model_local": "Супервайзер: локальная модель {model} ({url})",
    "sup.not_configured": "Супервайзер не настроен. Выберите его на вкладке «Настройки».",
    "sup.nothing_to_summarize": "Пока нечего обобщать - нет готовых результатов.",
    # --- навигация ---
    "nav.workspaces": "Воркспейсы",
    "nav.keys": "API-ключи",
    "nav.agents": "Агенты",
    "nav.task": "Задача",
    "nav.dashboard": "Дашборд",
    "nav.settings": "Настройки",
    "nav.logout": "Выйти",
    # --- воркспейсы ---
    "ws.title": "Воркспейсы",
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
    "task.placeholder": "Опишите, что нужно сделать. Чем подробнее - тем точнее разбиение на подзадачи.",
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
    "settings.hitl_threshold_hint": "Если исполнитель оценил свою уверенность ниже этого значения, система остановится и спросит вас. 0 - не спрашивать никогда.",
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
    "settings.restart_note": "Язык переключается сразу. Во время прогона - после выхода и повторного входа.",
    "settings.lang_after_run": "Идёт прогон - язык сменится после выхода и повторного входа, чтобы не прерывать агентов.",
    "settings.budget": "Бюджеты и лимиты",
}

EN: dict[str, str] = {
    "app.title": "Agent Forge - multi-agent orchestration",
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
    "login.no_profiles": "No profiles yet - create the first one",
    "login.bad_credentials": "Wrong profile name or password",
    "login.password_mismatch": "Passwords do not match",
    "login.password_short": "Password must be at least 8 characters",
    "login.user_exists": "A profile with this name already exists",
    "login.warning": (
        "The profile password is also the master key that encrypts your API keys. "
        "It cannot be recovered - if lost, keys must be re-entered."
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
    "bud.exceeded": "Limit reached - further model calls are blocked",
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
    "dash.no_feed": "No reports yet - start the agents on the Run tab.",
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
    "sup.no_incidents": "No incidents - the supervisor found no problems.",
    "sup.resolve": "Close incident",
    "sup.resolution": "Resolution",
    "sup.delivered": "recipients: {n}",
    "sup.by_timer": "on timer",
    "sup.by_event": "on event",
    "sup.by_hand": "manual",
    "sup.by_final": "final",
    "sup.model_api": "Supervisor: {name} - {model}",
    "sup.model_local": "Supervisor: local model {model} ({url})",
    "sup.not_configured": "Supervisor is not configured. Pick one on the Settings tab.",
    "sup.nothing_to_summarize": "Nothing to summarize yet - no finished results.",
    "nav.workspaces": "Workspaces",
    "nav.keys": "API keys",
    "nav.agents": "Agents",
    "nav.task": "Task",
    "nav.dashboard": "Dashboard",
    "nav.settings": "Settings",
    "nav.logout": "Log out",
    "ws.title": "Workspaces",
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
    "settings.hitl_threshold_hint": "If an agent rates its own confidence below this, the system stops and asks you. 0 - never ask.",
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
    "settings.lang_after_run": "A run is in progress - the language will change after you log out and back in, so agents are not interrupted.",
    "settings.budget": "Budgets and limits",
}

# Строки нового интерфейса лежат в отдельном модуле и вливаются сюда.
from app.i18n_ui import EN_UI, RU_UI  # noqa: E402

RU.update(RU_UI)
EN.update(EN_UI)

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


def catalog_for(code: str) -> dict[str, str]:
    """Словарь строк языка (для моста QML)."""
    return _CATALOG.get(code, RU)


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
-- Схема локальной БД Agent Forge (SQLite).
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

*134 строк*

````python
"""Подключение к локальной SQLite-БД и применение схемы.

Соединение одно на процесс (``check_same_thread=False``), запись защищена
мьютексом - этого достаточно, потому что вся работа с БД идёт из одного
asyncio-лупа, а фоновые потоки обращаются к ней редко.
"""

from __future__ import annotations

import sqlite3
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

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
            if current < 2:
                # Версия 2: сохранённые промпты агентов приводятся к тому же
                # набору символов, что и шаблоны ролей.
                long_dash, mid_dash = chr(0x2014), chr(0x2013)
                self.conn.execute(
                    "UPDATE agents SET system_prompt = REPLACE(REPLACE(REPLACE("
                    "system_prompt, ?, ' - '), ?, '-'), ?, '-') "
                    "WHERE instr(system_prompt, ?) > 0 OR instr(system_prompt, ?) > 0",
                    (f" {long_dash} ", long_dash, mid_dash, long_dash, mid_dash),
                )
            if current != SCHEMA_VERSION:
                self.conn.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            self.conn.commit()

    # -- базовые операции ----------------------------------------------------
    @contextmanager
    def transaction(self) -> Iterator[sqlite3.Connection]:
        """Несколько изменений одним коммитом: либо применяются все, либо ни одно.

        Внутри блока писать нужно через возвращённое соединение, а не через
        ``execute``: тот коммитит каждую команду по отдельности.
        """
        with self._lock:
            try:
                self.conn.execute("BEGIN")
                yield self.conn
                self.conn.commit()
            except BaseException:
                self.conn.rollback()
                raise

    def execute(self, sql: str, params: Sequence[Any] = ()) -> sqlite3.Cursor:
        with self._lock:
            try:
                cur = self.conn.execute(sql, params)
                self.conn.commit()
            except BaseException:
                # Упавшая команда оставляет открытой неявную транзакцию, и
                # следующий ``transaction()`` споткнулся бы на её ``BEGIN``.
                self.conn.rollback()
                raise
            return cur

    def executemany(self, sql: str, seq: Iterable[Sequence[Any]]) -> None:
        with self._lock:
            try:
                self.conn.executemany(sql, seq)
                self.conn.commit()
            except BaseException:
                self.conn.rollback()
                raise

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

*270 строк*

````python
"""Датаклассы предметной области - типизированное представление строк БД."""

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
    """Метаданные ключа. Сам секрет в объект не попадает - только по запросу."""

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

    # Параметры лежат в JSON и могли быть поправлены руками или старой
    # версией: битое значение не должно ронять запуск агента.
    @property
    def temperature(self) -> float:
        try:
            return float(self.params.get("temperature", 0.7))
        except (TypeError, ValueError):
            return 0.7

    @property
    def max_tokens(self) -> int:
        try:
            return max(1, int(self.params.get("max_tokens", 2048)))
        except (TypeError, ValueError):
            return 2048

    @property
    def tools(self) -> list[str]:
        raw = self.params.get("tools")
        return [str(t) for t in raw] if isinstance(raw, list) else []


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

*759 строк*

````python
"""Репозитории - единственная точка доступа к БД.

UI и ядро никогда не пишут SQL напрямую: это упрощает будущую замену
хранилища и гарантирует, что секреты шифруются в одном месте.
"""

from __future__ import annotations

import base64
import json
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


def _loads(raw: str | None) -> dict:
    try:
        data = json.loads(raw or "{}")
    except ValueError:
        return {}
    return data if isinstance(data, dict) else {}


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

        # Сначала расшифровываем всё старым ключом (если что-то не читается,
        # исключение вылетит до первой записи), затем пишем одной транзакцией:
        # сбой посередине не должен оставить часть ключей на новом мастер-ключе
        # при старом пароле - такие ключи было бы уже не расшифровать.
        rows = self.db.query(
            "SELECT id, secret_blob FROM api_keys WHERE user_id = ? AND secret_blob IS NOT NULL",
            (session.user_id,),
        )
        reencrypted = [
            (new_box.encrypt(old_box.decrypt(r["secret_blob"])), r["id"]) for r in rows
        ]
        # Ключ поискового API лежит в настройках воркспейсов, зашифрованный
        # тем же мастер-ключом. Без перешифровки он молча пропал бы после
        # смены пароля: расшифровать его новым ключом уже нельзя.
        resealed_ws = []
        for ws in self.db.query(
            "SELECT id, settings_json FROM workspaces WHERE user_id = ?", (session.user_id,)
        ):
            settings = _loads(ws["settings_json"])
            token = settings.get("search_api_key") or ""
            if isinstance(token, str) and token.startswith(SecretCodec.PREFIX):
                plain = SecretCodec(session).open(token)
                settings["search_api_key"] = (
                    SecretCodec.PREFIX + base64.b64encode(new_box.encrypt(plain)).decode("ascii")
                    if plain else ""
                )
                resealed_ws.append((dumps(settings), ws["id"]))
        new_hash = hash_password(new_password, new_verify_salt)
        with self.db.transaction() as conn:
            conn.executemany("UPDATE api_keys SET secret_blob = ? WHERE id = ?", reencrypted)
            conn.executemany("UPDATE workspaces SET settings_json = ? WHERE id = ?", resealed_ws)
            conn.execute(
                "UPDATE users SET password_hash = ?, verify_salt = ?, kdf_salt = ? WHERE id = ?",
                (new_hash, new_verify_salt, new_kdf_salt, session.user_id),
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

    def update_meta(self, key_id: int, **changes: Any) -> None:
        """Правит только метаданные (кэш моделей и т.п.), не трогая подпись и адрес.

        Фоновая проверка ключа пишет результат сюда: запись целиком затёрла
        бы правку, которую пользователь успел сделать, пока шёл запрос.
        """
        key = self.get(key_id)
        if key is None:
            return
        meta = {**key.meta, **changes}
        self.db.execute(
            "UPDATE api_keys SET meta_json = ? WHERE id = ? AND user_id = ?",
            (dumps(meta), key_id, self.session.user_id),
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
        """Закрывает открытые инциденты подзадачи - например, после доработки.

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
        """История решений, новые сверху - для вкладки супервайзера."""
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

        Возвращает последние ``limit`` записей в прямом порядке - из них
        дашборд строит кумулятивные кривые расхода.
        """
        rows = self.db.query(
            "SELECT created_at, tokens_in + tokens_out AS tokens, cost_usd FROM ("
            "  SELECT id, created_at, tokens_in, tokens_out, cost_usd FROM usage_log "
            "  WHERE workspace_id = ? ORDER BY id DESC LIMIT ?"
            ") ORDER BY id",
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
        """Инциденты по статусам - для плашки «требуют решения»."""
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
        """Последние ``limit`` сообщений агента в хронологическом порядке.

        Выбираются именно последние: при длинной истории (несколько кругов
        доработки) агенту важнее свежие замечания, чем самые первые шаги.
        """
        sql = "SELECT * FROM messages WHERE agent_id = ?"
        params: list[Any] = [agent_id]
        if subtask_id is not None:
            sql += " AND subtask_id = ?"
            params.append(subtask_id)
        sql += " ORDER BY id DESC LIMIT ?"
        params.append(limit)
        rows = [dict(r) for r in self.db.query(sql, params)]
        rows.reverse()
        return rows

    def clear(self, agent_id: int) -> None:
        self.db.execute("DELETE FROM messages WHERE agent_id = ?", (agent_id,))


class SecretCodec:
    """Шифрует короткие секреты, которые хранятся не в ``api_keys``.

    Например, ключ поискового API лежит в настройках воркспейса: там это
    строка base64, а открытым текстом она существует только в памяти.
    """

    PREFIX = "enc:"

    def __init__(self, session: Session) -> None:
        self.session = session

    def seal(self, text: str) -> str:
        if not text:
            return ""
        return self.PREFIX + base64.b64encode(self.session.box.encrypt(text)).decode("ascii")

    def open(self, token: str) -> str:
        if not token:
            return ""
        if not token.startswith(self.PREFIX):
            return token          # старое значение, сохранённое открытым текстом
        try:
            return self.session.box.decrypt(base64.b64decode(token[len(self.PREFIX):]))
        except Exception:  # noqa: BLE001 - повреждённый секрет равен отсутствующему
            return ""


class Repos:
    """Агрегатор репозиториев - удобно передавать одним объектом в UI."""

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
        self.secrets = SecretCodec(session)

    def recover_interrupted_runs(self) -> int:
        """Приводит в порядок статусы после аварийного завершения приложения.

        Если процесс упал посреди прогона, в базе остаются «работающие»
        задачи и агенты, которых на самом деле никто не выполняет. Интерфейс
        показывал бы их как активные, а повторный запуск считал бы занятыми.
        Возвращает количество исправленных записей.
        """
        user_ws = "SELECT id FROM workspaces WHERE user_id = ?"
        uid = (self.session.user_id,)
        with self.db.transaction() as conn:
            changed = conn.execute(
                f"UPDATE tasks SET status = 'stopped' WHERE status = 'running' "
                f"AND workspace_id IN ({user_ws})", uid).rowcount
            changed += conn.execute(
                f"UPDATE subtasks SET status = 'paused' WHERE status = 'running' "
                f"AND task_id IN (SELECT id FROM tasks WHERE workspace_id IN ({user_ws}))",
                uid).rowcount
            changed += conn.execute(
                f"UPDATE agents SET status = 'idle' WHERE status IN ('running', 'paused') "
                f"AND workspace_id IN ({user_ws})", uid).rowcount
            conn.execute(
                "UPDATE approvals SET decision = 'cancelled', "
                "comment = 'Приложение было закрыто до решения', decided_at = ? "
                f"WHERE decision = '' AND workspace_id IN ({user_ws})",
                (utcnow(), *uid))
        return changed
````


## Безопасность

### `core/security/crypto.py`

*164 строк*

````python
"""Криптография профиля: вывод мастер-ключа и шифрование секретов.

Схема (ответ на вопросы 4 и 5):

* Пароль профиля - единственный секрет, который вводит пользователь.
* ``Argon2id(password, salt)`` → 32-байтовый мастер-ключ. Ключ живёт только
  в оперативной памяти и никогда не пишется на диск.
* Проверка пароля при входе - по хэшу ``Argon2id(password, verify_salt)``,
  сравнение выполняется в постоянном времени.
* API-ключи шифруются ``AES-256-GCM`` мастер-ключом. На диск ложится
  ``nonce(12) || ciphertext || tag`` - сама БД остаётся обычным SQLite,
  открытым для чтения инструментами, но секреты в ней нечитаемы.

Зависимость только одна - ``cryptography``. Argon2id берётся из неё
(версия ≥ 42 с поддержкой KDF), при её отсутствии - из ``argon2-cffi``.
"""

from __future__ import annotations

import hmac
import os
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

# Параметры Argon2id: ~64 МБ памяти, 3 прохода - разумный компромисс
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
    except ImportError:  # pragma: no cover - путь для старых cryptography
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

_KEYRING_SERVICE = "agent-forge"


def keyring_available() -> bool:
    import importlib.util

    try:
        return importlib.util.find_spec("keyring") is not None
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

*194 строк*

````python
"""Единый интерфейс LLM-провайдера.

Все провайдеры (OpenAI, Anthropic, Gemini, Groq, OpenRouter, Ollama, HF)
приводятся к одному набору типов, чтобы ядро агентов ничего не знало
о различиях в их HTTP-API - включая формат tool-calling.
"""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, AsyncIterator, Callable

#: получатель фрагментов при потоковой генерации: (текст, вид). Вид -
#: ``"text"`` для ответа модели или ``"reasoning"`` для рассуждения
#: моделей, которые отдают его отдельно (DeepSeek-R1, Claude thinking и т.п.)
DeltaHandler = Callable[[str, str], None]


def estimate_tokens(text: str) -> int:
    """Грубая оценка числа токенов, если провайдер не прислал расход.

    Лучше посчитать приблизительно, чем записать ноль: нулевой расход
    незаметно обходил бы лимиты бюджета.
    """
    return max(1, len(text or "") // 4) if text else 0


#: признаки моделей, которые не ведут диалог: озвучка, распознавание речи,
#: картинки, видео, эмбеддинги, модерация. Агенту они не подходят, и в
#: выпадающем списке только мешают выбрать рабочую модель.
_NOT_CHAT = re.compile(
    r"embed|whisper|tts|transcri|speech|audio|realtime|live|image|imagen|veo|"
    r"lyria|dall-e|moderation|guard|orpheus|robotics|computer-use|deep-research|"
    r"antigravity|omni|davinci|babbage|aqa", re.IGNORECASE)


def is_chat_model(name: str) -> bool:
    """Годится ли модель для агента: текст на входе, текст и вызовы на выходе."""
    return bool(name) and not _NOT_CHAT.search(name)


@dataclass
class ToolCall:
    """Запрос модели на вызов инструмента."""

    id: str
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)
    #: служебная подпись вызова, которую провайдер просит вернуть вместе с
    #: ним в следующем запросе (``thoughtSignature`` у Gemini)
    signature: str = ""

    @staticmethod
    def parse_args(raw: Any) -> dict[str, Any]:
        """Аргументы вызова всегда словарь: инструменты получают их как ``**kwargs``."""
        if isinstance(raw, dict):
            return raw
        try:
            data = json.loads(raw or "{}")
        except (TypeError, ValueError):
            return {"_raw": str(raw)}
        return data if isinstance(data, dict) else {"_raw": str(raw)}


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
    и не хранить состояние диалога - вся история приходит в ``messages``.
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

    async def stream_complete(
        self,
        model: str,
        messages: list[ChatMessage],
        *,
        temperature: float = 0.7,
        max_tokens: int = 2048,
        tools: list[ToolSpec] | None = None,
        on_delta: DeltaHandler | None = None,
    ) -> CompletionResult:
        """Вызов модели с потоковой выдачей текста.

        Результат тот же, что у ``complete`` (текст, вызовы инструментов,
        расход), но по ходу генерации каждый фрагмент текста передаётся в
        ``on_delta`` - так интерфейс показывает рассуждение агента вживую.
        Реализация по умолчанию делает обычный вызов и отдаёт текст целиком:
        провайдер без стриминга просто покажет ответ разом.
        """
        result = await self.complete(model, messages, temperature=temperature,
                                     max_tokens=max_tokens, tools=tools)
        if on_delta and result.text:
            on_delta(result.text, "text")
        return result

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
        """Потоковая генерация. По умолчанию - эмуляция через ``complete``."""
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

*139 строк*

````python
"""Пресеты подключения к провайдерам «из коробки».

Пользователю достаточно выбрать провайдера и вставить свой ключ - base URL,
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
        # Только модели, которые вызывают инструменты через Chat Completions.
        # gpt-6-astra и gpt-6.1-sol умеют это лишь через Responses API: их
        # можно вписать вручную для агентов без инструментов или взять
        # через OpenRouter.
        suggested_models=["gpt-5.4-mini", "gpt-5.4-nano", "gpt-5.4", "gpt-6-luna",
                          "gpt-6-sol", "gpt-4.1", "gpt-4.1-mini", "gpt-4o-mini"],
        notes="Запросы платные: нужен пополненный баланс в Billing.",
    ),
    "anthropic": ProviderPreset(
        key="anthropic",
        title="Anthropic (Claude)",
        base_url="https://api.anthropic.com/v1",
        api_style="anthropic",
        docs_url="https://console.anthropic.com/settings/keys",
        suggested_models=[
            "claude-sonnet-5-5", "claude-opus-5-5", "claude-fable-5-1",
            "claude-haiku-4-5-20251001",
        ],
    ),
    "gemini": ProviderPreset(
        key="gemini",
        title="Google Gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta",
        api_style="gemini",
        free_tier=True,
        docs_url="https://aistudio.google.com/app/apikey",
        # Модели 2.5 Google открыл только тем, кто пользовался ими раньше,
        # 2.0 отключены: новым ключам они отвечают ошибкой.
        suggested_models=[
            "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash",
            "gemini-3.5-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite",
            "gemini-3.1-pro-preview", "gemini-3-flash-preview", "gemini-flash-latest",
        ],
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
            "openai/gpt-oss-120b", "openai/gpt-oss-20b", "qwen/qwen3.8-27b",
            "llama-3.3-70b-versatile", "llama-3.1-8b-instant",
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
            "google/gemini-3.8-flash", "openai/gpt-6-luna", "openai/gpt-6-astra",
            "anthropic/claude-sonnet-5.5", "deepseek/deepseek-v4.1-flash",
            "moonshotai/kimi-k3", "qwen/qwen3.8-27b:free", "google/gemma-4-31b-it:free",
            "nvidia/nemotron-3-super-120b-a12b:free",
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
        suggested_models=["qwen3.8:27b", "qwen3.6:27b", "granite4.1:8b", "lfm2.5:8b",
                          "qwen2.5:7b-instruct", "llama3.1:8b"],
        notes="Работает офлайн. Ключ не нужен - достаточно запущенного сервера Ollama.",
    ),
    "huggingface": ProviderPreset(
        key="huggingface",
        title="Hugging Face Inference",
        base_url="https://router.huggingface.co/v1",
        api_style="openai",
        free_tier=True,
        docs_url="https://huggingface.co/settings/tokens",
        suggested_models=[
            "Qwen/Qwen3.8-27B", "deepseek-ai/DeepSeek-V4.1-Flash", "openai/gpt-oss-120b",
            "moonshotai/Kimi-K3", "google/gemma-4-31B-it", "meta-llama/Llama-3.3-70B-Instruct",
        ],
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

*369 строк*

````python
"""Провайдер для всех OpenAI-совместимых API.

Покрывает OpenAI, Groq, OpenRouter, Ollama, Hugging Face Router и любой
локальный сервер (LM Studio, vLLM, llama.cpp) - различается только base_url.
"""

from __future__ import annotations

import json
import re
from typing import Any, AsyncIterator

import httpx

from providers.base import (
    ChatMessage,
    CompletionResult,
    DeltaHandler,
    LLMProvider,
    ProviderError,
    ToolCall,
    ToolSpec,
    Usage,
    estimate_tokens,
    is_chat_model,
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

    def _payload(self, model: str, messages: list[ChatMessage], temperature: float,
                 max_tokens: int, tools: list[ToolSpec] | None) -> dict[str, Any]:
        """Тело запроса с поправками под особенности конкретного API.

        Официальный OpenAI API для новых моделей не принимает ``max_tokens``
        (нужен ``max_completion_tokens``), а «рассуждающие» модели (o1, o3,
        o4, gpt-5) отвергают любую температуру, кроме стандартной. Совместимые
        серверы (Groq, Ollama, vLLM…) знают только ``max_tokens``.
        """
        payload: dict[str, Any] = {"model": model, "messages": self._to_wire(messages)}
        tool_payload = self._tools_payload(tools)
        if self.key == "openai":
            payload["max_completion_tokens"] = max_tokens
            if not _is_reasoning_model(model):
                payload["temperature"] = temperature
            if tool_payload:
                name = _bare(model)
                if name.startswith(_TOOLS_NEED_RESPONSES):
                    # Понятная ошибка вместо загадочного отказа API.
                    raise ProviderError(
                        f"Модель {model} вызывает инструменты только через Responses API, "
                        "а программа работает через Chat Completions. Выберите для агента "
                        "gpt-6-luna, gpt-6-sol или gpt-5.4, отключите ему инструменты "
                        "либо подключите эту модель через OpenRouter.")
                if name.startswith(_TOOLS_NEED_NO_REASONING):
                    # Через Chat Completions эти модели вызывают инструменты
                    # только без рассуждения.
                    payload["reasoning_effort"] = "none"
        else:
            payload["max_tokens"] = max_tokens
            payload["temperature"] = temperature
        if tool_payload:
            payload["tools"] = tool_payload
            payload["tool_choice"] = "auto"
        return payload

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
        payload = self._payload(model, messages, temperature, max_tokens, tools)

        try:
            resp = await self._http().post(
                f"{self.base_url}/chat/completions", headers=self._headers(), json=payload
            )
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc

        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)

        data = _json_body(resp)
        choice = (data.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        calls = [
            ToolCall(id=c.get("id", ""),
                     name=(c.get("function") or {}).get("name", ""),
                     arguments=ToolCall.parse_args((c.get("function") or {}).get("arguments")))
            for c in (msg.get("tool_calls") or [])
        ]
        text = msg.get("content") or ""
        u = data.get("usage") or {}
        if u:
            usage = Usage(_int(u.get("prompt_tokens")), _int(u.get("completion_tokens")))
        else:
            # Сервер не прислал расход - оценка лучше нуля, иначе вызов
            # незаметно обходил бы лимиты бюджета.
            usage = Usage(sum(len(m.content or "") for m in messages) // 4,
                          estimate_tokens(text))
        return CompletionResult(
            text=text,
            tool_calls=calls,
            usage=usage,
            finish_reason=choice.get("finish_reason") or "",
            model=data.get("model", model),
            raw=data,
        )

    async def stream_complete(self, model: str, messages: list[ChatMessage], *,
                              temperature: float = 0.7, max_tokens: int = 2048,
                              tools: list[ToolSpec] | None = None,
                              on_delta: DeltaHandler | None = None) -> CompletionResult:
        """Потоковый ``/chat/completions`` с разбором вызовов инструментов.

        Аргументы вызова инструмента приходят кусками JSON в нескольких
        чанках, поэтому они склеиваются по ``index`` и разбираются в конце.
        Расход токенов сервер присылает последним чанком, если попросить
        ``stream_options.include_usage``; часть совместимых серверов этот
        параметр не знает - тогда запрос повторяется без него.
        """
        payload = self._payload(model, messages, temperature, max_tokens, tools)
        payload["stream"] = True
        payload["stream_options"] = {"include_usage": True}
        try:
            return await self._stream_once(payload, model, messages, on_delta)
        except ProviderError as exc:
            if exc.status == 400 and "stream_options" in str(exc):
                payload.pop("stream_options", None)
                return await self._stream_once(payload, model, messages, on_delta)
            raise

    async def _stream_once(self, payload: dict[str, Any], model: str,
                           messages: list[ChatMessage],
                           on_delta: DeltaHandler | None) -> CompletionResult:
        text_parts: list[str] = []
        reasoning_parts: list[str] = []
        calls: dict[int, dict[str, str]] = {}
        usage: dict[str, Any] = {}
        finish_reason = ""
        model_name = model
        try:
            async with self._http().stream(
                "POST", f"{self.base_url}/chat/completions",
                headers=self._headers(), json=payload,
            ) as resp:
                if resp.status_code >= 400:
                    await resp.aread()
                    raise ProviderError(_error_text(resp), resp.status_code)
                async for line in resp.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    raw = line[5:].strip()
                    if not raw or raw == "[DONE]":
                        continue
                    try:
                        chunk = json.loads(raw)
                    except ValueError:
                        continue
                    if not isinstance(chunk, dict):
                        continue
                    if chunk.get("error"):
                        err = chunk["error"]
                        raise ProviderError(err.get("message", str(err))
                                            if isinstance(err, dict) else str(err))
                    model_name = chunk.get("model") or model_name
                    usage = (chunk.get("usage")
                             or (chunk.get("x_groq") or {}).get("usage")
                             or usage)
                    for choice in chunk.get("choices") or []:
                        delta = choice.get("delta") or {}
                        piece = delta.get("content")
                        if piece:
                            text_parts.append(piece)
                            if on_delta:
                                on_delta(piece, "text")
                        thought = delta.get("reasoning_content") or delta.get("reasoning")
                        if isinstance(thought, str) and thought:
                            reasoning_parts.append(thought)
                            if on_delta:
                                on_delta(thought, "reasoning")
                        for tc in delta.get("tool_calls") or []:
                            slot = calls.setdefault(int(tc.get("index", len(calls))),
                                                    {"id": "", "name": "", "args": ""})
                            slot["id"] = tc.get("id") or slot["id"]
                            fn = tc.get("function") or {}
                            slot["name"] = fn.get("name") or slot["name"]
                            slot["args"] += fn.get("arguments") or ""
                        finish_reason = choice.get("finish_reason") or finish_reason
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc

        text = "".join(text_parts)
        tool_calls = [
            ToolCall(id=slot["id"] or f"call_{index}", name=slot["name"],
                     arguments=ToolCall.parse_args(slot["args"]))
            for index, slot in sorted(calls.items()) if slot["name"]
        ]
        if usage:
            result_usage = Usage(_int(usage.get("prompt_tokens")),
                                 _int(usage.get("completion_tokens")))
        else:
            prompt = sum(len(m.content or "") for m in messages)
            output = text + "".join(reasoning_parts) + "".join(
                c["args"] for c in calls.values())
            result_usage = Usage(prompt // 4, estimate_tokens(output))
        return CompletionResult(text=text, tool_calls=tool_calls, usage=result_usage,
                                finish_reason=finish_reason, model=model_name)

    async def stream(self, model: str, messages: list[ChatMessage], *,
                     temperature: float = 0.7,
                     max_tokens: int = 2048) -> AsyncIterator[str]:
        payload = self._payload(model, messages, temperature, max_tokens, None)
        payload["stream"] = True
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
        try:
            data = resp.json()
        except ValueError as exc:
            raise ProviderError(f"Сервер вернул не JSON: {resp.text[:200]}") from exc
        # Обычно {"data": [...]}, но часть серверов отдаёт голый список.
        items = data if isinstance(data, list) else (data.get("data") or data.get("models") or [])
        names = [it.get("id") or it.get("name", "") for it in items if isinstance(it, dict)]
        # Озвучка, распознавание речи, картинки и эмбеддинги агенту не подходят.
        return sorted(n for n in names if is_chat_model(n))


#: модели, которые через Chat Completions вызывают инструменты только при
#: ``reasoning_effort: none`` (так написано в их карточках на сайте OpenAI)
_TOOLS_NEED_NO_REASONING = ("gpt-6-luna", "gpt-6-sol", "gpt-5.6-luna")
#: модели, которые через Chat Completions инструменты не вызывают вовсе
_TOOLS_NEED_RESPONSES = ("gpt-6-astra", "gpt-6.1-sol")


def _bare(model: str) -> str:
    return (model or "").lower().rsplit("/", 1)[-1]


def _is_reasoning_model(model: str) -> bool:
    """Модели OpenAI с рассуждением: o-серия и GPT начиная с пятой версии.

    Они принимают только стандартную температуру, любую другую API отвергает.
    """
    name = _bare(model)
    if re.match(r"o\d", name):
        return True
    match = re.match(r"gpt-(\d+)", name)
    return bool(match) and int(match.group(1)) >= 5 and "-chat" not in name


def _int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def _json_body(resp: httpx.Response) -> dict[str, Any]:
    """Тело ответа как словарь; прокси и заглушки иногда отдают HTML."""
    try:
        data = resp.json()
    except ValueError as exc:
        raise ProviderError(f"Сервер вернул не JSON: {resp.text[:200]}", resp.status_code) from exc
    if not isinstance(data, dict):
        raise ProviderError("Неожиданный формат ответа сервера", resp.status_code)
    return data


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

*261 строк*

````python
"""Провайдер Anthropic Messages API.

Отличия от OpenAI, которые здесь скрываются:
* системный промпт передаётся отдельным полем ``system``;
* результат инструмента - блок ``tool_result`` внутри сообщения роли ``user``;
* заголовки ``x-api-key`` и ``anthropic-version``.
"""

from __future__ import annotations

from typing import Any, AsyncIterator

import httpx

from providers.base import (
    ChatMessage,
    CompletionResult,
    DeltaHandler,
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

    def _payload(self, model: str, messages: list[ChatMessage], temperature: float,
                 max_tokens: int, tools: list[ToolSpec] | None) -> dict[str, Any]:
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
        return payload

    async def stream_complete(self, model: str, messages: list[ChatMessage], *,
                              temperature: float = 0.7, max_tokens: int = 2048,
                              tools: list[ToolSpec] | None = None,
                              on_delta: DeltaHandler | None = None) -> CompletionResult:
        """Потоковый Messages API: текст, рассуждение и вызовы инструментов.

        Блоки ответа приходят событиями ``content_block_*``; аргументы
        ``tool_use`` приходят кусками JSON (``input_json_delta``) и
        собираются по индексу блока.
        """
        import json as _json

        payload = self._payload(model, messages, temperature, max_tokens, tools)
        payload["stream"] = True
        blocks: dict[int, dict[str, Any]] = {}
        usage_in = usage_out = 0
        stop_reason = ""
        model_name = model
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
                    kind = event.get("type")
                    if kind == "message_start":
                        message = event.get("message") or {}
                        model_name = message.get("model", model_name)
                        u = message.get("usage") or {}
                        usage_in = int(u.get("input_tokens", 0))
                        usage_out = int(u.get("output_tokens", 0))
                    elif kind == "content_block_start":
                        block = dict(event.get("content_block") or {})
                        block["_json"] = ""
                        blocks[int(event.get("index", len(blocks)))] = block
                    elif kind == "content_block_delta":
                        block = blocks.setdefault(int(event.get("index", 0)),
                                                  {"type": "text", "text": "", "_json": ""})
                        delta = event.get("delta") or {}
                        if delta.get("type") == "text_delta":
                            piece = delta.get("text", "")
                            block["text"] = block.get("text", "") + piece
                            if on_delta and piece:
                                on_delta(piece, "text")
                        elif delta.get("type") == "thinking_delta":
                            piece = delta.get("thinking", "")
                            if on_delta and piece:
                                on_delta(piece, "reasoning")
                        elif delta.get("type") == "input_json_delta":
                            block["_json"] += delta.get("partial_json", "")
                    elif kind == "message_delta":
                        stop_reason = (event.get("delta") or {}).get("stop_reason") or stop_reason
                        u = event.get("usage") or {}
                        usage_out = int(u.get("output_tokens", usage_out))
                    elif kind == "error":
                        err = event.get("error") or {}
                        raise ProviderError(err.get("message", "ошибка потока Anthropic"))
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc

        text_parts: list[str] = []
        calls: list[ToolCall] = []
        for _, block in sorted(blocks.items()):
            if block.get("type") == "text":
                text_parts.append(block.get("text", ""))
            elif block.get("type") == "tool_use":
                args = ToolCall.parse_args(block["_json"] or block.get("input") or {})
                calls.append(ToolCall(id=block.get("id", ""), name=block.get("name", ""),
                                      arguments=args))
        return CompletionResult(text="".join(text_parts), tool_calls=calls,
                                usage=Usage(usage_in, usage_out),
                                finish_reason=stop_reason, model=model_name)

    async def complete(self, model: str, messages: list[ChatMessage], *,
                       temperature: float = 0.7, max_tokens: int = 2048,
                       tools: list[ToolSpec] | None = None) -> CompletionResult:
        payload = self._payload(model, messages, temperature, max_tokens, tools)
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
                                      arguments=ToolCall.parse_args(block.get("input") or {})))
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
            # Список постраничный (по умолчанию 20 штук) - просим сразу все.
            resp = await self._http().get(f"{self.base_url}/models", headers=self._headers(),
                                          params={"limit": 1000})
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

*318 строк*

````python
"""Провайдер Google Gemini (generativeLanguage API).

Особенности, скрытые внутри класса:
* роли называются ``user``/``model``, системный промпт - ``systemInstruction``;
* ключ передаётся заголовком ``x-goog-api-key``;
* инструменты описываются как ``functionDeclarations``.
"""

from __future__ import annotations

import re
import uuid
from typing import Any

import httpx

from providers.base import (
    ChatMessage,
    CompletionResult,
    DeltaHandler,
    LLMProvider,
    ProviderError,
    ToolCall,
    ToolSpec,
    Usage,
    is_chat_model,
)

#: сколько токенов сверх лимита ответа оставить «думающим» моделям: у Gemini
#: ``maxOutputTokens`` включает размышления, и при лимите агента в 2048
#: модель могла потратить всё на них и вернуть пустой ответ
THINKING_HEADROOM = 8192

#: почему кандидат остался пустым (``finishReason``) и что сказать человеку
_EMPTY_REASONS = {
    "MAX_TOKENS": "модель израсходовала лимит токенов на размышления и не успела "
                  "ответить. Увеличьте «Макс. токенов» у агента",
    "SAFETY": "ответ заблокирован фильтром безопасности Google",
    "PROHIBITED_CONTENT": "ответ заблокирован фильтром безопасности Google",
    "BLOCKLIST": "ответ заблокирован фильтром безопасности Google",
    "SPII": "ответ заблокирован: в нём были персональные данные",
    "RECITATION": "ответ заблокирован: он повторял защищённый текст",
    "MALFORMED_FUNCTION_CALL": "модель сформировала некорректный вызов инструмента",
}


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
        previous_tool = False
        for m in messages:
            if m.role == "system":
                system_parts.append(m.content)
                continue
            if m.role == "tool":
                part = {"functionResponse": {"name": m.name or "tool",
                                             "response": {"result": m.content}}}
                # Ответы на несколько вызовов одного хода Gemini ждёт одним
                # сообщением: число частей должно совпасть с числом вызовов.
                if previous_tool:
                    contents[-1]["parts"].append(part)
                else:
                    contents.append({"role": "user", "parts": [part]})
                previous_tool = True
                continue
            previous_tool = False
            if m.role == "assistant":
                parts: list[dict[str, Any]] = []
                if m.content:
                    parts.append({"text": m.content})
                for tc in m.tool_calls:
                    call: dict[str, Any] = {"functionCall": {"name": tc.name, "args": tc.arguments}}
                    if tc.signature:
                        # Новые модели требуют вернуть подпись вместе с вызовом.
                        call["thoughtSignature"] = tc.signature
                    parts.append(call)
                contents.append({"role": "model", "parts": parts or [{"text": " "}]})
            else:
                contents.append({"role": "user", "parts": [{"text": m.content or " "}]})
        return "\n\n".join(p for p in system_parts if p), contents

    def _payload(self, messages: list[ChatMessage], temperature: float, max_tokens: int,
                 tools: list[ToolSpec] | None, model: str = "") -> dict[str, Any]:
        system, contents = self._split(messages)
        config: dict[str, Any] = {"temperature": temperature, "maxOutputTokens": max_tokens}
        if _thinks(model):
            # Размышления входят в maxOutputTokens: без запаса модель может
            # потратить весь лимит на них и не выдать ответа. Сами мысли
            # просим присылать, чтобы экран «Выполнение» показывал их вживую.
            config["maxOutputTokens"] = max_tokens + THINKING_HEADROOM
            config["thinkingConfig"] = {"includeThoughts": True}
        if _is_gemini3(model):
            # Для Gemini 3 Google просит не трогать температуру: ниже 1.0
            # модель склонна зацикливаться (а супервайзер ставит 0.2).
            config.pop("temperature", None)
        payload: dict[str, Any] = {"contents": contents, "generationConfig": config}
        if system:
            payload["systemInstruction"] = {"parts": [{"text": system}]}
        if tools:
            payload["tools"] = [{
                "functionDeclarations": [
                    {"name": t.name, "description": t.description,
                     "parameters": _schema(t.parameters)}
                    for t in tools
                ]
            }]
        return payload

    @staticmethod
    def _call(part: dict[str, Any]) -> ToolCall:
        fc = part.get("functionCall") or {}
        return ToolCall(id=uuid.uuid4().hex[:12], name=fc.get("name", ""),
                        arguments=ToolCall.parse_args(fc.get("args") or {}),
                        signature=part.get("thoughtSignature") or "")

    async def stream_complete(self, model: str, messages: list[ChatMessage], *,
                              temperature: float = 0.7, max_tokens: int = 2048,
                              tools: list[ToolSpec] | None = None,
                              on_delta: DeltaHandler | None = None) -> CompletionResult:
        """``streamGenerateContent`` в режиме SSE.

        Каждый чанк - полноценный ответ с частью ``parts``; вызовы функций
        приходят целиком, а ``usageMetadata`` в последнем чанке содержит
        итоговый расход.
        """
        import json as _json

        payload = self._payload(messages, temperature, max_tokens, tools, model)
        url = f"{self.base_url}/models/{_model_id(model)}:streamGenerateContent?alt=sse"
        text_parts: list[str] = []
        calls: list[ToolCall] = []
        usage: dict[str, Any] = {}
        finish_reason = ""
        block_reason = ""
        try:
            async with self._http().stream("POST", url, headers=self._headers(),
                                           json=payload) as resp:
                if resp.status_code >= 400:
                    await resp.aread()
                    raise ProviderError(_error_text(resp), resp.status_code)
                async for line in resp.aiter_lines():
                    if not line.startswith("data:"):
                        continue
                    try:
                        chunk = _json.loads(line[5:].strip())
                    except ValueError:
                        continue
                    usage = chunk.get("usageMetadata") or usage
                    block_reason = ((chunk.get("promptFeedback") or {}).get("blockReason")
                                    or block_reason)
                    for candidate in chunk.get("candidates") or []:
                        finish_reason = candidate.get("finishReason") or finish_reason
                        for part in (candidate.get("content") or {}).get("parts", []):
                            if "functionCall" in part:
                                calls.append(self._call(part))
                            elif part.get("text"):
                                kind = "reasoning" if part.get("thought") else "text"
                                if kind == "text":
                                    text_parts.append(part["text"])
                                if on_delta:
                                    on_delta(part["text"], kind)
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        text = "".join(text_parts)
        _raise_if_empty(text, calls, finish_reason, block_reason)
        return CompletionResult(
            text=text, tool_calls=calls,
            usage=Usage(int(usage.get("promptTokenCount", 0)),
                        int(usage.get("candidatesTokenCount", 0))
                        + int(usage.get("thoughtsTokenCount", 0))),
            finish_reason=finish_reason, model=model,
        )

    async def complete(self, model: str, messages: list[ChatMessage], *,
                       temperature: float = 0.7, max_tokens: int = 2048,
                       tools: list[ToolSpec] | None = None) -> CompletionResult:
        payload = self._payload(messages, temperature, max_tokens, tools, model)
        url = f"{self.base_url}/models/{_model_id(model)}:generateContent"
        try:
            resp = await self._http().post(url, headers=self._headers(), json=payload)
        except httpx.HTTPError as exc:
            raise ProviderError(f"Сетевая ошибка: {exc}") from exc
        if resp.status_code >= 400:
            raise ProviderError(_error_text(resp), resp.status_code)

        try:
            data = resp.json()
        except ValueError as exc:
            raise ProviderError(f"Сервер вернул не JSON: {resp.text[:200]}") from exc
        candidate = (data.get("candidates") or [{}])[0]
        text_parts, calls = [], []
        for part in (candidate.get("content") or {}).get("parts", []):
            if "functionCall" in part:
                calls.append(self._call(part))
            elif "text" in part and not part.get("thought"):
                # Рассуждение «думающих» моделей в ответ не входит.
                text_parts.append(part["text"])
        text = "".join(text_parts)
        _raise_if_empty(text, calls, candidate.get("finishReason", ""),
                        (data.get("promptFeedback") or {}).get("blockReason", ""))
        u = data.get("usageMetadata") or {}
        return CompletionResult(
            text=text,
            tool_calls=calls,
            # Токены рассуждения оплачиваются как выходные.
            usage=Usage(int(u.get("promptTokenCount", 0)),
                        int(u.get("candidatesTokenCount", 0))
                        + int(u.get("thoughtsTokenCount", 0))),
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
            methods = m.get("supportedGenerationMethods") or ["generateContent"]
            # Озвучка, картинки и эмбеддинги агенту не подходят, а список и так
            # длинный: оставляем только модели для диалога.
            if "generateContent" in methods and is_chat_model(name):
                names.append(name)
        return sorted(names)


def _model_id(model: str) -> str:
    """Имя модели для адреса запроса: префикс «models/» уже есть в пути."""
    return (model or "").strip().removeprefix("models/")


def _thinks(model: str) -> bool:
    """Модель рассуждает перед ответом: семейства 2.5 и 3.x, алиасы latest."""
    name = _model_id(model).lower()
    return bool(re.match(r"gemini-(2\.5|[3-9])", name)) or (
        name.startswith("gemini-") and name.endswith("-latest"))


def _is_gemini3(model: str) -> bool:
    name = _model_id(model).lower()
    return bool(re.match(r"gemini-[3-9]", name)) or (
        name.startswith("gemini-") and name.endswith("-latest"))


def _raise_if_empty(text: str, calls: list[ToolCall], finish_reason: str,
                    block_reason: str) -> None:
    """Пустой ответ без объяснения выглядел бы как «агент ничего не сделал».

    Gemini в таких случаях сообщает причину отдельным полем: лимит токенов
    ушёл на размышления, сработал фильтр безопасности и т.п. Её и отдаём.
    """
    if text.strip() or calls:
        return
    if block_reason:
        raise ProviderError(f"Gemini отклонил запрос: {block_reason}")
    reason = (finish_reason or "").upper()
    if reason in _EMPTY_REASONS:
        raise ProviderError(f"Gemini: {_EMPTY_REASONS[reason]} ({reason})")


#: ключи JSON Schema, которые понимает ``functionDeclarations``; прочие
#: (``default``, ``additionalProperties``, ``$schema``…) Gemini отвергает
_SCHEMA_KEYS = {"type", "format", "description", "nullable", "enum", "properties",
                "required", "items", "minimum", "maximum", "minItems", "maxItems"}


def _schema(node: Any) -> Any:
    """Приводит JSON Schema инструмента к подмножеству, которое принимает Gemini."""
    if not isinstance(node, dict):
        return node
    out: dict[str, Any] = {}
    for key, value in node.items():
        if key not in _SCHEMA_KEYS:
            continue
        if key == "properties" and isinstance(value, dict):
            out[key] = {name: _schema(sub) for name, sub in value.items()}
        elif key == "items":
            out[key] = _schema(value)
        else:
            out[key] = value
    return out


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

Провайдеры почти никогда не возвращают цену - только токены. Поэтому
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
        extra = {"HTTP-Referer": "https://localhost/agent-forge",
                 "X-Title": "Agent Forge"}
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
    """Сбрасывает кэш - используется после ручного редактирования таблицы цен."""
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

*77 строк*

````json
{
  "_comment": "USD за 1 000 000 токенов: [вход, выход]. Цены ориентировочные, обновляйте вручную по прайс-листам провайдеров. Ключ ищется по точному совпадению, затем по самому длинному префиксу.",
  "_default": [0.0, 0.0],

  "openai": {
    "gpt-6-astra": [10.00, 50.00],
    "gpt-6.1-sol": [2.00, 10.00],
    "gpt-6-sol": [2.00, 10.00],
    "gpt-6-luna": [0.10, 0.50],
    "gpt-5.6-luna": [0.20, 1.20],
    "gpt-5.4": [2.50, 15.00],
    "gpt-5.4-mini": [0.75, 4.50],
    "gpt-5.4-nano": [0.20, 1.25],
    "gpt-5-mini": [0.25, 2.00],
    "gpt-4o": [2.50, 10.00],
    "gpt-4o-mini": [0.15, 0.60],
    "gpt-4.1": [2.00, 8.00],
    "gpt-4.1-mini": [0.40, 1.60],
    "gpt-4.1-nano": [0.10, 0.40],
    "o3": [2.00, 8.00],
    "o4-mini": [1.10, 4.40]
  },

  "anthropic": {
    "claude-fable-5-1": [10.00, 50.00],
    "claude-opus-5-5": [4.00, 20.00],
    "claude-sonnet-5-5": [2.00, 10.00],
    "claude-haiku-4-5": [1.00, 5.00],
    "claude-opus-4": [15.00, 75.00],
    "claude-sonnet-4": [3.00, 15.00],
    "claude-3-7-sonnet": [3.00, 15.00],
    "claude-3-5-sonnet": [3.00, 15.00],
    "claude-3-5-haiku": [0.80, 4.00],
    "claude-3-haiku": [0.25, 1.25]
  },

  "gemini": {
    "gemini-3.8-flash": [0.75, 3.75],
    "gemini-3.7-flash": [0.75, 3.75],
    "gemini-3.6-flash": [0.75, 3.75],
    "gemini-3.5-flash-lite": [0.30, 2.50],
    "gemini-3.5-flash": [1.50, 9.00],
    "gemini-3.1-flash-lite": [0.25, 1.50],
    "gemini-3.1-pro": [2.00, 12.00],
    "gemini-3-flash": [0.50, 3.00],
    "gemini-flash-latest": [0.75, 3.75],
    "gemini-2.5-pro": [1.25, 10.00],
    "gemini-2.5-flash": [0.30, 2.50],
    "gemini-2.5-flash-lite": [0.10, 0.40],
    "gemini-2.0-flash": [0.10, 0.40]
  },

  "groq": {
    "openai/gpt-oss-120b": [0.15, 0.75],
    "openai/gpt-oss-20b": [0.10, 0.50],
    "llama-3.3-70b-versatile": [0.59, 0.79],
    "llama-3.1-8b-instant": [0.05, 0.08],
    "qwen/qwen3-32b": [0.29, 0.59],
    "deepseek-r1-distill-llama-70b": [0.75, 0.99]
  },

  "openrouter": {
    "google/gemini-3.8-flash": [0.75, 3.75],
    "openai/gpt-6-luna": [0.10, 0.50],
    "openai/gpt-6-astra": [10.00, 50.00],
    "anthropic/claude-sonnet-5.5": [2.00, 10.00],
    "deepseek/deepseek-v4.1-flash": [0.30, 1.20],
    "moonshotai/kimi-k3": [3.00, 15.00],
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
        except Exception as exc:  # noqa: BLE001 - модель должна узнать о сбое
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

*303 строк*

````python
"""Песочница для исполнения кода агентами.

Ответ на вопрос 3: интерфейс ``Sandbox`` с двумя реализациями.

``SubprocessSandbox`` (по умолчанию, работает везде)
    * отдельный процесс в одноразовом временном каталоге;
    * ``setsid`` + убийство всей группы процессов по таймауту;
    * POSIX: ``RLIMIT_CPU``, ``RLIMIT_AS``, ``RLIMIT_FSIZE``, ``RLIMIT_NPROC``;
    * вычищенное окружение (нет API-ключей и прочих переменных хоста);
    * сеть по умолчанию отключается подстановкой недоступного прокси -
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
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

# Языки, которые разрешено исполнять. Shell намеренно не включён в Docker-режиме
# по умолчанию - он нужен реже, а рисков даёт больше.
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


def _preexec(memory_mb: int, cpu_seconds: int):  # pragma: no cover - POSIX-only
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
    """Убивает процесс вместе со всеми потомками.

    На Windows ``proc.kill()`` завершает только сам процесс: запущенные им
    дочерние (``subprocess``, ``multiprocessing``) продолжили бы работать
    после таймаута. ``taskkill /T`` снимает всё дерево.
    """
    try:
        if os.name == "posix":
            os.killpg(os.getpgid(proc.pid), 9)
        else:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                           capture_output=True, timeout=10,
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            if proc.returncode is None:
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

        # Имя нужно, чтобы по таймауту остановить именно контейнер: убийство
        # процесса docker CLI оставило бы контейнер работать в фоне.
        name = f"aiorc-{uuid.uuid4().hex[:12]}"
        cmd = [
            "docker", "run", "--rm", "--name", name,
            "--network", "bridge" if network else "none",
            "--memory", f"{memory_mb}m", "--memory-swap", f"{memory_mb}m",
            "--cpus", "1", "--pids-limit", "128",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", "1000:1000",
            # Корень контейнера только для чтения; писать можно в /tmp и в
            # одноразовый каталог со скриптом.
            "--read-only", "--tmpfs", "/tmp:rw,size=64m",
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
                await _docker_kill(name)
                proc.kill()
                out, err = b"", "Контейнер остановлен по таймауту".encode("utf-8")
            return SandboxResult(
                proc.returncode if proc.returncode is not None else -1,
                out.decode("utf-8", "replace"), err.decode("utf-8", "replace"),
                timed_out, self.name,
            )
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


async def _docker_kill(name: str) -> None:
    try:
        proc = await asyncio.create_subprocess_exec(
            "docker", "kill", name,
            stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.DEVNULL,
        )
        await asyncio.wait_for(proc.wait(), timeout=10)
    except Exception:  # noqa: BLE001 - контейнер мог уже завершиться сам
        pass


#: результат проверки Docker кэшируется: ``docker info`` занимает секунды
_DOCKER_CACHE: dict[str, float | bool] = {}
_DOCKER_TTL = 60.0


def docker_available(use_cache: bool = True) -> bool:
    """Проверяет, что Docker установлен и демон отвечает."""
    now = time.monotonic()
    if use_cache and _DOCKER_CACHE and now - float(_DOCKER_CACHE["at"]) < _DOCKER_TTL:
        return bool(_DOCKER_CACHE["ok"])
    ok = False
    if shutil.which("docker") is not None:
        try:
            res = subprocess.run(["docker", "info", "--format", "{{json .ServerVersion}}"],
                                 capture_output=True, timeout=5,
                                 creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            ok = res.returncode == 0 and bool(json.loads(res.stdout or b'""'))
        except Exception:  # noqa: BLE001
            ok = False
    _DOCKER_CACHE.update(ok=ok, at=now)
    return ok


async def docker_available_async() -> bool:
    """То же, но без блокировки общего asyncio-лупа (и интерфейса вместе с ним)."""
    return await asyncio.to_thread(docker_available)


async def get_sandbox(backend: str = "auto") -> Sandbox:
    """Фабрика песочницы по настройке воркспейса."""
    if backend == "docker":
        return DockerSandbox()
    if backend == "subprocess":
        return SubprocessSandbox()
    return DockerSandbox() if await docker_available_async() else SubprocessSandbox()
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
            raise ToolError("Пустой код - нечего исполнять")
        if language not in LANG_COMMANDS:
            raise ToolError(f"Язык «{language}» не поддерживается")

        sandbox = await get_sandbox(ctx.sandbox_backend)
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

*118 строк*

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
            raise ToolError(f"«{path.name}» - каталог, используй list_dir")
        try:
            limit = min(max(1, int(kwargs.get("max_bytes") or MAX_READ_BYTES)), MAX_READ_BYTES)
        except (TypeError, ValueError):
            limit = MAX_READ_BYTES
        # Читаем только нужный кусок: файл на гигабайт не должен целиком
        # попадать в память ради первых 200 КБ.
        with path.open("rb") as fh:
            data = fh.read(limit)
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
            raise ToolError(f"«{path.name}» - не каталог")
        lines: list[str] = []
        for item in sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())):
            if item.name.startswith("."):
                continue
            lines.append(f"{'DIR ' if item.is_dir() else 'FILE'}  {item.name}"
                         + ("" if item.is_dir() else f"  ({_human(item)})"))
        return f"Каталог: {path}\n" + ("\n".join(lines) if lines else "(пусто)")


def _human(path: Path) -> str:
    try:
        size = path.stat().st_size
    except OSError:          # битая ссылка или файл исчез между листингом и stat
        return "?"
    for unit in ("Б", "КБ", "МБ", "ГБ"):
        if size < 1024:
            return f"{size:.0f} {unit}"
        size /= 1024
    return f"{size:.1f} ТБ"
````

### `core/tools/web_search.py`

*199 строк*

````python
"""Веб-поиск и чтение страниц.

Ответ на вопрос 9: по умолчанию используется DuckDuckGo (библиотека ``ddgs``) -
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
#: сколько байт страницы скачивать не больше
MAX_DOWNLOAD_BYTES = 5_000_000


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
        try:
            n = max(1, min(int(kwargs.get("max_results") or 5), MAX_RESULTS))
        except (TypeError, ValueError):
            n = 5

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
                headers={"User-Agent": "Mozilla/5.0 (compatible; AgentForge/1.1)"},
            ) as client:
                async with client.stream("GET", url) as resp:
                    if resp.status_code >= 400:
                        raise ToolError(f"HTTP {resp.status_code} при загрузке {url}")
                    kind = resp.headers.get("content-type", "").split(";")[0].strip().lower()
                    if kind and not (kind.startswith("text/") or "html" in kind
                                     or "xml" in kind or "json" in kind):
                        raise ToolError(f"По ссылке не страница, а файл ({kind}) - "
                                        "его текст этим инструментом не прочитать")
                    # Ограничение объёма: ссылка на гигабайтный файл не должна
                    # выкачиваться в память целиком.
                    body = bytearray()
                    async for chunk in resp.aiter_bytes():
                        body += chunk
                        if len(body) >= MAX_DOWNLOAD_BYTES:
                            break
                    encoding = resp.encoding or "utf-8"
        except ToolError:
            raise
        except Exception as exc:  # noqa: BLE001
            raise ToolError(f"Не удалось загрузить страницу: {exc}") from exc

        try:
            html = bytes(body).decode(encoding, "replace")
        except LookupError:          # сервер назвал несуществующую кодировку
            html = bytes(body).decode("utf-8", "replace")
        text = await asyncio.to_thread(_extract_text, html)
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

*105 строк*

````python
"""Шина событий между ядром и интерфейсом.

Ядро не знает о Qt: оно публикует события, а UI на них подписывается.
Всё происходит в одном asyncio-лупе (он же луп Qt), поэтому обработчики
могут напрямую трогать виджеты - отдельная синхронизация не нужна.
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
    AGENT_DELTA = "agent_delta"          # очередной фрагмент текста модели (стриминг)
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
    BUDGET_EXTENDED = "budget_extended"    # пользователь поднял лимит во время прогона
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
            except Exception:  # noqa: BLE001 - UI не должен ронять агентов
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
"""Шаблоны ролей агентов - отправная точка, которую пользователь правит под себя.

Системные промпты намеренно написаны так, чтобы агент:
* знал общую задачу проекта, но отвечал только за свою подзадачу;
* не догадывался о существовании конкретных коллег (изоляция);
* честно сообщал о неуверенности - это сырьё для human-in-the-loop.
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
4. Если данных не хватает - прямо скажи, чего не хватает, не выдумывай.
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
            "Ты - аналитик. Твоя работа: собрать факты, проверить их по источникам, "
            "структурировать и выделить риски и неизвестные. Ты не пишешь код и не "
            "принимаешь продуктовых решений - ты даёшь основу для них. "
            "Каждый нетривиальный факт сопровождай ссылкой или пометкой «без источника»."
        ),
        suggested_tools=["web_search", "files"],
    ),
    RoleTemplate(
        key="developer",
        title_ru="Разработчик",
        title_en="Developer",
        prompt=(
            "Ты - разработчик. Твоя работа: писать рабочий, читаемый код по заданию. "
            "Прежде чем отдать код, мысленно прогони его на граничных случаях, а при "
            "возможности - запусти в песочнице. Код отдавай целыми файлами с указанием "
            "пути, а не фрагментами без контекста."
        ),
        suggested_tools=["code_exec", "files", "web_search"],
    ),
    RoleTemplate(
        key="tester",
        title_ru="Тестировщик",
        title_en="Tester",
        prompt=(
            "Ты - тестировщик. Твоя работа: находить, где решение ломается. "
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
            "Ты - критик. Твоя работа: искать слабые места в предложенном решении: "
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
            "Ты - технический писатель. Твоя работа: превращать сырые материалы в "
            "понятный документ: структура, однозначные формулировки, примеры. "
            "Не добавляй фактов, которых нет в исходных материалах; если чего-то "
            "не хватает - оставь пометку TODO с точным вопросом."
        ),
        suggested_tools=["files"],
    ),
    RoleTemplate(
        key="researcher",
        title_ru="Исследователь",
        title_en="Researcher",
        prompt=(
            "Ты - исследователь. Твоя работа: находить первоисточники, сравнивать "
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
            "Ты - супервайзер команды исполнителей. Ты проверяешь их отчёты по чек-листу: "
            "(1) соответствие исходному заданию; (2) внутренняя логическая "
            "непротиворечивость; (3) фактические ошибки и выдумки; (4) противоречия "
            "между отчётами разных исполнителей. Ты не переписываешь работу за них - "
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

*499 строк*

````python
"""Этап 4 - исполнитель одного агента над одной подзадачей.

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
from typing import TYPE_CHECKING

from app.config import PATHS
from core.events import Event, EventBus, EventType
from core.tools.base import ToolContext, ToolRegistry, expand_tool_names
from providers.base import ChatMessage, CompletionResult, LLMProvider, ProviderError, ToolCall
from providers.factory import estimate_cost
from storage.models import Agent, Subtask, Task
from storage.repositories import Repos

if TYPE_CHECKING:  # pragma: no cover
    from core.budget import BudgetGuard

log = logging.getLogger("aiorc.runner")

#: сколько последних сообщений истории подмешивать без сжатия
HISTORY_WINDOW = 24
#: после какого количества символов истории включается сжатие
HISTORY_COMPACT_CHARS = 24_000
#: фрагменты стриминга копятся до такой длины, прежде чем уйти в шину:
#: отправлять событие на каждый токен бессмысленно дорого
DELTA_FLUSH_CHARS = 16
#: статусы HTTP, при которых провайдер, вероятно, просто не умеет стриминг
STREAM_UNSUPPORTED = {400, 404, 405, 415, 422, 501}

FINALIZE_PROMPT = (
    "Лимит шагов на эту подзадачу исчерпан, инструменты больше недоступны. "
    "Подведи итог по тому, что уже успел выяснить: выдай его после строки RESULT: "
    "и укажи строку CONFIDENCE: <0..1>. Честно отметь, что осталось непроверенным."
)


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
        # Пустой список значит «все инструменты выключены», а не «все включены».
        raw_enabled = workspace_settings.get("tools_enabled")
        enabled = (expand_tool_names(raw_enabled) if raw_enabled is not None
                   else registry.names())
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
            # Ключ поискового API хранится в настройках зашифрованным.
            search_api_key=self.repos.secrets.open(self.settings.get("search_api_key", "")),
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
                "(источник не указан намеренно - оценивай содержание, а не авторитет)",
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
                chunks.append(f"- {dep.title}:\n{dep.result[:4000]}")
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

    # -- вызов модели --------------------------------------------------------
    async def _check_budget(self) -> str:
        """Проверка ДО вызова модели: узнавать о лимите постфактум бессмысленно.

        Возвращает текст ошибки, если вызов делать нельзя, иначе пустую строку.
        """
        if self.budget is None:
            return ""
        ensure = getattr(self.budget, "ensure_allowed", None)
        blocked = (await ensure(self.agent.id) if ensure is not None
                   else self.budget.blocking_scope(self.agent.id))
        return f"Лимит исчерпан - {blocked.reason()}" if blocked is not None else ""

    async def _call_model(self, messages: list[ChatMessage], step: int,
                          tools: list | None) -> CompletionResult:
        """Один вызов модели со стримингом текста в интерфейс.

        Фрагменты копятся в небольшой буфер и уходят в шину пачками. Если
        провайдер отверг потоковый запрос ещё до первого фрагмента (частая
        история с самописными OpenAI-совместимыми серверами), вызов
        повторяется в обычном режиме, а не роняет подзадачу.
        """
        buffer: dict[str, list[str]] = {"text": [], "reasoning": []}
        streamed = False

        def flush(kind: str) -> None:
            if buffer[kind]:
                chunk = "".join(buffer[kind])
                buffer[kind].clear()
                self._emit(EventType.AGENT_DELTA, chunk, step=step, stream=kind)

        def on_delta(piece: str, kind: str = "text") -> None:
            nonlocal streamed
            streamed = True
            kind = kind if kind in buffer else "text"
            buffer[kind].append(piece)
            if sum(map(len, buffer[kind])) >= DELTA_FLUSH_CHARS or "\n" in piece:
                flush(kind)

        options = dict(temperature=self.agent.temperature,
                       max_tokens=self.agent.max_tokens, tools=tools)
        try:
            result = await self.provider.stream_complete(
                self.agent.model, messages, on_delta=on_delta, **options)
        except ProviderError as exc:
            if streamed or exc.status not in STREAM_UNSUPPORTED:
                raise
            log.info("Стриминг не поддержан (%s), повтор обычным запросом", exc)
            result = await self.provider.complete(self.agent.model, messages, **options)
            if result.text:
                on_delta(result.text, "text")
        finally:
            flush("reasoning")
            flush("text")
        return result

    # -- основной цикл -------------------------------------------------------
    async def run(self) -> RunResult:
        """Прогоняет ReAct-цикл до готового результата или до стоп-условия."""
        tool_ctx = self._tool_context()
        specs = self.registry.specs(self.tools_allowed)

        system_prompt = self.agent.system_prompt.strip() or "Ты - полезный ассистент."
        messages: list[ChatMessage] = [ChatMessage("system", system_prompt)]
        messages += self._history()
        briefing = self._briefing()
        messages.append(ChatMessage("user", briefing))
        self.repos.messages.add(self.agent.id, "user", briefing, self.subtask.id)

        totals = RunResult(ok=False)
        last_text = ""
        last_step_used_tools = False

        # Об ошибке подзадачи сообщает оркестратор по ``RunResult.error``:
        # если сообщать и здесь, в ленте и уведомлениях всё удваивается.
        for step in range(1, self.max_steps + 1):
            blocked = await self._check_budget()
            if blocked:
                totals.error = blocked
                return totals

            totals.steps = step
            self._emit(EventType.AGENT_THINKING, f"шаг {step}/{self.max_steps}", step=step)

            try:
                result = await self._call_model(messages, step, specs or None)
            except asyncio.CancelledError:
                raise
            except ProviderError as exc:
                totals.error = f"Провайдер: {exc}"
                return totals
            except Exception as exc:  # noqa: BLE001
                log.exception("Сбой вызова модели")
                totals.error = f"{type(exc).__name__}: {exc}"
                return totals

            self._add_usage(totals, result)
            last_text = result.text or last_text

            # Ответ модели сохраняем в её личную историю.
            if result.text:
                self.repos.messages.add(self.agent.id, "assistant", result.text,
                                        self.subtask.id, tokens=result.usage.output_tokens)

            if not result.tool_calls:
                last_step_used_tools = False
                if looks_done(result.text) or (step == self.max_steps and last_text):
                    # Пустой последний ответ не затирает то, что модель
                    # сказала шагом раньше.
                    return self._finish(totals, result.text or last_text)
                if result.text:
                    # Пустое сообщение ассистента часть провайдеров отвергает.
                    messages.append(ChatMessage("assistant", result.text))
                # Модель не обозначила финал - просим завершить.
                nudge = ("Если подзадача выполнена - выдай итог после строки RESULT: "
                         "и строку CONFIDENCE. Если нет - продолжай работу.")
                messages.append(ChatMessage("user", nudge))
                continue

            # --- есть вызовы инструментов ---
            last_step_used_tools = True
            messages.append(ChatMessage("assistant", result.text,
                                        tool_calls=result.tool_calls))
            for call in result.tool_calls:
                output = await self._invoke_tool(call, tool_ctx, totals)
                messages.append(ChatMessage("tool", output, tool_call_id=call.id,
                                            name=call.name))
                self.repos.messages.add(self.agent.id, "tool", output[:20000],
                                        self.subtask.id, tool_name=call.name,
                                        tool_call_id=call.id)

        if last_step_used_tools:
            # Последний шаг ушёл на инструменты, итога модель не дала. Выдать
            # промежуточное «сейчас посчитаю» за результат нельзя - просим
            # подвести итог одним дополнительным вызовом без инструментов.
            finalized = await self._finalize(messages, totals)
            if finalized is not None:
                return finalized

        totals.ok = bool(last_text)
        totals.result_text = parse_result(last_text)
        totals.confidence = parse_confidence(last_text)
        if not totals.ok:
            totals.error = "Агент не выдал результат за отведённое число шагов"
        return totals

    def _add_usage(self, totals: RunResult, result: CompletionResult) -> None:
        totals.tokens_in += result.usage.input_tokens
        totals.tokens_out += result.usage.output_tokens
        totals.cost_usd += self._account(result)

    def _finish(self, totals: RunResult, text: str) -> RunResult:
        totals.ok = True
        totals.result_text = parse_result(text)
        totals.confidence = parse_confidence(text)
        self._emit(EventType.SUBTASK_PROGRESS, "получен результат")
        return totals

    async def _finalize(self, messages: list[ChatMessage],
                        totals: RunResult) -> RunResult | None:
        """Дополнительный вызов для итога, когда шаги кончились на инструментах."""
        if await self._check_budget():
            return None
        messages.append(ChatMessage("user", FINALIZE_PROMPT))
        step = totals.steps + 1
        self._emit(EventType.AGENT_THINKING, "подведение итога", step=step)
        try:
            result = await self._call_model(messages, step, None)
        except asyncio.CancelledError:
            raise
        except Exception:  # noqa: BLE001 - итог не получился, вернём что было
            log.exception("Не удалось получить итог после исчерпания шагов")
            return None
        self._add_usage(totals, result)
        if not result.text:
            return None
        self.repos.messages.add(self.agent.id, "assistant", result.text,
                                self.subtask.id, tokens=result.usage.output_tokens)
        return self._finish(totals, result.text)

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

*850 строк*

````python
"""Этап 4 - оркестратор выполнения задачи.

Отвечает за расписание: какие подзадачи можно запускать сейчас, какие ждут
предшественников, сколько агентов работают параллельно. Каждый агент
выполняет свои подзадачи последовательно (лок на агента), разные агенты -
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
from core.budget import BudgetGuard, ScopeState
from core.events import Event, EventBus, EventType
from core.hitl import Answer, ApprovalGate, Decision, Reason
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

#: сколько агентов могут работать одновременно, если в настройках не указано
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
        self._semaphore: asyncio.Semaphore | None = None
        self._workspace_id: int | None = None
        #: id подзадач текущей задачи - зависимости на прочие id игнорируются
        self._known_ids: set[int] | None = None

    # -- управление ----------------------------------------------------------
    def pause(self) -> None:
        if self.state.running and not self.state.paused:
            self.state.paused = True
            self._pause.clear()
            self.bus.emit(Event(EventType.RUN_PAUSED, task_id=self.state.task_id,
                                workspace_id=self._workspace_id,
                                message="Выполнение поставлено на паузу"))

    def resume(self) -> None:
        if self.state.running and self.state.paused:
            self.state.paused = False
            self._pause.set()
            self.bus.emit(Event(EventType.RUN_RESUMED, task_id=self.state.task_id,
                                workspace_id=self._workspace_id,
                                message="Выполнение возобновлено"))

    def stop(self) -> None:
        if not self.state.running:
            return
        self._stop.set()
        self._pause.set()                       # разбудить ожидающих
        if self._gate is not None:
            self._gate.cancel_all()             # снять висящие вопросы
        for task in list(self._tasks):
            task.cancel()
        self.bus.emit(Event(EventType.RUN_STOPPED, task_id=self.state.task_id,
                            workspace_id=self._workspace_id,
                            message="Остановка по команде пользователя"))

    # -- основной запуск -----------------------------------------------------
    async def run_task(self, workspace_id: int, task_id: int,
                       concurrency: int | None = None) -> RunState:
        """Прогоняет все подзадачи задачи с учётом зависимостей."""
        if self.state.running:
            raise RuntimeError("Выполнение уже запущено")

        workspace = self.repos.workspaces.get(workspace_id)
        task = self.repos.tasks.get(task_id)
        if workspace is None or task is None:
            raise RuntimeError("Воркспейс или задача не найдены")

        settings = {**DEFAULT_WORKSPACE_SETTINGS, **workspace.settings}
        PATHS.workspace_dir(workspace_id).mkdir(parents=True, exist_ok=True)

        subtasks = [s for s in self.repos.tasks.subtasks(task_id) if s.status != "done"]
        unassigned = [s for s in subtasks if not s.agent_id]
        if unassigned:
            raise RuntimeError(
                "Не у всех подзадач назначен исполнитель: "
                + ", ".join(s.title for s in unassigned[:5])
            )
        if not subtasks:
            raise RuntimeError("Нет подзадач для выполнения")

        if concurrency is None:
            try:
                concurrency = int(settings.get("max_parallel_agents") or DEFAULT_CONCURRENCY)
            except (TypeError, ValueError):
                concurrency = DEFAULT_CONCURRENCY

        self._workspace_id = workspace_id
        self._reset_state(task_id, len(subtasks))
        self._start_gate(workspace_id, settings)
        self._budget = BudgetGuard(self.repos, self.bus, workspace_id,
                                   task.id, task.token_limit)
        if self._gate is not None:
            self._budget.on_blocked = self._on_budget_blocked
        self.repos.tasks.update(task_id, status="running")
        self.bus.emit(Event(EventType.RUN_STARTED, workspace_id=workspace_id,
                            task_id=task_id,
                            message=f"Запуск: {len(subtasks)} подзадач"))

        self._start_supervisor(workspace_id, settings, task)

        self._semaphore = asyncio.Semaphore(max(1, concurrency))
        try:
            await self._schedule(workspace_id, settings, task, subtasks)
            if self._supervisor is not None and not self._stop.is_set():
                # Финальный разбор: ищем расхождения между результатами
                # и подводим общий итог для команды. Сбой здесь не должен
                # перечеркнуть уже сделанную работу.
                try:
                    await self._supervisor.find_conflicts(task)
                    await self._supervisor.make_summary(task, trigger="final")
                except asyncio.CancelledError:
                    raise
                except Exception:  # noqa: BLE001
                    log.exception("Сбой финального разбора супервайзера")
                    self.bus.error("финальный разбор супервайзера не выполнен",
                                   workspace_id=workspace_id, task_id=task_id,
                                   agent_name="Супервайзер")
        except asyncio.CancelledError:
            log.info("Прогон отменён")
        finally:
            await self._cleanup()
            self.state.running = False
            self.repos.tasks.update(task_id, status=self._final_status())
            self.bus.emit(Event(
                EventType.RUN_FINISHED, workspace_id=workspace_id, task_id=task_id,
                message=(f"Готово: {self.state.finished} выполнено, "
                         f"{self.state.failed} с ошибкой, "
                         f"{self.state.reworks} доработок, "
                         f"{self.state.escalated} на решение пользователя, "
                         f"{self.state.tokens} токенов, ~${self.state.cost:.4f}"),
                payload={"finished": self.state.finished, "failed": self.state.failed,
                         "reworks": self.state.reworks,
                         "escalated": self.state.escalated,
                         "stopped": self._stop.is_set()},
            ))
        return self.state

    def _final_status(self) -> str:
        if self._stop.is_set():
            return "stopped"
        if self.state.failed:
            return "failed"
        if self.state.escalated:
            return "review"         # есть результаты, которые ждут человека
        return "done"

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
                        subtasks: list[Subtask]) -> None:
        """Волнами запускает подзадачи, у которых выполнены зависимости."""
        pending = {s.id: s for s in subtasks}
        all_subtasks = self.repos.tasks.subtasks(task.id)
        done_ids: set[int] = {s.id for s in all_subtasks if s.status == "done"}
        titles = {s.id: s.title for s in all_subtasks}
        # Ссылка на подзадачу, которой в задаче больше нет (удалена, осталась
        # от старой версии), не должна навсегда блокировать зависимую.
        self._known_ids = set(titles)

        while pending and not self._stop.is_set():
            ready = [s for s in pending.values() if self._deps_met(s, done_ids)]
            if not ready:
                self._block_unreachable(workspace_id, task, pending, done_ids, titles)
                break

            wave = [
                asyncio.ensure_future(self._run_subtask(workspace_id, settings, task, s))
                for s in ready
            ]
            self._tasks.update(wave)
            results = await asyncio.gather(*wave, return_exceptions=True)
            self._tasks.difference_update(wave)
            for subtask, outcome in zip(ready, results):
                pending.pop(subtask.id, None)
                # CancelledError наследуется от BaseException, а не от Exception,
                # поэтому проверяем именно BaseException - иначе отменённая
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
            # На последней волне вопрос не задаём - спрашивать «продолжать?»,
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

    def _block_unreachable(self, workspace_id: int, task: Task,
                           pending: dict[int, Subtask], done_ids: set[int],
                           titles: dict[int, str]) -> None:
        """Помечает подзадачи, которые уже не смогут стартовать, и объясняет почему.

        Причин две, и путать их нельзя: либо не выполнена одна из
        зависимостей (упала или не принята), либо зависимости замкнуты в
        цикл. Раньше обе выдавались как «невозможно разрешить зависимости»,
        и упавший предшественник выглядел как ошибка в графе.
        """
        for subtask in pending.values():
            missing = [dep for dep in self._deps(subtask) if dep not in done_ids]
            failed_deps = [dep for dep in missing if dep not in pending]
            if failed_deps:
                names = ", ".join(f"«{titles.get(d, d)}»" for d in failed_deps)
                reason = f"не выполнена зависимость {names}"
            else:
                reason = "зависимости замкнуты в цикл"
            self.repos.tasks.update_subtask(subtask.id, status="error")
            self.state.failed += 1
            self.bus.emit(Event(
                EventType.SUBTASK_FAILED, workspace_id=workspace_id, task_id=task.id,
                subtask_id=subtask.id, agent_id=subtask.agent_id,
                message=f"«{subtask.title}» не запущена: {reason}",
            ))

    def _wave_summary(self, task: Task, done_ids: set[int]) -> str:
        """Короткая сводка по завершённой волне - чтобы решать осознанно."""
        lines: list[str] = []
        for subtask in self.repos.tasks.subtasks(task.id):
            if subtask.id not in done_ids:
                continue
            body = (subtask.result or "").strip().replace("\n", " ")
            lines.append(f"· {subtask.title}: {body[:180]}" if body else f"· {subtask.title}")
        tokens, cost = self.repos.budgets.task_totals(task.id)
        lines.append("")
        lines.append(f"Израсходовано по задаче: {tokens} токенов, ~${cost:.4f}")
        return "\n".join(lines)

    def _deps(self, subtask: Subtask) -> list[int]:
        raw = (subtask.depends_on or "").strip()
        deps = [int(t) for t in (tok.strip() for tok in raw.split(",")) if t.isdigit()]
        known = self._known_ids
        return [d for d in deps if known is None or d in known]

    def _deps_met(self, subtask: Subtask, done_ids: set[int]) -> bool:
        return all(dep in done_ids for dep in self._deps(subtask))

    # -- выполнение одной подзадачи -----------------------------------------
    async def _run_subtask(self, workspace_id: int, settings: dict, task: Task,
                           subtask: Subtask) -> bool:
        agent = self.repos.agents.get(subtask.agent_id or 0)
        if agent is None or not agent.enabled:
            self._fail(subtask, agent, "Исполнитель недоступен или отключён")
            return False

        # Сначала лок агента, потом слот параллельности. В обратном порядке
        # подзадачи одного агента занимали бы слоты, простаивая в очереди
        # к собственному локу, и другие агенты ждали бы впустую.
        lock = self._agent_locks.setdefault(agent.id, asyncio.Lock())
        assert self._semaphore is not None
        async with lock, self._semaphore:
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

                # accepted is None → назначена доработка, идём на новый круг.
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

            # Сюда попадаем, когда человек снова вернул работу, а его круги
            # доработки уже исчерпаны. Подзадача не должна остаться висеть
            # «на доработке»: прогон считал бы её не ошибкой, а ничем.
            self._fail(subtask, agent, f"исчерпан лимит доработок по «{subtask.title}»")
            self.repos.agents.set_status(agent.id, "idle")
            return False

    async def _ask_human(self, reason: Reason, question: str, **kwargs) -> Answer:
        """Вопрос человеку изнутри подзадачи.

        Пока человек думает, агент не работает, поэтому его слот
        параллельности отдаётся другим подзадачам и забирается обратно
        после ответа. Лок агента при этом держится: к ответу он вернётся
        со связной историей.
        """
        assert self._gate is not None and self._semaphore is not None
        self._semaphore.release()
        try:
            return await self._gate.ask(reason, question, **kwargs)
        finally:
            await self._semaphore.acquire()

    async def _review_result(self, workspace_id: int, task: Task, subtask: Subtask,
                             agent: Agent, result: RunResult,
                             attempt: int, max_rework: int
                             ) -> tuple[bool | None, str, bool]:
        """Сохраняет результат и проводит его через супервайзера.

        Возвращает ``(итог, замечания, доработку назначил человек)``:
        итог ``True``/``False`` - подзадача закрыта успешно или с ошибкой,
        ``None`` - назначена доработка. Третий флаг говорит вызывающему коду,
        что круг доработки нужно выдать сверх автоматического лимита.
        """
        finished = self._finish_subtask(workspace_id, task, subtask, agent, result)
        if not finished:
            return False, "", False

        supervisor = self._supervisor
        report = self._last_report(subtask.id) if supervisor is not None else None
        if supervisor is None or report is None:
            # Без супервайзера отчёт принимается как есть: пользователь сам
            # отказался от проверки, и в ленте об этом написано при старте.
            self.repos.tasks.update_subtask(subtask.id, status="done")
            self.state.finished += 1
            return True, "", False

        verdict = await supervisor.review(task, subtask, report)

        if verdict.verdict == "unverified":
            return await self._handle_unverified(workspace_id, task, subtask, agent,
                                                 report, verdict)

        if verdict.accepted:
            self.repos.tasks.update_subtask(subtask.id, status="done")
            self.state.finished += 1
            # Замечания по подзадаче закрываем: результат принят, и открытый
            # инцидент без причины висел бы на дашборде как «ждёт решения».
            # Это и замечания, из-за которых работа уходила на доработку, и
            # мелкие пометки, которые супервайзер оставил, принимая отчёт.
            reworked = bool(subtask.rework_count or attempt > 0)
            closed = self.repos.incidents.resolve_for_subtask(
                subtask.id,
                "Исправлено при доработке, результат принят" if reworked
                else "Результат принят супервайзером, замечание некритично",
            )
            if closed and reworked:
                self.bus.log(f"закрыто замечаний после доработки: {closed}",
                             workspace_id=workspace_id, subtask_id=subtask.id,
                             agent_name="Супервайзер")
            # Супервайзер доволен, но сам исполнитель - нет. Это как раз тот
            # случай, когда дешевле спросить человека, чем нести сомнительный
            # результат дальше по цепочке подзадач.
            if (self._gate is not None and report.confidence is not None
                    and report.confidence < self._confidence_threshold):
                self._set_status(agent, subtask, "paused")
                answer = await self._ask_human(
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
                # Пользователь подтвердил результат - возвращаем статусы,
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

        # Доработки исчерпаны либо это конфликт - фиксируем инцидент
        # и, если human-in-the-loop включён, останавливаемся и спрашиваем.
        incident_id = self.repos.incidents.add(
            workspace_id,
            kind="conflict" if verdict.verdict == "conflict" else "contradiction",
            description=(verdict.notes
                         or "Супервайзер не принял результат после доработок"),
            severity=verdict.max_severity,
            task_id=task.id, subtask_id=subtask.id, report_id=report.id,
        )
        reason = (Reason.CONFLICT if verdict.verdict == "conflict"
                  else Reason.NOT_ACCEPTED)
        return await self._escalate(workspace_id, task, subtask, agent, report,
                                    verdict, incident_id, reason)

    async def _handle_unverified(self, workspace_id: int, task: Task, subtask: Subtask,
                                 agent: Agent, report: Report, verdict
                                 ) -> tuple[bool | None, str, bool]:
        """Супервайзер не смог проверить отчёт - решение за человеком."""
        incident_id = self.repos.incidents.add(
            workspace_id, kind="unverified",
            description=verdict.notes or "Результат не прошёл проверку супервайзера",
            severity="medium", task_id=task.id, subtask_id=subtask.id,
            report_id=report.id,
        )
        return await self._escalate(workspace_id, task, subtask, agent, report,
                                    verdict, incident_id, Reason.UNVERIFIED)

    async def _escalate(self, workspace_id: int, task: Task, subtask: Subtask,
                        agent: Agent, report: Report, verdict, incident_id: int,
                        reason: Reason) -> tuple[bool | None, str, bool]:
        """Результат не принят автоматически: спросить человека или отложить.

        Без human-in-the-loop спросить некого, поэтому результат остаётся
        на проверке и НЕ передаётся зависимым подзадачам: строить дальше на
        непринятом результате значит размножить возможную ошибку.
        """
        self.repos.tasks.update_subtask(subtask.id, status="review")
        self.state.escalated += 1
        self.repos.incidents.resolve(incident_id, "escalated",
                                     "Требуется решение пользователя")

        if self._gate is None:
            self.repos.agents.set_status(agent.id, "idle")
            self.bus.emit(Event(
                EventType.APPROVAL_REQUESTED, workspace_id=workspace_id, task_id=task.id,
                subtask_id=subtask.id, agent_id=agent.id, agent_name=agent.name,
                message=f"нужно решение по «{subtask.title}»: {verdict.notes[:150]}",
                payload={"incident_id": incident_id, "verdict": verdict.verdict},
            ))
            await self._maybe_summarize(task)
            return False, "", False

        self._set_status(agent, subtask, "paused")
        answer = await self._ask_human(
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
        elif verdict.notes:
            parts.append("Супервайзер:\n" + verdict.notes[:600])
        parts.append("Результат исполнителя:\n" + (report.content or "")[:1200])
        return "\n\n".join(p for p in parts if p)

    async def _apply_decision(self, workspace_id: int, task: Task, subtask: Subtask,
                              agent: Agent, answer: Answer, incident_id: int | None
                              ) -> tuple[bool | None, str, bool]:
        """Применяет решение пользователя к подзадаче.

        Третий элемент кортежа - признак того, что круг доработки назначил
        человек, а значит его надо выдать сверх автоматического лимита.
        """
        if incident_id is not None:
            self.state.escalated = max(0, self.state.escalated - 1)

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
            return None, answer.comment or "Пользователь вернул работу на доработку.", True

        if answer.decision is Decision.SKIP:
            self.repos.tasks.update_subtask(subtask.id, status="error")
            self.repos.agents.set_status(agent.id, "idle")
            self.state.failed += 1
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
        if incident_id:
            self.repos.incidents.resolve(
                incident_id, "resolved",
                f"Принято пользователем: {answer.comment[:200] or 'без комментария'}"
            )
        await self._maybe_summarize(task)
        return True, "", False

    async def _on_budget_blocked(self, state: ScopeState) -> bool:
        """Лимит исчерпан посреди прогона: спросить, поднимать ли его.

        Возвращает ``True``, если пользователь разрешил продолжить (лимит
        поднимает сам ``BudgetGuard``). Остановка прогона - отдельное
        решение: тогда заблокированные вызовы завершаются ошибкой.
        """
        gate = self._gate
        if gate is None or self._stop.is_set():
            return False
        answer = await gate.ask(
            Reason.BUDGET,
            f"Исчерпан лимит: {state.reason()}. Поднять лимит на 50% и продолжить?",
            details=(f"Уровень: {state.name}\n"
                     f"Текущий лимит: {BudgetGuard.describe_limit(state)}\n"
                     f"Израсходовано: {state.tokens} токенов, ~${state.cost:.4f}"),
            task_id=self.state.task_id, agent_name="Бюджет",
        )
        if answer.decision is Decision.ABORT:
            self.bus.log("Прогон остановлен: лимит бюджета исчерпан",
                         workspace_id=self._workspace_id, task_id=self.state.task_id)
            self._stop.set()
            self._pause.set()
        return answer.decision is Decision.EXTEND

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

        # Отчёт - это то, что увидит супервайзер.
        report_id = self.repos.reports.add_report(
            workspace_id, task.id, subtask.id, agent.id,
            content=result.result_text, confidence=result.confidence,
            tokens_in=result.tokens_in, tokens_out=result.tokens_out,
            cost_usd=result.cost_usd,
        )
        self.repos.agents.set_status(agent.id, "idle")

        confidence = (f", уверенность {result.confidence:.2f}"
                      if result.confidence is not None else "")
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
        """Замечания супервайзера к прошлой версии подзадачи."""
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
        self.bus.emit(Event(EventType.AGENT_STATUS, workspace_id=self._workspace_id,
                            task_id=self.state.task_id, agent_id=agent.id,
                            agent_name=agent.name, subtask_id=subtask.id,
                            message=status, payload={"status": status}))

    def _fail(self, subtask: Subtask, agent: Agent | None, message: str) -> None:
        self.state.failed += 1
        self.repos.tasks.update_subtask(subtask.id, status="error")
        if agent:
            self.repos.agents.set_status(agent.id, "error")
        self.bus.emit(Event(
            EventType.SUBTASK_FAILED, workspace_id=self._workspace_id,
            task_id=self.state.task_id, subtask_id=subtask.id,
            agent_id=agent.id if agent else None,
            agent_name=agent.name if agent else "", message=message,
        ))

    def _start_gate(self, workspace_id: int, settings: dict) -> None:
        """Включает human-in-the-loop, если он разрешён в настройках проекта."""
        if not settings.get("human_in_the_loop", True):
            self._gate = None
            self._confidence_threshold = 0.0
            self.bus.log("Human-in-the-loop выключен - система не будет останавливаться",
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
        """Ворота согласования - интерфейс отдаёт через них решения пользователя."""
        return self._gate

    @property
    def budget(self) -> BudgetGuard | None:
        """Бюджет текущего прогона - для живых индикаторов в интерфейсе."""
        return self._budget

    def _count_supervisor_usage(self, tokens: int, cost: float) -> None:
        self.state.tokens += tokens
        self.state.cost += cost

    def _start_supervisor(self, workspace_id: int, settings: dict, task: Task) -> None:
        """Поднимает супервайзера, если он настроен, и включает сводки по таймеру."""
        self._summary_on_event = bool(settings.get("summary_on_event", True))
        supervisor = Supervisor(self.repos, self.bus, workspace_id, settings,
                                budget=self._budget,
                                on_usage=self._count_supervisor_usage)
        if not supervisor.available():
            self._supervisor = None
            self.bus.log("Супервайзер не настроен - отчёты принимаются без проверки",
                         workspace_id=workspace_id, task_id=task.id)
            return
        self._supervisor = supervisor
        supervisor.start_timer(task)

    async def _cleanup(self) -> None:
        if self._gate is not None:
            self._gate.cancel_all()
            self._gate = None
        # Прогон окончен: агенты, остановленные посреди работы или
        # ожидавшие решения, больше не «работают» и не «на паузе».
        # Статус подзадачи (paused) сохраняется - по нему видно, что
        # её можно продолжить следующим запуском.
        if self._workspace_id is not None:
            for agent in self.repos.agents.list(self._workspace_id):
                if agent.status in ("running", "paused"):
                    self.repos.agents.set_status(agent.id, "idle")
        if self._budget is not None:
            self._budget.on_blocked = None
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

*163 строк*

````python
"""Автоматическое разбиение задачи на подзадачи через ИИ (этап 3).

Планировщик - обычный вызов модели с требованием вернуть строгий JSON.
Модель берётся у агента-супервайзера, а если он не назначен - у первого
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
Ты - планировщик работ. Тебе дают формулировку задачи и список доступных \
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
            "Нет ни одного агента с моделью и ключом - некому планировать. "
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

    # Планирование тоже тратит бюджет, поэтому лимиты проверяются заранее.
    from core.budget import BudgetGuard
    from core.events import EventBus

    task = repos.tasks.current(workspace_id)
    guard = BudgetGuard(repos, EventBus(), workspace_id,
                        task.id if task else None, task.token_limit if task else None)
    blocked = guard.blocking_scope(agent.id)
    if blocked is not None:
        raise RuntimeError(f"Планирование не запущено: лимит исчерпан - {blocked.reason()}")

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

    # Учёт расхода - планирование тоже стоит денег.
    cost = estimate_cost(agent.provider, agent.model,
                         result.usage.input_tokens, result.usage.output_tokens)
    repos.budgets.log_call(workspace_id, task.id if task else None, None, agent.id,
                           agent.provider,
                           agent.model, result.usage.input_tokens,
                           result.usage.output_tokens, cost)

    try:
        data = _extract_json(result.text)
    except ValueError as exc:
        log.warning("Планировщик вернул не-JSON: %s", result.text[:400])
        raise RuntimeError("Модель вернула ответ не в формате JSON. "
                           "Попробуйте ещё раз или выберите другую модель.") from exc

    # Некоторые модели отвечают голым списком вместо объекта - принимаем и так.
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and isinstance(data.get("subtasks"), list):
        items = data["subtasks"]
    else:
        items = []
    out: list[PlannedSubtask] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title", "")).strip()
        if not title:
            continue
        out.append(PlannedSubtask(
            title=title,
            description=str(item.get("description", "")).strip(),
            assignee_role=(str(item.get("assignee_role") or "").strip() or None),
        ))
    if not out:
        raise RuntimeError("Модель не вернула ни одной подзадачи.")
    return out


def match_agent_by_role(repos: Repos, workspace_id: int, role: str | None) -> int | None:
    """Подбирает агента под предложенную планировщиком роль."""
    wanted = str(role or "").strip().lower()
    if not wanted:
        return None
    # Модель пишет роль как вздумается: «Analyst», « analyst».
    for a in repos.agents.list(workspace_id):
        if a.enabled and not a.is_supervisor and (a.role or "").strip().lower() == wanted:
            return a.id
    return None
````

### `core/supervisor/checklist.py`

*316 строк*

````python
"""Этап 5 - промпты супервайзера и разбор его ответов.

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
Ты - супервайзер команды исполнителей. Ты не переписываешь работу за них:
ты выносишь вердикт и формулируешь, что именно нужно исправить.

Проверь отчёт строго по чек-листу:
1. СООТВЕТСТВИЕ ЗАДАНИЮ - отчёт отвечает именно на поставленную подзадачу,
   ничего из требуемого не пропущено, лишнего не добавлено.
2. ЛОГИЧЕСКАЯ НЕПРОТИВОРЕЧИВОСТЬ - выводы следуют из приведённых данных,
   внутри отчёта нет взаимоисключающих утверждений.
3. ФАКТИЧЕСКИЕ ОШИБКИ - проверяемые утверждения верны, нет выдуманных
   источников, цифр, API, цитат и ссылок.
4. СОГЛАСОВАННОСТЬ С ПРОЕКТОМ - отчёт не противоречит ранее принятым
   результатам других подзадач.

Будь требователен, но конкретен: замечание без указания, что именно исправить,
бесполезно. Не придирайся к стилю и оформлению, если суть верна.

Вердикты:
- "ok"       - работа принимается;
- "rework"   - есть исправимые недостатки, нужна доработка;
- "conflict" - отчёт противоречит другим результатам проекта, нужен разбор.

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
Ты - супервайзер проекта. Составь краткую сводку хода работ для всех
исполнителей.

Жёсткие требования:
- пиши СВОИМИ СЛОВАМИ, не копируй формулировки из отчётов;
- НЕ указывай, кто что сделал: ни имён, ни ролей, ни «первый исполнитель»;
- отделяй проверенные факты от предположений;
- отдельно перечисли расхождения между результатами, если они есть;
- отдельно перечисли открытые вопросы, которые мешают двигаться дальше;
- не более 250 слов, без вступлений и заключений.

Формат ответа - обычный текст с тремя разделами:
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
Ты - супервайзер. Сравни результаты разных подзадач одного проекта и найди
ПРЯМЫЕ противоречия: взаимоисключающие утверждения, несовпадающие числа,
разные ответы на один и тот же вопрос.

Не считай противоречием: разный уровень детализации, разный ракурс на одну
тему, дополняющие друг друга сведения.

Для каждого противоречия оцени, можно ли решить его автоматически - то есть
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
Если противоречий нет - верни {"conflicts": []}.
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

    # Ответ без вердикта (пустой объект, список вместо объекта) - это не
    # «принято»: по той же логике, что и нечитаемый ответ, отправляем на
    # доработку, а не пропускаем непроверенным.
    verdict = str(data.get("verdict") or "").lower().strip()
    if verdict not in _VALID_VERDICTS:
        if not data.get("notes"):
            data = {**data, "notes": "Супервайзер не вынес вердикт. "
                                     "Переформулируй отчёт короче и по пунктам."}
        verdict = "rework"

    issues: list[Issue] = []
    raw_issues = data.get("issues")
    for item in raw_issues if isinstance(raw_issues, list) else []:
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
    raw_conflicts = data.get("conflicts")
    for item in raw_conflicts if isinstance(raw_conflicts, list) else []:
        if not isinstance(item, dict):
            continue
        description = str(item.get("description", "")).strip()
        if not description:
            continue
        severity = str(item.get("severity", "medium")).lower()
        out.append(Conflict(
            description=description,
            severity=severity if severity in _VALID_SEVERITY else "medium",
            labels=[str(x) for x in item["labels"]] if isinstance(item.get("labels"), list) else [],
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
        """Вычищает имена агентов из готового текста - страховка на случай,
        если модель всё-таки назвала кого-то по имени."""
        result = text or ""
        # Длинные имена первыми: «Аналитик Пётр» не должно превратиться в
        # «Исполнитель A Пётр» из-за того, что сначала заменили «Аналитик».
        for agent_id, name in sorted(names.items(), key=lambda kv: -len(kv[1] or "")):
            if name and len(name) > 2:
                # Только целые слова: имя «Ан» не должно резать «Анализ».
                pattern = rf"(?<!\w){re.escape(name)}(?!\w)"
                result = re.sub(pattern, self.label(agent_id), result, flags=re.IGNORECASE)
        return result
````

### `core/supervisor/supervisor.py`

*399 строк*

````python
"""Этап 5 - служба супервайзера.

Обязанности:
* проверять отчёты агентов по чек-листу и выносить вердикт;
* возвращать работу на доработку (не более ``max_rework_rounds`` раз);
* составлять анонимные сводки и рассылать их всем агентам;
* находить противоречия между результатами и заводить инциденты;
* эскалировать пользователю то, что не разрешается автоматически.

Модель супервайзера выбирается в настройках воркспейса: либо один из
подключённых агентов со своим API-ключом, либо локальная модель через
OpenAI-совместимый endpoint (Ollama, по умолчанию Qwen) - она работает
офлайн и ничего не стоит.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Callable

from core.budget import BudgetBlocked, BudgetGuard
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
from providers.base import ChatMessage, LLMProvider
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
                 settings: dict, budget: BudgetGuard | None = None,
                 on_usage: Callable[[int, float], None] | None = None) -> None:
        self.repos = repos
        self.bus = bus
        self.workspace_id = workspace_id
        self.settings = settings
        #: лимиты прогона: проверки супервайзера - самая дорогая часть
        #: системы, поэтому они обязаны проходить через тот же бюджет
        self.budget = budget
        self.on_usage = on_usage
        self.anonymize = bool(settings.get("anonymize_summaries", True))
        self.anon = Anonymizer()
        self._names = {a.id: a.name for a in repos.agents.list(workspace_id)}
        self._model: SupervisorModel | None = None
        self._summary_task: asyncio.Task | None = None
        self._stop = asyncio.Event()
        #: текст последней ошибки сводки - чтобы интерфейс не выдавал её за
        #: «нечего пересказывать»
        self.last_error = ""
        #: задача текущего прогона - для привязки событий к нему
        self._task_id: int | None = None

    def _label(self, agent_id: int | None) -> str:
        """Как подписать автора: анонимной меткой или по имени (если выключено)."""
        if not self.anonymize and agent_id in self._names:
            return self._names[agent_id]
        return self.anon.label(agent_id)

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
        try:
            agent = self.repos.agents.get(int(agent_id)) if agent_id else None
        except (TypeError, ValueError):
            agent = None
        if agent is not None and agent.workspace_id != self.workspace_id:
            agent = None        # агент из другого воркспейса здесь не судья
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
        if self.budget is not None:
            blocked = await self.budget.ensure_allowed(None)
            if blocked is not None:
                raise BudgetBlocked(f"лимит исчерпан - {blocked.reason()}")
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
        if self.budget is not None:
            self.budget.add(result.usage.total, cost, None)
        if self.on_usage is not None:
            self.on_usage(result.usage.total, cost)
        self.bus.emit(Event(
            EventType.USAGE, workspace_id=self.workspace_id, task_id=task_id,
            agent_name="Супервайзер",
            message=f"+{result.usage.total} токенов (~${cost:.4f})",
            payload={"tokens": result.usage.total, "cost": cost, "supervisor": True},
        ))
        return result.text

    def _emit(self, kind: EventType, message: str, **payload) -> None:
        self.bus.emit(Event(kind, workspace_id=self.workspace_id, task_id=self._task_id,
                            subtask_id=payload.get("subtask_id"),
                            agent_name="Супервайзер", message=message,
                            payload=payload))

    # -- проверка отчёта -----------------------------------------------------
    async def review(self, task: Task, subtask: Subtask, report: Report) -> Verdict:
        """Проверяет отчёт по чек-листу и возвращает вердикт.

        Если проверить не удалось (сеть, лимит, модель не настроена),
        вердикт - ``unverified``: такой результат не считается принятым и
        не уходит дальше по конвейеру, пока его не посмотрит человек.
        """
        self._task_id = task.id
        label = self._label(report.agent_id)
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
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 - любая причина равна «не проверено»
            log.warning("Супервайзер не смог проверить отчёт: %s", exc)
            # Раньше непроверенный отчёт молча принимался. Это опаснее, чем
            # остановиться: ошибка ушла бы в зависимые подзадачи без следа.
            self._emit(EventType.ERROR, f"проверка не выполнена: {exc}")
            notes = f"Проверка не выполнена: {exc}"
            self.repos.reports.mark_reviewed(report.id, "unverified", notes)
            return Verdict(verdict="unverified", notes=notes)

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
            # Только принятое: статус review - это отчёт, который ещё
            # проверяется или ждёт человека, мерить им другие рано.
            if st.status != "done":
                continue
            chunks.append(f"[{self._label(st.agent_id)}] {st.title}:\n"
                          f"{st.result[:1200]}")
        return "\n\n".join(chunks[-CONTEXT_REPORTS:])

    # -- сводки --------------------------------------------------------------
    async def make_summary(self, task: Task, trigger: str = "manual") -> str:
        """Составляет анонимную сводку и «рассылает» её всем агентам.

        Рассылка означает запись в таблицу ``summaries``: каждый агент
        подхватывает последнюю сводку при следующем запуске, не зная,
        кто из коллег что написал.
        """
        self._task_id = task.id
        self.last_error = ""
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
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 - сводка не повод ронять прогон
            self._emit(EventType.ERROR, f"сводка не составлена: {exc}")
            self.last_error = str(exc)
            return ""

        # Страховка: вычищаем имена агентов, если модель их всё-таки назвала.
        names = {a.id: a.name for a in self.repos.agents.list(self.workspace_id)}
        content = self.anon.scrub(raw.strip(), names) if self.anonymize else raw.strip()
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
            # У упавшей подзадачи в поле результата текст ошибки, а не работа.
            if not st.result or st.status == "error":
                continue
            chunks.append(f"[{self._label(st.agent_id)}] {st.title}:\n"
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
        готовом результате вызов модели пропускается - это экономит токены,
        а не срезает проверку.
        """
        self._task_id = task.id
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
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001
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

*225 строк*

````python
"""Этап 7 - human-in-the-loop: реальная пауза в критических точках.

Ядро не спрашивает пользователя напрямую - оно публикует запрос в шину и
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
    EXTEND = "extend"      # поднять исчерпанный лимит бюджета и продолжить


class Reason(str, Enum):
    """Почему система остановилась."""

    CONFLICT = "conflict"              # супервайзер нашёл противоречие
    NOT_ACCEPTED = "not_accepted"      # доработки исчерпаны, результат не принят
    LOW_CONFIDENCE = "low_confidence"  # агент сам не уверен в результате
    MILESTONE = "milestone"            # завершён этап работ
    UNVERIFIED = "unverified"          # супервайзер не смог проверить результат
    BUDGET = "budget"                  # исчерпан лимит бюджета


REASON_TITLES = {
    Reason.CONFLICT: "Конфликт данных",
    Reason.NOT_ACCEPTED: "Результат не принят супервайзером",
    Reason.LOW_CONFIDENCE: "Низкая уверенность исполнителя",
    Reason.MILESTONE: "Завершён этап работ",
    Reason.UNVERIFIED: "Результат не проверен",
    Reason.BUDGET: "Исчерпан лимит бюджета",
}

#: какие кнопки показывать для каждой причины
REASON_OPTIONS: dict[Reason, list[Decision]] = {
    Reason.CONFLICT: [Decision.APPROVE, Decision.REWORK, Decision.SKIP, Decision.ABORT],
    Reason.NOT_ACCEPTED: [Decision.APPROVE, Decision.REWORK, Decision.SKIP, Decision.ABORT],
    Reason.LOW_CONFIDENCE: [Decision.APPROVE, Decision.REWORK, Decision.ABORT],
    Reason.MILESTONE: [Decision.APPROVE, Decision.ABORT],
    Reason.UNVERIFIED: [Decision.APPROVE, Decision.REWORK, Decision.SKIP, Decision.ABORT],
    Reason.BUDGET: [Decision.EXTEND, Decision.SKIP, Decision.ABORT],
}

DECISION_TITLES = {
    Decision.APPROVE: "Принять",
    Decision.REWORK: "На доработку",
    Decision.SKIP: "Пропустить",
    Decision.ABORT: "Остановить прогон",
    Decision.EXTEND: "Увеличить лимит на 50%",
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

        Если прогон уже остановлен, вопрос не задаётся - возвращается
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
                    + (f" - {answer.comment[:120]}" if answer.comment else ""),
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
                # Неизвестное решение не превращаем молча в «Принять»:
                # это ровно та ошибка, ради которой человека и спрашивают.
                return False
        request = self._open.get(approval_id)
        if request is not None and request.options and decision not in request.options:
            return False
        future.set_result(Answer(decision, (comment or "").strip()))
        return True

    def cancel_all(self) -> None:
        """Снимает все ожидания - нужно при остановке прогона."""
        self._aborted = True
        for approval_id, future in list(self._waiters.items()):
            if not future.done():
                future.set_result(Answer(Decision.ABORT, "Прогон остановлен"))
            self._waiters.pop(approval_id, None)
        self._open.clear()

    def pending(self) -> list[ApprovalRequest]:
        """Список открытых вопросов - интерфейс рисует их карточками."""
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

*362 строк*

````python
"""Этап 9 - бюджеты, лимиты и алерты.

Лимит можно поставить на трёх уровнях: весь воркспейс, текущая задача и
отдельный агент. Каждый уровень ограничивается и по токенам, и по деньгам.

Две важные детали реализации:

* Проверка идёт **перед** вызовом модели, а не после. Иначе лимит узнавался бы
  постфактум - деньги уже потрачены, а сказать об этом нечем.
* Фактический расход берётся из ``usage_log``, а не из накопительных счётчиков
  в таблице ``budgets``. Журнал вызовов - единственный источник правды, и при
  перезапуске приложения лимит не «обнуляется» сам собой.
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Awaitable, Callable

from core.events import Event, EventBus, EventType
from storage.repositories import Repos

log = logging.getLogger("aiorc.budget")

#: во сколько раз поднимается лимит по решению пользователя
EXTEND_FACTOR = 1.5


class BudgetBlocked(RuntimeError):
    """Вызов модели не выполнен: исчерпан лимит бюджета."""

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
    exceeded_reported: bool = False

    def ratio(self) -> float:
        """Доля израсходованного - максимум из токенов и денег."""
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
        #: лимит на уровне задачи взят из формы задачи, а не из таблицы budgets
        self._task_limit_from_form = False
        #: кто решает, что делать при исчерпании лимита; ``None`` - блокировать
        self.on_blocked: Callable[[ScopeState], Awaitable[bool]] | None = None
        #: один вопрос на уровень: параллельные агенты ждут общего ответа
        self._pending: dict[tuple[str, int], asyncio.Future] = {}
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
                self._task_limit_from_form = self.repos.budgets.get(
                    "task", self.task_id) is None
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

    def reload_limits(self) -> None:
        """Перечитывает лимиты из базы, сохраняя накопленный расход.

        Нужно, когда пользователь правит лимиты на странице бюджетов прямо
        во время прогона: иначе новое значение вступило бы в силу только со
        следующим запуском, а до тех пор агенты работали бы по старому.
        """
        for (scope, scope_id), state in self._scopes.items():
            limit = self._limit_of(scope, scope_id)
            if scope == "task" and limit.token_limit is None:
                task = self.repos.tasks.get(scope_id)
                if task is not None and task.token_limit:
                    limit.token_limit = task.token_limit
                    self._task_limit_from_form = self.repos.budgets.get(
                        "task", scope_id) is None
            state.limit = limit
            if not state.exceeded():
                state.exceeded_reported = False
            if state.ratio() < limit.alert_threshold:
                state.alerted = False

    def _limit_of(self, scope: str, scope_id: int) -> Limit:
        row = self.repos.budgets.get(scope, scope_id)
        if row is None:
            return Limit()
        return Limit(row.token_limit, row.cost_limit_usd, row.alert_threshold)

    # -- проверка ------------------------------------------------------------
    def blocking_scope(self, agent_id: int | None = None) -> ScopeState | None:
        """Возвращает уровень, лимит которого исчерпан, или ``None``.

        Проверка идёт от общего к частному: сначала воркспейс, потом задача,
        потом конкретный агент - так сообщение получается по самой
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

    async def ensure_allowed(self, agent_id: int | None = None) -> ScopeState | None:
        """Проверка перед вызовом модели с возможностью продлить лимит.

        Возвращает ``None``, если вызов разрешён, иначе уровень, который
        его блокирует. Когда назначен ``on_blocked`` (включён
        human-in-the-loop), исчерпанный лимит не обрывает работу сразу:
        пользователя спрашивают, поднять ли лимит. Параллельные агенты,
        упёршиеся в тот же уровень, ждут одного общего ответа, а не
        заваливают человека одинаковыми вопросами.
        """
        while True:
            blocked = self.blocking_scope(agent_id)
            if blocked is None or self.on_blocked is None:
                return blocked
            key = (blocked.scope, blocked.scope_id)
            future = self._pending.get(key)
            if future is None:
                future = asyncio.ensure_future(self._ask_extension(blocked))
                self._pending[key] = future
                future.add_done_callback(lambda _f, k=key: self._pending.pop(k, None))
            if not await asyncio.shield(future):
                return blocked
            # лимит поднят - проверяем все уровни заново: мог упереться другой

    async def _ask_extension(self, state: ScopeState) -> bool:
        assert self.on_blocked is not None
        if not await self.on_blocked(state):
            return False
        self.extend(state)
        return True

    def extend(self, state: ScopeState, factor: float = EXTEND_FACTOR) -> None:
        """Поднимает исчерпанный лимит и сохраняет новое значение."""
        limit = state.limit
        if limit.token_limit:
            limit.token_limit = int(max(limit.token_limit, state.tokens) * factor)
        if limit.cost_limit:
            limit.cost_limit = round(max(limit.cost_limit, state.cost) * factor, 6)
        state.alerted = False
        if state.scope == "task" and self._task_limit_from_form:
            # Лимит задан в форме задачи - там его и обновляем.
            self.repos.tasks.update(state.scope_id, token_limit=limit.token_limit)
        else:
            self.repos.budgets.upsert(state.scope, state.scope_id, limit.token_limit,
                                      limit.cost_limit, limit.alert_threshold)
            self.repos.budgets.sync_used(state.scope, state.scope_id,
                                         state.tokens, state.cost)
        self.bus.emit(Event(
            EventType.BUDGET_EXTENDED, workspace_id=self.workspace_id,
            task_id=self.task_id,
            message=(f"лимит поднят: {SCOPE_TITLES.get(state.scope, state.scope)} "
                     f"«{state.name}» - {self.describe_limit(state)}"),
            payload={"scope": state.scope, "scope_id": state.scope_id},
        ))

    @staticmethod
    def describe_limit(state: ScopeState) -> str:
        parts = []
        if state.limit.token_limit:
            parts.append(f"{state.limit.token_limit} токенов")
        if state.limit.cost_limit:
            parts.append(money(state.limit.cost_limit))
        return ", ".join(parts) or "без лимита"

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
        """Каждый алерт срабатывает один раз на уровень - иначе это шум.

        «Подходим к порогу» и «лимит исчерпан» - разные события, поэтому у
        них отдельные флаги: предупреждение о пороге не должно глушить
        сообщение о превышении, и наоборот.
        """
        if state.exceeded():
            if state.exceeded_reported:
                return
            state.exceeded_reported = True
            state.alerted = True
            self.bus.emit(Event(
                EventType.BUDGET_EXCEEDED, workspace_id=self.workspace_id,
                task_id=self.task_id,
                message=f"лимит исчерпан - {state.reason()}",
                payload={"scope": state.scope, "scope_id": state.scope_id,
                         "ratio": state.ratio()},
            ))
            return

        state.exceeded_reported = False     # после продления лимита снова следим
        if not state.alerted and state.ratio() >= state.limit.alert_threshold:
            state.alerted = True
            percent = state.ratio() * 100
            self.bus.emit(Event(
                EventType.BUDGET_ALERT, workspace_id=self.workspace_id,
                task_id=self.task_id,
                message=(f"бюджет на {percent:.0f}% - "
                         f"{SCOPE_TITLES.get(state.scope, state.scope)} "
                         f"«{state.name}»"),
                payload={"scope": state.scope, "scope_id": state.scope_id,
                         "ratio": state.ratio()},
            ))

    # -- отчётность ----------------------------------------------------------
    def snapshot(self) -> list[ScopeState]:
        """Состояние всех уровней - для дашборда и страницы бюджетов."""
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
    """Состояние бюджетов вне прогона - для страницы настройки лимитов."""
    task = repos.tasks.current(workspace_id)
    guard = BudgetGuard(repos, EventBus(), workspace_id,
                        task.id if task else None,
                        task.token_limit if task else None)
    return guard.snapshot()
````


## Экспорт результата

### `core/export/bundle.py`

*394 строк*

````python
"""Этап 8 - сборка результата проекта.

Формат результата зависит от задачи, поэтому экспорт устроен в два слоя:

1. Из базы и рабочего каталога собирается ``ResultBundle`` - всё, что
   наработал проект.
2. Из него строится **единая модель документа** (список блоков), и уже её
   рендерят четыре формата. Благодаря этому Markdown, DOCX и PDF получаются
   одинаковыми по содержанию: правится один сборщик, а не три экспортёра.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

from app.config import PATHS
from core.hitl import parse_payload
from storage.db import local_time
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
    """Что включать в выгрузку. Значения по умолчанию - «полезное без шума»."""

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
            if agent_id not in ordered:
                # Удалённый агент не должен получить чужую метку «A».
                return "Исполнитель ?"
            index = ordered.index(agent_id)
            suffix = chr(ord("A") + index) if index < 26 else str(index + 1)
            return f"Исполнитель {suffix}"
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
    # В воркспейсе может быть несколько задач подряд: в документ идёт только
    # текущая, иначе отчёты и расход прошлых задач смешались бы с новыми.
    tokens, cost = (repos.budgets.task_totals(task.id) if task
                    else repos.budgets.workspace_totals(workspace_id))

    def of_task(items):
        return [i for i in items if task is None or i.task_id in (task.id, None)]

    decisions = [row for row in repos.approvals.history(workspace_id, limit=200)
                 if task is None or row.get("task_id") in (task.id, None)]

    bundle = ResultBundle(
        workspace=workspace,
        task=task,
        subtasks=subtasks,
        reports=of_task(repos.reports.list_reports(workspace_id, limit=500)),
        summaries=of_task(repos.reports.list_summaries(workspace_id, limit=100)),
        incidents=of_task(repos.incidents.list(workspace_id, limit=500)),
        decisions=decisions,
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
        return "zip", (f"В рабочем каталоге {len(bundle.files)} файлов - "
                       f"архив удобнее одного документа.")

    haystack = " ".join(filter(None, [
        bundle.task.title if bundle.task else "",
        bundle.task.description if bundle.task else "",
    ])).lower()

    # Совпадение с начала слова: иначе «api» находится в «capital», а «код»
    # в «эпизоде», и задача про историю уходит в ZIP как «код».
    def mentions(words: tuple[str, ...]) -> bool:
        return any(re.search(rf"(?<!\w){re.escape(w)}", haystack) for w in words)

    if mentions(CODE_HINTS):
        return "zip", "Формулировка задачи говорит о коде - собираем архив."
    if mentions(DOC_HINTS):
        return "docx", "Формулировка задачи говорит о документе."

    total = sum(len(s.result) for s in bundle.subtasks)
    if total > 20_000:
        return "docx", "Результат объёмный - документ Word удобнее читать."
    return "markdown", "Результат текстовый и компактный - подойдёт Markdown."


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
            comment = f" - {row['comment']}" if row.get("comment") else ""
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
    не испортить, - ограждённые блоки кода.
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
    # В базе время в UTC; в документе - местное, как и «Сформировано».
    return local_time(raw, "%d.%m.%Y %H:%M") if raw else ""


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

*408 строк*

````python
"""Рендеринг результата в конкретные форматы (этап 8).

Все экспортёры получают одну и ту же модель блоков из ``bundle.py``,
поэтому содержание Markdown, DOCX и PDF совпадает по построению.

Отдельная история - кириллица в PDF: встроенные шрифты reportlab её не
знают, поэтому приходится искать в системе TrueType-шрифт. Если не нашли,
экспорт не молчит и не выдаёт кракозябры, а честно говорит об этом.
"""

from __future__ import annotations

import json
import logging
import re
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

    blocks = [_clean_block(b) for b in build_document(bundle, options)]
    document = Document()

    # Моноширинный стиль для кода - в стандартном шаблоне его нет.
    styles = document.styles
    try:
        code_style = styles.add_style("AiorcCode", WD_STYLE_TYPE.PARAGRAPH)
        code_style.font.name = "Consolas"
        code_style.font.size = Pt(9)
    except Exception:  # noqa: BLE001 - стиль уже есть
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
    """Ищет шрифт в системе, а если не нашёл - в пакете matplotlib.

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
            "её не знают - текст получился бы нечитаемым.\n\n"
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
    for block in (_clean_block(b) for b in build_document(bundle, options)):
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


#: управляющие символы, недопустимые в XML (DOCX их не принимает вовсе):
#: всё ниже пробела, кроме табуляции и переводов строки
_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
#: ANSI-последовательности цвета из вывода терминала: «\x1b[31m»
_ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


def _clean(text: str) -> str:
    """Убирает то, что сломало бы DOCX/PDF: цвета терминала и управляющие символы.

    Агенты вставляют в результат вывод программ как есть, а python-docx
    на первом же таком символе бросает исключение и экспорт целиком падает.
    """
    return _CONTROL.sub("", _ANSI.sub("", text or ""))


def _clean_block(block: Block) -> Block:
    return Block(block.kind, text=_clean(block.text), level=block.level,
                 items=[_clean(i) for i in block.items], language=block.language)


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
            else "Файлов в рабочем каталоге не было - в архиве только отчёт.")
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


## Интерфейс: мост Python и QML

### `ui/app.py`

*152 строк*

````python
"""Запуск интерфейса на Qt Quick.

Порядок: приложение Qt → шрифты → мост (Backend, I18n) → QML-движок →
главное окно → общий цикл asyncio (qasync).
"""

from __future__ import annotations

import ctypes
import logging
import sys
from pathlib import Path

from PySide6.QtCore import QtMsgType, qInstallMessageHandler
from PySide6.QtGui import QFontDatabase, QGuiApplication, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuickControls2 import QQuickStyle

from app.config import AppSettings
from storage.db import Database

log = logging.getLogger("aiorc.qml")

UI_DIR = Path(__file__).resolve().parent
QML_DIR = UI_DIR / "qml"
FONTS_DIR = UI_DIR / "assets" / "fonts"

#: сообщения QML, собранные за сессию (смоук-тест интерфейса проверяет,
#: что среди них нет ошибок)
QML_MESSAGES: list[tuple[str, str]] = []


def _qt_message(mode: QtMsgType, context, message: str) -> None:
    level = {QtMsgType.QtWarningMsg: "warning", QtMsgType.QtCriticalMsg: "error",
             QtMsgType.QtFatalMsg: "error"}.get(mode, "info")
    if "Cannot find font directory" in message:
        level = "info"    # платформа без системных шрифтов; свои шрифты мы приносим сами
    QML_MESSAGES.append((level, message))
    if level == "info":
        log.debug(message)
    else:
        log.warning("Qt: %s", message)


def ensure_qt_dll_path() -> None:
    """Помогает Windows найти DLL Qt для QML-плагинов.

    Плагины (например, стиль Basic для Qt Quick Controls) лежат в подкаталогах
    PySide6 и зависят от DLL в его корне. В части окружений (venv, запуск не
    из консоли Python) Windows их не находит, и загрузка QML падает с
    «Не найден указанный модуль». Явное добавление каталога это лечит.
    """
    if sys.platform != "win32":
        return
    import os

    import PySide6

    qt_dir = os.path.dirname(PySide6.__file__)
    try:
        os.add_dll_directory(qt_dir)
    except (OSError, AttributeError):
        pass
    if qt_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = qt_dir + os.pathsep + os.environ.get("PATH", "")


def load_fonts() -> dict[str, str]:
    """Регистрирует шрифты из комплекта и возвращает имена семейств для QML."""
    families = {"sans": "Segoe UI", "mono": "Consolas", "icons": "lucide"}
    found: dict[str, str] = {}
    for path in sorted(FONTS_DIR.glob("*.ttf")):
        font_id = QFontDatabase.addApplicationFont(str(path))
        names = QFontDatabase.applicationFontFamilies(font_id) if font_id >= 0 else []
        if not names:
            log.warning("Не удалось загрузить шрифт %s", path.name)
            continue
        if path.name.startswith("Inter"):
            found["sans"] = names[0]
        elif path.name.startswith("JetBrains"):
            found["mono"] = names[0]
        elif path.name.startswith("lucide"):
            found["icons"] = names[0]
    families.update(found)
    return families


def apply_dark_titlebar(window) -> None:
    """Тёмный системный заголовок окна на Windows 10/11, в цвет фона приложения."""
    if sys.platform != "win32" or window is None:
        return
    try:
        hwnd = int(window.winId())
        dwm = ctypes.windll.dwmapi
        value = ctypes.c_int(1)
        # DWMWA_USE_IMMERSIVE_DARK_MODE: 20 (новые сборки) и 19 (старые)
        for attr in (20, 19):
            if dwm.DwmSetWindowAttribute(hwnd, attr, ctypes.byref(value), ctypes.sizeof(value)) == 0:
                break
        # DWMWA_CAPTION_COLOR (Windows 11): цвет заголовка = цвет фона (BGR)
        caption = ctypes.c_int(0x0F0809)
        dwm.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(caption), ctypes.sizeof(caption))
    except Exception:  # noqa: BLE001 - косметика, не повод падать
        log.debug("Тёмный заголовок окна недоступен", exc_info=True)


class UiApp:
    """Собранное приложение: держит ссылки, чтобы их не собрал сборщик мусора."""

    def __init__(self, settings: AppSettings, db: Database | None = None) -> None:
        from ui.bridge.backend import Backend
        from ui.bridge.i18n_bridge import I18n

        ensure_qt_dll_path()
        qInstallMessageHandler(_qt_message)
        QQuickStyle.setStyle("Basic")
        self.app = QGuiApplication.instance()
        assert self.app is not None, "QApplication должно быть создано до UiApp"
        icon = UI_DIR / "assets" / "icon.png"
        if icon.exists():
            self.app.setWindowIcon(QIcon(str(icon)))

        self.fonts = load_fonts()
        self.backend = Backend(db or Database(), settings)
        self.i18n = I18n()
        self.engine = QQmlApplicationEngine()
        self.engine.addImportPath(str(QML_DIR))
        ctx = self.engine.rootContext()
        ctx.setContextProperty("backend", self.backend)
        ctx.setContextProperty("i18n", self.i18n)
        ctx.setContextProperty("fonts", self.fonts)
        self.engine.load(str(QML_DIR / "Main.qml"))
        if not self.engine.rootObjects():
            raise RuntimeError("Не удалось загрузить интерфейс (Main.qml). Подробности в логе.")
        self.window = self.engine.rootObjects()[0]
        apply_dark_titlebar(self.window)

    def dispose(self) -> None:
        """Порядок важен: сначала гасим агентов и QML, потом мост.

        Если мост уничтожить раньше движка, биндинги QML успевают обратиться
        к уже удалённым объектам и засыпают лог ошибками «of null».

        Вызывается явно после выхода из цикла событий, а не по
        ``aboutToQuit``: qasync выходит из цикла Qt и в служебных случаях
        (``run_until_complete``), и окно пропадало бы посреди работы.
        """
        self.backend.shutdown()
        # Движок принадлежит Python: снятие ссылки удаляет его сразу, вместе
        # с деревом QML, пока мост ещё жив.
        self.window = None
        self.engine = None
````

### `ui/bridge/core.py`

*158 строк*

````python
"""Общие кирпичики моста: объект состояния, контроллер страницы, форматтеры."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.i18n import tr
from storage.db import local_time

if TYPE_CHECKING:  # pragma: no cover
    from core.events import Event
    from storage.repositories import Repos
    from ui.bridge.backend import Backend


class StateObject(QObject):
    """QObject, у которого все свойства лежат в одном словаре.

    Одного сигнала ``changed`` хватает всем свойствам: QML перечитывает
    только те биндинги, что зависят от объекта, а объектов немного. Это
    избавляет от десятков однотипных сигналов и сеттеров.

    Важно: сигнал ``changed = Signal()`` объявляет КАЖДЫЙ конечный класс, а
    не этот базовый. PySide6 связывает ``notify`` свойства только с сигналом
    того же класса; с унаследованным сигналом свойство становится
    «неуведомляемым», и биндинги QML перестают обновляться.
    """

    changed: Signal  # объявляется в подклассе

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._s: dict[str, Any] = {}

    def _set(self, **values: Any) -> None:
        dirty = False
        for name, value in values.items():
            if self._s.get(name, _MISSING) != value:
                self._s[name] = value
                dirty = True
        if dirty:
            self.changed.emit()


_MISSING = object()


def sprop(type_: Any, name: str, default: Any, signal: Signal) -> Property:
    """Свойство, читающее ``self._s[name]`` и уведомляющее сигналом класса."""

    def getter(self: StateObject) -> Any:
        return self._s.get(name, default)

    return Property(type_, getter, notify=signal)


class Controller(StateObject):
    """Контроллер одной страницы: данные для QML и действия пользователя."""

    def __init__(self, backend: "Backend") -> None:
        super().__init__(backend)
        self.backend = backend

    @property
    def repos(self) -> "Repos":
        assert self.backend.repos is not None, "контроллер вызван до входа в профиль"
        return self.backend.repos

    @property
    def ws_id(self) -> int | None:
        return self.backend.workspace_id

    @property
    def ready(self) -> bool:
        return self.backend.repos is not None

    def toast(self, kind: str, title: str, message: str = "") -> None:
        self.backend.toast.emit(kind, title, message)

    # -- переопределяемое ---------------------------------------------------
    @Slot()
    def refresh(self) -> None:
        """Перечитать данные из хранилища."""

    def on_workspace_changed(self) -> None:
        self.refresh()

    def on_event(self, event: "Event") -> None:
        """Реакция на событие ядра (по умолчанию ничего)."""

    def reset(self) -> None:
        """Сброс при выходе из профиля."""
        self._s.clear()
        self.changed.emit()


# -- форматтеры -------------------------------------------------------------------


def fmt_tokens(value: int | float) -> str:
    value = int(value or 0)
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    if value >= 10_000:
        return f"{value / 1000:.1f}k"
    return f"{value:,}".replace(",", " ")


def fmt_money(value: float) -> str:
    """Сумма с точностью, при которой копеечные расходы не превращаются в $0.00."""
    value = float(value or 0)
    if value >= 100:
        return f"${value:,.0f}".replace(",", " ")
    if value >= 1:
        return f"${value:.2f}"
    if value >= 0.01:
        return f"${value:.3f}"
    if value == 0:
        return "$0"
    return f"${value:.4f}"


def when(iso: str | None, fmt: str = "%d.%m %H:%M") -> str:
    return local_time(iso or "", fmt) if iso else ""


def as_int(value: Any, default: int = -1) -> int:
    """Число из QML: там вместо него легко приходит ``undefined``, строка или 3.0."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def as_float(value: Any, default: float) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def elide(text: str, limit: int) -> str:
    text = (text or "").strip().replace("\n", " ")
    return text if len(text) <= limit else text[: limit - 1] + "…"


def error_text(exc: BaseException) -> str:
    from providers.base import ProviderError

    if isinstance(exc, (ProviderError, RuntimeError, ValueError)):
        return str(exc)
    return f"{type(exc).__name__}: {exc}"


def status_title(code: str) -> str:
    return tr(f"status.{code}") if code else ""
````

### `ui/bridge/listmodel.py`

*164 строк*

````python
"""Модель списка для QML поверх обычных словарей.

Главное отличие от «сбросить и заполнить заново»: ``set_items`` сравнивает
старый и новый списки по ключу и сообщает QML только о реальных изменениях
(вставках, удалениях, правках строк). Благодаря этому ``ListView`` может
анимировать появление и исчезновение карточек, а прокрутка и выделение не
прыгают при каждом обновлении данных.
"""

from __future__ import annotations

from typing import Any, Iterable

from PySide6.QtCore import (
    Property,
    QAbstractListModel,
    QByteArray,
    QModelIndex,
    QPersistentModelIndex,
    Qt,
    Signal,
    Slot,
)

_BASE_ROLE = Qt.ItemDataRole.UserRole + 1


class DictListModel(QAbstractListModel):
    """Список словарей с фиксированным набором ролей.

    Роли задаются при создании: каждый ключ словаря доступен в делегате QML
    как одноимённое свойство (``model.title`` или просто ``title``).
    """

    countChanged = Signal()

    def __init__(self, roles: Iterable[str], key: str = "id", parent=None) -> None:
        super().__init__(parent)
        self._roles = list(roles)
        if "model" in self._roles:
            # Роль «model» в делегате перекрывает сам объект model, и все
            # обращения вида model.title молча становятся undefined.
            raise ValueError("роль 'model' запрещена: переименуйте её, например в 'modelName'")
        if key not in self._roles:
            self._roles.insert(0, key)
        self._key = key
        self._role_ids = {name: _BASE_ROLE + i for i, name in enumerate(self._roles)}
        self._items: list[dict[str, Any]] = []

    # -- Qt API ----------------------------------------------------------------
    def rowCount(self, parent: QModelIndex | QPersistentModelIndex = QModelIndex()) -> int:  # noqa: N802
        return 0 if parent.isValid() else len(self._items)

    def data(self, index: QModelIndex | QPersistentModelIndex, role: int = Qt.ItemDataRole.DisplayRole) -> Any:
        if not index.isValid() or not 0 <= index.row() < len(self._items):
            return None
        name = self._roles[role - _BASE_ROLE] if role >= _BASE_ROLE else None
        return self._items[index.row()].get(name) if name else None

    def roleNames(self) -> dict[int, QByteArray]:  # noqa: N802
        return {rid: QByteArray(name.encode()) for name, rid in self._role_ids.items()}

    def _count(self) -> int:
        return len(self._items)

    count = Property(int, _count, notify=countChanged)

    # -- Python API ------------------------------------------------------------
    @property
    def items(self) -> list[dict[str, Any]]:
        return self._items

    @Slot(int, result="QVariantMap")
    def get(self, row: int) -> dict[str, Any]:
        return dict(self._items[row]) if 0 <= row < len(self._items) else {}

    def find(self, key_value: Any) -> int:
        for row, item in enumerate(self._items):
            if item.get(self._key) == key_value:
                return row
        return -1

    def update_row(self, key_value: Any, **changes: Any) -> None:
        """Точечная правка одной строки - без пересборки списка."""
        row = self.find(key_value)
        if row < 0:
            return
        item = self._items[row]
        changed = [name for name, value in changes.items() if item.get(name) != value]
        if not changed:
            return
        item.update(changes)
        idx = self.index(row)
        self.dataChanged.emit(idx, idx, [self._role_ids[n] for n in changed
                                         if n in self._role_ids])

    def append(self, item: dict[str, Any], limit: int | None = None) -> None:
        """Добавляет строку в конец; при превышении ``limit`` срезает начало."""
        if limit is not None and len(self._items) >= limit:
            drop = len(self._items) - limit + 1
            self.beginRemoveRows(QModelIndex(), 0, drop - 1)
            del self._items[:drop]
            self.endRemoveRows()
        row = len(self._items)
        self.beginInsertRows(QModelIndex(), row, row)
        self._items.append(dict(item))
        self.endInsertRows()
        self.countChanged.emit()

    def clear(self) -> None:
        if not self._items:
            return
        self.beginResetModel()
        self._items = []
        self.endResetModel()
        self.countChanged.emit()

    def set_items(self, new_items: list[dict[str, Any]]) -> None:
        """Приводит модель к новому списку минимальным набором изменений."""
        new_items = [dict(it) for it in new_items]
        old_keys = [it.get(self._key) for it in self._items]
        new_keys = [it.get(self._key) for it in new_items]
        if (len(set(new_keys)) != len(new_keys) or None in new_keys
                or len(set(old_keys)) != len(old_keys)):
            self._reset(new_items)
            return

        before = len(self._items)
        new_set = set(new_keys)
        # 1. удаляем то, чего больше нет (с конца, чтобы не сбивать индексы)
        for row in range(len(self._items) - 1, -1, -1):
            if self._items[row].get(self._key) not in new_set:
                self.beginRemoveRows(QModelIndex(), row, row)
                del self._items[row]
                self.endRemoveRows()

        # 2. если порядок оставшихся изменился - проще пересобрать целиком
        kept = [it.get(self._key) for it in self._items]
        if kept != [k for k in new_keys if k in set(kept)]:
            self._reset(new_items)
            return

        # 3. вставляем новые на свои места и правим изменившиеся
        for row, item in enumerate(new_items):
            key = item.get(self._key)
            if row < len(self._items) and self._items[row].get(self._key) == key:
                old = self._items[row]
                changed = [n for n in self._roles if old.get(n) != item.get(n)]
                if changed:
                    self._items[row] = item
                    idx = self.index(row)
                    self.dataChanged.emit(idx, idx, [self._role_ids[n] for n in changed])
            else:
                self.beginInsertRows(QModelIndex(), row, row)
                self._items.insert(row, item)
                self.endInsertRows()
        if len(self._items) != before:
            self.countChanged.emit()

    def _reset(self, items: list[dict[str, Any]]) -> None:
        self.beginResetModel()
        self._items = items
        self.endResetModel()
        self.countChanged.emit()
````

### `ui/bridge/i18n_bridge.py`

*63 строк*

````python
"""Локализация для QML.

Словарь строк текущего языка отдаётся в QML свойством ``t``; биндинги вида
``text: i18n.t["login.title"]`` зависят от этого свойства, поэтому при смене
языка весь интерфейс перерисовывается сам - без пересборки окна, как было
в версии на виджетах.
"""

from __future__ import annotations

from typing import Any

from PySide6.QtCore import Property, QObject, Signal, Slot

from app import i18n as catalog


class I18n(QObject):
    changed = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._strings: dict[str, str] = {}
        self._rebuild()
        catalog.on_language_changed(self._on_catalog_changed)

    def _rebuild(self) -> None:
        # Русский словарь - базовый: если в английском чего-то нет, строка
        # всё равно не пропадёт из интерфейса.
        merged = dict(catalog.RU)
        merged.update(catalog.catalog_for(catalog.current_language()))
        self._strings = merged

    def _on_catalog_changed(self) -> None:
        self._rebuild()
        self.changed.emit()

    def _t(self) -> dict[str, str]:
        return self._strings

    t = Property("QVariantMap", _t, notify=changed)

    def _lang(self) -> str:
        return catalog.current_language()

    lang = Property(str, _lang, notify=changed)

    def _languages(self) -> list[dict[str, str]]:
        return [{"code": c, "title": t} for c, t in catalog.available_languages()]

    languages = Property("QVariantList", _languages, constant=True)

    @Slot(str, "QVariantMap", result=str)
    def fmt(self, template: str, args: dict[str, Any]) -> str:
        """Подставляет ``{placeholders}``; сломанный шаблон возвращается как есть."""
        try:
            return (template or "").format(**(args or {}))
        except (KeyError, IndexError, ValueError):
            return template or ""

    @Slot(str, result=str)
    def status(self, code: str) -> str:
        return self._strings.get(f"status.{code}", code)
````

### `ui/bridge/backend.py`

*441 строк*

````python
"""Корневой объект моста: профиль, воркспейс, события ядра, уведомления.

QML видит его как контекстное свойство ``backend``; контроллеры страниц
доступны как его свойства (``backend.agents``, ``backend.run`` …).
"""

from __future__ import annotations

import asyncio
import logging
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import Property, QObject, QTimer, QUrl, Signal, Slot
from PySide6.QtGui import QDesktopServices

from app.config import APP_NAME, APP_VERSION, PATHS, AppSettings
from app.i18n import available_languages, set_language, tr
from core.events import Event, EventBus, EventType
from core.orchestrator import Orchestrator
from core.security.crypto import (
    Session,
    keyring_available,
    keyring_delete_password,
    keyring_get_password,
    keyring_store_password,
)
from storage.db import Database
from storage.repositories import Repos, UserRepo
from ui.bridge.core import StateObject, error_text, fmt_money, sprop
from utils.asyncutils import run_async

log = logging.getLogger("aiorc.ui")

MIN_PASSWORD_LEN = 8
MOTION_LEVELS = {"off": 0, "reduced": 1, "full": 2}


class Backend(StateObject):
    """Состояние приложения, общее для всех экранов."""

    changed = Signal()
    #: уведомление в углу окна: вид (success|info|warning|error), заголовок, текст
    toast = Signal(str, str, str)
    #: завершилась попытка входа или регистрации: ok, текст ошибки
    authFinished = Signal(bool, str)
    #: ядро прислало событие - для страниц, которым нужна живая лента
    coreEvent = Signal("QVariantMap")
    #: просьба интерфейсу открыть страницу
    navigateRequested = Signal(str)

    def __init__(self, db: Database, settings: AppSettings, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.db = db
        self.settings = settings
        self.users = UserRepo(db)
        self.session: Session | None = None
        self.repos: Repos | None = None
        self.bus: EventBus | None = None
        self.orchestrator: Orchestrator | None = None
        self.workspace_id: int | None = None

        from ui.bridge.pages import build_controllers

        self._controllers = build_controllers(self)
        for name, controller in self._controllers.items():
            setattr(self, f"_c_{name}", controller)

        self._state_timer = QTimer(self)
        self._state_timer.setInterval(1000)
        self._state_timer.timeout.connect(self._tick)

        self._set(loggedIn=False, username="", workspaceId=-1, workspaceName="",
                  running=False, paused=False, pendingApprovals=0, authBusy=False,
                  runElapsed="", runTokens="0", runCost="$0",
                  motion=settings.motion if settings.motion in MOTION_LEVELS else "full")
        self.refresh_profiles()

    # -- свойства -------------------------------------------------------------
    loggedIn = sprop(bool, "loggedIn", False, changed)
    username = sprop(str, "username", "", changed)
    profiles = sprop("QVariantList", "profiles", [], changed)
    lastUsername = sprop(str, "lastUsername", "", changed)
    rememberDefault = sprop(bool, "rememberDefault", False, changed)
    authBusy = sprop(bool, "authBusy", False, changed)
    workspaceId = sprop(int, "workspaceId", -1, changed)
    workspaceName = sprop(str, "workspaceName", "", changed)
    running = sprop(bool, "running", False, changed)
    paused = sprop(bool, "paused", False, changed)
    pendingApprovals = sprop(int, "pendingApprovals", 0, changed)
    runElapsed = sprop(str, "runElapsed", "", changed)
    runTokens = sprop(str, "runTokens", "0", changed)
    runCost = sprop(str, "runCost", "$0", changed)
    motion = sprop(str, "motion", "full", changed)

    def _motion_level(self) -> int:
        return MOTION_LEVELS.get(self._s.get("motion", "full"), 2)

    motionLevel = Property(int, _motion_level, notify=changed)

    def _const(value):  # noqa: N805 - фабрика константных свойств
        return Property(str, lambda self: value, constant=True)

    appName = _const(APP_NAME)
    appVersion = _const(APP_VERSION)
    dataRoot = _const(str(PATHS.home))

    def _keyring(self) -> bool:
        return keyring_available()

    keyringAvailable = Property(bool, _keyring, constant=True)

    def _controller(name: str):  # noqa: N805
        return Property(QObject, lambda self: self._controllers[name], constant=True)

    workspaces = _controller("workspaces")
    keys = _controller("keys")
    agents = _controller("agents")
    task = _controller("task")
    run = _controller("run")
    supervisor = _controller("supervisor")
    dashboard = _controller("dashboard")
    budget = _controller("budget")
    exporter = _controller("exporter")
    prefs = _controller("prefs")

    # -- профиль --------------------------------------------------------------
    def refresh_profiles(self) -> None:
        names = self.users.list_usernames()
        last = self.settings.last_username if self.settings.last_username in names else \
            (names[0] if names else "")
        self._set(profiles=names, lastUsername=last,
                  rememberDefault=bool(self.settings.remember_master_password))

    @Slot(str, result=str)
    def savedPassword(self, username: str) -> str:  # noqa: N802
        """Пароль из хранилища ОС, если пользователь просил его запомнить."""
        if username and self.settings.remember_master_password and keyring_available():
            return keyring_get_password(username) or ""
        return ""

    @Slot(str, str, bool)
    def signIn(self, username: str, password: str, remember: bool) -> None:  # noqa: N802
        username = (username or "").strip()
        if not username or not password:
            self.authFinished.emit(False, tr("login.bad_credentials"))
            return
        self._set(authBusy=True)

        async def job() -> Session | None:
            # Argon2id занимает десятые доли секунды - в отдельном потоке,
            # чтобы индикатор на кнопке не замирал.
            return await asyncio.to_thread(self.users.authenticate, username, password)

        def done(session: Session | None) -> None:
            self._set(authBusy=False)
            if session is None:
                self.authFinished.emit(False, tr("login.bad_credentials"))
                return
            self.settings.last_username = username
            self.settings.remember_master_password = bool(remember)
            self.settings.save()
            if remember:
                keyring_store_password(username, password)
            else:
                keyring_delete_password(username)
            self._open_session(session)
            self.authFinished.emit(True, "")

        def failed(exc: Exception) -> None:
            self._set(authBusy=False)
            self.authFinished.emit(False, error_text(exc))

        run_async(job(), done, failed)

    @Slot(str, str, str)
    def signUp(self, username: str, password: str, password2: str) -> None:  # noqa: N802
        username = (username or "").strip()
        error = ""
        if not username:
            error = tr("login.need_username")
        elif self.users.exists(username):
            error = tr("login.user_exists")
        elif len(password) < MIN_PASSWORD_LEN:
            error = tr("login.password_short")
        elif password != password2:
            error = tr("login.password_mismatch")
        if error:
            self.authFinished.emit(False, error)
            return
        self._set(authBusy=True)

        async def job() -> Session:
            return await asyncio.to_thread(self.users.create, username, password)

        def done(session: Session) -> None:
            self._set(authBusy=False)
            self.settings.last_username = username
            self.settings.save()
            self.refresh_profiles()
            self._open_session(session)
            self.authFinished.emit(True, "")
            self.toast.emit("success", tr("toast.profile_created"), username)

        def failed(exc: Exception) -> None:
            self._set(authBusy=False)
            self.authFinished.emit(False, error_text(exc))

        run_async(job(), done, failed)

    @Slot(str, result=int)
    def passwordStrength(self, password: str) -> int:  # noqa: N802
        """Оценка 0..4 для индикатора надёжности при создании профиля."""
        if not password:
            return 0
        score = 0
        if len(password) >= MIN_PASSWORD_LEN:
            score += 1
        if len(password) >= 12:
            score += 1
        classes = sum(bool(f(password)) for f in (
            lambda p: any(c.islower() for c in p), lambda p: any(c.isupper() for c in p),
            lambda p: any(c.isdigit() for c in p), lambda p: any(not c.isalnum() for c in p)))
        if classes >= 2:
            score += 1
        if classes >= 3 and len(password) >= 10:
            score += 1
        return min(score, 4)

    def _open_session(self, session: Session) -> None:
        self.session = session
        self.repos = Repos(self.db, session)
        fixed = self.repos.recover_interrupted_runs()
        if fixed:
            log.info("После аварийного завершения исправлено статусов: %s", fixed)
        self.bus = EventBus()
        self.bus.subscribe(self._on_event)
        self.orchestrator = Orchestrator(self.repos, self.bus)
        self._set(loggedIn=True, username=session.username)
        self._restore_workspace()
        self._state_timer.start()
        if fixed:
            self.toast.emit("info", tr("toast.recovered"), tr("toast.recovered_text"))

    @Slot()
    def logout(self) -> None:
        if self.orchestrator and self.orchestrator.state.running:
            self.orchestrator.stop()
        self._state_timer.stop()
        # Остановленный прогон ещё досылает события о завершении; экраны
        # вышедшего профиля их получать не должны.
        if self.bus is not None:
            self.bus.unsubscribe(self._on_event)
        if self.session:
            self.session.wipe()
        self.session = None
        self.repos = None
        self.bus = None
        self.orchestrator = None
        self.workspace_id = None
        for controller in self._controllers.values():
            controller.reset()
        self._set(loggedIn=False, username="", workspaceId=-1, workspaceName="",
                  running=False, paused=False, pendingApprovals=0)
        self.refresh_profiles()

    def change_password(self, old: str, new1: str, new2: str) -> str:
        """Смена пароля; возвращает текст ошибки или пустую строку."""
        if self.repos is None or self.session is None:
            return tr("login.bad_credentials")
        if len(new1) < MIN_PASSWORD_LEN:
            return tr("login.password_short")
        if new1 != new2:
            return tr("login.password_mismatch")
        if not self.repos.users.change_password(self.session, old, new1):
            return tr("login.bad_credentials")
        # Сохранённый в хранилище ОС пароль иначе перестал бы подходить.
        if self.settings.remember_master_password and keyring_available():
            keyring_store_password(self.session.username, new1)
        return ""

    # -- воркспейс --------------------------------------------------------------
    def _restore_workspace(self) -> None:
        assert self.repos is not None and self.session is not None
        user = self.repos.users.get(self.session.user_id)
        last = user.settings.get("last_workspace_id") if user else None
        ids = [w.id for w in self.repos.workspaces.list(self.session.user_id)]
        self.select_workspace(last if last in ids else (ids[0] if ids else None))

    def select_workspace(self, ws_id: int | None) -> None:
        if self.repos is None or self.session is None:
            return
        if self.orchestrator and self.orchestrator.state.running and ws_id != self.workspace_id:
            self.toast.emit("warning", tr("toast.run_active"), tr("toast.run_active_text"))
            return
        self.workspace_id = ws_id
        if ws_id is not None:
            PATHS.workspace_dir(ws_id).mkdir(parents=True, exist_ok=True)
            user = self.repos.users.get(self.session.user_id)
            if user is not None:
                settings = dict(user.settings)
                settings["last_workspace_id"] = ws_id
                self.repos.users.save_settings(self.session.user_id, settings)
        self._update_workspace_name()
        for controller in self._controllers.values():
            try:
                controller.on_workspace_changed()
            except Exception:  # noqa: BLE001 - одна страница не должна ломать остальные
                log.exception("Контроллер %s не обновился", type(controller).__name__)

    def _update_workspace_name(self) -> None:
        ws = self.repos.workspaces.get(self.workspace_id) if (self.repos and self.workspace_id) else None
        self._set(workspaceId=ws.id if ws else -1, workspaceName=ws.name if ws else "")

    @Slot(int)
    def selectWorkspace(self, ws_id: int) -> None:  # noqa: N802
        self.select_workspace(ws_id if ws_id >= 0 else None)

    # -- настройки приложения ---------------------------------------------------
    @Slot(str)
    def setLanguage(self, code: str) -> None:  # noqa: N802
        if code not in {c for c, _ in available_languages()}:
            return
        set_language(code)
        self.settings.language = code
        self.settings.save()
        # Статусы и подписи, собранные в Python, тоже на новом языке.
        for controller in self._controllers.values():
            if self.repos is not None:
                try:
                    controller.refresh()
                except Exception:  # noqa: BLE001
                    log.exception("Не обновился после смены языка: %s", controller)

    @Slot(str)
    def setMotion(self, level: str) -> None:  # noqa: N802
        if level not in MOTION_LEVELS:
            return
        self.settings.motion = level
        self.settings.save()
        self._set(motion=level)

    @Slot(str)
    def navigate(self, page: str) -> None:
        self.navigateRequested.emit(page)

    @Slot(str)
    def openPath(self, path: str) -> None:  # noqa: N802
        """Открывает файл или каталог в системном проводнике."""
        target = Path(path)
        if not target.exists():
            self.toast.emit("warning", tr("toast.not_found"), str(target))
            return
        if sys.platform == "win32" and target.is_file():
            subprocess.Popen(["explorer", "/select,", str(target)])  # noqa: S603, S607
            return
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(target if target.is_dir() else target.parent)))

    @Slot(str)
    def copyText(self, text: str) -> None:  # noqa: N802
        from PySide6.QtGui import QGuiApplication

        QGuiApplication.clipboard().setText(text or "")
        self.toast.emit("info", tr("toast.copied"), "")

    # -- события ядра --------------------------------------------------------------
    def _on_event(self, event: Event) -> None:
        if event.workspace_id is not None and self.workspace_id is not None \
                and event.workspace_id != self.workspace_id:
            return
        for controller in self._controllers.values():
            try:
                controller.on_event(event)
            except Exception:  # noqa: BLE001
                log.exception("Сбой обработки события %s", event.type)
        self._sync_run_state()
        self._toast_for(event)
        if event.type is not EventType.AGENT_DELTA:
            self.coreEvent.emit({"type": event.type.value, "message": event.message,
                                 "agent": event.agent_name})

    def _sync_run_state(self) -> None:
        orch = self.orchestrator
        if orch is None:
            return
        gate = orch.gate
        self._set(running=orch.state.running, paused=orch.state.paused,
                  pendingApprovals=len(gate.pending()) if gate else 0)

    def _tick(self) -> None:
        """Раз в секунду: таймер прогона и живые счётчики расхода."""
        orch = self.orchestrator
        if orch is None or not orch.state.running:
            if self._s.get("runElapsed"):
                self._set(runElapsed="")
            return
        from datetime import datetime, timezone

        try:
            started = datetime.fromisoformat(orch.state.started_at)
            seconds = int((datetime.now(timezone.utc) - started).total_seconds())
        except ValueError:
            seconds = 0
        minutes, sec = divmod(max(seconds, 0), 60)
        hours, minutes = divmod(minutes, 60)
        elapsed = f"{hours}:{minutes:02d}:{sec:02d}" if hours else f"{minutes:02d}:{sec:02d}"
        from ui.bridge.core import fmt_tokens

        self._set(runElapsed=elapsed, runTokens=fmt_tokens(orch.state.tokens),
                  runCost=fmt_money(orch.state.cost))

    def _toast_for(self, event: Event) -> None:
        kind = event.type
        if kind is EventType.RUN_FINISHED:
            p = event.payload
            if p.get("stopped"):
                self.toast.emit("warning", tr("toast.run_stopped"), event.message)
            elif p.get("failed"):
                self.toast.emit("error", tr("toast.run_failed"), event.message)
            elif p.get("escalated"):
                self.toast.emit("warning", tr("toast.run_review"), event.message)
            else:
                self.toast.emit("success", tr("toast.run_done"), event.message)
        elif kind is EventType.APPROVAL_REQUESTED:
            self.toast.emit("warning", tr("toast.need_decision"), event.message)
        elif kind is EventType.BUDGET_ALERT:
            self.toast.emit("warning", tr("toast.budget_alert"), event.message)
        elif kind is EventType.BUDGET_EXCEEDED:
            self.toast.emit("error", tr("toast.budget_exceeded"), event.message)
        elif kind is EventType.BUDGET_EXTENDED:
            self.toast.emit("info", tr("toast.budget_extended"), event.message)
        elif kind is EventType.SUBTASK_FAILED:
            who = f"{event.agent_name}: " if event.agent_name else ""
            self.toast.emit("error", tr("toast.subtask_failed"), who + event.message)

    # -- служебное -----------------------------------------------------------------
    def shutdown(self) -> None:
        """Закрытие окна: гасим агентов, чтобы не оставить висящих запросов."""
        if self.orchestrator and self.orchestrator.state.running:
            self.orchestrator.stop()
````

### `ui/bridge/pages.py`

*31 строк*

````python
"""Сборка контроллеров страниц - в одном месте, чтобы Backend не знал деталей."""

from __future__ import annotations

from ui.bridge.c_agents import AgentsController
from ui.bridge.c_budget import BudgetController
from ui.bridge.c_dashboard import DashboardController
from ui.bridge.c_export import ExportController
from ui.bridge.c_keys import KeysController
from ui.bridge.c_prefs import PrefsController
from ui.bridge.c_run import RunController
from ui.bridge.c_supervisor import SupervisorController
from ui.bridge.c_task import TaskController
from ui.bridge.c_workspaces import WorkspacesController


def build_controllers(backend) -> dict:
    # Порядок важен: супервайзер описывает модель раньше, чем её спросит
    # карточка супервайзера на странице выполнения.
    return {
        "workspaces": WorkspacesController(backend),
        "keys": KeysController(backend),
        "agents": AgentsController(backend),
        "task": TaskController(backend),
        "supervisor": SupervisorController(backend),
        "run": RunController(backend),
        "dashboard": DashboardController(backend),
        "budget": BudgetController(backend),
        "exporter": ExportController(backend),
        "prefs": PrefsController(backend),
    }
````

### `ui/bridge/c_workspaces.py`

*93 строк*

````python
"""Воркспейсы: параллельные проекты со своими агентами, задачей и настройками."""

from __future__ import annotations

import shutil

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.config import DEFAULT_WORKSPACE_SETTINGS, PATHS
from app.i18n import tr
from ui.bridge.core import Controller, fmt_money, fmt_tokens, when
from ui.bridge.listmodel import DictListModel


class WorkspacesController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._model = DictListModel(["id", "name", "description", "agents", "updated",
                                     "active", "tokens", "cost", "taskTitle"], parent=self)

    def _get_model(self) -> QObject:
        return self._model

    model = Property(QObject, _get_model, constant=True)

    @Slot()
    def refresh(self) -> None:
        if not self.ready:
            return
        items = []
        for ws in self.repos.workspaces.list(self.repos.session.user_id):
            tokens, cost = self.repos.budgets.workspace_totals(ws.id)
            task = self.repos.tasks.current(ws.id)
            items.append({
                "id": ws.id, "name": ws.name, "description": ws.description,
                "agents": self.repos.workspaces.agent_count(ws.id),
                "updated": when(ws.updated_at), "active": ws.id == self.ws_id,
                "tokens": fmt_tokens(tokens), "cost": fmt_money(cost),
                "taskTitle": task.title if task else "",
            })
        self._model.set_items(items)

    def reset(self) -> None:
        super().reset()
        self._model.clear()

    @Slot(str, str, result=str)
    def create(self, name: str, description: str) -> str:
        name = (name or "").strip()
        if not name:
            return tr("ws.need_name")
        ws = self.repos.workspaces.create(self.repos.session.user_id, name,
                                          (description or "").strip(),
                                          dict(DEFAULT_WORKSPACE_SETTINGS))
        PATHS.workspace_dir(ws.id).mkdir(parents=True, exist_ok=True)
        self.backend.select_workspace(ws.id)
        # Во время прогона переключение не состоится, но новый воркспейс
        # всё равно должен появиться в списке.
        self.refresh()
        self.toast("success", tr("toast.ws_created"), name)
        return ""

    @Slot(int, str, str, result=str)
    def update(self, ws_id: int, name: str, description: str) -> str:
        name = (name or "").strip()
        if not name:
            return tr("ws.need_name")
        self.repos.workspaces.update(ws_id, name=name, description=(description or "").strip())
        self.backend._update_workspace_name()
        self.refresh()
        return ""

    @Slot(int)
    def remove(self, ws_id: int) -> None:
        if self.backend.orchestrator and self.backend.orchestrator.state.running \
                and ws_id == self.ws_id:
            self.toast("warning", tr("toast.run_active"), tr("toast.run_active_text"))
            return
        ws = self.repos.workspaces.get(ws_id)
        self.repos.workspaces.delete(ws_id)
        shutil.rmtree(PATHS.workspace_dir(ws_id), ignore_errors=True)
        if ws_id == self.ws_id:
            remaining = self.repos.workspaces.list(self.repos.session.user_id)
            self.backend.select_workspace(remaining[0].id if remaining else None)
        else:
            self.refresh()
        self.toast("info", tr("toast.ws_deleted"), ws.name if ws else "")

    @Slot(int)
    def select(self, ws_id: int) -> None:
        self.backend.select_workspace(ws_id)
````

### `ui/bridge/c_keys.py`

*139 строк*

````python
"""API-ключи провайдеров: общие для всех воркспейсов профиля."""

from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.i18n import tr
from providers.factory import build_provider
from providers.presets import preset, preset_list
from ui.bridge.core import Controller, error_text, when
from ui.bridge.listmodel import DictListModel
from utils.asyncutils import run_async


class KeysController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._model = DictListModel(
            ["id", "label", "provider", "providerTitle", "baseUrl", "hasSecret",
             "local", "free", "models", "testState", "testMessage", "created"],
            parent=self)
        self._presets = [
            {"key": p.key, "title": p.title, "baseUrl": p.base_url,
             "requiresKey": p.requires_key, "free": p.free_tier, "local": p.local,
             "notes": p.notes, "docsUrl": p.docs_url,
             "models": ", ".join(p.suggested_models[:3])}
            for p in preset_list()
        ]
        #: результаты проверок живут до выхода из профиля
        self._tests: dict[int, tuple[str, str]] = {}

    def _get_model(self) -> QObject:
        return self._model

    model = Property(QObject, _get_model, constant=True)

    def _get_presets(self) -> list:
        return self._presets

    presets = Property("QVariantList", _get_presets, constant=True)

    @Slot()
    def refresh(self) -> None:
        if not self.ready:
            return
        items = []
        for key in self.repos.keys.list():
            p = preset(key.provider)
            state, message = self._tests.get(key.id, ("", ""))
            items.append({
                "id": key.id, "label": key.label, "provider": key.provider,
                "providerTitle": p.title, "baseUrl": key.base_url or p.base_url,
                "hasSecret": key.has_secret, "local": p.local, "free": p.free_tier,
                "models": len(key.meta.get("models") or []),
                "testState": state, "testMessage": message, "created": when(key.created_at),
            })
        self._model.set_items(items)

    def reset(self) -> None:
        super().reset()
        self._tests.clear()
        self._model.clear()

    @Slot(str, str, str, str, result=str)
    def create(self, provider: str, label: str, base_url: str, secret: str) -> str:
        p = preset(provider)
        secret = (secret or "").strip()
        if p.requires_key and not secret:
            return tr("keys.need_secret")
        if p.key == "custom" and not (base_url or "").strip():
            return tr("keys.need_url")
        key = self.repos.keys.create((label or "").strip() or p.title, provider, secret,
                                     (base_url or "").strip())
        self.refresh()
        self.backend.agents.refresh()
        self.toast("success", tr("toast.key_saved"), key.label)
        self.test(key.id)
        return ""

    @Slot(int, str, str, str, result=str)
    def update(self, key_id: int, label: str, base_url: str, secret: str) -> str:
        key = self.repos.keys.get(key_id)
        if key is None:
            return tr("keys.not_found")
        self.repos.keys.update(key_id, (label or "").strip() or key.label,
                               (base_url or "").strip(), (secret or "").strip() or None)
        self._tests.pop(key_id, None)
        self.refresh()
        self.backend.agents.refresh()
        return ""

    @Slot(int)
    def remove(self, key_id: int) -> None:
        key = self.repos.keys.get(key_id)
        self.repos.keys.delete(key_id)
        self._tests.pop(key_id, None)
        self.refresh()
        self.backend.agents.refresh()
        self.toast("info", tr("toast.key_deleted"), key.label if key else "")

    @Slot(int)
    def test(self, key_id: int) -> None:
        """Реальный запрос списка моделей: проверяет и ключ, и адрес сервера."""
        key = self.repos.keys.get(key_id)
        if key is None:
            return
        self._tests[key_id] = ("testing", "")
        self._model.update_row(key_id, testState="testing", testMessage="")

        async def job() -> list[str]:
            secret = self.repos.keys.reveal(key.id)
            provider = build_provider(key.provider, secret, key.base_url, timeout=20)
            try:
                return await provider.test()
            finally:
                await provider.aclose()

        def done(models: list[str]) -> None:
            if not self.ready:          # за время проверки вышли из профиля
                return
            message = tr("keys.test_ok", n=len(models))
            self._tests[key_id] = ("ok", message)
            # Кэш для выпадающего списка моделей. Пишем только его: подпись и
            # адрес ключа могли поправить, пока шёл запрос.
            self.repos.keys.update_meta(key.id, models=models[:300])
            self._model.update_row(key_id, testState="ok", testMessage=message,
                                   models=len(models))
            self.backend.agents.refresh()

        def failed(exc: Exception) -> None:
            if not self.ready:
                return
            message = tr("keys.test_fail", err=error_text(exc))
            self._tests[key_id] = ("fail", message)
            self._model.update_row(key_id, testState="fail", testMessage=message)

        run_async(job(), done, failed)
````

### `ui/bridge/c_agents.py`

*245 строк*

````python
"""Агенты воркспейса: роли, модели, инструменты, системные промпты."""

from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.i18n import current_language, tr
from core.agents.roles import COMMON_RULES, TEMPLATES, by_key, title as role_title
from core.tools.base import default_registry, expand_tool_names
from providers.base import is_chat_model
from providers.factory import build_provider, model_price
from providers.presets import preset
from ui.bridge.core import Controller, as_float, as_int, elide, error_text, status_title
from ui.bridge.listmodel import DictListModel
from utils.asyncutils import run_async

#: подписи инструментов в интерфейсе
TOOL_TITLES = {
    "web_search": "tool.web_search", "fetch_url": "tool.fetch_url",
    "read_file": "tool.read_file", "write_file": "tool.write_file",
    "list_dir": "tool.list_dir", "code_exec": "tool.code_exec",
}

ROLE_ICONS = {
    "analyst": "chart-line", "developer": "terminal", "tester": "badge-check",
    "critic": "scale", "documenter": "file-text", "researcher": "book-open",
    "supervisor": "shield-check", "custom": "sparkles",
}


def ordered_models(suggested: list[str], available: list[str]) -> list[str]:
    """Сначала рекомендованные модели, потом остальные, что вернул провайдер.

    Провайдер отдаёт список по алфавиту, и наверх попадают старые модели:
    у Gemini это отключённые 2.0 и закрытые для новых ключей 2.5. Если
    провайдер список прислал, рекомендованные берутся только из него: модель,
    которой у ключа нет, предлагать незачем.
    """
    # Кэш мог сохраниться до того, как появился фильтр, поэтому чистим и здесь.
    available = [m for m in available if is_chat_model(m)]
    if not available:
        return list(suggested)
    have = set(available)
    top = [m for m in suggested if m in have]
    return top + [m for m in available if m not in set(top)]


class AgentsController(Controller):
    changed = Signal()

    #: список моделей загружен с сервера провайдера: id ключа, модели, ошибка
    modelsLoaded = Signal(int, "QVariantList", str)

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._model = DictListModel(
            ["id", "name", "role", "roleTitle", "icon", "provider", "providerTitle",
             "modelName", "keyId", "keyLabel", "temperature", "maxTokens", "tools",
             "toolTitles", "prompt", "promptPreview", "isSupervisor", "status",
             "statusTitle", "enabled", "price"], parent=self)
        self._set(hasKeys=False, keyOptions=[], supervisorId=-1)

    hasKeys = Property(bool, lambda self: self._s.get("hasKeys", False),
                       notify=changed)
    keyOptions = Property("QVariantList", lambda self: self._s.get("keyOptions", []),
                          notify=changed)

    def _get_model(self) -> QObject:
        return self._model

    model = Property(QObject, _get_model, constant=True)

    def _templates(self) -> list[dict]:
        lang = current_language()
        return [{"key": t.key, "title": role_title(t, lang), "icon": ROLE_ICONS.get(t.key, "bot"),
                 "tools": expand_tool_names(t.suggested_tools)} for t in TEMPLATES]

    templates = Property("QVariantList", _templates, notify=changed)

    def _tools(self) -> list[dict]:
        return [{"name": n, "title": tr(TOOL_TITLES.get(n, n))} for n in default_registry().names()]

    tools = Property("QVariantList", _tools, notify=changed)

    @Slot()
    def refresh(self) -> None:
        if not self.ready:
            return
        keys = self.repos.keys.list()
        key_by_id = {k.id: k for k in keys}
        self._set(hasKeys=bool(keys), keyOptions=[
            {"id": k.id, "title": f"{k.label} · {preset(k.provider).title}",
             "provider": k.provider} for k in keys])
        if self.ws_id is None:
            self._model.clear()
            self.changed.emit()
            return
        lang = current_language()
        items = []
        for a in self.repos.agents.list(self.ws_id):
            key = key_by_id.get(a.api_key_id or -1)
            tools = expand_tool_names(a.tools)
            p_in, p_out = model_price(a.provider, a.model) if a.model else (0.0, 0.0)
            items.append({
                "id": a.id, "name": a.name, "role": a.role or "custom",
                "roleTitle": role_title(by_key(a.role or "custom"), lang),
                "icon": ROLE_ICONS.get(a.role or "custom", "bot"),
                "provider": a.provider, "providerTitle": preset(a.provider).title if a.provider else "",
                "modelName": a.model, "keyId": a.api_key_id or -1,
                "keyLabel": key.label if key else tr("agents.key_missing"),
                "temperature": a.temperature, "maxTokens": a.max_tokens,
                "tools": tools, "toolTitles": [tr(TOOL_TITLES.get(t, t)) for t in tools],
                "prompt": a.system_prompt, "promptPreview": elide(a.system_prompt, 150),
                "isSupervisor": a.is_supervisor, "status": a.status,
                "statusTitle": status_title(a.status), "enabled": a.enabled,
                "price": (f"${p_in:g} / ${p_out:g}" if (p_in or p_out)
                          else (tr("agents.free") if a.provider and preset(a.provider).local else "")),
            })
        self._model.set_items(items)
        self.changed.emit()

    def reset(self) -> None:
        super().reset()
        self._model.clear()

    def on_event(self, event) -> None:
        from core.events import EventType

        if event.type is EventType.AGENT_STATUS and event.agent_id:
            status = event.payload.get("status", event.message)
            self._model.update_row(event.agent_id, status=status,
                                   statusTitle=status_title(status))
        elif event.type in (EventType.RUN_FINISHED, EventType.RUN_STOPPED):
            self.refresh()

    # -- форма агента ---------------------------------------------------------
    @Slot(str, result="QVariantMap")
    def templateInfo(self, key: str) -> dict:  # noqa: N802
        template = by_key(key)
        prompt = (template.prompt + "\n\n" + COMMON_RULES.strip()) if template.prompt else ""
        return {"name": role_title(template, current_language()), "prompt": prompt,
                "tools": expand_tool_names(template.suggested_tools)}

    @Slot(int, result="QVariantList")
    def modelsForKey(self, key_id: int) -> list[str]:  # noqa: N802
        """Рекомендованные модели пресета, за ними остальные из кэша проверки ключа."""
        key = self.repos.keys.get(key_id) if self.ready and key_id >= 0 else None
        if key is None:
            return []
        return ordered_models(preset(key.provider).suggested_models,
                              key.meta.get("models") or [])

    @Slot(int)
    def loadModels(self, key_id: int) -> None:  # noqa: N802
        key = self.repos.keys.get(key_id)
        if key is None:
            self.modelsLoaded.emit(key_id, [], tr("keys.not_found"))
            return

        async def job() -> list[str]:
            provider = build_provider(key.provider, self.repos.keys.reveal(key.id),
                                      key.base_url, timeout=20)
            try:
                return await provider.list_models()
            finally:
                await provider.aclose()

        def done(models: list[str]) -> None:
            if self.ready:
                # Только кэш моделей: подпись и адрес за время запроса могли
                # поменять, и старые значения их бы затёрли.
                self.repos.keys.update_meta(key.id, models=models[:300])
            self.modelsLoaded.emit(
                key_id, ordered_models(preset(key.provider).suggested_models, models[:300]), "")

        def failed(exc: Exception) -> None:
            self.modelsLoaded.emit(key_id, [], tr("keys.test_fail", err=error_text(exc)))

        run_async(job(), done, failed)

    @Slot("QVariantMap", result=str)
    def save(self, data: dict) -> str:
        """Создаёт или обновляет агента. Возвращает текст ошибки или пустую строку."""
        if self.ws_id is None:
            return tr("ws.empty")
        name = str(data.get("name") or "").strip()
        model = str(data.get("model") or "").strip()
        key_id = as_int(data.get("keyId"))
        key = self.repos.keys.get(key_id) if key_id >= 0 else None
        if not name:
            return tr("agents.need_name")
        if key is None:
            return tr("agents.need_key")
        if not model:
            return tr("agents.need_model")
        tools = [t for t in (data.get("tools") or []) if t in default_registry().names()]
        fields = dict(
            name=name, role=str(data.get("role") or "custom"),
            system_prompt=str(data.get("prompt") or "").strip(),
            api_key_id=key.id, provider=key.provider, model=model,
            params={"temperature": round(min(max(as_float(data.get("temperature"), 0.7), 0.0), 2.0), 2),
                    "max_tokens": max(1, as_int(data.get("maxTokens"), 2048)), "tools": tools},
            is_supervisor=bool(data.get("isSupervisor", False)),
        )
        agent_id = as_int(data.get("id"))
        if agent_id >= 0:
            self.repos.agents.update(agent_id, **fields)
            self.toast("success", tr("toast.agent_saved"), name)
        else:
            self.repos.agents.create(self.ws_id, **fields)
            self.toast("success", tr("toast.agent_created"), name)
        self._after_change()
        return ""

    @Slot(int)
    def remove(self, agent_id: int) -> None:
        if self.backend.running:
            # Агент мог быть занят подзадачей: его история и отчёт ссылаются
            # на запись, которой больше нет, и прогон падает на сохранении.
            self.toast("warning", tr("toast.run_active"), tr("toast.run_active_text"))
            return
        agent = self.repos.agents.get(agent_id)
        self.repos.agents.delete(agent_id)
        self._after_change()
        self.toast("info", tr("toast.agent_deleted"), agent.name if agent else "")

    @Slot(int, bool)
    def setEnabled(self, agent_id: int, enabled: bool) -> None:  # noqa: N802
        self.repos.agents.update(agent_id, enabled=enabled)
        self._model.update_row(agent_id, enabled=enabled)

    @Slot(int)
    def duplicate(self, agent_id: int) -> None:
        a = self.repos.agents.get(agent_id)
        if a is None:
            return
        self.repos.agents.create(a.workspace_id, a.name + " 2", a.role, a.system_prompt,
                                 a.api_key_id, a.provider, a.model, dict(a.params), False)
        self._after_change()

    def _after_change(self) -> None:
        self.refresh()
        self.backend.task.refresh()
        self.backend.prefs.refresh()
        self.backend.dashboard.schedule()
````

### `ui/bridge/c_task.py`

*290 строк*

````python
"""Постановка задачи и подзадачи: вручную или разбиением через ИИ."""

from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.i18n import tr
from core.planner import match_agent_by_role, plan_subtasks
from ui.bridge.core import (
    Controller,
    as_int,
    elide,
    error_text,
    fmt_money,
    fmt_tokens,
    status_title,
)
from ui.bridge.listmodel import DictListModel
from utils.asyncutils import run_async

FORMATS = ["auto", "markdown", "docx", "pdf", "zip"]
FORMAT_ICONS = {"auto": "wand-sparkles", "markdown": "file-text", "docx": "file-type",
                "pdf": "book-open", "zip": "file-archive"}


def parse_limit(raw: str) -> int | None:
    raw = (raw or "").replace(" ", "").replace("_", "").strip()
    if not raw:
        return None           # пусто = без лимита
    try:
        value = int(raw)
    except ValueError:
        return None
    return value if value > 0 else None


class TaskController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._subtasks = DictListModel(
            ["id", "index", "title", "description", "agentId", "agentName", "status",
             "statusTitle", "deps", "depTitles", "result", "resultPreview", "reworks",
             "tokens", "cost"], parent=self)
        self._set(hasTask=False, taskId=-1, title="", description="", format="auto",
                  tokenLimit="", planning=False, agentOptions=[], status="",
                  statusTitle="", dirty=False)

    hasTask = Property(bool, lambda s: s._s.get("hasTask", False), notify=changed)
    taskId = Property(int, lambda s: s._s.get("taskId", -1), notify=changed)
    title = Property(str, lambda s: s._s.get("title", ""), notify=changed)
    description = Property(str, lambda s: s._s.get("description", ""), notify=changed)
    format = Property(str, lambda s: s._s.get("format", "auto"), notify=changed)
    tokenLimit = Property(str, lambda s: s._s.get("tokenLimit", ""), notify=changed)
    planning = Property(bool, lambda s: s._s.get("planning", False), notify=changed)
    status = Property(str, lambda s: s._s.get("status", ""), notify=changed)
    statusTitle = Property(str, lambda s: s._s.get("statusTitle", ""), notify=changed)
    agentOptions = Property("QVariantList", lambda s: s._s.get("agentOptions", []),
                            notify=changed)

    def _formats(self) -> list[dict]:
        return [{"key": k, "title": tr(f"fmt.{k}"), "icon": FORMAT_ICONS[k]} for k in FORMATS]

    formats = Property("QVariantList", _formats, notify=changed)

    def _get_subtasks(self) -> QObject:
        return self._subtasks

    subtasks = Property(QObject, _get_subtasks, constant=True)

    # -- данные --------------------------------------------------------------
    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            self._subtasks.clear()
            self._set(hasTask=False, taskId=-1, title="", description="", format="auto",
                      tokenLimit="", agentOptions=[], status="", statusTitle="")
            return
        agents = self.repos.agents.list(self.ws_id)
        options = [{"id": a.id, "name": a.name, "model": a.model} for a in agents
                   if not a.is_supervisor]
        task = self.repos.tasks.current(self.ws_id)
        if task is None:
            self._subtasks.clear()
            self._set(hasTask=False, taskId=-1, title="", description="", format="auto",
                      tokenLimit="", agentOptions=options, status="", statusTitle="")
            return
        self._set(hasTask=True, taskId=task.id, title=task.title,
                  description=task.description, format=task.result_format or "auto",
                  tokenLimit=str(task.token_limit) if task.token_limit else "",
                  agentOptions=options, status=task.status,
                  statusTitle=status_title(task.status))
        self._fill_subtasks(task.id, {a.id: a.name for a in agents})

    def _fill_subtasks(self, task_id: int, names: dict[int, str]) -> None:
        subtasks = self.repos.tasks.subtasks(task_id)
        titles = {s.id: s.title for s in subtasks}
        items = []
        for i, s in enumerate(subtasks, 1):
            deps = [int(t) for t in (s.depends_on or "").split(",") if t.strip().isdigit()]
            items.append({
                "id": s.id, "index": i, "title": s.title, "description": s.description,
                "agentId": s.agent_id or -1,
                "agentName": names.get(s.agent_id or -1, tr("task.unassigned")),
                "status": s.status, "statusTitle": status_title(s.status),
                "deps": deps, "depTitles": [titles[d] for d in deps if d in titles],
                "result": s.result, "resultPreview": elide(s.result, 220),
                "reworks": s.rework_count, "tokens": fmt_tokens(s.tokens_in + s.tokens_out),
                "cost": fmt_money(s.cost_usd),
            })
        self._subtasks.set_items(items)

    def reset(self) -> None:
        super().reset()
        self._subtasks.clear()

    def on_event(self, event) -> None:
        from core.events import EventType

        if event.type in (EventType.AGENT_STATUS, EventType.SUBTASK_STARTED,
                          EventType.SUBTASK_FINISHED, EventType.SUBTASK_FAILED,
                          EventType.REPORT_REVIEWED, EventType.APPROVAL_RESOLVED,
                          EventType.RUN_FINISHED, EventType.RUN_STARTED):
            self.refresh()

    # -- задача -------------------------------------------------------------------
    @Slot(str, str, str, str, result=str)
    def saveTask(self, title: str, description: str, fmt: str, limit: str) -> str:  # noqa: N802
        if self.ws_id is None:
            return tr("ws.empty")
        body = (description or "").strip()
        if not body:
            return tr("task.need_body")
        title = (title or "").strip() or tr("task.untitled")
        fmt = fmt if fmt in FORMATS else "auto"
        token_limit = parse_limit(limit)
        if (limit or "").strip() and token_limit is None:
            return tr("task.bad_limit")
        task = self.repos.tasks.current(self.ws_id)
        if task is None:
            self.repos.tasks.create(self.ws_id, title, body, fmt, token_limit)
        else:
            self.repos.tasks.update(task.id, title=title, description=body,
                                    result_format=fmt, token_limit=token_limit)
            # Лимит задачи поменяли посреди прогона - он действует сразу.
            orch = self.backend.orchestrator
            if orch is not None and orch.state.running and orch.budget is not None:
                orch.budget.reload_limits()
        self.refresh()
        self.backend.dashboard.schedule()
        return ""

    @Slot(result=str)
    def newTask(self) -> str:  # noqa: N802
        """Начать новую задачу: прежняя остаётся в истории, экспорт её видит."""
        if self.backend.running:
            return tr("toast.run_active_text")
        if self.ws_id is None:
            return tr("ws.empty")
        self.repos.tasks.create(self.ws_id, tr("task.untitled"), "", "auto", None)
        self.refresh()
        return ""

    # -- подзадачи --------------------------------------------------------------------
    def _ensure_task(self) -> int | None:
        task = self.repos.tasks.current(self.ws_id) if self.ws_id else None
        return task.id if task else None

    @Slot("QVariantMap", result=str)
    def saveSubtask(self, data: dict) -> str:  # noqa: N802
        task_id = self._ensure_task()
        if task_id is None:
            return tr("task.save_first")
        sid = as_int(data.get("id"))
        if sid >= 0 and self.backend.running:
            # Правка подзадачи, которую сейчас выполняет агент, разошлась бы
            # с тем, что он делает, и с тем, что потом проверит супервайзер.
            return tr("toast.run_active_text")
        title = str(data.get("title") or "").strip()
        if not title:
            return tr("task.need_subtask_title")
        agent_id = as_int(data.get("agentId"))
        known = {s.id for s in self.repos.tasks.subtasks(task_id)}
        deps = []
        for raw in data.get("deps") or []:
            dep = as_int(raw)
            if dep in known and dep != sid and dep not in deps:
                deps.append(dep)
        if sid >= 0 and self._creates_cycle(task_id, sid, deps):
            return tr("task.dep_cycle")
        description = str(data.get("description") or "").strip()
        if sid >= 0:
            self.repos.tasks.update_subtask(
                sid, title=title, description=description,
                agent_id=agent_id if agent_id >= 0 else None,
                depends_on=",".join(str(d) for d in deps))
        else:
            st = self.repos.tasks.add_subtask(task_id, title, description,
                                              agent_id if agent_id >= 0 else None)
            if deps:
                self.repos.tasks.update_subtask(st.id, depends_on=",".join(map(str, deps)))
        self.refresh()
        return ""

    def _creates_cycle(self, task_id: int, sid: int, deps: list[int]) -> bool:
        graph = {s.id: [int(t) for t in (s.depends_on or "").split(",") if t.strip().isdigit()]
                 for s in self.repos.tasks.subtasks(task_id)}
        graph[sid] = deps
        seen: set[int] = set()
        stack = list(deps)
        while stack:
            node = stack.pop()
            if node == sid:
                return True
            if node in seen:
                continue
            seen.add(node)
            stack.extend(graph.get(node, []))
        return False

    @Slot(int)
    def removeSubtask(self, sid: int) -> None:  # noqa: N802
        if self.backend.running:
            # Удаление подзадачи посреди прогона рвёт связи в базе, и агент,
            # который её выполняет, падает на записи отчёта.
            self.toast("warning", tr("toast.run_active"), tr("toast.run_active_text"))
            return
        task_id = self._ensure_task()
        self.repos.tasks.delete_subtask(sid)
        # Ссылки на удалённую подзадачу из зависимостей других тоже убираем.
        if task_id is not None:
            for s in self.repos.tasks.subtasks(task_id):
                deps = [t for t in (s.depends_on or "").split(",") if t.strip() and t.strip() != str(sid)]
                if ",".join(deps) != (s.depends_on or ""):
                    self.repos.tasks.update_subtask(s.id, depends_on=",".join(deps))
        self.refresh()

    @Slot(int, int)
    def move(self, sid: int, delta: int) -> None:
        if self.backend.running:
            return
        task_id = self._ensure_task()
        if task_id is None:
            return
        ids = [s.id for s in self.repos.tasks.subtasks(task_id)]
        if sid not in ids:
            return
        i = ids.index(sid)
        j = i + delta
        if 0 <= j < len(ids):
            ids[i], ids[j] = ids[j], ids[i]
            self.repos.tasks.reorder(ids)
            self.refresh()

    @Slot(int)
    def resetSubtask(self, sid: int) -> None:  # noqa: N802
        """Вернуть подзадачу в очередь: следующий прогон выполнит её заново."""
        if self.backend.running:
            self.toast("warning", tr("toast.run_active"), tr("toast.run_active_text"))
            return
        self.repos.tasks.update_subtask(sid, status="idle")
        self.refresh()

    @Slot()
    def autosplit(self) -> None:
        """ИИ разбивает задачу и сразу назначает исполнителей по ролям."""
        task = self.repos.tasks.current(self.ws_id) if self.ws_id else None
        if task is None or not task.description.strip():
            self.toast("warning", tr("task.save_first"), "")
            return
        ws_id, task_id = self.ws_id, task.id
        self._set(planning=True)

        def done(planned) -> None:
            self._set(planning=False)
            # Пока модель думала, пользователь мог выйти из профиля.
            if not self.ready:
                return
            for item in planned:
                agent_id = match_agent_by_role(self.repos, ws_id, item.assignee_role)
                self.repos.tasks.add_subtask(task_id, item.title, item.description, agent_id)
            self.refresh()
            self.toast("success", tr("toast.planned"), tr("toast.planned_n", n=len(planned)))

        def failed(exc: Exception) -> None:
            self._set(planning=False)
            self.toast("error", tr("toast.plan_failed"), error_text(exc))

        run_async(plan_subtasks(self.repos, ws_id, task.title, task.description), done, failed)
````

### `ui/bridge/c_run.py`

*470 строк*

````python
"""Выполнение: запуск прогона, живые рассуждения агентов, граф, лента, решения.

Самое «горячее» место интерфейса: во время прогона события идут десятками
в секунду. Поэтому фрагменты стриминга не пишутся в модель на каждое
событие, а копятся и сбрасываются таймером раз в ~60 мс; ячейки графа и
ленты обновляются точечно, без пересборки списков.
"""

from __future__ import annotations

import html
from collections import defaultdict

from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot

from app.i18n import tr
from core.events import Event, EventType
from core.hitl import Reason
from ui.bridge.c_agents import ROLE_ICONS
from ui.bridge.core import Controller, elide, error_text, fmt_tokens, status_title
from ui.bridge.listmodel import DictListModel
from utils.asyncutils import run_async

#: как часто сбрасывать накопленный стриминг в интерфейс
STREAM_FLUSH_MS = 60
#: сколько символов рассуждения держать в карточке агента
STREAM_KEEP_CHARS = 9000
FEED_LIMIT = 600
SUPERVISOR_CARD = -1
#: так подписывает свои события служба супервайзера (core/supervisor)
SUPERVISOR_NAME = "Супервайзер"

#: как окрашивать события в ленте
FEED_TONES = {
    EventType.RUN_STARTED: "accent", EventType.RUN_FINISHED: "success",
    EventType.RUN_PAUSED: "warning", EventType.RUN_RESUMED: "accent",
    EventType.RUN_STOPPED: "warning", EventType.AGENT_THINKING: "muted",
    EventType.AGENT_TOOL_CALL: "tool", EventType.AGENT_TOOL_RESULT: "muted",
    EventType.SUBTASK_STARTED: "accent", EventType.SUBTASK_PROGRESS: "info",
    EventType.SUBTASK_FINISHED: "success", EventType.SUBTASK_FAILED: "error",
    EventType.REPORT_CREATED: "success", EventType.REPORT_REVIEWED: "violet",
    EventType.SUMMARY_CREATED: "violet", EventType.INCIDENT_CREATED: "error",
    EventType.APPROVAL_REQUESTED: "warning", EventType.APPROVAL_RESOLVED: "info",
    EventType.BUDGET_ALERT: "warning", EventType.BUDGET_EXCEEDED: "error",
    EventType.BUDGET_EXTENDED: "info", EventType.USAGE: "muted",
    EventType.LOG: "muted", EventType.ERROR: "error",
}
#: события, которые в ленте только шумят
FEED_SKIP = {EventType.AGENT_STATUS, EventType.AGENT_DELTA, EventType.USAGE}

DECISION_TONES = {"approve": "success", "rework": "warning", "skip": "muted",
                  "abort": "error", "extend": "accent"}
REASON_ICONS = {
    Reason.CONFLICT.value: "split", Reason.NOT_ACCEPTED.value: "circle-x",
    Reason.LOW_CONFIDENCE.value: "gauge", Reason.MILESTONE.value: "flag",
    Reason.UNVERIFIED.value: "scan-eye", Reason.BUDGET.value: "wallet",
}

_COLORS = {"reasoning": "#8E88B4", "tool": "#22D3EE", "result": "#A7F3D0",
           "marker": "#6F6A91", "error": "#FB7185"}


class _Stream:
    """Рассуждение одного агента как список окрашенных отрезков."""

    def __init__(self) -> None:
        self.segments: list[list[str]] = []    # [вид, текст]
        self.dirty = False

    def add(self, kind: str, text: str) -> None:
        if not text:
            return
        if self.segments and self.segments[-1][0] == kind:
            self.segments[-1][1] += text
        else:
            self.segments.append([kind, text])
        size = sum(len(s[1]) for s in self.segments)
        while size > STREAM_KEEP_CHARS and len(self.segments) > 1:
            size -= len(self.segments.pop(0)[1])
        if size > STREAM_KEEP_CHARS:
            self.segments[0][1] = "…" + self.segments[0][1][-STREAM_KEEP_CHARS:]
        self.dirty = True

    def reset(self) -> None:
        self.segments.clear()
        self.dirty = True

    def html(self) -> str:
        parts = []
        for kind, text in self.segments:
            body = html.escape(text).replace("\n", "<br>")
            if kind == "text":
                parts.append(body)
            elif kind == "reasoning":
                parts.append(f'<i><font color="{_COLORS["reasoning"]}">{body}</font></i>')
            else:
                parts.append(f'<font color="{_COLORS.get(kind, "#A6A1C4")}">{body}</font>')
        return "".join(parts)


class RunController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._streams_model = DictListModel(
            ["id", "name", "icon", "modelName", "status", "statusTitle", "phase", "subtask",
             "step", "maxSteps", "html", "lastTool", "tokens", "isSupervisor", "live"],
            parent=self)
        self._nodes = DictListModel(
            ["id", "title", "agentName", "status", "statusTitle", "level", "row",
             "reworks", "deps"], parent=self)
        self._edges = DictListModel(
            ["id", "source", "target", "fromLevel", "fromRow", "toLevel", "toRow", "state"],
            parent=self)
        self._feed = DictListModel(["id", "time", "agent", "tone", "kind", "message"],
                                   parent=self)
        self._approvals = DictListModel(
            ["id", "reason", "reasonTitle", "icon", "question", "details", "agent",
             "options", "created"], parent=self)
        self._streams: dict[int, _Stream] = defaultdict(_Stream)
        self._feed_seq = 0
        self._max_steps = 10
        self._flush = QTimer(self)
        self._flush.setInterval(STREAM_FLUSH_MS)
        self._flush.timeout.connect(self._flush_streams)
        self._set(taskTitle="", done=0, total=0, errors=0, review=0, progress=0.0,
                  canStart=False, blocker="", levels=0, maxRows=0, starting=False)

    # -- свойства -------------------------------------------------------------
    def _p(name, type_=str, default="", sig=changed):  # noqa: N805
        return Property(type_, lambda self: self._s.get(name, default), notify=sig)

    taskTitle = _p("taskTitle")
    done = _p("done", int, 0)
    total = _p("total", int, 0)
    errors = _p("errors", int, 0)
    review = _p("review", int, 0)
    progress = _p("progress", float, 0.0)
    canStart = _p("canStart", bool, False)
    blocker = _p("blocker")
    levels = _p("levels", int, 0)
    maxRows = _p("maxRows", int, 0)
    starting = _p("starting", bool, False)

    def _m(attr):  # noqa: N805
        return Property(QObject, lambda self: getattr(self, attr), constant=True)

    streams = _m("_streams_model")
    nodes = _m("_nodes")
    edges = _m("_edges")
    feed = _m("_feed")
    approvals = _m("_approvals")

    # -- данные ---------------------------------------------------------------
    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            self._set(taskTitle="", done=0, total=0, errors=0, review=0, progress=0.0,
                      canStart=False, blocker=tr("ws.empty"), levels=0, maxRows=0)
            self._nodes.clear()
            self._edges.clear()
            self._streams_model.clear()
            return
        ws = self.repos.workspaces.get(self.ws_id)
        if ws is not None:
            self._max_steps = int(ws.settings.get("agent_max_steps", 10) or 10)
        task = self.repos.tasks.current(self.ws_id)
        subtasks = self.repos.tasks.subtasks(task.id) if task else []
        agents = self.repos.agents.list(self.ws_id)
        names = {a.id: a.name for a in agents}

        blocker = ""
        if task is None or not task.description.strip():
            blocker = tr("run.no_task")
        elif not subtasks:
            blocker = tr("run.no_subtasks")
        elif any(not s.agent_id for s in subtasks if s.status != "done"):
            blocker = tr("run.unassigned_short")
        elif all(s.status == "done" for s in subtasks):
            blocker = tr("run.all_done")

        done = sum(1 for s in subtasks if s.status == "done")
        self._set(taskTitle=task.title if task else "", done=done, total=len(subtasks),
                  errors=sum(1 for s in subtasks if s.status == "error"),
                  review=sum(1 for s in subtasks if s.status == "review"),
                  progress=(done / len(subtasks)) if subtasks else 0.0,
                  blocker=blocker, canStart=not blocker and not self.backend.running)
        self._fill_graph(subtasks, names)
        self._fill_streams(agents, subtasks)
        self._sync_approvals()

    def _fill_graph(self, subtasks, names: dict[int, str]) -> None:
        deps = {s.id: [int(t) for t in (s.depends_on or "").split(",") if t.strip().isdigit()]
                for s in subtasks}
        ids = set(deps)
        level: dict[int, int] = {}

        def depth(sid: int, trail: frozenset[int]) -> int:
            if sid in level:
                return level[sid]
            parents = [d for d in deps.get(sid, []) if d in ids and d not in trail]
            value = 0 if not parents else 1 + max(depth(p, trail | {sid}) for p in parents)
            level[sid] = value
            return value

        rows: dict[int, int] = defaultdict(int)
        position: dict[int, tuple[int, int]] = {}
        nodes = []
        for s in subtasks:
            lv = depth(s.id, frozenset())
            row = rows[lv]
            rows[lv] += 1
            position[s.id] = (lv, row)
            nodes.append({"id": s.id, "title": s.title,
                          "agentName": names.get(s.agent_id or -1, tr("task.unassigned")),
                          "status": s.status, "statusTitle": status_title(s.status),
                          "level": lv, "row": row, "reworks": s.rework_count,
                          "deps": len(deps[s.id])})
        status = {s.id: s.status for s in subtasks}
        edges = []
        for sid, parents in deps.items():
            for p in parents:
                if p in position and sid in position:
                    edges.append({
                        "id": f"{p}-{sid}", "source": p, "target": sid,
                        "fromLevel": position[p][0], "fromRow": position[p][1],
                        "toLevel": position[sid][0], "toRow": position[sid][1],
                        "state": ("active" if status.get(sid) in ("running", "rework")
                                  else "done" if status.get(p) == "done" else "idle"),
                    })
        self._nodes.set_items(nodes)
        self._edges.set_items(edges)
        self._set(levels=(max(level.values()) + 1) if level else 0,
                  maxRows=max(rows.values()) if rows else 0)

    def _fill_streams(self, agents, subtasks) -> None:
        current = {s.agent_id: s.title for s in subtasks
                   if s.agent_id and s.status in ("running", "rework", "paused")}
        usage = {aid: t for aid, t, _ in self.repos.budgets.usage_by_agent(self.ws_id)}
        items = []
        for a in agents:
            if a.is_supervisor:
                continue
            old = self._streams_model.find(a.id)
            prev = self._streams_model.items[old] if old >= 0 else {}
            items.append({
                "id": a.id, "name": a.name, "icon": ROLE_ICONS.get(a.role or "custom", "bot"),
                "modelName": a.model, "status": a.status, "statusTitle": status_title(a.status),
                "phase": prev.get("phase", "idle"), "subtask": current.get(a.id, prev.get("subtask", "")),
                "step": prev.get("step", 0), "maxSteps": self._max_steps,
                "html": self._streams[a.id].html(), "lastTool": prev.get("lastTool", ""),
                "tokens": fmt_tokens(usage.get(a.id, 0)), "isSupervisor": False,
                "live": a.status == "running",
            })
        old = self._streams_model.find(SUPERVISOR_CARD)
        prev = self._streams_model.items[old] if old >= 0 else {}
        items.append({
            "id": SUPERVISOR_CARD, "name": tr("run.supervisor"), "icon": "shield-check",
            "modelName": self.backend.supervisor.modelShort, "status": prev.get("status", "idle"),
            "statusTitle": prev.get("statusTitle", status_title("idle")),
            "phase": prev.get("phase", "idle"), "subtask": prev.get("subtask", ""),
            "step": 0, "maxSteps": 0, "html": self._streams[SUPERVISOR_CARD].html(),
            "lastTool": "", "tokens": fmt_tokens(usage.get(None, 0)), "isSupervisor": True,
            "live": prev.get("live", False),
        })
        self._streams_model.set_items(items)

    def _sync_approvals(self) -> None:
        orch = self.backend.orchestrator
        gate = orch.gate if orch else None
        items = []
        for req in (gate.pending() if gate else []):
            items.append({
                "id": req.id, "reason": req.reason.value,
                "reasonTitle": tr(f"reason.{req.reason.value}"),
                "icon": REASON_ICONS.get(req.reason.value, "hand"),
                "question": req.question, "details": req.details,
                "agent": req.agent_name,
                "options": [{"value": d.value, "title": tr(f"decision.{d.value}"),
                             "tone": DECISION_TONES.get(d.value, "muted")} for d in req.options],
                "created": req.created_at,
            })
        self._approvals.set_items(items)

    def reset(self) -> None:
        super().reset()
        self._flush.stop()
        self._streams.clear()
        for model in (self._streams_model, self._nodes, self._edges, self._feed, self._approvals):
            model.clear()

    # -- события ----------------------------------------------------------------------
    def on_event(self, event: Event) -> None:
        kind = event.type
        if kind not in FEED_SKIP:
            self._append_feed(event)

        if kind is EventType.AGENT_DELTA:
            self._stream_for(event).add(event.payload.get("stream", "text"), event.message)
            self._ensure_flush()
            return
        if kind is EventType.RUN_STARTED:
            for stream in self._streams.values():
                stream.reset()
            self._set(starting=False)
            self._ensure_flush()
        if kind is EventType.SUBTASK_STARTED and event.agent_id:
            stream = self._streams[event.agent_id]
            stream.reset()
            stream.add("marker", f"{tr('run.subtask')}: {event.message}\n")
            self._streams_model.update_row(event.agent_id, subtask=event.message,
                                           phase="thinking", step=0, live=True)
            self._ensure_flush()
        elif kind is EventType.AGENT_THINKING and event.agent_id:
            step = int(event.payload.get("step", 0) or 0)
            if step > 1:
                self._streams[event.agent_id].add("marker", f"\n\n{tr('run.step')} {step}\n")
            self._streams_model.update_row(event.agent_id, step=step, phase="thinking")
            self._ensure_flush()
        elif kind is EventType.AGENT_THINKING and event.agent_name and not event.agent_id:
            self._supervisor_line(event.message, phase="review")
        elif kind is EventType.AGENT_TOOL_CALL and event.agent_id:
            tool = event.payload.get("tool", "")
            self._streams[event.agent_id].add("tool", f"\n⚙ {elide(event.message, 220)}\n")
            self._streams_model.update_row(event.agent_id, phase="tool", lastTool=tool)
            self._ensure_flush()
        elif kind is EventType.AGENT_TOOL_RESULT and event.agent_id:
            text = event.message.split("→", 1)[-1].strip()
            self._streams[event.agent_id].add("reasoning", f"↳ {elide(text, 200)}\n")
            self._streams_model.update_row(event.agent_id, phase="thinking")
            self._ensure_flush()
        elif kind is EventType.SUBTASK_FINISHED and event.agent_id:
            self._streams_model.update_row(event.agent_id, phase="done", live=False)
        elif kind is EventType.SUBTASK_FAILED and event.agent_id:
            self._streams[event.agent_id].add("error", f"\n✕ {event.message}\n")
            self._streams_model.update_row(event.agent_id, phase="error", live=False)
            self._ensure_flush()
        elif kind is EventType.REPORT_REVIEWED:
            self._supervisor_line(event.message, phase="idle",
                                  verdict=event.payload.get("verdict", ""))
        elif kind is EventType.SUMMARY_CREATED:
            self._supervisor_line(event.message, phase="idle")
        elif kind is EventType.ERROR and not event.agent_id and event.agent_name == SUPERVISOR_NAME:
            # Проверка или сводка сорвалась: карточка не должна «проверять» вечно.
            self._supervisor_line(event.message, phase="idle", verdict="unverified")
        elif kind is EventType.AGENT_STATUS and event.agent_id:
            status = event.payload.get("status", event.message)
            self._streams_model.update_row(event.agent_id, status=status,
                                           statusTitle=status_title(status),
                                           live=status == "running")
            if event.subtask_id:
                self._nodes.update_row(event.subtask_id, status=status,
                                       statusTitle=status_title(status))
                self._update_edges(event.subtask_id, status)

        if kind in (EventType.APPROVAL_REQUESTED, EventType.APPROVAL_RESOLVED,
                    EventType.RUN_FINISHED, EventType.RUN_STOPPED):
            self._sync_approvals()
        if kind in (EventType.SUBTASK_FINISHED, EventType.SUBTASK_FAILED,
                    EventType.REPORT_REVIEWED, EventType.RUN_STARTED,
                    EventType.RUN_FINISHED, EventType.APPROVAL_RESOLVED):
            self.refresh()
        if kind is EventType.RUN_FINISHED:
            self._supervisor_line("", phase="idle", live=False)
            for row in list(self._streams_model.items):
                self._streams_model.update_row(row["id"], live=False)

    def _update_edges(self, subtask_id: int, status: str) -> None:
        for edge in self._edges.items:
            if edge["target"] == subtask_id:
                state = "active" if status in ("running", "rework") else edge["state"]
                self._edges.update_row(edge["id"], state=state)

    def _stream_for(self, event: Event) -> _Stream:
        return self._streams[event.agent_id if event.agent_id else SUPERVISOR_CARD]

    def _supervisor_line(self, message: str, phase: str, verdict: str = "",
                         live: bool | None = None) -> None:
        if message:
            kind = {"ok": "result", "rework": "tool", "conflict": "error",
                    "unverified": "error"}.get(verdict, "reasoning" if phase == "review" else "text")
            self._streams[SUPERVISOR_CARD].add(kind, f"{message}\n")
            self._ensure_flush()
        working = phase == "review"
        self._streams_model.update_row(
            SUPERVISOR_CARD, phase=phase, live=working if live is None else live,
            status="running" if working else "idle",
            statusTitle=status_title("running" if working else "idle"))

    def _ensure_flush(self) -> None:
        if not self._flush.isActive():
            self._flush.start()

    def _flush_streams(self) -> None:
        idle = True
        for agent_id, stream in self._streams.items():
            if stream.dirty:
                stream.dirty = False
                idle = False
                self._streams_model.update_row(agent_id, html=stream.html())
        if idle and not self.backend.running:
            self._flush.stop()

    def _append_feed(self, event: Event) -> None:
        self._feed_seq += 1
        self._feed.append({
            "id": self._feed_seq, "time": event.time_short,
            "agent": event.agent_name or tr("run.system"),
            "tone": FEED_TONES.get(event.type, "muted"), "kind": event.type.value,
            "message": elide(event.message, 400),
        }, limit=FEED_LIMIT)

    # -- действия ---------------------------------------------------------------------
    @Slot()
    def start(self) -> None:
        orch = self.backend.orchestrator
        if orch is None or self.ws_id is None or orch.state.running:
            return
        self.refresh()
        if self._s.get("blocker"):
            self.toast("warning", tr("run.cannot_start"), self._s["blocker"])
            return
        task = self.repos.tasks.current(self.ws_id)
        self._set(starting=True, canStart=False)

        def done(state) -> None:
            self._set(starting=False)
            self.refresh()
            self.backend.dashboard.schedule()

        def failed(exc: Exception) -> None:
            self._set(starting=False)
            self.refresh()
            self.toast("error", tr("run.cannot_start"), error_text(exc))

        run_async(orch.run_task(self.ws_id, task.id), done, failed)

    @Slot()
    def togglePause(self) -> None:  # noqa: N802
        orch = self.backend.orchestrator
        if orch is None:
            return
        if orch.state.paused:
            orch.resume()
        else:
            orch.pause()

    @Slot()
    def stop(self) -> None:
        orch = self.backend.orchestrator
        if orch is not None:
            orch.stop()

    @Slot(int, str, str, result=bool)
    def decide(self, approval_id: int, decision: str, comment: str) -> bool:
        orch = self.backend.orchestrator
        gate = orch.gate if orch else None
        ok = bool(gate and gate.resolve(approval_id, decision, comment))
        self._sync_approvals()
        return ok

    @Slot()
    def clearFeed(self) -> None:  # noqa: N802
        self._feed.clear()

    @Slot(int, result=str)
    def fullText(self, agent_id: int) -> str:  # noqa: N802
        """Текст рассуждения без разметки - для копирования в буфер."""
        return "".join(t for _, t in self._streams[agent_id].segments)
````

### `ui/bridge/c_supervisor.py`

*187 строк*

````python
"""Супервайзер: сводки, инциденты и история решений человека."""

from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.config import DEFAULT_WORKSPACE_SETTINGS
from app.i18n import tr
from core.events import EventType
from core.hitl import parse_payload
from ui.bridge.core import Controller, as_int, error_text, when
from ui.bridge.listmodel import DictListModel
from utils.asyncutils import run_async

SEVERITY_TONES = {"low": "muted", "medium": "warning", "high": "error"}
DECISION_TONES = {"approve": "success", "rework": "warning", "skip": "muted",
                  "abort": "error", "extend": "accent", "cancelled": "muted", "": "accent"}


class SupervisorController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._summaries = DictListModel(["id", "when", "trigger", "triggerTitle",
                                         "recipients", "content"], parent=self)
        self._incidents = DictListModel(
            ["id", "kind", "kindTitle", "severity", "severityTitle", "tone", "status",
             "statusTitle", "open", "description", "resolution", "when"], parent=self)
        self._decisions = DictListModel(
            ["id", "reason", "reasonTitle", "decision", "decisionTitle", "tone",
             "question", "agent", "comment", "when"], parent=self)
        self._set(configured=False, modelTitle="", modelShort="", mode="api",
                  summarizing=False, openIncidents=0)

    def _p(name, type_=str, default="", sig=changed):  # noqa: N805
        return Property(type_, lambda self: self._s.get(name, default), notify=sig)

    configured = _p("configured", bool, False)
    modelTitle = _p("modelTitle")
    modelShort = _p("modelShort")
    mode = _p("mode")
    summarizing = _p("summarizing", bool, False)
    openIncidents = _p("openIncidents", int, 0)

    def _m(attr):  # noqa: N805
        return Property(QObject, lambda self: getattr(self, attr), constant=True)

    summaries = _m("_summaries")
    incidents = _m("_incidents")
    decisions = _m("_decisions")

    def _settings(self) -> dict:
        ws = self.repos.workspaces.get(self.ws_id) if self.ws_id else None
        return {**DEFAULT_WORKSPACE_SETTINGS, **(ws.settings if ws else {})}

    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            for m in (self._summaries, self._incidents, self._decisions):
                m.clear()
            self._set(configured=False, modelTitle="", modelShort="", openIncidents=0)
            return
        self._describe_model()
        triggers = {"timer": tr("sup.by_timer"), "event": tr("sup.by_event"),
                    "manual": tr("sup.by_hand"), "final": tr("sup.by_final")}
        self._summaries.set_items([
            {"id": s.id, "when": when(s.created_at), "trigger": s.trigger,
             "triggerTitle": triggers.get(s.trigger, s.trigger),
             "recipients": len([x for x in s.delivered_to.split(",") if x]),
             "content": s.content}
            for s in self.repos.reports.list_summaries(self.ws_id, limit=40)])

        incidents = self.repos.incidents.list(self.ws_id, limit=200)
        self._incidents.set_items([
            {"id": i.id, "kind": i.kind, "kindTitle": tr(f"kind.{i.kind}"),
             "severity": i.severity, "severityTitle": tr(f"sev.{i.severity}"),
             "tone": SEVERITY_TONES.get(i.severity, "warning"), "status": i.status,
             "statusTitle": tr(f"inc.{i.status}"), "open": i.status in ("open", "escalated"),
             "description": i.description, "resolution": i.resolution,
             "when": when(i.created_at)}
            for i in incidents])
        self._set(openIncidents=sum(1 for i in incidents if i.status in ("open", "escalated")))

        rows = self.repos.approvals.history(self.ws_id, limit=80)
        items = []
        for row in rows:
            payload = parse_payload(row.get("payload_json", "{}"))
            decision = row.get("decision", "")
            items.append({
                "id": row["id"], "reason": row["reason"],
                "reasonTitle": tr(f"reason.{row['reason']}"),
                "decision": decision,
                "decisionTitle": tr(f"hist.{decision or 'pending'}"),
                "tone": DECISION_TONES.get(decision, "muted"),
                "question": payload.get("question", ""),
                "agent": payload.get("agent_name", ""), "comment": row.get("comment", ""),
                "when": when(row.get("created_at")),
            })
        self._decisions.set_items(items)

    def _describe_model(self) -> None:
        s = self._settings()
        if s.get("supervisor_mode") == "local":
            model = s.get("supervisor_local_model", "")
            self._set(configured=bool(model), mode="local", modelShort=model,
                      modelTitle=tr("sup.model_local", model=model,
                                    url=s.get("supervisor_local_base_url", "")))
            return
        agent = None
        if s.get("supervisor_agent_id"):
            agent = self.repos.agents.get(as_int(s["supervisor_agent_id"]))
        if agent is None:
            agent = next((a for a in self.repos.agents.list(self.ws_id) if a.is_supervisor), None)
        if agent is None:
            self._set(configured=False, mode="api", modelShort="",
                      modelTitle=tr("sup.not_configured"))
            return
        self._set(configured=True, mode="api", modelShort=agent.model,
                  modelTitle=tr("sup.model_api", name=agent.name, model=agent.model))

    def reset(self) -> None:
        super().reset()
        for m in (self._summaries, self._incidents, self._decisions):
            m.clear()

    def on_event(self, event) -> None:
        if event.type in (EventType.SUMMARY_CREATED, EventType.INCIDENT_CREATED,
                          EventType.REPORT_REVIEWED, EventType.RUN_FINISHED,
                          EventType.APPROVAL_REQUESTED, EventType.APPROVAL_RESOLVED):
            self.refresh()

    @Slot()
    def makeSummary(self) -> None:  # noqa: N802
        """Сводка вручную - удобно освежить контекст агентов вне прогона."""
        if self.ws_id is None:
            return
        task = self.repos.tasks.current(self.ws_id)
        if task is None:
            self.toast("warning", tr("task.no_task"), "")
            return
        from core.budget import BudgetGuard
        from core.supervisor.supervisor import Supervisor

        bus = self.backend.bus
        # Ручная сводка тоже тратит деньги и подчиняется тем же лимитам.
        budget = BudgetGuard(self.repos, bus, self.ws_id, task.id, task.token_limit)
        blocked = budget.blocking_scope(None)
        if blocked is not None:
            self.toast("warning", tr("toast.summary_failed"), blocked.reason())
            return
        supervisor = Supervisor(self.repos, bus, self.ws_id, self._settings(), budget=budget)
        if not supervisor.available():
            self.toast("warning", tr("sup.not_configured"), "")
            return
        self._set(summarizing=True)

        async def job() -> str:
            try:
                return await supervisor.make_summary(task, trigger="manual")
            finally:
                await supervisor.aclose()

        def done(content: str) -> None:
            self._set(summarizing=False)
            if content:
                self.toast("success", tr("toast.summary_done"), "")
            elif supervisor.last_error:
                # Ошибка - это не «нечего пересказывать».
                self.toast("error", tr("toast.summary_failed"), supervisor.last_error)
            else:
                self.toast("info", tr("sup.nothing_to_summarize"), "")
            if self.ready:
                self.refresh()

        def failed(exc: Exception) -> None:
            self._set(summarizing=False)
            self.toast("error", tr("toast.summary_failed"), error_text(exc))

        run_async(job(), done, failed)

    @Slot(int, str)
    def resolveIncident(self, incident_id: int, text: str) -> None:  # noqa: N802
        self.repos.incidents.resolve(incident_id, "resolved",
                                     (text or "").strip() or tr("sup.closed_by_user"))
        self.refresh()
        self.backend.dashboard.schedule()
````

### `ui/bridge/c_dashboard.py`

*188 строк*

````python
"""Дашборд: метрики, прогресс, кривые расхода, агенты, лента и инциденты.

Во время прогона события идут пачками, поэтому перерисовка собирается
таймером не чаще раза в секунду; шаги рассуждений дашборд не интересуют.
"""

from __future__ import annotations

from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot

from app.i18n import tr
from core.events import EventType
from ui.bridge.c_agents import ROLE_ICONS
from ui.bridge.core import Controller, elide, fmt_money, fmt_tokens, status_title, when
from ui.bridge.listmodel import DictListModel

THROTTLE_MS = 1000
SERIES_LIMIT = 300
FEED_LIMIT = 40
STATUS_ORDER = ["done", "review", "rework", "running", "paused", "error", "idle"]
QUIET = {EventType.AGENT_THINKING, EventType.AGENT_DELTA, EventType.AGENT_TOOL_CALL,
         EventType.AGENT_TOOL_RESULT}


class DashboardController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._agents = DictListModel(["id", "name", "icon", "status", "statusTitle",
                                      "doing", "tokens", "cost", "share", "isSupervisor"],
                                     parent=self)
        self._feed = DictListModel(["id", "who", "when", "text", "tone", "badge",
                                    "confidence"], parent=self)
        self._incidents = DictListModel(["id", "kindTitle", "tone", "statusTitle",
                                         "description", "when"], parent=self)
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(THROTTLE_MS)
        self._timer.timeout.connect(self.refresh)
        self._set(agentsCount=0, done=0, total=0, tokens=0, tokensText="0", cost=0.0,
                  costText="$0", reworks=0, openIncidents=0, limitPct=-1.0,
                  taskTitle="", segments=[], costSeries=[], tokenSeries=[], bars=[],
                  supervisorShare=0.0)

    def _p(name, type_=str, default="", sig=changed):  # noqa: N805
        return Property(type_, lambda self: self._s.get(name, default), notify=sig)

    agentsCount = _p("agentsCount", int, 0)
    done = _p("done", int, 0)
    total = _p("total", int, 0)
    tokens = _p("tokens", float, 0.0)
    tokensText = _p("tokensText")
    cost = _p("cost", float, 0.0)
    costText = _p("costText")
    reworks = _p("reworks", int, 0)
    openIncidents = _p("openIncidents", int, 0)
    limitPct = _p("limitPct", float, -1.0)
    taskTitle = _p("taskTitle")
    supervisorShare = _p("supervisorShare", float, 0.0)
    segments = _p("segments", "QVariantList", [])
    costSeries = _p("costSeries", "QVariantList", [])
    tokenSeries = _p("tokenSeries", "QVariantList", [])
    bars = _p("bars", "QVariantList", [])

    def _m(attr):  # noqa: N805
        return Property(QObject, lambda self: getattr(self, attr), constant=True)

    agentsModel = _m("_agents")
    feed = _m("_feed")
    incidents = _m("_incidents")

    def schedule(self) -> None:
        if self.ready and not self._timer.isActive():
            self._timer.start()

    def on_event(self, event) -> None:
        if event.type not in QUIET:
            self.schedule()

    def reset(self) -> None:
        super().reset()
        self._timer.stop()
        for m in (self._agents, self._feed, self._incidents):
            m.clear()

    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            for m in (self._agents, self._feed, self._incidents):
                m.clear()
            self._set(agentsCount=0, done=0, total=0, tokens=0.0, tokensText="0",
                      cost=0.0, costText="$0", reworks=0, openIncidents=0, limitPct=-1.0,
                      taskTitle="", segments=[], costSeries=[], tokenSeries=[], bars=[],
                      supervisorShare=0.0)
            return
        ws_id = self.ws_id
        agents = self.repos.agents.list(ws_id)
        task = self.repos.tasks.current(ws_id)
        subtasks = self.repos.tasks.subtasks(task.id) if task else []
        tokens, cost = self.repos.budgets.workspace_totals(ws_id)
        counts = self.repos.budgets.incident_counts(ws_id)

        buckets = {k: 0 for k in STATUS_ORDER}
        for s in subtasks:
            buckets[s.status] = buckets.get(s.status, 0) + 1
        segments = [{"status": k, "title": status_title(k), "count": buckets[k]}
                    for k in STATUS_ORDER if buckets.get(k)]

        series = self.repos.budgets.usage_series(ws_id, SERIES_LIMIT)
        cost_acc = token_acc = 0.0
        cost_series, token_series = [], []
        for created, t, c in series:
            cost_acc += c
            token_acc += t
            label = when(created, "%H:%M")
            cost_series.append({"label": label, "value": round(cost_acc, 6)})
            token_series.append({"label": label, "value": token_acc})

        names = {a.id: a for a in agents}
        usage = self.repos.budgets.usage_by_agent(ws_id)
        total_tokens = sum(t for _, t, _ in usage) or 1
        bars = []
        for agent_id, t, c in usage:
            if not t:
                continue
            a = names.get(agent_id) if agent_id else None
            label = a.name if a else (tr("dash.supervisor_line") if agent_id is None
                                      else tr("dash.unknown_agent"))
            bars.append({"label": label, "value": t, "text": fmt_tokens(t),
                         "cost": fmt_money(c), "supervisor": agent_id is None})
        supervisor_tokens = sum(t for aid, t, _ in usage if aid is None)

        limit_pct = -1.0
        if task and task.token_limit:
            task_tokens, _ = self.repos.budgets.task_totals(task.id)
            limit_pct = min(task_tokens / task.token_limit, 9.99)

        self._set(agentsCount=len(agents), done=buckets.get("done", 0), total=len(subtasks),
                  tokens=float(tokens), tokensText=fmt_tokens(tokens), cost=float(cost),
                  costText=fmt_money(cost), reworks=sum(s.rework_count for s in subtasks),
                  openIncidents=counts.get("open", 0) + counts.get("escalated", 0),
                  limitPct=limit_pct, taskTitle=task.title if task else "",
                  segments=segments, costSeries=cost_series, tokenSeries=token_series,
                  bars=bars[:10], supervisorShare=supervisor_tokens / total_tokens)

        per_agent = {aid: (t, c) for aid, t, c in usage}
        doing = {s.agent_id: s.title for s in subtasks
                 if s.agent_id and s.status in ("running", "rework")}
        self._agents.set_items([
            {"id": a.id, "name": a.name, "icon": ROLE_ICONS.get(a.role or "custom", "bot"),
             "status": a.status, "statusTitle": status_title(a.status),
             "doing": doing.get(a.id, ""),
             "tokens": fmt_tokens(per_agent.get(a.id, (0, 0))[0]),
             "cost": fmt_money(per_agent.get(a.id, (0, 0.0))[1]),
             "share": per_agent.get(a.id, (0, 0))[0] / total_tokens,
             "isSupervisor": a.is_supervisor}
            for a in agents])
        self._fill_feed(names)
        self._incidents.set_items([
            {"id": i.id, "kindTitle": tr(f"kind.{i.kind}"),
             "tone": {"low": "muted", "medium": "warning", "high": "error"}.get(i.severity, "warning"),
             "statusTitle": tr(f"inc.{i.status}"), "description": elide(i.description, 160),
             "when": when(i.created_at)}
            for i in self.repos.incidents.list(ws_id, limit=FEED_LIMIT)])

    def _fill_feed(self, names: dict) -> None:
        entries = []
        verdicts = {"ok": ("dash.v_ok", "success"), "rework": ("dash.v_rework", "warning"),
                    "conflict": ("dash.v_conflict", "error"),
                    "unverified": ("dash.v_unverified", "error")}
        for r in self.repos.reports.list_reports(self.ws_id, limit=FEED_LIMIT):
            badge, tone = verdicts.get(r.review_verdict, ("", "muted"))
            agent = names.get(r.agent_id)
            entries.append({"id": f"r{r.id}", "who": agent.name if agent else tr("dash.unknown_agent"),
                            "when_raw": r.created_at, "when": when(r.created_at, "%H:%M:%S"),
                            "text": elide(r.content, 180), "tone": tone,
                            "badge": tr(badge) if badge else "",
                            "confidence": f"{r.confidence:.2f}" if r.confidence is not None else ""})
        for s in self.repos.reports.list_summaries(self.ws_id, limit=FEED_LIMIT):
            entries.append({"id": f"s{s.id}", "who": tr("dash.summary_line"),
                            "when_raw": s.created_at, "when": when(s.created_at, "%H:%M:%S"),
                            "text": elide(s.content, 180), "tone": "violet", "badge": "",
                            "confidence": ""})
        entries.sort(key=lambda e: e["when_raw"], reverse=True)
        for e in entries:
            e.pop("when_raw", None)
        self._feed.set_items(entries[:FEED_LIMIT])
````

### `ui/bridge/c_budget.py`

*121 строк*

````python
"""Бюджеты: лимиты по токенам и деньгам на проект, задачу и каждого агента."""

from __future__ import annotations

from PySide6.QtCore import Property, QObject, Signal, Slot

from app.i18n import tr
from core.budget import load_states
from core.events import EventType
from ui.bridge.core import Controller, fmt_money, fmt_tokens
from ui.bridge.listmodel import DictListModel

SCOPE_ICONS = {"workspace": "layers", "task": "list-checks", "agent": "bot"}


def parse_int(raw: str) -> int | None:
    raw = (raw or "").replace(" ", "").replace("_", "").strip()
    if not raw:
        return None
    try:
        value = int(float(raw))
    except ValueError:
        return None
    return value if value > 0 else None


def parse_money(raw: str) -> float | None:
    raw = (raw or "").replace(",", ".").replace("$", "").replace(" ", "").strip()
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError:
        return None
    return value if value > 0 else None


class BudgetController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._model = DictListModel(
            ["id", "scope", "scopeId", "scopeTitle", "icon", "name", "tokens", "cost",
             "tokenLimit", "costLimit", "threshold", "ratio", "exceeded", "isSet",
             "tokensText", "costText"], parent=self)
        self._set(alert="", alertTone="")

    alert = Property(str, lambda s: s._s.get("alert", ""), notify=changed)
    alertTone = Property(str, lambda s: s._s.get("alertTone", ""), notify=changed)

    def _get_model(self) -> QObject:
        return self._model

    model = Property(QObject, _get_model, constant=True)

    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            self._model.clear()
            return
        items = []
        for st in load_states(self.repos, self.ws_id):
            items.append({
                "id": f"{st.scope}:{st.scope_id}", "scope": st.scope, "scopeId": st.scope_id,
                "scopeTitle": tr(f"scope.{st.scope}"), "icon": SCOPE_ICONS.get(st.scope, "wallet"),
                "name": st.name, "tokens": st.tokens, "cost": st.cost,
                "tokenLimit": str(st.limit.token_limit) if st.limit.token_limit else "",
                "costLimit": f"{st.limit.cost_limit:g}" if st.limit.cost_limit else "",
                "threshold": float(st.limit.alert_threshold or 0.8),
                "ratio": float(st.ratio()), "exceeded": st.exceeded(),
                "isSet": st.limit.is_set, "tokensText": fmt_tokens(st.tokens),
                "costText": fmt_money(st.cost),
            })
        self._model.set_items(items)

    def reset(self) -> None:
        super().reset()
        self._model.clear()

    def on_event(self, event) -> None:
        if event.type in (EventType.BUDGET_ALERT, EventType.BUDGET_EXCEEDED,
                          EventType.BUDGET_EXTENDED):
            tone = {EventType.BUDGET_EXCEEDED: "error",
                    EventType.BUDGET_ALERT: "warning"}.get(event.type, "info")
            self._set(alert=event.message, alertTone=tone)
            self.refresh()
        elif event.type in (EventType.RUN_FINISHED, EventType.USAGE):
            # расход меняется во время прогона - но не чаще, чем пересчитает дашборд
            if event.type is EventType.RUN_FINISHED:
                self.refresh()

    @Slot(str, int, str, str, float, result=str)
    def save(self, scope: str, scope_id: int, token_limit: str, cost_limit: str,
             threshold: float) -> str:
        """Сохраняет лимит; пустые поля означают «без ограничения»."""
        tokens = parse_int(token_limit)
        cost = parse_money(cost_limit)
        if (token_limit or "").strip() and tokens is None:
            return tr("bud.bad_tokens")
        if (cost_limit or "").strip() and cost is None:
            return tr("bud.bad_cost")
        threshold = min(max(float(threshold or 0.8), 0.1), 1.0)
        if scope == "task":
            # Лимит токенов задачи живёт и в форме задачи - держим их в согласии.
            self.repos.tasks.update(scope_id, token_limit=tokens)
        if tokens is None and cost is None:
            self.repos.budgets.delete_limit(scope, scope_id)
        else:
            self.repos.budgets.upsert(scope, scope_id, tokens, cost, round(threshold, 2))
        # Идёт прогон - новый лимит действует сразу, а не со следующего запуска.
        orch = self.backend.orchestrator
        if orch is not None and orch.state.running and orch.budget is not None:
            orch.budget.reload_limits()
        self.refresh()
        self.backend.task.refresh()
        return ""

    @Slot()
    def dismissAlert(self) -> None:  # noqa: N802
        self._set(alert="", alertTone="")
````

### `ui/bridge/c_export.py`

*172 строк*

````python
"""Экспорт результата: формат с объяснением выбора, состав, путь сохранения."""

from __future__ import annotations

import asyncio
from pathlib import Path

from PySide6.QtCore import Property, Signal, Slot

from app.config import PATHS
from app.i18n import tr
from core.export.bundle import ExportOptions, collect, detect_format
from core.export.exporters import ExportError, export, suggest_filename
from ui.bridge.core import Controller, error_text
from utils.asyncutils import run_async

FORMATS = [("markdown", "file-text"), ("docx", "file-type"), ("pdf", "book-open"),
           ("zip", "file-archive")]
OPTIONS = ["results", "reports", "summaries", "incidents", "decisions", "stats",
           "files", "anon"]
DEFAULT_OPTIONS = {"results": True, "reports": False, "summaries": False,
                   "incidents": True, "decisions": False, "stats": True,
                   "files": True, "anon": False}


def human_size(size: int) -> str:
    value = float(size)
    for unit in ("B", "KB", "MB", "GB"):
        if value < 1024:
            return f"{value:.0f} {unit}"
        value /= 1024
    return f"{value:.1f} TB"


class ExportController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._bundle = None
        self._set(format="markdown", recommended="markdown", reason="", stats="",
                  path="", canExport=False, options=dict(DEFAULT_OPTIONS),
                  lastPath="", lastInfo="", exporting=False, nothing=True)

    def _p(name, type_=str, default="", sig=changed):  # noqa: N805
        return Property(type_, lambda self: self._s.get(name, default), notify=sig)

    format = _p("format")
    recommended = _p("recommended")
    reason = _p("reason")
    stats = _p("stats")
    path = _p("path")
    canExport = _p("canExport", bool, False)
    options = _p("options", "QVariantMap", {})
    lastPath = _p("lastPath")
    lastInfo = _p("lastInfo")
    exporting = _p("exporting", bool, False)
    nothing = _p("nothing", bool, True)

    def _formats(self) -> list[dict]:
        return [{"key": k, "title": tr(f"exp.f_{k}"), "hint": tr(f"exp.fh_{k}"), "icon": icon}
                for k, icon in FORMATS]

    formats = Property("QVariantList", _formats, notify=changed)

    def _option_list(self) -> list[dict]:
        return [{"key": k, "title": tr(f"exp.opt_{k}")} for k in OPTIONS]

    optionList = Property("QVariantList", _option_list, notify=changed)

    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            self._bundle = None
            self._set(canExport=False, stats="", reason="", nothing=True)
            return
        try:
            self._bundle = collect(self.repos, self.ws_id)
        except ValueError as exc:
            self._bundle = None
            self._set(canExport=False, reason=str(exc), nothing=True)
            return
        b = self._bundle
        done = sum(1 for s in b.subtasks if s.result.strip())
        nothing = done == 0 and not b.files
        fmt, reason = detect_format(b)
        self._set(stats=tr("exp.stats", results=done, total=len(b.subtasks),
                           files=len(b.files), reports=len(b.reports)),
                  recommended=fmt, reason=reason, nothing=nothing,
                  canExport=not nothing)
        self.setFormat(fmt)

    def reset(self) -> None:
        super().reset()
        self._bundle = None
        self._set(format="markdown", options=dict(DEFAULT_OPTIONS), lastPath="", lastInfo="")

    @Slot(str)
    def setFormat(self, fmt: str) -> None:  # noqa: N802
        if fmt not in dict(FORMATS):
            return
        path = ""
        if self._bundle is not None:
            PATHS.ensure()
            path = str(PATHS.exports_dir / suggest_filename(self._bundle, fmt))
        self._set(format=fmt, path=path)

    @Slot(str, bool)
    def setOption(self, key: str, value: bool) -> None:  # noqa: N802
        options = dict(self._s.get("options", DEFAULT_OPTIONS))
        options[key] = bool(value)
        self._set(options=options)

    @Slot(str)
    def setPath(self, path: str) -> None:  # noqa: N802
        self._set(path=(path or "").strip())

    @Slot()
    def browse(self) -> None:
        from PySide6.QtWidgets import QFileDialog

        current = self._s.get("path") or str(PATHS.exports_dir)
        chosen, _ = QFileDialog.getSaveFileName(None, tr("exp.output"), current)
        if chosen:
            self._set(path=chosen)

    @Slot()
    def exportNow(self) -> None:  # noqa: N802
        if self._bundle is None or self._s.get("exporting") or self.ws_id is None:
            return
        raw = (self._s.get("path") or "").strip()
        if not raw:
            self.toast("warning", tr("exp.no_path"), "")
            return
        o = self._s.get("options", DEFAULT_OPTIONS)
        fmt = self._s.get("format", "markdown")
        options = ExportOptions(
            include_results=o.get("results", True), include_reports=o.get("reports", False),
            include_summaries=o.get("summaries", False),
            include_incidents=o.get("incidents", True),
            include_decisions=o.get("decisions", False),
            include_files=o.get("files", True) and fmt == "zip",
            include_stats=o.get("stats", True), anonymize=o.get("anon", False))
        repos, ws_id, target = self.repos, self.ws_id, Path(raw).expanduser()
        self._set(exporting=True)

        def job():
            # Данные собираются заново: с момента открытия экрана агенты
            # могли дописать результаты. Сборка DOCX/PDF занимает секунды -
            # в отдельном потоке, чтобы окно не замирало.
            bundle = collect(repos, ws_id)
            return export(bundle, options, fmt, target)

        def done(result) -> None:
            self._set(exporting=False)
            info = f"{result.path.name} · {human_size(result.size)}"
            if result.note:
                info += f" · {result.note}"
            self._set(lastPath=str(result.path), lastInfo=info)
            self.toast("success", tr("toast.exported"), info)

        def failed(exc: Exception) -> None:
            self._set(exporting=False)
            text = str(exc) if isinstance(exc, ExportError) else error_text(exc)
            self.toast("error", tr("toast.export_failed"), text)

        run_async(asyncio.to_thread(job), done, failed)

    @Slot()
    def openFolder(self) -> None:  # noqa: N802
        if self._s.get("lastPath"):
            self.backend.openPath(self._s["lastPath"])
````

### `ui/bridge/c_prefs.py`

*154 строк*

````python
"""Настройки воркспейса: human-in-the-loop, супервайзер, выполнение, инструменты,
песочница, доступные каталоги и безопасность профиля."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Property, Signal, Slot

from app.config import DEFAULT_WORKSPACE_SETTINGS
from app.i18n import tr
from core.tools.base import TOOL_GROUPS
from core.tools.sandbox import docker_available_async
from ui.bridge.core import Controller
from utils.asyncutils import run_async

#: допустимые диапазоны числовых настроек: (минимум, максимум)
RANGES = {
    "hitl_confidence_threshold": (0.0, 1.0),
    "summary_interval_minutes": (0, 600),
    "agent_max_steps": (1, 50),
    "max_rework_rounds": (0, 10),
    "max_parallel_agents": (1, 32),
    "sandbox_timeout_sec": (5, 600),
    "sandbox_memory_mb": (64, 8192),
}
#: группы инструментов, которые можно включать на уровне воркспейса
TOOL_SWITCHES = ["web_search", "files", "code_exec"]


class PrefsController(Controller):
    changed = Signal()

    def __init__(self, backend) -> None:
        super().__init__(backend)
        self._set(ws={}, supervisorOptions=[], docker="unknown", hasSearchKey=False)

    ws = Property("QVariantMap", lambda s: s._s.get("ws", {}), notify=changed)
    supervisorOptions = Property("QVariantList", lambda s: s._s.get("supervisorOptions", []),
                                 notify=changed)
    docker = Property(str, lambda s: s._s.get("docker", "unknown"), notify=changed)
    hasSearchKey = Property(bool, lambda s: s._s.get("hasSearchKey", False),
                            notify=changed)

    def _tool_switches(self) -> list[dict]:
        return [{"key": k, "title": tr(f"toolgroup.{k}")} for k in TOOL_SWITCHES]

    toolSwitches = Property("QVariantList", _tool_switches, notify=changed)

    def _settings(self) -> dict:
        ws = self.repos.workspaces.get(self.ws_id) if self.ws_id else None
        return {**DEFAULT_WORKSPACE_SETTINGS, **(ws.settings if ws else {})}

    @Slot()
    def refresh(self) -> None:
        if not self.ready or self.ws_id is None:
            self._set(ws={}, supervisorOptions=[], hasSearchKey=False)
            return
        s = self._settings()
        view = {k: v for k, v in s.items() if k != "search_api_key"}
        view["tools_enabled"] = self._groups(s.get("tools_enabled") or [])
        view["extra_allowed_paths"] = [str(p) for p in s.get("extra_allowed_paths") or []]
        view["supervisor_agent_id"] = int(s.get("supervisor_agent_id") or -1)
        options = [{"id": -1, "title": tr("prefs.sup_auto")}] + [
            {"id": a.id, "title": f"{a.name} · {a.model}"}
            for a in self.repos.agents.list(self.ws_id)]
        self._set(ws=view, supervisorOptions=options,
                  hasSearchKey=bool(s.get("search_api_key")))
        if self._s.get("docker") == "unknown":
            self.checkDocker()

    @staticmethod
    def _groups(names: list[str]) -> list[str]:
        """Настройка хранит смесь групп и имён инструментов - приводим к группам."""
        groups = []
        for group in TOOL_SWITCHES:
            members = TOOL_GROUPS.get(group, [group])
            if group in names or any(m in names for m in members):
                groups.append(group)
        return groups

    def _save(self, **changes) -> None:
        s = self._settings()
        s.update(changes)
        self.repos.workspaces.update(self.ws_id, settings=s)
        self.refresh()

    @Slot(str, "QVariant")
    def setValue(self, key: str, value) -> None:  # noqa: N802
        if self.ws_id is None or key not in DEFAULT_WORKSPACE_SETTINGS or key == "search_api_key":
            return
        default = DEFAULT_WORKSPACE_SETTINGS[key]
        if key == "supervisor_agent_id":
            value = int(value) if value is not None and int(value) >= 0 else None
        elif isinstance(default, bool):
            value = bool(value)
        elif isinstance(default, int):
            value = int(round(float(value)))
        elif isinstance(default, float):
            value = round(float(value), 2)
        elif isinstance(default, str):
            value = str(value or "").strip()
        if key in RANGES and isinstance(value, (int, float)):
            low, high = RANGES[key]
            value = min(max(value, low), high)
        self._save(**{key: value})
        if key.startswith("supervisor"):
            self.backend.supervisor.refresh()

    @Slot(str, bool)
    def setTool(self, group: str, enabled: bool) -> None:  # noqa: N802
        groups = set(self._s.get("ws", {}).get("tools_enabled", []))
        if enabled:
            groups.add(group)
        else:
            groups.discard(group)
        self._save(tools_enabled=[g for g in TOOL_SWITCHES if g in groups])

    @Slot(str)
    def setSearchKey(self, secret: str) -> None:  # noqa: N802
        """Ключ Tavily/Brave хранится зашифрованным мастер-ключом профиля."""
        self._save(search_api_key=self.repos.secrets.seal((secret or "").strip()))
        self.toast("success" if secret else "info",
                   tr("toast.search_key_saved") if secret else tr("toast.search_key_removed"), "")

    @Slot()
    def addPath(self) -> None:  # noqa: N802
        from PySide6.QtWidgets import QFileDialog

        folder = QFileDialog.getExistingDirectory(None, tr("prefs.add_path"), str(Path.home()))
        if folder:
            paths = list(self._s.get("ws", {}).get("extra_allowed_paths", []))
            if folder not in paths:
                paths.append(folder)
                self._save(extra_allowed_paths=paths)

    @Slot(str)
    def removePath(self, path: str) -> None:  # noqa: N802
        paths = [p for p in self._s.get("ws", {}).get("extra_allowed_paths", []) if p != path]
        self._save(extra_allowed_paths=paths)

    @Slot()
    def checkDocker(self) -> None:  # noqa: N802
        self._set(docker="checking")
        run_async(docker_available_async(),
                  lambda ok: self._set(docker="yes" if ok else "no"),
                  lambda exc: self._set(docker="no"))

    @Slot(str, str, str, result=str)
    def changePassword(self, old: str, new1: str, new2: str) -> str:  # noqa: N802
        error = self.backend.change_password(old, new1, new2)
        if not error:
            self.toast("success", tr("toast.password_changed"), tr("toast.password_changed_text"))
        return error
````

### `app/i18n_ui.py`

*565 строк*

````python
"""Строки интерфейса версии 1.1 (Qt Quick).

Вынесены отдельно от ``i18n.py``, чтобы словари не разрастались в один
нечитаемый файл. При импорте ``app.i18n`` они вливаются в общие каталоги.
"""

from __future__ import annotations

RU_UI: dict[str, str] = {
    # --- общее ---
    "common.copy": "Копировать",
    # --- статусы (дополнение) ---
    "status.stopped": "Остановлено",
    "status.failed": "С ошибками",
    "status.draft": "Черновик",
    # --- вход ---
    "login.tagline": "Команда ИИ-агентов под контролем супервайзера. Независимая проверка результатов, пауза для вашего решения и контроль расходов.",
    "login.f1": "Агенты работают параллельно и не видят переписку друг друга",
    "login.f2": "Супервайзер проверяет каждый отчёт и ищет противоречия",
    "login.f3": "Ключи зашифрованы, данные не покидают этот компьютер",
    "login.have_profile": "У меня уже есть профиль",
    "login.local": "данные хранятся локально",
    "login.need_username": "Введите имя профиля",
    "login.s0": "", "login.s1": "слабый", "login.s2": "средний", "login.s3": "хороший",
    "login.s4": "надёжный",
    # --- навигация ---
    "nav.g_project": "Проект",
    "nav.g_work": "Работа",
    "nav.g_resources": "Ресурсы",
    "nav.local_profile": "локальный профиль",
    "nav.search": "Переход и команды",
    "top.no_ws": "Воркспейс не выбран",
    "top.running": "Идёт прогон",
    "top.paused": "На паузе",
    "top.pending": "Ждут вашего решения: {n}",
    "palette.title": "Быстрый переход",
    "palette.placeholder": "Страница или действие…",
    "palette.page": "страница",
    "palette.action": "действие",
    "palette.start": "Запустить агентов",
    "palette.motion": "Переключить уровень анимаций",
    # --- воркспейсы ---
    "ws.subtitle": "Параллельные проекты: у каждого свои агенты, задача, файлы и настройки",
    "ws.empty_title": "Нет ни одного воркспейса",
    "ws.edit": "Изменить воркспейс",
    "ws.active": "активный",
    "ws.updated": "изменён {when}",
    "ws.no_description": "Без описания",
    "ws.desc_placeholder": "Коротко: о чём проект и для кого результат",
    "ws.delete_title": "Удалить воркспейс?",
    "ws.need_name": "Введите название проекта",
    # --- ключи ---
    "keys.empty_title": "Ключей пока нет",
    "keys.edit": "Изменить ключ",
    "keys.free": "бесплатно",
    "keys.local": "локально",
    "keys.stored": "ключ сохранён",
    "keys.no_secret": "без ключа",
    "keys.models_cached": "моделей в кэше: {n}",
    "keys.testing": "Проверяю соединение…",
    "keys.get_key": "Где взять ключ",
    "keys.keep_secret": "оставьте пустым, чтобы не менять",
    "keys.encrypted_note": "Ключ шифруется AES-256-GCM и не хранится открытым текстом",
    "keys.delete_title": "Удалить ключ?",
    "keys.need_secret": "Этому провайдеру нужен API-ключ",
    "keys.need_url": "Укажите адрес сервера (Base URL)",
    "keys.not_found": "Ключ не найден",
    # --- агенты ---
    "agents.edit": "Изменить агента",
    "agents.empty_title": "Агентов пока нет",
    "agents.no_keys_title": "Сначала нужен API-ключ",
    "agents.no_prompt": "Системный промпт не задан",
    "agents.duplicate": "Дублировать",
    "agents.delete_title": "Удалить агента?",
    "agents.tools": "Инструменты",
    "agents.is_supervisor": "Может быть супервайзером",
    "agents.is_supervisor_hint": "Помеченный агент проверяет отчёты, если в настройках не выбран другой",
    "agents.key_missing": "ключ удалён",
    "agents.free": "бесплатно",
    "agents.need_name": "Введите имя агента",
    "agents.need_key": "Выберите API-ключ",
    "agents.need_model": "Укажите модель",
    "tool.web_search": "Веб-поиск",
    "tool.fetch_url": "Чтение страниц",
    "tool.read_file": "Чтение файлов",
    "tool.write_file": "Запись файлов",
    "tool.list_dir": "Список файлов",
    "tool.code_exec": "Запуск кода",
    "toolgroup.web_search": "Веб-поиск и страницы",
    "toolgroup.files": "Файлы проекта",
    "toolgroup.code_exec": "Запуск кода",
    # --- задача ---
    "task.subtitle": "Сформулируйте задачу и разложите её на подзадачи вручную или с помощью ИИ",
    "task.statement": "Постановка",
    "task.untitled": "Без названия",
    "task.token_limit_note": "Проверяется перед каждым вызовом модели, включая проверки супервайзера",
    "task.subtasks_hint": "Зависимости задают порядок: результат предшественника уходит исполнителю как исходный материал",
    "task.no_subtasks_title": "Подзадач пока нет",
    "task.no_subtasks": "Добавьте их вручную или нажмите «Разбить автоматически»",
    "task.edit_subtask": "Изменить подзадачу",
    "task.delete_subtask": "Удалить подзадачу?",
    "task.depends_on": "Зависит от",
    "task.depends_hint": "Подзадача стартует только после того, как выбранные будут приняты",
    "task.no_deps_possible": "Других подзадач пока нет",
    "task.reworks": "доработок: {n}",
    "task.rerun": "Выполнить заново",
    "task.new_task": "Новая задача",
    "task.new_task_confirm": "Текущая задача останется в истории, а форма очистится для новой. Продолжить?",
    "task.need_body": "Опишите задачу: без формулировки агентам не с чем работать",
    "task.bad_limit": "Лимит токенов должен быть целым положительным числом",
    "task.save_first": "Сначала сохраните задачу",
    "task.need_subtask_title": "Опишите, что нужно сделать",
    "task.dep_cycle": "Такая зависимость замкнёт подзадачи в цикл",
    "fmt.auto": "Авто", "fmt.markdown": "Markdown", "fmt.docx": "DOCX", "fmt.pdf": "PDF",
    "fmt.zip": "ZIP",
    # --- выполнение ---
    "run.no_task": "Сначала поставьте задачу на вкладке «Задача»",
    "run.unassigned_short": "Не у всех подзадач назначен исполнитель",
    "run.all_done": "Все подзадачи выполнены. Чтобы повторить, верните нужные в очередь на вкладке «Задача»",
    "run.cannot_start": "Прогон не запущен",
    "run.k_done": "готово",
    "run.k_review": "на проверке",
    "run.k_errors": "ошибок",
    "run.k_time": "время",
    "run.k_tokens": "токенов",
    "run.k_cost": "стоимость",
    "run.live": "Рассуждения агентов",
    "run.live_hint": "Текст модели появляется по мере генерации; курсивом - внутреннее рассуждение, голубым - вызовы инструментов",
    "run.graph": "Граф подзадач",
    "run.graph_empty": "Подзадач пока нет",
    "run.feed_empty": "Событий пока нет",
    "run.f_all": "Все",
    "run.f_key": "Важные",
    "run.f_errors": "Ошибки",
    "run.show_details": "Подробности",
    "run.hide_details": "Скрыть",
    "run.comment_placeholder": "Комментарий исполнителю (необязательно)",
    "run.ph_idle": "ожидает",
    "run.ph_thinking": "думает",
    "run.ph_tool": "инструмент",
    "run.ph_review": "проверяет",
    "run.ph_done": "готово",
    "run.ph_error": "ошибка",
    "run.step_of": "шаг {n} из {m}",
    "run.step": "Шаг",
    "run.subtask": "Подзадача",
    "run.waiting": "Ждёт подзадачу",
    "run.stream_empty": "Рассуждение появится, когда агент начнёт работу",
    "run.sup_empty": "Здесь будут проверки и сводки супервайзера",
    "run.copy_stream": "Скопировать рассуждение",
    "run.to_latest": "К последнему",
    "run.supervisor": "Супервайзер",
    "run.system": "Система",
    "reason.conflict": "Конфликт данных",
    "reason.not_accepted": "Результат не принят",
    "reason.low_confidence": "Низкая уверенность",
    "reason.milestone": "Завершён этап",
    "reason.unverified": "Результат не проверен",
    "reason.budget": "Исчерпан лимит бюджета",
    "decision.approve": "Принять",
    "decision.rework": "На доработку",
    "decision.skip": "Пропустить",
    "decision.abort": "Остановить прогон",
    "decision.extend": "Поднять лимит на 50%",
    # --- супервайзер ---
    "sup.checklist": "Проверяет каждый отчёт: соответствие заданию, логика, факты, согласованность с проектом",
    "sup.configure_hint": "Выберите агента-супервайзера или локальную модель в настройках",
    "sup.mode_api": "через API",
    "sup.mode_local": "локально",
    "sup.no_summaries_title": "Сводок пока нет",
    "sup.no_incidents_title": "Инцидентов нет",
    "sup.no_approvals_title": "Решений пока не было",
    "sup.closed_by_user": "Закрыто пользователем",
    "kind.conflict": "Конфликт данных",
    "kind.factual_error": "Фактическая ошибка",
    "kind.contradiction": "Противоречие",
    "kind.off_scope": "Выход за рамки задания",
    "kind.unverified": "Не проверено",
    "sev.low": "низкая", "sev.medium": "средняя", "sev.high": "высокая",
    "inc.open": "открыт", "inc.escalated": "требует решения",
    "inc.auto_resolved": "разрешён автоматически", "inc.resolved": "закрыт",
    "hist.approve": "принято", "hist.rework": "на доработку", "hist.skip": "пропущено",
    "hist.abort": "прогон остановлен", "hist.extend": "лимит поднят",
    "hist.cancelled": "снято без решения", "hist.pending": "ожидает решения",
    # --- дашборд ---
    "dash.m_tokens_pct": "токенов · {pct}% от лимита задачи",
    "dash.spend": "Расход нарастающим итогом",
    "dash.money": "Деньги",
    "dash.tokens": "Токены",
    "dash.sup_share": "супервайзер {pct}%",
    "dash.v_unverified": "не проверено",
    # --- бюджеты ---
    "bud.h_before": "Лимит проверяется до вызова модели, а не после: лишний запрос просто не уходит",
    "bud.h_ask": "С включённым human-in-the-loop система спросит, поднять ли лимит, вместо того чтобы оборвать работу",
    "bud.h_log": "Расход считается по журналу вызовов, поэтому перезапуск приложения его не обнуляет",
    "bud.nothing_title": "Ограничивать пока нечего",
    "bud.tokens_short": "ток.",
    "bud.bad_tokens": "Лимит токенов должен быть целым положительным числом",
    "bud.bad_cost": "Лимит стоимости должен быть положительным числом",
    "scope.workspace": "проект",
    "scope.task": "задача",
    "scope.agent": "агент",
    # --- экспорт ---
    "exp.recommended": "рекомендуем",
    "exp.f_markdown": "Markdown", "exp.f_docx": "Word", "exp.f_pdf": "PDF", "exp.f_zip": "ZIP-архив",
    "exp.fh_markdown": "Лёгкий текст для заметок, вики и репозиториев",
    "exp.fh_docx": "Документ для отчёта, который будут читать и править",
    "exp.fh_pdf": "Готовый к отправке документ с кириллицей",
    "exp.fh_zip": "Отчёт, манифест и все файлы проекта со структурой",
    # --- настройки ---
    "settings.subtitle": "Интерфейс и настройки активного воркспейса",
    "settings.interface": "Интерфейс",
    "settings.motion": "Анимации",
    "settings.motion_hint": "Полные: живой фон и выразительные переходы. Сдержанные: только короткие переходы. Выключены: интерфейс без движения",
    "settings.motion_full": "Полные",
    "settings.motion_reduced": "Сдержанные",
    "settings.motion_off": "Выключены",
    "settings.hitl_title": "Решения человека",
    "settings.hitl_hint": "Система останавливается в критических точках и ждёт вашего решения",
    "settings.never": "никогда",
    "settings.supervisor_agent": "Агент-супервайзер",
    "settings.sup_api_short": "Агент с API-ключом",
    "settings.sup_local_short": "Локальная модель",
    "settings.local_model": "Локальная модель",
    "settings.off": "выкл.",
    "settings.min": "мин",
    "settings.summary_cost_hint": "Сводки после каждой подзадачи заметно увеличивают расход токенов",
    "settings.anonymize": "Анонимные сводки",
    "settings.anonymize_hint": "Агенты получают пересказ без указания, кто что написал",
    "settings.execution": "Выполнение",
    "settings.max_steps": "Шагов на подзадачу",
    "settings.rework_rounds": "Автоматических доработок",
    "settings.parallel": "Агентов одновременно",
    "settings.tools": "Инструменты",
    "settings.tools_hint": "Что вообще разрешено агентам этого воркспейса. Конкретному агенту можно сузить набор в его карточке",
    "settings.search_backend": "Поисковый сервис",
    "settings.search_key": "Ключ поискового API",
    "settings.search_key_set": "ключ сохранён, введите новый, чтобы заменить",
    "settings.fetch_pages": "Разрешить открывать найденные страницы",
    "settings.sb_auto": "Авто",
    "settings.sb_process": "Процесс",
    "settings.sb_timeout": "Таймаут",
    "settings.sb_memory": "Память",
    "settings.docker_yes": "Docker доступен",
    "settings.docker_no": "Docker не найден",
    "settings.docker_recheck": "Проверить снова",
    "settings.docker_note_yes": "Код агентов выполняется в контейнере без сети, с корнем только для чтения",
    "settings.docker_note_no": "Код выполняется отдельным процессом: окружение очищено, но файловая система не изолирована. Для строгой изоляции установите Docker",
    "settings.paths_warning": "Агенты получают доступ на чтение и запись в эти каталоги. Не добавляйте системные папки и каталоги с личными данными",
    "settings.paths_empty": "Агентам доступен только рабочий каталог воркспейса",
    "settings.security": "Безопасность и данные",
    "settings.security_text": "API-ключи зашифрованы AES-256-GCM. Ключ шифрования выводится из пароля профиля функцией Argon2id и существует только в оперативной памяти",
    "settings.open_data": "Открыть каталог данных",
    "settings.old_password": "Текущий пароль",
    "settings.password_note": "Все API-ключи будут перешифрованы новым паролем",
    "prefs.sup_auto": "Автоматически (агент со звёздочкой)",
    "prefs.add_path": "Выберите каталог",
    # --- уведомления ---
    "toast.profile_created": "Профиль создан",
    "toast.recovered": "Прошлый сеанс завершился аварийно",
    "toast.recovered_text": "Статусы незавершённого прогона приведены в порядок, его можно запустить снова",
    "toast.run_active": "Идёт прогон",
    "toast.run_active_text": "Дождитесь завершения или остановите прогон",
    "toast.not_found": "Путь не найден",
    "toast.copied": "Скопировано в буфер обмена",
    "toast.run_done": "Прогон завершён",
    "toast.run_failed": "Прогон завершён с ошибками",
    "toast.run_review": "Прогон завершён, нужны ваши решения",
    "toast.run_stopped": "Прогон остановлен",
    "toast.need_decision": "Нужно ваше решение",
    "toast.budget_alert": "Бюджет подходит к лимиту",
    "toast.budget_exceeded": "Лимит бюджета исчерпан",
    "toast.budget_extended": "Лимит поднят",
    "toast.subtask_failed": "Подзадача не выполнена",
    "toast.ws_created": "Воркспейс создан",
    "toast.ws_deleted": "Воркспейс удалён",
    "toast.key_saved": "Ключ сохранён",
    "toast.key_deleted": "Ключ удалён",
    "toast.agent_created": "Агент создан",
    "toast.agent_saved": "Агент сохранён",
    "toast.agent_deleted": "Агент удалён",
    "toast.task_saved": "Задача сохранена",
    "toast.planned": "Задача разбита",
    "toast.planned_n": "Подзадач: {n}. Проверьте исполнителей и зависимости",
    "toast.plan_failed": "Не удалось разбить задачу",
    "toast.summary_done": "Сводка составлена и разослана",
    "toast.summary_failed": "Сводка не составлена",
    "toast.exported": "Экспорт готов",
    "toast.export_failed": "Экспорт не удался",
    "toast.search_key_saved": "Ключ поиска сохранён",
    "toast.search_key_removed": "Ключ поиска удалён",
    "toast.password_changed": "Пароль изменён",
    "toast.password_changed_text": "API-ключи перешифрованы новым паролем",
}

EN_UI: dict[str, str] = {
    "common.copy": "Copy",
    "status.stopped": "Stopped",
    "status.failed": "Failed",
    "status.draft": "Draft",
    "login.tagline": "A team of AI agents under a supervisor. Independent review of results, pauses for your decision and cost control.",
    "login.f1": "Agents work in parallel and never see each other's chats",
    "login.f2": "The supervisor reviews every report and looks for contradictions",
    "login.f3": "Keys are encrypted, data never leaves this computer",
    "login.have_profile": "I already have a profile",
    "login.local": "data is stored locally",
    "login.need_username": "Enter a profile name",
    "login.s0": "", "login.s1": "weak", "login.s2": "fair", "login.s3": "good", "login.s4": "strong",
    "nav.g_project": "Project",
    "nav.g_work": "Work",
    "nav.g_resources": "Resources",
    "nav.local_profile": "local profile",
    "nav.search": "Go to and commands",
    "top.no_ws": "No workspace selected",
    "top.running": "Run in progress",
    "top.paused": "Paused",
    "top.pending": "Awaiting your decision: {n}",
    "palette.title": "Quick switch",
    "palette.placeholder": "Page or action…",
    "palette.page": "page",
    "palette.action": "action",
    "palette.start": "Run agents",
    "palette.motion": "Toggle animation level",
    "ws.subtitle": "Parallel projects, each with its own agents, task, files and settings",
    "ws.empty_title": "No workspaces yet",
    "ws.edit": "Edit workspace",
    "ws.active": "active",
    "ws.updated": "updated {when}",
    "ws.no_description": "No description",
    "ws.desc_placeholder": "In short: what the project is about and who needs the result",
    "ws.delete_title": "Delete workspace?",
    "ws.need_name": "Enter a project name",
    "keys.empty_title": "No keys yet",
    "keys.edit": "Edit key",
    "keys.free": "free",
    "keys.local": "local",
    "keys.stored": "key stored",
    "keys.no_secret": "no key",
    "keys.models_cached": "models cached: {n}",
    "keys.testing": "Testing connection…",
    "keys.get_key": "Where to get a key",
    "keys.keep_secret": "leave empty to keep the current key",
    "keys.encrypted_note": "The key is encrypted with AES-256-GCM and never stored in plain text",
    "keys.delete_title": "Delete key?",
    "keys.need_secret": "This provider needs an API key",
    "keys.need_url": "Enter the server address (Base URL)",
    "keys.not_found": "Key not found",
    "agents.edit": "Edit agent",
    "agents.empty_title": "No agents yet",
    "agents.no_keys_title": "An API key comes first",
    "agents.no_prompt": "No system prompt",
    "agents.duplicate": "Duplicate",
    "agents.delete_title": "Delete agent?",
    "agents.tools": "Tools",
    "agents.is_supervisor": "Can act as supervisor",
    "agents.is_supervisor_hint": "A marked agent reviews reports unless another one is chosen in settings",
    "agents.key_missing": "key deleted",
    "agents.free": "free",
    "agents.need_name": "Enter an agent name",
    "agents.need_key": "Choose an API key",
    "agents.need_model": "Enter a model",
    "tool.web_search": "Web search",
    "tool.fetch_url": "Read pages",
    "tool.read_file": "Read files",
    "tool.write_file": "Write files",
    "tool.list_dir": "List files",
    "tool.code_exec": "Run code",
    "toolgroup.web_search": "Web search and pages",
    "toolgroup.files": "Project files",
    "toolgroup.code_exec": "Run code",
    "task.subtitle": "State the task and split it into subtasks by hand or with AI",
    "task.statement": "Statement",
    "task.untitled": "Untitled",
    "task.token_limit_note": "Checked before every model call, supervisor reviews included",
    "task.subtasks_hint": "Dependencies set the order: a predecessor's result goes to the assignee as input",
    "task.no_subtasks_title": "No subtasks yet",
    "task.no_subtasks": "Add them by hand or press Auto-split",
    "task.edit_subtask": "Edit subtask",
    "task.delete_subtask": "Delete subtask?",
    "task.depends_on": "Depends on",
    "task.depends_hint": "The subtask starts only after the selected ones are accepted",
    "task.no_deps_possible": "There are no other subtasks yet",
    "task.reworks": "reworks: {n}",
    "task.rerun": "Run again",
    "task.new_task": "New task",
    "task.new_task_confirm": "The current task stays in history and the form is cleared for a new one. Continue?",
    "task.need_body": "Describe the task: without it agents have nothing to work on",
    "task.bad_limit": "The token limit must be a positive whole number",
    "task.save_first": "Save the task first",
    "task.need_subtask_title": "Describe what needs to be done",
    "task.dep_cycle": "This dependency would create a cycle",
    "fmt.auto": "Auto", "fmt.markdown": "Markdown", "fmt.docx": "DOCX", "fmt.pdf": "PDF",
    "fmt.zip": "ZIP",
    "run.no_task": "Define a task on the Task tab first",
    "run.unassigned_short": "Some subtasks have no assignee",
    "run.all_done": "All subtasks are done. To repeat, requeue them on the Task tab",
    "run.cannot_start": "Run not started",
    "run.k_done": "done",
    "run.k_review": "in review",
    "run.k_errors": "errors",
    "run.k_time": "time",
    "run.k_tokens": "tokens",
    "run.k_cost": "cost",
    "run.live": "Agent reasoning",
    "run.live_hint": "Model output appears as it is generated; italic is inner reasoning, cyan is tool calls",
    "run.graph": "Subtask graph",
    "run.graph_empty": "No subtasks yet",
    "run.feed_empty": "No events yet",
    "run.f_all": "All",
    "run.f_key": "Key",
    "run.f_errors": "Errors",
    "run.show_details": "Details",
    "run.hide_details": "Hide",
    "run.comment_placeholder": "Comment for the agent (optional)",
    "run.ph_idle": "idle",
    "run.ph_thinking": "thinking",
    "run.ph_tool": "tool",
    "run.ph_review": "reviewing",
    "run.ph_done": "done",
    "run.ph_error": "error",
    "run.step_of": "step {n} of {m}",
    "run.step": "Step",
    "run.subtask": "Subtask",
    "run.waiting": "Waiting for a subtask",
    "run.stream_empty": "Reasoning appears when the agent starts working",
    "run.sup_empty": "Supervisor reviews and summaries show up here",
    "run.copy_stream": "Copy reasoning",
    "run.to_latest": "Latest",
    "run.supervisor": "Supervisor",
    "run.system": "System",
    "reason.conflict": "Data conflict",
    "reason.not_accepted": "Result not accepted",
    "reason.low_confidence": "Low confidence",
    "reason.milestone": "Stage completed",
    "reason.unverified": "Result not verified",
    "reason.budget": "Budget limit reached",
    "decision.approve": "Approve",
    "decision.rework": "Send back",
    "decision.skip": "Skip",
    "decision.abort": "Stop run",
    "decision.extend": "Raise limit by 50%",
    "sup.checklist": "Reviews each report: scope, logic, facts, consistency with the project",
    "sup.configure_hint": "Pick a supervisor agent or a local model in settings",
    "sup.mode_api": "via API",
    "sup.mode_local": "local",
    "sup.no_summaries_title": "No summaries yet",
    "sup.no_incidents_title": "No incidents",
    "sup.no_approvals_title": "No decisions yet",
    "sup.closed_by_user": "Closed by the user",
    "kind.conflict": "Data conflict",
    "kind.factual_error": "Factual error",
    "kind.contradiction": "Contradiction",
    "kind.off_scope": "Out of scope",
    "kind.unverified": "Not verified",
    "sev.low": "low", "sev.medium": "medium", "sev.high": "high",
    "inc.open": "open", "inc.escalated": "needs a decision",
    "inc.auto_resolved": "auto-resolved", "inc.resolved": "closed",
    "hist.approve": "approved", "hist.rework": "sent back", "hist.skip": "skipped",
    "hist.abort": "run stopped", "hist.extend": "limit raised",
    "hist.cancelled": "dropped without a decision", "hist.pending": "awaiting decision",
    "dash.m_tokens_pct": "tokens · {pct}% of the task limit",
    "dash.spend": "Cumulative spending",
    "dash.money": "Money",
    "dash.tokens": "Tokens",
    "dash.sup_share": "supervisor {pct}%",
    "dash.v_unverified": "not verified",
    "bud.h_before": "Limits are checked before a model call, not after: an extra request is simply not sent",
    "bud.h_ask": "With human-in-the-loop on, the system asks whether to raise the limit instead of stopping work",
    "bud.h_log": "Spending comes from the call log, so restarting the app does not reset it",
    "bud.nothing_title": "Nothing to limit yet",
    "bud.tokens_short": "tok.",
    "bud.bad_tokens": "The token limit must be a positive whole number",
    "bud.bad_cost": "The cost limit must be a positive number",
    "scope.workspace": "project",
    "scope.task": "task",
    "scope.agent": "agent",
    "exp.recommended": "recommended",
    "exp.f_markdown": "Markdown", "exp.f_docx": "Word", "exp.f_pdf": "PDF", "exp.f_zip": "ZIP archive",
    "exp.fh_markdown": "Light text for notes, wikis and repositories",
    "exp.fh_docx": "A report people will read and edit",
    "exp.fh_pdf": "A ready-to-send document with Cyrillic support",
    "exp.fh_zip": "Report, manifest and all project files with structure",
    "settings.subtitle": "Interface and the active workspace",
    "settings.interface": "Interface",
    "settings.motion": "Animations",
    "settings.motion_hint": "Full: live background and expressive transitions. Reduced: short transitions only. Off: no motion",
    "settings.motion_full": "Full",
    "settings.motion_reduced": "Reduced",
    "settings.motion_off": "Off",
    "settings.hitl_title": "Human decisions",
    "settings.hitl_hint": "The system stops at critical points and waits for your decision",
    "settings.never": "never",
    "settings.supervisor_agent": "Supervisor agent",
    "settings.sup_api_short": "Agent with API key",
    "settings.sup_local_short": "Local model",
    "settings.local_model": "Local model",
    "settings.off": "off",
    "settings.min": "min",
    "settings.summary_cost_hint": "Summaries after every subtask noticeably increase token spending",
    "settings.anonymize": "Anonymous summaries",
    "settings.anonymize_hint": "Agents get a retelling without who wrote what",
    "settings.execution": "Execution",
    "settings.max_steps": "Steps per subtask",
    "settings.rework_rounds": "Automatic rework rounds",
    "settings.parallel": "Agents at once",
    "settings.tools": "Tools",
    "settings.tools_hint": "What agents of this workspace may use at all. Each agent can narrow the set in its card",
    "settings.search_backend": "Search service",
    "settings.search_key": "Search API key",
    "settings.search_key_set": "key saved, enter a new one to replace it",
    "settings.fetch_pages": "Allow opening found pages",
    "settings.sb_auto": "Auto",
    "settings.sb_process": "Process",
    "settings.sb_timeout": "Timeout",
    "settings.sb_memory": "Memory",
    "settings.docker_yes": "Docker available",
    "settings.docker_no": "Docker not found",
    "settings.docker_recheck": "Check again",
    "settings.docker_note_yes": "Agent code runs in a container without network, with a read-only root",
    "settings.docker_note_no": "Code runs as a separate process: the environment is clean, but the file system is not isolated. Install Docker for strict isolation",
    "settings.paths_warning": "Agents get read and write access to these folders. Do not add system folders or folders with personal data",
    "settings.paths_empty": "Agents can only access the workspace folder",
    "settings.security": "Security and data",
    "settings.security_text": "API keys are encrypted with AES-256-GCM. The encryption key is derived from the profile password with Argon2id and exists only in memory",
    "settings.open_data": "Open data folder",
    "settings.old_password": "Current password",
    "settings.password_note": "All API keys will be re-encrypted with the new password",
    "prefs.sup_auto": "Automatic (starred agent)",
    "prefs.add_path": "Choose a folder",
    "toast.profile_created": "Profile created",
    "toast.recovered": "The previous session ended unexpectedly",
    "toast.recovered_text": "Statuses of the unfinished run were fixed, you can start it again",
    "toast.run_active": "A run is in progress",
    "toast.run_active_text": "Wait until it finishes or stop the run",
    "toast.not_found": "Path not found",
    "toast.copied": "Copied to clipboard",
    "toast.run_done": "Run finished",
    "toast.run_failed": "Run finished with errors",
    "toast.run_review": "Run finished, your decisions are needed",
    "toast.run_stopped": "Run stopped",
    "toast.need_decision": "Your decision is needed",
    "toast.budget_alert": "Budget is close to the limit",
    "toast.budget_exceeded": "Budget limit reached",
    "toast.budget_extended": "Limit raised",
    "toast.subtask_failed": "Subtask failed",
    "toast.ws_created": "Workspace created",
    "toast.ws_deleted": "Workspace deleted",
    "toast.key_saved": "Key saved",
    "toast.key_deleted": "Key deleted",
    "toast.agent_created": "Agent created",
    "toast.agent_saved": "Agent saved",
    "toast.agent_deleted": "Agent deleted",
    "toast.task_saved": "Task saved",
    "toast.planned": "Task split",
    "toast.planned_n": "Subtasks: {n}. Check assignees and dependencies",
    "toast.plan_failed": "Could not split the task",
    "toast.summary_done": "Summary created and broadcast",
    "toast.summary_failed": "Summary not created",
    "toast.exported": "Export ready",
    "toast.export_failed": "Export failed",
    "toast.search_key_saved": "Search key saved",
    "toast.search_key_removed": "Search key removed",
    "toast.password_changed": "Password changed",
    "toast.password_changed_text": "API keys were re-encrypted with the new password",
}
````


## Интерфейс: QML

### `ui/qml/Main.qml`

*69 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import Ao

// Главное окно: живой фон, экран входа или оболочка приложения, уведомления.
T.ApplicationWindow {
    id: window
    width: 1440
    height: 900
    minimumWidth: 1180
    minimumHeight: 720
    visible: true
    color: Theme.bg
    title: backend.loggedIn ? backend.appName + " · " + backend.username : backend.appName
    font.family: Theme.fontFamily

    Component.onCompleted: {
        Theme.fontFamily = fonts.sans
        Theme.monoFamily = fonts.mono
        Theme.iconFamily = fonts.icons
        Theme.motion = Qt.binding(function() { return backend.motionLevel })
    }

    Aurora {
        anchors.fill: parent
        intensity: backend.loggedIn ? 0.75 : 1.0
        Behavior on intensity { NumberAnimation { duration: Theme.slow } }
    }

    // Экран входа и оболочка сменяют друг друга плавным «растворением».
    Loader {
        id: loginLoader
        anchors.fill: parent
        active: opacity > 0
        opacity: backend.loggedIn ? 0 : 1
        visible: opacity > 0
        source: "Login.qml"
        Behavior on opacity { NumberAnimation { duration: Theme.slow; easing.type: Easing.InOutQuad } }
    }
    Loader {
        id: shellLoader
        anchors.fill: parent
        active: backend.loggedIn
        opacity: backend.loggedIn ? 1 : 0
        visible: opacity > 0
        source: "Shell.qml"
        Behavior on opacity { NumberAnimation { duration: Theme.slow; easing.type: Easing.InOutQuad } }
        transform: Scale {
            origin.x: shellLoader.width / 2; origin.y: shellLoader.height / 2
            xScale: backend.loggedIn ? 1 : 0.985; yScale: xScale
            Behavior on xScale { NumberAnimation { duration: Theme.slow; easing.type: Easing.OutCubic } }
        }
    }

    Toasts {
        id: toasts
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.topMargin: 18
        anchors.rightMargin: 18
        height: parent.height - 36
        z: 1000
    }

    Connections {
        target: backend
        function onToast(kind, title, message) { toasts.show(kind, title, message) }
    }
}
````

### `ui/qml/Login.qml`

*303 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts
import Ao

// Экран входа: слева - знак и суть продукта, справа - карточка входа или
// создания профиля с индикатором надёжности пароля.
Item {
    id: root
    property bool signUp: backend.profiles.length === 0
    property string error: ""
    property real appear: 0
    Component.onCompleted: appear = 1
    Behavior on appear { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }

    Connections {
        target: backend
        function onAuthFinished(ok, message) {
            root.error = ok ? "" : message
            if (!ok) shake.restart()
        }
    }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // --- бренд --------------------------------------------------------------
        Item {
            Layout.fillWidth: true
            Layout.fillHeight: true
            ColumnLayout {
                anchors.centerIn: parent
                width: Math.min(parent.width - 120, 520)
                spacing: 22
                opacity: root.appear
                transform: Translate { y: (1 - root.appear) * 24 }

                OrbitLogo { size: 132; Layout.alignment: Qt.AlignLeft; speed: 0.8 }
                AText {
                    text: backend.appName
                    size: 44
                    weight: Font.Bold
                    Layout.fillWidth: true
                }
                AText {
                    text: i18n.t["login.tagline"]
                    size: Theme.fsH3
                    dim: true
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                    Layout.fillWidth: true
                    lineHeight: 1.25
                }
                ColumnLayout {
                    Layout.topMargin: 6
                    spacing: 14
                    Repeater {
                        model: [
                            { icon: "users", text: i18n.t["login.f1"] },
                            { icon: "shield-check", text: i18n.t["login.f2"] },
                            { icon: "lock", text: i18n.t["login.f3"] }
                        ]
                        delegate: RowLayout {
                            required property var modelData
                            required property int index
                            spacing: 12
                            opacity: root.appear
                            Rectangle {
                                width: 34; height: 34; radius: 11
                                color: Theme.alpha(Theme.violet, 0.14)
                                border.color: Theme.alpha(Theme.violetSoft, 0.25)
                                Icon { anchors.centerIn: parent; name: modelData.icon; size: 16; color: Theme.violetSoft }
                            }
                            AText { text: modelData.text; dim: true; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone }
                        }
                    }
                }
            }
        }

        // --- форма ---------------------------------------------------------------
        Item {
            Layout.preferredWidth: 560
            Layout.fillHeight: true

            Card {
                id: card
                anchors.centerIn: parent
                width: 420
                padding: 30
                radius: Theme.radiusXL
                opacity: root.appear
                transform: [
                    Translate { id: shakeShift; x: 0 },
                    Translate { y: (1 - root.appear) * 36 }
                ]

                SequentialAnimation {
                    id: shake
                    NumberAnimation { target: shakeShift; property: "x"; to: -10; duration: 50 }
                    NumberAnimation { target: shakeShift; property: "x"; to: 10; duration: 70 }
                    NumberAnimation { target: shakeShift; property: "x"; to: -6; duration: 60 }
                    NumberAnimation { target: shakeShift; property: "x"; to: 0; duration: 60 }
                }

                ColumnLayout {
                    width: parent.width
                    spacing: 16

                    RowLayout {
                        Layout.fillWidth: true
                        AText {
                            text: root.signUp ? i18n.t["login.create_title"] : i18n.t["login.title"]
                            size: Theme.fsH1
                            weight: Font.Bold
                            Layout.fillWidth: true
                            wrapMode: Text.Wrap
                            elide: Text.ElideNone
                        }
                        Segmented {
                            options: i18n.languages.map(function(l) { return { value: l.code, title: l.code.toUpperCase() } })
                            value: i18n.lang
                            onPicked: function(v) { backend.setLanguage(v) }
                        }
                    }
                    AText {
                        text: i18n.t["login.subtitle"]
                        dim: true
                        wrapMode: Text.Wrap
                        elide: Text.ElideNone
                        Layout.fillWidth: true
                    }

                    // --- вход ---
                    ColumnLayout {
                        visible: !root.signUp
                        Layout.fillWidth: true
                        spacing: 14
                        Select {
                            id: profile
                            Layout.fillWidth: true
                            label: i18n.t["login.username"]
                            icon: "user"
                            options: backend.profiles
                            value: backend.lastUsername
                            onPicked: function(v) { password.text = backend.savedPassword(v); password.focusInput() }
                        }
                        Field {
                            id: password
                            Layout.fillWidth: true
                            label: i18n.t["login.password"]
                            icon: "lock"
                            password: true
                            onAccepted: signInButton.clicked()
                            Component.onCompleted: {
                                text = backend.savedPassword(backend.lastUsername)
                                focusInput()
                            }
                        }
                        Toggle {
                            id: remember
                            Layout.fillWidth: true
                            label: i18n.t["login.remember"]
                            checked: backend.rememberDefault
                            enabled: backend.keyringAvailable
                        }
                    }

                    // --- создание профиля ---
                    ColumnLayout {
                        visible: root.signUp
                        Layout.fillWidth: true
                        spacing: 14
                        Rectangle {
                            Layout.fillWidth: true
                            radius: Theme.radius
                            color: Theme.alpha(Theme.warning, 0.08)
                            border.color: Theme.alpha(Theme.warning, 0.3)
                            implicitHeight: warn.implicitHeight + 22
                            RowLayout {
                                id: warn
                                anchors.fill: parent
                                anchors.margins: 11
                                spacing: 10
                                Icon { name: "triangle-alert"; color: Theme.warning; Layout.alignment: Qt.AlignTop }
                                AText {
                                    text: i18n.t["login.warning"]
                                    size: Theme.fsSmall
                                    color: Theme.textDim
                                    wrapMode: Text.Wrap
                                    elide: Text.ElideNone
                                    Layout.fillWidth: true
                                }
                            }
                        }
                        Field { id: newName; Layout.fillWidth: true; label: i18n.t["login.username"]; icon: "user" }
                        Field {
                            id: newPass
                            Layout.fillWidth: true
                            label: i18n.t["login.password"]
                            icon: "lock"
                            password: true
                        }
                        // Индикатор надёжности пароля.
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 6
                            property int strength: backend.passwordStrength(newPass.text)
                            Repeater {
                                model: 4
                                delegate: Rectangle {
                                    required property int index
                                    Layout.fillWidth: true
                                    height: 4
                                    radius: 2
                                    color: index < parent.strength
                                           ? (parent.strength <= 1 ? Theme.danger : parent.strength === 2 ? Theme.warning : Theme.success)
                                           : Theme.surface3
                                    Behavior on color { ColorAnimation { duration: Theme.normal } }
                                }
                            }
                            AText {
                                text: [i18n.t["login.s0"], i18n.t["login.s1"], i18n.t["login.s2"], i18n.t["login.s3"], i18n.t["login.s4"]][parent.strength]
                                size: Theme.fsMicro
                                mute: true
                                Layout.preferredWidth: 80
                                horizontalAlignment: Text.AlignRight
                            }
                        }
                        Field {
                            id: newPass2
                            Layout.fillWidth: true
                            label: i18n.t["login.password2"]
                            icon: "lock"
                            password: true
                            error: newPass2.text !== "" && newPass2.text !== newPass.text ? i18n.t["login.password_mismatch"] : ""
                            onAccepted: signUpButton.clicked()
                        }
                    }

                    // Ошибка входа.
                    Rectangle {
                        Layout.fillWidth: true
                        visible: root.error !== ""
                        radius: Theme.radius
                        color: Theme.alpha(Theme.danger, 0.1)
                        border.color: Theme.alpha(Theme.danger, 0.35)
                        implicitHeight: errText.implicitHeight + 18
                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 9
                            spacing: 8
                            Icon { name: "circle-alert"; color: Theme.danger }
                            AText { id: errText; text: root.error; color: Theme.danger; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true; size: Theme.fsSmall }
                        }
                    }

                    Button {
                        id: signInButton
                        visible: !root.signUp
                        Layout.fillWidth: true
                        Layout.topMargin: 4
                        variant: "primary"
                        iconName: "arrow-right"
                        text: i18n.t["login.signin"]
                        loading: backend.authBusy
                        enabled: !backend.authBusy
                        onClicked: backend.signIn(profile.combo.currentText, password.text, remember.checked)
                    }
                    Button {
                        id: signUpButton
                        visible: root.signUp
                        Layout.fillWidth: true
                        Layout.topMargin: 4
                        variant: "primary"
                        iconName: "sparkles"
                        text: i18n.t["login.create"]
                        loading: backend.authBusy
                        enabled: !backend.authBusy
                        onClicked: backend.signUp(newName.text, newPass.text, newPass2.text)
                    }
                    Button {
                        visible: backend.profiles.length > 0
                        Layout.fillWidth: true
                        variant: "ghost"
                        text: root.signUp ? i18n.t["login.have_profile"] : i18n.t["login.create"]
                        onClicked: { root.signUp = !root.signUp; root.error = "" }
                    }
                }
            }

            AText {
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 22
                anchors.horizontalCenter: parent.horizontalCenter
                text: backend.appName + " " + backend.appVersion + " · " + i18n.t["login.local"]
                mute: true
                size: Theme.fsSmall
            }
        }
    }
}
````

### `ui/qml/Shell.qml`

*495 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts
import Ao

// Оболочка после входа: боковая навигация, верхняя панель со статусом
// прогона и страницы, которые загружаются при первом открытии и дальше
// переключаются с анимацией.
Item {
    id: shell
    // Стартовая страница выбирается один раз; дальше страницу меняет только
    // пользователь. Связывание со статусом воркспейса сбрасывало бы выбор при
    // каждом изменении состояния приложения.
    property string page: ""
    Component.onCompleted: page = backend.workspaceId >= 0 ? "dashboard" : "workspaces"

    readonly property var sections: [
        { title: i18n.t["nav.g_project"], items: [
            { key: "workspaces", icon: "layers", title: i18n.t["nav.workspaces"] },
            { key: "agents", icon: "bot", title: i18n.t["nav.agents"] },
            { key: "task", icon: "list-checks", title: i18n.t["nav.task"] } ] },
        { title: i18n.t["nav.g_work"], items: [
            { key: "run", icon: "play", title: i18n.t["nav.run"] },
            { key: "supervisor", icon: "shield-check", title: i18n.t["nav.supervisor"] },
            { key: "dashboard", icon: "layout-dashboard", title: i18n.t["nav.dashboard"] } ] },
        { title: i18n.t["nav.g_resources"], items: [
            { key: "keys", icon: "key-round", title: i18n.t["nav.keys"] },
            { key: "budget", icon: "wallet", title: i18n.t["nav.budget"] },
            { key: "export", icon: "package", title: i18n.t["nav.export"] } ] }
    ]
    readonly property var pageFiles: ({
        workspaces: "pages/Workspaces.qml", agents: "pages/Agents.qml", task: "pages/Task.qml",
        run: "pages/Run.qml", supervisor: "pages/Supervisor.qml", dashboard: "pages/Dashboard.qml",
        keys: "pages/Keys.qml", budget: "pages/Budget.qml", export: "pages/Export.qml",
        settings: "pages/Settings.qml"
    })
    readonly property var order: ["workspaces", "agents", "task", "run", "supervisor",
                                  "dashboard", "keys", "budget", "export", "settings"]

    function go(key) { if (pageFiles[key]) page = key }

    Connections {
        target: backend
        function onNavigateRequested(key) { shell.go(key) }
    }

    // Горячие клавиши: Ctrl+1…0 - страницы, Ctrl+K - палитра команд.
    Repeater {
        model: shell.order
        delegate: Item {
            required property string modelData
            required property int index
            Shortcut {
                sequence: "Ctrl+" + ((index + 1) % 10)
                onActivated: shell.go(modelData)
            }
        }
    }
    Shortcut { sequence: "Ctrl+K"; onActivated: palette.open() }

    RowLayout {
        anchors.fill: parent
        spacing: 0

        // --- боковая панель -----------------------------------------------------
        Rectangle {
            id: sidebar
            Layout.preferredWidth: 248
            Layout.fillHeight: true
            color: Theme.alpha(Theme.sidebar, 0.86)
            Rectangle { anchors.right: parent.right; width: 1; height: parent.height; color: Theme.border }

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 16
                anchors.topMargin: 20
                spacing: 4

                RowLayout {
                    Layout.fillWidth: true
                    Layout.leftMargin: 6
                    Layout.bottomMargin: 18
                    spacing: 12
                    OrbitLogo { size: 36 }
                    ColumnLayout {
                        spacing: 0
                        AText { text: backend.appName; weight: Font.Bold; size: Theme.fsH3 }
                        AText { text: "v" + backend.appVersion; mute: true; size: Theme.fsMicro; mono: true }
                    }
                }

                // Быстрый поиск / палитра команд.
                Rectangle {
                    Layout.fillWidth: true
                    Layout.bottomMargin: 10
                    height: 36
                    radius: Theme.radius
                    color: searchHover.hovered ? Theme.surface2 : Theme.input
                    border.color: Theme.border
                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 12
                        anchors.rightMargin: 8
                        spacing: 8
                        Icon { name: "search"; size: 15; color: Theme.textMute }
                        AText { text: i18n.t["nav.search"]; mute: true; size: Theme.fsSmall; Layout.fillWidth: true }
                        Rectangle {
                            radius: 5; color: Theme.surface3
                            implicitWidth: kbd.implicitWidth + 10; implicitHeight: 20
                            AText { id: kbd; anchors.centerIn: parent; text: "Ctrl K"; size: Theme.fsMicro; mono: true; dim: true }
                        }
                    }
                    HoverHandler { id: searchHover; cursorShape: Qt.PointingHandCursor }
                    TapHandler { onTapped: palette.open() }
                }

                // Навигация с «переезжающей» подсветкой.
                Item {
                    id: navArea
                    Layout.fillWidth: true
                    Layout.fillHeight: true

                    Rectangle {
                        id: highlight
                        property Item target: null
                        x: 0
                        width: navArea.width
                        height: 38
                        // Зависимость от высот нужна, чтобы позиция пересчиталась после раскладки.
                        y: target ? (navColumn.height, sidebar.height, target.mapToItem(navArea, 0, 0).y) : -100
                        radius: Theme.radius
                        visible: target !== null
                        gradient: Gradient {
                            orientation: Gradient.Horizontal
                            GradientStop { position: 0; color: Theme.alpha(Theme.violet, 0.28) }
                            GradientStop { position: 1; color: Theme.alpha(Theme.cyan, 0.06) }
                        }
                        border.color: Theme.alpha(Theme.violetSoft, 0.25)
                        Behavior on y { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
                        Rectangle {
                            width: 3; height: 18; radius: 2
                            anchors.verticalCenter: parent.verticalCenter
                            x: 4
                            gradient: Gradient {
                                GradientStop { position: 0; color: Theme.violetSoft }
                                GradientStop { position: 1; color: Theme.cyan }
                            }
                        }
                    }

                    Column {
                        id: navColumn
                        width: parent.width
                        spacing: 2
                        Repeater {
                            model: shell.sections
                            delegate: Column {
                                id: section
                                required property var modelData
                                width: navColumn.width
                                spacing: 2
                                AText {
                                    text: section.modelData.title.toUpperCase()
                                    size: Theme.fsMicro
                                    weight: Font.DemiBold
                                    color: Theme.textFaint
                                    leftPadding: 12
                                    topPadding: 12
                                    bottomPadding: 6
                                    font.letterSpacing: 1.2
                                }
                                Repeater {
                                    model: section.modelData.items
                                    delegate: NavItem {
                                        width: navColumn.width
                                    }
                                }
                            }
                        }
                    }
                }

                NavItem {
                    Layout.fillWidth: true
                    modelData: ({ key: "settings", icon: "settings", title: i18n.t["nav.settings"] })
                }

                // Профиль и выход.
                Rectangle {
                    Layout.fillWidth: true
                    Layout.topMargin: 8
                    height: 56
                    radius: Theme.radius
                    color: Theme.alpha(Theme.surface2, 0.7)
                    border.color: Theme.border
                    RowLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 10
                        Rectangle {
                            width: 34; height: 34; radius: 17
                            gradient: Gradient {
                                GradientStop { position: 0; color: Theme.violet }
                                GradientStop { position: 1; color: Theme.teal }
                            }
                            AText {
                                anchors.centerIn: parent
                                text: backend.username.length ? backend.username[0].toUpperCase() : "?"
                                weight: Font.Bold
                                color: "white"
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 0
                            AText { text: backend.username; weight: Font.DemiBold; Layout.fillWidth: true }
                            AText { text: i18n.t["nav.local_profile"]; mute: true; size: Theme.fsMicro; Layout.fillWidth: true }
                        }
                        IconButton {
                            iconName: "log-out"
                            tip: i18n.t["nav.logout"]
                            onClicked: backend.logout()
                        }
                    }
                }
            }
        }

        // --- правая часть ------------------------------------------------------
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 0

            TopBar {
                Layout.fillWidth: true
                Layout.preferredHeight: 60
            }

            Item {
                id: stage
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true

                Repeater {
                    model: shell.order
                    delegate: Loader {
                        id: pageLoader
                        required property string modelData
                        readonly property bool current: shell.page === modelData
                        property bool visited: false
                        anchors.fill: parent
                        active: visited || current
                        visible: opacity > 0.01
                        opacity: current ? 1 : 0
                        source: shell.pageFiles[modelData]
                        onCurrentChanged: if (current) { visited = true; slide.y = Theme.rich ? 16 : 0; slideIn.restart() }
                        Behavior on opacity { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
                        transform: Translate { id: slide }
                        NumberAnimation { id: slideIn; target: slide; property: "y"; to: 0; duration: Theme.slow; easing.type: Easing.OutCubic }
                    }
                }
            }
        }
    }

    // Строка навигации (используется и для «Настроек» внизу панели).
    component NavItem: Item {
        id: nav
        required property var modelData
        readonly property bool active: shell.page === modelData.key
        height: 38
        onActiveChanged: if (active) highlight.target = nav
        Component.onCompleted: if (active) highlight.target = nav

        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 14
            anchors.rightMargin: 10
            spacing: 12
            Icon {
                name: nav.modelData.icon
                size: 17
                color: nav.active ? Theme.violetSoft : (navMouse.containsMouse ? Theme.text : Theme.textMute)
            }
            AText {
                text: nav.modelData.title
                Layout.fillWidth: true
                weight: nav.active ? Font.DemiBold : Font.Medium
                color: nav.active ? Theme.text : (navMouse.containsMouse ? Theme.text : Theme.textDim)
                Behavior on color { ColorAnimation { duration: Theme.fast } }
            }
            // Живые индикаторы: идёт прогон, ждут решения.
            StatusDot {
                visible: nav.modelData.key === "run" && backend.running
                status: "running"
            }
            Badge {
                visible: nav.modelData.key === "run" && backend.pendingApprovals > 0
                text: backend.pendingApprovals
                tone: "warning"
                solid: true
            }
            Badge {
                visible: nav.modelData.key === "supervisor" && backend.supervisor.openIncidents > 0
                text: backend.supervisor.openIncidents
                tone: "error"
            }
        }
        MouseArea {
            id: navMouse
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor
            onClicked: shell.go(nav.modelData.key)
        }
    }

    // Верхняя панель: активный воркспейс и живой статус прогона.
    component TopBar: Rectangle {
        color: "transparent"
        Rectangle { anchors.bottom: parent.bottom; width: parent.width; height: 1; color: Theme.alpha(Theme.border, 0.7) }
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: Theme.pagePad
            anchors.rightMargin: Theme.pagePad
            spacing: 14

            Icon { name: "layers"; size: 15; color: Theme.textMute }
            T.AbstractButton {
                id: wsButton
                hoverEnabled: true
                implicitHeight: 34
                implicitWidth: wsRow.implicitWidth + 20
                onClicked: shell.go("workspaces")
                background: Rectangle {
                    radius: Theme.radiusS
                    color: wsButton.hovered ? Theme.surface2 : "transparent"
                    Behavior on color { ColorAnimation { duration: Theme.fast } }
                }
                contentItem: Item {
                    RowLayout {
                        id: wsRow
                        anchors.centerIn: parent
                        spacing: 8
                        AText {
                            text: backend.workspaceName !== "" ? backend.workspaceName : i18n.t["top.no_ws"]
                            weight: Font.DemiBold
                            color: backend.workspaceName !== "" ? Theme.text : Theme.textMute
                        }
                        Icon { name: "chevron-down"; size: 14; color: Theme.textMute }
                    }
                }
            }

            Item { Layout.fillWidth: true }

            // Статус прогона: пульсирующая точка, время, токены, стоимость.
            Rectangle {
                visible: backend.running
                implicitHeight: 34
                implicitWidth: runRow.implicitWidth + 24
                radius: 17
                color: Theme.alpha(Theme.cyan, 0.08)
                border.color: Theme.alpha(Theme.cyan, 0.35)
                RowLayout {
                    id: runRow
                    anchors.centerIn: parent
                    spacing: 10
                    StatusDot { status: backend.paused ? "paused" : "running" }
                    AText { text: backend.paused ? i18n.t["top.paused"] : i18n.t["top.running"]; weight: Font.DemiBold; size: Theme.fsSmall }
                    AText { text: backend.runElapsed; mono: true; size: Theme.fsSmall; dim: true }
                    Rectangle { width: 1; height: 14; color: Theme.border }
                    Icon { name: "coins"; size: 13; color: Theme.textMute }
                    AText { text: backend.runTokens; mono: true; size: Theme.fsSmall; dim: true }
                    AText { text: backend.runCost; mono: true; size: Theme.fsSmall; color: Theme.teal }
                }
                MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: shell.go("run") }
            }

            // Колокольчик: ждут решения человека.
            T.AbstractButton {
                id: bell
                visible: backend.pendingApprovals > 0
                implicitWidth: 38; implicitHeight: 34
                hoverEnabled: true
                onClicked: shell.go("run")
                background: Rectangle {
                    radius: Theme.radiusS
                    color: Theme.alpha(Theme.warning, bell.hovered ? 0.22 : 0.12)
                    border.color: Theme.alpha(Theme.warning, 0.4)
                }
                contentItem: Icon {
                    name: "bell"; size: 16; color: Theme.warning
                    SequentialAnimation on rotation {
                        running: Theme.rich && bell.visible
                        loops: Animation.Infinite
                        NumberAnimation { to: 14; duration: 90 }
                        NumberAnimation { to: -12; duration: 110 }
                        NumberAnimation { to: 8; duration: 90 }
                        NumberAnimation { to: 0; duration: 90 }
                        PauseAnimation { duration: 2200 }
                    }
                }
                Tip { text: i18n.fmt(i18n.t["top.pending"], { n: backend.pendingApprovals }); shown: bell.hovered }
            }

            Button {
                visible: !backend.running && shell.page !== "run"
                compact: true
                variant: "secondary"
                iconName: "play"
                text: i18n.t["run.start"]
                enabled: backend.run.canStart
                onClicked: { shell.go("run"); backend.run.start() }
            }
        }
    }

    CommandPalette { id: palette }

    // Палитра команд: переход на страницы и частые действия с клавиатуры.
    component CommandPalette: Sheet {
        id: pal
        sheetWidth: 560
        title: i18n.t["palette.title"]
        icon: "command"
        property string query: ""
        readonly property var entries: {
            var list = []
            for (var s = 0; s < shell.sections.length; ++s)
                for (var i = 0; i < shell.sections[s].items.length; ++i) {
                    var it = shell.sections[s].items[i]
                    list.push({ kind: "page", key: it.key, icon: it.icon, title: it.title })
                }
            list.push({ kind: "page", key: "settings", icon: "settings", title: i18n.t["nav.settings"] })
            list.push({ kind: "action", key: "start", icon: "play", title: i18n.t["palette.start"] })
            list.push({ kind: "action", key: "summary", icon: "scroll-text", title: i18n.t["sup.make_summary"] })
            list.push({ kind: "action", key: "motion", icon: "sparkles", title: i18n.t["palette.motion"] })
            var q = pal.query.toLowerCase()
            return q === "" ? list : list.filter(function(e) { return e.title.toLowerCase().indexOf(q) >= 0 })
        }
        property int selected: 0
        onOpened: { query = ""; selected = 0; searchField.text = ""; searchField.focusInput() }

        function run(entry) {
            close()
            if (!entry) return
            if (entry.kind === "page") shell.go(entry.key)
            else if (entry.key === "start") { shell.go("run"); backend.run.start() }
            else if (entry.key === "summary") backend.supervisor.makeSummary()
            else if (entry.key === "motion") backend.setMotion(backend.motion === "full" ? "reduced" : backend.motion === "reduced" ? "off" : "full")
        }

        Field {
            id: searchField
            Layout.fillWidth: true
            icon: "search"
            placeholder: i18n.t["palette.placeholder"]
            onTextChanged: { pal.query = text; pal.selected = 0 }
            onAccepted: pal.run(pal.entries[pal.selected])
            onDownPressed: pal.selected = Math.min(pal.selected + 1, pal.entries.length - 1)
            onUpPressed: pal.selected = Math.max(pal.selected - 1, 0)
        }
        Repeater {
            model: pal.entries
            delegate: Rectangle {
                required property var modelData
                required property int index
                Layout.fillWidth: true
                height: 40
                radius: Theme.radius
                color: index === pal.selected ? Theme.alpha(Theme.violet, 0.18)
                     : (entryMouse.containsMouse ? Theme.surface2 : "transparent")
                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 12
                    anchors.rightMargin: 12
                    spacing: 12
                    Icon { name: modelData.icon; size: 16; color: index === pal.selected ? Theme.violetSoft : Theme.textMute }
                    AText { text: modelData.title; Layout.fillWidth: true }
                    AText { text: modelData.kind === "page" ? i18n.t["palette.page"] : i18n.t["palette.action"]; mute: true; size: Theme.fsMicro }
                }
                MouseArea {
                    id: entryMouse
                    anchors.fill: parent
                    hoverEnabled: true
                    onEntered: pal.selected = index
                    onClicked: pal.run(modelData)
                }
            }
        }
    }
}
````

### `ui/qml/pages/Workspaces.qml`

*204 строк*

````qml
import QtQuick
import QtQuick.Layouts
import Ao

// Воркспейсы: параллельные проекты. Активный подсвечен, клик - сделать активным.
Page {
    id: page
    title: i18n.t["ws.title"]
    subtitle: i18n.t["ws.subtitle"]
    icon: "layers"
    readonly property var ctl: backend.workspaces

    headerActions: [
        Button {
            variant: "primary"
            iconName: "plus"
            text: i18n.t["ws.new"]
            onClicked: editor.edit(-1, "", "")
        }
    ]

    EmptyState {
        visible: page.ctl.model.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "layers"
        title: i18n.t["ws.empty_title"]
        text: i18n.t["ws.empty"]
        actionText: i18n.t["ws.new"]
        onAction: editor.edit(-1, "", "")
    }

    GridLayout {
        id: grid
        Layout.fillWidth: true
        visible: page.ctl.model.count > 0
        columns: Math.max(1, Math.floor((page.contentWidth + 16) / 340))
        columnSpacing: 16
        rowSpacing: 16

        Repeater {
            model: page.ctl.model
            delegate: Card {
                id: wsCard
                Layout.fillWidth: true
                Layout.preferredHeight: 214
                hoverable: true
                glow: model.active
                stagger: index

                MouseArea {
                    anchors.fill: parent
                    cursorShape: model.active ? Qt.ArrowCursor : Qt.PointingHandCursor
                    onClicked: if (!model.active) page.ctl.select(model.id)
                }

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 10

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        Rectangle {
                            width: 40; height: 40; radius: 12
                            gradient: Gradient {
                                GradientStop { position: 0; color: model.active ? Theme.violet : Theme.surface3 }
                                GradientStop { position: 1; color: model.active ? Theme.teal : Theme.surface2 }
                            }
                            AText {
                                anchors.centerIn: parent
                                text: model.name.length ? model.name[0].toUpperCase() : "?"
                                weight: Font.Bold
                                size: Theme.fsH2
                                color: model.active ? "white" : Theme.textDim
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 2
                            AText { text: model.name; weight: Font.DemiBold; size: Theme.fsH3; Layout.fillWidth: true }
                            AText { text: i18n.fmt(i18n.t["ws.updated"], { when: model.updated }); mute: true; size: Theme.fsSmall }
                        }
                        Badge {
                            visible: model.active
                            text: i18n.t["ws.active"]
                            tone: "violet"
                            icon: "check"
                        }
                    }

                    AText {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: model.description !== "" ? model.description : i18n.t["ws.no_description"]
                        dim: model.description !== ""
                        mute: model.description === ""
                        wrapMode: Text.Wrap
                        elide: Text.ElideRight
                        maximumLineCount: 2
                        verticalAlignment: Text.AlignTop
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 14
                        Stat { glyph: "bot"; value: model.agents }
                        Stat { glyph: "coins"; value: model.tokens }
                        Stat { glyph: "dollar-sign"; value: model.cost; tint: Theme.teal }
                        Item { Layout.fillWidth: true }
                        IconButton {
                            iconName: "pencil"
                            tip: i18n.t["common.edit"]
                            onClicked: editor.edit(model.id, model.name, model.description)
                        }
                        IconButton {
                            iconName: "trash-2"
                            danger: true
                            tip: i18n.t["common.delete"]
                            onClicked: confirm.ask(i18n.t["ws.delete_title"], i18n.t["ws.delete_confirm"],
                                                   function() { page.ctl.remove(model.id) })
                        }
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        visible: model.taskTitle !== ""
                        height: 30
                        radius: Theme.radiusS
                        color: Theme.alpha(Theme.surface3, 0.6)
                        RowLayout {
                            anchors.fill: parent
                            anchors.leftMargin: 10
                            anchors.rightMargin: 10
                            spacing: 8
                            Icon { name: "list-checks"; size: 13; color: Theme.textMute }
                            AText { text: model.taskTitle; size: Theme.fsSmall; dim: true; Layout.fillWidth: true }
                        }
                    }
                }
            }
        }
    }

    component Stat: Row {
        property string glyph: ""
        property var value
        property color tint: Theme.textDim
        spacing: 5
        Icon { name: glyph; size: 13; color: Theme.textMute; anchors.verticalCenter: parent.verticalCenter }
        AText { text: value; size: Theme.fsSmall; mono: true; color: tint; anchors.verticalCenter: parent.verticalCenter }
    }

    Confirm {
        id: confirm
        confirmText: i18n.t["common.delete"]
        cancelText: i18n.t["common.cancel"]
    }

    Sheet {
        id: editor
        property int wsId: -1
        property string error: ""
        title: wsId >= 0 ? i18n.t["ws.edit"] : i18n.t["ws.new"]
        icon: "layers"
        sheetWidth: 480

        function edit(id, name, description) {
            wsId = id
            error = ""
            nameField.text = name
            descField.text = description
            open()
            nameField.focusInput()
        }
        function save() {
            var err = wsId >= 0 ? page.ctl.update(wsId, nameField.text, descField.text)
                                : page.ctl.create(nameField.text, descField.text)
            if (err === "") close(); else error = err
        }

        Field {
            id: nameField
            Layout.fillWidth: true
            label: i18n.t["ws.name"]
            icon: "layers"
            error: editor.error
            onAccepted: editor.save()
        }
        TextBox {
            id: descField
            Layout.fillWidth: true
            label: i18n.t["common.description"]
            placeholder: i18n.t["ws.desc_placeholder"]
            minHeight: 100
        }

        footer: [
            Item { Layout.fillWidth: true },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: editor.close() },
            Button { text: i18n.t["common.save"]; variant: "primary"; iconName: "check"; onClicked: editor.save() }
        ]
    }
}
````

### `ui/qml/pages/Keys.qml`

*293 строк*

````qml
import QtQuick
import QtQuick.Layouts
import Ao

// API-ключи: карточки подключений с живой проверкой и мастер добавления,
// где провайдер выбирается плиткой, а адрес подставляется сам.
Page {
    id: page
    title: i18n.t["keys.title"]
    subtitle: i18n.t["keys.subtitle"]
    icon: "key-round"
    readonly property var ctl: backend.keys

    headerActions: [
        Button {
            variant: "primary"
            iconName: "plus"
            text: i18n.t["keys.new"]
            onClicked: editor.openNew()
        }
    ]

    EmptyState {
        visible: page.ctl.model.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "key-round"
        title: i18n.t["keys.empty_title"]
        text: i18n.t["keys.empty"]
        actionText: i18n.t["keys.new"]
        onAction: editor.openNew()
    }

    Repeater {
        model: page.ctl.model
        delegate: Card {
            Layout.fillWidth: true
            hoverable: true
            stagger: index
            padding: 18

            RowLayout {
                width: parent.width
                spacing: 16

                Rectangle {
                    width: 46; height: 46; radius: 14
                    color: model.local ? Theme.alpha(Theme.teal, 0.14) : Theme.alpha(Theme.violet, 0.14)
                    border.color: model.local ? Theme.alpha(Theme.teal, 0.35) : Theme.alpha(Theme.violetSoft, 0.3)
                    Icon {
                        anchors.centerIn: parent
                        name: model.local ? "hard-drive" : "key-round"
                        size: 20
                        color: model.local ? Theme.teal : Theme.violetSoft
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 4
                    RowLayout {
                        spacing: 8
                        AText { text: model.label; weight: Font.DemiBold; size: Theme.fsH3 }
                        Badge { text: model.providerTitle; tone: "violet" }
                        Badge { visible: model.free; text: i18n.t["keys.free"]; tone: "success" }
                        Badge { visible: model.local; text: i18n.t["keys.local"]; tone: "accent"; icon: "hard-drive" }
                    }
                    AText { text: model.baseUrl; mute: true; mono: true; size: Theme.fsSmall; Layout.fillWidth: true }
                    RowLayout {
                        spacing: 8
                        Icon {
                            name: model.hasSecret ? "lock" : "circle-dot"
                            size: 12
                            color: model.hasSecret ? Theme.success : Theme.textMute
                        }
                        AText {
                            text: model.hasSecret ? i18n.t["keys.stored"] : i18n.t["keys.no_secret"]
                            size: Theme.fsSmall
                            dim: true
                        }
                        AText {
                            visible: model.models > 0
                            text: "· " + i18n.fmt(i18n.t["keys.models_cached"], { n: model.models })
                            size: Theme.fsSmall
                            mute: true
                        }
                    }
                    // Результат проверки соединения.
                    RowLayout {
                        visible: model.testState !== ""
                        spacing: 8
                        Spinner { visible: model.testState === "testing"; size: 14 }
                        Icon {
                            visible: model.testState !== "testing"
                            name: model.testState === "ok" ? "circle-check" : "circle-x"
                            size: 14
                            color: model.testState === "ok" ? Theme.success : Theme.danger
                        }
                        AText {
                            text: model.testState === "testing" ? i18n.t["keys.testing"] : model.testMessage
                            size: Theme.fsSmall
                            color: model.testState === "fail" ? Theme.danger
                                 : model.testState === "ok" ? Theme.success : Theme.textDim
                            Layout.maximumWidth: 560
                            wrapMode: Text.Wrap
                            elide: Text.ElideNone
                        }
                    }
                }

                Button {
                    Layout.alignment: Qt.AlignTop
                    compact: true
                    iconName: "activity"
                    text: i18n.t["common.test"]
                    loading: model.testState === "testing"
                    enabled: model.testState !== "testing"
                    onClicked: page.ctl.test(model.id)
                }
                IconButton {
                    Layout.alignment: Qt.AlignTop
                    iconName: "pencil"
                    tip: i18n.t["common.edit"]
                    onClicked: editor.openEdit(model.id, model.provider, model.label, model.baseUrl)
                }
                IconButton {
                    Layout.alignment: Qt.AlignTop
                    iconName: "trash-2"
                    danger: true
                    tip: i18n.t["common.delete"]
                    onClicked: confirm.ask(i18n.t["keys.delete_title"], i18n.t["keys.delete_confirm"],
                                           function() { page.ctl.remove(model.id) })
                }
            }
        }
    }

    Confirm {
        id: confirm
        confirmText: i18n.t["common.delete"]
        cancelText: i18n.t["common.cancel"]
    }

    Sheet {
        id: editor
        property int keyId: -1
        property string provider: "openai"
        property string error: ""
        readonly property var preset: {
            var list = page.ctl.presets
            for (var i = 0; i < list.length; ++i) if (list[i].key === provider) return list[i]
            return list.length ? list[0] : ({})
        }
        title: keyId >= 0 ? i18n.t["keys.edit"] : i18n.t["keys.new"]
        subtitle: i18n.t["keys.subtitle"]
        icon: "key-round"
        sheetWidth: 680

        function openNew() {
            keyId = -1; error = ""; provider = "openai"
            labelField.text = ""; urlField.text = preset.baseUrl; secretField.text = ""
            open()
        }
        function openEdit(id, prov, label, url) {
            keyId = id; error = ""; provider = prov
            labelField.text = label; urlField.text = url; secretField.text = ""
            open()
        }
        function pick(key) {
            provider = key
            urlField.text = preset.baseUrl
            if (labelField.text === "") labelField.text = ""
        }
        function save() {
            var err = keyId >= 0 ? page.ctl.update(keyId, labelField.text, urlField.text, secretField.text)
                                 : page.ctl.create(provider, labelField.text, urlField.text, secretField.text)
            if (err === "") close(); else error = err
        }

        // Провайдеры плитками (только при создании: провайдер ключа не меняется).
        AText { visible: editor.keyId < 0; text: i18n.t["keys.provider"]; size: Theme.fsSmall; weight: Font.Medium; dim: true }
        GridLayout {
            visible: editor.keyId < 0
            Layout.fillWidth: true
            columns: 4
            columnSpacing: 10
            rowSpacing: 10
            Repeater {
                model: page.ctl.presets
                delegate: Rectangle {
                    id: tile
                    required property var modelData
                    readonly property bool chosen: editor.provider === modelData.key
                    Layout.fillWidth: true
                    implicitHeight: 64
                    radius: Theme.radius
                    color: chosen ? Theme.alpha(Theme.violet, 0.16) : (tileMouse.containsMouse ? Theme.surface3 : Theme.surface2)
                    border.color: chosen ? Theme.violet : Theme.border
                    Behavior on color { ColorAnimation { duration: Theme.fast } }
                    ColumnLayout {
                        anchors.fill: parent
                        anchors.margins: 10
                        spacing: 4
                        AText { text: tile.modelData.title; weight: Font.DemiBold; size: Theme.fsSmall; Layout.fillWidth: true }
                        RowLayout {
                            spacing: 4
                            Badge { visible: tile.modelData.free; text: i18n.t["keys.free"]; tone: "success" }
                            Badge { visible: tile.modelData.local; text: i18n.t["keys.local"]; tone: "accent" }
                        }
                    }
                    MouseArea {
                        id: tileMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        cursorShape: Qt.PointingHandCursor
                        onClicked: editor.pick(tile.modelData.key)
                    }
                }
            }
        }

        Rectangle {
            Layout.fillWidth: true
            visible: (editor.preset.notes || "") !== "" || (editor.preset.docsUrl || "") !== ""
            radius: Theme.radius
            color: Theme.alpha(Theme.cyan, 0.06)
            border.color: Theme.alpha(Theme.cyan, 0.2)
            implicitHeight: notesCol.implicitHeight + 20
            ColumnLayout {
                id: notesCol
                anchors.fill: parent
                anchors.margins: 10
                spacing: 4
                AText {
                    visible: (editor.preset.notes || "") !== ""
                    text: editor.preset.notes || ""
                    size: Theme.fsSmall
                    dim: true
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                    Layout.fillWidth: true
                }
                AText {
                    visible: (editor.preset.docsUrl || "") !== ""
                    text: "<a href=\"" + editor.preset.docsUrl + "\">" + i18n.t["keys.get_key"] + " ↗</a>"
                    textFormat: Text.RichText
                    size: Theme.fsSmall
                    onLinkActivated: function(link) { Qt.openUrlExternally(link) }
                    HoverHandler { cursorShape: Qt.PointingHandCursor }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            Field {
                id: labelField
                Layout.fillWidth: true
                label: i18n.t["keys.label"]
                placeholder: editor.preset.title || ""
                icon: "star"
            }
            Field {
                id: urlField
                Layout.fillWidth: true
                Layout.preferredWidth: 2
                label: i18n.t["keys.base_url"]
                mono: true
                icon: "globe"
            }
        }
        Field {
            id: secretField
            Layout.fillWidth: true
            label: i18n.t["keys.key"]
            password: true
            mono: true
            icon: "lock"
            placeholder: editor.keyId >= 0 ? i18n.t["keys.keep_secret"] : "sk-…"
            hint: editor.preset.requiresKey === false ? i18n.t["keys.no_key_needed"] : ""
            error: editor.error
            onAccepted: editor.save()
        }

        footer: [
            Icon { name: "shield-check"; size: 14; color: Theme.success },
            AText { text: i18n.t["keys.encrypted_note"]; mute: true; size: Theme.fsSmall; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: editor.close() },
            Button { text: i18n.t["common.save"]; variant: "primary"; iconName: "check"; onClicked: editor.save() }
        ]
    }
}
````

### `ui/qml/pages/Agents.qml`

*392 строк*

````qml
import QtQuick
import QtQuick.Layouts
import Ao

// Агенты воркспейса: сетка карточек и редактор с шаблонами ролей,
// загрузкой моделей, инструментами и системным промптом.
Page {
    id: page
    title: i18n.t["agents.title"]
    subtitle: i18n.t["agents.isolated_note"]
    icon: "bot"
    readonly property var ctl: backend.agents

    headerActions: [
        Button {
            variant: "primary"
            iconName: "plus"
            text: i18n.t["agents.new"]
            enabled: backend.workspaceId >= 0 && page.ctl.hasKeys
            onClicked: editor.openNew()
        }
    ]

    EmptyState {
        visible: backend.workspaceId < 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "layers"
        title: i18n.t["ws.empty_title"]
        text: i18n.t["ws.empty"]
        actionText: i18n.t["nav.workspaces"]
        actionIcon: "arrow-right"
        onAction: backend.navigate("workspaces")
    }
    EmptyState {
        visible: backend.workspaceId >= 0 && !page.ctl.hasKeys
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "key-round"
        title: i18n.t["agents.no_keys_title"]
        text: i18n.t["agents.no_keys"]
        actionText: i18n.t["keys.new"]
        onAction: backend.navigate("keys")
    }
    EmptyState {
        visible: backend.workspaceId >= 0 && page.ctl.hasKeys && page.ctl.model.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "bot"
        title: i18n.t["agents.empty_title"]
        text: i18n.t["agents.empty"]
        actionText: i18n.t["agents.new"]
        onAction: editor.openNew()
    }

    GridLayout {
        Layout.fillWidth: true
        visible: page.ctl.model.count > 0
        columns: Math.max(1, Math.floor((page.contentWidth + 16) / 360))
        columnSpacing: 16
        rowSpacing: 16

        Repeater {
            model: page.ctl.model
            delegate: Card {
                id: agentCard
                Layout.fillWidth: true
                Layout.preferredHeight: 232
                hoverable: true
                stagger: index
                glow: model.status === "running"
                glowColor: Theme.cyan
                opacity: model.enabled ? enter : enter * 0.55
                readonly property var toolList: model.toolTitles

                ColumnLayout {
                    anchors.fill: parent
                    spacing: 10

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 12
                        Item {
                            width: 46; height: 46
                            Rectangle {
                                anchors.fill: parent
                                radius: 23
                                gradient: Gradient {
                                    GradientStop { position: 0; color: model.isSupervisor ? Theme.magenta : Theme.violet }
                                    GradientStop { position: 1; color: model.isSupervisor ? Theme.violetSoft : Theme.cyan }
                                }
                                opacity: 0.9
                                Icon { anchors.centerIn: parent; name: model.icon; size: 20; color: "white" }
                            }
                            StatusDot {
                                anchors.right: parent.right
                                anchors.bottom: parent.bottom
                                size: 11
                                status: model.status
                            }
                        }
                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 2
                            RowLayout {
                                spacing: 6
                                AText { text: model.name; weight: Font.DemiBold; size: Theme.fsH3; Layout.maximumWidth: 180 }
                                Icon { visible: model.isSupervisor; name: "star"; size: 14; color: Theme.warning }
                            }
                            AText { text: model.roleTitle + " · " + model.statusTitle; mute: true; size: Theme.fsSmall }
                        }
                        Toggle {
                            isOn: model.enabled
                            onToggled: page.ctl.setEnabled(model.id, checked)
                        }
                    }

                    RowLayout {
                        spacing: 6
                        Badge { text: model.modelName !== "" ? model.modelName : "-"; tone: "accent"; icon: "cpu" }
                        Badge { visible: model.price !== ""; text: model.price; tone: "muted"; icon: "coins" }
                    }

                    AText {
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: model.promptPreview !== "" ? model.promptPreview : i18n.t["agents.no_prompt"]
                        dim: true
                        size: Theme.fsSmall
                        wrapMode: Text.Wrap
                        elide: Text.ElideRight
                        maximumLineCount: 3
                        verticalAlignment: Text.AlignTop
                    }

                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 6
                        // Инструменты: сколько помещается; край плавно гаснет.
                        Item {
                            Layout.fillWidth: true
                            height: 22
                            clip: true
                            Row {
                                id: toolRow
                                spacing: 6
                                Repeater {
                                    model: agentCard.toolList
                                    delegate: Rectangle {
                                        required property string modelData
                                        required property int index
                                        radius: 8
                                        height: 22
                                        width: toolText.implicitWidth + 14
                                        color: Theme.surface3
                                        AText { id: toolText; anchors.centerIn: parent; text: modelData; size: Theme.fsMicro; dim: true }
                                    }
                                }
                            }
                            Rectangle {
                                visible: toolRow.width > parent.width
                                anchors.right: parent.right
                                width: 28
                                height: parent.height
                                gradient: Gradient {
                                    orientation: Gradient.Horizontal
                                    GradientStop { position: 0; color: "transparent" }
                                    GradientStop { position: 1; color: agentCard.color }
                                }
                            }
                        }
                        IconButton { iconName: "copy"; tip: i18n.t["agents.duplicate"]; onClicked: page.ctl.duplicate(model.id) }
                        IconButton {
                            iconName: "pencil"
                            tip: i18n.t["common.edit"]
                            onClicked: editor.openEdit(page.ctl.model.get(index))
                        }
                        IconButton {
                            iconName: "trash-2"
                            danger: true
                            tip: i18n.t["common.delete"]
                            onClicked: confirm.ask(i18n.t["agents.delete_title"], i18n.t["agents.delete_confirm"],
                                                   function() { page.ctl.remove(model.id) })
                        }
                    }
                }
            }
        }
    }

    Confirm {
        id: confirm
        confirmText: i18n.t["common.delete"]
        cancelText: i18n.t["common.cancel"]
    }

    Sheet {
        id: editor
        property int agentId: -1
        property string role: "analyst"
        property string autoName: ""
        property string autoPrompt: ""
        property var tools: []
        property var models: []
        property string error: ""
        property bool loadingModels: false
        title: agentId >= 0 ? i18n.t["agents.edit"] : i18n.t["agents.new"]
        subtitle: i18n.t["agents.isolated_note"]
        icon: "bot"
        sheetWidth: 760

        function openNew() {
            agentId = -1; error = ""
            nameField.text = ""; promptBox.text = ""
            autoName = ""; autoPrompt = ""
            temp.value = 0.7; maxTok.value = 2048
            supervisorToggle.checked = false
            keySelect.value = page.ctl.keyOptions.length ? page.ctl.keyOptions[0].id : -1
            applyTemplate("analyst")
            refreshModels()
            modelSelect.combo.editText = models.length ? models[0] : ""
            open()
        }
        function openEdit(data) {
            agentId = data.id; error = ""
            role = data.role
            nameField.text = data.name; autoName = ""
            promptBox.text = data.prompt; autoPrompt = ""
            tools = data.tools
            temp.value = data.temperature; maxTok.value = data.maxTokens
            supervisorToggle.checked = data.isSupervisor
            keySelect.value = data.keyId
            refreshModels()
            modelSelect.combo.editText = data.modelName
            open()
        }
        // Шаблон роли подставляет имя, промпт и инструменты, но не затирает
        // то, что пользователь уже успел поправить руками.
        function applyTemplate(key) {
            role = key
            var info = page.ctl.templateInfo(key)
            if (nameField.text === "" || nameField.text === autoName) { nameField.text = info.name; autoName = info.name }
            if (info.prompt !== "" && (promptBox.text === "" || promptBox.text === autoPrompt)) { promptBox.text = info.prompt; autoPrompt = info.prompt }
            tools = info.tools
        }
        function refreshModels() { models = page.ctl.modelsForKey(keySelect.value === undefined ? -1 : keySelect.value) }
        function toggleTool(name, on) {
            var list = tools.slice()
            var i = list.indexOf(name)
            if (on && i < 0) list.push(name)
            if (!on && i >= 0) list.splice(i, 1)
            tools = list
        }
        function save() {
            var err = page.ctl.save({
                id: agentId, name: nameField.text, role: role, prompt: promptBox.text,
                keyId: keySelect.value === undefined ? -1 : keySelect.value,
                model: modelSelect.combo.editText, temperature: temp.value, maxTokens: maxTok.value,
                tools: tools, isSupervisor: supervisorToggle.checked
            })
            if (err === "") close(); else error = err
        }

        Connections {
            target: page.ctl
            function onModelsLoaded(keyId, list, err) {
                // Пока шёл запрос, могли выбрать другой ключ: чужой список не нужен.
                if (keyId !== keySelect.value) return
                editor.loadingModels = false
                if (err !== "") { editor.error = err; return }
                var current = modelSelect.combo.editText
                editor.models = list
                modelSelect.combo.editText = current
            }
        }

        AText { text: i18n.t["agents.template"]; size: Theme.fsSmall; weight: Font.Medium; dim: true }
        Flow {
            Layout.fillWidth: true
            spacing: 8
            Repeater {
                model: page.ctl.templates
                delegate: Chip {
                    required property var modelData
                    text: modelData.title
                    iconName: modelData.icon
                    isOn: editor.role === modelData.key
                    onClicked: editor.applyTemplate(modelData.key)
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            Field { id: nameField; Layout.fillWidth: true; label: i18n.t["agents.name"]; icon: "user" }
            Select {
                id: keySelect
                Layout.fillWidth: true
                label: i18n.t["agents.provider_key"]
                icon: "key-round"
                options: page.ctl.keyOptions.map(function(k) { return { value: k.id, title: k.title } })
                onPicked: function(v) { keySelect.value = v; editor.loadingModels = false; editor.refreshModels() }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 12
            Select {
                id: modelSelect
                Layout.fillWidth: true
                label: i18n.t["agents.model"]
                icon: "cpu"
                editable: true
                options: editor.models
                placeholder: "gpt-4o-mini"
            }
            Button {
                Layout.alignment: Qt.AlignBottom
                iconName: "refresh-cw"
                text: i18n.t["agents.load_models"]
                loading: editor.loadingModels
                onClicked: { editor.loadingModels = true; editor.error = ""; page.ctl.loadModels(keySelect.value) }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 24
            RangeSlider {
                id: temp
                Layout.fillWidth: true
                label: i18n.t["agents.temperature"]
                from: 0; to: 2; stepSize: 0.1; decimals: 1
                onCommitted: function(v) { temp.value = v }
            }
            RangeSlider {
                id: maxTok
                Layout.fillWidth: true
                label: i18n.t["agents.max_tokens"]
                from: 256; to: 32768; stepSize: 256; decimals: 0
                onCommitted: function(v) { maxTok.value = v }
            }
        }

        AText { text: i18n.t["agents.tools"]; size: Theme.fsSmall; weight: Font.Medium; dim: true }
        Flow {
            Layout.fillWidth: true
            spacing: 8
            Repeater {
                model: page.ctl.tools
                delegate: Chip {
                    required property var modelData
                    text: modelData.title
                    isOn: editor.tools.indexOf(modelData.name) >= 0
                    onClicked: editor.toggleTool(modelData.name, checked)
                }
            }
        }

        TextBox {
            id: promptBox
            Layout.fillWidth: true
            label: i18n.t["agents.prompt"]
            mono: true
            minHeight: 190
        }

        Toggle {
            id: supervisorToggle
            Layout.fillWidth: true
            label: i18n.t["agents.is_supervisor"]
            hint: i18n.t["agents.is_supervisor_hint"]
        }

        AText {
            visible: editor.error !== ""
            text: editor.error
            color: Theme.danger
            wrapMode: Text.Wrap
            elide: Text.ElideNone
            Layout.fillWidth: true
        }

        footer: [
            Item { Layout.fillWidth: true },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: editor.close() },
            Button { text: i18n.t["common.save"]; variant: "primary"; iconName: "check"; onClicked: editor.save() }
        ]
    }
}
````

### `ui/qml/pages/Task.qml`

*407 строк*

````qml
import QtQuick
import QtQuick.Layouts
import Ao

// Постановка задачи слева, подзадачи справа: ручные или от ИИ-планировщика,
// с исполнителями и зависимостями.
Page {
    id: page
    title: i18n.t["task.title"]
    subtitle: i18n.t["task.subtitle"]
    icon: "list-checks"
    readonly property var ctl: backend.task
    property string error: ""
    property string fmt: ctl.format

    Connections {
        target: page.ctl
        function onChanged() {
            if (!titleField.input.activeFocus) titleField.text = page.ctl.title
            if (!bodyBox.area.activeFocus) bodyBox.text = page.ctl.description
            if (!limitField.input.activeFocus) limitField.text = page.ctl.tokenLimit
            page.fmt = page.ctl.format
        }
    }
    Component.onCompleted: {
        titleField.text = ctl.title
        bodyBox.text = ctl.description
        limitField.text = ctl.tokenLimit
    }

    function save() {
        error = ctl.saveTask(titleField.text, bodyBox.text, fmt, limitField.text)
        if (error === "") backend.toast("success", i18n.t["toast.task_saved"], "")
        return error === ""
    }

    headerActions: [
        Button {
            iconName: "square-pen"
            text: i18n.t["task.new_task"]
            visible: page.ctl.hasTask
            enabled: !backend.running
            onClicked: confirm.ask(i18n.t["task.new_task"], i18n.t["task.new_task_confirm"],
                                   function() { var e = page.ctl.newTask(); if (e !== "") backend.toast("warning", e, "") }, false,
                                   i18n.t["task.new_task"])
        },
        Button {
            variant: "primary"
            iconName: "play"
            text: i18n.t["run.start"]
            enabled: !backend.running && backend.workspaceId >= 0
            onClicked: if (page.save()) { backend.navigate("run"); backend.run.start() }
        }
    ]

    EmptyState {
        visible: backend.workspaceId < 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "layers"
        title: i18n.t["ws.empty_title"]
        text: i18n.t["ws.empty"]
        actionText: i18n.t["nav.workspaces"]
        actionIcon: "arrow-right"
        onAction: backend.navigate("workspaces")
    }

    RowLayout {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        spacing: 18

        // --- задача -----------------------------------------------------------
        Card {
            Layout.preferredWidth: Math.max(380, page.contentWidth * 0.42)
            Layout.alignment: Qt.AlignTop
            stagger: 0

            ColumnLayout {
                width: parent.width
                spacing: 16

                SectionTitle {
                    Layout.fillWidth: true
                    text: i18n.t["task.statement"]
                    icon: "square-pen"
                    Badge {
                        visible: page.ctl.status !== ""
                        text: page.ctl.statusTitle
                        tone: page.ctl.status === "done" ? "success" : page.ctl.status === "running" ? "accent"
                            : page.ctl.status === "failed" ? "error" : "muted"
                    }
                }
                Field {
                    id: titleField
                    Layout.fillWidth: true
                    label: i18n.t["task.name"]
                    placeholder: i18n.t["task.untitled"]
                    icon: "sparkles"
                }
                TextBox {
                    id: bodyBox
                    Layout.fillWidth: true
                    label: i18n.t["task.body"]
                    placeholder: i18n.t["task.placeholder"]
                    minHeight: 240
                }

                AText { text: i18n.t["task.result_format"]; size: Theme.fsSmall; weight: Font.Medium; dim: true }
                Segmented {
                    Layout.fillWidth: true
                    stretch: true
                    options: page.ctl.formats.map(function(f) { return { value: f.key, title: f.title, icon: f.icon } })
                    value: page.fmt
                    onPicked: function(v) { page.fmt = v }
                }

                Field {
                    id: limitField
                    Layout.fillWidth: true
                    label: i18n.t["task.token_limit"]
                    placeholder: i18n.t["task.token_limit_hint"]
                    hint: i18n.t["task.token_limit_note"]
                    icon: "gauge"
                    mono: true
                }

                AText {
                    visible: page.error !== ""
                    text: page.error
                    color: Theme.danger
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                    Layout.fillWidth: true
                }

                Button {
                    Layout.fillWidth: true
                    variant: "primary"
                    iconName: "check"
                    text: i18n.t["task.save"]
                    onClicked: page.save()
                }
            }
        }

        // --- подзадачи ----------------------------------------------------------
        ColumnLayout {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop
            spacing: 12

            SectionTitle {
                Layout.fillWidth: true
                text: i18n.t["task.subtasks"] + (page.ctl.subtasks.count ? "  ·  " + page.ctl.subtasks.count : "")
                hint: i18n.t["task.subtasks_hint"]
                icon: "workflow"
                Button {
                    compact: true
                    iconName: "plus"
                    text: i18n.t["task.add_subtask"]
                    onClicked: { if (!page.ctl.hasTask && !page.save()) return; subEditor.openNew() }
                }
                Button {
                    compact: true
                    variant: "primary"
                    iconName: "wand-sparkles"
                    text: i18n.t["task.autosplit"]
                    loading: page.ctl.planning
                    enabled: !page.ctl.planning
                    onClicked: if (page.save()) page.ctl.autosplit()
                }
            }

            // Пока ИИ планирует - «скелет» будущих карточек.
            Repeater {
                model: page.ctl.planning ? 3 : 0
                delegate: Card {
                    Layout.fillWidth: true
                    padding: 16
                    ColumnLayout {
                        width: parent.width
                        spacing: 10
                        Skeleton { Layout.preferredWidth: parent.width * 0.55; height: 14 }
                        Skeleton { Layout.fillWidth: true; height: 10 }
                        Skeleton { Layout.preferredWidth: parent.width * 0.35; height: 10 }
                    }
                }
            }

            Card {
                visible: page.ctl.subtasks.count === 0 && !page.ctl.planning
                Layout.fillWidth: true
                EmptyState {
                    width: parent.width
                    icon: "workflow"
                    title: i18n.t["task.no_subtasks_title"]
                    text: i18n.t["task.no_subtasks"]
                }
            }

            ListView {
                id: subList
                Layout.fillWidth: true
                Layout.preferredHeight: contentHeight
                interactive: false
                spacing: 10
                model: page.ctl.subtasks
                move: Transition { NumberAnimation { properties: "y"; duration: Theme.normal; easing.type: Easing.OutCubic } }
                displaced: Transition { NumberAnimation { properties: "y"; duration: Theme.normal; easing.type: Easing.OutCubic } }
                add: Transition {
                    ParallelAnimation {
                        NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.slow }
                        NumberAnimation { property: "scale"; from: 0.96; to: 1; duration: Theme.slow; easing.type: Easing.OutBack }
                    }
                }
                remove: Transition { NumberAnimation { property: "opacity"; to: 0; duration: Theme.normal } }

                delegate: Card {
                    width: subList.width
                    padding: 16
                    hoverable: true
                    glow: model.status === "running"
                    glowColor: Theme.cyan

                    RowLayout {
                        width: parent.width
                        spacing: 14

                        Rectangle {
                            Layout.alignment: Qt.AlignTop
                            width: 30; height: 30; radius: 15
                            color: Theme.alpha(Theme.statusColor(model.status), 0.16)
                            border.color: Theme.alpha(Theme.statusColor(model.status), 0.5)
                            AText { anchors.centerIn: parent; text: model.index; weight: Font.Bold; size: Theme.fsSmall; color: Theme.statusColor(model.status) }
                        }

                        ColumnLayout {
                            Layout.fillWidth: true
                            spacing: 6
                            RowLayout {
                                Layout.fillWidth: true
                                spacing: 8
                                AText { text: model.title; weight: Font.DemiBold; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone }
                                Badge {
                                    text: model.statusTitle
                                    tint: Theme.statusColor(model.status)
                                }
                            }
                            Flow {
                                Layout.fillWidth: true
                                spacing: 6
                                Badge {
                                    text: model.agentName
                                    icon: model.agentId >= 0 ? "bot" : "circle-alert"
                                    tone: model.agentId >= 0 ? "violet" : "warning"
                                }
                                Repeater {
                                    model: depsHolder.titles
                                    delegate: Badge {
                                        required property string modelData
                                        text: modelData
                                        icon: "git-branch"
                                        tone: "muted"
                                    }
                                }
                                Badge { visible: model.reworks > 0; text: i18n.fmt(i18n.t["task.reworks"], { n: model.reworks }); tone: "warning"; icon: "rotate-ccw" }
                                Badge { visible: model.tokens !== "0"; text: model.tokens + " · " + model.cost; tone: "muted"; icon: "coins" }
                            }
                            Item { id: depsHolder; property var titles: model.depTitles; visible: false }
                            AText {
                                visible: model.description !== ""
                                text: model.description
                                dim: true
                                size: Theme.fsSmall
                                wrapMode: Text.Wrap
                                maximumLineCount: 3
                                Layout.fillWidth: true
                            }
                            Rectangle {
                                visible: model.result !== ""
                                Layout.fillWidth: true
                                radius: Theme.radiusS
                                color: Theme.alpha(Theme.success, 0.06)
                                border.color: Theme.alpha(Theme.success, 0.2)
                                implicitHeight: resultText.implicitHeight + 16
                                AText {
                                    id: resultText
                                    anchors.fill: parent
                                    anchors.margins: 8
                                    text: model.resultPreview
                                    size: Theme.fsSmall
                                    dim: true
                                    wrapMode: Text.Wrap
                                    maximumLineCount: 3
                                }
                            }
                        }

                        ColumnLayout {
                            Layout.alignment: Qt.AlignTop
                            spacing: 2
                            RowLayout {
                                spacing: 2
                                IconButton { iconName: "chevron-up"; size: 28; enabled: index > 0; tip: i18n.t["task.move_up"]; onClicked: page.ctl.move(model.id, -1) }
                                IconButton { iconName: "chevron-down"; size: 28; enabled: index < subList.count - 1; tip: i18n.t["task.move_down"]; onClicked: page.ctl.move(model.id, 1) }
                            }
                            RowLayout {
                                spacing: 2
                                IconButton { iconName: "pencil"; size: 28; tip: i18n.t["common.edit"]; onClicked: subEditor.openEdit(page.ctl.subtasks.get(index)) }
                                IconButton {
                                    iconName: "trash-2"; size: 28; danger: true; tip: i18n.t["common.delete"]
                                    onClicked: confirm.ask(i18n.t["task.delete_subtask"], model.title, function() { page.ctl.removeSubtask(model.id) })
                                }
                            }
                            IconButton {
                                visible: model.status === "done" || model.status === "error" || model.status === "review"
                                iconName: "rotate-ccw"; size: 28; tip: i18n.t["task.rerun"]
                                onClicked: page.ctl.resetSubtask(model.id)
                            }
                        }
                    }
                }
            }
        }
    }

    Confirm {
        id: confirm
        confirmText: i18n.t["common.delete"]
        cancelText: i18n.t["common.cancel"]
    }

    Sheet {
        id: subEditor
        property int subId: -1
        property var deps: []
        property int agentId: -1
        property string error: ""
        title: subId >= 0 ? i18n.t["task.edit_subtask"] : i18n.t["task.add_subtask"]
        icon: "workflow"
        sheetWidth: 620

        function openNew() {
            subId = -1; deps = []; error = ""
            agentId = page.ctl.agentOptions.length ? page.ctl.agentOptions[0].id : -1
            subTitle.text = ""; subDesc.text = ""
            open(); subTitle.focusInput()
        }
        function openEdit(d) {
            subId = d.id; deps = d.deps; error = ""
            agentId = d.agentId
            subTitle.text = d.title; subDesc.text = d.description
            open()
        }
        function toggleDep(id, on) {
            var list = deps.slice()
            var i = list.indexOf(id)
            if (on && i < 0) list.push(id)
            if (!on && i >= 0) list.splice(i, 1)
            deps = list
        }
        function save() {
            var err = page.ctl.saveSubtask({ id: subId, title: subTitle.text, description: subDesc.text,
                                             agentId: agentId, deps: deps })
            if (err === "") close(); else error = err
        }

        Field { id: subTitle; Layout.fillWidth: true; label: i18n.t["task.subtask_title"]; icon: "square-pen"; error: subEditor.error }
        TextBox { id: subDesc; Layout.fillWidth: true; label: i18n.t["common.description"]; minHeight: 120 }
        Select {
            Layout.fillWidth: true
            label: i18n.t["task.assignee"]
            icon: "bot"
            options: [{ value: -1, title: i18n.t["task.unassigned"] }].concat(
                         page.ctl.agentOptions.map(function(a) { return { value: a.id, title: a.name + " · " + a.model } }))
            value: subEditor.agentId
            onPicked: function(v) { subEditor.agentId = v }
        }
        SectionTitle { Layout.fillWidth: true; text: i18n.t["task.depends_on"]; hint: i18n.t["task.depends_hint"]; icon: "git-branch" }
        Flow {
            Layout.fillWidth: true
            spacing: 8
            Repeater {
                model: page.ctl.subtasks
                delegate: Chip {
                    visible: model.id !== subEditor.subId
                    text: model.index + ". " + model.title
                    isOn: subEditor.deps.indexOf(model.id) >= 0
                    onClicked: subEditor.toggleDep(model.id, checked)
                }
            }
        }
        AText {
            visible: page.ctl.subtasks.count <= (subEditor.subId >= 0 ? 1 : 0)
            text: i18n.t["task.no_deps_possible"]
            mute: true
            size: Theme.fsSmall
        }

        footer: [
            Item { Layout.fillWidth: true },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: subEditor.close() },
            Button { text: i18n.t["common.save"]; variant: "primary"; iconName: "check"; onClicked: subEditor.save() }
        ]
    }
}
````

### `ui/qml/pages/Run.qml`

*581 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts
import QtQuick.Shapes
import Ao

// Выполнение: управление прогоном, решения человека, живые рассуждения
// агентов, граф подзадач и лента событий.
Page {
    id: page
    title: i18n.t["run.title"]
    subtitle: backend.run.taskTitle !== "" ? backend.run.taskTitle : i18n.t["run.subtitle"]
    icon: "play"
    fill: true
    readonly property var ctl: backend.run

    headerActions: [
        Button {
            visible: !backend.running
            variant: "primary"
            iconName: "play"
            text: i18n.t["run.start"]
            loading: page.ctl.starting
            enabled: page.ctl.canStart && !page.ctl.starting
            onClicked: page.ctl.start()
        },
        Button {
            visible: backend.running
            iconName: backend.paused ? "circle-play" : "circle-pause"
            text: backend.paused ? i18n.t["run.resume"] : i18n.t["run.pause"]
            onClicked: page.ctl.togglePause()
        },
        Button {
            visible: backend.running
            variant: "danger"
            iconName: "square"
            text: i18n.t["run.stop"]
            onClicked: confirm.ask(i18n.t["run.stop"], i18n.t["run.stop_confirm"],
                                   function() { page.ctl.stop() }, true, i18n.t["run.stop"])
        }
    ]

    // --- сводка прогона ------------------------------------------------------
    Card {
        Layout.fillWidth: true
        padding: 16
        RowLayout {
            width: parent.width
            spacing: 22
            ProgressRing {
                size: 64
                thickness: 6
                value: page.ctl.progress
                label: page.ctl.total > 0 ? Math.round(page.ctl.progress * 100) + "%" : "-"
            }
            Kpi { caption: i18n.t["run.k_done"]; value: page.ctl.done + " / " + page.ctl.total; tint: Theme.success }
            Kpi { caption: i18n.t["run.k_review"]; value: page.ctl.review; tint: page.ctl.review ? Theme.violetSoft : Theme.text }
            Kpi { caption: i18n.t["run.k_errors"]; value: page.ctl.errors; tint: page.ctl.errors ? Theme.danger : Theme.text }
            Kpi { caption: i18n.t["run.k_time"]; value: backend.runElapsed !== "" ? backend.runElapsed : "-" }
            Kpi { caption: i18n.t["run.k_tokens"]; value: backend.running ? backend.runTokens : "-" }
            Kpi { caption: i18n.t["run.k_cost"]; value: backend.running ? backend.runCost : "-"; tint: Theme.teal }
            Item { Layout.fillWidth: true }
            // Почему нельзя запустить - сразу видно, без попытки.
            RowLayout {
                visible: !backend.running && page.ctl.blocker !== ""
                spacing: 8
                Icon { name: "info"; size: 15; color: Theme.warning }
                AText { text: page.ctl.blocker; color: Theme.warning; size: Theme.fsSmall; Layout.maximumWidth: 360; wrapMode: Text.Wrap; elide: Text.ElideNone }
            }
        }
    }

    // --- решения человека ------------------------------------------------------
    Repeater {
        model: page.ctl.approvals
        delegate: Card {
            id: ask
            Layout.fillWidth: true
            glow: true
            glowColor: Theme.warning
            padding: 18
            stagger: 0
            property bool expanded: false
            readonly property var opts: model.options
            readonly property int approvalId: model.id

            ColumnLayout {
                width: parent.width
                spacing: 12
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12
                    Rectangle {
                        width: 38; height: 38; radius: 12
                        color: Theme.alpha(Theme.warning, 0.16)
                        Icon { anchors.centerIn: parent; name: model.icon; size: 18; color: Theme.warning }
                    }
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 2
                        RowLayout {
                            spacing: 8
                            AText { text: model.reasonTitle; weight: Font.Bold; color: Theme.warning }
                            AText { visible: model.agent !== ""; text: "· " + model.agent; dim: true }
                        }
                        AText { text: model.question; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone }
                    }
                    Button {
                        visible: model.details !== ""
                        compact: true
                        variant: "ghost"
                        iconName: ask.expanded ? "chevron-up" : "chevron-down"
                        text: ask.expanded ? i18n.t["run.hide_details"] : i18n.t["run.show_details"]
                        onClicked: ask.expanded = !ask.expanded
                    }
                }
                Rectangle {
                    visible: ask.expanded
                    Layout.fillWidth: true
                    radius: Theme.radius
                    color: Theme.input
                    border.color: Theme.border
                    implicitHeight: Math.min(detailsText.implicitHeight + 20, 260)
                    clip: true
                    Flickable {
                        anchors.fill: parent
                        anchors.margins: 10
                        contentHeight: detailsText.implicitHeight
                        T.ScrollBar.vertical: ScrollBar {}
                        AText {
                            id: detailsText
                            width: parent.width
                            text: model.details
                            dim: true
                            size: Theme.fsSmall
                            wrapMode: Text.Wrap
                            elide: Text.ElideNone
                        }
                    }
                }
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10
                    Field {
                        id: comment
                        Layout.fillWidth: true
                        placeholder: i18n.t["run.comment_placeholder"]
                        icon: "message-square-text"
                    }
                    Repeater {
                        model: ask.opts
                        delegate: Button {
                            required property var modelData
                            text: modelData.title
                            variant: modelData.value === "approve" || modelData.value === "extend" ? "primary"
                                   : modelData.value === "abort" ? "danger" : "secondary"
                            iconName: modelData.value === "approve" ? "check"
                                    : modelData.value === "rework" ? "rotate-ccw"
                                    : modelData.value === "skip" ? "skip-forward"
                                    : modelData.value === "extend" ? "trending-up" : "octagon-x"
                            onClicked: page.ctl.decide(ask.approvalId, modelData.value, comment.text)
                        }
                    }
                }
            }
        }
    }

    // --- основная область --------------------------------------------------------
    RowLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        spacing: 18

        // Живые рассуждения агентов.
        ColumnLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true
            spacing: 12
            SectionTitle {
                Layout.fillWidth: true
                text: i18n.t["run.live"]
                hint: i18n.t["run.live_hint"]
                icon: "brain"
            }
            GridView {
                id: streams
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                model: page.ctl.streams
                readonly property int cols: Math.max(1, Math.floor(width / 420))
                cellWidth: Math.floor(width / cols)
                cellHeight: Math.max(300, Math.floor(height / Math.ceil(Math.max(1, count) / cols)))
                boundsBehavior: Flickable.StopAtBounds
                T.ScrollBar.vertical: ScrollBar {}
                delegate: Item {
                    width: streams.cellWidth
                    height: streams.cellHeight
                    StreamCard {
                        anchors.fill: parent
                        anchors.rightMargin: 12
                        anchors.bottomMargin: 12
                    }
                }
            }
        }

        // Граф и лента.
        ColumnLayout {
            Layout.preferredWidth: Math.min(460, page.contentWidth * 0.38)
            Layout.fillHeight: true
            spacing: 12

            SectionTitle { Layout.fillWidth: true; text: i18n.t["run.graph"]; icon: "workflow" }
            Card {
                Layout.fillWidth: true
                Layout.preferredHeight: 260
                padding: 0
                Graph { anchors.fill: parent; anchors.margins: 12 }
            }

            SectionTitle {
                Layout.fillWidth: true
                text: i18n.t["run.feed"]
                icon: "activity"
                Segmented {
                    id: feedFilter
                    property string mode: "all"
                    options: [{ value: "all", title: i18n.t["run.f_all"] }, { value: "key", title: i18n.t["run.f_key"] },
                              { value: "error", title: i18n.t["run.f_errors"] }]
                    value: mode
                    onPicked: function(v) { mode = v }
                }
                IconButton { iconName: "eraser"; tip: i18n.t["run.clear_feed"]; onClicked: page.ctl.clearFeed() }
            }
            Card {
                Layout.fillWidth: true
                Layout.fillHeight: true
                padding: 6
                ListView {
                    id: feed
                    anchors.fill: parent
                    clip: true
                    model: page.ctl.feed
                    spacing: 0
                    boundsBehavior: Flickable.StopAtBounds
                    T.ScrollBar.vertical: ScrollBar {}
                    property bool follow: true
                    onCountChanged: if (follow) Qt.callLater(positionViewAtEnd)
                    onMovementEnded: follow = atYEnd
                    add: Transition { NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.normal } }
                    delegate: Item {
                        readonly property bool shown: feedFilter.mode === "all"
                                                   || (feedFilter.mode === "error" && model.tone === "error")
                                                   || (feedFilter.mode === "key" && model.tone !== "muted")
                        width: feed.width
                        height: shown ? row.implicitHeight + 10 : 0
                        visible: shown
                        RowLayout {
                            id: row
                            anchors { left: parent.left; right: parent.right; verticalCenter: parent.verticalCenter; leftMargin: 8; rightMargin: 8 }
                            spacing: 8
                            AText { text: model.time; mono: true; size: Theme.fsMicro; mute: true; Layout.alignment: Qt.AlignTop; topPadding: 2 }
                            Rectangle { width: 6; height: 6; radius: 3; color: Theme.tone(model.tone); Layout.alignment: Qt.AlignTop; Layout.topMargin: 6 }
                            AText {
                                Layout.fillWidth: true
                                text: "<b>" + model.agent.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</b>  "
                                      + model.message.replace(/&/g, "&amp;").replace(/</g, "&lt;")
                                textFormat: Text.StyledText
                                size: Theme.fsSmall
                                color: model.tone === "muted" ? Theme.textMute : Theme.textDim
                                wrapMode: Text.Wrap
                                elide: Text.ElideNone
                            }
                        }
                    }
                    AText {
                        anchors.centerIn: parent
                        visible: feed.count === 0
                        text: i18n.t["run.feed_empty"]
                        mute: true
                    }
                }
            }
        }
    }

    Confirm {
        id: confirm
        confirmText: i18n.t["run.stop"]
        cancelText: i18n.t["common.cancel"]
    }

    // --- компоненты страницы -------------------------------------------------------
    component Kpi: ColumnLayout {
        property string caption: ""
        property var value: ""
        property color tint: Theme.text
        spacing: 2
        AText { text: value; size: Theme.fsH2; weight: Font.Bold; color: tint; mono: true }
        AText { text: caption; size: Theme.fsMicro; mute: true }
    }

    // Карточка агента с живым потоком рассуждения.
    component StreamCard: Card {
        id: sc
        padding: 0
        glow: model.live
        glowColor: model.isSupervisor ? Theme.magenta : Theme.cyan
        readonly property string phaseTitle: model.phase === "tool" ? i18n.t["run.ph_tool"]
                                            : model.phase === "thinking" ? i18n.t["run.ph_thinking"]
                                            : model.phase === "review" ? i18n.t["run.ph_review"]
                                            : model.phase === "done" ? i18n.t["run.ph_done"]
                                            : model.phase === "error" ? i18n.t["run.ph_error"] : i18n.t["run.ph_idle"]

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 14
            spacing: 10

            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                Item {
                    width: 36; height: 36
                    Rectangle {
                        anchors.fill: parent
                        radius: 18
                        gradient: Gradient {
                            GradientStop { position: 0; color: model.isSupervisor ? Theme.magenta : Theme.violet }
                            GradientStop { position: 1; color: model.isSupervisor ? Theme.violetSoft : Theme.cyan }
                        }
                        Icon { anchors.centerIn: parent; name: model.icon; size: 16; color: "white" }
                    }
                    // Вращающееся кольцо вокруг аватара, пока агент работает.
                    Rectangle {
                        anchors.centerIn: parent
                        width: 44; height: 44; radius: 22
                        color: "transparent"
                        border.width: 2
                        border.color: Theme.alpha(sc.glowColor, 0.5)
                        visible: model.live
                        opacity: 0.8
                        SequentialAnimation on scale {
                            running: model.live && Theme.rich
                            loops: Animation.Infinite
                            NumberAnimation { from: 0.92; to: 1.08; duration: 900; easing.type: Easing.InOutSine }
                            NumberAnimation { from: 1.08; to: 0.92; duration: 900; easing.type: Easing.InOutSine }
                        }
                    }
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 1
                    RowLayout {
                        spacing: 6
                        AText { text: model.name; weight: Font.DemiBold; Layout.maximumWidth: 170 }
                        AText { text: model.modelName; mono: true; size: Theme.fsMicro; mute: true; Layout.maximumWidth: 150 }
                    }
                    AText {
                        text: model.subtask !== "" ? model.subtask : i18n.t["run.waiting"]
                        dim: model.subtask !== ""
                        mute: model.subtask === ""
                        size: Theme.fsSmall
                        Layout.fillWidth: true
                    }
                }
                Badge {
                    text: sc.phaseTitle
                    tone: model.phase === "tool" ? "accent" : model.phase === "done" ? "success"
                        : model.phase === "error" ? "error" : model.phase === "idle" ? "muted" : "violet"
                    icon: model.phase === "tool" ? "zap" : model.phase === "done" ? "check" : ""
                }
                IconButton {
                    iconName: "copy"
                    size: 28
                    tip: i18n.t["run.copy_stream"]
                    onClicked: backend.copyText(page.ctl.fullText(model.id))
                }
            }

            // Шаги: точки заполняются по мере продвижения по ReAct-циклу.
            RowLayout {
                visible: model.maxSteps > 0
                spacing: 4
                Repeater {
                    model: sc.stepsCount
                    delegate: Rectangle {
                        required property int index
                        width: 16; height: 4; radius: 2
                        color: index < sc.currentStep ? (index === sc.currentStep - 1 && sc.isLive ? Theme.cyan : Theme.violet) : Theme.surface3
                        Behavior on color { ColorAnimation { duration: Theme.normal } }
                    }
                }
                AText {
                    visible: sc.currentStep > 0
                    text: i18n.fmt(i18n.t["run.step_of"], { n: sc.currentStep, m: sc.stepsCount })
                    size: Theme.fsMicro
                    mute: true
                    leftPadding: 6
                }
                Item { Layout.fillWidth: true }
                TypingDots { visible: sc.isLive && model.phase === "thinking" }
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.fillHeight: true
                radius: Theme.radius
                color: Theme.alpha(Theme.bg, 0.55)
                border.color: Theme.border
                clip: true

                Flickable {
                    id: flow
                    anchors.fill: parent
                    anchors.margins: 12
                    contentHeight: streamText.implicitHeight
                    boundsBehavior: Flickable.StopAtBounds
                    T.ScrollBar.vertical: ScrollBar {}
                    property bool follow: true
                    onContentHeightChanged: if (follow && contentHeight > height) contentY = contentHeight - height
                    onMovementEnded: follow = contentY >= contentHeight - height - 8
                    Text {
                        id: streamText
                        width: flow.width - 8
                        text: model.html
                        textFormat: Text.StyledText
                        wrapMode: Text.Wrap
                        color: Theme.text
                        font.family: Theme.monoFamily
                        font.pixelSize: 13
                        lineHeight: 1.15
                        renderType: Text.QtRendering
                    }
                }
                AText {
                    anchors.centerIn: parent
                    visible: model.html === ""
                    text: model.isSupervisor ? i18n.t["run.sup_empty"] : i18n.t["run.stream_empty"]
                    mute: true
                    size: Theme.fsSmall
                }
                Button {
                    visible: !flow.follow
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    anchors.margins: 10
                    compact: true
                    iconName: "arrow-down"
                    text: i18n.t["run.to_latest"]
                    onClicked: { flow.follow = true; flow.contentY = Math.max(0, flow.contentHeight - flow.height) }
                }
            }
        }
        readonly property int stepsCount: Math.min(model.maxSteps, 20)
        readonly property int currentStep: Math.min(model.step, stepsCount)
        readonly property bool isLive: model.live
    }

    // «Печатает…» - три прыгающие точки.
    component TypingDots: Row {
        spacing: 4
        Repeater {
            model: 3
            delegate: Rectangle {
                required property int index
                width: 5; height: 5; radius: 2.5
                color: Theme.cyan
                SequentialAnimation on opacity {
                    running: Theme.motion > 0
                    loops: Animation.Infinite
                    PauseAnimation { duration: index * 160 }
                    NumberAnimation { from: 0.25; to: 1; duration: 320 }
                    NumberAnimation { from: 1; to: 0.25; duration: 320 }
                    PauseAnimation { duration: (2 - index) * 160 }
                }
            }
        }
    }

    // Граф подзадач: слои по зависимостям, рёбра «текут», пока идёт работа.
    component Graph: Flickable {
        id: graph
        // Узлы сужаются, чтобы все слои графа помещались в колонку без прокрутки.
        readonly property int nodeW: page.ctl.levels > 0
            ? Math.max(118, Math.min(170, Math.floor((width - gapX * (page.ctl.levels - 1)) / page.ctl.levels)))
            : 170
        readonly property int nodeH: 54
        readonly property int gapX: 34
        readonly property int gapY: 12
        clip: true
        contentWidth: Math.max(width, page.ctl.levels * (nodeW + gapX) - gapX)
        contentHeight: Math.max(height, page.ctl.maxRows * (nodeH + gapY) - gapY)
        boundsBehavior: Flickable.StopAtBounds
        T.ScrollBar.vertical: ScrollBar {}
        T.ScrollBar.horizontal: ScrollBar {}

        Repeater {
            model: page.ctl.edges
            delegate: Shape {
                id: edge
                readonly property real x1: model.fromLevel * (graph.nodeW + graph.gapX) + graph.nodeW
                readonly property real y1: model.fromRow * (graph.nodeH + graph.gapY) + graph.nodeH / 2
                readonly property real x2: model.toLevel * (graph.nodeW + graph.gapX)
                readonly property real y2: model.toRow * (graph.nodeH + graph.gapY) + graph.nodeH / 2
                anchors.fill: parent
                preferredRendererType: Shape.CurveRenderer
                ShapePath {
                    id: path
                    strokeWidth: model.state === "active" ? 2 : 1.5
                    strokeColor: model.state === "active" ? Theme.cyan
                               : model.state === "done" ? Theme.alpha(Theme.success, 0.6) : Theme.borderStrong
                    fillColor: "transparent"
                    strokeStyle: model.state === "active" ? ShapePath.DashLine : ShapePath.SolidLine
                    dashPattern: [4, 3]
                    startX: edge.x1; startY: edge.y1
                    PathCubic {
                        x: edge.x2; y: edge.y2
                        control1X: edge.x1 + graph.gapX * 0.6; control1Y: edge.y1
                        control2X: edge.x2 - graph.gapX * 0.6; control2Y: edge.y2
                    }
                    NumberAnimation on dashOffset {
                        running: model.state === "active" && Theme.motion > 0
                        from: 7; to: 0; duration: 500; loops: Animation.Infinite
                    }
                }
            }
        }

        Repeater {
            model: page.ctl.nodes
            delegate: Rectangle {
                id: node
                x: model.level * (graph.nodeW + graph.gapX)
                y: model.row * (graph.nodeH + graph.gapY)
                width: graph.nodeW
                height: graph.nodeH
                radius: Theme.radius
                color: Theme.alpha(Theme.statusColor(model.status), 0.10)
                border.width: model.status === "running" ? 2 : 1
                border.color: Theme.alpha(Theme.statusColor(model.status), model.status === "idle" ? 0.35 : 0.8)
                Behavior on color { ColorAnimation { duration: Theme.normal } }
                Behavior on x { NumberAnimation { duration: Theme.slow; easing.type: Easing.OutCubic } }
                Behavior on y { NumberAnimation { duration: Theme.slow; easing.type: Easing.OutCubic } }
                scale: model.status === "done" ? 1 : 1
                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 8
                    spacing: 2
                    RowLayout {
                        spacing: 6
                        StatusDot { status: model.status; size: 7 }
                        AText { text: model.title; size: Theme.fsSmall; weight: Font.DemiBold; Layout.fillWidth: true }
                        Icon { visible: model.status === "done"; name: "check"; size: 13; color: Theme.success }
                    }
                    AText { text: model.agentName; size: Theme.fsMicro; mute: true; Layout.fillWidth: true }
                }
                Tip { text: model.title + " · " + model.statusTitle; shown: nodeHover.hovered }
                HoverHandler { id: nodeHover }
                // «Щелчок» при завершении подзадачи.
                SequentialAnimation {
                    id: pop
                    NumberAnimation { target: node; property: "scale"; to: 1.08; duration: 120; easing.type: Easing.OutQuad }
                    NumberAnimation { target: node; property: "scale"; to: 1.0; duration: 220; easing.type: Easing.OutBack }
                }
                property string lastStatus: model.status
                onLastStatusChanged: if (lastStatus === "done" && Theme.rich) pop.restart()
            }
        }

        AText {
            anchors.centerIn: parent
            visible: page.ctl.nodes.count === 0
            text: i18n.t["run.graph_empty"]
            mute: true
            size: Theme.fsSmall
        }
    }
}
````

### `ui/qml/pages/Supervisor.qml`

*246 строк*

````qml
import QtQuick
import QtQuick.Layouts
import Ao

// Супервайзер: кто проверяет, анонимные сводки, инциденты и решения человека.
Page {
    id: page
    title: i18n.t["sup.title"]
    subtitle: i18n.t["sup.subtitle"]
    icon: "shield-check"
    readonly property var ctl: backend.supervisor
    property string tab: "summaries"

    headerActions: [
        Button {
            variant: "primary"
            iconName: "scroll-text"
            text: i18n.t["sup.make_summary"]
            loading: page.ctl.summarizing
            enabled: backend.workspaceId >= 0 && !backend.running && !page.ctl.summarizing
            onClicked: page.ctl.makeSummary()
        }
    ]

    // Кто сейчас супервайзер.
    Card {
        Layout.fillWidth: true
        padding: 16
        glow: page.ctl.configured
        glowColor: Theme.magenta
        RowLayout {
            width: parent.width
            spacing: 14
            Rectangle {
                width: 42; height: 42; radius: 21
                gradient: Gradient {
                    GradientStop { position: 0; color: page.ctl.configured ? Theme.magenta : Theme.surface3 }
                    GradientStop { position: 1; color: page.ctl.configured ? Theme.violetSoft : Theme.surface2 }
                }
                Icon { anchors.centerIn: parent; name: page.ctl.mode === "local" ? "hard-drive" : "shield-check"; size: 18; color: "white" }
            }
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 2
                AText { text: page.ctl.modelTitle; weight: Font.DemiBold; Layout.fillWidth: true }
                AText {
                    text: page.ctl.configured ? i18n.t["sup.checklist"] : i18n.t["sup.configure_hint"]
                    dim: true
                    size: Theme.fsSmall
                    Layout.fillWidth: true
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                }
            }
            Badge {
                text: page.ctl.mode === "local" ? i18n.t["sup.mode_local"] : i18n.t["sup.mode_api"]
                tone: page.ctl.mode === "local" ? "accent" : "violet"
            }
            Button {
                compact: true
                iconName: "settings"
                text: i18n.t["nav.settings"]
                onClicked: backend.navigate("settings")
            }
        }
    }

    Segmented {
        options: [
            { value: "summaries", title: i18n.t["sup.summaries"] + " · " + page.ctl.summaries.count, icon: "scroll-text" },
            { value: "incidents", title: i18n.t["sup.incidents"] + " · " + page.ctl.incidents.count, icon: "triangle-alert" },
            { value: "decisions", title: i18n.t["sup.approvals"] + " · " + page.ctl.decisions.count, icon: "hand" }
        ]
        value: page.tab
        onPicked: function(v) { page.tab = v }
    }

    // --- сводки ---
    EmptyState {
        visible: page.tab === "summaries" && page.ctl.summaries.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 30
        icon: "scroll-text"
        title: i18n.t["sup.no_summaries_title"]
        text: i18n.t["sup.no_summaries"]
    }
    Repeater {
        model: page.tab === "summaries" ? page.ctl.summaries : null
        delegate: Card {
            Layout.fillWidth: true
            stagger: index
            ColumnLayout {
                width: parent.width
                spacing: 10
                RowLayout {
                    spacing: 10
                    Icon { name: "scroll-text"; size: 15; color: Theme.violetSoft }
                    AText { text: model.when; weight: Font.DemiBold }
                    Badge { text: model.triggerTitle; tone: model.trigger === "final" ? "success" : "violet" }
                    Item { Layout.fillWidth: true }
                    AText { text: i18n.fmt(i18n.t["sup.delivered"], { n: model.recipients }); mute: true; size: Theme.fsSmall }
                    IconButton { iconName: "copy"; size: 28; tip: i18n.t["common.copy"]; onClicked: backend.copyText(model.content) }
                }
                AText {
                    Layout.fillWidth: true
                    text: model.content
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                    dim: true
                    lineHeight: 1.2
                }
            }
        }
    }

    // --- инциденты ---
    EmptyState {
        visible: page.tab === "incidents" && page.ctl.incidents.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 30
        icon: "badge-check"
        title: i18n.t["sup.no_incidents_title"]
        text: i18n.t["sup.no_incidents"]
    }
    Repeater {
        model: page.tab === "incidents" ? page.ctl.incidents : null
        delegate: Card {
            Layout.fillWidth: true
            stagger: index
            padding: 16
            glow: model.status === "escalated"
            glowColor: Theme.warning
            RowLayout {
                width: parent.width
                spacing: 14
                Rectangle {
                    Layout.alignment: Qt.AlignTop
                    width: 34; height: 34; radius: 10
                    color: Theme.alpha(Theme.tone(model.tone), 0.15)
                    Icon { anchors.centerIn: parent; name: model.open ? "triangle-alert" : "circle-check"; size: 16; color: model.open ? Theme.tone(model.tone) : Theme.success }
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 5
                    RowLayout {
                        spacing: 8
                        AText { text: model.kindTitle; weight: Font.DemiBold }
                        Badge { text: model.severityTitle; tone: model.tone }
                        Badge { text: model.statusTitle; tone: model.open ? "warning" : "success" }
                        Item { Layout.fillWidth: true }
                        AText { text: model.when; mute: true; size: Theme.fsSmall }
                    }
                    AText { text: model.description; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone; dim: true }
                    AText {
                        visible: model.resolution !== ""
                        text: "→ " + model.resolution
                        Layout.fillWidth: true
                        wrapMode: Text.Wrap
                        elide: Text.ElideNone
                        mute: true
                        size: Theme.fsSmall
                    }
                }
                Button {
                    Layout.alignment: Qt.AlignTop
                    visible: model.open
                    compact: true
                    iconName: "check"
                    text: i18n.t["sup.resolve"]
                    onClicked: resolver.openFor(model.id, model.description)
                }
            }
        }
    }

    // --- решения ---
    EmptyState {
        visible: page.tab === "decisions" && page.ctl.decisions.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 30
        icon: "hand"
        title: i18n.t["sup.no_approvals_title"]
        text: i18n.t["sup.no_approvals"]
    }
    Repeater {
        model: page.tab === "decisions" ? page.ctl.decisions : null
        delegate: Card {
            Layout.fillWidth: true
            stagger: index
            padding: 16
            RowLayout {
                width: parent.width
                spacing: 14
                Rectangle {
                    Layout.alignment: Qt.AlignTop
                    width: 10; height: 10; radius: 5
                    Layout.topMargin: 5
                    color: Theme.tone(model.tone)
                }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 4
                    RowLayout {
                        spacing: 8
                        AText { text: model.reasonTitle; weight: Font.DemiBold }
                        Badge { text: model.decisionTitle; tone: model.tone }
                        Item { Layout.fillWidth: true }
                        AText { text: model.when; mute: true; size: Theme.fsSmall }
                    }
                    AText { text: model.question; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone; dim: true }
                    AText {
                        visible: model.comment !== "" || model.agent !== ""
                        text: [model.agent, model.comment].filter(function(x) { return x !== "" }).join(" · ")
                        mute: true
                        size: Theme.fsSmall
                        Layout.fillWidth: true
                        wrapMode: Text.Wrap
                        elide: Text.ElideNone
                    }
                }
            }
        }
    }

    Sheet {
        id: resolver
        property int incidentId: -1
        property string problem: ""
        title: i18n.t["sup.resolve"]
        subtitle: problem
        icon: "badge-check"
        sheetWidth: 520
        function openFor(id, text) { incidentId = id; problem = text; resolution.text = ""; open() }
        TextBox { id: resolution; Layout.fillWidth: true; label: i18n.t["sup.resolution"]; minHeight: 110 }
        footer: [
            Item { Layout.fillWidth: true },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: resolver.close() },
            Button {
                text: i18n.t["sup.resolve"]
                variant: "primary"
                iconName: "check"
                onClicked: { page.ctl.resolveIncident(resolver.incidentId, resolution.text); resolver.close() }
            }
        ]
    }
}
````

### `ui/qml/pages/Dashboard.qml`

*315 строк*

````qml
import QtQuick
import QtQuick.Layouts
import Ao

// Дашборд: метрики, прогресс, кривые расхода, агенты, лента и инциденты.
Page {
    id: page
    title: i18n.t["dash.title"]
    subtitle: i18n.t["dash.subtitle"]
    icon: "layout-dashboard"
    readonly property var ctl: backend.dashboard
    property string series: "cost"

    Component.onCompleted: ctl.refresh()

    headerActions: [
        IconButton { iconName: "refresh-cw"; tip: i18n.t["common.refresh"]; onClicked: page.ctl.refresh() }
    ]

    EmptyState {
        visible: backend.workspaceId < 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "layers"
        title: i18n.t["ws.empty_title"]
        text: i18n.t["ws.empty"]
        actionText: i18n.t["nav.workspaces"]
        actionIcon: "arrow-right"
        onAction: backend.navigate("workspaces")
    }

    // --- метрики ---------------------------------------------------------------
    GridLayout {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        columns: page.contentWidth > 1100 ? 6 : 3
        columnSpacing: 14
        rowSpacing: 14
        Metric { idx: 0; glyph: "bot"; caption: i18n.t["dash.m_agents"]; value: page.ctl.agentsCount }
        Metric {
            idx: 1; glyph: "list-checks"; caption: i18n.t["dash.m_subtasks"]
            value: page.ctl.done; total: page.ctl.total > 0 ? String(page.ctl.total) : ""
            tint: Theme.success
        }
        Metric {
            idx: 2; glyph: "coins"; unit: "tokens"; value: page.ctl.tokens
            caption: page.ctl.limitPct >= 0 ? i18n.fmt(i18n.t["dash.m_tokens_pct"], { pct: Math.round(page.ctl.limitPct * 100) })
                                            : i18n.t["dash.m_tokens"]
            tint: page.ctl.limitPct >= 1 ? Theme.danger : page.ctl.limitPct >= 0.8 ? Theme.warning : Theme.text
        }
        Metric { idx: 3; glyph: "dollar-sign"; unit: "usd"; caption: i18n.t["dash.m_cost"]; value: page.ctl.cost; tint: Theme.teal }
        Metric { idx: 4; glyph: "rotate-ccw"; caption: i18n.t["dash.m_reworks"]; value: page.ctl.reworks; tint: page.ctl.reworks ? Theme.warning : Theme.text }
        Metric {
            idx: 5; glyph: "triangle-alert"; caption: i18n.t["dash.m_open_incidents"]; value: page.ctl.openIncidents
            tint: page.ctl.openIncidents ? Theme.danger : Theme.text
            clickable: true
            onActivated: backend.navigate("supervisor")
        }
    }

    // --- прогресс --------------------------------------------------------------
    Card {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        stagger: 2
        ColumnLayout {
            width: parent.width
            spacing: 12
            RowLayout {
                Layout.fillWidth: true
                Icon { name: "list-checks"; color: Theme.violetSoft }
                AText {
                    text: page.ctl.taskTitle !== "" ? page.ctl.taskTitle : i18n.t["task.no_task"]
                    weight: Font.DemiBold
                    size: Theme.fsH3
                    Layout.fillWidth: true
                }
                AText {
                    visible: page.ctl.total > 0
                    text: page.ctl.done + " / " + page.ctl.total + "  ·  " + Math.round(page.ctl.total ? page.ctl.done / page.ctl.total * 100 : 0) + "%"
                    mono: true
                    dim: true
                }
            }
            SegmentBar { Layout.fillWidth: true; segments: page.ctl.segments }
        }
    }

    // --- графики ------------------------------------------------------------------
    RowLayout {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        spacing: 16
        Card {
            Layout.fillWidth: true
            Layout.preferredWidth: 3
            Layout.preferredHeight: 300
            stagger: 3
            ColumnLayout {
                anchors.fill: parent
                spacing: 12
                RowLayout {
                    Layout.fillWidth: true
                    SectionTitle { Layout.fillWidth: true; text: i18n.t["dash.spend"]; icon: "chart-line" }
                    Segmented {
                        options: [{ value: "cost", title: i18n.t["dash.money"] }, { value: "tokens", title: i18n.t["dash.tokens"] }]
                        value: page.series
                        onPicked: function(v) { page.series = v }
                    }
                }
                LineChart {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    points: page.series === "cost" ? page.ctl.costSeries : page.ctl.tokenSeries
                    unit: page.series === "cost" ? "usd" : "tokens"
                    lineColor: page.series === "cost" ? Theme.teal : Theme.violetSoft
                    fillColor: page.series === "cost" ? Theme.teal : Theme.violet
                    emptyText: i18n.t["dash.no_usage"]
                }
            }
        }
        Card {
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Layout.preferredHeight: 300
            stagger: 4
            ColumnLayout {
                anchors.fill: parent
                spacing: 12
                SectionTitle {
                    Layout.fillWidth: true
                    text: i18n.t["dash.by_agent"]
                    icon: "chart-bar"
                    Badge {
                        visible: page.ctl.supervisorShare > 0
                        text: i18n.fmt(i18n.t["dash.sup_share"], { pct: Math.round(page.ctl.supervisorShare * 100) })
                        tone: page.ctl.supervisorShare > 0.5 ? "warning" : "violet"
                        icon: "shield-check"
                    }
                }
                Flickable {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    contentHeight: bars.implicitHeight
                    BarList { id: bars; width: parent.width; bars: page.ctl.bars; emptyText: i18n.t["dash.no_usage"] }
                }
            }
        }
    }

    // --- агенты ------------------------------------------------------------------
    Card {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        stagger: 5
        ColumnLayout {
            width: parent.width
            spacing: 8
            SectionTitle { Layout.fillWidth: true; text: i18n.t["dash.agents"]; icon: "users" }
            AText { visible: page.ctl.agentsModel.count === 0; text: i18n.t["agents.empty"]; mute: true }
            Repeater {
                model: page.ctl.agentsModel
                delegate: Rectangle {
                    Layout.fillWidth: true
                    height: 46
                    radius: Theme.radius
                    color: rowHover.hovered ? Theme.alpha(Theme.surface3, 0.6) : "transparent"
                    HoverHandler { id: rowHover }
                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 10
                        anchors.rightMargin: 10
                        spacing: 12
                        StatusDot { status: model.status }
                        Icon { name: model.icon; size: 15; color: model.isSupervisor ? Theme.magenta : Theme.violetSoft }
                        AText { text: model.name; weight: Font.Medium; Layout.preferredWidth: 180 }
                        AText {
                            text: model.doing !== "" ? "→ " + model.doing : model.statusTitle
                            dim: model.doing !== ""
                            mute: model.doing === ""
                            size: Theme.fsSmall
                            Layout.fillWidth: true
                        }
                        Rectangle {
                            Layout.preferredWidth: 120
                            height: 5
                            radius: 3
                            color: Theme.surface3
                            Rectangle {
                                height: parent.height
                                radius: 3
                                width: parent.width * Math.min(1, model.share)
                                color: Theme.violet
                                Behavior on width { NumberAnimation { duration: Theme.slow } }
                            }
                        }
                        AText { text: model.tokens; mono: true; size: Theme.fsSmall; dim: true; Layout.preferredWidth: 70; horizontalAlignment: Text.AlignRight }
                        AText { text: model.cost; mono: true; size: Theme.fsSmall; color: Theme.teal; Layout.preferredWidth: 70; horizontalAlignment: Text.AlignRight }
                    }
                }
            }
        }
    }

    // --- лента и инциденты -------------------------------------------------------------
    RowLayout {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        spacing: 16
        Card {
            Layout.fillWidth: true
            Layout.preferredWidth: 3
            Layout.alignment: Qt.AlignTop
            stagger: 6
            ColumnLayout {
                width: parent.width
                spacing: 10
                SectionTitle { Layout.fillWidth: true; text: i18n.t["dash.feed"]; icon: "message-square-text" }
                AText { visible: page.ctl.feed.count === 0; text: i18n.t["dash.no_feed"]; mute: true; wrapMode: Text.Wrap; Layout.fillWidth: true }
                Repeater {
                    model: page.ctl.feed
                    delegate: ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 3
                        RowLayout {
                            Layout.fillWidth: true
                            spacing: 8
                            Rectangle { width: 6; height: 6; radius: 3; color: Theme.tone(model.tone) }
                            AText { text: model.who; weight: Font.DemiBold; size: Theme.fsSmall; color: Theme.tone(model.tone) }
                            Badge { visible: model.badge !== ""; text: model.badge; tone: model.tone }
                            AText { visible: model.confidence !== ""; text: i18n.t["dash.confidence"] + " " + model.confidence; mute: true; size: Theme.fsMicro }
                            Item { Layout.fillWidth: true }
                            AText { text: model.when; mute: true; mono: true; size: Theme.fsMicro }
                        }
                        AText { text: model.text; dim: true; size: Theme.fsSmall; Layout.fillWidth: true; wrapMode: Text.Wrap; maximumLineCount: 2; leftPadding: 14 }
                    }
                }
            }
        }
        Card {
            Layout.fillWidth: true
            Layout.preferredWidth: 2
            Layout.alignment: Qt.AlignTop
            stagger: 7
            ColumnLayout {
                width: parent.width
                spacing: 10
                SectionTitle { Layout.fillWidth: true; text: i18n.t["dash.incidents"]; icon: "triangle-alert" }
                AText { visible: page.ctl.incidents.count === 0; text: i18n.t["sup.no_incidents"]; mute: true; wrapMode: Text.Wrap; Layout.fillWidth: true }
                Repeater {
                    model: page.ctl.incidents
                    delegate: ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 3
                        RowLayout {
                            Layout.fillWidth: true
                            AText { text: model.kindTitle; weight: Font.DemiBold; size: Theme.fsSmall; color: Theme.tone(model.tone) }
                            Item { Layout.fillWidth: true }
                            AText { text: model.statusTitle; mute: true; size: Theme.fsMicro }
                        }
                        AText { text: model.description; dim: true; size: Theme.fsSmall; Layout.fillWidth: true; wrapMode: Text.Wrap; maximumLineCount: 2 }
                    }
                }
            }
        }
    }

    // Крупная метрика с «досчитывающим» числом.
    component Metric: Card {
        id: metric
        property int idx: 0
        property string glyph: ""
        property string caption: ""
        property real value: 0
        property string total: ""
        property string unit: "int"
        property color tint: Theme.text
        property bool clickable: false
        signal activated()
        Layout.fillWidth: true
        stagger: idx
        hoverable: true
        padding: 16
        ColumnLayout {
            width: parent.width
            spacing: 6
            RowLayout {
                Layout.fillWidth: true
                Rectangle {
                    width: 30; height: 30; radius: 9
                    color: Theme.alpha(metric.tint === Theme.text ? Theme.violet : metric.tint, 0.14)
                    Icon { anchors.centerIn: parent; name: metric.glyph; size: 15; color: metric.tint === Theme.text ? Theme.violetSoft : metric.tint }
                }
                Item { Layout.fillWidth: true }
                Icon { visible: metric.clickable; name: "arrow-up-right"; size: 14; color: Theme.textMute }
            }
            Ticker {
                value: metric.value
                unit: metric.unit
                total: metric.total
                size: 26
                weight: Font.Bold
                color: metric.tint
            }
            AText { text: metric.caption; mute: true; size: Theme.fsSmall; Layout.fillWidth: true }
        }
        MouseArea {
            anchors.fill: parent
            enabled: metric.clickable
            cursorShape: Qt.PointingHandCursor
            onClicked: metric.activated()
        }
    }
}
````

### `ui/qml/pages/Budget.qml`

*189 строк*

````qml
import QtQuick
import QtQuick.Layouts
import Ao

// Бюджеты: по одной карточке на уровень (проект, задача, агент) с живой
// шкалой расхода и полями лимитов, которые сохраняются по Enter.
Page {
    id: page
    title: i18n.t["bud.title"]
    subtitle: i18n.t["bud.subtitle"]
    icon: "wallet"
    readonly property var ctl: backend.budget

    Component.onCompleted: ctl.refresh()

    headerActions: [
        IconButton { iconName: "refresh-cw"; tip: i18n.t["common.refresh"]; onClicked: page.ctl.refresh() }
    ]

    // Последний алерт бюджета.
    Rectangle {
        visible: page.ctl.alert !== ""
        Layout.fillWidth: true
        radius: Theme.radius
        color: Theme.alpha(Theme.tone(page.ctl.alertTone), 0.1)
        border.color: Theme.alpha(Theme.tone(page.ctl.alertTone), 0.4)
        implicitHeight: alertRow.implicitHeight + 22
        RowLayout {
            id: alertRow
            anchors.fill: parent
            anchors.margins: 11
            spacing: 10
            Icon { name: page.ctl.alertTone === "error" ? "octagon-x" : "triangle-alert"; color: Theme.tone(page.ctl.alertTone) }
            AText { text: page.ctl.alert; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone; color: Theme.tone(page.ctl.alertTone) }
            IconButton { iconName: "x"; size: 26; onClicked: page.ctl.dismissAlert() }
        }
    }

    // Как работает бюджет - коротко, один раз.
    Card {
        Layout.fillWidth: true
        padding: 16
        RowLayout {
            width: parent.width
            spacing: 18
            Hint { glyph: "shield-check"; text: i18n.t["bud.h_before"] }
            Hint { glyph: "hand"; text: i18n.t["bud.h_ask"] }
            Hint { glyph: "database"; text: i18n.t["bud.h_log"] }
        }
    }

    EmptyState {
        visible: page.ctl.model.count === 0
        Layout.fillWidth: true
        Layout.topMargin: 40
        icon: "wallet"
        title: i18n.t["bud.nothing_title"]
        text: i18n.t["bud.nothing"]
    }

    Repeater {
        model: page.ctl.model
        delegate: Card {
            id: row
            Layout.fillWidth: true
            stagger: index
            hoverable: true
            glow: model.exceeded
            glowColor: Theme.danger
            property string error: ""
            readonly property color barColor: model.ratio >= 1 ? Theme.danger : model.ratio >= model.threshold ? Theme.warning : Theme.violet

            function save(tokens, cost, threshold) {
                row.error = page.ctl.save(model.scope, model.scopeId, tokens, cost, threshold)
            }

            ColumnLayout {
                width: parent.width
                spacing: 14

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12
                    Rectangle {
                        width: 38; height: 38; radius: 12
                        color: Theme.alpha(Theme.violet, 0.14)
                        Icon { anchors.centerIn: parent; name: model.icon; size: 17; color: Theme.violetSoft }
                    }
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 1
                        AText { text: model.name; weight: Font.DemiBold; size: Theme.fsH3; Layout.fillWidth: true }
                        AText { text: model.scopeTitle; mute: true; size: Theme.fsSmall }
                    }
                    ColumnLayout {
                        spacing: 1
                        AText { text: model.tokensText + " " + i18n.t["bud.tokens_short"]; mono: true; Layout.alignment: Qt.AlignRight }
                        AText { text: model.costText; mono: true; color: Theme.teal; Layout.alignment: Qt.AlignRight }
                    }
                }

                // Шкала расхода.
                ColumnLayout {
                    visible: model.isSet
                    Layout.fillWidth: true
                    spacing: 6
                    Rectangle {
                        Layout.fillWidth: true
                        height: 10
                        radius: 5
                        color: Theme.surface3
                        Rectangle {
                            height: parent.height
                            radius: 5
                            width: parent.width * Math.min(1, model.ratio)
                            gradient: Gradient {
                                orientation: Gradient.Horizontal
                                GradientStop { position: 0; color: Theme.alpha(row.barColor, 0.7) }
                                GradientStop { position: 1; color: row.barColor }
                            }
                            Behavior on width { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }
                        }
                        // Отметка порога алерта.
                        Rectangle {
                            x: parent.width * model.threshold - 1
                            width: 2
                            height: parent.height + 6
                            y: -3
                            radius: 1
                            color: Theme.warning
                            opacity: 0.8
                        }
                    }
                    AText {
                        text: model.exceeded ? i18n.t["bud.exceeded"] : i18n.fmt(i18n.t["bud.used_pct"], { pct: Math.round(model.ratio * 100) })
                        color: row.barColor
                        size: Theme.fsSmall
                    }
                }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 14
                    Field {
                        id: tokField
                        Layout.fillWidth: true
                        label: i18n.t["bud.token_limit"]
                        placeholder: i18n.t["bud.no_limit"]
                        text: model.tokenLimit
                        icon: "coins"
                        mono: true
                        onAccepted: row.save(tokField.text, costField.text, thr.value)
                        onEditingFinished: if (tokField.text !== model.tokenLimit) row.save(tokField.text, costField.text, thr.value)
                    }
                    Field {
                        id: costField
                        Layout.fillWidth: true
                        label: i18n.t["bud.cost_limit"]
                        placeholder: i18n.t["bud.no_limit"]
                        text: model.costLimit
                        icon: "dollar-sign"
                        mono: true
                        onAccepted: row.save(tokField.text, costField.text, thr.value)
                        onEditingFinished: if (costField.text !== model.costLimit) row.save(tokField.text, costField.text, thr.value)
                    }
                    RangeSlider {
                        id: thr
                        Layout.preferredWidth: 220
                        label: i18n.t["bud.alert_at"]
                        from: 0.1; to: 1; stepSize: 0.05
                        value: model.threshold
                        format: function(v) { return Math.round(v * 100) + "%" }
                        onCommitted: function(v) { if (model.isSet) row.save(tokField.text, costField.text, v) }
                    }
                }
                AText { visible: row.error !== ""; text: row.error; color: Theme.danger; size: Theme.fsSmall }
            }
        }
    }

    component Hint: RowLayout {
        property string glyph: ""
        property string text: ""
        Layout.fillWidth: true
        spacing: 10
        Icon { name: glyph; size: 16; color: Theme.violetSoft; Layout.alignment: Qt.AlignTop }
        AText { text: parent.text; dim: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
    }
}
````

### `ui/qml/pages/Export.qml`

*173 строк*

````qml
import QtQuick
import QtQuick.Layouts
import Ao

// Экспорт: формат выбирается плиткой (рекомендованный отмечен и объяснён),
// состав документа - переключателями, путь - полем с кнопкой «Обзор».
Page {
    id: page
    title: i18n.t["exp.title"]
    subtitle: i18n.t["exp.subtitle"]
    icon: "package"
    readonly property var ctl: backend.exporter

    Component.onCompleted: ctl.refresh()

    headerActions: [
        IconButton { iconName: "refresh-cw"; tip: i18n.t["common.refresh"]; onClicked: page.ctl.refresh() }
    ]

    EmptyState {
        visible: backend.workspaceId < 0
        Layout.fillWidth: true
        Layout.topMargin: 60
        icon: "layers"
        title: i18n.t["ws.empty_title"]
        text: i18n.t["ws.empty"]
    }

    ColumnLayout {
        visible: backend.workspaceId >= 0
        Layout.fillWidth: true
        spacing: 18

        // Статистика и рекомендация.
        Card {
            Layout.fillWidth: true
            padding: 16
            RowLayout {
                width: parent.width
                spacing: 12
                Icon { name: page.ctl.nothing ? "inbox" : "wand-sparkles"; size: 18; color: page.ctl.nothing ? Theme.textMute : Theme.violetSoft }
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 2
                    AText {
                        text: page.ctl.nothing ? i18n.t["exp.nothing"] : i18n.fmt(i18n.t["exp.auto_hint"], { reason: page.ctl.reason })
                        Layout.fillWidth: true
                        wrapMode: Text.Wrap
                        elide: Text.ElideNone
                    }
                    AText { text: page.ctl.stats; mute: true; size: Theme.fsSmall }
                }
            }
        }

        SectionTitle { Layout.fillWidth: true; text: i18n.t["exp.format"]; icon: "file-type" }
        GridLayout {
            Layout.fillWidth: true
            columns: 4
            columnSpacing: 14
            Repeater {
                model: page.ctl.formats
                delegate: Card {
                    id: fmtCard
                    required property var modelData
                    required property int index
                    readonly property bool chosen: page.ctl.format === modelData.key
                    readonly property bool recommended: page.ctl.recommended === modelData.key
                    Layout.fillWidth: true
                    Layout.preferredHeight: 150
                    hoverable: true
                    glow: chosen
                    stagger: index
                    ColumnLayout {
                        anchors.fill: parent
                        spacing: 8
                        RowLayout {
                            Layout.fillWidth: true
                            Rectangle {
                                width: 40; height: 40; radius: 12
                                color: fmtCard.chosen ? Theme.alpha(Theme.violet, 0.3) : Theme.surface3
                                Icon { anchors.centerIn: parent; name: fmtCard.modelData.icon; size: 18; color: fmtCard.chosen ? "white" : Theme.textDim }
                            }
                            Item { Layout.fillWidth: true }
                            Badge { visible: fmtCard.recommended; text: i18n.t["exp.recommended"]; tone: "success"; icon: "sparkles" }
                        }
                        AText { text: fmtCard.modelData.title; weight: Font.DemiBold; size: Theme.fsH3 }
                        AText { text: fmtCard.modelData.hint; dim: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
                    }
                    MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: page.ctl.setFormat(fmtCard.modelData.key) }
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 18

            Card {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop
                ColumnLayout {
                    width: parent.width
                    spacing: 12
                    SectionTitle { Layout.fillWidth: true; text: i18n.t["exp.content"]; icon: "list-checks" }
                    Repeater {
                        model: page.ctl.optionList
                        delegate: Toggle {
                            required property var modelData
                            Layout.fillWidth: true
                            label: modelData.title
                            hint: modelData.key === "files" && page.ctl.format !== "zip" ? i18n.t["exp.files_zip_only"]
                                : modelData.key === "anon" ? i18n.t["exp.opt_anon_hint"] : ""
                            enabled: modelData.key !== "files" || page.ctl.format === "zip"
                            isOn: !!page.ctl.options[modelData.key]
                            onToggled: page.ctl.setOption(modelData.key, checked)
                        }
                    }
                }
            }

            Card {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignTop
                ColumnLayout {
                    width: parent.width
                    spacing: 14
                    SectionTitle { Layout.fillWidth: true; text: i18n.t["exp.output"]; icon: "folder-open" }
                    RowLayout {
                        Layout.fillWidth: true
                        spacing: 10
                        Field {
                            id: pathField
                            Layout.fillWidth: true
                            text: page.ctl.path
                            mono: true
                            icon: "folder"
                            onEditingFinished: page.ctl.setPath(text)
                        }
                        Button { iconName: "folder-open"; text: i18n.t["exp.browse"]; onClicked: page.ctl.browse() }
                    }
                    Button {
                        Layout.fillWidth: true
                        variant: "primary"
                        iconName: "download"
                        text: i18n.t["exp.export"]
                        enabled: page.ctl.canExport && !page.ctl.exporting
                        loading: page.ctl.exporting
                        onClicked: { page.ctl.setPath(pathField.text); page.ctl.exportNow() }
                    }
                    // Результат последнего экспорта.
                    Rectangle {
                        visible: page.ctl.lastPath !== ""
                        Layout.fillWidth: true
                        radius: Theme.radius
                        color: Theme.alpha(Theme.success, 0.08)
                        border.color: Theme.alpha(Theme.success, 0.35)
                        implicitHeight: doneRow.implicitHeight + 20
                        RowLayout {
                            id: doneRow
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 10
                            Icon { name: "circle-check"; color: Theme.success }
                            AText { text: page.ctl.lastInfo; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone; size: Theme.fsSmall }
                            Button { compact: true; iconName: "external-link"; text: i18n.t["exp.open_folder"]; onClicked: page.ctl.openFolder() }
                        }
                    }
                }
            }
        }
    }
}
````

### `ui/qml/pages/Settings.qml`

*389 строк*

````qml
import QtQuick
import QtQuick.Layouts
import Ao

// Настройки: интерфейс, human-in-the-loop, супервайзер, выполнение,
// инструменты, песочница, доступные каталоги и безопасность профиля.
Page {
    id: page
    title: i18n.t["settings.title"]
    subtitle: i18n.t["settings.subtitle"]
    icon: "settings"
    readonly property var ctl: backend.prefs
    readonly property var ws: ctl.ws
    readonly property bool hasWs: backend.workspaceId >= 0

    function set(key, value) { ctl.setValue(key, value) }

    Component.onCompleted: ctl.refresh()

    GridLayout {
        Layout.fillWidth: true
        columns: page.contentWidth > 1050 ? 2 : 1
        columnSpacing: 18
        rowSpacing: 18

        // --- интерфейс -----------------------------------------------------------
        Section {
            glyph: "monitor"
            heading: i18n.t["settings.interface"]
            idx: 0
            RowLayout {
                Layout.fillWidth: true
                AText { text: i18n.t["settings.language"]; Layout.fillWidth: true }
                Segmented {
                    options: i18n.languages.map(function(l) { return { value: l.code, title: l.title } })
                    value: i18n.lang
                    onPicked: function(v) { backend.setLanguage(v) }
                }
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 14
                ColumnLayout {
                    Layout.fillWidth: true
                    spacing: 2
                    AText { text: i18n.t["settings.motion"] }
                    AText { text: i18n.t["settings.motion_hint"]; mute: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
                }
                OrbitLogo { size: 34 }
            }
            Segmented {
                Layout.fillWidth: true
                stretch: true
                options: [
                    { value: "full", title: i18n.t["settings.motion_full"], icon: "sparkles" },
                    { value: "reduced", title: i18n.t["settings.motion_reduced"], icon: "gauge" },
                    { value: "off", title: i18n.t["settings.motion_off"], icon: "pause" }
                ]
                value: backend.motion
                onPicked: function(v) { backend.setMotion(v) }
            }
        }

        // --- human-in-the-loop -----------------------------------------------------
        Section {
            glyph: "hand"
            heading: i18n.t["settings.hitl_title"]
            idx: 1
            enabled: page.hasWs
            Toggle {
                Layout.fillWidth: true
                label: i18n.t["settings.hitl"]
                hint: i18n.t["settings.hitl_hint"]
                isOn: !!page.ws.human_in_the_loop
                onToggled: page.set("human_in_the_loop", checked)
            }
            RangeSlider {
                Layout.fillWidth: true
                enabled: !!page.ws.human_in_the_loop
                opacity: enabled ? 1 : 0.45
                label: i18n.t["settings.hitl_threshold"]
                from: 0; to: 1; stepSize: 0.05
                value: page.ws.hitl_confidence_threshold || 0
                format: function(v) { return v <= 0 ? i18n.t["settings.never"] : v.toFixed(2) }
                onCommitted: function(v) { page.set("hitl_confidence_threshold", v) }
            }
            AText { text: i18n.t["settings.hitl_threshold_hint"]; mute: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
            Toggle {
                Layout.fillWidth: true
                enabled: !!page.ws.human_in_the_loop
                label: i18n.t["settings.hitl_milestone"]
                hint: i18n.t["settings.hitl_milestone_hint"]
                isOn: !!page.ws.hitl_pause_on_milestone
                onToggled: page.set("hitl_pause_on_milestone", checked)
            }
        }

        // --- супервайзер -------------------------------------------------------------
        Section {
            glyph: "shield-check"
            heading: i18n.t["settings.supervisor"]
            idx: 2
            enabled: page.hasWs
            Segmented {
                Layout.fillWidth: true
                stretch: true
                options: [
                    { value: "api", title: i18n.t["settings.sup_api_short"], icon: "key-round" },
                    { value: "local", title: i18n.t["settings.sup_local_short"], icon: "hard-drive" }
                ]
                value: page.ws.supervisor_mode || "api"
                onPicked: function(v) { page.set("supervisor_mode", v) }
            }
            Select {
                visible: (page.ws.supervisor_mode || "api") === "api"
                Layout.fillWidth: true
                label: i18n.t["settings.supervisor_agent"]
                icon: "bot"
                options: page.ctl.supervisorOptions.map(function(o) { return { value: o.id, title: o.title } })
                value: page.ws.supervisor_agent_id === undefined ? -1 : page.ws.supervisor_agent_id
                onPicked: function(v) { page.set("supervisor_agent_id", v) }
            }
            RowLayout {
                visible: page.ws.supervisor_mode === "local"
                Layout.fillWidth: true
                spacing: 12
                Field {
                    Layout.fillWidth: true
                    label: i18n.t["settings.local_model"]
                    text: page.ws.supervisor_local_model || ""
                    mono: true
                    icon: "cpu"
                    onEditingFinished: page.set("supervisor_local_model", text)
                }
                Field {
                    Layout.fillWidth: true
                    label: i18n.t["keys.base_url"]
                    text: page.ws.supervisor_local_base_url || ""
                    mono: true
                    icon: "globe"
                    onEditingFinished: page.set("supervisor_local_base_url", text)
                }
            }
            RangeSlider {
                Layout.fillWidth: true
                label: i18n.t["settings.summary_interval"]
                from: 0; to: 120; stepSize: 5
                value: page.ws.summary_interval_minutes || 0
                format: function(v) { return v <= 0 ? i18n.t["settings.off"] : Math.round(v) + " " + i18n.t["settings.min"] }
                onCommitted: function(v) { page.set("summary_interval_minutes", v) }
            }
            Toggle {
                Layout.fillWidth: true
                label: i18n.t["settings.summary_on_event"]
                hint: i18n.t["settings.summary_cost_hint"]
                isOn: !!page.ws.summary_on_event
                onToggled: page.set("summary_on_event", checked)
            }
            Toggle {
                Layout.fillWidth: true
                label: i18n.t["settings.anonymize"]
                hint: i18n.t["settings.anonymize_hint"]
                isOn: page.ws.anonymize_summaries !== false
                onToggled: page.set("anonymize_summaries", checked)
            }
        }

        // --- выполнение ---------------------------------------------------------------
        Section {
            glyph: "workflow"
            heading: i18n.t["settings.execution"]
            idx: 3
            enabled: page.hasWs
            RangeSlider {
                Layout.fillWidth: true
                label: i18n.t["settings.max_steps"]
                from: 1; to: 50; stepSize: 1; decimals: 0
                value: page.ws.agent_max_steps || 10
                onCommitted: function(v) { page.set("agent_max_steps", v) }
            }
            RangeSlider {
                Layout.fillWidth: true
                label: i18n.t["settings.rework_rounds"]
                from: 0; to: 10; stepSize: 1; decimals: 0
                value: page.ws.max_rework_rounds === undefined ? 2 : page.ws.max_rework_rounds
                onCommitted: function(v) { page.set("max_rework_rounds", v) }
            }
            RangeSlider {
                Layout.fillWidth: true
                label: i18n.t["settings.parallel"]
                from: 1; to: 16; stepSize: 1; decimals: 0
                value: page.ws.max_parallel_agents || 6
                onCommitted: function(v) { page.set("max_parallel_agents", v) }
            }
        }

        // --- инструменты -----------------------------------------------------------------
        Section {
            glyph: "zap"
            heading: i18n.t["settings.tools"]
            idx: 4
            enabled: page.hasWs
            AText { text: i18n.t["settings.tools_hint"]; mute: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
            Flow {
                Layout.fillWidth: true
                spacing: 8
                Repeater {
                    model: page.ctl.toolSwitches
                    delegate: Chip {
                        required property var modelData
                        text: modelData.title
                        isOn: (page.ws.tools_enabled || []).indexOf(modelData.key) >= 0
                        onClicked: page.ctl.setTool(modelData.key, checked)
                    }
                }
            }
            AText { text: i18n.t["settings.search_backend"]; size: Theme.fsSmall; weight: Font.Medium; dim: true }
            Segmented {
                options: [{ value: "duckduckgo", title: "DuckDuckGo" }, { value: "tavily", title: "Tavily" }, { value: "brave", title: "Brave" }]
                value: page.ws.search_backend || "duckduckgo"
                onPicked: function(v) { page.set("search_backend", v) }
            }
            RowLayout {
                visible: (page.ws.search_backend || "duckduckgo") !== "duckduckgo"
                Layout.fillWidth: true
                spacing: 10
                Field {
                    id: searchKey
                    Layout.fillWidth: true
                    label: i18n.t["settings.search_key"]
                    placeholder: page.ctl.hasSearchKey ? i18n.t["settings.search_key_set"] : "tvly-…"
                    password: true
                    mono: true
                    icon: "lock"
                    onAccepted: { page.ctl.setSearchKey(text); text = "" }
                }
                Button {
                    Layout.alignment: Qt.AlignBottom
                    iconName: "check"
                    text: i18n.t["common.save"]
                    onClicked: { page.ctl.setSearchKey(searchKey.text); searchKey.text = "" }
                }
            }
            Toggle {
                Layout.fillWidth: true
                label: i18n.t["settings.fetch_pages"]
                isOn: page.ws.fetch_pages !== false
                onToggled: page.set("fetch_pages", checked)
            }
        }

        // --- песочница ---------------------------------------------------------------------
        Section {
            glyph: "box"
            heading: i18n.t["settings.sandbox"]
            idx: 5
            enabled: page.hasWs
            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                Segmented {
                    options: [{ value: "auto", title: i18n.t["settings.sb_auto"] },
                              { value: "subprocess", title: i18n.t["settings.sb_process"] },
                              { value: "docker", title: "Docker" }]
                    value: page.ws.sandbox_backend || "auto"
                    onPicked: function(v) { page.set("sandbox_backend", v) }
                }
                Item { Layout.fillWidth: true }
                Spinner { visible: page.ctl.docker === "checking"; size: 14 }
                Badge {
                    visible: page.ctl.docker !== "checking"
                    text: page.ctl.docker === "yes" ? i18n.t["settings.docker_yes"] : i18n.t["settings.docker_no"]
                    tone: page.ctl.docker === "yes" ? "success" : "warning"
                    icon: page.ctl.docker === "yes" ? "circle-check" : "triangle-alert"
                }
                IconButton { iconName: "refresh-cw"; tip: i18n.t["settings.docker_recheck"]; onClicked: page.ctl.checkDocker() }
            }
            AText {
                text: page.ctl.docker === "yes" ? i18n.t["settings.docker_note_yes"] : i18n.t["settings.docker_note_no"]
                mute: true
                size: Theme.fsSmall
                wrapMode: Text.Wrap
                elide: Text.ElideNone
                Layout.fillWidth: true
            }
            RowLayout {
                Layout.fillWidth: true
                spacing: 20
                RangeSlider {
                    Layout.fillWidth: true
                    label: i18n.t["settings.sb_timeout"]
                    from: 5; to: 300; stepSize: 5; decimals: 0; suffix: " s"
                    value: page.ws.sandbox_timeout_sec || 30
                    onCommitted: function(v) { page.set("sandbox_timeout_sec", v) }
                }
                RangeSlider {
                    Layout.fillWidth: true
                    label: i18n.t["settings.sb_memory"]
                    from: 64; to: 4096; stepSize: 64; decimals: 0; suffix: " MB"
                    value: page.ws.sandbox_memory_mb || 512
                    onCommitted: function(v) { page.set("sandbox_memory_mb", v) }
                }
            }
        }

        // --- каталоги --------------------------------------------------------------------------
        Section {
            glyph: "folder-open"
            heading: i18n.t["settings.allowed_paths"]
            idx: 6
            enabled: page.hasWs
            AText { text: i18n.t["settings.paths_warning"]; color: Theme.warning; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
            Repeater {
                model: page.ws.extra_allowed_paths || []
                delegate: Rectangle {
                    required property string modelData
                    Layout.fillWidth: true
                    height: 38
                    radius: Theme.radiusS
                    color: Theme.surface2
                    RowLayout {
                        anchors.fill: parent
                        anchors.leftMargin: 12
                        anchors.rightMargin: 4
                        Icon { name: "folder"; size: 14; color: Theme.textMute }
                        AText { text: modelData; mono: true; size: Theme.fsSmall; Layout.fillWidth: true; elide: Text.ElideMiddle }
                        IconButton { iconName: "x"; size: 28; danger: true; onClicked: page.ctl.removePath(modelData) }
                    }
                }
            }
            AText { visible: (page.ws.extra_allowed_paths || []).length === 0; text: i18n.t["settings.paths_empty"]; mute: true; size: Theme.fsSmall }
            Button { iconName: "plus"; text: i18n.t["settings.add_path"]; onClicked: page.ctl.addPath() }
        }

        // --- безопасность и данные ----------------------------------------------------------
        Section {
            glyph: "lock"
            heading: i18n.t["settings.security"]
            idx: 7
            AText { text: i18n.t["settings.security_text"]; dim: true; size: Theme.fsSmall; wrapMode: Text.Wrap; elide: Text.ElideNone; Layout.fillWidth: true }
            RowLayout {
                spacing: 10
                Button { iconName: "key-round"; text: i18n.t["settings.change_password"]; onClicked: pwd.openFresh() }
                Button { iconName: "folder-open"; text: i18n.t["settings.open_data"]; onClicked: backend.openPath(backend.dataRoot) }
            }
            AText { text: backend.dataRoot; mono: true; mute: true; size: Theme.fsMicro; Layout.fillWidth: true; elide: Text.ElideMiddle }
        }
    }

    component Section: Card {
        id: sec
        property string glyph: ""
        property string heading: ""
        property int idx: 0
        default property alias items: sectionBody.data
        Layout.fillWidth: true
        Layout.alignment: Qt.AlignTop
        stagger: idx
        opacity: enabled ? enter : enter * 0.5
        ColumnLayout {
            id: sectionBody
            width: parent.width
            spacing: 14
            SectionTitle { Layout.fillWidth: true; text: sec.heading; icon: sec.glyph }
        }
    }

    Sheet {
        id: pwd
        title: i18n.t["settings.change_password"]
        subtitle: i18n.t["settings.password_note"]
        icon: "key-round"
        sheetWidth: 460
        property string error: ""
        function openFresh() { error = ""; oldPwd.text = ""; newPwd.text = ""; newPwd2.text = ""; open(); oldPwd.focusInput() }
        function submit() {
            error = page.ctl.changePassword(oldPwd.text, newPwd.text, newPwd2.text)
            if (error === "") close()
        }
        Field { id: oldPwd; Layout.fillWidth: true; label: i18n.t["settings.old_password"]; password: true; icon: "lock" }
        Field { id: newPwd; Layout.fillWidth: true; label: i18n.t["login.password"]; password: true; icon: "lock" }
        Field { id: newPwd2; Layout.fillWidth: true; label: i18n.t["login.password2"]; password: true; icon: "lock"; error: pwd.error; onAccepted: pwd.submit() }
        footer: [
            Item { Layout.fillWidth: true },
            Button { text: i18n.t["common.cancel"]; variant: "ghost"; onClicked: pwd.close() },
            Button { text: i18n.t["common.save"]; variant: "primary"; iconName: "check"; onClicked: pwd.submit() }
        ]
    }
}
````


## Интерфейс: дизайн-система Ao

### `ui/qml/Ao/qmldir`

*35 строк*

````text
module Ao
singleton Theme 1.0 Theme.qml
singleton Icons 1.0 Icons.qml
AText 1.0 AText.qml
Aurora 1.0 Aurora.qml
Badge 1.0 Badge.qml
BarList 1.0 BarList.qml
Button 1.0 Button.qml
Card 1.0 Card.qml
Chip 1.0 Chip.qml
Confirm 1.0 Confirm.qml
EmptyState 1.0 EmptyState.qml
Field 1.0 Field.qml
Icon 1.0 Icon.qml
IconButton 1.0 IconButton.qml
LineChart 1.0 LineChart.qml
OrbitLogo 1.0 OrbitLogo.qml
PageHeader 1.0 PageHeader.qml
ProgressRing 1.0 ProgressRing.qml
RangeSlider 1.0 RangeSlider.qml
ScrollBar 1.0 ScrollBar.qml
SectionTitle 1.0 SectionTitle.qml
SegmentBar 1.0 SegmentBar.qml
Segmented 1.0 Segmented.qml
Select 1.0 Select.qml
Sheet 1.0 Sheet.qml
Skeleton 1.0 Skeleton.qml
Spinner 1.0 Spinner.qml
StatusDot 1.0 StatusDot.qml
TextBox 1.0 TextBox.qml
Ticker 1.0 Ticker.qml
Tip 1.0 Tip.qml
Toasts 1.0 Toasts.qml
Toggle 1.0 Toggle.qml
Page 1.0 Page.qml
````

### `ui/qml/Ao/Theme.qml`

*110 строк*

````qml
pragma Singleton
import QtQuick

// Дизайн-система: палитра, типографика, отступы, радиусы и анимации.
// Основа - глубокий чернильно-фиолетовый фон; акцент - фиолетовый,
// второй акцент - сине-зелёный (teal → cyan). Все длительности анимаций
// проходят через dur(), поэтому уровень «движения» из настроек
// одним переключателем делает интерфейс спокойнее или выключает анимации.
QtObject {
    id: theme

    // --- движение: 2 - полное, 1 - сдержанное, 0 - без анимаций ---------
    property int motion: 2
    readonly property bool rich: motion >= 2
    function dur(ms) { return motion === 0 ? 0 : (motion === 1 ? Math.round(ms * 0.6) : ms) }
    readonly property int fast: dur(140)
    readonly property int normal: dur(220)
    readonly property int slow: dur(420)

    // --- шрифты (семейства задаёт Python после загрузки файлов) --------------
    property string fontFamily: "Inter"
    property string monoFamily: "JetBrains Mono"
    property string iconFamily: "lucide"

    // --- фоны и поверхности ----------------------------------------------------
    readonly property color bg: "#09080F"
    readonly property color bgRaised: "#0E0C18"
    readonly property color sidebar: "#0C0A16"
    readonly property color surface: Qt.rgba(0.10, 0.09, 0.17, 0.78)
    readonly property color surfaceSolid: "#15132A"
    readonly property color surfaceHover: Qt.rgba(0.14, 0.12, 0.24, 0.85)
    readonly property color surface2: "#1A1733"
    readonly property color surface3: "#221E40"
    readonly property color input: "#120F22"
    readonly property color overlay: Qt.rgba(0.02, 0.01, 0.05, 0.62)

    readonly property color border: "#262244"
    readonly property color borderSoft: Qt.rgba(1, 1, 1, 0.06)
    readonly property color borderStrong: "#3B3566"

    // --- текст ---------------------------------------------------------------------
    readonly property color text: "#EEEBFA"
    readonly property color textDim: "#A9A3C8"
    readonly property color textMute: "#6E6891"
    readonly property color textFaint: "#4B4668"

    // --- акценты ---------------------------------------------------------------------
    readonly property color violet: "#8B5CF6"
    readonly property color violetSoft: "#A78BFA"
    readonly property color violetDeep: "#6D28D9"
    readonly property color indigo: "#6366F1"
    readonly property color teal: "#2DD4BF"
    readonly property color cyan: "#22D3EE"
    readonly property color magenta: "#D946EF"

    readonly property color success: "#34D399"
    readonly property color warning: "#FBBF24"
    readonly property color danger: "#FB7185"
    readonly property color info: "#60A5FA"

    function tone(name) {
        switch (name) {
        case "success": return success
        case "warning": return warning
        case "error": return danger
        case "danger": return danger
        case "info": return info
        case "accent": return cyan
        case "tool": return cyan
        case "violet": return violetSoft
        case "muted": return textMute
        default: return textDim
        }
    }

    function statusColor(status) {
        switch (status) {
        case "running": return cyan
        case "done": return success
        case "review": return violetSoft
        case "rework": return warning
        case "paused": return "#F59E0B"
        case "error": return danger
        case "failed": return danger
        case "stopped": return "#F59E0B"
        default: return textMute
        }
    }

    function alpha(c, a) { return Qt.rgba(c.r, c.g, c.b, a) }

    // --- типографика ---------------------------------------------------------------------
    readonly property int fsDisplay: 30
    readonly property int fsH1: 23
    readonly property int fsH2: 17
    readonly property int fsH3: 15
    readonly property int fsBody: 14
    readonly property int fsSmall: 13
    readonly property int fsMicro: 11

    // --- геометрия -------------------------------------------------------------------------
    readonly property int radiusS: 8
    readonly property int radius: 12
    readonly property int radiusL: 16
    readonly property int radiusXL: 22
    readonly property int gap: 12
    readonly property int pad: 20
    readonly property int pagePad: 28
    readonly property int controlH: 38
}
````

### `ui/qml/Ao/Icons.qml`

*117 строк*

````qml
pragma Singleton
import QtQuick

// Иконки Lucide (ISC): имя -> символ иконочного шрифта.
QtObject {
    readonly property var map: ({
        "layers": "\ue529",
        "key-round": "\ue4a3",
        "bot": "\ue1bb",
        "list-checks": "\ue1d0",
        "play": "\ue13c",
        "activity": "\ue038",
        "shield-check": "\ue1ff",
        "layout-dashboard": "\ue1c1",
        "wallet": "\ue204",
        "package": "\ue129",
        "settings": "\ue154",
        "log-out": "\ue10e",
        "plus": "\ue13d",
        "trash-2": "\ue18e",
        "pencil": "\ue1f9",
        "check": "\ue06c",
        "x": "\ue1b2",
        "chevron-down": "\ue06d",
        "chevron-right": "\ue06f",
        "chevron-up": "\ue070",
        "chevron-left": "\ue06e",
        "search": "\ue151",
        "refresh-cw": "\ue145",
        "pause": "\ue12e",
        "square": "\ue167",
        "circle-alert": "\ue077",
        "triangle-alert": "\ue193",
        "info": "\ue0f9",
        "sparkles": "\ue412",
        "zap": "\ue1b4",
        "brain": "\ue3c6",
        "cpu": "\ue0a9",
        "terminal": "\ue181",
        "globe": "\ue0e8",
        "file-text": "\ue0cc",
        "folder": "\ue0d7",
        "folder-open": "\ue247",
        "link": "\ue102",
        "star": "\ue176",
        "user": "\ue19f",
        "users": "\ue1a4",
        "lock": "\ue10b",
        "eye": "\ue0ba",
        "eye-off": "\ue0bb",
        "arrow-right": "\ue049",
        "arrow-up": "\ue04a",
        "arrow-down": "\ue042",
        "git-branch": "\ue0e2",
        "workflow": "\ue425",
        "network": "\ue125",
        "download": "\ue0b2",
        "upload": "\ue19e",
        "clock": "\ue087",
        "timer": "\ue1e0",
        "gauge": "\ue1bf",
        "flame": "\ue0d2",
        "circle-check": "\ue226",
        "circle-x": "\ue084",
        "circle-dot": "\ue345",
        "loader-circle": "\ue10a",
        "wand-sparkles": "\ue357",
        "message-square-text": "\ue575",
        "send": "\ue152",
        "split": "\ue440",
        "rotate-ccw": "\ue148",
        "skip-forward": "\ue160",
        "octagon-x": "\ue128",
        "hand": "\ue1d7",
        "bell": "\ue059",
        "sliders-horizontal": "\ue29a",
        "languages": "\ue0fe",
        "monitor": "\ue11d",
        "database": "\ue0ad",
        "hard-drive": "\ue0ed",
        "coins": "\ue097",
        "dollar-sign": "\ue0b1",
        "trending-up": "\ue191",
        "chart-line": "\ue2a5",
        "chart-bar": "\ue2a2",
        "list-tree": "\ue408",
        "scroll-text": "\ue45f",
        "badge-check": "\ue241",
        "scan-eye": "\ue536",
        "file-archive": "\ue30d",
        "file-code": "\ue0c3",
        "file-type": "\ue329",
        "book-open": "\ue05f",
        "copy": "\ue09e",
        "external-link": "\ue0b9",
        "grip-vertical": "\ue0eb",
        "ellipsis": "\ue0b6",
        "filter": "\ue0dc",
        "box": "\ue061",
        "boxes": "\ue2d0",
        "hourglass": "\ue296",
        "circle-pause": "\ue07f",
        "circle-play": "\ue080",
        "scale": "\ue212",
        "shield": "\ue158",
        "flag": "\ue0d1",
        "orbit": "\ue3e7",
        "command": "\ue09a",
        "keyboard": "\ue284",
        "square-pen": "\ue172",
        "house": "\ue0f5",
        "power": "\ue140",
        "arrow-up-right": "\ue04d",
        "inbox": "\ue0f7"
    })
    function glyph(name) { return map[name] || map["circle-dot"] }
}
````

### `ui/qml/Ao/AText.qml`

*20 строк*

````qml
import QtQuick

// Базовый текст интерфейса с шрифтом и цветом темы.
Text {
    property bool dim: false
    property bool mute: false
    property bool mono: false
    property int size: Theme.fsBody
    property int weight: Font.Normal

    color: mute ? Theme.textMute : (dim ? Theme.textDim : Theme.text)
    font.family: mono ? Theme.monoFamily : Theme.fontFamily
    font.pixelSize: size
    font.weight: weight
    wrapMode: Text.NoWrap
    elide: Text.ElideRight
    textFormat: Text.PlainText
    renderType: Text.QtRendering
    linkColor: Theme.cyan
}
````

### `ui/qml/Ao/Icon.qml`

*15 строк*

````qml
import QtQuick

// Иконка из шрифта Lucide: Icon { name: "bot"; size: 18; color: Theme.textDim }
Text {
    property string name: "circle-dot"
    property int size: 16
    text: Icons.glyph(name)
    font.family: Theme.iconFamily
    font.pixelSize: size
    color: Theme.textDim
    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignVCenter
    renderType: Text.QtRendering
    Behavior on color { ColorAnimation { duration: Theme.fast } }
}
````

### `ui/qml/Ao/Button.qml`

*127 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T

// Кнопка с вариантами: primary | secondary | ghost | danger | success.
// Микровзаимодействия: подсветка при наведении, «вдавливание» при нажатии,
// бегущий блик на основной кнопке и индикатор загрузки вместо иконки.
T.AbstractButton {
    id: control
    property string variant: "secondary"
    property string iconName: ""
    property bool loading: false
    property bool compact: false
    property color accent: variant === "danger" ? Theme.danger
                         : variant === "success" ? Theme.success : Theme.violet

    readonly property bool primary: variant === "primary"
    readonly property bool hot: hovered && enabled && !loading

    implicitHeight: compact ? 32 : Theme.controlH
    implicitWidth: Math.max(implicitHeight, row.implicitWidth + (compact ? 22 : 30))
    hoverEnabled: true
    focusPolicy: Qt.StrongFocus
    opacity: enabled ? 1 : 0.45
    scale: pressed ? 0.965 : 1
    Behavior on scale { NumberAnimation { duration: Theme.fast; easing.type: Easing.OutBack } }
    Behavior on opacity { NumberAnimation { duration: Theme.fast } }

    background: Rectangle {
        id: bg
        radius: Theme.radius
        clip: true
        color: control.primary ? "transparent"
             : control.variant === "ghost" ? (control.hot ? Theme.alpha(Theme.text, 0.06) : "transparent")
             : control.variant === "danger" ? (control.hot ? Theme.alpha(Theme.danger, 0.22) : Theme.alpha(Theme.danger, 0.12))
             : control.variant === "success" ? (control.hot ? Theme.alpha(Theme.success, 0.22) : Theme.alpha(Theme.success, 0.12))
             : (control.hot ? Theme.surface3 : Theme.surface2)
        border.width: control.primary || control.variant === "ghost" ? 0 : 1
        border.color: control.variant === "danger" ? Theme.alpha(Theme.danger, 0.35)
                    : control.variant === "success" ? Theme.alpha(Theme.success, 0.35)
                    : (control.hot ? Theme.borderStrong : Theme.border)
        Behavior on color { ColorAnimation { duration: Theme.fast } }

        // Градиент основной кнопки: фиолетовый → индиго, при наведении ярче.
        Rectangle {
            anchors.fill: parent
            radius: parent.radius
            visible: control.primary
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0; color: control.hot ? "#9D72FF" : Theme.violet }
                GradientStop { position: 1; color: control.hot ? "#7C7FFB" : Theme.indigo }
            }
        }
        // Бегущий блик - только на основной кнопке и только при полном движении.
        Rectangle {
            id: shine
            visible: control.primary && Theme.rich
            width: parent.height * 1.6
            height: parent.height * 3
            y: -parent.height
            x: -width * 1.5
            rotation: 20
            opacity: 0.0
            gradient: Gradient {
                orientation: Gradient.Horizontal
                GradientStop { position: 0; color: "transparent" }
                GradientStop { position: 0.5; color: Qt.rgba(1, 1, 1, 0.28) }
                GradientStop { position: 1; color: "transparent" }
            }
        }
        // Светящийся контур фокуса клавиатуры.
        Rectangle {
            anchors.fill: parent
            anchors.margins: -3
            radius: parent.radius + 3
            color: "transparent"
            border.width: 2
            border.color: Theme.alpha(Theme.violetSoft, 0.7)
            visible: control.visualFocus
        }
    }

    SequentialAnimation {
        running: control.hot && control.primary && Theme.rich
        loops: 1
        PropertyAction { target: shine; property: "opacity"; value: 1 }
        NumberAnimation { target: shine; property: "x"; from: -shine.width * 1.5
                          to: control.width + shine.width; duration: 650; easing.type: Easing.OutCubic }
        PropertyAction { target: shine; property: "opacity"; value: 0 }
    }

    contentItem: Item {
        implicitWidth: row.implicitWidth
        implicitHeight: row.implicitHeight
        Row {
            id: row
            anchors.centerIn: parent
            spacing: 8
            Spinner {
                visible: control.loading
                size: 14
                color: control.primary ? "white" : Theme.violetSoft
                anchors.verticalCenter: parent.verticalCenter
            }
            Icon {
                visible: control.iconName !== "" && !control.loading
                name: control.iconName
                size: control.compact ? 14 : 16
                color: control.primary ? "white"
                     : control.variant === "danger" ? Theme.danger
                     : control.variant === "success" ? Theme.success
                     : (control.hot ? Theme.text : Theme.textDim)
                anchors.verticalCenter: parent.verticalCenter
            }
            AText {
                visible: control.text !== ""
                text: control.text
                size: control.compact ? Theme.fsSmall : Theme.fsBody
                weight: Font.DemiBold
                color: control.primary ? "white"
                     : control.variant === "danger" ? Theme.danger
                     : control.variant === "success" ? Theme.success : Theme.text
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
}
````

### `ui/qml/Ao/IconButton.qml`

*36 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T

// Кнопка-иконка с подсказкой: IconButton { icon: "pencil"; tip: "Изменить" }
T.AbstractButton {
    id: control
    property string iconName: "circle-dot"
    property string tip: ""
    property color tint: Theme.textDim
    property color hoverTint: Theme.text
    property bool danger: false
    property int size: 32
    implicitWidth: size
    implicitHeight: size
    hoverEnabled: true
    opacity: enabled ? 1 : 0.4
    scale: pressed ? 0.9 : 1
    Behavior on scale { NumberAnimation { duration: Theme.fast; easing.type: Easing.OutBack } }

    background: Rectangle {
        radius: Theme.radiusS
        color: control.hovered ? (control.danger ? Theme.alpha(Theme.danger, 0.16)
                                                 : Theme.alpha(Theme.text, 0.07)) : "transparent"
        Behavior on color { ColorAnimation { duration: Theme.fast } }
    }
    contentItem: Icon {
        name: control.iconName
        size: Math.round(control.size * 0.5)
        color: control.hovered ? (control.danger ? Theme.danger : control.hoverTint) : control.tint
    }

    Tip {
        text: control.tip
        shown: control.hovered && control.tip !== ""
    }
}
````

### `ui/qml/Ao/Card.qml`

*65 строк*

````qml
import QtQuick

// «Стеклянная» карточка. hoverable: при наведении приподнимается и
// подсвечивает контур; glow: постоянное свечение (активный элемент).
Rectangle {
    id: card
    default property alias content: body.data
    property int padding: Theme.pad
    property bool hoverable: false
    property bool glow: false
    property color glowColor: Theme.violet
    property alias hovered: hover.hovered
    readonly property bool lifted: hoverable && hover.hovered
    // порядковый номер для каскадного появления списка; -1 - без анимации
    property int stagger: -1
    property real enter: stagger >= 0 && Theme.motion > 0 ? 0 : 1

    radius: Theme.radiusL
    color: lifted ? Theme.surfaceHover : Theme.surface
    border.width: 1
    border.color: glow ? Theme.alpha(glowColor, 0.55) : (lifted ? Theme.borderStrong : Theme.border)
    implicitHeight: body.childrenRect.height + padding * 2
    opacity: enter
    transform: Translate {
        y: (card.lifted && Theme.rich ? -2 : 0) + (1 - card.enter) * 16
        Behavior on y { enabled: card.enter >= 1; NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
    }
    SequentialAnimation {
        running: card.stagger >= 0 && card.enter < 1
        PauseAnimation { duration: Theme.rich ? Math.max(0, Math.min(card.stagger, 12)) * 45 : 0 }
        NumberAnimation { target: card; property: "enter"; to: 1; duration: Theme.slow; easing.type: Easing.OutCubic }
    }
    Behavior on color { ColorAnimation { duration: Theme.normal } }
    Behavior on border.color { ColorAnimation { duration: Theme.normal } }

    // Мягкий блик по верхней кромке - ощущение объёма стекла.
    Rectangle {
        anchors { left: parent.left; right: parent.right; top: parent.top; margins: 1 }
        height: parent.radius * 2
        radius: parent.radius
        opacity: 0.55
        gradient: Gradient {
            GradientStop { position: 0; color: Qt.rgba(1, 1, 1, 0.045) }
            GradientStop { position: 1; color: "transparent" }
        }
    }
    // Свечение вокруг активной карточки.
    Rectangle {
        anchors.fill: parent
        anchors.margins: -4
        radius: parent.radius + 4
        color: "transparent"
        border.width: 4
        border.color: Theme.alpha(card.glowColor, 0.12)
        visible: card.glow
    }

    HoverHandler { id: hover; enabled: card.hoverable }

    Item {
        id: body
        anchors.fill: parent
        anchors.margins: card.padding
    }
}
````

### `ui/qml/Ao/Page.qml`

*47 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Шаблон страницы: заголовок с действиями и прокручиваемое содержимое.
// fill: true - содержимое растягивается на всю высоту без прокрутки
// (страницы с собственными прокручиваемыми панелями, как «Выполнение»).
Item {
    id: page
    property string title: ""
    property string subtitle: ""
    property string icon: ""
    property bool fill: false
    property alias headerActions: header.actions
    default property alias content: col.data
    readonly property int contentWidth: col.width

    PageHeader {
        id: header
        anchors { left: parent.left; right: parent.right; top: parent.top }
        anchors.margins: Theme.pagePad
        anchors.bottomMargin: 0
        title: page.title
        subtitle: page.subtitle
        icon: page.icon
    }

    Flickable {
        id: flick
        anchors { left: parent.left; right: parent.right; top: header.bottom; bottom: parent.bottom }
        anchors.topMargin: 22
        clip: true
        interactive: !page.fill
        contentWidth: width
        contentHeight: page.fill ? height : col.implicitHeight + Theme.pagePad
        boundsBehavior: Flickable.StopAtBounds
        T.ScrollBar.vertical: ScrollBar { visible: !page.fill }

        ColumnLayout {
            id: col
            x: Theme.pagePad
            width: flick.width - Theme.pagePad * 2
            height: page.fill ? flick.height - Theme.pagePad : implicitHeight
            spacing: 18
        }
    }
}
````

### `ui/qml/Ao/PageHeader.qml`

*50 строк*

````qml
import QtQuick
import QtQuick.Layouts

// Заголовок страницы: иконка, название, подзаголовок и действия справа.
RowLayout {
    id: root
    property string title: ""
    property string subtitle: ""
    property string icon: ""
    default property alias actions: actionRow.data
    spacing: 16

    Rectangle {
        visible: root.icon !== ""
        Layout.alignment: Qt.AlignTop
        width: 44; height: 44; radius: 14
        gradient: Gradient {
            GradientStop { position: 0; color: Theme.alpha(Theme.violet, 0.30) }
            GradientStop { position: 1; color: Theme.alpha(Theme.cyan, 0.14) }
        }
        border.color: Theme.alpha(Theme.violetSoft, 0.3)
        Icon { anchors.centerIn: parent; name: root.icon; size: 20; color: Theme.violetSoft }
    }

    ColumnLayout {
        Layout.fillWidth: true
        spacing: 3
        AText {
            text: root.title
            size: Theme.fsH1
            weight: Font.Bold
            Layout.fillWidth: true
        }
        AText {
            visible: root.subtitle !== ""
            text: root.subtitle
            dim: true
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            elide: Text.ElideNone
            maximumLineCount: 2
        }
    }

    RowLayout {
        id: actionRow
        Layout.alignment: Qt.AlignTop
        spacing: 10
    }
}
````

### `ui/qml/Ao/SectionTitle.qml`

*28 строк*

````qml
import QtQuick
import QtQuick.Layouts

// Подзаголовок секции внутри страницы или карточки.
RowLayout {
    id: root
    property string text: ""
    property string icon: ""
    property string hint: ""
    default property alias trailing: trail.data
    spacing: 10
    Icon { visible: root.icon !== ""; name: root.icon; size: 16; color: Theme.violetSoft }
    ColumnLayout {
        Layout.fillWidth: true
        spacing: 1
        AText { text: root.text; size: Theme.fsH3; weight: Font.DemiBold; Layout.fillWidth: true }
        AText {
            visible: root.hint !== ""
            text: root.hint
            mute: true
            size: Theme.fsSmall
            Layout.fillWidth: true
            wrapMode: Text.Wrap
            elide: Text.ElideNone
        }
    }
    RowLayout { id: trail; spacing: 8 }
}
````

### `ui/qml/Ao/Field.qml`

*113 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Поле ввода с подписью, иконкой, ошибкой и светящимся фокусом.
// password: true - скрытый ввод с кнопкой «показать».
ColumnLayout {
    id: root
    property alias text: input.text
    property alias placeholder: input.placeholderText
    property alias input: input
    property string label: ""
    property string hint: ""
    property string error: ""
    property string icon: ""
    property bool password: false
    property bool mono: false
    property bool readOnly: false
    property int inputMethodHints: Qt.ImhNone
    property bool reveal: false
    signal accepted()
    signal editingFinished()
    signal upPressed()
    signal downPressed()
    spacing: 6

    function focusInput() { input.forceActiveFocus() }

    AText {
        visible: root.label !== ""
        text: root.label
        size: Theme.fsSmall
        weight: Font.Medium
        dim: true
    }

    T.TextField {
        id: input
        Layout.fillWidth: true
        implicitHeight: Theme.controlH + 2
        leftPadding: root.icon !== "" ? 38 : 12
        rightPadding: root.password ? 40 : 12
        font.family: root.mono ? Theme.monoFamily : Theme.fontFamily
        font.pixelSize: Theme.fsBody
        color: Theme.text
        placeholderTextColor: Theme.textFaint
        selectionColor: Theme.alpha(Theme.violet, 0.45)
        selectedTextColor: Theme.text
        echoMode: root.password && !root.reveal ? TextInput.Password : TextInput.Normal
        readOnly: root.readOnly
        inputMethodHints: root.inputMethodHints
        verticalAlignment: TextInput.AlignVCenter
        onAccepted: root.accepted()
        onEditingFinished: root.editingFinished()
        Keys.onUpPressed: root.upPressed()
        Keys.onDownPressed: root.downPressed()

        background: Rectangle {
            radius: Theme.radius
            color: input.activeFocus ? Theme.surface2 : Theme.input
            border.width: 1
            border.color: root.error !== "" ? Theme.danger
                        : input.activeFocus ? Theme.violet
                        : (hover.hovered ? Theme.borderStrong : Theme.border)
            Behavior on border.color { ColorAnimation { duration: Theme.fast } }
            Behavior on color { ColorAnimation { duration: Theme.fast } }

            // Внешнее свечение фокуса.
            Rectangle {
                anchors.fill: parent
                anchors.margins: -3
                radius: parent.radius + 3
                color: "transparent"
                border.width: 3
                border.color: Theme.alpha(root.error !== "" ? Theme.danger : Theme.violet, 0.18)
                opacity: input.activeFocus ? 1 : 0
                Behavior on opacity { NumberAnimation { duration: Theme.normal } }
            }
            HoverHandler { id: hover }
        }

        Icon {
            visible: root.icon !== ""
            name: root.icon
            size: 16
            color: input.activeFocus ? Theme.violetSoft : Theme.textMute
            anchors.left: parent.left
            anchors.leftMargin: 12
            anchors.verticalCenter: parent.verticalCenter
        }

        IconButton {
            visible: root.password
            iconName: root.reveal ? "eye-off" : "eye"
            size: 28
            anchors.right: parent.right
            anchors.rightMargin: 6
            anchors.verticalCenter: parent.verticalCenter
            onClicked: root.reveal = !root.reveal
            focusPolicy: Qt.NoFocus
        }
    }

    AText {
        visible: root.error !== "" || root.hint !== ""
        text: root.error !== "" ? root.error : root.hint
        color: root.error !== "" ? Theme.danger : Theme.textMute
        size: Theme.fsSmall
        wrapMode: Text.Wrap
        elide: Text.ElideNone
        Layout.fillWidth: true
    }
}
````

### `ui/qml/Ao/TextBox.qml`

*80 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Многострочное поле с прокруткой и тем же фокусом, что у Field.
ColumnLayout {
    id: root
    property alias text: area.text
    property alias placeholder: area.placeholderText
    property alias area: area
    property string label: ""
    property string hint: ""
    property bool mono: false
    property bool readOnly: false
    property int minHeight: 120
    spacing: 6

    AText {
        visible: root.label !== ""
        text: root.label
        size: Theme.fsSmall
        weight: Font.Medium
        dim: true
    }

    Rectangle {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.minimumHeight: root.minHeight
        radius: Theme.radius
        color: area.activeFocus ? Theme.surface2 : Theme.input
        border.width: 1
        border.color: area.activeFocus ? Theme.violet : Theme.border
        Behavior on border.color { ColorAnimation { duration: Theme.fast } }

        Rectangle {
            anchors.fill: parent
            anchors.margins: -3
            radius: parent.radius + 3
            color: "transparent"
            border.width: 3
            border.color: Theme.alpha(Theme.violet, 0.18)
            opacity: area.activeFocus ? 1 : 0
            Behavior on opacity { NumberAnimation { duration: Theme.normal } }
        }

        T.ScrollView {
            id: scroll
            anchors.fill: parent
            anchors.margins: 2
            clip: true
            T.ScrollBar.vertical: ScrollBar {}

            T.TextArea {
                id: area
                padding: 10
                wrapMode: TextEdit.Wrap
                readOnly: root.readOnly
                font.family: root.mono ? Theme.monoFamily : Theme.fontFamily
                font.pixelSize: root.mono ? Theme.fsSmall : Theme.fsBody
                color: Theme.text
                placeholderTextColor: Theme.textFaint
                selectionColor: Theme.alpha(Theme.violet, 0.45)
                selectedTextColor: Theme.text
                background: null
                selectByMouse: true
            }
        }
    }

    AText {
        visible: root.hint !== ""
        text: root.hint
        mute: true
        size: Theme.fsSmall
        wrapMode: Text.Wrap
        elide: Text.ElideNone
        Layout.fillWidth: true
    }
}
````

### `ui/qml/Ao/Select.qml`

*169 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Выпадающий список. options: [{value, title}] или массив строк.
// editable: можно вписать своё значение (например, имя модели).
ColumnLayout {
    id: root
    property var options: []
    property var value: undefined
    property string label: ""
    property string placeholder: ""
    property bool editable: false
    property string icon: ""
    property alias combo: combo
    readonly property string editText: combo.editText
    signal picked(var value)
    signal edited(string text)
    spacing: 6

    readonly property bool plain: options.length > 0 && typeof options[0] !== "object"

    function titleOf(v) {
        for (var i = 0; i < options.length; ++i) {
            var o = options[i]
            if (plain ? o === v : o.value === v) return plain ? o : o.title
        }
        return v === undefined || v === null ? "" : String(v)
    }
    function indexOf(v) {
        for (var i = 0; i < options.length; ++i) {
            var o = options[i]
            if (plain ? o === v : o.value === v) return i
        }
        return -1
    }

    AText {
        visible: root.label !== ""
        text: root.label
        size: Theme.fsSmall
        weight: Font.Medium
        dim: true
    }

    T.ComboBox {
        id: combo
        Layout.fillWidth: true
        implicitHeight: Theme.controlH + 2
        model: root.options
        textRole: root.plain ? "" : "title"
        valueRole: root.plain ? "" : "value"
        editable: root.editable
        currentIndex: root.indexOf(root.value)
        font.family: Theme.fontFamily
        font.pixelSize: Theme.fsBody
        hoverEnabled: true
        onActivated: function(index) {
            var o = root.options[index]
            root.picked(root.plain ? o : o.value)
        }
        onAccepted: root.edited(editText)
        Component.onCompleted: if (root.editable && root.indexOf(root.value) < 0) editText = root.titleOf(root.value)

        leftPadding: root.icon !== "" ? 38 : 12
        rightPadding: 36

        contentItem: T.TextField {
            text: combo.editable ? combo.editText : combo.displayText
            readOnly: !combo.editable
            enabled: combo.editable
            color: text === "" ? Theme.textFaint : Theme.text
            placeholderText: root.placeholder
            placeholderTextColor: Theme.textFaint
            font: combo.font
            verticalAlignment: Text.AlignVCenter
            selectionColor: Theme.alpha(Theme.violet, 0.45)
            background: null
            leftPadding: 0
            onTextEdited: root.edited(text)
        }

        indicator: Icon {
            name: "chevron-down"
            size: 16
            color: combo.hovered ? Theme.text : Theme.textMute
            x: combo.width - width - 12
            y: (combo.height - height) / 2
            rotation: combo.popup.visible ? 180 : 0
            Behavior on rotation { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
        }

        background: Rectangle {
            radius: Theme.radius
            color: combo.activeFocus || combo.popup.visible ? Theme.surface2 : Theme.input
            border.width: 1
            border.color: combo.popup.visible || combo.activeFocus ? Theme.violet
                        : (combo.hovered ? Theme.borderStrong : Theme.border)
            Behavior on border.color { ColorAnimation { duration: Theme.fast } }
            Icon {
                visible: root.icon !== ""
                name: root.icon
                size: 16
                color: Theme.textMute
                anchors.left: parent.left
                anchors.leftMargin: 12
                anchors.verticalCenter: parent.verticalCenter
            }
        }

        delegate: T.ItemDelegate {
            id: item
            required property var modelData
            required property int index
            width: ListView.view ? ListView.view.width : combo.width
            height: 36
            hoverEnabled: true
            highlighted: combo.highlightedIndex === index
            contentItem: RowLayout {
                spacing: 8
                AText {
                    Layout.fillWidth: true
                    text: root.plain ? item.modelData : item.modelData.title
                    color: item.index === combo.currentIndex ? Theme.violetSoft : Theme.text
                    weight: item.index === combo.currentIndex ? Font.DemiBold : Font.Normal
                }
                Icon {
                    visible: item.index === combo.currentIndex
                    name: "check"
                    size: 14
                    color: Theme.violetSoft
                }
            }
            background: Rectangle {
                radius: Theme.radiusS
                color: item.highlighted ? Theme.alpha(Theme.violet, 0.16) : "transparent"
                Behavior on color { ColorAnimation { duration: Theme.fast } }
            }
        }

        popup: T.Popup {
            y: combo.height + 6
            width: combo.width
            implicitHeight: Math.min(contentItem.implicitHeight + 12, 320)
            padding: 6
            contentItem: ListView {
                clip: true
                implicitHeight: contentHeight
                model: combo.popup.visible ? combo.delegateModel : null
                currentIndex: combo.highlightedIndex
                boundsBehavior: Flickable.StopAtBounds
                T.ScrollBar.vertical: ScrollBar {}
            }
            background: Rectangle {
                radius: Theme.radius
                color: Theme.surfaceSolid
                border.color: Theme.borderStrong
            }
            enter: Transition {
                ParallelAnimation {
                    NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.fast }
                    NumberAnimation { property: "y"; from: combo.height; to: combo.height + 6
                                      duration: Theme.normal; easing.type: Easing.OutCubic }
                }
            }
            exit: Transition { NumberAnimation { property: "opacity"; to: 0; duration: Theme.fast } }
        }
    }
}
````

### `ui/qml/Ao/Toggle.qml`

*77 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Переключатель с «пружинящим» бегунком и подписью слева.
//
// Состояние из данных задаётся через isOn, а не через checked. Щелчок
// переключает checked (обработчики onToggled видят новое значение), а затем
// переключатель снова показывает isOn - то, что реально сохранено. Кнопка,
// которой задали checked напрямую, после щелчка, не изменившего данные
// (сохранение не прошло, щелчок по уже выбранному пункту), показывала бы
// состояние, которого на самом деле нет.
T.AbstractButton {
    id: control
    property string label: ""
    property string hint: ""
    property var isOn: undefined
    checkable: true
    checked: isOn === undefined ? false : !!isOn
    hoverEnabled: true

    function resync() {
        control.checked = Qt.binding(function() { return !!control.isOn })
    }
    Connections {
        target: control
        function onToggled() { if (control.isOn !== undefined) Qt.callLater(control.resync) }
    }
    implicitWidth: row.implicitWidth
    implicitHeight: Math.max(28, row.implicitHeight)
    opacity: enabled ? 1 : 0.45

    contentItem: RowLayout {
        id: row
        spacing: 14
        ColumnLayout {
            Layout.fillWidth: true
            spacing: 2
            visible: control.label !== ""
            AText { text: control.label; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone }
            AText {
                visible: control.hint !== ""
                text: control.hint
                mute: true
                size: Theme.fsSmall
                wrapMode: Text.Wrap
                elide: Text.ElideNone
                Layout.fillWidth: true
            }
        }
        Rectangle {
            id: track
            Layout.alignment: Qt.AlignVCenter
            width: 42; height: 24; radius: 12
            color: control.checked ? "transparent" : Theme.surface3
            border.width: control.checked ? 0 : 1
            border.color: control.hovered ? Theme.borderStrong : Theme.border
            gradient: control.checked ? onGradient : null
            Gradient {
                id: onGradient
                orientation: Gradient.Horizontal
                GradientStop { position: 0; color: Theme.violet }
                GradientStop { position: 1; color: Theme.teal }
            }
            Rectangle {
                id: knob
                width: 18; height: 18; radius: 9
                y: 3
                x: control.checked ? track.width - width - 3 : 3
                color: "white"
                scale: control.pressed ? 0.85 : 1
                Behavior on x { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutBack; easing.overshoot: 1.6 } }
                Behavior on scale { NumberAnimation { duration: Theme.fast } }
            }
        }
    }
}
````

### `ui/qml/Ao/Chip.qml`

*57 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T

// Переключаемая «таблетка»: для инструментов, опций, фильтров.
// Состояние из данных - через isOn (подробности в Toggle.qml).
T.AbstractButton {
    id: control
    property string iconName: ""
    property color accent: Theme.violet
    property var isOn: undefined
    checkable: true
    checked: isOn === undefined ? false : !!isOn
    hoverEnabled: true

    function resync() {
        control.checked = Qt.binding(function() { return !!control.isOn })
    }
    Connections {
        target: control
        function onToggled() { if (control.isOn !== undefined) Qt.callLater(control.resync) }
    }
    implicitHeight: 32
    implicitWidth: row.implicitWidth + 26
    scale: pressed ? 0.95 : 1
    Behavior on scale { NumberAnimation { duration: Theme.fast; easing.type: Easing.OutBack } }

    background: Rectangle {
        radius: height / 2
        color: control.checked ? Theme.alpha(control.accent, 0.18)
             : (control.hovered ? Theme.surface3 : Theme.surface2)
        border.width: 1
        border.color: control.checked ? Theme.alpha(control.accent, 0.65) : Theme.border
        Behavior on color { ColorAnimation { duration: Theme.fast } }
        Behavior on border.color { ColorAnimation { duration: Theme.fast } }
    }
    contentItem: Item {
        Row {
            id: row
            anchors.centerIn: parent
            spacing: 6
            Icon {
                name: control.checked ? "check" : control.iconName
                visible: control.checked || control.iconName !== ""
                size: 14
                color: control.checked ? Theme.violetSoft : Theme.textMute
                anchors.verticalCenter: parent.verticalCenter
            }
            AText {
                text: control.text
                size: Theme.fsSmall
                weight: Font.Medium
                color: control.checked ? Theme.text : Theme.textDim
                anchors.verticalCenter: parent.verticalCenter
            }
        }
    }
}
````

### `ui/qml/Ao/Segmented.qml`

*91 строк*

````qml
import QtQuick
import QtQuick.Layouts

// Сегментированный переключатель: подсветка «переезжает» к выбранному пункту.
// options: [{value, title, icon?}]
Rectangle {
    id: root
    property var options: []
    property var value
    property bool stretch: false
    signal picked(var value)

    readonly property int current: {
        for (var i = 0; i < options.length; ++i)
            if (options[i].value === value) return i
        return -1
    }

    implicitHeight: 36
    implicitWidth: stretch ? 200 : row.implicitWidth + 8
    radius: Theme.radius
    color: Theme.input
    border.color: Theme.border

    Rectangle {
        id: pill
        visible: root.current >= 0 && repeater.count > root.current
        property Item target: repeater.count > root.current && root.current >= 0 ? repeater.itemAt(root.current) : null
        x: target ? row.x + target.x : 4
        y: 4
        width: target ? target.width : 0
        height: root.height - 8
        radius: Theme.radiusS
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0; color: Theme.alpha(Theme.violet, 0.9) }
            GradientStop { position: 1; color: Theme.alpha(Theme.indigo, 0.9) }
        }
        Behavior on x { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
        Behavior on width { NumberAnimation { duration: Theme.normal; easing.type: Easing.OutCubic } }
    }

    RowLayout {
        id: row
        x: 4
        y: 4
        height: root.height - 8
        width: root.stretch ? root.width - 8 : implicitWidth
        spacing: 2
        Repeater {
            id: repeater
            model: root.options
            delegate: Item {
                id: seg
                required property var modelData
                required property int index
                readonly property bool active: index === root.current
                Layout.fillWidth: root.stretch
                Layout.fillHeight: true
                implicitWidth: segRow.implicitWidth + 24
                Row {
                    id: segRow
                    anchors.centerIn: parent
                    spacing: 6
                    Icon {
                        visible: !!seg.modelData.icon
                        name: seg.modelData.icon || "circle-dot"
                        size: 14
                        color: seg.active ? "white" : Theme.textMute
                        anchors.verticalCenter: parent.verticalCenter
                    }
                    AText {
                        text: seg.modelData.title
                        size: Theme.fsSmall
                        weight: seg.active ? Font.DemiBold : Font.Medium
                        color: seg.active ? "white" : (mouse.containsMouse ? Theme.text : Theme.textDim)
                        anchors.verticalCenter: parent.verticalCenter
                        Behavior on color { ColorAnimation { duration: Theme.fast } }
                    }
                }
                MouseArea {
                    id: mouse
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                    onClicked: root.picked(seg.modelData.value)
                }
            }
        }
    }
}
````

### `ui/qml/Ao/RangeSlider.qml`

*77 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Слайдер с подписью и значением справа; значение применяется по отпусканию.
ColumnLayout {
    id: root
    property string label: ""
    property real from: 0
    property real to: 1
    property real stepSize: 0.05
    property real value: 0
    property int decimals: 2
    property string suffix: ""
    property var format: null
    signal committed(real value)
    spacing: 6

    RowLayout {
        Layout.fillWidth: true
        AText { text: root.label; size: Theme.fsSmall; weight: Font.Medium; dim: true; Layout.fillWidth: true }
        AText {
            text: root.format ? root.format(slider.value) : slider.value.toFixed(root.decimals) + root.suffix
            size: Theme.fsSmall
            weight: Font.DemiBold
            color: Theme.violetSoft
            mono: true
        }
    }

    T.Slider {
        id: slider
        Layout.fillWidth: true
        from: root.from
        to: root.to
        stepSize: root.stepSize
        value: root.value
        snapMode: T.Slider.SnapAlways
        hoverEnabled: true
        onPressedChanged: if (!pressed) root.committed(value)
        // Стрелки и колёсико двигают ползунок без нажатия - применяем сразу.
        onMoved: if (!pressed) root.committed(value)

        background: Rectangle {
            x: slider.leftPadding
            y: slider.topPadding + slider.availableHeight / 2 - height / 2
            width: slider.availableWidth
            height: 6
            radius: 3
            color: Theme.surface3
            Rectangle {
                width: slider.visualPosition * parent.width
                height: parent.height
                radius: 3
                gradient: Gradient {
                    orientation: Gradient.Horizontal
                    GradientStop { position: 0; color: Theme.violet }
                    GradientStop { position: 1; color: Theme.teal }
                }
            }
        }
        handle: Rectangle {
            x: slider.leftPadding + slider.visualPosition * (slider.availableWidth - width)
            y: slider.topPadding + slider.availableHeight / 2 - height / 2
            width: 18; height: 18; radius: 9
            color: "white"
            scale: slider.pressed ? 1.25 : (slider.hovered ? 1.1 : 1)
            Behavior on scale { NumberAnimation { duration: Theme.fast; easing.type: Easing.OutBack } }
            Rectangle {
                anchors.centerIn: parent
                width: 30; height: 30; radius: 15
                color: Theme.alpha(Theme.violet, 0.25)
                visible: slider.pressed
            }
        }
    }
}
````

### `ui/qml/Ao/Badge.qml`

*38 строк*

````qml
import QtQuick

// Цветная метка-таблетка: Badge { text: "готово"; tone: "success" }
Rectangle {
    id: badge
    property string text: ""
    property string tone: "muted"
    property string icon: ""
    property color tint: Theme.tone(tone)
    property bool solid: false
    implicitHeight: 22
    implicitWidth: row.implicitWidth + 16
    radius: height / 2
    color: solid ? tint : Theme.alpha(tint, 0.14)
    border.width: solid ? 0 : 1
    border.color: Theme.alpha(tint, 0.35)
    Behavior on color { ColorAnimation { duration: Theme.normal } }

    Row {
        id: row
        anchors.centerIn: parent
        spacing: 5
        Icon {
            visible: badge.icon !== ""
            name: badge.icon
            size: 12
            color: badge.solid ? Theme.bg : badge.tint
            anchors.verticalCenter: parent.verticalCenter
        }
        AText {
            text: badge.text
            size: Theme.fsMicro
            weight: Font.DemiBold
            color: badge.solid ? Theme.bg : badge.tint
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}
````

### `ui/qml/Ao/StatusDot.qml`

*39 строк*

````qml
import QtQuick

// Точка статуса; для «работает» - расходящиеся круги пульса.
Item {
    id: root
    property string status: "idle"
    property int size: 8
    readonly property color tint: Theme.statusColor(status)
    readonly property bool live: status === "running"
    implicitWidth: size
    implicitHeight: size

    Rectangle {
        id: pulse
        anchors.centerIn: parent
        width: root.size; height: root.size; radius: width / 2
        color: "transparent"
        border.width: 2
        border.color: root.tint
        opacity: 0
        visible: root.live && Theme.motion > 0
        SequentialAnimation on scale {
            running: pulse.visible
            loops: Animation.Infinite
            NumberAnimation { from: 1; to: 2.8; duration: 1300; easing.type: Easing.OutCubic }
        }
        SequentialAnimation on opacity {
            running: pulse.visible
            loops: Animation.Infinite
            NumberAnimation { from: 0.8; to: 0; duration: 1300; easing.type: Easing.OutCubic }
        }
    }
    Rectangle {
        anchors.centerIn: parent
        width: root.size; height: root.size; radius: width / 2
        color: root.tint
        Behavior on color { ColorAnimation { duration: Theme.normal } }
    }
}
````

### `ui/qml/Ao/Spinner.qml`

*35 строк*

````qml
import QtQuick
import QtQuick.Shapes

// Индикатор ожидания: вращающаяся дуга с градиентным хвостом.
Item {
    id: root
    property int size: 18
    property color color: Theme.violetSoft
    property real stroke: Math.max(2, size / 8)
    implicitWidth: size
    implicitHeight: size

    Shape {
        id: arc
        anchors.fill: parent
        preferredRendererType: Shape.CurveRenderer
        ShapePath {
            strokeWidth: root.stroke
            strokeColor: root.color
            fillColor: "transparent"
            capStyle: ShapePath.RoundCap
            PathAngleArc {
                centerX: root.size / 2; centerY: root.size / 2
                radiusX: root.size / 2 - root.stroke; radiusY: root.size / 2 - root.stroke
                startAngle: 0; sweepAngle: 270
            }
        }
        RotationAnimator on rotation {
            from: 0; to: 360
            duration: 900
            loops: Animation.Infinite
            running: root.visible
        }
    }
}
````

### `ui/qml/Ao/Skeleton.qml`

*27 строк*

````qml
import QtQuick

// Заглушка загрузки с бегущим отблеском.
Rectangle {
    id: root
    radius: Theme.radiusS
    color: Theme.surface2
    clip: true
    Rectangle {
        id: sweep
        width: root.width * 0.5
        height: root.height
        x: -width
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop { position: 0; color: "transparent" }
            GradientStop { position: 0.5; color: Qt.rgba(1, 1, 1, 0.06) }
            GradientStop { position: 1; color: "transparent" }
        }
        NumberAnimation on x {
            from: -sweep.width; to: root.width
            duration: 1300
            loops: Animation.Infinite
            running: root.visible && Theme.motion > 0
        }
    }
}
````

### `ui/qml/Ao/Tip.qml`

*37 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T

// Подсказка в стиле темы; появляется с небольшой задержкой и «всплывает».
T.ToolTip {
    id: tip
    property bool shown: false
    visible: shown && text !== ""
    delay: 450
    timeout: 6000
    y: -implicitHeight - 8
    x: (parent ? parent.width - implicitWidth : 0) / 2
    padding: 8
    leftPadding: 10
    rightPadding: 10

    contentItem: AText {
        text: tip.text
        size: Theme.fsSmall
        color: Theme.text
        wrapMode: Text.Wrap
        elide: Text.ElideNone
        width: Math.min(implicitWidth, 320)
    }
    background: Rectangle {
        radius: Theme.radiusS
        color: Theme.surface3
        border.color: Theme.borderStrong
    }
    enter: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.fast }
            NumberAnimation { property: "scale"; from: 0.92; to: 1; duration: Theme.fast; easing.type: Easing.OutBack }
        }
    }
    exit: Transition { NumberAnimation { property: "opacity"; to: 0; duration: Theme.fast } }
}
````

### `ui/qml/Ao/ScrollBar.qml`

*22 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T

// Тонкая полоса прокрутки, которая проявляется при наведении и движении.
T.ScrollBar {
    id: bar
    implicitWidth: 10
    implicitHeight: 10
    padding: 2
    minimumSize: 0.08
    policy: T.ScrollBar.AsNeeded
    contentItem: Rectangle {
        implicitWidth: 6
        implicitHeight: 6
        radius: 3
        color: bar.pressed ? Theme.violetSoft : (bar.hovered ? Theme.borderStrong : Theme.surface3)
        opacity: bar.active || bar.hovered ? 1 : 0
        Behavior on opacity { NumberAnimation { duration: Theme.normal } }
        Behavior on color { ColorAnimation { duration: Theme.fast } }
    }
    background: Item {}
}
````

### `ui/qml/Ao/EmptyState.qml`

*63 строк*

````qml
import QtQuick
import QtQuick.Layouts

// Пустое состояние: парящая иконка в градиентном круге, текст и действие.
ColumnLayout {
    id: root
    property string icon: "sparkles"
    property string title: ""
    property string text: ""
    property string actionText: ""
    property string actionIcon: "plus"
    signal action()
    spacing: 10

    Item {
        Layout.alignment: Qt.AlignHCenter
        implicitWidth: 76
        implicitHeight: 76
        Rectangle {
            id: orb
            anchors.centerIn: parent
            width: 64; height: 64; radius: 32
            gradient: Gradient {
                GradientStop { position: 0; color: Theme.alpha(Theme.violet, 0.35) }
                GradientStop { position: 1; color: Theme.alpha(Theme.teal, 0.18) }
            }
            border.color: Theme.alpha(Theme.violetSoft, 0.35)
            Icon { anchors.centerIn: parent; name: root.icon; size: 26; color: Theme.violetSoft }
            SequentialAnimation on anchors.verticalCenterOffset {
                running: Theme.rich && root.visible
                loops: Animation.Infinite
                NumberAnimation { from: 0; to: -6; duration: 1800; easing.type: Easing.InOutSine }
                NumberAnimation { from: -6; to: 0; duration: 1800; easing.type: Easing.InOutSine }
            }
        }
    }
    AText {
        visible: root.title !== ""
        Layout.alignment: Qt.AlignHCenter
        text: root.title
        size: Theme.fsH3
        weight: Font.DemiBold
    }
    AText {
        visible: root.text !== ""
        Layout.alignment: Qt.AlignHCenter
        Layout.maximumWidth: 420
        horizontalAlignment: Text.AlignHCenter
        text: root.text
        dim: true
        wrapMode: Text.Wrap
        elide: Text.ElideNone
    }
    Button {
        visible: root.actionText !== ""
        Layout.alignment: Qt.AlignHCenter
        Layout.topMargin: 6
        variant: "primary"
        text: root.actionText
        iconName: root.actionIcon
        onClicked: root.action()
    }
}
````

### `ui/qml/Ao/Sheet.qml`

*126 строк*

````qml
import QtQuick
import QtQuick.Controls.Basic as T
import QtQuick.Layouts

// Модальное окно внутри приложения: затемнение, «всплытие» с пружиной,
// закрытие по Esc и клику мимо. Содержимое - в default-свойство.
T.Popup {
    id: sheet
    property string title: ""
    property string subtitle: ""
    property string icon: ""
    property int sheetWidth: 560
    default property alias content: body.data
    property alias footer: footerRow.data
    property bool busy: false

    parent: T.Overlay.overlay
    anchors.centerIn: parent
    width: Math.min(sheetWidth, (parent ? parent.width : sheetWidth) - 48)
    height: Math.min(implicitHeight, (parent ? parent.height : 800) - 48)
    modal: true
    focus: true
    padding: 0
    closePolicy: busy ? T.Popup.NoAutoClose : (T.Popup.CloseOnEscape | T.Popup.CloseOnPressOutside)

    T.Overlay.modal: Rectangle {
        color: Theme.overlay
        Behavior on opacity { NumberAnimation { duration: Theme.normal } }
    }

    enter: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.normal }
            NumberAnimation { property: "scale"; from: 0.94; to: 1; duration: Theme.slow
                              easing.type: Easing.OutBack; easing.overshoot: 1.2 }
        }
    }
    exit: Transition {
        ParallelAnimation {
            NumberAnimation { property: "opacity"; to: 0; duration: Theme.fast }
            NumberAnimation { property: "scale"; to: 0.97; duration: Theme.fast }
        }
    }

    background: Rectangle {
        radius: Theme.radiusXL
        color: Theme.surfaceSolid
        border.color: Theme.borderStrong
        Rectangle {
            anchors { left: parent.left; right: parent.right; top: parent.top; margins: 1 }
            height: 90
            radius: parent.radius
            gradient: Gradient {
                GradientStop { position: 0; color: Theme.alpha(Theme.violet, 0.10) }
                GradientStop { position: 1; color: "transparent" }
            }
        }
    }

    contentItem: ColumnLayout {
        spacing: 0

        RowLayout {
            Layout.fillWidth: true
            Layout.margins: 24
            Layout.bottomMargin: 8
            spacing: 14
            Rectangle {
                visible: sheet.icon !== ""
                width: 40; height: 40; radius: 12
                color: Theme.alpha(Theme.violet, 0.18)
                border.color: Theme.alpha(Theme.violetSoft, 0.3)
                Icon { anchors.centerIn: parent; name: sheet.icon; size: 18; color: Theme.violetSoft }
            }
            ColumnLayout {
                Layout.fillWidth: true
                spacing: 2
                AText { text: sheet.title; size: Theme.fsH2; weight: Font.Bold; Layout.fillWidth: true }
                AText {
                    visible: sheet.subtitle !== ""
                    text: sheet.subtitle
                    dim: true
                    size: Theme.fsSmall
                    wrapMode: Text.Wrap
                    elide: Text.ElideNone
                    Layout.fillWidth: true
                }
            }
            IconButton {
                Layout.alignment: Qt.AlignTop
                iconName: "x"
                enabled: !sheet.busy
                onClicked: sheet.close()
            }
        }

        T.ScrollView {
            id: scroll
            Layout.fillWidth: true
            Layout.fillHeight: true
            Layout.preferredHeight: body.implicitHeight + 16
            clip: true
            contentWidth: availableWidth
            T.ScrollBar.vertical: ScrollBar {}
            ColumnLayout {
                id: body
                width: scroll.availableWidth - 48
                x: 24
                y: 8
                spacing: 14
            }
        }

        Rectangle { Layout.fillWidth: true; height: 1; color: Theme.border; visible: footerRow.children.length > 0 }

        RowLayout {
            id: footerRow
            Layout.fillWidth: true
            Layout.margins: 18
            Layout.leftMargin: 24
            Layout.rightMargin: 24
            spacing: 10
            visible: children.length > 0
        }
    }
}
````

### `ui/qml/Ao/Confirm.qml`

*42 строк*

````qml
import QtQuick
import QtQuick.Layouts

// Подтверждение действия. open(title, text, callback[, danger])
Sheet {
    id: dlg
    property var onYes: null
    property bool danger: true
    property string confirmText: ""
    property string cancelText: ""
    property string actionText: ""
    sheetWidth: 440
    icon: danger ? "triangle-alert" : "circle-alert"

    function ask(title, text, callback, isDanger, yesText) {
        dlg.title = title
        dlg.subtitle = text
        dlg.onYes = callback
        dlg.danger = isDanger === undefined ? true : isDanger
        dlg.actionText = yesText ? yesText : dlg.confirmText
        open()
    }

    footer: [
        Item { Layout.fillWidth: true },
        Button {
            text: dlg.cancelText
            variant: "ghost"
            onClicked: dlg.close()
        },
        Button {
            text: dlg.actionText !== "" ? dlg.actionText : dlg.confirmText
            variant: dlg.danger ? "danger" : "primary"
            iconName: dlg.danger ? "trash-2" : "check"
            onClicked: {
                var cb = dlg.onYes
                dlg.close()
                if (cb) cb()
            }
        }
    ]
}
````

### `ui/qml/Ao/Toasts.qml`

*131 строк*

````qml
import QtQuick
import QtQuick.Layouts
import QtQuick.Effects

// Стопка уведомлений в правом верхнем углу. Каждое въезжает справа,
// показывает полосу оставшегося времени и уходит само (наведение - пауза).
Item {
    id: host
    width: 380
    property int maxVisible: 4

    function show(kind, title, message) {
        if (toastModel.count >= maxVisible) toastModel.remove(0)
        toastModel.append({ kind: kind || "info", title: title || "", message: message || "",
                            life: kind === "error" || kind === "warning" ? 7000 : 4500 })
    }

    ListModel { id: toastModel }

    ListView {
        id: list
        anchors.fill: parent
        spacing: 10
        interactive: false
        model: toastModel
        verticalLayoutDirection: ListView.TopToBottom

        add: Transition {
            ParallelAnimation {
                NumberAnimation { property: "x"; from: 420; to: 0; duration: Theme.slow; easing.type: Easing.OutBack; easing.overshoot: 0.9 }
                NumberAnimation { property: "opacity"; from: 0; to: 1; duration: Theme.normal }
            }
        }
        remove: Transition {
            ParallelAnimation {
                NumberAnimation { property: "x"; to: 420; duration: Theme.normal; easing.type: Easing.InCubic }
                NumberAnimation { property: "opacity"; to: 0; duration: Theme.normal }
            }
        }
        displaced: Transition {
            NumberAnimation { properties: "y"; duration: Theme.normal; easing.type: Easing.OutCubic }
        }

        delegate: Item {
            id: toast
            required property int index
            required property string kind
            required property string title
            required property string message
            required property int life
            width: list.width
            height: card.height
            readonly property color tint: Theme.tone(kind === "info" ? "accent" : kind)
            readonly property string glyph: kind === "success" ? "circle-check"
                                          : kind === "error" ? "octagon-x"
                                          : kind === "warning" ? "triangle-alert" : "info"

            Rectangle {
                id: card
                width: parent.width
                height: col.implicitHeight + 28
                radius: Theme.radiusL
                color: Theme.surfaceSolid
                border.color: Theme.alpha(toast.tint, 0.45)
                layer.enabled: Theme.rich
                layer.effect: MultiEffect {
                    shadowEnabled: true
                    shadowColor: Qt.rgba(0, 0, 0, 0.55)
                    shadowBlur: 0.8
                    shadowVerticalOffset: 8
                }

                RowLayout {
                    id: col
                    anchors { left: parent.left; right: parent.right; top: parent.top; margins: 14 }
                    spacing: 12
                    Rectangle {
                        Layout.alignment: Qt.AlignTop
                        width: 30; height: 30; radius: 10
                        color: Theme.alpha(toast.tint, 0.16)
                        Icon { anchors.centerIn: parent; name: toast.glyph; size: 16; color: toast.tint }
                    }
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 3
                        AText { text: toast.title; weight: Font.DemiBold; Layout.fillWidth: true; wrapMode: Text.Wrap; elide: Text.ElideNone }
                        AText {
                            visible: toast.message !== ""
                            text: toast.message
                            dim: true
                            size: Theme.fsSmall
                            Layout.fillWidth: true
                            wrapMode: Text.Wrap
                            elide: Text.ElideRight
                            maximumLineCount: 4
                        }
                    }
                    IconButton {
                        Layout.alignment: Qt.AlignTop
                        iconName: "x"
                        size: 26
                        onClicked: toastModel.remove(toast.index)
                    }
                }

                // Полоса оставшегося времени.
                Rectangle {
                    id: bar
                    anchors { left: parent.left; bottom: parent.bottom; leftMargin: 14; bottomMargin: 7 }
                    height: 2
                    radius: 1
                    color: toast.tint
                    opacity: 0.7
                    width: card.width - 28
                }
                NumberAnimation {
                    id: countdown
                    target: bar
                    property: "width"
                    from: card.width - 28
                    to: 0
                    duration: toast.life
                    running: true
                    paused: hover.hovered
                    onFinished: toastModel.remove(toast.index)
                }
                HoverHandler { id: hover }
            }
        }
    }
}
````

### `ui/qml/Ao/ProgressRing.qml`

*68 строк*

````qml
import QtQuick
import QtQuick.Shapes

// Кольцевой индикатор прогресса: дуга плавно дорастает до значения,
// а её цвет по пути переходит от фиолетового к сине-зелёному.
Item {
    id: root
    property real value: 0          // 0..1
    property int size: 72
    property real thickness: 7
    property string label: ""
    property string caption: ""
    property color from: Theme.violet
    property color to: Theme.teal
    property real shown: value
    implicitWidth: size
    implicitHeight: size
    Behavior on shown { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }

    function mix(a, b, t) {
        t = Math.max(0, Math.min(1, t))
        return Qt.rgba(a.r + (b.r - a.r) * t, a.g + (b.g - a.g) * t, a.b + (b.b - a.b) * t, 1)
    }

    Shape {
        anchors.fill: parent
        preferredRendererType: Shape.CurveRenderer
        ShapePath {
            strokeWidth: root.thickness
            strokeColor: Theme.surface3
            fillColor: "transparent"
            PathAngleArc {
                centerX: root.size / 2; centerY: root.size / 2
                radiusX: (root.size - root.thickness) / 2; radiusY: (root.size - root.thickness) / 2
                startAngle: 0; sweepAngle: 360
            }
        }
        ShapePath {
            strokeWidth: root.thickness
            fillColor: "transparent"
            capStyle: ShapePath.RoundCap
            strokeColor: root.shown > 0.002 ? root.mix(root.from, root.to, root.shown) : "transparent"
            PathAngleArc {
                centerX: root.size / 2; centerY: root.size / 2
                radiusX: (root.size - root.thickness) / 2; radiusY: (root.size - root.thickness) / 2
                startAngle: -90; sweepAngle: Math.max(0.01, Math.min(root.shown, 1)) * 360
            }
        }
    }

    Column {
        anchors.centerIn: parent
        spacing: 0
        AText {
            anchors.horizontalCenter: parent.horizontalCenter
            text: root.label
            size: root.size > 80 ? Theme.fsH2 : Theme.fsBody
            weight: Font.Bold
        }
        AText {
            visible: root.caption !== ""
            anchors.horizontalCenter: parent.horizontalCenter
            text: root.caption
            size: Theme.fsMicro
            mute: true
        }
    }
}
````

### `ui/qml/Ao/SegmentBar.qml`

*54 строк*

````qml
import QtQuick
import QtQuick.Layouts

// Полоса прогресса по статусам: сегменты растут плавно, а под полосой - легенда.
ColumnLayout {
    id: root
    property var segments: []      // [{status, title, count}]
    property bool legend: true
    readonly property int total: {
        var t = 0
        for (var i = 0; i < segments.length; ++i) t += segments[i].count
        return t
    }
    spacing: 10

    Rectangle {
        id: track
        Layout.fillWidth: true
        height: 10
        radius: 5
        color: Theme.surface3
        clip: true
        Row {
            anchors.fill: parent
            spacing: 2
            Repeater {
                model: root.segments
                delegate: Rectangle {
                    required property var modelData
                    height: track.height
                    width: root.total > 0 ? Math.max(0, (track.width - 2 * (root.segments.length - 1)) * modelData.count / root.total) : 0
                    radius: 5
                    color: Theme.statusColor(modelData.status)
                    Behavior on width { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }
                }
            }
        }
    }

    Flow {
        visible: root.legend && root.segments.length > 0
        Layout.fillWidth: true
        spacing: 14
        Repeater {
            model: root.segments
            delegate: Row {
                required property var modelData
                spacing: 6
                Rectangle { width: 8; height: 8; radius: 4; color: Theme.statusColor(modelData.status); anchors.verticalCenter: parent.verticalCenter }
                AText { text: modelData.title + " · " + modelData.count; size: Theme.fsSmall; dim: true }
            }
        }
    }
}
````

### `ui/qml/Ao/LineChart.qml`

*156 строк*

````qml
import QtQuick

// Кривая нарастающего итога: градиентная заливка, «прорисовка» слева
// направо при обновлении и перекрестие с подсказкой при наведении.
Item {
    id: root
    property var points: []          // [{label, value}]
    property string unit: "tokens"   // tokens | usd
    property color lineColor: Theme.violetSoft
    property color fillColor: Theme.violet
    property string emptyText: ""
    property real reveal: 1
    property int hoverIndex: -1

    readonly property real maxValue: {
        var m = 0
        for (var i = 0; i < points.length; ++i) m = Math.max(m, points[i].value)
        return m > 0 ? m * 1.12 : 1
    }
    readonly property int padL: 8
    readonly property int padB: 18

    function fmt(v) {
        if (unit === "usd") return v >= 1 ? "$" + v.toFixed(2) : "$" + v.toFixed(v >= 0.01 ? 3 : 4)
        if (v >= 1e6) return (v / 1e6).toFixed(2) + "M"
        if (v >= 1e4) return (v / 1e3).toFixed(1) + "k"
        return Math.round(v).toString()
    }
    function px(i) { return padL + (points.length > 1 ? i / (points.length - 1) : 0.5) * (width - padL * 2) }
    function py(v) { return (height - padB) - (v / maxValue) * (height - padB - 10) }

    onPointsChanged: {
        canvas.requestPaint()
        if (Theme.rich && points.length > 1) { reveal = 0; revealAnim.restart() }
    }
    onRevealChanged: canvas.requestPaint()
    onWidthChanged: canvas.requestPaint()
    onHeightChanged: canvas.requestPaint()
    NumberAnimation { id: revealAnim; target: root; property: "reveal"; from: 0; to: 1; duration: 900; easing.type: Easing.OutCubic }

    Canvas {
        id: canvas
        anchors.fill: parent
        renderTarget: Canvas.FramebufferObject
        onPaint: {
            var ctx = getContext("2d")
            ctx.reset()
            var n = root.points.length
            // Сетка
            ctx.strokeStyle = Qt.rgba(1, 1, 1, 0.05)
            ctx.lineWidth = 1
            for (var g = 0; g <= 3; ++g) {
                var gy = root.py(root.maxValue / 1.12 * g / 3)
                ctx.beginPath(); ctx.moveTo(root.padL, gy); ctx.lineTo(width - root.padL, gy); ctx.stroke()
            }
            if (n < 2) return
            var limitX = root.padL + (width - root.padL * 2) * root.reveal
            ctx.save()
            ctx.beginPath()
            ctx.rect(0, 0, limitX + 1, height)
            ctx.clip()
            // Заливка
            var grad = ctx.createLinearGradient(0, 0, 0, height - root.padB)
            grad.addColorStop(0, Qt.rgba(root.fillColor.r, root.fillColor.g, root.fillColor.b, 0.35))
            grad.addColorStop(1, Qt.rgba(root.fillColor.r, root.fillColor.g, root.fillColor.b, 0.0))
            ctx.beginPath()
            ctx.moveTo(root.px(0), height - root.padB)
            for (var i = 0; i < n; ++i) ctx.lineTo(root.px(i), root.py(root.points[i].value))
            ctx.lineTo(root.px(n - 1), height - root.padB)
            ctx.closePath()
            ctx.fillStyle = grad
            ctx.fill()
            // Линия
            ctx.beginPath()
            for (var j = 0; j < n; ++j) {
                var x = root.px(j), y = root.py(root.points[j].value)
                if (j === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y)
            }
            ctx.strokeStyle = root.lineColor
            ctx.lineWidth = 2.2
            ctx.lineJoin = "round"
            ctx.stroke()
            ctx.restore()
        }
    }

    // Подписи оси: первая и последняя метка времени, максимум слева сверху.
    AText {
        visible: root.points.length > 1
        text: root.fmt(root.maxValue / 1.12)
        mute: true; size: Theme.fsMicro; mono: true
        x: root.padL + 2; y: 0
    }
    AText {
        visible: root.points.length > 1
        text: root.points.length ? root.points[0].label : ""
        mute: true; size: Theme.fsMicro
        x: root.padL; anchors.bottom: parent.bottom
    }
    AText {
        visible: root.points.length > 1
        text: root.points.length ? root.points[root.points.length - 1].label : ""
        mute: true; size: Theme.fsMicro
        anchors.right: parent.right; anchors.rightMargin: root.padL; anchors.bottom: parent.bottom
    }

    // Перекрестие и подсказка.
    Rectangle {
        visible: root.hoverIndex >= 0
        x: root.hoverIndex >= 0 ? root.px(root.hoverIndex) : 0
        y: 0; width: 1; height: root.height - root.padB
        color: Theme.alpha(Theme.text, 0.18)
    }
    Rectangle {
        visible: root.hoverIndex >= 0
        width: 10; height: 10; radius: 5
        color: root.lineColor
        border.color: Theme.bg; border.width: 2
        x: root.hoverIndex >= 0 ? root.px(root.hoverIndex) - 5 : 0
        y: root.hoverIndex >= 0 ? root.py(root.points[root.hoverIndex].value) - 5 : 0
    }
    Rectangle {
        visible: root.hoverIndex >= 0
        radius: Theme.radiusS
        color: Theme.surface3
        border.color: Theme.borderStrong
        width: tipText.implicitWidth + 16
        height: tipText.implicitHeight + 10
        x: root.hoverIndex >= 0 ? Math.min(Math.max(0, root.px(root.hoverIndex) - width / 2), root.width - width) : 0
        y: 4
        AText {
            id: tipText
            anchors.centerIn: parent
            size: Theme.fsSmall
            text: root.hoverIndex >= 0 ? root.points[root.hoverIndex].label + "  ·  " + root.fmt(root.points[root.hoverIndex].value) : ""
        }
    }
    MouseArea {
        anchors.fill: parent
        hoverEnabled: true
        onPositionChanged: function(mouse) {
            var n = root.points.length
            if (n < 2) { root.hoverIndex = -1; return }
            var t = (mouse.x - root.padL) / (root.width - root.padL * 2)
            root.hoverIndex = Math.max(0, Math.min(n - 1, Math.round(t * (n - 1))))
        }
        onExited: root.hoverIndex = -1
    }

    AText {
        anchors.centerIn: parent
        visible: root.points.length < 2
        text: root.emptyText
        mute: true
    }
}
````

### `ui/qml/Ao/BarList.qml`

*62 строк*

````qml
import QtQuick
import QtQuick.Layouts

// Горизонтальные полосы «кто сколько потратил»; полосы дорастают плавно.
ColumnLayout {
    id: root
    property var bars: []        // [{label, value, text, cost, supervisor}]
    property string emptyText: ""
    readonly property real maxValue: {
        var m = 0
        for (var i = 0; i < bars.length; ++i) m = Math.max(m, bars[i].value)
        return m || 1
    }
    spacing: 12

    Repeater {
        model: root.bars
        delegate: ColumnLayout {
            required property var modelData
            required property int index
            Layout.fillWidth: true
            spacing: 5
            RowLayout {
                Layout.fillWidth: true
                Icon {
                    name: modelData.supervisor ? "shield-check" : "bot"
                    size: 13
                    color: modelData.supervisor ? Theme.violetSoft : Theme.textMute
                }
                AText { text: modelData.label; size: Theme.fsSmall; Layout.fillWidth: true }
                AText { text: modelData.text; size: Theme.fsSmall; mono: true; dim: true }
                AText { text: modelData.cost; size: Theme.fsSmall; mono: true; mute: true }
            }
            Rectangle {
                Layout.fillWidth: true
                height: 8
                radius: 4
                color: Theme.surface3
                Rectangle {
                    id: fill
                    height: parent.height
                    radius: 4
                    width: 0
                    gradient: Gradient {
                        orientation: Gradient.Horizontal
                        GradientStop { position: 0; color: modelData.supervisor ? Theme.magenta : Theme.violet }
                        GradientStop { position: 1; color: modelData.supervisor ? Theme.violetSoft : Theme.cyan }
                    }
                    Behavior on width { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }
                    Component.onCompleted: width = Qt.binding(function() { return parent.width * modelData.value / root.maxValue })
                }
            }
        }
    }

    AText {
        visible: root.bars.length === 0
        text: root.emptyText
        mute: true
        Layout.alignment: Qt.AlignHCenter
    }
}
````

### `ui/qml/Ao/Ticker.qml`

*25 строк*

````qml
import QtQuick

// Число, которое «досчитывает» до нового значения.
AText {
    id: root
    property real value: 0
    property string unit: "int"     // int | tokens | usd | percent | fraction
    property real shown: 0
    property string total: ""
    Behavior on shown { NumberAnimation { duration: Theme.slow * 2; easing.type: Easing.OutCubic } }
    onValueChanged: shown = value
    Component.onCompleted: shown = value

    function fmt(v) {
        if (unit === "usd") return v >= 100 ? "$" + Math.round(v) : v >= 1 ? "$" + v.toFixed(2) : v === 0 ? "$0" : "$" + v.toFixed(v >= 0.01 ? 3 : 4)
        if (unit === "tokens") {
            if (v >= 1e6) return (v / 1e6).toFixed(2) + "M"
            if (v >= 1e4) return (v / 1e3).toFixed(1) + "k"
            return Math.round(v).toLocaleString(Qt.locale("ru_RU"), "f", 0)
        }
        if (unit === "percent") return Math.round(v * 100) + "%"
        return Math.round(v).toString()
    }
    text: fmt(shown) + (total !== "" ? " / " + total : "")
}
````

### `ui/qml/Ao/Aurora.qml`

*78 строк*

````qml
import QtQuick
import QtQuick.Shapes

// Живой фон: крупные размытые «сияния» фиолетового, бирюзового и голубого
// медленно дрейфуют под интерфейсом. На сдержанном уровне движения замирают,
// оставаясь мягким градиентом; при выключенных анимациях - неподвижны.
Item {
    id: root
    property real intensity: 1.0
    clip: true

    Rectangle { anchors.fill: parent; color: Theme.bg }

    component Glow: Shape {
        id: glow
        property color tint: Theme.violet
        property real strength: 0.5
        property int radius: 420
        property real driftX: 120
        property real driftY: 80
        property int period: 22000
        property real baseX: 0
        property real baseY: 0
        width: radius * 2
        height: radius * 2
        x: baseX - radius
        y: baseY - radius
        preferredRendererType: Shape.GeometryRenderer
        opacity: root.intensity
        ShapePath {
            strokeColor: "transparent"
            fillGradient: RadialGradient {
                centerX: glow.radius; centerY: glow.radius; centerRadius: glow.radius
                focalX: glow.radius; focalY: glow.radius
                GradientStop { position: 0.0; color: Qt.rgba(glow.tint.r, glow.tint.g, glow.tint.b, glow.strength) }
                GradientStop { position: 0.45; color: Qt.rgba(glow.tint.r, glow.tint.g, glow.tint.b, glow.strength * 0.35) }
                GradientStop { position: 1.0; color: "transparent" }
            }
            PathAngleArc {
                centerX: glow.radius; centerY: glow.radius
                radiusX: glow.radius; radiusY: glow.radius
                startAngle: 0; sweepAngle: 360
            }
        }
        transform: Translate { id: shift }
        SequentialAnimation {
            running: Theme.rich && root.visible
            loops: Animation.Infinite
            ParallelAnimation {
                NumberAnimation { target: shift; property: "x"; to: glow.driftX; duration: glow.period; easing.type: Easing.InOutSine }
                NumberAnimation { target: shift; property: "y"; to: glow.driftY; duration: glow.period; easing.type: Easing.InOutSine }
            }
            ParallelAnimation {
                NumberAnimation { target: shift; property: "x"; to: -glow.driftX * 0.6; duration: glow.period * 1.1; easing.type: Easing.InOutSine }
                NumberAnimation { target: shift; property: "y"; to: glow.driftY * 0.4; duration: glow.period * 1.1; easing.type: Easing.InOutSine }
            }
            ParallelAnimation {
                NumberAnimation { target: shift; property: "x"; to: 0; duration: glow.period; easing.type: Easing.InOutSine }
                NumberAnimation { target: shift; property: "y"; to: 0; duration: glow.period; easing.type: Easing.InOutSine }
            }
        }
    }

    Glow { tint: Theme.violet; strength: 0.34; radius: 520; baseX: root.width * 0.18; baseY: root.height * 0.10; driftX: 160; driftY: 120; period: 26000 }
    Glow { tint: Theme.teal; strength: 0.20; radius: 460; baseX: root.width * 0.92; baseY: root.height * 0.22; driftX: -140; driftY: 150; period: 30000 }
    Glow { tint: Theme.cyan; strength: 0.14; radius: 420; baseX: root.width * 0.70; baseY: root.height * 0.98; driftX: -170; driftY: -90; period: 34000 }
    Glow { tint: Theme.magenta; strength: 0.12; radius: 380; baseX: root.width * 0.05; baseY: root.height * 0.95; driftX: 120; driftY: -110; period: 38000 }

    // Лёгкая виньетка, чтобы края не спорили с контентом.
    Rectangle {
        anchors.fill: parent
        gradient: Gradient {
            GradientStop { position: 0.0; color: Theme.alpha(Theme.bg, 0.0) }
            GradientStop { position: 0.75; color: Theme.alpha(Theme.bg, 0.25) }
            GradientStop { position: 1.0; color: Theme.alpha(Theme.bg, 0.7) }
        }
    }
}
````

### `ui/qml/Ao/OrbitLogo.qml`

*79 строк*

````qml
import QtQuick
import QtQuick.Shapes

// Знак приложения: центральный узел-«оркестратор» и спутники-агенты на
// орбитах, связанные с центром. Вращение - только при полном движении.
Item {
    id: root
    property int size: 40
    property bool animated: true
    property real speed: 1.0
    implicitWidth: size
    implicitHeight: size

    readonly property real r1: size * 0.30
    readonly property real r2: size * 0.44

    Shape {
        anchors.fill: parent
        preferredRendererType: Shape.CurveRenderer
        ShapePath {
            strokeColor: Theme.alpha(Theme.violetSoft, 0.28)
            strokeWidth: Math.max(1, root.size / 48)
            fillColor: "transparent"
            strokeStyle: ShapePath.DashLine
            dashPattern: [2, 3]
            PathAngleArc { centerX: root.size / 2; centerY: root.size / 2; radiusX: root.r1; radiusY: root.r1; startAngle: 0; sweepAngle: 360 }
        }
        ShapePath {
            strokeColor: Theme.alpha(Theme.cyan, 0.22)
            strokeWidth: Math.max(1, root.size / 48)
            fillColor: "transparent"
            PathAngleArc { centerX: root.size / 2; centerY: root.size / 2; radiusX: root.r2; radiusY: root.r2; startAngle: 0; sweepAngle: 360 }
        }
    }

    // Центральный узел с градиентом.
    Rectangle {
        anchors.centerIn: parent
        width: root.size * 0.30; height: width; radius: width / 2
        gradient: Gradient {
            GradientStop { position: 0; color: Theme.violetSoft }
            GradientStop { position: 1; color: Theme.indigo }
        }
        Rectangle {
            anchors.centerIn: parent
            width: parent.width * 1.9; height: width; radius: width / 2
            color: "transparent"
            border.width: Math.max(1, root.size / 40)
            border.color: Theme.alpha(Theme.violet, 0.25)
        }
    }

    component Satellite: Item {
        id: sat
        property real orbit: root.r1
        property real phase: 0
        property color tint: Theme.teal
        property real dot: root.size * 0.12
        property int period: 9000
        anchors.fill: parent
        rotation: phase
        Rectangle {
            width: sat.dot; height: sat.dot; radius: sat.dot / 2
            color: sat.tint
            x: root.size / 2 + sat.orbit - sat.dot / 2
            y: root.size / 2 - sat.dot / 2
        }
        NumberAnimation on rotation {
            from: sat.phase; to: sat.phase + 360
            duration: sat.period / root.speed
            loops: Animation.Infinite
            running: root.animated && Theme.rich && root.visible
        }
    }

    Satellite { orbit: root.r1; phase: 20; tint: Theme.teal; period: 7000 }
    Satellite { orbit: root.r2; phase: 150; tint: Theme.cyan; period: 11000; dot: root.size * 0.10 }
    Satellite { orbit: root.r2; phase: 270; tint: Theme.magenta; period: 13000; dot: root.size * 0.09 }
}
````


## Служебное и тесты

### `utils/asyncutils.py`

*68 строк*

````python
"""Мост между Qt и asyncio.

Ответ на вопрос 2: в приложении ОДИН asyncio-луп, который qasync делает
общим с циклом событий Qt. Агенты - это корутины/таски в этом лупе, поэтому
15+ параллельных агентов не превращаются в 15 потоков. Блокирующие вызовы
(sqlite, ddgs, чтение файлов) уводятся в пул потоков через ``asyncio.to_thread``,
исполнение кода - в отдельный процесс.
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

### `tests/conftest.py`

*24 строк*

````python
"""Общая настройка pytest: изолированный каталог данных и путь к проекту.

Каталог данных задаётся ДО импорта модулей приложения: ``app.config``
вычисляет пути при импорте, и тесты не должны трогать реальный профиль.
"""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

_HOME = Path(tempfile.mkdtemp(prefix="aiorc_pytest_"))
os.environ["AGENTFORGE_HOME"] = str(_HOME)


def pytest_sessionfinish(session, exitstatus):  # noqa: ARG001
    shutil.rmtree(_HOME, ignore_errors=True)
````

### `tests/fakes.py`

*178 строк*

````python
"""Подменные провайдеры и каркас сценариев для тестов ядра.

Общие для ``tests/smoke.py`` и pytest-тестов. Модуль не трогает переменные
окружения: каталог данных задаёт тот, кто запускает тесты.
"""

from __future__ import annotations

import asyncio
import itertools

import core.orchestrator as orchestrator_module
from app.config import DEFAULT_WORKSPACE_SETTINGS
from core.hitl import Decision
from core.orchestrator import Orchestrator
from core.supervisor.supervisor import Supervisor, SupervisorModel
from providers.base import CompletionResult, LLMProvider, ToolCall, Usage
from storage.db import Database
from storage.repositories import Repos, UserRepo

_counter = itertools.count()


class Worker(LLMProvider):
    """Исполнитель: при наличии инструментов сначала вызывает один из них."""

    def __init__(self, name: str = "agent", confidence: str = "0.9",
                 use_tool: bool = False, tokens: tuple[int, int] = (200, 80),
                 delay: float = 0.0, always_tool: bool = False) -> None:
        super().__init__()
        self.name = name
        self.confidence = confidence
        self.use_tool = use_tool
        self.always_tool = always_tool
        self.tokens = tokens
        self.delay = delay
        self.calls = 0
        self.tool_rounds = 0

    async def list_models(self) -> list[str]:
        return ["fake-model"]

    async def aclose(self) -> None:
        return None

    async def complete(self, model, messages, *, temperature=0.7,
                       max_tokens=2048, tools=None):
        self.calls += 1
        if self.delay:
            await asyncio.sleep(self.delay)
        if tools and (self.always_tool or (self.use_tool and self.calls == 1)):
            self.tool_rounds += 1
            return CompletionResult(
                text="Посчитаю в песочнице.",
                tool_calls=[ToolCall(f"call-{self.calls}", "code_exec",
                                     {"code": "print(6 * 7)", "language": "python"})],
                usage=Usage(*self.tokens),
            )
        return CompletionResult(
            text=(f"Готово.\nCONFIDENCE: {self.confidence}\n"
                  f"RESULT:\nРезультат от {self.name}, попытка {self.calls}."),
            usage=Usage(*self.tokens),
        )


class SupervisorProvider(LLMProvider):
    """Проверяющий: вердикты задаются списком, остальное - заглушки."""

    def __init__(self, verdicts: list[str] | None = None,
                 conflicts: str = '{"conflicts": []}',
                 tokens: tuple[int, int] = (150, 20), fail_reviews: bool = False) -> None:
        super().__init__()
        self.verdicts = verdicts or []
        self.conflicts = conflicts
        self.tokens = tokens
        self.fail_reviews = fail_reviews
        self.reviews = 0
        self.calls = 0

    async def list_models(self) -> list[str]:
        return ["fake-model"]

    async def aclose(self) -> None:
        return None

    async def complete(self, model, messages, **kwargs):
        from providers.base import ProviderError

        self.calls += 1
        system, user = messages[0].content, messages[1].content
        if "ПРОВЕРЯЕМАЯ ПОДЗАДАЧА" in user:
            self.reviews += 1
            if self.fail_reviews:
                raise ProviderError("503: сервис проверки недоступен", 503)
            if self.reviews <= len(self.verdicts):
                return CompletionResult(text=self.verdicts[self.reviews - 1],
                                        usage=Usage(*self.tokens))
            return CompletionResult(text='{"verdict":"ok","notes":"","issues":[]}',
                                    usage=Usage(*self.tokens))
        if "Сравни результаты" in system:
            return CompletionResult(text=self.conflicts, usage=Usage(*self.tokens))
        return CompletionResult(
            text=("ФАКТЫ:\nработа идёт\nРАСХОЖДЕНИЯ:\nнет\nОТКРЫТЫЕ ВОПРОСЫ:\nнет"),
            usage=Usage(*self.tokens),
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
                if decision not in request.options:
                    decision = request.options[0]
                gate.resolve(request.id, decision, comment)
            await asyncio.sleep(0.02)

    helper = asyncio.ensure_future(responder())
    try:
        return await asyncio.wait_for(orch.run_task(workspace_id, task_id), timeout)
    finally:
        helper.cancel()
````

### `tests/smoke.py`

*344 строк*

````python
"""Смоук-тесты ядра: все девять этапов MVP без сети и без GUI.

Запуск::

    python tests/smoke.py

Модели подменяются фейковыми провайдерами, поэтому тесты не ходят в интернет,
не тратят токены и выполняются за секунды. Проверяется именно логика ядра:
шифрование, изоляция агентов, конвейер выполнения, супервайзер, паузы,
экспорт и бюджеты. Интерфейс сюда не входит - его надо смотреть глазами.
"""

from __future__ import annotations

import asyncio
import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Изолированный каталог данных, чтобы не трогать реальный профиль.
_TEMP_HOME = Path(tempfile.mkdtemp(prefix="aiorc_smoke_"))
os.environ["AGENTFORGE_HOME"] = str(_TEMP_HOME)

from app.config import PATHS  # noqa: E402
from core.budget import load_states  # noqa: E402
from core.events import EventBus, EventType  # noqa: E402
from core.export.bundle import ExportOptions, collect, detect_format  # noqa: E402
from core.export.exporters import export, suggest_filename  # noqa: E402
from core.hitl import Decision  # noqa: E402
from core.orchestrator import Orchestrator  # noqa: E402

_passed: list[str] = []
_failed: list[str] = []


def check(name: str, condition: bool, detail: str = "") -> None:
    """Печатает результат одной проверки и копит статистику."""
    mark = "OK  " if condition else "FAIL"
    print(f"  [{mark}] {name}" + (f" - {detail}" if detail else ""))
    (_passed if condition else _failed).append(name)


# Подменные провайдеры и каркас сценариев вынесены в tests/fakes.py:
# их же используют pytest-тесты.
from tests.fakes import (  # noqa: E402
    SupervisorProvider,
    Worker,
    build_project,
    drive,
    patch_supervisor,
)


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

    await drive(orch, workspace.id, task.id,
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

    await drive(orch, workspace.id, task.id)
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
            print(f"  [SKIP] {optional} - пакет {module} не установлен")
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
    print("Смоук-тесты Agent Forge (без сети, без GUI)")
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

### `tests/test_core_fixes.py`

*430 строк*

````python
"""Регрессионные тесты на исправления ядра версии 1.1.

Каждый тест фиксирует конкретную ошибку, найденную при ревью: если она
вернётся, тест упадёт с понятным названием.
"""

from __future__ import annotations

import json

import httpx
import pytest

from core.budget import BudgetGuard
from core.events import EventBus, EventType
from core.hitl import ApprovalGate, Decision, Reason
from core.orchestrator import Orchestrator
from core.supervisor.checklist import Anonymizer
from providers.base import ChatMessage, ToolSpec
from storage.db import Database
from storage.repositories import Repos, UserRepo
from tests.fakes import SupervisorProvider, Worker, build_project, drive, patch_supervisor


def _events(bus: EventBus, *types: EventType) -> list:
    seen: list = []
    bus.subscribe(lambda e: seen.append(e) if not types or e.type in types else None)
    return seen


# --- хранилище ----------------------------------------------------------------


def test_history_returns_latest_messages_in_order():
    repos, _, task, agents, _ = build_project(subtask_count=1)
    subtask = repos.tasks.subtasks(task.id)[0]
    for i in range(10):
        repos.messages.add(agents[0].id, "user", f"сообщение {i}", subtask.id)
    rows = repos.messages.history(agents[0].id, subtask.id, limit=3)
    assert [r["content"] for r in rows] == ["сообщение 7", "сообщение 8", "сообщение 9"]


def test_change_password_is_atomic(monkeypatch):
    repos, _, _, _, key = build_project()
    original = repos.db.transaction

    def broken_transaction():
        class Boom:
            def __enter__(self_inner):
                self_inner.ctx = original()
                conn = self_inner.ctx.__enter__()

                class Proxy:
                    def executemany(self, *a):
                        return conn.executemany(*a)

                    def execute(self, sql, *a):
                        if sql.startswith("UPDATE users"):
                            raise RuntimeError("сбой диска посередине")
                        return conn.execute(sql, *a)
                return Proxy()

            def __exit__(self_inner, *exc):
                return self_inner.ctx.__exit__(*exc)
        return Boom()

    monkeypatch.setattr(repos.db, "transaction", broken_transaction)
    with pytest.raises(RuntimeError):
        repos.users.change_password(repos.session, "password123", "newpassword456")
    monkeypatch.undo()

    # Старый пароль по-прежнему открывает профиль, и ключ им же расшифровывается.
    session = repos.users.authenticate(repos.session.username, "password123")
    assert session is not None
    assert Repos(repos.db, session).keys.reveal(key.id) == "sk-secret-value"


def test_secret_codec_roundtrip_and_plain_fallback():
    repos, *_ = build_project()
    sealed = repos.secrets.seal("tvly-123")
    assert sealed.startswith("enc:") and "tvly-123" not in sealed
    assert repos.secrets.open(sealed) == "tvly-123"
    assert repos.secrets.open("legacy-plain") == "legacy-plain"
    assert repos.secrets.open("") == ""


def test_recover_interrupted_runs_resets_stale_statuses():
    repos, _, task, agents, _ = build_project(subtask_count=1)
    subtask = repos.tasks.subtasks(task.id)[0]
    repos.tasks.update(task.id, status="running")
    repos.tasks.update_subtask(subtask.id, status="running")
    repos.agents.set_status(agents[0].id, "running")
    assert repos.recover_interrupted_runs() >= 3
    assert repos.tasks.get(task.id).status == "stopped"
    assert repos.tasks.get_subtask(subtask.id).status == "paused"
    assert repos.agents.get(agents[0].id).status == "idle"


# --- оркестратор ----------------------------------------------------------------


async def test_agent_lock_is_taken_before_concurrency_slot():
    """Подзадачи одного агента не должны занимать слоты, ожидая свой же лок."""
    repos, ws, task, agents, _ = build_project(subtask_count=0)
    for i in range(3):
        repos.tasks.add_subtask(task.id, f"A{i}", "", agents[0].id)
    repos.tasks.add_subtask(task.id, "B", "", agents[1].id)

    bus = EventBus()
    seen = _events(bus, EventType.SUBTASK_STARTED, EventType.SUBTASK_FINISHED)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, bus)
    workers = {a.id: Worker(a.name, delay=0.05) for a in agents}
    orch._provider_for = lambda agent: workers[agent.id]

    await drive(orch, ws.id, task.id)  # параллельность по умолчанию достаточна
    repos2, ws2, task2, agents2, _ = build_project(subtask_count=0)
    for i in range(3):
        repos2.tasks.add_subtask(task2.id, f"A{i}", "", agents2[0].id)
    b = repos2.tasks.add_subtask(task2.id, "B", "", agents2[1].id)
    bus2 = EventBus()
    seen2 = _events(bus2, EventType.SUBTASK_STARTED, EventType.SUBTASK_FINISHED)
    orch2 = Orchestrator(repos2, bus2)
    workers2 = {a.id: Worker(a.name, delay=0.05) for a in agents2}
    orch2._provider_for = lambda agent: workers2[agent.id]
    await drive_with_concurrency(orch2, ws2.id, task2.id, concurrency=2)

    first_finish = next(i for i, e in enumerate(seen2) if e.type is EventType.SUBTASK_FINISHED)
    b_start = next(i for i, e in enumerate(seen2)
                   if e.type is EventType.SUBTASK_STARTED and e.subtask_id == b.id)
    assert b_start < first_finish, "агент B ждал, пока A освободит слоты"
    assert len([e for e in seen if e.type is EventType.SUBTASK_FINISHED]) == 4


async def drive_with_concurrency(orch, ws_id, task_id, concurrency):
    return await orch.run_task(ws_id, task_id, concurrency=concurrency)


async def test_failed_dependency_is_reported_as_such():
    repos, ws, task, agents, _ = build_project(subtask_count=2)
    first, second = repos.tasks.subtasks(task.id)
    repos.tasks.update_subtask(second.id, depends_on=str(first.id))
    repos.agents.update(agents[0].id, enabled=False)      # первая упадёт сразу

    bus = EventBus()
    failed = _events(bus, EventType.SUBTASK_FAILED)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, bus)
    orch._provider_for = lambda agent: Worker(agent.name)
    await drive(orch, ws.id, task.id)

    messages = " | ".join(e.message for e in failed)
    assert "не выполнена зависимость «Подзадача 1»" in messages
    assert "цикл" not in messages


async def test_cycle_is_reported_as_cycle():
    repos, ws, task, _, _ = build_project(subtask_count=2)
    first, second = repos.tasks.subtasks(task.id)
    repos.tasks.update_subtask(first.id, depends_on=str(second.id))
    repos.tasks.update_subtask(second.id, depends_on=str(first.id))
    bus = EventBus()
    failed = _events(bus, EventType.SUBTASK_FAILED)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, bus)
    orch._provider_for = lambda agent: Worker(agent.name)
    await drive(orch, ws.id, task.id)
    assert any("замкнуты в цикл" in e.message for e in failed)


async def test_unverified_result_does_not_flow_to_dependents_without_hitl():
    repos, ws, task, _, _ = build_project(subtask_count=2)
    first, second = repos.tasks.subtasks(task.id)
    repos.tasks.update_subtask(second.id, depends_on=str(first.id))
    patch_supervisor(SupervisorProvider(fail_reviews=True))
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: Worker(agent.name)
    state = await drive(orch, ws.id, task.id)

    statuses = {s.id: s.status for s in repos.tasks.subtasks(task.id)}
    assert statuses[first.id] == "review"      # ждёт человека, не «done»
    assert statuses[second.id] == "error"      # на непроверенном не строим
    assert state.finished == 0 and state.escalated == 1
    assert any(i.kind == "unverified" for i in repos.incidents.list(ws.id))


async def test_unverified_result_asks_human_when_hitl_on():
    repos, ws, task, _, _ = build_project(
        subtask_count=1, settings={"human_in_the_loop": True,
                                   "hitl_confidence_threshold": 0.0})
    patch_supervisor(SupervisorProvider(fail_reviews=True))
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: Worker(agent.name)
    state = await drive(orch, ws.id, task.id, answers=[(Decision.APPROVE, "проверил сам")])
    history = repos.approvals.history(ws.id)
    assert history and history[0]["reason"] == Reason.UNVERIFIED.value
    assert state.finished == 1
    assert repos.tasks.subtasks(task.id)[0].status == "done"


async def test_supervisor_spend_counts_toward_task_limit():
    repos, ws, task, _, _ = build_project(subtask_count=2, token_limit=600)
    first, second = repos.tasks.subtasks(task.id)
    repos.tasks.update_subtask(second.id, depends_on=str(first.id))
    # Исполнитель: 280 токенов; супервайзер: 400 на каждую проверку.
    patch_supervisor(SupervisorProvider(tokens=(350, 50)))
    orch = Orchestrator(repos, EventBus())
    worker = Worker("A", tokens=(200, 80))
    orch._provider_for = lambda agent: worker
    state = await drive(orch, ws.id, task.id)

    # Без учёта супервайзера лимит 600 пропустил бы обе подзадачи
    # (2 × 280 = 560). С учётом - вторая упирается в лимит.
    assert worker.calls == 1
    assert state.tokens >= 280 + 400
    assert repos.tasks.subtasks(task.id)[1].status == "error"


async def test_budget_exceeded_event_is_emitted_once():
    repos, ws, task, agents, _ = build_project(subtask_count=3, agent_count=3)
    repos.budgets.upsert("workspace", ws.id, 100, None, 0.8)
    bus = EventBus()
    exceeded = _events(bus, EventType.BUDGET_EXCEEDED)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, bus)
    orch._provider_for = lambda agent: Worker(agent.name, delay=0.02)
    await drive(orch, ws.id, task.id)
    assert len(exceeded) == 1


async def test_budget_extension_with_hitl_continues_the_run():
    repos, ws, task, agents, _ = build_project(
        subtask_count=2, agent_count=1,
        settings={"human_in_the_loop": True, "hitl_confidence_threshold": 0.0})
    first, second = repos.tasks.subtasks(task.id)
    repos.tasks.update_subtask(second.id, depends_on=str(first.id))
    repos.budgets.upsert("agent", agents[0].id, 250, None, 0.9)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, EventBus())
    worker = Worker("A", tokens=(200, 80))
    orch._provider_for = lambda agent: worker
    state = await drive(orch, ws.id, task.id, answers=[(Decision.EXTEND, "")])

    assert state.finished == 2
    reasons = [r["reason"] for r in repos.approvals.history(ws.id)]
    assert Reason.BUDGET.value in reasons
    assert repos.budgets.get("agent", agents[0].id).token_limit >= 420


async def test_steps_exhausted_on_tools_gets_a_real_summary():
    repos, ws, task, _, _ = build_project(subtask_count=1,
                                          settings={"agent_max_steps": 2})
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, EventBus())
    worker = Worker("A", always_tool=True)
    orch._provider_for = lambda agent: worker
    await drive(orch, ws.id, task.id)
    subtask = repos.tasks.subtasks(task.id)[0]
    # Два шага ушли на инструменты, третий вызов - подведение итога.
    assert worker.calls == 3
    assert subtask.result.startswith("Результат от A")
    assert "Посчитаю в песочнице" not in subtask.result


async def test_agent_output_is_streamed_to_the_bus():
    repos, ws, task, _, _ = build_project(subtask_count=1)
    bus = EventBus()
    deltas = _events(bus, EventType.AGENT_DELTA)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, bus)
    orch._provider_for = lambda agent: Worker(agent.name)
    await drive(orch, ws.id, task.id)
    text = "".join(e.message for e in deltas)
    assert "RESULT:" in text
    assert all(e.payload.get("stream") == "text" for e in deltas)


# --- human-in-the-loop -----------------------------------------------------------


async def test_gate_rejects_unknown_and_foreign_decisions():
    db = Database()
    session = UserRepo(db).create("gate-user", "password123")
    repos = Repos(db, session)
    ws = repos.workspaces.create(session.user_id, "ws", "", {})
    gate = ApprovalGate(repos, EventBus(), ws.id)

    import asyncio

    asking = asyncio.ensure_future(gate.ask(Reason.MILESTONE, "Продолжать?"))
    await asyncio.sleep(0)
    request = gate.pending()[0]
    assert gate.resolve(request.id, "definitely-not-a-decision") is False
    assert gate.resolve(request.id, Decision.REWORK) is False   # не из вариантов вехи
    assert gate.resolve(request.id, Decision.APPROVE) is True
    assert (await asking).decision is Decision.APPROVE


# --- супервайзер -------------------------------------------------------------------


def test_scrub_replaces_whole_words_longest_first():
    anon = Anonymizer()
    names = {1: "Лев", 2: "Аналитик Пётр"}
    out = anon.scrub("Аналитик Пётр и Лев согласны; Левша тоже.", names)
    assert "Левша" in out                      # «Лев» не режет чужое слово
    assert "Пётр" not in out
    assert out.count("Исполнитель") == 2


def test_budget_guard_extend_updates_task_form_limit():
    repos, ws, task, agents, _ = build_project(subtask_count=1, token_limit=1000)
    guard = BudgetGuard(repos, EventBus(), ws.id, task.id, task.token_limit)
    state = next(s for s in guard.snapshot() if s.scope == "task")
    state.tokens = 1200
    guard.extend(state)
    assert repos.tasks.get(task.id).token_limit == 1800


# --- провайдеры: разбор потоков ---------------------------------------------------


def _sse(events: list[dict | str]) -> bytes:
    lines = []
    for ev in events:
        payload = ev if isinstance(ev, str) else json.dumps(ev, ensure_ascii=False)
        lines.append(f"data: {payload}\n\n")
    return "".join(lines).encode("utf-8")


async def test_openai_stream_assembles_text_tool_calls_and_usage():
    from providers.openai_compat import OpenAICompatProvider

    body = _sse([
        {"model": "m", "choices": [{"delta": {"reasoning_content": "думаю "}}]},
        {"choices": [{"delta": {"content": "Сейчас "}}]},
        {"choices": [{"delta": {"content": "посчитаю"}}]},
        {"choices": [{"delta": {"tool_calls": [
            {"index": 0, "id": "c1", "function": {"name": "code_exec", "arguments": "{\"co"}}]}}]},
        {"choices": [{"delta": {"tool_calls": [
            {"index": 0, "function": {"arguments": "de\": \"print(1)\"}"}}]},
            "finish_reason": "tool_calls"}]},
        {"choices": [], "usage": {"prompt_tokens": 11, "completion_tokens": 7}},
        "[DONE]",
    ])
    provider = OpenAICompatProvider("k", "https://example.test/v1")
    provider._client = httpx.AsyncClient(transport=httpx.MockTransport(
        lambda request: httpx.Response(200, content=body)))
    got: list[tuple[str, str]] = []
    result = await provider.stream_complete(
        "m", [ChatMessage("user", "привет")],
        tools=[ToolSpec("code_exec", "", {"type": "object"})],
        on_delta=lambda t, k: got.append((k, t)))
    await provider.aclose()

    assert result.text == "Сейчас посчитаю"
    assert result.tool_calls[0].name == "code_exec"
    assert result.tool_calls[0].arguments == {"code": "print(1)"}
    assert (result.usage.input_tokens, result.usage.output_tokens) == (11, 7)
    assert ("reasoning", "думаю ") in got


async def test_openai_stream_retries_without_stream_options():
    from providers.openai_compat import OpenAICompatProvider

    calls: list[dict] = []

    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content)
        calls.append(payload)
        if "stream_options" in payload:
            return httpx.Response(400, json={"error": {"message": "unknown field stream_options"}})
        return httpx.Response(200, content=_sse([
            {"choices": [{"delta": {"content": "ок"}}]}, "[DONE]"]))

    provider = OpenAICompatProvider("", "http://localhost:1/v1")
    provider._client = httpx.AsyncClient(transport=httpx.MockTransport(handler))
    result = await provider.stream_complete("m", [ChatMessage("user", "привет всем")])
    await provider.aclose()
    assert result.text == "ок"
    assert len(calls) == 2
    assert result.usage.total > 0          # расход оценён, а не ноль


async def test_anthropic_stream_assembles_blocks():
    from providers.anthropic_provider import AnthropicProvider

    body = _sse([
        {"type": "message_start", "message": {"model": "claude", "usage": {"input_tokens": 20, "output_tokens": 1}}},
        {"type": "content_block_start", "index": 0, "content_block": {"type": "text", "text": ""}},
        {"type": "content_block_delta", "index": 0, "delta": {"type": "text_delta", "text": "Ищу "}},
        {"type": "content_block_start", "index": 1,
         "content_block": {"type": "tool_use", "id": "tu1", "name": "web_search", "input": {}}},
        {"type": "content_block_delta", "index": 1,
         "delta": {"type": "input_json_delta", "partial_json": "{\"query\": \"qt"}},
        {"type": "content_block_delta", "index": 1,
         "delta": {"type": "input_json_delta", "partial_json": "\"}"}},
        {"type": "message_delta", "delta": {"stop_reason": "tool_use"}, "usage": {"output_tokens": 15}},
        {"type": "message_stop"},
    ])
    provider = AnthropicProvider("k", "https://example.test/v1")
    provider._client = httpx.AsyncClient(transport=httpx.MockTransport(
        lambda request: httpx.Response(200, content=body)))
    result = await provider.stream_complete("claude", [ChatMessage("user", "q")])
    await provider.aclose()
    assert result.text == "Ищу "
    assert result.tool_calls[0].arguments == {"query": "qt"}
    assert (result.usage.input_tokens, result.usage.output_tokens) == (20, 15)
    assert result.finish_reason == "tool_use"


async def test_gemini_stream_skips_thoughts_in_text():
    from providers.gemini_provider import GeminiProvider

    body = _sse([
        {"candidates": [{"content": {"parts": [{"text": "план", "thought": True}]}}]},
        {"candidates": [{"content": {"parts": [{"text": "Ответ"}]}, "finishReason": "STOP"}],
         "usageMetadata": {"promptTokenCount": 5, "candidatesTokenCount": 3,
                           "thoughtsTokenCount": 4}},
    ])
    provider = GeminiProvider("k", "https://example.test/v1beta")
    provider._client = httpx.AsyncClient(transport=httpx.MockTransport(
        lambda request: httpx.Response(200, content=body)))
    kinds: list[str] = []
    result = await provider.stream_complete("g", [ChatMessage("user", "q")],
                                            on_delta=lambda t, k: kinds.append(k))
    await provider.aclose()
    assert result.text == "Ответ"
    assert kinds == ["reasoning", "text"]
    assert result.usage.output_tokens == 7
````

### `tests/test_audit_fixes.py`

*253 строк*

````python
"""Регрессионные тесты на ошибки, найденные при полном проходе по коду.

Как и в ``test_core_fixes.py``, каждый тест назван по ошибке: если она
вернётся, по названию упавшего теста сразу понятно, что сломалось.
"""

from __future__ import annotations

import asyncio

from core.budget import BudgetGuard
from core.events import EventBus, EventType
from core.export.bundle import ExportOptions, ResultBundle, detect_format
from core.export.exporters import export_docx
from core.hitl import Decision
from core.orchestrator import Orchestrator
from core.supervisor.checklist import parse_verdict
from providers.base import ChatMessage, LLMProvider, ProviderError, ToolCall, ToolSpec
from providers.gemini_provider import GeminiProvider
from providers.openai_compat import OpenAICompatProvider
from storage.models import Subtask, Task, Workspace
from storage.repositories import Repos, UserRepo
from tests.fakes import SupervisorProvider, Worker, build_project, drive, patch_supervisor


#: символы, которые миграция версии 2 заменяет в сохранённых промптах
EM, EN = chr(0x2014), chr(0x2013)


def _events(bus: EventBus, *types: EventType) -> list:
    seen: list = []
    bus.subscribe(lambda e: seen.append(e) if e.type in types else None)
    return seen


# --- хранилище ------------------------------------------------------------------


def test_change_password_keeps_search_api_key():
    repos, workspace, _, _, _ = build_project()
    ws = repos.workspaces.get(workspace.id)
    repos.workspaces.update(workspace.id, settings={
        **ws.settings, "search_api_key": repos.secrets.seal("tvly-secret")})

    assert repos.users.change_password(repos.session, "password123", "newpassword456")

    token = repos.workspaces.get(workspace.id).settings["search_api_key"]
    assert repos.secrets.open(token) == "tvly-secret"


def test_migration_normalizes_saved_prompts(tmp_path):
    from storage.db import Database

    path = tmp_path / "old.db"
    db = Database(path)
    session = UserRepo(db).create("prompt-owner", "password123")
    repos = Repos(db, session)
    ws = repos.workspaces.create(session.user_id, "W", "", {})
    agent = repos.agents.create(ws.id, "A", "analyst", f"Ты {EM} аналитик, 2{EN}5 фактов",
                                None, "openai", "m", {})
    db.conn.execute("PRAGMA user_version = 1")        # база прежней версии
    db.conn.commit()
    db.close()

    reopened = Database(path)
    prompt = reopened.query_one("SELECT system_prompt FROM agents WHERE id = ?",
                                (agent.id,))["system_prompt"]
    assert prompt == "Ты - аналитик, 2-5 фактов"
    reopened.close()


def test_failed_statement_does_not_leave_open_transaction():
    repos, *_ = build_project()
    try:
        repos.db.execute("INSERT INTO agents(workspace_id, name, created_at) VALUES (?,?,?)",
                         (999_999, "призрак", "2026-01-01"))
    except Exception:  # noqa: BLE001 - нарушение внешнего ключа ожидаемо
        pass
    with repos.db.transaction() as conn:          # раньше: «transaction within a transaction»
        conn.execute("SELECT 1")


# --- супервайзер ------------------------------------------------------------------


def test_verdict_without_field_is_not_accepted():
    for raw in ("{}", '{"notes": "что-то"}', "[]", '{"verdict": "maybe"}'):
        verdict = parse_verdict(raw)
        assert verdict.verdict == "rework", raw
        assert not verdict.accepted
        assert verdict.notes


async def test_accepted_result_closes_supervisor_notes():
    repos, workspace, task, _, _ = build_project(subtask_count=1)
    patch_supervisor(SupervisorProvider(verdicts=[
        '{"verdict": "ok", "notes": "", "issues": '
        '[{"kind": "factual_error", "severity": "low", "description": "мелочь"}]}']))
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: Worker()
    await drive(orch, workspace.id, task.id)

    statuses = {i.status for i in repos.incidents.list(workspace.id)}
    assert statuses == {"resolved"}          # не висит «ждёт решения» на дашборде


# --- оркестратор и исполнитель ------------------------------------------------------


class _Broken(LLMProvider):
    async def complete(self, model, messages, **kwargs):
        raise ProviderError("500: модель недоступна", 500)

    async def list_models(self):
        return []


async def test_failed_subtask_is_reported_once():
    repos, workspace, task, _, _ = build_project(subtask_count=1)
    patch_supervisor(SupervisorProvider())
    bus = EventBus()
    failed = _events(bus, EventType.SUBTASK_FAILED)
    orch = Orchestrator(repos, bus)
    orch._provider_for = lambda agent: _Broken()
    await drive(orch, workspace.id, task.id)

    assert len(failed) == 1                  # раньше приходило два одинаковых
    assert "модель недоступна" in failed[0].message


async def test_exhausted_user_reworks_mark_subtask_as_error():
    repos, workspace, task, _, _ = build_project(
        subtask_count=1, settings={"human_in_the_loop": True, "max_rework_rounds": 0,
                                   "hitl_confidence_threshold": 0})
    rework = '{"verdict": "rework", "notes": "ещё раз", "issues": []}'
    patch_supervisor(SupervisorProvider(verdicts=[rework] * 10))
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: Worker()
    state = await drive(orch, workspace.id, task.id, fallback=Decision.REWORK)

    subtask = repos.tasks.subtasks(task.id)[0]
    assert subtask.status == "error"         # не «на доработке» навсегда
    assert state.failed == 1


async def test_dependency_on_missing_subtask_does_not_block():
    repos, workspace, task, _, _ = build_project(subtask_count=1)
    subtask = repos.tasks.subtasks(task.id)[0]
    repos.tasks.update_subtask(subtask.id, depends_on="999999")
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: Worker()
    await drive(orch, workspace.id, task.id)

    assert repos.tasks.subtasks(task.id)[0].status == "done"


async def test_agents_are_idle_after_stop():
    repos, workspace, task, agents, _ = build_project(subtask_count=2)
    patch_supervisor(SupervisorProvider())
    orch = Orchestrator(repos, EventBus())
    orch._provider_for = lambda agent: Worker(delay=0.5)
    run = asyncio.ensure_future(orch.run_task(workspace.id, task.id))
    await asyncio.sleep(0.2)
    orch.stop()
    await run

    assert {repos.agents.get(a.id).status for a in agents} == {"idle"}


# --- бюджет -------------------------------------------------------------------------


def test_budget_limit_change_applies_to_running_guard():
    repos, workspace, task, agents, _ = build_project()
    guard = BudgetGuard(repos, EventBus(), workspace.id, task.id)
    guard.add(500, 0.0, agents[0].id)
    assert guard.blocking_scope(agents[0].id) is None

    repos.budgets.upsert("agent", agents[0].id, 400, None)
    guard.reload_limits()
    blocked = guard.blocking_scope(agents[0].id)
    assert blocked is not None and blocked.scope == "agent"


# --- провайдеры ---------------------------------------------------------------------


def test_openai_payload_matches_api_family():
    messages = [ChatMessage("user", "привет")]
    official = OpenAICompatProvider("k")
    official.key = "openai"
    reasoning = official._payload("o4-mini", messages, 0.7, 500, None)
    assert reasoning["max_completion_tokens"] == 500
    assert "max_tokens" not in reasoning and "temperature" not in reasoning
    chat = official._payload("gpt-4o-mini", messages, 0.7, 500, None)
    assert chat["temperature"] == 0.7 and "max_tokens" not in chat

    compatible = OpenAICompatProvider("k", "https://api.groq.com/openai/v1")
    compatible.key = "groq"
    other = compatible._payload("llama-3.3-70b-versatile", messages, 0.7, 500, None)
    assert other["max_tokens"] == 500 and other["temperature"] == 0.7


def test_tool_arguments_are_always_a_dict():
    assert ToolCall.parse_args('["a", "b"]') == {"_raw": '["a", "b"]'}
    assert ToolCall.parse_args("42") == {"_raw": "42"}
    assert ToolCall.parse_args('{"path": "a.txt"}') == {"path": "a.txt"}


def test_gemini_groups_tool_responses_and_returns_signature():
    calls = [ToolCall("1", "read_file", {"path": "a"}, signature="sig-1"),
             ToolCall("2", "list_dir", {})]
    _, contents = GeminiProvider._split([
        ChatMessage("user", "задача"),
        ChatMessage("assistant", "", tool_calls=calls),
        ChatMessage("tool", "текст файла", tool_call_id="1", name="read_file"),
        ChatMessage("tool", "список", tool_call_id="2", name="list_dir"),
    ])
    assert [c["role"] for c in contents] == ["user", "model", "user"]
    assert len(contents[2]["parts"]) == 2            # оба ответа одним сообщением
    assert contents[1]["parts"][0]["thoughtSignature"] == "sig-1"


def test_gemini_schema_drops_unsupported_keys():
    spec = ToolSpec("t", "d", {"type": "object", "additionalProperties": False,
                               "properties": {"n": {"type": "integer", "default": 5}}})
    payload = GeminiProvider("k")._payload([ChatMessage("user", "x")], 0.5, 100, [spec])
    params = payload["tools"][0]["functionDeclarations"][0]["parameters"]
    assert params == {"type": "object", "properties": {"n": {"type": "integer"}}}


# --- экспорт --------------------------------------------------------------------------


def _bundle(result: str, title: str = "T", description: str = "d") -> ResultBundle:
    ws = Workspace(1, 1, "WS", "", {}, False, "", "")
    task = Task(1, 1, title, description, "done", "auto", None, "", "")
    sub = Subtask(1, 1, None, "A", "", "done", 0, "", result, 0, 0, 0, 0.0, "", "")
    return ResultBundle(workspace=ws, task=task, subtasks=[sub])


def test_docx_export_survives_terminal_output(tmp_path):
    bundle = _bundle("вывод: \x1b[31mкрасный\x1b[0m \x00 и \x07 сигнал")
    result = export_docx(bundle, ExportOptions(), tmp_path / "r.docx")
    assert result.size > 0


def test_format_detection_ignores_word_fragments():
    # «api» внутри «capital» и «app» внутри «happy» - не про код.
    fmt, _ = detect_format(_bundle("коротко", "Столица Франции",
                                   "Назови capital и один happy fact"))
    assert fmt != "zip"
````

### `tests/test_models.py`

*143 строк*

````python
"""Выбор моделей и особенности актуальных API провайдеров (сентябрь 2026).

Каждый тест закрепляет поведение, без которого модель у провайдера просто
не работает: Gemini 2.x закрыты для новых ключей, у Gemini 3 размышления
съедают лимит ответа, флагманы GPT-6 не вызывают инструменты через Chat
Completions.
"""

from __future__ import annotations

import json

import httpx
import pytest

from providers.base import ChatMessage, ProviderError, ToolSpec, is_chat_model
from providers.gemini_provider import THINKING_HEADROOM, GeminiProvider
from providers.openai_compat import OpenAICompatProvider
from providers.presets import PRESETS
from ui.bridge.c_agents import ordered_models

TOOL = ToolSpec("read_file", "читает файл", {"type": "object", "properties": {}})
MESSAGES = [ChatMessage("system", "Ты агент."), ChatMessage("user", "задача")]


def _sse(events: list[dict]) -> bytes:
    return "".join(f"data: {json.dumps(e, ensure_ascii=False)}\n\n" for e in events).encode()


def _gemini(body: bytes) -> GeminiProvider:
    provider = GeminiProvider("k", "https://example.test/v1beta")
    provider._client = httpx.AsyncClient(transport=httpx.MockTransport(
        lambda request: httpx.Response(200, content=body)))
    return provider


# --- рекомендованные модели ------------------------------------------------------


def test_gemini_suggestions_work_for_new_keys():
    suggested = PRESETS["gemini"].suggested_models
    assert suggested and suggested[0].startswith("gemini-3")
    # 2.0 отключены, 2.5 закрыты для новых ключей: предлагать их нельзя.
    assert not [m for m in suggested if m.startswith(("gemini-2", "gemini-1"))]


def test_every_provider_offers_several_models():
    for key, preset in PRESETS.items():
        if key != "custom":
            assert len(preset.suggested_models) >= 4, key


def test_recommended_models_come_first_and_junk_is_hidden():
    available = ["gemini-2.0-flash", "gemini-2.5-flash", "gemini-3.5-flash-lite",
                 "gemini-3.8-flash", "gemini-3.8-flash-tts", "gemini-embedding-001"]
    ordered = ordered_models(["gemini-3.8-flash", "gemini-3.5-flash-lite", "gemini-9"],
                             available)
    assert ordered[:2] == ["gemini-3.8-flash", "gemini-3.5-flash-lite"]
    assert "gemini-9" not in ordered                 # у ключа такой модели нет
    assert "gemini-3.8-flash-tts" not in ordered and "gemini-embedding-001" not in ordered
    assert ordered_models(["a", "b"], []) == ["a", "b"]


def test_chat_model_filter():
    assert is_chat_model("gpt-6-luna") and is_chat_model("qwen/qwen3.8-27b")
    for name in ("whisper-1", "gpt-4o-mini-tts", "text-embedding-3-large", "gpt-image-2",
                 "gemini-3.8-live", "omni-moderation-latest"):
        assert not is_chat_model(name), name


# --- Gemini ----------------------------------------------------------------------------


def test_gemini3_payload_leaves_room_for_thinking_and_keeps_temperature_default():
    payload = GeminiProvider("k")._payload(MESSAGES, 0.2, 2048, None, "gemini-3.8-flash")
    config = payload["generationConfig"]
    assert config["maxOutputTokens"] == 2048 + THINKING_HEADROOM
    assert config["thinkingConfig"] == {"includeThoughts": True}
    assert "temperature" not in config               # Google: ниже 1.0 зацикливается


def test_gemini_older_model_keeps_plain_config():
    config = GeminiProvider("k")._payload(MESSAGES, 0.2, 2048, None,
                                          "gemini-2.0-flash")["generationConfig"]
    assert config == {"temperature": 0.2, "maxOutputTokens": 2048}


async def test_gemini_empty_answer_explains_token_limit():
    provider = _gemini(_sse([
        {"candidates": [{"content": {"parts": [{"text": "думаю", "thought": True}]}}]},
        {"candidates": [{"content": {"parts": []}, "finishReason": "MAX_TOKENS"}]},
    ]))
    with pytest.raises(ProviderError, match="лимит токенов"):
        await provider.stream_complete("gemini-3.8-flash", MESSAGES)
    await provider.aclose()


async def test_gemini_blocked_prompt_is_reported():
    provider = _gemini(_sse([{"promptFeedback": {"blockReason": "SAFETY"}}]))
    with pytest.raises(ProviderError, match="SAFETY"):
        await provider.stream_complete("gemini-3.8-flash", MESSAGES)
    await provider.aclose()


async def test_gemini_model_list_hides_non_chat_models():
    body = json.dumps({"models": [
        {"name": "models/gemini-3.8-flash", "supportedGenerationMethods": ["generateContent"]},
        {"name": "models/gemini-3.8-flash-tts", "supportedGenerationMethods": ["generateContent"]},
        {"name": "models/gemini-embedding-001", "supportedGenerationMethods": ["embedContent"]},
    ]}).encode()
    provider = _gemini(body)
    assert await provider.list_models() == ["gemini-3.8-flash"]
    await provider.aclose()


# --- OpenAI ------------------------------------------------------------------------------


def _openai() -> OpenAICompatProvider:
    provider = OpenAICompatProvider("k")
    provider.key = "openai"
    return provider


def test_gpt6_luna_calls_tools_without_reasoning():
    payload = _openai()._payload("gpt-6-luna", MESSAGES, 0.7, 1000, [TOOL])
    assert payload["reasoning_effort"] == "none"
    assert "temperature" not in payload and payload["max_completion_tokens"] == 1000
    plain = _openai()._payload("gpt-6-luna", MESSAGES, 0.7, 1000, None)
    assert "reasoning_effort" not in plain           # без инструментов рассуждает как обычно


def test_gpt6_flagship_with_tools_gets_a_clear_error():
    with pytest.raises(ProviderError, match="Responses API"):
        _openai()._payload("gpt-6-astra", MESSAGES, 0.7, 1000, [TOOL])
    assert _openai()._payload("gpt-6-astra", MESSAGES, 0.7, 1000, None)["model"] == "gpt-6-astra"


def test_reasoning_models_are_recognised_by_version():
    for model in ("gpt-5.4-mini", "gpt-6-sol", "o3"):
        assert "temperature" not in _openai()._payload(model, MESSAGES, 0.7, 100, None), model
    for model in ("gpt-4.1", "gpt-4o-mini"):
        assert _openai()._payload(model, MESSAGES, 0.7, 100, None)["temperature"] == 0.7, model
````

### `tests/qml_controls_check.py`

*98 строк*

````python
"""Переключатели Ao (Toggle, Chip) держатся за данные и после щелчка.

Отдельный процесс, как и тур: Qt нужен собственный цикл событий. Код
возврата 0 - всё в порядке, иначе в stdout описание расхождения.

Ошибка, которую ловит проверка: checkable-кнопка сама переключает
``checked``, и если щелчок не изменил данные (сохранение не прошло, щелчок
по уже выбранной роли агента), она показывала состояние, которого нет.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

QML = b"""
import QtQuick
import Ao

Item {
    id: root
    property bool store: false
    property bool saves: false
    Toggle {
        objectName: "toggle"
        isOn: root.store
        onToggled: if (root.saves) root.store = checked
    }
    Chip {
        objectName: "chip"
        isOn: root.store
        onClicked: if (root.saves) root.store = checked
    }
}
"""


def main() -> int:
    from PySide6.QtCore import QUrl
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQml import QQmlComponent, QQmlEngine
    from PySide6.QtQuickControls2 import QQuickStyle

    from ui.app import QML_DIR, ensure_qt_dll_path

    ensure_qt_dll_path()
    QQuickStyle.setStyle("Basic")
    app = QGuiApplication(sys.argv)
    engine = QQmlEngine()
    engine.addImportPath(str(QML_DIR))
    component = QQmlComponent(engine)
    component.setData(QML, QUrl.fromLocalFile(str(ROOT / "tests" / "controls.qml")))
    root = component.create()
    if root is None:
        print("QML не загрузился:", [e.toString() for e in component.errors()])
        return 1

    def settle() -> None:
        for _ in range(5):
            app.processEvents()

    problems: list[str] = []
    for name in ("toggle", "chip"):
        control = root.findChild(object, name)

        def expect(state: bool, when: str) -> None:
            settle()
            if bool(control.property("checked")) != state:
                problems.append(f"{name}: {when}: checked={control.property('checked')}, "
                                f"ожидалось {state}")

        root.setProperty("saves", False)
        root.setProperty("store", False)
        control.click()
        expect(False, "владелец не сохранил щелчок - показываем сохранённое")
        root.setProperty("store", True)
        expect(True, "данные изменились извне - переключатель следует за ними")

        root.setProperty("saves", True)
        control.click()
        expect(False, "щелчок сохранён владельцем")
        root.setProperty("store", True)
        expect(True, "после щелчка привязка к данным не потеряна")

    if problems:
        print("\n".join(problems))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
````

### `tests/test_ui.py`

*73 строк*

````python
"""Интерфейс на Qt Quick: загрузка всех экранов и живой прогон без сети.

Тур запускается отдельным процессом: у Qt и qasync свой цикл событий, и
смешивать его с циклом pytest-asyncio в одном процессе ненадёжно.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_bridge_properties_notify_qml():
    """Каждое свойство моста либо константное, либо с сигналом изменения.

    Иначе биндинги QML молча перестают обновляться (так было с сигналом,
    унаследованным от базового класса).
    """
    from ui.bridge import (backend, c_agents, c_budget, c_dashboard, c_export, c_keys,
                           c_prefs, c_run, c_supervisor, c_task, c_workspaces, i18n_bridge,
                           listmodel)

    modules = (c_agents, c_budget, c_dashboard, c_export, c_keys, c_prefs, c_run,
               c_supervisor, c_task, c_workspaces)
    classes = [backend.Backend, i18n_bridge.I18n, listmodel.DictListModel] + [
        getattr(m, n) for m in modules for n in dir(m)
        if n.endswith("Controller") and n != "Controller"]
    silent = []
    for cls in classes:
        mo = cls.staticMetaObject
        for i in range(mo.propertyOffset(), mo.propertyCount()):
            prop = mo.property(i)
            if not prop.hasNotifySignal() and not prop.isConstant():
                silent.append(f"{cls.__name__}.{prop.name()}")
    assert not silent, silent


def test_translation_keys_exist_in_both_languages():
    import re

    from app import i18n

    used = set()
    for f in (ROOT / "ui" / "qml").rglob("*.qml"):
        used |= set(re.findall(r'i18n\.t\["([^"]+)"\]', f.read_text("utf-8")))
    missing_ru = sorted(k for k in used if k not in i18n.RU)
    missing_en = sorted(k for k in i18n.RU if k not in i18n.EN)
    assert not missing_ru, missing_ru
    assert not missing_en, missing_en


def test_toggles_show_saved_state_after_click():
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen")
    proc = subprocess.run([sys.executable, str(ROOT / "tests" / "qml_controls_check.py")],
                          cwd=ROOT, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=120)
    assert proc.returncode == 0, proc.stdout[-3000:] + proc.stderr[-3000:]


def test_ui_tour_runs_without_qml_errors(tmp_path):
    env = dict(os.environ, QT_QPA_PLATFORM="offscreen",
               AGENTFORGE_HOME=str(tmp_path / "data"))
    proc = subprocess.run([sys.executable, str(ROOT / "tests" / "ui_tour.py"),
                           str(tmp_path / "shots")],
                          cwd=ROOT, env=env, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=300)
    assert proc.returncode == 0, proc.stdout[-3000:] + proc.stderr[-3000:]
    shots = sorted(p.name for p in (tmp_path / "shots").glob("*.png"))
    assert len(shots) >= 15, shots
````

### `tests/ui_tour.py`

*281 строк*

````python
"""Сквозной прогон интерфейса без реальной сети: вход, данные, все экраны.

Используется двумя способами:

* ``pytest tests/test_ui.py`` - проверяет, что каждый экран открывается
  без ошибок QML и что живой прогон с фейковыми агентами доходит до конца;
* ``python tests/ui_tour.py [каталог]`` - то же самое, плюс сохраняет
  скриншоты всех экранов, чтобы их можно было посмотреть глазами.

Окно рисуется без экрана (``QT_QPA_PLATFORM=offscreen``), модели заменены
фейковым провайдером со стримингом, поэтому ни токены, ни сеть не тратятся.
"""

from __future__ import annotations

import asyncio
import os
import sys
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
if "AGENTFORGE_HOME" not in os.environ:
    os.environ["AGENTFORGE_HOME"] = tempfile.mkdtemp(prefix="aiorc_ui_")

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PAGES = ["dashboard", "workspaces", "agents", "task", "run", "supervisor",
         "keys", "budget", "export", "settings"]


class StreamingWorker:
    """Фабрика фейковых провайдеров, которые «печатают» ответ по кусочкам."""

    @staticmethod
    def make(name: str, confidence: str = "0.85", delay: float = 0.01):
        from providers.base import CompletionResult, LLMProvider, ToolCall, Usage

        class Provider(LLMProvider):
            def __init__(self) -> None:
                super().__init__()
                self.calls = 0

            async def list_models(self):
                return ["demo-model"]

            async def aclose(self):
                return None

            async def complete(self, model, messages, *, temperature=0.7, max_tokens=2048, tools=None):
                return await self.stream_complete(model, messages, tools=tools)

            async def stream_complete(self, model, messages, *, temperature=0.7, max_tokens=2048,
                                      tools=None, on_delta=None):
                self.calls += 1
                if self.calls == 1 and tools:
                    thought = f"{name}: сначала соберу данные по теме, затем проверю цифры.\n"
                    for part in thought.split(" "):
                        if on_delta:
                            on_delta(part + " ", "reasoning")
                        await asyncio.sleep(delay)
                    return CompletionResult(
                        text="Проверю расчёт в песочнице.",
                        tool_calls=[ToolCall("c1", "code_exec", {"code": "print(21 * 2)"})],
                        usage=Usage(420, 60))
                text = (f"Итоги работы {name}. Сравнил три источника, расхождений в ключевых "
                        f"цифрах нет; оценка рынка подтверждена расчётом.\n"
                        f"CONFIDENCE: {confidence}\nRESULT:\nКраткий вывод {name}: рынок растёт "
                        f"на 18% в год, основные риски связаны с регулированием.")
                for i in range(0, len(text), 9):
                    if on_delta:
                        on_delta(text[i:i + 9], "text")
                    await asyncio.sleep(delay)
                return CompletionResult(text=text, usage=Usage(900, 180))

        return Provider()


class Tour:
    """Проходит интерфейс и складывает сообщения QML и скриншоты."""

    def __init__(self, shots_dir: Path | None = None) -> None:
        import qasync
        from PySide6.QtWidgets import QApplication

        from app.config import AppSettings
        from app.i18n import set_language

        self.shots_dir = shots_dir
        set_language("ru")
        self.qapp = QApplication.instance() or QApplication(sys.argv)
        self.loop = qasync.QEventLoop(self.qapp)
        asyncio.set_event_loop(self.loop)
        from ui.app import QML_MESSAGES, UiApp

        self.messages = QML_MESSAGES
        self.ui = UiApp(AppSettings())
        self.window = self.ui.window
        self.window.setProperty("width", 1480)
        self.window.setProperty("height", 940)
        self.backend = self.ui.backend

    # -- утилиты --------------------------------------------------------------
    async def wait(self, seconds: float) -> None:
        await asyncio.sleep(seconds)

    def play(self, coro):
        """Весь сценарий идёт внутри одного работающего цикла - как в приложении.

        Если прерывать цикл между шагами, Qt продолжает обрабатывать события
        (например, при снимке окна), и корутины агентов просыпаются вне цикла.
        """
        return self.loop.run_until_complete(coro)

    def shot(self, name: str) -> None:
        if self.shots_dir is None:
            return
        self.shots_dir.mkdir(parents=True, exist_ok=True)
        self.window.grabWindow().save(str(self.shots_dir / f"{name}.png"))

    def errors(self) -> list[str]:
        # Сообщение Qt о системном каталоге шрифтов к интерфейсу не относится:
        # приложение приносит свои шрифты.
        return [m for level, m in self.messages
                if level in ("warning", "error") and "font directory" not in m]

    def shell(self):
        from PySide6.QtCore import QObject

        for obj in self.window.findChildren(QObject):
            if obj.property("pageFiles") is not None:
                return obj
        return None

    def mark(self, name: str) -> None:
        self.messages.append(("mark", name))

    def go(self, page: str) -> None:
        self.mark("go " + page)
        shell = self.shell()
        assert shell is not None, "оболочка приложения не найдена"
        shell.setProperty("page", page)
        assert shell.property("page") == page

    # -- сценарий ------------------------------------------------------------------
    async def login(self) -> None:
        self.shot("00_signup")
        done: list[tuple[bool, str]] = []
        self.backend.authFinished.connect(lambda ok, err: done.append((ok, err)))
        self.backend.signUp("demo", "demo-password-1", "demo-password-1")
        for _ in range(100):
            if done:
                break
            await self.wait(0.05)
        assert done and done[0][0], f"вход не удался: {done}"
        await self.wait(0.8)

    async def seed(self) -> None:
        """Проект с агентами, задачей и подзадачами - как у живого пользователя."""
        self.mark("seed")
        b = self.backend
        b.workspaces.create("Анализ рынка EdTech", "Исследование рынка онлайн-обучения для отчёта инвестору")
        b.workspaces.create("Бот поддержки", "Прототип ассистента первой линии")
        repos = b.repos
        ws_id = b.workspace_id
        # Ключ без сети: Ollama не требует секрета.
        key = repos.keys.create("Локальный Ollama", "ollama", "", "http://localhost:11434/v1")
        roles = [("Аналитик", "analyst"), ("Исследователь", "researcher"), ("Критик", "critic")]
        agents = []
        for name, role in roles:
            agents.append(repos.agents.create(
                ws_id, name, role, f"Ты - {name.lower()}.", key.id, "ollama", "qwen2.5:7b-instruct",
                {"temperature": 0.4, "max_tokens": 1024, "tools": ["web_search", "code_exec"]}))
        sup = repos.agents.create(ws_id, "Супервайзер", "supervisor", "Проверяй отчёты.", key.id,
                                  "ollama", "qwen2.5:14b-instruct", {}, is_supervisor=True)
        ws = repos.workspaces.get(ws_id)
        repos.workspaces.update(ws_id, settings={**ws.settings, "supervisor_agent_id": sup.id,
                                                 "summary_interval_minutes": 0,
                                                 "human_in_the_loop": True,
                                                 "hitl_confidence_threshold": 0.6})
        task = repos.tasks.create(ws_id, "Рынок EdTech в 2026 году",
                                  "Оценить объём рынка онлайн-обучения, ключевых игроков и риски. "
                                  "Результат: короткий отчёт для инвестора.", "docx", 60000)
        s1 = repos.tasks.add_subtask(task.id, "Собрать данные об объёме рынка", "Источники за 2024-2026", agents[1].id)
        s2 = repos.tasks.add_subtask(task.id, "Проанализировать ключевых игроков", "", agents[0].id)
        s3 = repos.tasks.add_subtask(task.id, "Оценить риски и ограничения", "", agents[2].id)
        s4 = repos.tasks.add_subtask(task.id, "Свести выводы для инвестора", "", agents[0].id)
        repos.tasks.update_subtask(s2.id, depends_on=str(s1.id))
        repos.tasks.update_subtask(s3.id, depends_on=str(s1.id))
        repos.tasks.update_subtask(s4.id, depends_on=f"{s2.id},{s3.id}")
        repos.budgets.upsert("workspace", ws_id, 500000, 5.0, 0.8)
        for c in b._controllers.values():
            c.refresh()
        await self.wait(0.3)

    async def run_with_fakes(self, decide: bool = True) -> None:
        """Живой прогон с фейковыми агентами: стриминг, граф, вопрос человеку."""
        from core.hitl import Decision
        from tests.fakes import SupervisorProvider, patch_supervisor

        orch = self.backend.orchestrator
        providers = {}
        low = {"Критик"}

        def provider_for(agent):
            if agent.id not in providers:
                providers[agent.id] = StreamingWorker.make(
                    agent.name, confidence="0.4" if agent.name in low else "0.86")
            return providers[agent.id]

        orch._provider_for = provider_for
        self.mark("run")
        patch_supervisor(SupervisorProvider())
        self.go("run")
        await self.wait(0.4)
        self.backend.run.start()
        shot_taken = False
        for _ in range(400):
            await self.wait(0.05)
            gate = orch.gate
            if gate and gate.pending():
                if not shot_taken:
                    await self.wait(0.5)
                    self.shot("05b_run_decision")
                    shot_taken = True
                if decide:
                    req = gate.pending()[0]
                    self.backend.run.decide(req.id, Decision.APPROVE.value, "Проверено вручную")
            if not orch.state.running and orch.state.task_id is not None and _ > 5:
                break
        await self.wait(0.6)


async def scenario(tour: "Tour") -> None:
    await tour.login()
    await tour.seed()
    for i, page in enumerate(PAGES):
        tour.go(page)
        await tour.wait(1.0)
        tour.shot(f"{i + 1:02d}_{page}")
    await tour.run_with_fakes()
    tour.go("run")
    await tour.wait(0.8)
    tour.shot("20_run_after")
    for page in ("dashboard", "supervisor", "task", "export"):
        tour.go(page)
        await tour.wait(1.0)
        tour.shot(f"21_{page}_after")


def main(shots_dir: str) -> int:
    tour = Tour(Path(shots_dir))
    tour.play(scenario(tour))
    tour.mark("end")
    for level, m in tour.messages:
        if level == "mark":
            print("--", m)
        elif level in ("warning", "error") and "font directory" not in m:
            print("   ", m[:160])
    errors = tour.errors()
    orch = tour.backend.orchestrator
    task = tour.backend.repos.tasks.current(tour.backend.workspace_id)
    statuses = [s.status for s in tour.backend.repos.tasks.subtasks(task.id)]
    print(f"Статусы подзадач после прогона: {statuses}")
    if statuses != ["done"] * len(statuses) or orch.state.running:
        errors.append(f"прогон не завершился успешно: {statuses}")
    print(f"Скриншоты: {shots_dir}")
    print(f"Сообщений QML с предупреждениями: {len(errors)}")
    for e in errors[:60]:
        print("  ", e)
    tour.ui.dispose()
    # Закрытие цикла останавливает поток исполнителя qasync; без этого
    # процесс падает при выходе с «QThread: Destroyed while thread is running».
    tour.loop.close()
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else str(ROOT / "shots")))
````

### `pytest.ini`

*5 строк*

````ini
[pytest]
testpaths = tests
python_files = test_*.py
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
````


## Сборка и запуск

### `requirements.txt`

*25 строк*

````text
# ============================================================================
#  Agent Forge - зависимости
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

### `requirements-dev.txt`

*6 строк*

````text
# Зависимости для разработки и тестов (приложению не нужны)
# Установка:  pip install -r requirements-dev.txt
-r requirements.txt
pytest>=8.0
pytest-asyncio>=0.24
pyflakes>=3.0
````

### `run.sh`

*30 строк*

````bash
#!/usr/bin/env bash
# Запуск Agent Forge на Linux и macOS.
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
REM  Agent Forge - launcher for Windows
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
    echo  See the log: %%APPDATA%%\agent-forge\logs\app.log
    pause
)
````

### `.gitignore`

*229 строк*

````text
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[codz]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#   Usually these files are written by a python script from a template
#   before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py.cover
.hypothesis/
.pytest_cache/
cover/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
.pybuilder/
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
#   For a library or package, you might want to ignore these files since the code is
#   intended to run in multiple environments; otherwise, check them in:
# .python-version

# pipenv
#   According to pypa/pipenv#598, it is recommended to include Pipfile.lock in version control.
#   However, in case of collaboration, if having platform-specific dependencies or dependencies
#   having no cross-platform support, pipenv may install dependencies that don't work, or not
#   install all needed dependencies.
# Pipfile.lock

# UV
#   Similar to Pipfile.lock, it is generally recommended to include uv.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
# uv.lock

# poetry
#   Similar to Pipfile.lock, it is generally recommended to include poetry.lock in version control.
#   This is especially recommended for binary packages to ensure reproducibility, and is more
#   commonly ignored for libraries.
#   https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control
# poetry.lock
# poetry.toml

# pdm
#   Similar to Pipfile.lock, it is generally recommended to include pdm.lock in version control.
#   pdm recommends including project-wide configuration in pdm.toml, but excluding .pdm-python.
#   https://pdm-project.org/en/latest/usage/project/#working-with-version-control
# pdm.lock
# pdm.toml
.pdm-python
.pdm-build/

# pixi
#   Similar to Pipfile.lock, it is generally recommended to include pixi.lock in version control.
# pixi.lock
#   Pixi creates a virtual environment in the .pixi directory, just like venv module creates one
#   in the .venv directory. It is recommended not to include this directory in version control.
.pixi

# PEP 582; used by e.g. github.com/David-OConnor/pyflow and github.com/pdm-project/pdm
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# Redis
*.rdb
*.aof
*.pid

# RabbitMQ
mnesia/
rabbitmq/
rabbitmq-data/

# ActiveMQ
activemq-data/

# SageMath parsed files
*.sage.py

# Environments
.env
.envrc
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/

# pytype static type analyzer
.pytype/

# Cython debug symbols
cython_debug/

# PyCharm
#   JetBrains specific template is maintained in a separate JetBrains.gitignore that can
#   be found at https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
#   and can be added to the global gitignore or merged into this file.  For a more nuclear
#   option (not recommended) you can uncomment the following to ignore the entire idea folder.
# .idea/

# Abstra
#   Abstra is an AI-powered process automation framework.
#   Ignore directories containing user credentials, local state, and settings.
#   Learn more at https://abstra.io/docs
.abstra/

# Visual Studio Code
#   Visual Studio Code specific template is maintained in a separate VisualStudioCode.gitignore 
#   that can be found at https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
#   and can be added to the global gitignore or merged into this file. However, if you prefer, 
#   you could uncomment the following to ignore the entire vscode folder
# .vscode/
# Temporary file for partial code execution
tempCodeRunnerFile.py

# Ruff stuff:
.ruff_cache/

# PyPI configuration file
.pypirc

# Marimo
marimo/_static/
marimo/_lsp/
__marimo__/

# Streamlit
.streamlit/secrets.toml

# Agent Forge
*.db
*.db-wal
*.db-shm
logs/
exports/
.DS_Store

# скриншоты тура по интерфейсу
shots/
````



---

# Что осталось сделать

## Сделано в версии 1.1

- **Интерфейс переписан на Qt Quick**: дизайн-система `Ao`, живой фон,
  каскадные анимации, уведомления, палитра команд, выключатель анимаций.
- **Стриминг рассуждений агентов** во всех трёх семействах провайдеров
  (OpenAI-совместимые, Anthropic, Gemini), с вызовами инструментов и
  расходом токенов; при отказе сервера от стриминга вызов повторяется обычным.
- **Исправления ядра** (каждое закреплено тестом в `tests/test_core_fixes.py`):
  учёт расходов супервайзера в лимитах, порядок «лок агента, потом слот»,
  освобождение слота на время вопроса человеку, строгий режим для
  непроверенных результатов, вопрос о продлении бюджета, различение упавшей
  зависимости и цикла, последние сообщения в истории агента, атомарная смена
  пароля, итог при исчерпании шагов, дерево процессов в песочнице.
- **Проект переименован** из AI Orchestrator в Agent Forge; старый каталог
  данных подхватывается автоматически.

## Сделано в версии 1.1.1

Полный проход по коду; каждое исправление закреплено тестом в
`tests/test_audit_fixes.py` или `tests/qml_controls_check.py`.

- **Ядро**: подзадача, у которой кончились круги доработки, получает статус
  ошибки, а не висит «на доработке»; зависимость на удалённую подзадачу не
  блокирует прогон; принятый результат закрывает замечания супервайзера;
  агенты после остановки возвращаются в статус «свободен»; ошибка подзадачи
  приходит одним событием, а не двумя; пустой последний ответ модели не
  засчитывается как результат.
- **Супервайзер**: ответ без поля verdict больше не считается «принято»;
  в контекст проверки идут только принятые результаты; сбой финального
  разбора не роняет прогон.
- **Провайдеры**: для OpenAI `max_completion_tokens` и без температуры у
  моделей o1/o3/o4/gpt-5; Gemini получает ответы нескольких инструментов
  одним сообщением, подпись вызова и схему без неподдерживаемых ключей.
- **Данные**: смена пароля перешифровывает и ключ поискового API; упавшая
  команда SQLite не оставляет открытую транзакцию; лимит, изменённый во
  время прогона, действует сразу.
- **Экспорт**: DOCX не падает на цветном выводе терминала; решения и время
  в документе относятся к текущей задаче и показаны по местному времени;
  экспорт идёт в фоне и берёт свежие данные.
- **Интерфейс**: переключатели показывают сохранённое состояние после
  щелчка; во время прогона нельзя удалить агента или подзадачу, на которой
  он работает; ползунки применяются и с клавиатуры.

## Функциональные доработки

**Фильтр графиков по прогонам.** Дашборд показывает всю историю воркспейса
без разделения по запускам. В `usage_log` нет идентификатора прогона -
его нужно добавить и прокинуть через `BudgetRepo.log_call`.

**Граф зависимостей от планировщика.** ИИ-планировщик пока не расставляет
`depends_on`: зависимости задаются вручную в редакторе подзадачи. Следующая
волна стартует после завершения всей текущей волны; запуск по готовности
зависимостей сократит простой.

**Суммаризация длинной истории агента.** Сейчас история обрезается по
лимиту сообщений. Для длинных задач нужна сворачивающая суммаризация при
приближении к контекстному окну модели.

**Инструменты через MCP и RAG по документам проекта** - в плане курса.

**Шаблоны воркспейсов.** Готовые наборы «аналитик + разработчик +
тестировщик» с настроенными промптами, чтобы не собирать команду заново
под каждый проект.

**Повторный запуск подзадач** уже есть (кнопка на карточке подзадачи);
следующий шаг - перезапуск одной подзадачи без прогона всей задачи.

## Технический долг

**Таблица цен устаревает.** `providers/pricing.json` заполнен вручную
и требует сверки с прайс-листами. Стоит добавить дату последнего обновления
и предупреждение в интерфейсе, если она старше нескольких месяцев.

**Защита `fetch_url` от обращений в локальную сеть** и фильтр prompt
injection для содержимого страниц - в плане курса (зона платформы).

**`TokenBudget` в `core/agents/runner.py`** остался как совместимая обёртка
после появления `BudgetGuard`. Используется только в тестах - можно убрать,
когда в нём отпадёт нужда.

**Обработка ошибок провайдеров** сводится к тексту исключения. Полезно
различать исчерпание квоты, неверный ключ и временную недоступность:
на первое стоит останавливать агента, на третье - повторять с задержкой.

**Ретраи при сетевых сбоях** не реализованы вовсе. Одна оборвавшаяся
HTTP-сессия роняет подзадачу.

## Известные ограничения по замыслу

Это не баги, а осознанные решения - менять их стоит только вместе с
пониманием последствий:

- Пароль профиля невосстановим: механизма «забыли пароль» нет, иначе
  шифрование ключей теряло бы смысл.
- Режим `subprocess` в песочнице ограничивает ресурсы и окружение, но не
  изолирует файловую систему. Для строгой изоляции нужен Docker.
- Супервайзер - самая дорогая часть системы по токенам: на тестовом прогоне
  из трёх подзадач он израсходовал около двух третей бюджета. Это следствие
  того, что он читает каждый отчёт.
