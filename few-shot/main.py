from bot import Bot

SYSTEM_PROMPT = (
    "Ты — эксперт по Python. Всегда отвечай чётко, вежливо и приводи рабочий пример кода на Python. "
    "Объясни кратко, как он работает."
)

if __name__ == "__main__":
    bot = Bot(system_prompt=SYSTEM_PROMPT)

    question = input("Введите вопрос: ")
    answer = bot.ask(question)
    print("Ответ бота:\n")
    print(answer)