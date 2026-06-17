# Local AI Document Search (RAG)

Система интеллектуального поиска по документам с использованием локальных языковых моделей (LLM) через Ollama и технологии Retrieval-Augmented Generation (RAG).

## 📌 Описание проекта

**Local AI Document Search** — это веб-приложение, позволяющее загружать документы и задавать вопросы на естественном языке. Система ищет релевантную информацию в документах с помощью векторного поиска и генерирует ответы, используя локальную LLM.

Проект демонстрирует практическое применение современных AI-технологий:

* Retrieval-Augmented Generation (RAG)
* Локальные LLM через Ollama
* Векторные базы данных
* Embeddings
* REST API
* Интеграция ИИ в веб-приложения

---

## 🚀 Возможности

* 📄 Загрузка документов (PDF, TXT, DOCX, Markdown)
* ✂️ Автоматическое разбиение текста на чанки
* 🧠 Генерация embeddings через Ollama
* 🔍 Семантический поиск по смыслу
* 🤖 Генерация ответов с помощью LLM
* 📚 Отображение источников ответа
* 🌐 REST API на FastAPI
* 💻 Простой веб-интерфейс

---

## 🏗️ Как работает система

```text
Пользователь задаёт вопрос
            ↓
Создание embedding запроса
            ↓
Поиск похожих фрагментов в векторной БД
            ↓
Извлечение релевантных чанков
            ↓
Формирование промпта
            ↓
Отправка запроса в Ollama
            ↓
Генерация ответа
```

---

## 🛠️ Технологический стек

### Backend

* Python 3.13+
* FastAPI
* SQLAlchemy
* Alembic
* pymupdf(PDF),python-docx(docx) ИЛИ LangChain (я еще не решил)

### AI и RAG

* Ollama
* Llama 3.1 / Qwen / Mistral
* nomic-embed-text

### Векторная БД

* ChromaDB

### База данных

* PostgreSQL

### Frontend

* HTML
* CSS
* JavaScript

### Инструменты

* Docker
* Git
* uv
* ruff
---

## 📂 Структура проекта

```text
app/
├── api/
├── services/
│   ├── rag_service.py
│   ├── embedding_service.py
│   ├── ollama_service.py
│   └── document_service.py
├── models/
├── repositories/
├── schemas/
├── templates/
├── static/
└── main.py
```

---

## ⚙️ Принцип работы

### 1. Загрузка документов

Поддерживаемые форматы:

* PDF
* TXT
* DOCX
* Markdown

### 2. Обработка документов

После загрузки система:

1. Извлекает текст из документа.
2. Разбивает его на чанки.
3. Генерирует embeddings.
4. Сохраняет их в ChromaDB.

### 3. Поиск и генерация ответа

Пример вопроса:

```text
Как подключить PostgreSQL к FastAPI?
```

Система:

1. Создаёт embedding вопроса.
2. Ищет похожие фрагменты в базе.
3. Передаёт найденный контекст в LLM.
4. Генерирует ответ.

---

## 🔌 API

### Загрузка документа

```http
POST /documents/upload
```

### Получение списка документов

```http
GET /documents
```

### Запрос к AI

```http
POST /chat
```

Пример запроса:

```json
{
  "question": "Как использовать SQLAlchemy?"
}
```

Пример ответа:

```json
{
  "answer": "SQLAlchemy используется для работы с базами данных в Python...",
  "sources": [
    {
      "document": "manual.pdf",
      "chunk": 15
    }
  ]
}
```

### Удаление документа

```http
DELETE /documents/{id}
```

---

## 🚀 Установка и запуск

### Клонирование репозитория

```bash
git clone https://github.com/your_username/local-ai-document-search.git
cd local-ai-document-search
```

### Создание виртуального окружения

Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### Установка зависимостей

```bash
pip install uv
uv sync
```

### Установка моделей Ollama

```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

### Запуск приложения

```bash
uv run uvicorn app.main:app --reload
или (рекомендуется)
docker compose up --build
```

После запуска приложение будет доступно по адресу:

```text
http://localhost:8000
```

---

## 🔮 Возможности для развития

* Авторизация пользователей
* История чатов
* Поддержка нескольких пользователей
* Стриминг ответов через WebSocket
* Выбор LLM-модели
* Гибридный поиск
* Экспорт истории диалогов

---

