from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.data.redis.queries import RedisQueries
from bot.mics.text_formatting import format_text_with_html_entities
from bot.ui.res.strings import Strings
from bot.ui.keyboards.inline_markups import NewPublicationInlineMarkups
from bot.ui.states.state_machine import NewPublicationStates


router = Router()


@router.message(NewPublicationStates.publication_text)
async def publication_text_entry(message: Message, state: FSMContext, redis: RedisQueries) -> None:
    """
    Третий - это текст публикации.
    Пользователь отправляет текст, а после может редактировать его.
    :param message:
    :param state:
    :param redis:
    :return:
    """
    text = message.text
    if message.entities:
        text = format_text_with_html_entities(message)

    model = await redis.get_new_publication()
    model.text = text
    model.message_id = message.message_id
    await redis.save_new_publication(model)

    await message.answer(
        Strings.editing_publication_text,
        reply_markup=NewPublicationInlineMarkups.editing_publication_text())
    await state.set_state(NewPublicationStates.editing_publication_text)


@router.edited_message(NewPublicationStates.editing_publication_text)
async def editing_publication_text(message: Message, redis: RedisQueries) -> None:
    """
    Обрабатывает изменение сообщения, отправленного только на предыдущем шаге.
    :param message:
    :param redis:
    :return:
    """
    model = await redis.get_new_publication()
    if message.message_id != model.message_id:
        return

    text = message.text
    if message.entities:
        text = format_text_with_html_entities(message)

    model.text = text
    await redis.save_new_publication(model)
