from aiogram.types import Message

from bot.data.redis.models.publications import PublicationModel
from bot.ui.res.strings import Strings


def format_text_with_html_entities(message: Message) -> str:
    """
    Оборачивает элементы текста в HTML теги.
    :param message:
    :return: Отформатированный текст.
    """
    entities = {
        "italic": "<i>{}</i>",
        "bold": "<b>{}</b>",
        "code": "<code>{}</code>",
        "text_link": "<a href={}>{}</a>"
    }

    text = message.text
    formatted_text = ""
    previous_index = 0
    previous_element = ""
    previous_start, previous_end = 0, 0

    for entity in message.entities:
        if entity.type not in entities:
            continue

        start, end = entity.offset, entity.offset + entity.length

        # Проверка, если текущий элемент похож на предыдущий (более одного тега у одного элемента).
        is_same = start == previous_start and end == previous_end
        element = previous_element if is_same else text[start:end]

        # Форматирование элемента.
        if entity.type == "text_link" and hasattr(entity, "url"):
            formatted_element = entities[entity.type].format(entity.url, element)
        else:
            formatted_element = entities[entity.type].format(element)

        # Добавление элемента в текст.
        prefix = formatted_text + text[previous_index:start]
        if is_same:
            prefix = formatted_text[:start] + text[previous_index:start]
        formatted_text = prefix + formatted_element

        # Обновление предыдущих индексов.
        previous_index = previous_index if is_same else start + len(element)
        previous_element = formatted_element
        previous_start, previous_end = start, end

    formatted_text += text[previous_index:]
    return formatted_text


def format_text(message: Message, bolditalic: bool = False) -> str:
    """
    Форматирует текст, если в нем присутствуют HTML теги.
    :param message:
    :param bolditalic:
    :return:
    """
    text = message.text
    if message.entities:
        text = format_text_with_html_entities(message)

    if bolditalic:
        text = f"<b><i>{text}</i></b>"
    return text


def generate_text_upcoming_publications(publications: tuple[PublicationModel]):
    text = ""
    for num, publication in enumerate(publications, 1):
        print(num, publication)

