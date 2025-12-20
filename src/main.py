from src.bot.cli_bot import CLIBot


def main():
    system_prompt = '''Ты бот поддержки магазина «Shoply», который
                        ведёт диалог с историей, отвечает кратко и по делу;
                        использует внутренний FAQ (JSON) для типовых вопросов;
                        по команде /order (номер заказа) подтягивает статус из orders.json;'''

    bot = CLIBot(
        system_prompt=system_prompt
    )
    bot(system_prompt)

if __name__ == '__main__':
    main()