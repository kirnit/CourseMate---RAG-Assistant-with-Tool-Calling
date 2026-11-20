# CourseMate — AI Assistant for PDF Documents

**CourseMate** is a Python-based AI assistant that uses Retrieval-Augmented Generation (RAG) and LLM tool calling to answer questions about PDF documents.

Users can upload their own PDF files through a Telegram bot and ask questions about their contents. The assistant performs semantic search, retrieves relevant document fragments and uses an LLM to generate a contextual answer.

The project was developed to explore practical applications of RAG, vector embeddings, semantic retrieval and LLM agents.

## Features

- **PDF Upload** — upload PDF documents directly through Telegram.
- **Document Processing** — extract text and split it into overlapping chunks.
- **Semantic Search** — retrieve relevant fragments using multilingual embeddings and cosine similarity.
- **Agent with Tool Calling** — an LLM agent can invoke the `search_documents` tool.
- **Document-Based Answers** — generate responses using retrieved PDF context.
- **Source Metadata** — retrieved fragments contain document names and page numbers.
- **Separate Chat Sessions** — each Telegram chat has its own active document.
- **CLI Interface** — interact with CourseMate through the terminal.

## Architecture

### Document Processing

```text
PDF Document
     |
     v
Text Extraction (PyMuPDF)
     |
     v
Text Chunking
     |
     v
Multilingual Embeddings
     |
     v
Vector Representations
```

### Question Answering

```text
User Question
     |
     v
MiniAgent (LLM)
     |
     v
Tool Calling: search_documents
     |
     v
Semantic Retriever
     |
     v
Relevant PDF Chunks
     |
     v
LLM Response
     |
     v
Telegram / CLI
```

The project also includes a standard RAG pipeline for direct retrieval and answer generation without agent-based tool selection.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| PyMuPDF | PDF text extraction |
| SentenceTransformers | Text embeddings |
| paraphrase-multilingual-MiniLM-L12-v2 | Multilingual embedding model |
| NumPy | Vector operations and similarity search |
| OpenRouter API | Access to language models |
| OpenAI Python SDK | OpenAI-compatible API integration |
| python-telegram-bot | Telegram bot integration |

## Project Structure

```text
CourseMate/
├── app/
│   ├── agent.py
│   ├── llm_client.py
│   └── tools.py
├── rag/
│   ├── pdf_loader.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── retriever.py
│   ├── generator.py
│   └── pipeline.py
├── data/
│   └── documents/
├── bot.py
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/CourseMate.git
cd CourseMate
```

**2. Create a virtual environment**

```bash
python -m venv .venv
```

Activate it:

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Configure environment variables**

Create a `.env` file based on `.env.example`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openrouter/free
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Never commit real API keys or Telegram tokens.

## Usage

### Telegram Bot

Start the bot:

```bash
python bot.py
```

In Telegram:

1. Open your bot and send `/start`.
2. Upload a PDF document.
3. Wait for the document to be processed.
4. Ask a question about its contents.
5. Upload another PDF to switch the active document.

Example:

**User:** What font size is required for the coursework?

**Assistant:** The document specifies Times New Roman, 14 pt, with 1.5 line spacing.

The answer above is an illustrative example, not a guaranteed output.

### Command-Line Interface

Place a PDF in `data/documents/` and configure the document path in `main.py`.

Run:

```bash
python main.py
```

Enter questions in the terminal. Type `exit` to close the application.

## Limitations

- Only PDFs with extractable text are supported. OCR is not implemented.
- Semantic retrieval may return irrelevant document fragments.
- LLM responses are not guaranteed to be factually correct or fully grounded.
- Source metadata is available during retrieval, but generated citations require additional validation.
- Free OpenRouter models have request limits and may vary between calls.
- Telegram sessions are stored in memory and are lost when the application restarts.
- Uploaded files are stored locally; production deployment requires stronger file management and security controls.
- The bot currently supports one active PDF per chat.

## Future Improvements

- Hybrid search (BM25 + dense retrieval)
- Reranking
- Answer grounding and citation verification
- Persistent vector database
- Support for multiple documents per chat
- OCR for scanned PDFs
- Docker and cloud deployment

---

# CourseMate — ИИ-помощник для работы с PDF

**CourseMate** — интеллектуальный помощник на Python, использующий Retrieval-Augmented Generation (RAG) и вызов инструментов языковой моделью (Tool Calling) для ответов на вопросы по PDF-документам.

Пользователь загружает собственный PDF через Telegram-бота и задаёт вопросы по его содержимому. Система выполняет семантический поиск релевантных фрагментов документа и передаёт найденный контекст языковой модели для формирования ответа.

