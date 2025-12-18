from src.bot.cli_bot import CLIBot
from src.config.config import settings as cfg


def main():
    system_prompt = '''Ты бот поддержки магазина «Shoply», который
                        ведёт диалог с историей, отвечает кратко и по делу;
                        использует внутренний FAQ (JSON) для типовых вопросов;
                        по команде /order (номер заказа) подтягивает статус из orders.json;'''

    bot = CLIBot(
        system_prompt=system_prompt
    )
    bot("user")