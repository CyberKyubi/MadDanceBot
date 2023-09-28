from aiogram.types import Message


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

    for entity in message.entities:
        if entity.type in entities:
            start, end = entity.offset, entity.offset + entity.length
            element = text[start:end]
            if entity.type == "text_link" and hasattr(entity, "url"):
                formatted_element = entities[entity.type].format(entity.url, element)
            else:
                formatted_element = entities[entity.type].format(element)
            formatted_text = formatted_text + text[previous_index:start] + formatted_element
            previous_index = start + len(element)

    formatted_text = formatted_text + text[previous_index:]
    return formatted_text


def format_text(message: Message) -> str:
    """
    Форматирует текст, если в нем присутствуют HTML теги.
    :param message:
    :return:
    """
    text = message.text
    if message.entities:
        text = format_text_with_html_entities(message)
    return text

