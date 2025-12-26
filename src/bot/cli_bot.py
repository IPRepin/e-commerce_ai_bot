import re

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from src.bot.service import get_order_status, find_faq_answer
from src.utils.logger import logger
from config.config import settings as cfg


class CLIBot():
    def __init__(self, system_prompt: str):
        self.chat_model = ChatOpenAI(
            model=cfg.openrouter.OPENROUTER_MODEL,
            api_key=cfg.openrouter.OPENROUTER_API_KEY,
            base_url=cfg.openrouter.OPENROUTER_URL,
            temperature=0,
            request_timeout=20
        )

        # Создаём Хранилище истории
        self.conversation_history = {}

        # Создаем шаблон промпта
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{question}"),
        ])

        # Создаём цепочку
        self.chain = self.prompt | self.chat_model

        # Создаём цепочку с историей
        self.chain_with_history = RunnableWithMessageHistory(
            self.chain, # Цепочка с историей
            self.get_session_history, # метод для получения истории
            input_messages_key="question", # ключ для вопроса
            history_messages_key="history", # ключ для истории
        )

    # Метод для получения истории по session_id
    def get_session_history(self, session_id: str):
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = InMemoryChatMessageHistory()
        return self.conversation_history[session_id]

    def __call__(self, session_id):
        print(f"Добро пожаловать в чат-бот поддержки {cfg.shop.BRAND_NAME}! \n - Для выхода введите 'выход'.")
        logger.info("=== New session ===")

        while True:
            try:
                user_text = input("Вы: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nБот: Завершение работы.")
                break
            if not user_text:
                continue

            logger.info("User: %s", user_text)

            msg = user_text.lower()
            if msg in ("выход", "стоп", "конец"):
                print("Бот: До свидания!")
                logger.info("Пользователь завершил сессию. Сессия окончена.")
                break
            if msg == "сброс":
                if session_id in self.conversation_history:
                    del self.conversation_history[session_id]
                print("Бот: Контекст диалога очищен.")
                logger.info("Пользователь сбросил контекст.")
                continue

            # Проверка команды /order
            order_match = re.match(r"^/order\s+(\d+)$", msg.strip())
            if order_match:
                order_id = order_match.group(1)
                response = get_order_status(order_id)
                print(f"Бот: {response}")
                logger.info("Пользователь: %s. Бот: %s", msg, response)
                continue

            # Поиск в FAQ
            faq_response = find_faq_answer(msg)
            if faq_response:
                print(f"Бот: {faq_response}")
                # Логируем запрос и ответ из FAQ
                logger.info("Пользователь: %s. Бот: %s", msg, faq_response)
                continue

            try:
                responce = self.chain_with_history.invoke(
                    {"question": user_text},
                    {"configurable": {"session_id": session_id}}
                )
            except Exception as e:
                # Логируем и выводим ошибку, продолжаем чат
                logger.error("[error] %e", e)
                print(f"[Ошибка] {e}")
                continue

            # Форматируем и выводим ответ
            bot_reply = responce.content.strip()
            logger.info(f"Bot: {bot_reply}")
            print(f"Бот: {bot_reply}")