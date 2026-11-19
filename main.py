from rag.pipeline import RAGPipeline
from app.agent import MiniAgent
from openai import RateLimitError

def main():
    pipeline = RAGPipeline("data/documents/methodology_course.pdf")
    agent = MiniAgent(pipeline)

    while True:
        question = input("Вопрос: ").strip()
        if question.lower() == "exit": break

        if not question: continue

        try:
            response = agent.run(question)
            print(f"Ответ: {response}")
        except RateLimitError:
            print("Лимит запросов OpenRouter исчерпан. Попробуйте позже.")


if __name__ == "__main__":
    main()