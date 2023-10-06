from aiogram.types import Message

from bot.data.redis.models.publications import PublicationModel
from bot.ui.res.strings import Strings
from bot.mics.date_formatting import unix_timestamp_to_datetime

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


def generate_text_list_of_publications(publications: tuple[PublicationModel]):
    texts = [
        Strings.elem_of_list_of_publications.format(
            roman_num=roman(num),
            publication_title=publication.publication_title,
            publication_at=unix_timestamp_to_datetime(publication.publication_at))
        for num, publication in enumerate(publications, 1)
    ]
    return "".join(texts)


def roman(num: int) -> str:

    chlist = "VXLCDM"
    rev = [int(ch) for ch in reversed(str(num))]
    chlist = ["I"] + [chlist[i % len(chlist)] + "\u0304" * (i // len(chlist)) for i in range(0, len(rev) * 2)]

    def period(p: int, ten: str, five: str, one: str) -> str:
        if p == 9:
            return one + ten
        elif p >= 5:
            return five + one * (p - 5)
        elif p == 4:
            return one + five
        else:
            return one * p

    return "".join(reversed([period(rev[i], chlist[i * 2 + 2], chlist[i * 2 + 1], chlist[i * 2])
                            for i in range(0, len(rev))]))
