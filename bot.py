import os
import asyncio
import logging
import uuid
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, RateLimitError
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from rag.pipeline import RAGPipeline
from app.agent import MiniAgent


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("data/uploads")
MAX_PDF_SIZE = 10 * 1024 * 1024

sessions = {}

class MockAgent:
    def __init__(self, pipeline):
        self.pipeline = pipeline

    def run(self, question):
        results = self.pipeline.search(question, top_k=3)

        if not results:
            return "Ничего не найдено."

        return "\n\n".join(
            f"Документ: {r['document']}\n"
            f"Страница: {r['page']}\n"
            f"Фрагмент: {r['text'][:300]}"
            for r in results
        )


def register_pdf(chat_id, file_path):
    pipeline = RAGPipeline(file_path)
    agent = MiniAgent(pipeline)

    old_session = sessions.get(chat_id)

    sessions[chat_id] = {
        "agent": agent,
        "file_path": Path(file_path),
    }

    if old_session:
        old_path = old_session["file_path"]
        if old_path != Path(file_path):
            old_path.unlink(missing_ok=True)

    return len(pipeline.pages), len(pipeline.chunks)


def answer_from_session(chat_id, question):
    session = sessions.get(chat_id)

    if session is None:
        return "Сначала отправьте PDF-документ."

    return session["agent"].run(question)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я CourseMate.\n\n"
        "Отправь мне PDF, а затем задавай вопросы по нему."
    )


async def handle_pdf(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    document = update.message.document
    chat_id = update.effective_chat.id

    filename = Path(document.file_name or "document.pdf").name

    if Path(filename).suffix.lower() != ".pdf":
        await update.message.reply_text(
            "Поддерживаются только PDF-документы."
        )
        return

    if document.file_size and document.file_size > MAX_PDF_SIZE:
        await update.message.reply_text(
            "Файл слишком большой. Максимум — 10 МБ."
        )
        return

    folder = UPLOAD_DIR / str(chat_id) / uuid.uuid4().hex
    folder.mkdir(parents=True, exist_ok=True)
    file_path = folder / filename

    await update.message.reply_text(
        "PDF получен. Обрабатываю документ..."
    )

    try:
        telegram_file = await document.get_file()
        await telegram_file.download_to_drive(
            custom_path=file_path
        )

        if file_path.stat().st_size > MAX_PDF_SIZE:
            raise ValueError("PDF превышает лимит 10 МБ")

        with file_path.open("rb") as f:
            if f.read(5) != b"%PDF-":
                raise ValueError("Файл не является корректным PDF")

        pages_count, chunks_count = await asyncio.to_thread(
            register_pdf,
            chat_id,
            file_path,
        )

        await update.message.reply_text(
            f"Документ обработан!\n"
            f"Страниц с текстом: {pages_count}\n"
            f"Чанков: {chunks_count}\n\n"
            "Теперь можете задавать вопросы."
        )

    except Exception:
        logger.exception("Ошибка обработки PDF")
        file_path.unlink(missing_ok=True)
        await update.message.reply_text(
            "Не удалось обработать PDF. "
            "Проверьте, что он содержит извлекаемый текст."
        )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id
    question = update.message.text.strip()

    if not question:
        return

    if chat_id not in sessions:
        await update.message.reply_text(
            "Сначала отправьте PDF-документ."
        )
        return

    try:
        answer = await asyncio.to_thread(
            answer_from_session,
            chat_id,
            question,
        )

        text = str(answer or "Недостаточно данных для ответа.")

        for start_index in range(0, len(text), 3900):
            await update.message.reply_text(
                text[start_index:start_index + 3900]
            )

    except RateLimitError:
        await update.message.reply_text(
            "Суточный лимит LLM исчерпан. "
            "Попробуйте позже."
        )

    except APIError:
        logger.exception("Ошибка LLM API")
        await update.message.reply_text(
            "Сервис генерации ответа временно недоступен."
        )

    except Exception:
        logger.exception("Ошибка обработки вопроса")
        await update.message.reply_text(
            "Не удалось обработать вопрос."
        )


def main():
    token = os.environ["TELEGRAM_BOT_TOKEN"]

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.Document.ALL, handle_pdf)
    )
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    app.run_polling()


if __name__ == "__main__":
    main()