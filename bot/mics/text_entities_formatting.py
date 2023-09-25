from aiogram.types import Message


def text_entities_formatting(message: Message):
    entities = {
        "italic": "<i>%s</i>",
        "bold": "<b>%s</b>",
        "code": "<code>%s</code>",
        "text_link": "<a href=%s>%s</a>"
    }

    text = message.text
    new_text = ""
    previous_index = 0

    for entity in message.entities:
        start, end = entity.offset, entity.offset + entity.length
        if entity.type in entities:
            old_element = text[start:end]
            print(old_element)
            print(text[previous_index:])



            if entity.url:
                new_element = entities[entity.type] % (entity.url, old_element)
            else:
                new_element = entities[entity.type] % old_element

            new_text = new_text + text[previous_index:] + new_element
            previous_index = start + len(new_element)


    return new_text
