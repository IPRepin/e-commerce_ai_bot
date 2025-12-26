import json

from src.utils.logger import logger
from config.config import settings as cfg


def load_data(file_path: str):
    """Загружает JSON-данные из файла."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError as err:
        logger.error("Файл %s не найден", file_path)
        raise err
    except json.JSONDecodeError as err:
        logger.error("Файл %s содержит некорректный JSON.", file_path)
        raise err


def find_faq_answer(question):
    """Поиск ответа в FAQ по частичному совпадению."""
    faq_list = load_data(cfg.data.FAQ_PATH)
    question_lower = question.lower().strip()
    for item in faq_list:
        if item["q"].lower() in question_lower or question_lower in item["q"].lower():
            return item["a"]
    return None


def get_order_status(order_id):
    """Получает статус заказа по ID."""
    orders = load_data(cfg.data.ORDERS_PATH)
    order_info = orders.get(str(order_id))
    if order_info:
        status = order_info["status"]
        if status == "in_transit":
            eta = order_info.get("eta_days", "?")
            carrier = order_info.get("carrier", "неизвестно")
            return f"Заказ в пути. Прибывает через ~{eta} дн. Перевозчик: {carrier}."
        elif status == "delivered":
            delivered_at = order_info.get("delivered_at", "неизвестно")
            return f"Заказ доставлен. Дата доставки: {delivered_at}."
        elif status == "processing":
            note = order_info.get("note", "")
            return f"Заказ обрабатывается. {note}"
        else:
            return f"Заказ в статусе: {status}."
    else:
        return "Заказ с таким ID не найден."