Проект создан для практического изучения RAG-систем, векторных представлений текста, семантического поиска и LLM-агентов.

## Возможности

- **Загрузка PDF** — отправка документов через Telegram.
- **Обработка документов** — извлечение текста и разделение на пересекающиеся фрагменты.
- **Семантический поиск** — поиск релевантной информации с использованием эмбеддингов и косинусного сходства.
- **LLM-агент** — использование `MiniAgent` с инструментом `search_documents`.
- **Генерация ответов** — формирование ответов на основе найденных фрагментов PDF.
- **Источники** — сохранение названия документа и номера страницы для найденных фрагментов.
- **Отдельные сессии** — каждый Telegram-чат работает со своим документом.
- **CLI** — возможность взаимодействия через терминал.

## Архитектура

### Обработка документа

```text
PDF
 |
 v
Извлечение текста (PyMuPDF)
 |
 v
Разбиение на чанки
 |
 v
Создание эмбеддингов
 |
 v
Векторные представления
```

### Обработка вопросов

```text
Вопрос пользователя
        |
        v
   MiniAgent (LLM)
        |
        v
Вызов search_documents
        |
        v
 Семантический поиск
        |
        v
Релевантные чанки PDF
        |
        v
 Генерация ответа LLM
        |
        v
  Telegram / Терминал
```

Дополнительно реализован классический RAG-пайплайн, в котором поиск запускается непосредственно перед генерацией ответа, без выбора инструмента агентом.

## Используемые технологии

| Технология | Назначение |
|---|---|
| Python | Основная логика приложения |
| PyMuPDF | Извлечение текста из PDF |
| SentenceTransformers | Создание эмбеддингов |
| paraphrase-multilingual-MiniLM-L12-v2 | Многоязычная модель эмбеддингов |
| NumPy | Векторные операции и поиск по сходству |
| OpenRouter API | Доступ к языковым моделям |
| OpenAI Python SDK | Взаимодействие с LLM через API |
| python-telegram-bot | Интеграция с Telegram |

## Установка

**1. Клонировать репозиторий**

```bash
git clone https://github.com/YOUR_USERNAME/CourseMate.git
cd CourseMate
```

**2. Создать виртуальное окружение**

```bash
python -m venv .venv
```

Активировать его в Windows:

```bash
.venv\Scripts\activate
```

В macOS / Linux:

```bash
source .venv/bin/activate
```

**3. Установить зависимости**

```bash
pip install -r requirements.txt
```

**4. Настроить переменные окружения**

Создать файл `.env` на основе `.env.example`:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
LLM_BASE_URL=https://openrouter.ai/api/v1
LLM_MODEL=openrouter/free
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

Настоящие API-ключи и токены нельзя публиковать в GitHub.

## Запуск

### Telegram-бот

```bash
python bot.py
```

Порядок работы:

1. Открыть Telegram-бота и отправить `/start`.
2. Загрузить PDF-документ.
3. Дождаться окончания обработки документа.
4. Задать вопрос по содержимому PDF.
5. При необходимости загрузить другой документ, чтобы переключить активный контекст.

Пример:

**Пользователь:** Какой шрифт требуется для оформления курсовой работы?

**CourseMate:** В документе указаны шрифт Times New Roman, размер 14 пт и полуторный межстрочный интервал.

Это иллюстративный пример, а не гарантированный результат каждого запуска.

### Консольная версия

Поместить PDF в `data/documents/` и указать путь к нему в `main.py`.

```bash
python main.py
```

После запуска можно задавать вопросы через терминал. Для завершения работы используется команда `exit`.

## Ограничения

- Поддерживаются PDF с извлекаемым текстом; OCR пока отсутствует.
- Семантический поиск может возвращать нерелевантные фрагменты.
- Языковая модель может ошибаться или добавлять информацию, которой нет в документе.
- Метаданные источников сохраняются, но ссылки, сформированные LLM, требуют дополнительной проверки.
- Бесплатные модели OpenRouter имеют ограничения на количество запросов.
- Сессии Telegram хранятся в оперативной памяти и сбрасываются при перезапуске.
- Загруженные документы сохраняются локально; для публичного развёртывания необходимы дополнительные меры безопасности.
- В одном чате поддерживается один активный PDF.

## Планы по развитию

- Гибридный поиск (BM25 + dense retrieval)
- Реранжирование найденных фрагментов
- Проверка достоверности ответов и источников
- Постоянное хранение векторного индекса
- Поддержка нескольких PDF в одном чате
- OCR для сканированных документов
- Docker и развёртывание в облаке
