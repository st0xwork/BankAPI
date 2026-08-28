# BankAPI — API and UI Test Automation

## Что показывает проект

- слоистую архитектуру автотестов;
- API-клиенты и спецификации запросов и ответов;
- валидацию данных через Pydantic;
- подготовку и очистку тестовых данных через pytest-фикстуры;
- проверку состояния в PostgreSQL через SQLAlchemy;
- Page Object и Step Object для UI-тестов;
- Allure-шаги и автоматический скриншот при падении UI-теста;
- параллельный запуск через pytest-xdist;
- запуск в Docker и GitHub Actions.

## Стек

`Python` · `pytest` · `requests` · `Pydantic` · `SQLAlchemy` · `Playwright` ·
`Allure` · `Docker` · `GitHub Actions`

## Структура

```text
src/main/
├── api/
│   ├── classes/       # единая точка доступа к бизнес-шагам
│   ├── configs/       # конфигурация окружения
│   ├── db/            # SQLAlchemy-модели и CRUD
│   ├── fixtures/      # подготовка и очистка данных
│   ├── foundation/    # HTTP requesters и endpoints
│   ├── generators/    # генерация Pydantic-моделей
│   ├── models/        # модели запросов и ответов
│   ├── specs/         # request/response specifications
│   ├── steps/         # бизнес-шаги API
│   └── tests/         # API-тесты
├── ui/
│   ├── pages/         # Page Objects
│   ├── steps/         # бизнес-шаги и проверки
│   └── tests/         # UI-тесты
└── utils/             # общие константы
```

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m playwright install chromium
```

## Конфигурация API

Бэкенд банковского приложения не входит в репозиторий. Для API-тестов он должен
быть запущен отдельно.

Настройки можно передать переменными окружения:

```bash
export BACKEND_URL=http://localhost:4111/api
export DATA_BASE_URL=postgresql+psycopg2://user:password@localhost:5432/database
export ADMIN_USERNAME=admin
export ADMIN_PASSWORD=your-password
```

Либо скопировать пример локального конфига:

```bash
cp resources/urls.properties.example resources/urls.properties
```

Файл `resources/urls.properties` исключён из Git.

## Запуск тестов

Все тесты:

```bash
pytest
```

Только API:

```bash
pytest src/main/api/tests -m api
```

Только UI:

```bash
pytest src/main/ui/tests -m ui
```

Параллельный запуск:

```bash
pytest -n auto
```

Запуск с Allure:

```bash
pytest src/main/ui/tests -m ui --alluredir=allure-results
allure serve allure-results
```

Для команды `allure serve` должен быть установлен Allure CLI.

## Docker

Сборка образа:

```bash
docker build -t bank-tests .
```

API-тесты запускаются с передачей настроек окружения:

```bash
docker run --rm \
  -v "$PWD/reports:/app/reports" \
  -e BACKEND_URL=http://host.docker.internal:4111/api \
  -e DATA_BASE_URL=postgresql+psycopg2://user:password@host.docker.internal:5432/database \
  -e ADMIN_USERNAME=admin \
  -e ADMIN_PASSWORD=your-password \
  bank-tests
```

Результаты Allure сохранятся в локальной папке `reports/allure`.

UI-тесты:

```bash
docker run --rm bank-tests pytest src/main/ui/tests -m ui
```

## Наборы проверок

API-набор покрывает создание и авторизацию пользователей, счета, пополнение,
переводы, оформление и погашение кредита. UI-набор проверяет авторизацию,
каталог, сортировку, корзину и checkout.

Для каждого теста создаётся отдельное состояние. API-проверки дополнительно
сверяют результат с базой данных, а UI-тесты выполняются в изолированном
браузерном контексте.
